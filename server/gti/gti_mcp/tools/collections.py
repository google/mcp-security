
import typing

from mcp.server.fastmcp import Context

from .. import utils
from ..server import server, vt_client


COLLECTION_KEY_RELATIONSHIPS = [
    "associations",
    "files",
    "domains",
    "ip_addresses",
    "urls",
]
COLLECTION_EXCLUDED_ATTRS = ','.join([
    "aggregations"
])

COLLECTION_TYPES = {
    "threat-actor",
    "malware-family",
    "campaign",
    "report",
    "vulnerability",
    "collection"
}

# Load resources and tools.
@server.tool()
async def get_collection_report(collection_id: str, ctx: Context) -> typing.Dict[str, typing.Any]:
  """At Google Threat Intelligence, threats are modeled as "collections". This tool retrieves them from the platform.
  
  They have different sub types like: "malware-family", "threat-actor", "campaign", "report" or a generic "collection". You can find it in the "collection_type" field.
  
  You must always include the subtype and identifier as parameter for the tool the pattern will always be subtype--<id> such as "report--6e908e6adec4d5121a4b4e5ff5fdeb304f5148cf2377bfc070781353287dcb4c".

  Args:
    collection_id (required): Google Threat Intelligence identifier.
  Returns:
    A collection object. Put attention to the collection type to correctly understand what it represents.
  """
  res = await utils.fetch_object(
      vt_client(ctx), 
      "collections", 
      "collection", 
      collection_id,
      COLLECTION_KEY_RELATIONSHIPS,
      params={"exclude_attributes": COLLECTION_EXCLUDED_ATTRS})
  return res


async def _search_threats_by_collection_type(
    query: str, collection_type:str, ctx: Context, limit: int = 10, order_by: str = "relevance-") -> typing.List[typing.Dict[str, typing.Any]]:
  """Search a given threat type in the Google Threat Intelligence platform, 
  
  Args:
    query (required): Search query to find threats.
    collection_type (required): Collection type. One of: "threat-actor", "malware-family", "campaign", "report", "vulnerability", "collection".
    limit: Limit the number of threats to retrieve. 10 by default.
    order_by: Order results by the given order key. "relevance-" by default.
    
  Returns:
    List of collections, aka threats.
  """
  if collection_type not in COLLECTION_TYPES:
    raise ValueError(
      f"wrong collection_type. Available collection_type are: {','.join(COLLECTION_TYPES)} ")

  res = await utils.consume_vt_iterator(
      vt_client(ctx), 
      "/collections", 
      params={
          "filter": f'collection_type:{collection_type} {query}', 
          "order": order_by,
          "relationships": COLLECTION_KEY_RELATIONSHIPS, 
          "exclude_attributes": COLLECTION_EXCLUDED_ATTRS},
      limit=limit)
  return res


@server.tool()
async def search_threats(query: str, ctx: Context, limit: int = 10, order_by: str = "relevance-") -> typing.List[typing.Dict[str, typing.Any]]:
  """Search threats in the Google Threat Intelligence platform.
  
  Threats are modeled as collections. Once you get collections from this tool, you can use `get_collection_report` to fetch the full reports and their relationships.

  If you need to filter by any kind of threat in particular, you can use the "collection_type" modifier. Avalable types are: "threat-actor", "malware-family", "campaign", "report", "vulnerability" and a generic "collection" type.

  You can use order_by to sort the results by: "relevance", "creation_date". You can use the sign "+" to make it order ascending, or "-" to make it descending. By default is "relevance-"
  
  Args:
    query (required): Search query to find threats.
    limit: Limit the number of threats to retrieve. 10 by default.
    order_by: Order results by the given order key. "relevance-" by default.
    
  Returns:
    List of collections, aka threats.
  """
  res = await utils.consume_vt_iterator(
      vt_client(ctx), 
      "/collections", 
      params={
          "filter": query, 
          "order": order_by,
          "relationships": COLLECTION_KEY_RELATIONSHIPS, 
          "exclude_attributes": COLLECTION_EXCLUDED_ATTRS},
      limit=limit)
  return res


@server.tool()
async def search_campaigns(query: str, ctx: Context, limit: int = 10, order_by: str = "relevance-") -> typing.List[typing.Dict[str, typing.Any]]:
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
  res = await _search_threats_by_collection_type(query, "campaign", ctx, limit, order_by)
  return res


@server.tool()
async def search_threat_actors(query: str, ctx: Context, limit: int = 10, order_by: str = "relevance-") -> typing.List[typing.Dict[str, typing.Any]]:
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
  res = await _search_threats_by_collection_type(query, "threat-actor", ctx, limit, order_by)
  return res


@server.tool()
async def search_malware_families(query: str, ctx: Context, limit: int = 10, order_by: str = "relevance-") -> typing.List[typing.Dict[str, typing.Any]]:
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
  res = await _search_threats_by_collection_type(query, "malware-family", ctx, limit, order_by)
  return res


@server.tool()
async def search_threat_reports(query: str, ctx: Context, limit: int = 10, order_by: str = "relevance-") -> typing.List[typing.Dict[str, typing.Any]]:
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
  res = await _search_threats_by_collection_type(query, "report", ctx, limit, order_by)
  return res


@server.tool()
async def search_vulnerabilities(query: str, ctx: Context, limit: int = 10, order_by: str = "relevance-") -> typing.List[typing.Dict[str, typing.Any]]:
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
  res = await _search_threats_by_collection_type(query, "vulnerability", ctx, limit, order_by)
  return res
