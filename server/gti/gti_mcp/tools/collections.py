
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

# Load resources and tools.
@server.tool()
async def get_collection_report(collection_id: str, ctx: Context) -> typing.Dict[str, typing.Any]:
  """At Google Threat Intelligence, threats are modeled as "collections". This tool retrieves them from the platform.
  
  They have different sub types like: "malware-family", "threat-actor", "campaign", "report" or a generic "collection". You can find it in the "collection_type" field.
   
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
      COLLECTION_KEY_RELATIONSHIPS)
  return res


@server.tool()
async def search_threats(query: str, ctx: Context, limit: int = 10, order_by: str = "relevance-") -> typing.List[typing.Dict[str, typing.Any]]:
  """Search threats in the Google Threat Intelligence platform.
  
  Threats are modeled as collections. Once you get collections from this tool, you can use `get_collection_report` to fetch the full reports and their relationships.

  If you need to filter by any kind of threat in particular, you can use the "collection_type" modifier. Avalable types are: "threat-actor", "malware-family", "campaign", "report", "vulnerability" and a generic "collection".

  You can use order_by to sort the results by: "relevance", "creation_date". You can use the sign "+" to make it order ascending, or "-" to make it descending. By default is "relevance-"
  
  Args:
    filter (required): Search query to find threats.
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

