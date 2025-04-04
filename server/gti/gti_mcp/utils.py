import asyncio
import logging
import vt
import typing


async def consume_vt_iterator(vt_client: vt.Client, endpoint: str, params: dict = None, limit: int = 10):
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
    relationships: typing.List[str]):
  """Fetches objects from Google Threat Intelligence API."""
  logging.info(
      f"Fetching comprehensive {resource_collection_type} "
      f"report for id: {resource_id}")

  obj = await vt_client.get_object_async(
      f"/{resource_collection_type}/{resource_id}")

  if obj.error:
    logging.error(
        f"Error fetching main {resource_type} report for {resource_id}: {obj.error}"
    )
    return {
        "error": f"Failed to get main {resource_type} report: {obj.error}",
        # "details": report.get("details"),
    }

  # # Create a concise summary of key threat details
  threat_summary = obj.to_dict()
  threat_summary["relationships"] = await fetch_object_relationships(
      vt_client, resource_collection_type, resource_id, relationships)  

  logging.info(
      f"Successfully generated concise threat summary for id: {resource_id}")
  return threat_summary


async def fetch_object_relationships(
    vt_client: vt.Client, resource_collection_type: str, resource_id: str, relationships: typing.List[str]):
  """Fetches the given relationships from the given object."""
  rel_futures = {}
  async with asyncio.TaskGroup() as tg:
    for rel_name in relationships:
      rel_futures[rel_name] = tg.create_task(
          consume_vt_iterator(
              vt_client, 
              f"/{resource_collection_type}/{resource_id}/{rel_name}"))
      
  data = {}
  for name, items in rel_futures.items():
    data[name] = items.result()

  return data
