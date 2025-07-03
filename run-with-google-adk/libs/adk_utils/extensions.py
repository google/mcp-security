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


# imports for overriding `get_tools`
from typing_extensions import override
from google.adk.tools.mcp_tool.mcp_session_manager import retry_on_closed_resource
from typing import List
from typing import Optional, Union, TextIO
from google.adk.agents.readonly_context import ReadonlyContext
from google.adk.tools.mcp_tool.mcp_tool import MCPTool, BaseTool
from google.adk.tools.mcp_tool.mcp_session_manager import  StdioServerParameters, StdioConnectionParams, SseConnectionParams,StreamableHTTPConnectionParams
from mcp.types import ListToolsResult
from .cache import tools_cache
from  google.adk.tools.mcp_tool.mcp_toolset  import MCPToolset, ToolPredicate
import sys
import logging

logging.basicConfig(
    level=logging.INFO)

class MCPToolSetWithSchemaAccess(MCPToolset):
  """
  TODO - double check

  Required for - name for caching (any other way?)
  Required for - tool caching (is it alrady implemented?) (in get_tools)
  """

  def __init__(
      self,
      *,
      tool_set_name: str, # <-- new parameter
      connection_params: Union[
          StdioServerParameters,
          StdioConnectionParams,
          SseConnectionParams,
          StreamableHTTPConnectionParams,
      ],
      tool_filter: Optional[Union[ToolPredicate, List[str]]] = None,
      errlog: TextIO = sys.stderr,
  ):
    super().__init__(
        connection_params=connection_params,
        tool_filter=tool_filter,
        errlog=errlog
    )
    self.tool_set_name = tool_set_name
    logging.info(f"MCPToolSetWithSchemaAccess initialized with tool_set_name: '{self.tool_set_name}'")  
    self._session = None

  @retry_on_closed_resource("_reinitialize_session")
  @override
  async def get_tools(
      self,
      readonly_context: Optional[ReadonlyContext] = None,
  ) -> List[BaseTool]:
    """Return all tools in the toolset based on the provided context.

    Args:
        readonly_context: Context used to filter tools available to the agent.
            If None, all tools in the toolset are returned.

    Returns:
        List[BaseTool]: A list of tools available under the specified context.
    """
    # Get session from session manager
    if not self._session:
      self._session = await self._mcp_session_manager.create_session()

    if self.tool_set_name in tools_cache.keys():
      logging.info(f"Tools found in cache for toolset {self.tool_set_name}, returning them")  
      return tools_cache[self.tool_set_name]
    else:
      logging.info(f"No tools found in cache for toolset {self.tool_set_name}, loading")

    tools_response: ListToolsResult = await self._session.list_tools()

    # Apply filtering based on context and tool_filter
    tools = []
    for tool in tools_response.tools:
      mcp_tool = MCPTool(
          mcp_tool=tool,
          mcp_session_manager=self._mcp_session_manager,
      )

      if self._is_tool_selected(mcp_tool, readonly_context):
        tools.append(mcp_tool)

    tools_cache[self.tool_set_name] = tools
    return tools