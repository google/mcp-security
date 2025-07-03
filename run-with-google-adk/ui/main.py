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


# main.py
from fastapi import FastAPI, HTTPException
from fastapi.responses import StreamingResponse, HTMLResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import json
import os
from dotenv import load_dotenv
from google.genai import types
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService, DatabaseSessionService
from google.adk.artifacts.in_memory_artifact_service import InMemoryArtifactService
from google.adk.artifacts.gcs_artifact_service import GcsArtifactService
from contextlib import asynccontextmanager # Import for lifespan
from pydantic import BaseModel
from google.adk.tools.mcp_tool.mcp_toolset import MCPToolset

# this makes sure that your prompts are logged. 
# super useful for debugging
import logging
logging.basicConfig(level=logging.INFO)

# Load environment variables from .env file in the parent directory
# Place this near the top, before using env vars like API keys
load_dotenv('./google_mcp_security_agent/.env')
from google_mcp_security_agent import agent

app_name = os.environ.get("APP_NAME","ADK Agent")

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup event: Initialize resources
    print("Application starting up...")
    # Example: You might initialize a global database connection pool here
    # global_db_connection = await connect_to_db()

    # For our session_runner_map, we don't need to initialize it here
    # as runners are created on demand. But if you had a fixed pool, this is the place.

    yield # The application will now start serving requests

    # Shutdown event: Clean up resources
    print("Application shutting down...")
    for session_id in session_runner_map:
        print(f"Start-Cleaning up resources for Session[{session_id}]")
        tools = session_runner_map[session_id].agent.tools
        for mcp_toolset in tools:
            # only need to close MCP toolsets and not function tools
            print(f"Closing [{mcp_toolset}] of type  - [{type(mcp_toolset)}]")
            if isinstance(mcp_toolset,MCPToolset):
                await mcp_toolset.close()
            else:
                print(f"skipping {mcp_toolset}")                
        print(f"Done-Cleaning up resources for Session[{session_id}]")    

        # You could also delete the session if you wanted but generally not needed
        # for inmemory session service and for db session service we do not want it to be deleted.
        # also as such the MCPToolSet has a session shutdown method. which is more appropriate.
        # so commenting out
        # print(f"Start-Deleting session {session_id}")
        # await session_service.delete_session(app_name='repair_world_app', user_id='customer',session_id=session_id)
        # print(f"Done-Deleting session {session_id}")

    print("All session resources cleaned up.")
    # Example: Close global database connection
    # await global_db_connection.close()

app = FastAPI(lifespan=lifespan)

# Configure CORS to allow requests from the frontend (running on a different port/origin)
# Adjust origins as needed for your deployment environment
origins = [
    "http://localhost",
    "http://localhost:8000", # FastAPI's default port
    "http://localhost:5500", # Common for Live Server in VS Code
    "http://127.0.0.1:5500",
    "http://127.0.0.1:8000",
    "*"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount static files to serve index.html and app.js
# Ensure 'static' directory exists in the same location as main.py
current_dir = os.path.dirname(os.path.abspath(__file__))
static_dir = os.path.join(current_dir, "static")

# TODO Vertex AI session service
print(f"Session Service Type - {os.environ.get("SESSION_SERVICE","in_memory")}")
session_service = InMemorySessionService()
if os.environ.get("SESSION_SERVICE","in_memory") == "db":
    db_url = os.environ.get("SESSION_SERVICE_URL","sqlite:///./agent_data.db")
    session_service = DatabaseSessionService(db_url=db_url)

# Artifact service might not be needed for this example
print(f"Artifact Service Type - {os.environ.get("ARTIFACT_SERVICE","in_memory")}")
artifacts_service = InMemoryArtifactService()
if os.environ.get("ARTIFACT_SERVICE","gcs") == "gcs":
    artifacts_service = GcsArtifactService(bucket_name=os.environ.get("GCS_ARTIFACT_SERVICE_BUCKET"))

# Create 'static' directory if it doesn't exist
os.makedirs(static_dir, exist_ok=True)

app.mount("/static", StaticFiles(directory=static_dir), name="static")

# if os.environ.get("GOOGLE_API_KEY") == "NOT_SET":
#   print("Please set a Google API Key using - https://aistudio.google.com/app/apikey")
#   exit(1)

session_runner_map={}


@app.get("/", response_class=HTMLResponse)
async def read_root():
    """Serves the index.html (login page) when the root URL is accessed."""
    index_html_path = os.path.join(static_dir, "index.html")
    if not os.path.exists(index_html_path):
        raise HTTPException(status_code=404, detail="index.html not found in static directory.")
    with open(index_html_path, "r") as f:
        return HTMLResponse(content=f.read())

@app.get("/landing.html", response_class=HTMLResponse)
async def read_landing():
    """Serves the landing.html (chat page)."""
    landing_html_path = os.path.join(static_dir, "landing.html")
    if not os.path.exists(landing_html_path):
        raise HTTPException(status_code=404, detail="landing.html not found in static directory.")
    with open(landing_html_path, "r") as f:
        return HTMLResponse(content=f.read())

@app.get("/app_name")
async def get_app_name():
    """Returns the application name."""
    return JSONResponse(content={"app_name": app_name})

async def create_new_session(username):
    user_id = username # For simplicity, user_id is the username
    initial_state = {
        "user_name":f"{user_id}"
    }
    session = await session_service.create_session(
        state=initial_state, app_name=app_name, user_id=user_id
    )
    logging.info(f"Created session {session.id} for (app_name={app_name}, user_id={user_id}) with user - {session.state['user_name']}")
    return session

@app.get("/get_session")
async def get_session_and_user_id(username: str,start_new_session: str="N"):
    """
    Generates and Or get the first session
    """
    # in case username is not sent, use default_user
    user_id = "default_user" if username == "None" else username

    if start_new_session == "Y":
        logging.info(f"Fresh session requested for {username}")
        session = await create_new_session(username)
    else:
        list_session_response = await session_service.list_sessions(app_name=app_name, user_id=user_id)
        if len(list_session_response.sessions) > 0:
            session = list_session_response.sessions[0]
            logging.info(f"Retrieved session - {session.id}")
        else:
            session = await create_new_session(username)                        

    root_agent = agent.root_agent

    runner = Runner(
        app_name=app_name,
        agent=root_agent,
        artifact_service=artifacts_service, # Optional
        session_service=session_service,
    )    
    # TODO - Check if we could use a new running without any performance degradation
    session_runner_map[session.id] = runner
    return {"session_id": session.id, "user_id": user_id}

def enrich_output(event):
    type = ""
    author = event.author
    message = ""

    if event.content and event.content.parts:
        author = author+ "-" + event.content.role
        message = event.content.parts[0].text
        if event.get_function_calls():
            type="TCR"#"Tool Call Request"
            message = event.get_function_calls()[0].name
            #print("  Type: Tool Call Request")
        elif event.get_function_responses():
            type="TR"#"Tool Result"
            # in this case message is basically function name (same with TCR as well)
            message = event.get_function_responses()[0].name
            #print("  Type: Tool Result")
        elif event.content.parts[0].text:
            if event.partial:
                type="STC"#"Streaming Text Chunk"
                #print("  Type: Streaming Text Chunk")
            else:
                type="CTC" #"Complete Text Message"
                # print("  Type: Complete Text Message")
            #print(event.content.parts[0].text)                  
        else:
            type="OC"#"Other Content"
            #print("  Type: Other Content (e.g., code result)")
    elif event.actions and (event.actions.state_delta or event.actions.artifact_delta):
        type="S/A U"#"State/Artifact Update"
        #print("  Type: State/Artifact Update")
    else:
        type="CS/O"#"Control Signal or Other"
        #print("  Type: Control Signal or Other")  

    return(type,author,message)


# Define the structure for the POST request body
class ChatRequest(BaseModel):
    session_id: str
    user_id: str
    message: str

@app.post("/chat")
async def chat_endpoint(request_body: ChatRequest):

  session_id = request_body.session_id
  user_id = request_body.user_id
  message = request_body.message

  content = types.Content(role='user', parts=[types.Part(text=message)])
  runner = session_runner_map[session_id] 
  # todo get user from session  
  events_async = runner.run_async(
        session_id=session_id, user_id=user_id, new_message=content
    )
  
  async def event_generator():
    async for event in events_async:
        type,author,message = enrich_output(event)
        # if event.content and event.content.parts:
        data = {
            "text": f"<b>{type}({author}) :</b> \n\n {message}",
            "last_msg": False
        }    
        yield f"data: {json.dumps(data)}\n\n"

    # Once the async for loop finishes, it means events_async has been exhausted.
    # Now, send the final "last_msg" signal.
    final_data = {
        "text": "Stream finished.", # You can customize this final message or make it empty
        "last_msg": True
    }
    yield f"data: {json.dumps(final_data)}\n\n"

  return StreamingResponse(event_generator(), media_type="text/event-stream")

# To run this application:
# 1. Install dependencies: pip install -r requirements.txt
# 2. Run the server: uvicorn main:app --reload
# 3. Open your browser to http://localhost:8000/
