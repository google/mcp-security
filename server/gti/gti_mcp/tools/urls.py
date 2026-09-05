# Copyright 2026 Google LLC
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
import base64
import typing

from mcp.server.fastmcp import Context

from .. import utils
from ..server import server, vt_client


URL_RELATIONSHIPS = [
    "analyses",
    "associations",
    "campaigns",
    "collections",
    "comments",
    "communicating_files",
    "contacted_domains",
    "contacted_ips",
    "downloaded_files",
    "embedded_js_files",
    "graphs",
    "http_response_contents",
    "last_serving_ip_address",
    "malware_families",
    "memory_pattern_parents",
    "network_location",
    "parent_resource_urls",
    "redirecting_urls",
    "redirects_to",
    "referrer_files",
    "referrer_urls",
    "related_collections",
    "related_comments",
    "related_reports",
    "related_threat_actors",
    "reports",
    "software_toolkits",
    "submissions",
    "urls_related_by_tracker_id",
    "user_votes",
    "votes",
    "vulnerabilities",
]

URL_KEY_RELATIONSHIPS = [
    "associations",
]


def url_to_base64(url: str) -> str:
  """Converts the URL into base64.

  Without padding, as required by the Google Threat Intelligence API.
  """
  b = base64.b64encode(url.encode('utf-8'))
  return b.decode('utf-8').rstrip("=")


@server.tool()
async def get_url_report(url: str, ctx: Context) -> typing.Dict[str, typing.Any]:
  """Get a comprehensive URL analysis report from Google Threat Intelligence.

  Args:
    url (required): URL to analyse.
  Returns:
    Report with insights about the URL.
  """
  url_id = url_to_base64(url)
  async with vt_client(ctx) as client:
    res = await utils.fetch_object(
        client,
        "urls",
        "url",
        url_id,
        relationships=["associations"],
        params={"exclude_attributes": "last_analysis_results"})
  return utils.sanitize_response(res)


@server.tool()
async def get_entities_related_to_an_url(
    url: str, relationship_name: str, descriptors_only: bool, ctx: Context, limit: int = 10
) -> list[dict[str, typing.Any]]:
  """Retrieve entities related to the given URL.

  Available relationships: analyses, associations, campaigns, collections, comments,
  communicating_files, contacted_domains, contacted_ips, downloaded_files, embedded_js_files,
  last_serving_ip_address, malware_families, parent_resource_urls, redirects_to, referrer_files,
  referrer_urls.

  Args:
    url (required): URL to analyse.
    relationship_name (required): Relationship name.
    descriptors_only (required): Bool. Must be True when the target object type is one of file, domain, url, ip_address or collection.
    limit: Limit the number of objects to retrieve. 10 by default.
  Returns:
    List of entities related to the URL.
  """
  if not relationship_name in URL_RELATIONSHIPS:
    return {
       "error": f"Relationship {relationship_name} does not exist. "
                f"Available relationships are: {','.join(URL_RELATIONSHIPS)}"
    }

  url_id = url_to_base64(url)
  async with vt_client(ctx) as client:
    res = await utils.fetch_object_relationships(
        client,
        "urls", 
        url_id,
        relationships=[relationship_name],
        descriptors_only=descriptors_only,
        limit=limit)
  return utils.sanitize_response(res.get(relationship_name, []))
