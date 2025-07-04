import os
import sys
import vertexai.agent_engines

# Get message from command line argument or environment variable
message = None
if len(sys.argv) > 1:
    message = " ".join(sys.argv[1:])
else:
    message = os.getenv("TEST_MESSAGE", "List MCP Tools")

# Get deployed agent from Agent Engine
resource_name = os.getenv("AGENT_ENGINE_RESOURCE")
print(f">>> 🤖 Connecting to agent: {resource_name}")
deployed_agent = vertexai.agent_engines.get(resource_name)
print(">>> ✅ Connected successfully")

# List Agent Engine sessions
response = deployed_agent.list_sessions(user_id="test_user")
if response:
    sessions = response.get("sessions")
else:
    sessions = None

# Use existing session if available, to showcase session state
if sessions:
    print(f">>> 🗃️  Found {len(sessions)} existing session(s)")
    # Use the first session
    session = sessions[0]
    print(f">>> 🗂️  Using session: {session['id']}")
    session = deployed_agent.get_session(user_id="test_user", session_id=session['id'])
    print(f">>> 🧠  Session state: {session['state']}")
else:
    # Create an Agent Engine session
    print(">>> 📝 Creating new session...")
    session = deployed_agent.create_session(user_id="test_user")
    print(f">>> 📝 Created session: {session['id']}")
    print(f">>> 🧠  Session state: {session['state']}")

# Use the session to chat with the agent
print(f">>> 💬 Sending message: {message}")
print(">>> 🤖 Agent response:")
response_received = False
for event in deployed_agent.stream_query(
        user_id="test_user",
        session_id=session['id'],
        message=message,
    ):
    print(f">>> Raw event: {event}")  # Debug: show raw event structure
    if 'content' in event and 'parts' in event['content'] and event['content']['parts']:
        content = event['content']['parts'][0]
        if content:
            print(f"<<< 🤖 {content}")
            response_received = True
    elif 'content' in event and event['content']:
        # Handle different response structure
        content = event['content']
        if isinstance(content, dict) and 'parts' in content:
            for part in content['parts']:
                if part and isinstance(part, dict) and 'text' in part:
                    print(f"<<< 🤖 {part['text']}")
                    response_received = True
                elif part:
                    print(f"<<< 🤖 {part}")
                    response_received = True
        else:
            print(f"<<< 🤖 {content}")
            response_received = True

if not response_received:
    print(">>> ❌ No response received from agent")

# Get session and see updated state
session = deployed_agent.get_session(user_id="test_user", session_id=session['id'])
print(f">>> 🧠  Final session state: {session['state']}")
print(">>> ✨ Test completed")