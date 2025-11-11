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
import logging

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
    id: str, relationship_name: str, ctx: Context, limit: int = 10, descriptors_only: bool = True
) -> typing.List[typing.Dict[str, typing.Any]]:
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

    Note on descriptors_only: When True, returns basic descriptors. When False, returns
    detailed attributes.
    IMPORTANT: `descriptors_only` must be `False` for the 'attack_techniques' relationship.
    
    Args:
      id (required): Collection identifier.
      relationship_name (required): Relationship name.
      limit (optional): Limit the number of collections to retrieve. 10 by default.
      descriptors_only (optional)): Bool. Default True. Must be False when the target object type is 'attack_techniques'.
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
  return utils.sanitize_response([o.to_dict() for o in res])


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


@server.tool()
async def create_collection(
    name: str,
    description: str,
    iocs: typing.List[str],
    ctx: Context,
    private: bool = True,
) -> typing.Dict[str, typing.Any]:
  """Creates a new collection in Google Threat Intelligence.
      Ask for the collection's privacy (public or private) if the user doesn't specify.

  Args:
    name (required): The name of the collection.
    description (required): A description of the collection.
    iocs (required): Indicators of Compromise (IOCs) to include in the
      collection. The items in the list can be domains, files, ip_addresses, or urls.
      At least one IOC must be provided.
    private: Indicates whether the collection should be private.
  Returns:
    A dictionary representing the newly created collection.
  """
  async with vt_client(ctx) as client:
    collection_data = {
        "data": {
            "attributes": {"name": name, "description": description, "private": private},
            "type": "collection",
            "raw_items": ", ".join(iocs),
        }
    }
    
    res = await client.post_async("/collections", json_data=collection_data)
    data = await res.json_async()
  return utils.sanitize_response(data["data"])


@server.tool()
async def update_collection_attributes(
    id: str,
    ctx: Context,
    attributes: typing.Dict[str, typing.Any] = None,
) -> typing.Dict[str, typing.Any]:
  """Allows updating a collection's attributes (such as name or description)
  Args:
    id (required): The ID of the collection to update.
    attributes: Available attributes in a collection:
        *  name: string
        *  description: string
        *  private: boolean
        *  tags: array of strings
        *  alt_names: array of strings
  Returns:
    A dictionary representing the updated collection.
  """
  async with vt_client(ctx) as client:
    collection_data = {"data": {"attributes": attributes, "type": "collection"}}          

    res = await client.patch_async(
        f"/collections/{id}", json_data=collection_data
    )
    data = await res.json_async()
  return utils.sanitize_response(data["data"])


@server.tool()
async def update_iocs_in_collection(
    id: str,
    ctx: Context,
    relationship: str,
    iocs: typing.List[str],
    operation: str,
) -> str:
  """Updates (add or remove) Indicators of Compromise (IOCs) to a collection.
  Args:
    id (required): The ID of the collection to update.
    relationship (required): The type of relationship to add. Can be "domains", "files",
      "ip_addresses", or "urls".
    iocs (required): List of IOCs to add to the collection. For "urls", these
      are the full URLs. For other types, they are the identifiers (hashes for
      files, domain names for domains, etc.).
    operation (required): The operation to perform. Can be "add" or "remove".

  Returns:
    A string indicating the success or failure of the operation.
  """
  async with vt_client(ctx) as client:

    singular_type_map = {
        "domains": "domain",
        "files": "file",
        "ip_addresses": "ip_address",
        "urls": "url",
    }

    if relationship not in singular_type_map:
      return f"Error: Invalid IOC type '{relationship}'. Must be one of {list(singular_type_map.keys())}"

    singular_type = singular_type_map[relationship]

    if relationship == "urls":
      items = [{"type": singular_type, "url": ioc} for ioc in iocs]
    else:
      items = [{"type": singular_type, "id": ioc} for ioc in iocs]

    payload = {"data": items}
    if operation == "add":
      res = await client.post_async(f"/collections/{id}/{relationship}", json_data=payload)
    elif operation == "remove":
      res = await client.delete_async(f"/collections/{id}/{relationship}", json_data=payload)
    else:
      return f"Error: Invalid operation '{operation}'. Must be one of 'add' or 'remove'"

    status = res._aiohttp_resp.status
    return 'Sucesssfully updated collection' if status == 200 else 'Error updating collection'


@server.tool()
async def get_collection_feature_matches(
    collection_id: str,
    feature_type: str,
    feature_id: str,
    entity_type: str,
    search_space: str,
    entity_type_plural: str,
    ctx: Context,
    descriptors_only: bool=True,
) -> typing.List[typing.Dict[str, typing.Any]]:
  """Retrieves Indicators of Compromise (IOCs) from a collection that match a specific feature.

  This tool allows pivoting from a commonality to the specific IOCs within a collection that exhibit that feature.
  Commonalities are shared characteristics and hidden relationships between various Indicators of Compromise (e.g., files, URLs, domains, IPs).

  Available feature types by entity type:
  Files:
    - android_certificates, android_main_activities, android_package_names, attributions, behash,
      collections, compressed_parents, contacted_domains, contacted_ips, contacted_urls,
      crowdsourced_ids_results, crowdsourced_yara_results, elfhash, email_parents,
      embedded_domains, embedded_ips, embedded_urls, execution_parents, imphash,
      itw_domains, itw_urls, mutexes_created, mutexes_opened, pcap_parents,
      registry_keys_deleted, registry_keys_opened, registry_keys_set, tags, vhash, file_types,
      crowdsourced_sigma_results, deb_info_packages, debug_codeview_guids, debug_codeview_names,
      debug_timestamps, dropped_files_path, dropped_files_sha256, elfinfo_exports,
      elfinfo_imports, exiftool_authors, exiftool_companies, exiftool_create_dates,
      exiftool_creators, exiftool_last_modified, exiftool_last_printed, exiftool_producers,
      exiftool_subjects, exiftool_titles, filecondis_dhash, main_icon_dhash,
      main_icon_raw_md5, netassembly_mvid, nsrl_info_filenames, office_application_names,
      office_authors, office_creation_datetimes, office_last_saved, office_macro_names,
      permhash, pe_info_imports, pe_info_exports, pe_info_section_md5,
      pe_info_section_names, pwdinfo_values, sandbox_verdicts, signature_info_comments,
      signature_info_copyrights, signature_info_descriptions, signature_info_identifiers,
      signature_info_internal_names, signature_info_original_names, signature_info_products,
      symhash, trusted_verdict_filenames, rich_pe_header_hash, telfhash, tlshhash,
      email_senders, email_subjects, popular_threat_category, popular_threat_name,
      suggested_threat_label, attack_techniques, malware_config_family_name,
      malware_config_campaign_id, malware_config_campaign_group, malware_config_dga_seed,
      malware_config_dns_server, malware_config_service, malware_config_registry_key,
      malware_config_event, malware_config_pipe, malware_config_mutex, malware_config_folder,
      malware_config_file, malware_config_process_inject_target, malware_config_crypto_key,
      malware_config_displayed_message, malware_config_c2_url, malware_config_download_url,
      malware_config_misc_url, malware_config_decoy_url, malware_config_c2_user_agent,
      malware_config_download_user_agent, malware_config_misc_user_agent,
      malware_config_decoy_user_agent, malware_config_c2_password,
      malware_config_misc_username, malware_config_misc_password,
      malware_config_host_port, malware_config_dropped_file,
      malware_config_dropped_file_path, malware_config_registry_value,
      malware_config_download_password, malware_config_c2_username,
      malware_config_download_username, malware_config_exfiltration_username,
      malware_config_exfiltration_password, malware_config_exfiltration_url,
      malware_config_exfiltration_user_agent, malware_config_pivot_hash,
      memory_pattern_urls

  Domains:
    - attributions, collections, communicating_files, downloaded_files,
      favicon_dhash, favicon_raw_md5, urls, registrant_names

  IP Addresses:
    - attributions, collections, communicating_files, downloaded_files, urls

  URLs:
    - attributions, http_response_contents, collections, contacted_domains,
      communicating_files, cookie_names, cookie_values, downloaded_files,
      domains, embedded_js, favicon_dhash, favicon_raw_md5, html_titles,
      ip_addresses, memory_patterns, outgoing_links, path, prefix_paths,
      suffix_paths, ports, users, passwords, user_passwords, query_strings,
      query_param_keys, query_param_values, query_param_key_values,
      referring_files, tags, tracker_ids

  Args:
    collection_id (required): The ID of the collection to search within.
    feature_type (required): The type of feature to search for (e.g., 'attack_techniques').
    feature_id (required): The specific value of the feature (e.g., 'T1497.001').
    entity_type (required): 
    search_space (required): The scope of the search. Use 'collection' to search only within the specified collection, or 'corpus' to search across the entire VirusTotal dataset.
    entity_type_plural (required): The plural of 'entity_type'.
    descriptors_only (optional): Returns only the descriptors.
  Returns:
    A dictionary containing the list of matching IOCs.
  """
  async with vt_client(ctx) as client:
    params = {
        "feature_type": feature_type,
        "feature_id": feature_id,
        "entity_type": entity_type,
        "search_space": search_space,
        "type": entity_type_plural,
        "descriptors_only": str(descriptors_only).lower(),
    }
    
    response = await client.get_async(f"/collections/{collection_id}/features/search", params=params)
    data = await response.json_async()
    return utils.sanitize_response(data["data"])


@server.tool()
async def get_collections_commonalities(collection_id: str, ctx: Context) -> str:
  """Retrieve the common characteristics or features (attributes / relationships) of the indicators of compromise (IoC) within a collection, identified by its ID.
  Args:
    collection_id (required): Collection identifier.
  Returns:
    Markdown-formatted string with the commonalities of the collection.
  """
  async with vt_client(ctx) as client:
    data = await client.get_async(f"/collections/{collection_id}?attributes=aggregations")
    data = await data.json_async()
    sanitized_data = utils.sanitize_response(data["data"])
    markdown_output = utils.parse_collection_commonalities(sanitized_data)
  return markdown_output


async def _get_yara_rule_details(ctx: Context, rule: dict, rule_type: str) -> typing.Dict[str, typing.Any]:
  """Fetches details for a single YARA ruleset and formats the output."""

  ruleset_id = rule.get("value",{}).get("ruleset_id", None)
  if not ruleset_id:  
    return {"error": f"No ruleset_id found in rule"} 
  
  try:
    async with vt_client(ctx) as client:
      ruleset_resp = await client.get_async(f"/yara_rulesets/{ruleset_id}")
      ruleset_data = await ruleset_resp.json_async()
      ruleset_data = ruleset_data.get("data", {})
      ruleset_attributes = ruleset_data.get("attributes", {})
      if ruleset_data and ruleset_attributes:
        return {
            "rule_id": ruleset_data.get("id"),
            "rule_name": ruleset_attributes.get("name", ""),
            "rule_source": ruleset_attributes.get("source", ""),
            "rule_content": ruleset_attributes.get("rules", ""),
            "count" : rule.get("count", 0),
            "rule_type": rule_type
        }
      return {"error": f"No data found for YARA ruleset {ruleset_id}"}
  except Exception as e:
    logging.exception("Error fetching YARA ruleset %s: %s", ruleset_id, e)
    return {"error": f"Error fetching YARA ruleset {ruleset_id}: {e}"}

async def _get_sigma_rule_details(ctx: Context, rule: dict, rule_type: str) -> typing.Dict[str, typing.Any]:
  """Fetches details for a single Sigma ruleset and formats the output."""

  ruleset_id = rule.get("value",{}).get("id", None)
  if not ruleset_id:  
    return {"error": f"No ruleset_id found in rule"} 
  
  try:
    async with vt_client(ctx) as client:
      ruleset_resp = await client.get_async(f"/sigma_rules/{ruleset_id}")
      ruleset_data = await ruleset_resp.json_async()
      ruleset_data = ruleset_data.get("data", {})
      ruleset_attributes = ruleset_data.get("attributes", {})
      if ruleset_data and ruleset_attributes:
        return {
            "rule_id": ruleset_data.get("id", ""),
            "rule_name": rule.get("value", {}).get("title", ""),
            "rule_source": ruleset_attributes.get("source_url", ""),
            "rule_content": ruleset_attributes.get("rule", ""),
            "count" : rule.get("count", 0),
            "rule_type": rule_type
        }
      return {"error": f"No data found for Sigma ruleset {ruleset_id}"}
  except Exception as e:
    logging.exception("Error fetching Sigma ruleset %s: %s", ruleset_id, e)
    return {"error": f"Error fetching Sigma ruleset {ruleset_id}: {e}"}

@server.tool()
async def get_collection_rules(collection_id: str, ctx: Context, top_n: int = 4, rule_types: typing.List[str] = None) -> typing.Union[typing.List[typing.Dict[str, typing.Any]], typing.Dict[str, str]]:
  """Retrieve top N community rules and all curated hunting rules for a specific collection.

  Note:
    The `rule_types` argument filters the types of rules returned. Available types are:
    - 'crowdsourced_ids'
    - 'crowdsourced_sigma'
    - 'crowdsourced_yara'
    - 'curated_yara_rule'
    If `rule_types` is not provided, all types are returned.

  Example:
    - `rule_types=['crowdsourced_yara']`: Only crowdsourced YARA rules.
    - `rule_types=['crowdsourced_ids', 'curated_yara_rule']`: Crowdsourced IDS and curated YARA rules.

  Args:
    collection_id (required): The ID of the collection.
    top_n (optional): The number of top community rules to return from each category. Defaults to 4.
    rule_types (optional): List of rule types to fetch.

  Returns:
    A list of dictionaries, where each dictionary contains a rule and its metadata, or an error dictionary.
  """
  crowsourced_rules = []
  if rule_types is None:
    rule_types = ["crowdsourced_ids", "crowdsourced_sigma", "crowdsourced_yara", "curated_yara_rule"]

  rule_keys_map = {
      "crowdsourced_yara_results": "crowdsourced_yara",
      "crowdsourced_sigma_results": "crowdsourced_sigma",
      "crowdsourced_ids_results": "crowdsourced_ids",
  }
  # Fetch community rules from aggregations if requested
  if any(rt in rule_types for rt in ["crowdsourced_ids", "crowdsourced_sigma", "crowdsourced_yara"]):
      try:
        async with vt_client(ctx) as client:
          data = await client.get_async(f"/collections/{collection_id}?attributes=aggregations")
          data = await data.json_async()

        files_aggregations = data.get("data", {}).get("attributes", {}).get("aggregations", {}).get("files", {})

        if files_aggregations:
          # Iterate through different community rule types
          for key, rule_type in rule_keys_map.items():
            rules = files_aggregations.get(key, [])
            if rule_type not in rule_type and not rules:
              continue

            # Sort rules by count and take the top N
            sorted_rules = sorted(rules, key=lambda x: x.get("count", 0), reverse=True)
            top_rules = sorted_rules[:top_n]
            # Fetch detailed rule content for each type
            for rule in top_rules:
              if key == "crowdsourced_yara_results":
                rule_details = await _get_yara_rule_details(ctx, rule, rule_type)
                if "error" not in rule_details:
                  crowsourced_rules.append(rule_details)
              elif key == "crowdsourced_sigma_results":
                rule_details = await _get_sigma_rule_details(ctx, rule, rule_type)
                if "error" not in rule_details:
                  crowsourced_rules.append(rule_details)
              else: # IDS rules
                rule_value = rule.get("value", {})
                crowsourced_rules.append({
                    "rule_id": rule.get("id", ""),
                    "rule_name": rule_value.get("message", ""),
                    "rule_source": rule_value.get("url", ""),
                    "rule_content": rule_value.get("rule", ""),
                    "count" : rule.get("count", 0),
                    "rule_type": rule_type
                  })
      except Exception as e:
        logging.exception("Error fetching community rules aggregations: %s", e)
        # Continue execution to fetch other rule types
  crowsourced_rules = sorted(crowsourced_rules, key=lambda x: x.get("count", 0), reverse=True)
  curated_rules = []
  # Fetch curated hunting rulesets if requested
  if "curated_yara_rule" in rule_types:
    try:
      async with vt_client(ctx) as client:
        # 1. Get related hunting ruleset IDs from the collection
        related_rulesets_resp = await client.get_async(f"/collections/{collection_id}/hunting_rulesets")
        related_rulesets_data = await related_rulesets_resp.json_async()
        related_rulesets = related_rulesets_data.get("data", [])

      # Iterate through each related ruleset
      for ruleset in related_rulesets:
        ruleset_id = ruleset.get("id", None)
        if not ruleset_id:
          continue
        try:
          # 2. Get the full hunting ruleset object for each ID.
          async with vt_client(ctx) as client:
            ruleset_resp = await client.get_async(f"/intelligence/hunting_rulesets/{ruleset_id}")
            ruleset_data = await ruleset_resp.json_async()
        except Exception as e:
          logging.exception("Error processing rule: %s", e)
          continue

        attributes = ruleset_data.get("data", {}).get("attributes", {})
        rules = attributes.get("rules", "")
        rule_names = attributes.get("rule_names", [])
        n_rules = attributes.get("number_of_rules", 0)

        # Append each rule to the curated_rules list
        if n_rules == 1:
          curated_rules.append({
              "rule_type": "curated_yara_rule",
              "rule_name": rule_names[0],
              "rule_content": rules,
          })
        else:
          for i in range(n_rules):
            curated_rules.append({
                "rule_type": "curated_yara_rule",
                "rule_name": rule_names[i],
                "rule_content": rules[i],
            })
    except Exception as e:
      logging.exception("Error fetching curated rules: %s", e)
  all_rules = curated_rules + crowsourced_rules
  return utils.sanitize_response(all_rules)
