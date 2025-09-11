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


from typing import List
from typing import Optional, Union, TextIO
from google.adk.agents.readonly_context import ReadonlyContext
from google.adk.tools.base_tool import BaseTool
from google.adk.tools.mcp_tool.mcp_toolset import StdioServerParameters
from .cache import tools_cache
from google.adk.tools.mcp_tool.mcp_toolset import MCPToolset
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
      connection_params: StdioServerParameters,
      tool_filter: Optional[List[str]] = None,
      errlog: TextIO = sys.stderr,
  ):
    super().__init__(
        connection_params=connection_params,
        errlog=errlog
    )
    self.tool_set_name = tool_set_name
    logging.info(f"MCPToolSetWithSchemaAccess initialized with tool_set_name: '{self.tool_set_name}'")  
    self._session = None

  async def get_tools(
      self,
      readonly_context: Optional[ReadonlyContext] = None,
  ) -> List[BaseTool]:
    """Return all tools in the toolset based on the provided context with caching.

    Args:
        readonly_context: Context used to filter tools available to the agent.
            If None, all tools in the toolset are returned.

    Returns:
        List[BaseTool]: A list of tools available under the specified context.
    """
    # Check cache first
    if self.tool_set_name in tools_cache.keys():
      logging.info(f"Tools found in cache for toolset {self.tool_set_name}, returning them")  
      return tools_cache[self.tool_set_name]
    else:
      logging.info(f"No tools found in cache for toolset {self.tool_set_name}, loading from parent")

    # Get tools from parent class
    tools = await super().get_tools(readonly_context)
    
    # Cache the tools
    tools_cache[self.tool_set_name] = tools
    logging.info(f"Cached {len(tools)} tools for toolset {self.tool_set_name}")
    return tools
