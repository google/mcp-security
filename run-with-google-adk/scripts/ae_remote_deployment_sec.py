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

import dotenv
import os
import sys


# Load .env file with error checking
env_file_path = "./agents/google_mcp_security_agent/.env"
print(f"Attempting to load .env file from: {env_file_path}")

if not os.path.exists(env_file_path):
    print("=" * 80)
    print("CRITICAL ERROR: .env file not found!")
    print(f"Expected location: {env_file_path}")
    print("This will cause ALL MCP servers to be DISABLED!")
    print("Available .env files:")
    for root, dirs, files in os.walk("."):
        for file in files:
            if file.endswith('.env') or '.env' in file:
                print(f"   Found: {os.path.join(root, file)}")
    print("=" * 80)
    sys.exit(1)

dotenv.load_dotenv(env_file_path)
print(f"✅ Successfully loaded .env file from: {env_file_path}")

import vertexai
import sys

PROJECT_ID = os.environ.get("GOOGLE_CLOUD_PROJECT")
LOCATION = os.environ.get("GOOGLE_CLOUD_LOCATION")
STAGING_BUCKET = os.environ.get("AE_STAGING_BUCKET")

if not STAGING_BUCKET.startswith("gs://"):
    STAGING_BUCKET="gs://"+STAGING_BUCKET

vertexai.init(
    project=PROJECT_ID,
    location=LOCATION,
    staging_bucket=STAGING_BUCKET
)

# TODO add check for number of params.
env_vars = sys.argv[1]
env_vars_list=env_vars.split(",")

print(f"Raw environment variables string from command line: '{env_vars}'")
print(f"Parsed environment variables list: {env_vars_list}")

if not env_vars or env_vars.strip() == "" or env_vars_list == ['']:
    print("=" * 80)
    print("CRITICAL ERROR: No environment variables provided!")
    print("This means ALL MCP servers will be DISABLED!")
    print("The .env file processing failed in the calling script.")
    print("Check that the .env file exists and contains valid KEY=VALUE pairs.")
    print("=" * 80)
    sys.exit(1)

update=sys.argv[2]
update_resource_name=sys.argv[3]

env_vars_to_send = {}

for key in env_vars_list:
    if key not in ["GOOGLE_CLOUD_PROJECT","GOOGLE_CLOUD_LOCATION"]: # These are not allowed as env variables on the AE, filtering them.
        value = os.environ.get(key)
        env_vars_to_send[key] = value
        if value is None:
            print(f"⚠️  WARNING: Environment variable '{key}' is None/missing!")
        else:
            # Only show first few chars of sensitive values
            display_value = value[:10] + "..." if len(value) > 10 else value
            print(f"✅ Environment variable '{key}': {display_value}")

# Check specifically for MCP loader variables
mcp_vars = [k for k in env_vars_to_send.keys() if k.startswith('LOAD_') and k.endswith('_MCP')]
enabled_mcp = [k for k in mcp_vars if env_vars_to_send.get(k, '').lower() == 'true']

print(f"📊 MCP Status Summary:")
print(f"   Total MCP loader variables found: {len(mcp_vars)}")
print(f"   Enabled MCP servers: {len(enabled_mcp)}")
print(f"   Enabled servers: {enabled_mcp}")

if len(enabled_mcp) == 0:
    print("=" * 80)
    print("CRITICAL WARNING: NO MCP SERVERS ARE ENABLED!")
    print("The deployed agent will have no security tools available!")
    print("This is likely not what you want!")
    print("=" * 80)

# override
env_vars_to_send['GOOGLE_GENAI_USE_VERTEXAI'] = 'True'

# important for pickling
os.environ["AE_RUN"] = "Y"

env_vars_to_send['REMOTE_RUN'] = 'Y'
env_vars_to_send['AE_RUN'] = 'Y'


# # remote deplyment and first run
# # remote run
from vertexai import agent_engines
from agents.google_mcp_security_agent import agent

print(f"env_vars_to_send => {env_vars_to_send}")

if update == "n":
    print("Creating a new Agent Engine Agent")
    remote_app = agent_engines.create(
    # Mostly for agent engine Console.
    display_name="google_security_agent",description="Allows security actions on various google security products",
    agent_engine=agent.root_agent,
    requirements="requirements.txt",
    extra_packages=[
        "./agents/google_mcp_security_agent", # a directory
        "./libs/adk_utils", # a directory
        "./server", # a directory
        #"./temp",
        #"./object-viewer-sa.json", # a file
    ],
    env_vars=env_vars_to_send # send all required variables to agent engine.
    )

    # This is just for testing after the deployment.
    remote_session = remote_app.create_session(user_id="test_user")
    remote_session

    for event in remote_app.stream_query(
        user_id="test_user",
        session_id=remote_session["id"],
        message="what can you do?",
    ):
        print(event)

else:
    import datetime
    now = datetime.datetime.now()
    print(f"Updating the existing Agent Engine Agent {update_resource_name}")
    remote_app = agent_engines.update(
    resource_name=update_resource_name,
    # Mostly for agent engine Console.
    display_name="google_security_agent",description=f"Allows security actions on various google security products, updated {now.strftime("%Y_%m_%d_%H_%M_%S_%f")}",
    agent_engine=agent.root_agent,
    requirements="requirements.txt",
    extra_packages=[
        "./agents/google_mcp_security_agent", # a directory
        "./libs/adk_utils", # a directory
        "./server", # a directory
        "./temp",
        "./object-viewer-sa.json", # a file
    ],
    env_vars=env_vars_to_send # send all required variables to agent engine.
    )
