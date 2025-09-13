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
from  google.adk.tools.mcp_tool.mcp_toolset  import StdioServerParameters, StdioConnectionParams
import os
import logging

from utils_extensions_cbs_tools.extensions import MCPToolSetWithSchemaAccess
from utils_extensions_cbs_tools.tools import store_file, get_file_link, list_files
from utils_extensions_cbs_tools.callbacks import bmc_trim_llm_request, bac_setup_state_variable
from typing import TextIO
import sys


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

  timeout = float(os.environ.get("STDIO_PARAM_TIMEOUT","60.0"))
  
  uv_dir_prefix="../server"
  env_file_path = "../../../run-with-google-adk/google_mcp_security_agent/.env"

  if os.environ.get("REMOTE_RUN","N") == "Y":
    env_file_path="/tmp/.env"
    uv_dir_prefix="./server"

  if os.environ.get("AE_RUN","N") == "Y":
    env_file_path="../../../google_mcp_security_agent/.env"
    uv_dir_prefix="./server"

  logging.info(f"Using Env File Path - {env_file_path}, Current directory is - {os.getcwd()}, uv_dir_prefix is - {uv_dir_prefix}")

  # required temporarily for https://github.com/google/adk-python/issues/1024
  errlog_ae : TextIO = sys.stderr
  if os.environ.get("AE_RUN","N") == "Y":
    errlog_ae = None
    
  
  if os.environ.get("LOAD_SCC_MCP") == "Y":
    scc_tools = MCPToolSetWithSchemaAccess(
                  connection_params=StdioConnectionParams(
                    server_params=StdioServerParameters(
                                  command='uv',
                                  args=[ "--directory",
                                          uv_dir_prefix + "/scc",
                                          "run",
                                          "scc_mcp.py"
                                        ]
                    ),
                  timeout=timeout),
                tool_set_name="scc",
                errlog=errlog_ae 
                )

  if os.environ.get("LOAD_SECOPS_MCP") == "Y":
    secops_tools = MCPToolSetWithSchemaAccess(
                  connection_params=StdioConnectionParams(
                    server_params=StdioServerParameters(
                                  command='uv',
                                  args=[ "--directory",
                                          uv_dir_prefix + "/secops/secops_mcp",
                                          "run",
                                          "--env-file",
                                          env_file_path,
                                          "server.py"
                                        ]
                    ),
                  timeout=timeout),
                tool_set_name="secops_mcp",
                errlog=errlog_ae
                )

  if os.environ.get("LOAD_GTI_MCP") == "Y":
    gti_tools = MCPToolSetWithSchemaAccess(
                  connection_params=StdioConnectionParams(
                    server_params=StdioServerParameters(
                                  command='uv',
                                  args=[ "--directory",
                                          uv_dir_prefix + "/gti/gti_mcp",
                                          "run",
                                          "--env-file",
                                          env_file_path,
                                          "server.py"
                                        ]
                    ),
                  timeout=timeout),
                tool_set_name="gti_mcp",
                errlog=errlog_ae
                )    


  if os.environ.get("LOAD_SECOPS_SOAR_MCP") == "Y":
    secops_soar_tools = MCPToolSetWithSchemaAccess(
                  connection_params=StdioConnectionParams(
                    server_params=StdioServerParameters(
                                  command='uv',
                                  args=[ "--directory",
                                          uv_dir_prefix + "/secops-soar/secops_soar_mcp",
                                          "run",
                                          "--env-file",
                                          env_file_path,
                                          "server.py",
                                          "--integrations",
                                          os.environ.get("SECOPS_INTEGRATIONS","CSV,OKTA")
                                        ]
                    ),
                  timeout=timeout),
                tool_set_name="secops_soar_mcp",
                errlog=errlog_ae
                )    

  logging.info("MCP Toolsets created successfully.")
  return [secops_tools,gti_tools,secops_soar_tools,scc_tools]

def create_agent():
  tools:any = [item for item in get_all_tools() if item is not None]
  tools.append(store_file)
  tools.append(get_file_link)
  tools.append(list_files)

  agent = LlmAgent(
      model=os.environ.get("GOOGLE_MODEL"), 
      name="google_mcp_security_agent",
      instruction=os.environ.get("DEFAULT_PROMPT"),
      tools=tools,
      before_model_callback=bmc_trim_llm_request,
      before_agent_callback=bac_setup_state_variable,
#      sub_agents=[ADD SUB AGENTS HERE],
      description="You are the google_mcp_security_agent."

  )
  return agent


root_agent = create_agent()
