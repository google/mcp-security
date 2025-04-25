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
  res = await utils.fetch_object(
      vt_client(ctx),
      "urls",
      "url",
      url_id,
      ["associations"],
      params={"exclude_attributes": "last_analysis_results"})
  return res


@server.tool()
async def get_entities_related_to_an_url(url: str, relationship_name: str, ctx: Context) -> typing.Dict[str, typing.Any]:
  """Retrieve entities related to the the given URL.

    The following table shows a summary of available relationships for URL objects.

    | Relationship            | Description                                                    |
    | :---------------------- | :------------------------------------------------------------- |
    | analyses                | Analyses for the URL.                                          |
    | associations            | URL's associated objects (reports, campaigns, IoC collections, malware families, software toolkits, vulnerabilities, threat-actors), without filtering by the associated object type. |
    | campaigns               | Campaigns associated to the URL.                               |
    | collections             | IoC Collections associated to the URL.                         |
    | comments                | Community posted comments about the URL.                       |
    | communicating_files     | Files that communicate with a given URL when they're executed. |
    | contacted_domains       | Domains from which the URL loads some kind of resource.        |
    | contacted_ips           | IPs from which the URL loads some kind of resource.            |
    | downloaded_files        | Files downloaded from the URL.                                 |
    | embedded_js_files       | JS files embedded in a URL.                                    |
    | graphs                  | Graphs including the URL.                                      |
    | http_response_contents                  | TTP response contents from the URL.            |
    | last_serving_ip_address | Last IP address that served the URL.                           |
    | malware_families        | Malware families associated to the URL.                        |
    | memory_pattern_parents        | Files having a domain as string on memory during sandbox execution.                                |
    | network_location        | Domain or IP for the URL.                                      |
    | parent_resource_urls           | Returns the URLs where this URL has been loaded as resource.                                        |
    | redirecting_urls           | URLs that redirected to the given URL.                      |
    | redirects_to           | URLs that this url redirects to.                                |
    | referrer_files          | Files containing the URL.                                      |
    | referrer_urls           | URLs referring the URL.                                        |
    | related_collections        | Returns the Collections of the parent Domains or IPs of this URL.        |
    | related_comments        | Community posted comments in the URL's related objects.        |
    | related_reports    | Reports that are directly and indirectly related to the URL.        |
    | related_threat_actors    | URL's related threat actors.                                  |
    | reports                 | Reports directly associated to the URL.                        |
    | software_toolkits       | Software and Toolkits associated to the URL.                   |
    | submissions             | URL's submissions.                                             |
    | urls_related_by_tracker_id           | URLs that share the same tracker ID.              |
    | user_votes          | URL's votes made by current signed-in user.                        |
    | votes                  | Votes for the URL.                                              |
    | vulnerabilities        | Vulnerabilities associated to the URL.                          |

    Args:
      url (required): URL to analyse.
    Returns:
      List of entities related to the URL.
  """
  if not relationship_name in URL_RELATIONSHIPS:
    return {
       "error": f"Relationship {relationship_name} does not exist. "
                f"Available relationships are: {','.join(URL_RELATIONSHIPS)}"
    }

  url_id = url_to_base64(url)
  res = await utils.fetch_object_relationships(
      vt_client(ctx), "urls", url_id, [relationship_name])
  return res.get(relationship_name, [])
