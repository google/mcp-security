# main.py
from fastapi import FastAPI
from fastapi.responses import StreamingResponse, HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import json
import os
from dotenv import load_dotenv
from google.genai import types
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.adk.artifacts.in_memory_artifact_service import InMemoryArtifactService # Optional
import sys 
from contextlib import asynccontextmanager # Import for lifespan

# this makes sure that your prompts are logged. 
# super useful for debugging
import logging
logging.basicConfig(level=logging.INFO)

# Load environment variables from .env file in the parent directory
# Place this near the top, before using env vars like API keys
load_dotenv('./google_mcp_security_agent/.env')
from google_mcp_security_agent import agent

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
    # We are not doing this here anymore - as we do it on event exhaustion
    # because otherwise 
    # as every invocation runs new MCP server(s) the uv processes keep running.

    for session_id in session_runner_map:
        print(f"Start-Cleaning up resources for Session[{session_id}]")
        tools = session_runner_map[session_id].agent.root_agent.tools
        for mcp_toolset in tools:
            print(f"Closing {mcp_toolset}")
            await mcp_toolset.close()
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

session_service = InMemorySessionService()

# Artifact service might not be needed for this example
artifacts_service = InMemoryArtifactService()


# Create 'static' directory if it doesn't exist
os.makedirs(static_dir, exist_ok=True)

app.mount("/static", StaticFiles(directory=static_dir), name="static")

if os.environ.get("GOOGLE_API_KEY") == "NOT_SET":
  print("Please set a Google API Key using - https://aistudio.google.com/app/apikey")
  exit(1)

session_runner_map={}


@app.get("/", response_class=HTMLResponse)
async def read_root():
    """Serves the index.html file when the root URL is accessed."""
    with open(os.path.join(static_dir, "index.html"), "r") as f:
        return HTMLResponse(content=f.read())

@app.get("/get_session")
async def get_session_id():
    """
    Generates and returns a unique session ID.
    """
    session = await session_service.create_session(
        state={"user_name":"James"}, app_name='google_security_agent', user_id='analyst01'
    )

    root_agent = agent.root_agent


    runner = Runner(
        app_name='google_security_agent',
        agent=root_agent ,
        artifact_service=artifacts_service, # Optional
        session_service=session_service,
    )    
    session_runner_map[session.id] = runner
    return {"session_id": session.id}

def enrich_output(event):
    type = ""
    author = event.author
    message = ""

    if event.content and event.content.parts:
        author = event.content.role
        message = event.content.parts[0].text
        if event.get_function_calls():
            type="Tool Call Request"
            message = event.get_function_calls()[0].name
            #print("  Type: Tool Call Request")
        elif event.get_function_responses():
            type="Tool Result"
            message = event.get_function_responses()[0].name
            #print("  Type: Tool Result")
        elif event.content.parts[0].text:
            if event.partial:
                type="Streaming Text Chunk"
                #print("  Type: Streaming Text Chunk")
            else:
                type="Complete Text Message"
                # print("  Type: Complete Text Message")
            #print(event.content.parts[0].text)                  
        else:
            type="Other Content"
            #print("  Type: Other Content (e.g., code result)")
    elif event.actions and (event.actions.state_delta or event.actions.artifact_delta):
        type="State/Artifact Update"
        #print("  Type: State/Artifact Update")
    else:
        type="Control Signal or Other"
        #print("  Type: Control Signal or Other")  

    return(type,author,message)


@app.get("/chat")
async def chat_endpoint(message: str,session_id: str):

  content = types.Content(role='user', parts=[types.Part(text=message)])
  runner = session_runner_map[session_id] 
  # todo get user from session  
  events_async = runner.run_async(
        session_id=session_id, user_id='analyst01', new_message=content
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
    # yield statement is like return so following code is not executed when there are events still
    final_data = {
        "text": "Stream finished.", # You can customize this final message or make it empty
        "last_msg": True
    }
    yield f"data: {json.dumps(final_data)}\n\n"


#   # as a new server is run for every request.
#   # let's do the cleanup.
#   logging.info(f"Closing MCP server connections, for {len(agent.root_agent.tools)} MCP Toolsets")
#   for mcp_toolset in agent.root_agent.tools:
#        logging.info(f"Closing {mcp_toolset} for {mcp_toolset._connection_params.args[1]}")
#        try:
#            await mcp_toolset.close()
#        except:
#            logging.warning(f"There was an exception closing the toolset {sys.exc_info()[0]}")
#   logging.info("Cleanup complete.")

  return StreamingResponse(event_generator(), media_type="text/event-stream")

# To run this application:
# 1. Save the above code as main.py
# 2. Make sure you have a 'static' directory in the same location as main.py.
#    The script will create dummy index.html and app.js inside 'static' if they don't exist.
# 3. Install dependencies: pip install -r requirements.txt
# 4. Run the server: uvicorn main:app --reload
# 5. Open your browser to http://localhost:8000/
