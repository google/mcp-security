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

# Query the agent directly without sessions
print(f">>> 💬 Sending message: {message}")
print(">>> 🤖 Agent response:")

try:
    # Try direct query without session
    response = deployed_agent.query(message=message)
    print(response)
except Exception as e:
    print(f"❌ Error querying agent: {e}")
    print("\n>>> Trying invoke method instead...")
    try:
        # Alternative: try invoke method
        response = deployed_agent.invoke({"message": message})
        print(response)
    except Exception as e2:
        print(f"❌ Error invoking agent: {e2}")

print(">>> ✨ Test completed")