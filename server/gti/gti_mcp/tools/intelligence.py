
import typing

from mcp.server.fastmcp import Context

from .. import utils
from ..server import server, vt_client


@server.tool()
async def search_iocs(query: str, ctx: Context, limit: int = 10, order_by: str = "last_submission_date-") -> typing.List[typing.Dict[str, typing.Any]]:
  """Search Indicators of Compromise (IOC) in the Google Threat Intelligence platform.
  
  You can find all available modifers at: https://gtidocs.virustotal.com/docs/file-search-modifiers

  With integer modifers, use the `-` and `+` characters to indicate:
    - Greater than: `p:60+`
    - Less than: `p:60-`
    - Equal to: `p:60`

  You can search by for different IOC types using the `entity` modifier. Below, the different IOC types and the supported orders:

    | Entity type   | Supported orders | Default order |
    | ------------- | ---------------- | ------------- |
    | file          | first_submission_date, last_submission_date, positives, times_submitted, size	    | last_submission_date- |
    | url           | first_submission_date, last_submission_date, positives, times_submitted, status   | last_submission_date- |
    | domain        | creation_date, last_modification_date, last_update_date, positives                | last_modification_date- |
    | ip            | ip, last_modification_date, positives                                             | last_modification_date- |

  Args
    query (required): Search query to find IOCs.
    limit: Limit the number of threats to retrieve. 10 by default.
    
  Returns:
    List of collections, aka threats.
  """
  res = await utils.consume_vt_iterator(
      vt_client(ctx), 
      "/intelligence/search", 
      params={
          "query": query, 
          "order": order_by},
      limit=limit)
  return res

