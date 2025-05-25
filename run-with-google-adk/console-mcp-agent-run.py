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
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.adk.artifacts.in_memory_artifact_service import InMemoryArtifactService # Optional
import logging
import os
import time

# Load environment variables from .env file in the parent directory
# Place this near the top, before using env vars like API keys
load_dotenv('./google_mcp_security_agent/.env')
logging.basicConfig(level=os.environ.get("LOGGING_LEVEL",logging.ERROR))

from google_mcp_security_agent import agent


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


# --- Main Execution Logic ---
async def async_main():
  session_service = InMemorySessionService()
  artifacts_service = InMemoryArtifactService()

  session = await session_service.create_session(
      state={}, app_name='mcp_security_app', user_id='security_user'
  )

  runner = Runner(
      app_name='mcp_security_app',
      agent=agent.root_agent,
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
  for mcp_toolset in agent.root_agent.tools:
    print(f"Closing {mcp_toolset}")
    await mcp_toolset.close()
  print("Cleanup complete.")

if __name__ == '__main__':
  try:
    asyncio.run(async_main())
  except Exception as e:
    print(f"An error occurred: {e}")