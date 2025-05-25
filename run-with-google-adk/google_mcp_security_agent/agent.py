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
from google.adk.agents.llm_agent import LlmAgent
from  google.adk.tools.mcp_tool.mcp_toolset  import MCPToolset, StdioServerParameters
import os
import logging


# imports for overriding `get_tools`
from typing_extensions import override
from google.adk.tools.mcp_tool.mcp_session_manager import retry_on_closed_resource
from typing import List
from typing import Optional
from google.adk.agents.readonly_context import ReadonlyContext
from google.adk.tools.mcp_tool.mcp_tool import MCPTool, BaseTool
from mcp.types import ListToolsResult


logging.basicConfig(
    level=logging.INFO)


if os.environ.get("MINIMAL_LOGGING","N") == "Y":
  root_logger = logging.getLogger()
  root_logger.setLevel(logging.ERROR)


class MCPToolSetWithSchemaAccess(MCPToolset):


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

    # Fetch available tools from the MCP server
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

    ## Check if we need to perform schema compatible
    # Adding Gemini compatibility for non 2.5 models.
    # Vertex AI does not support anyOf schema type.
    # GenAI API supoprts it for models version >= 2.5
    # If you plan to use Gemini API - Models list - https://ai.google.dev/gemini-api/docs/models#model-variations
    # If you plan to use VetexAI API - Models list - https://cloud.google.com/vertex-ai/generative-ai/docs/models
    model_version = os.environ.get("GOOGLE_MODEL").split("-")[1]
    if float(model_version) < 2.5 or os.environ.get("GOOGLE_GENAI_USE_VERTEXAI").upper() == "TRUE": 
      logging.error(f"Model - {os.environ.get('GOOGLE_MODEL')} needs Gemini compatible tools, updating schema ...")
      tools = make_tools_compatible(tools)     
    else:
      logging.info(f"Model - {os.environ.get('GOOGLE_MODEL')} does not need updating schema")         
              
    return tools

def make_tools_compatible(tools):
  """
  This function makes the schema compatible with Gemini/Vertex AI API
  It is only needed when API used is Gemini and model is other than 2.5 models
  It is however needed for ALL models when API used is VertexAI
  """
  for tool in tools:
    for key in tool._mcp_tool.inputSchema.keys():
      if key == "properties":
          for prop_name in tool._mcp_tool.inputSchema["properties"].keys():
            if "anyOf" in tool._mcp_tool.inputSchema["properties"][prop_name].keys():
              if (tool._mcp_tool.inputSchema["properties"][prop_name]["anyOf"][0]["type"] == "array"):
                tool._mcp_tool.inputSchema["properties"][prop_name]["type"] = tool._mcp_tool.inputSchema["properties"][prop_name]["anyOf"][0]["items"]["type"]
              else:
                 tool._mcp_tool.inputSchema["properties"][prop_name]["type"] = tool._mcp_tool.inputSchema["properties"][prop_name]["anyOf"][0]["type"] 
              tool._mcp_tool.inputSchema["properties"][prop_name].pop("anyOf")

  return tools


def get_all_tools():
  """Get Tools from All MCP servers"""
  logging.info("Attempting to connect to MCP servers...")
  secops_tools = None
  gti_tools = None
  secops_soar_tools = None
  scc_tools = None # Initialize scc_tools
  
  uv_dir_prefix="../server"
  env_file_path = "../../../run-with-google-adk/google_mcp_security_agent/.env"

  if os.environ.get("REMOTE_RUN","N") == "Y":
    env_file_path="/tmp/.env"
    uv_dir_prefix="./server"

  logging.info(f"Using Env File Path - {env_file_path}, Current directory is - {os.getcwd()}")

  if os.environ.get("LOAD_SCC_MCP") == "Y":
    scc_tools = MCPToolSetWithSchemaAccess(
            connection_params=StdioServerParameters(
                command='uv',
                args=[ "--directory",
                        uv_dir_prefix + "/scc",
                        "run",
                        "scc_mcp.py"
                    ],
                )
    )  

  if os.environ.get("LOAD_SECOPS_MCP") == "Y":
    secops_tools = MCPToolSetWithSchemaAccess(
            connection_params=StdioServerParameters(
                command='uv',
                args=["--directory",
                        uv_dir_prefix + "/secops/secops_mcp",
                        "run",
                        "--env-file",
                        env_file_path,
                        "server.py"
                    ],
                )
    )

  if os.environ.get("LOAD_GTI_MCP") == "Y":
    gti_tools = MCPToolSetWithSchemaAccess(
            connection_params=StdioServerParameters(
                command='uv',
                args=[ "--directory",
                        uv_dir_prefix + "/gti/gti_mcp",
                        "run",
                        "--env-file",
                        env_file_path,
                        "server.py"
                    ],
                )
    )  

  if os.environ.get("LOAD_SECOPS_SOAR_MCP") == "Y":
    secops_soar_tools = MCPToolSetWithSchemaAccess(
            connection_params=StdioServerParameters(
                command='uv',
                args=["--directory",
                        uv_dir_prefix + "/secops-soar/secops_soar_mcp",
                        "run",
                        "--env-file",
                        env_file_path,
                        "server.py",
                        "--integrations",
                        "CSV,OKTA"
                    ]
                )
                )  



  logging.info("MCP Toolsets created successfully.")
  return [secops_tools,gti_tools,secops_soar_tools,scc_tools]

def create_agent():
  """Gets tools from MCP Server."""
  tools = [item for item in get_all_tools() if item is not None]

  print(f"Model is - {os.environ.get("GOOGLE_MODEL")}")
  agent = LlmAgent(
      model=os.environ.get("GOOGLE_MODEL"), 
      name='google_security_assistant',
      instruction=os.environ.get("DEFAULT_PROMPT"),
      tools=tools 
  )
  return agent


root_agent = create_agent()
