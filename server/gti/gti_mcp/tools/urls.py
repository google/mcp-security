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
) -> typing.Dict[str, typing.Any]:
  """Retrieve entities related to the the given URL.

    The following table shows a summary of available relationships for URL objects.

    | Relationship            | Description                                                    | Return type  |
    | ----------------------- | -------------------------------------------------------------- | ------------ | 
    | analyses                | Analyses for the URL.                                          | analyse      |
    | associations            | URL's associated objects (reports, campaigns, IoC collections, malware families, software toolkits, vulnerabilities, threat-actors), without filtering by the associated object type. | collection |
    | campaigns               | Campaigns associated to the URL.                               | collection   |
    | collections             | IoC Collections associated to the URL.                         | collection   |
    | comments                | Community posted comments about the URL.                       | comment      |
    | communicating_files     | Files that communicate with a given URL when they're executed. | file         |
    | contacted_domains       | Domains from which the URL loads some kind of resource.        | domain       |
    | contacted_ips           | IPs from which the URL loads some kind of resource.            | ip_address   |
    | downloaded_files        | Files downloaded from the URL.                                 | file         |
    | embedded_js_files       | JS files embedded in a URL.                                    | file         |
    | graphs                  | Graphs including the URL.                                      | graph        |
    | http_response_contents  | HTTP response contents from the URL.                           | file         |
    | last_serving_ip_address | Last IP address that served the URL.                           | ip_address   |
    | malware_families        | Malware families associated to the URL.                        | collection   |
    | memory_pattern_parents  | Files having a domain as string on memory during sandbox execution. | file    |
    | network_location        | Domain or IP for the URL.                                      | domain or ip_address |
    | parent_resource_urls    | Returns the URLs where this URL has been loaded as resource.   | url          |
    | redirecting_urls        | URLs that redirected to the given URL.                         | url          |
    | redirects_to            | URLs that this url redirects to.                               | url          |
    | referrer_files          | Files containing the URL.                                      | file         |
    | referrer_urls           | URLs referring the URL.                                        | url          |
    | related_collections     | Returns the Collections of the parent Domains or IPs of this URL. | collection  |
    | related_comments        | Community posted comments in the URL's related objects.        | comment      |
    | related_reports         | Reports that are directly and indirectly related to the URL.   | collection   |
    | related_threat_actors   | URL's related threat actors.                                   | collection   |
    | reports                 | Reports directly associated to the URL.                        | collection   |
    | software_toolkits       | Software and Toolkits associated to the URL.                   | collection   |
    | submissions             | URL's submissions.                                             | url          |
    | urls_related_by_tracker_id | URLs that share the same tracker ID.                        | url          |
    | user_votes          | URL's votes made by current signed-in user.                        | vote         |
    | votes                  | Votes for the URL.                                              | vote         |
    | vulnerabilities        | Vulnerabilities associated to the URL.                          | collection   |

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
