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
from pydantic import BaseModel
from vertexai import agent_engines
# this makes sure that your prompts are logged. 
# super useful for debugging
import logging
logging.basicConfig(level=logging.INFO)

# Load environment variables from .env file in the parent directory
# Place this near the top, before using env vars like API keys
load_dotenv('./google_mcp_security_agent/.env')

app_name = os.environ.get("APP_NAME","ADK Agent")

app = FastAPI()

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

# Create 'static' directory if it doesn't exist
os.makedirs(static_dir, exist_ok=True)

app.mount("/static", StaticFiles(directory=static_dir), name="static")

# if os.environ.get("GOOGLE_API_KEY") == "NOT_SET":
#   print("Please set a Google API Key using - https://aistudio.google.com/app/apikey")
#   exit(1)

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


@app.get("/get_session")
async def get_session_and_user_id(username: str,start_new_session: str="N"):
    """
    Generates and Or get the first session
    """
    # in case username is not sent, use default_user
    user_id = "default_user" if username == "None" else username
    agent_resource=os.environ.get("AGENT_ENGINE_RESOURCE_NAME")
    print(f"Agent Resource - {agent_resource}")
    remote_app = agent_engines.get(agent_resource)
    print(f"Current User Id - {user_id}")
    remote_sessions = remote_app.list_sessions(user_id=user_id)
    print(f"remote_sessions - {remote_sessions}")
    session_available = False

    if start_new_session != "Y":
        if "sessions" in remote_sessions and len(remote_sessions["sessions"]) > 0:
            print(f"Fetched {len(remote_sessions)} sessions back",remote_sessions)
            print("using sesion 0")
            remote_session = remote_sessions["sessions"][0]
            session_available = True
    
    if not session_available:
        print("No sessions fetched for the given user and engine combination / or new requested - creating one")
        remote_session = remote_app.create_session(user_id=user_id)

    print(f"Using remote session -> {remote_session["id"]}")

    return {"session_id": remote_session["id"], "user_id": user_id}

def enrich_output(event):
    #print(event)
    msg_type = ""
    author = event["author"]
    message = ""

    if "content" in event and "parts" in event["content"]:
        author = author+ "-" + event["content"]["role"]
        if "text" in event["content"]["parts"][0]:
            message = event["content"]["parts"][0]["text"]
            if "partial" in event:
                msg_type="STC"#"Streaming Text Chunk"
                #print("  Type: Streaming Text Chunk")
            else:
                msg_type="CTC" #"Complete Text Message"            
        elif "function_call" in event["content"]["parts"][0]:
            msg_type="TCR"#"Tool Call Request"
            message = event["content"]["parts"][0]["function_call"]["name"]
            #print("  Type: Tool Call Request")
        elif "function_response" in event["content"]["parts"][0]:
            msg_type="TR"#"Tool Result"
            # in this case message is basically function name (same with TCR as well)
            message = event["content"]["parts"][0]["function_response"]["name"]
            #print("  Type: Tool Result")
        else:
            msg_type="OC"#"Other Content"
            #print("  Type: Other Content (e.g., code result)")
    elif "actions" in event and ("state_delta" in event["actions"] or "artifact_delta" in event["actions"]):
        msg_type="S/A U"#"State/Artifact Update"
        #print("  Type: State/Artifact Update")
    else:
        msg_type="CS/O"#"Control Signal or Other"
        #print("  Type: Control Signal or Other")  

    return(msg_type,author,message)


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

  remote_app = agent_engines.get(os.environ.get("AGENT_ENGINE_RESOURCE_NAME"))
  
  async def event_generator():

    for event in remote_app.stream_query(
            user_id=user_id,
            session_id=session_id,
            message=request_body.message,
        ):
            #print(event)
            #print(type(event)) # dict
            msg_type,author,message = enrich_output(event)
            data = {
            "text": f"<b>{msg_type}({author}) :</b> \n\n {message}",
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
# 2. Run the server: uvicorn main_ae:app --reload
# 3. Open your browser to http://localhost:8000/
