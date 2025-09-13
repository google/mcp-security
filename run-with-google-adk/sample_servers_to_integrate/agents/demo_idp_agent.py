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
from utils_extensions_cbs_tools.callbacks import bmc_trim_llm_request
from typing import TextIO
import sys

# TODO improve logging
logging.basicConfig(
    level=logging.INFO)

if os.environ.get("MINIMAL_LOGGING","N") == "Y":
  root_logger = logging.getLogger()
  root_logger.setLevel(logging.ERROR)


is_any_variable_unset = any(
    os.getenv(var, "NOT_SET") == "NOT_SET"
    for var in ["IDP_CLIENT_ID","IDP_CLIENT_SECRET",]
)
if is_any_variable_unset:
  print(f"Please set all required environment variables, check .env file")
  exit(1)

def get_all_tools():
  """Get Tools from IDP MCP"""
  logging.info("Attempting to connect to MCP servers for IDP...")
  idp_tools = None # Initialize scc_tools
  
  uv_dir_prefix="../server"
  if os.environ.get("REMOTE_RUN","N") == "Y":
    uv_dir_prefix="./server"

  if os.environ.get("AE_RUN","N") == "Y":
    uv_dir_prefix="./server"    

  # required temporarily for https://github.com/google/adk-python/issues/1024
  errlog_ae : TextIO = sys.stderr
  if os.environ.get("AE_RUN","N") == "Y":
    errlog_ae = None

  timeout = float(os.environ.get("STDIO_PARAM_TIMEOUT","60.0"))

  if os.environ.get("LOAD_IDP_MCP") == "Y":

    idp_tools = MCPToolSetWithSchemaAccess(
                  connection_params=StdioConnectionParams(
                    server_params=StdioServerParameters(
                      command='python',
                      args=[ f"{uv_dir_prefix}/demo_idp/idp_mcp_server.py",
                              "--client-id",
                              os.environ.get("IDP_CLIENT_ID"),
                              "--client-secret",
                              os.environ.get("IDP_CLIENT_SECRET")
                            ]
                    ),
                  timeout=timeout),
                tool_set_name="demo_idp_tools",
                errlog=errlog_ae
                )

  logging.info("MCP Toolsets for IDP created successfully.")
  return [idp_tools]

tools:any = [item for item in get_all_tools() if item is not None]

demo_idp_agent = LlmAgent(
    model=os.environ.get("GOOGLE_MODEL"), 
    name="demo_idp_agent",
    instruction="You help users to gather information about their users/identities from their IDP backend to investigate. Do take calculated guesses based on your own knowledge base to help the user as much as you can, even if you may not know much about the IDP product itself. At the end of a query when there is some data do let them know your opinion and the steps you carried to achieve the output.",
    tools=tools,
    before_model_callback=bmc_trim_llm_request,
    description="You are the demo_idp_agent. Anything not related to IDP please delegate to google_mcp_security_agent"
)
