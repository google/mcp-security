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
from google.adk.tools.mcp_tool.mcp_toolset import MCPToolset, StdioServerParameters
import os
import logging
from contextlib import AsyncExitStack

logging.basicConfig(
    level=logging.INFO)


if os.environ.get("MINIMAL_LOGGING","N") == "Y":
  root_logger = logging.getLogger()
  root_logger.setLevel(logging.ERROR)



async def get_all_tools():
  """Get Tools from All MCP servers"""
  logging.info("Attempting to connect to MCP servers...")
  secops_tools = []
  gti_tools = []
  secops_soar_tools = []
  scc_tools = []  # Initialize scc_tools
  compliance_tools = []  # Initialize compliance_tools

  exit_stack = AsyncExitStack()
  uv_dir_prefix="../server"
  env_file_path = "../../../run-with-google-adk/google-mcp-security-agent/.env"

  if os.environ.get("REMOTE_RUN","N") == "Y":
    env_file_path="/tmp/.env"
    uv_dir_prefix="./server"

  logging.info(f"Using Env File Path - {env_file_path}, Current directory is - {os.getcwd()}")

  if os.environ.get("LOAD_SECOPS_MCP") == "Y":
    secops_tools, exit_stack = await MCPToolset.from_server(
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
    gti_tools, exit_stack = await MCPToolset.from_server(
            connection_params=StdioServerParameters(
                command='uv',
                args=[ "--directory",
                        uv_dir_prefix + "/gti/gti_mcp",
                        "run",
                        "--env-file",
                        env_file_path,
                        "server.py"
                    ],
                ),async_exit_stack=exit_stack
    )  

  if os.environ.get("LOAD_SECOPS_SOAR_MCP") == "Y":
    secops_soar_tools, exit_stack = await MCPToolset.from_server(
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
                    ],
                ),async_exit_stack=exit_stack
    )  

  if os.environ.get("LOAD_SCC_MCP") == "Y":
    scc_tools, exit_stack = await MCPToolset.from_server(
            connection_params=StdioServerParameters(
                command='uv',
                args=[ "--directory",
                        uv_dir_prefix + "/scc/",
                        "run",
                        "scc_mcp.py"
                    ],
                ),async_exit_stack=exit_stack
    )

  if os.environ.get("LOAD_COMPLIANCE_MCP") == "Y":
    compliance_tools, exit_stack = await MCPToolset.from_server(
            connection_params=StdioServerParameters(
                command='uv',
                args=[ "--directory",
                        uv_dir_prefix + "/compliance/",
                        "run",
                        "compliance_mcp.py"
                    ],
                ),async_exit_stack=exit_stack
    )    


  logging.info("MCP Toolsets created successfully.")
  return secops_tools+gti_tools+secops_soar_tools+scc_tools+compliance_tools, exit_stack

def make_tools_gemini_compatible(tools):
  """
  This function makes the schema compatible with Gemini/Vertex AI API
  It is only needed when API used is Gemini and model is other than 2.5 models
  It is however needed for ALL models when API used is VertexAI
  """
  for tool in tools:
    for key in tool.mcp_tool.inputSchema.keys():
      if key == "properties":
          for prop_name in tool.mcp_tool.inputSchema["properties"].keys():
            if "anyOf" in tool.mcp_tool.inputSchema["properties"][prop_name].keys():
              if (tool.mcp_tool.inputSchema["properties"][prop_name]["anyOf"][0]["type"] == "array"):
                tool.mcp_tool.inputSchema["properties"][prop_name]["type"] = tool.mcp_tool.inputSchema["properties"][prop_name]["anyOf"][0]["items"]["type"]
              else:
                 tool.mcp_tool.inputSchema["properties"][prop_name]["type"] = tool.mcp_tool.inputSchema["properties"][prop_name]["anyOf"][0]["type"] 
              tool.mcp_tool.inputSchema["properties"][prop_name].pop("anyOf")

  return tools

async def create_agent():
  """Gets tools from MCP Server."""
  tools, exit_stack = await get_all_tools()

  # Adding Gemini compatibility for non 2.5 models.
  # Vertex AI does not support anyOf schema type.
  # GenAI API supoprts it for models version >= 2.5
  # If you plan to use Gemini API - Models list - https://ai.google.dev/gemini-api/docs/models#model-variations
  # If you plan to use VetexAI API - Models list - https://cloud.google.com/vertex-ai/generative-ai/docs/models
  model_version = os.environ.get("GOOGLE_MODEL").split("-")[1]
  if float(model_version) < 2.5 or os.environ.get("GOOGLE_GENAI_USE_VERTEXAI").upper() == "TRUE": 
    logging.error(f"Model - {os.environ.get('GOOGLE_MODEL')} needs Gemini compatible tools, updating schema ...")
    tools = make_tools_gemini_compatible(tools)     
  else:
    logging.info(f"Model - {os.environ.get('GOOGLE_MODEL')} does not need updating schema") 

  agent = LlmAgent(
      model=os.environ.get("GOOGLE_MODEL"), 
      name='google_security_assistant',
      instruction=os.environ.get("DEFAULT_PROMPT"),
      tools=tools 
  )
  return agent, exit_stack


root_agent = create_agent()
