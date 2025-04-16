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


@server.tool()
async def search_iocs(query: str, ctx: Context, limit: int = 10, order_by: str = "last_submission_date-") -> typing.List[typing.Dict[str, typing.Any]]:
  """Search Indicators of Compromise (IOC) in the Google Threat Intelligence platform.

  You can search by for different IOC types using the `entity` modifier. Below, the different IOC types and the supported orders:

    | Entity type   | Supported orders | Default order |
    | ------------- | ---------------- | ------------- |
    | file          | first_submission_date, last_submission_date, positives, times_submitted, size	    | last_submission_date- |
    | url           | first_submission_date, last_submission_date, positives, times_submitted, status   | last_submission_date- |
    | domain        | creation_date, last_modification_date, last_update_date, positives                | last_modification_date- |
    | ip            | ip, last_modification_date, positives                                             | last_modification_date- |

  You can find all available modifers at:
    - Files: https://gtidocs.virustotal.com/docs/file-search-modifiers
    - URLs: https://gtidocs.virustotal.com/docs/url-search-modifiers
    - Domains: https://gtidocs.virustotal.com/docs/domain-search-modifiers
    - IP Addresses: https://gtidocs.virustotal.com/docs/ip-address-search-modifiers

  With integer modifers, use the `-` and `+` characters to indicate:
    - Greater than: `p:60+`
    - Less than: `p:60-`
    - Equal to: `p:60`

  Args
    query (required): Search query to find IOCs.
    limit: Limit the number of IoCs to retrieve. 10 by default.
    order_by: Order the results. "last_submission_date-" by default.

  Returns:
    List of Indicators of Compromise (IoCs).
  """
  res = await utils.consume_vt_iterator(
      vt_client(ctx),
      "/intelligence/search",
      params={
          "query": query,
          "order": order_by},
      limit=limit)
  return res
