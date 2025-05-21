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

logging.basicConfig(
    level=logging.INFO)


if os.environ.get("MINIMAL_LOGGING","N") == "Y":
  root_logger = logging.getLogger()
  root_logger.setLevel(logging.ERROR)



def get_all_tools():
  """Get Tools from All MCP servers"""
  logging.info("Attempting to connect to MCP servers...")
  secops_tools = None
  gti_tools = None
  secops_soar_tools = None
  scc_tools = None # Initialize scc_tools
  
  uv_dir_prefix="../server"
  env_file_path = "../../../run-with-google-adk/google-mcp-security-agent/.env"

  if os.environ.get("REMOTE_RUN","N") == "Y":
    env_file_path="/tmp/.env"
    uv_dir_prefix="./server"

  logging.info(f"Using Env File Path - {env_file_path}, Current directory is - {os.getcwd()}")

  if os.environ.get("LOAD_SECOPS_MCP") == "Y":
    secops_tools = MCPToolset(
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
    gti_tools = MCPToolset(
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
    secops_soar_tools = MCPToolset(
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

  if os.environ.get("LOAD_SCC_MCP") == "Y":
    scc_tools = MCPToolset(
            connection_params=StdioServerParameters(
                command='uv',
                args=[ "--directory",
                        uv_dir_prefix + "/scc/",
                        "run",
                        "scc_mcp.py"
                    ],
                )
    )  


  logging.info("MCP Toolsets created successfully.")
  return [secops_tools,gti_tools,secops_soar_tools,scc_tools]

def create_agent():
  """Gets tools from MCP Server."""
  tools = [item for item in get_all_tools() if item is not None]

  agent = LlmAgent(
      model=os.environ.get("GOOGLE_MODEL"), 
      name='google_security_assistant',
      instruction=os.environ.get("DEFAULT_PROMPT"),
      tools=tools 
  )
  return agent


root_agent = create_agent()
