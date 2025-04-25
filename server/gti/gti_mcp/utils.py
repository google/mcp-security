# Copyright 2025 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
import asyncio
import logging
import vt
import typing


async def consume_vt_iterator(vt_client: vt.Client, endpoint: str, params: dict | None, limit: int = 10):
  """Consumes a vt.Iterator iterator and return the list of objects."""
  res = []
  async for obj in vt_client.iterator(endpoint, params=params, limit=limit):
    res.append(obj)
  return res


async def fetch_object(
    vt_client: vt.Client,
    resource_collection_type: str,
    resource_type: str,
    resource_id: str,
    attributes: list[str] | None = None,
    relationships: list[str] | None = None,
    params: dict[str, typing.Any] | None = None):
  """Fetches objects from Google Threat Intelligence API."""
  logging.info(
      f"Fetching comprehensive {resource_collection_type} "
      f"report for id: {resource_id}")
  
  params = {k: v for k, v in params.items()} if params else {}

  # Retrieve a selection of object attributes and/or relationships.
  if attributes:
    params["attributes"] = ",".join(attributes)
  if relationships:
    params["relationships"] = ",".join(relationships)

  obj = await vt_client.get_object_async(
      f"/{resource_collection_type}/{resource_id}", params=params)

  if obj.error:
    logging.error(
        f"Error fetching main {resource_type} report for {resource_id}: {obj.error}"
    )
    return {
        "error": f"Failed to get main {resource_type} report: {obj.error}",
        # "details": report.get("details"),
    }

  # Build response.
  obj_dict = obj.to_dict()
  obj_dict['id'] = obj.id
  if 'aggregations' in obj_dict['attributes']:
    del obj_dict['attributes']['aggregations']

  logging.info(
      f"Successfully generated concise threat summary for id: {resource_id}")
  return obj_dict


async def fetch_object_relationships(
    vt_client: vt.Client,
    resource_collection_type: str,
    resource_id: str,
    relationships: typing.List[str],
    params: dict[str, typing.Any] | None = None):
  """Fetches the given relationships descriptors from the given object."""
  rel_futures = {}
  async with asyncio.TaskGroup() as tg:
    for rel_name in relationships:
      rel_futures[rel_name] = tg.create_task(
          consume_vt_iterator(
              vt_client,
              f"/{resource_collection_type}/{resource_id}"
              f"/relationship/{rel_name}", params=params))

  data = {}
  for name, items in rel_futures.items():
    data[name] = []
    for obj in items.result():
      obj_dict = obj.to_dict()
      if 'aggregations' in obj_dict['attributes']:
        del obj_dict['attributes']['aggregations']
      data[name].append(obj_dict)

  return data
