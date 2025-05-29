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

import asyncio
from dotenv import load_dotenv
from google.genai import types
from google.adk.agents.llm_agent import LlmAgent
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.adk.artifacts.in_memory_artifact_service import InMemoryArtifactService # Optional
from google.adk.tools.mcp_tool.mcp_toolset import MCPToolset, SseServerParams, StdioServerParameters
import logging
import os
import time
from contextlib import AsyncExitStack

# Load environment variables from .env file in the parent directory
# Place this near the top, before using env vars like API keys
load_dotenv('./google-mcp-security-agent/.env')


logging.basicConfig(level=os.environ.get("LOGGING_LEVEL",logging.ERROR))

def print_event(event):
   debug_str = f"ET {event.timestamp} PT {time.time()}"
   if event.content != None:
      debug_str += f" R {event.content.role}"
   else:
      debug_str += f" NO_CONTENT"    
   if os.environ.get("PRINT_EVENT_DETAILS","VERBOSE") == "VERBOSE":
      if event.content and event.content.parts:
          if event.get_function_calls():
              debug_str += " T TCR" # Tool Call Request
          elif event.get_function_responses():
              debug_str += " T TR" # Tool Result
          elif event.content.parts[0].text:
              if event.partial:
                  debug_str += " T STC" # Streaming Text Chunk
              else:
                  debug_str += " T CTC" #Complete Text Message
          else:
              debug_str += " T OC" # Other Content (e.g., code result)
      elif event.actions and (event.actions.state_delta or event.actions.artifact_delta):
          debug_str += " T S/AU" # State/Artifact Update
      else:
          debug_str += " T CS/O" # Control Signal or Other
   
   print(f"[{debug_str}]")
   if event.content != None and event.content.parts[0].text:
      print(event.content.parts[0].text)


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

async def get_all_tools():
  """Get Tools from All MCP servers"""
  logging.info("Attempting to connect to MCP servers...")
  secops_tools = []
  gti_tools = []
  secops_soar_tools = []
  scc_tools = []
  compliance_tools = []
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
  all_tools = secops_tools + gti_tools + secops_soar_tools + scc_tools + compliance_tools
  return all_tools, exit_stack

async def get_agent_async():
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
      model= os.environ.get("GOOGLE_MODEL"), 
      name='google_security_assistant',
      instruction=os.environ.get("DEFAULT_PROMPT"),
      tools=tools 
  )
  return agent, exit_stack

# --- Step 3: Main Execution Logic ---
async def async_main():
  session_service = InMemorySessionService()
  artifacts_service = InMemoryArtifactService()

  session = session_service.create_session(
      state={}, app_name='mcp_security_app', user_id='security_user'
  )


  root_agent, exit_stack = await get_agent_async()

  runner = Runner(
      app_name='mcp_security_app',
      agent=root_agent,
      artifact_service=artifacts_service, # Optional
      session_service=session_service,
  )
  query = ""
  while query != "bye":
    query = input(">")
    content = types.Content(role='user', parts=[types.Part(text=query)])

    events_async = runner.run_async(
        session_id=session.id, user_id=session.user_id, new_message=content
    )

    async for event in events_async:
      print_event(event)


  # Crucial Cleanup: Ensure the MCP server process connection is closed.
  print("Closing MCP server connection...")
  await exit_stack.aclose()
  print("Cleanup complete.")

if __name__ == '__main__':
  try:
    asyncio.run(async_main())
  except Exception as e:
    print(f"An error occurred: {e}")
