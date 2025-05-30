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

import typing

from mcp.server.fastmcp import Context

from .. import utils
from ..server import server, vt_client


COLLECTION_RELATIONSHIPS = [
    "associations",
    "attack_techniques",
    "domains",
    "files",
    "ip_addresses",
    "urls",
    "threat_actors",
    "malware_families",
    "software_toolkits",
    "campaigns",
    "vulnerabilities",
    "reports",
    "suspected_threat_actors",
    "hunting_rulesets",
]

COLLECTION_KEY_RELATIONSHIPS = [
    "associations",
]
COLLECTION_EXCLUDED_ATTRS = ",".join(["aggregations"])

COLLECTION_TYPES = {
    "threat-actor",
    "malware-family",
    "campaign",
    "report",
    "software-toolkit",
    "vulnerability",
    "collection",
}


@server.tool()
async def get_collection_report(id: str, ctx: Context) -> typing.Dict[str, typing.Any]:
  """At Google Threat Intelligence, threats are modeled as "collections". This tool retrieves them from the platform.

  They have different collections types like: 
    - "malware-family"
    - "threat-actor"
    - "campaign"
    - "report"
    - "collection". 

  You can find the collection type in the "collection_type" field.

  Args:
    id (required): Google Threat Intelligence identifier.
  Returns:
    A collection object. Put attention to the collection type to correctly understand what it represents.
  """
  async with vt_client(ctx) as client:
    res = await utils.fetch_object(
        client,
        "collections",
        "collection",
        id,
        relationships=COLLECTION_KEY_RELATIONSHIPS,
        params={"exclude_attributes": COLLECTION_EXCLUDED_ATTRS})
  return res


@server.tool()
async def get_entities_related_to_a_collection(
    id: str, relationship_name: str, descriptors_only: bool, ctx: Context, limit: int = 10
) -> typing.Dict[str, typing.Any]:
  """Retrieve entities related to the the given collection ID.

    The following table shows a summary of available relationships for collection objects.

    | Relationship         | Description                                       | Return type  |
    | -------------------- | ------------------------------------------------- | ------------ |
    | associations         | List of associated threats                        | collection   |
    | attack_techniques    | List of attack techniques                         | attack_technique |
    | domains              | List of Domains                                   | domain       |
    | files                | List of Files                                     | file         |
    | ip_addresses         | List of IP addresses                              | ip_address   |
    | urls                 | List of URLs                                      | url          |
    | threat_actors        | List of related threat actors                     | collection   |
    | malware_families     | List of related malware families                  | collection   |
    | software_toolkits    | List of related tools                             | collection   |
    | campaigns            | List of related campaigns                         | collection   |
    | vulnerabilities      | List of related vulnerabilities                   | collection   |
    | reports              | List of reports                                   | collection   |
    | suspected_threat_actors | List of related suspected threat actors        | collection   |
    | hunting_rulesets     | Google Threat Intelligence Yara rules that identify the given collection | hunting_ruleset |

    Args:
      id (required): Collection identifier.
      relationship_name (required): Relationship name.
      descriptors_only (required): Bool. Must be True when the target object type is one of file, domain, url, ip_address or collection.
      limit: Limit the number of collections to retrieve. 10 by default.
    Returns:
      List of objects related to the collection.
  """
  if not relationship_name in COLLECTION_RELATIONSHIPS:
      return {
          "error": f"Relationship {relationship_name} does not exist. "
          f"Available relationships are: {','.join(COLLECTION_RELATIONSHIPS)}"
      }
  async with vt_client(ctx) as client:
    res = await utils.fetch_object_relationships(
        client, 
        "collections", 
        id, 
        [relationship_name],
        descriptors_only=descriptors_only,
        limit=limit)
  return utils.sanitize_response(res.get(relationship_name, []))


async def _search_threats_by_collection_type(
    query: str,
    collection_type: str,
    ctx: Context,
    limit: int = 10,
    order_by: str = "relevance-",
) -> typing.List[typing.Dict[str, typing.Any]]:
  """Search a given threat type in the Google Threat Intelligence platform,

  Args:
    query (required): Search query to find threats. If you want any threat, just pass an empty string.
    collection_type (required): Collection type. One of: "threat-actor", "malware-family", "campaign", "report", "vulnerability", "collection".
    limit: Limit the number of threats to retrieve. 10 by default.
    order_by: Order results by the given order key. "relevance-" by default.

  Returns:
    List of collections, aka threats.
  """
  if collection_type not in COLLECTION_TYPES:
      raise ValueError(
          f"wrong collection_type. Available collection_type are: {','.join(COLLECTION_TYPES)} ")

  async with vt_client(ctx) as client:
    res = await utils.consume_vt_iterator(
        client,
        "/collections",
        params={
            "filter": f"collection_type:{collection_type} {query}",
            "order": order_by,
            "relationships": COLLECTION_KEY_RELATIONSHIPS,
            "exclude_attributes": COLLECTION_EXCLUDED_ATTRS,
        },
        limit=limit,
    )
  return utils.sanitize_response([o.to_dict() for o in res])


@server.tool()
async def search_threats(
    ctx: Context,
    query: str,
    collection_type: str = None,
    limit: int = 5,
    order_by: str = "relevance-",
) -> typing.List[typing.Dict[str, typing.Any]]:
  """Search threats in the Google Threat Intelligence platform.

  Threats are modeled as collections. Once you get collections from this tool, you can use `get_collection_report` to fetch the full reports and their relationships.

  **IMPORTANT CONTEXT CLUE:** Pay close attention to the user's request. If their request mentions specific *kinds* of threats such as "threat actor", "malware family", "campaign", "report", or "vulnerability", treat this as a strong signal that you **must** use the `collection_type` filter in your `query` to ensure relevant results. Using this filter significantly improves search precision.

  **Filtering by Type:**
  To filter your search results to a specific *type* of threat, include the `collection_type` modifier *within your query string*.
  Syntax: `collection_type:"<type>"`
  Available `<type>` values:
    - "threat-actor": Use when the user asks about specific actors, groups, or APTs.
    - "malware-family": Use when the user asks about malware, trojans, viruses, ransomware families.
    - "software-toolkit": Use when the user asks about legit tools usually related to malware.
    - "campaign": Use when the user asks about specific attack campaigns.
    - "report": Use when the user is looking for analysis reports.
    - "vulnerability": Use when the user asks about specific CVEs or vulnerabilities.
    - "collection": A generic type, use only if no other type fits or if the user explicitly asks for generic "collections".

  You can use order_by to sort the results by: "relevance", "creation_date". You can use the sign "+" to make it order ascending, or "-" to make it descending. By default is "relevance-"

  When asked for latest threats, prioritize campaigns or vulnerabilities over reports.

  Args:
    query (required): Search query to find threats.
    collection_type: Filter your search results to a specific *type* of threat
    limit: Limit the number of threats to retrieve. 5 by default.
    order_by: Order results by the given order key. "relevance-" by default.

  Returns:
    List of collections, aka threats. They are full collection objects, you do not need to retrieve them`using the `get_collection_report` tool. You may need to extend with relationships using `get_entities_related_to_a_collection` tool.
  """
  filter = ""
  if collection_type:
    if collection_type not in COLLECTION_TYPES:
      raise ValueError(
          f"unknown collection_type. Available are {','.join(COLLECTION_TYPES)}")
    filter += f"collection_type:{collection_type} "
  if query:
    filter += query
  
  async with vt_client(ctx) as client:
    res = await utils.consume_vt_iterator(
        client,
        "/collections",
        params={
            "filter": filter,
            "order": order_by,
            "relationships": COLLECTION_KEY_RELATIONSHIPS,
            "exclude_attributes": COLLECTION_EXCLUDED_ATTRS,
        },
        limit=limit,
    )
  res = utils.sanitize_response([o.to_dict() for o in res])
  return res


@server.tool()
async def search_campaigns(
    query: str, ctx: Context, limit: int = 10, order_by: str = "relevance-"
) -> typing.List[typing.Dict[str, typing.Any]]:
  """Search threat campaigns in the Google Threat Intelligence platform.

  Campaigns are modeled as collections. Once you get collections from this tool, you can use `get_collection_report` to fetch the full reports and their relationships.

  You can use order_by to sort the results by: "relevance", "creation_date". You can use the sign "+" to make it order ascending, or "-" to make it descending. By default is "relevance-"

  Args:
    query (required): Search query to find threats.
    limit: Limit the number of threats to retrieve. 10 by default.
    order_by: Order results by the given order key. "relevance-" by default.

  Returns:
    List of collections, aka threats.
  """
  res = await _search_threats_by_collection_type(
      query, "campaign", ctx, limit, order_by)
  return res


@server.tool()
async def search_threat_actors(
    query: str, ctx: Context, limit: int = 10, order_by: str = "relevance-"
) -> typing.List[typing.Dict[str, typing.Any]]:
  """Search threat actors in the Google Threat Intelligence platform.

  Threat actors are modeled as collections. Once you get collections from this tool, you can use `get_collection_report` to fetch the full reports and their relationships.

  You can use order_by to sort the results by: "relevance", "creation_date". You can use the sign "+" to make it order ascending, or "-" to make it descending. By default is "relevance-"

  Args:
    query (required): Search query to find threats.
    limit: Limit the number of threats to retrieve. 10 by default.
    order_by: Order results by the given order key. "relevance-" by default.

  Returns:
    List of collections, aka threats.
  """
  res = await _search_threats_by_collection_type(
      query, "threat-actor", ctx, limit, order_by)
  return res


@server.tool()
async def search_malware_families(
    query: str, ctx: Context, limit: int = 10, order_by: str = "relevance-"
) -> typing.List[typing.Dict[str, typing.Any]]:
  """Search malware families in the Google Threat Intelligence platform.

  Malware families are modeled as collections. Once you get collections from this tool, you can use `get_collection_report` to fetch the full reports and their relationships.

  You can use order_by to sort the results by: "relevance", "creation_date". You can use the sign "+" to make it order ascending, or "-" to make it descending. By default is "relevance-"

  Args:
    query (required): Search query to find threats.
    limit: Limit the number of threats to retrieve. 10 by default.
    order_by: Order results by the given order key. "relevance-" by default.

  Returns:
    List of collections, aka threats.
  """
  res = await _search_threats_by_collection_type(
      query, "malware-family", ctx, limit, order_by)
  return res


@server.tool()
async def search_software_toolkits(
    query: str, ctx: Context, limit: int = 10, order_by: str = "relevance-"
) -> typing.List[typing.Dict[str, typing.Any]]:
  """Search software toolkits (or just tools) in the Google Threat Intelligence platform.

  Software toolkits are modeled as collections. Once you get collections from this tool, you can use `get_collection_report` to fetch the full reports and their relationships.

  You can use order_by to sort the results by: "relevance", "creation_date". You can use the sign "+" to make it order ascending, or "-" to make it descending. By default is "relevance-"

  Args:
    query (required): Search query to find threats.
    limit: Limit the number of threats to retrieve. 10 by default.
    order_by: Order results by the given order key. "relevance-" by default.

  Returns:
    List of collections, aka threats.
  """
  res = await _search_threats_by_collection_type(
      query, "software-toolkit", ctx, limit, order_by)
  return res


@server.tool()
async def search_threat_reports(
    query: str, ctx: Context, limit: int = 10, order_by: str = "relevance-"
) -> typing.List[typing.Dict[str, typing.Any]]:
  """Search threat reports in the Google Threat Intelligence platform.

  Google Threat Intelligence provides continuously updated reports and analysis of threat actors, campaigns, vulnerabilities, malware, and tools

  Threat reports are modeled as collections. Once you get collections from this tool, you can use `get_collection_report` to fetch the full reports and their relationships.

  You can use order_by to sort the results by: "relevance", "creation_date". You can use the sign "+" to make it order ascending, or "-" to make it descending. By default is "relevance-"

  Args:
    query (required): Search query to find threats.
    limit: Limit the number of threats to retrieve. 10 by default.
    order_by: Order results by the given order key. "relevance-" by default.

  Returns:
    List of collections, aka threats.
  """
  res = await _search_threats_by_collection_type(
      query, "report", ctx, limit, order_by)
  return res


@server.tool()
async def search_vulnerabilities(
    query: str, ctx: Context, limit: int = 10, order_by: str = "relevance-"
) -> typing.List[typing.Dict[str, typing.Any]]:
  """Search vulnerabilities (CVEs) in the Google Threat Intelligence platform.

  Vulnerabilities are modeled as collections. Once you get collections from this tool, you can use `get_collection_report` to fetch the full reports and their relationships.

  You can use order_by to sort the results by: "relevance", "creation_date". You can use the sign "+" to make it order ascending, or "-" to make it descending. By default is "relevance-"

  Args:
    query (required): Search query to find threats.
    limit: Limit the number of threats to retrieve. 10 by default.
    order_by: Order results by the given order key. "relevance-" by default.

  Returns:
    List of collections, aka threats.
  """
  res = await _search_threats_by_collection_type(
      query, "vulnerability", ctx, limit, order_by)
  return res


@server.tool()
async def get_collection_timeline_events(id: str, ctx: Context):
  """Retrieves timeline events from the given collection, when available.

  This is super valuable curated information produced by security analysits at Google Threat Intelligence.

  We should fetch this information for campaigns and threat actors always.

  It's common to display the events grouped by the "event_category" field.

  Args:
    id (required): Collection identifier
  Return:
    List of events related to the given collection.
  """
  async with vt_client(ctx) as client:
    data = await client.get_async(f"/collections/{id}/timeline/events")
    data = await data.json_async()
  return utils.sanitize_response(data["data"])


@server.tool()
async def get_collection_mitre_tree(id: str, ctx: Context) -> typing.Dict:
  """Retrieves the Mitre tactics and techniques associated with a threat.

  Args:
    id (required): Collection identifiers.
  Return:
    A dictionary including the tactics and techniques associated to the given threat.
  """
  async with vt_client(ctx) as client:
    data = await client.get_async(f"/collections/{id}/mitre_tree")
    data = await data.json_async()
  return utils.sanitize_response(data["data"])

