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

#!/bin/bash

ENV_FILE="./agents/google_mcp_security_agent/.env"

# Check if .env file exists at the expected location
if [ ! -f "$ENV_FILE" ]; then
    echo "=================================================================================="
    echo "CRITICAL ERROR: .env file not found at expected location: $ENV_FILE"
    echo "This will cause ALL MCP servers to be DISABLED in the deployment!"
    echo "Expected file location: $ENV_FILE"
    echo "Available .env files found:"
    find . -name "*.env*" -type f 2>/dev/null || echo "🚨 No .env files found in current directory tree"
    echo "=================================================================================="
    echo "DEPLOYMENT WILL FAIL - Please fix the .env file path before continuing"
    echo "=================================================================================="
    exit 1
fi

echo "Found .env file at: $ENV_FILE"
list_of_vars=`cat $ENV_FILE  | grep = | grep -v ^# | cut -d "=" -f1 | tr "\n" "," | sed s/,$//g`

if [ -z "$list_of_vars" ]; then
    echo "=================================================================================="
    echo "WARNING: No environment variables extracted from .env file!"
    echo "This will cause ALL MCP servers to be DISABLED in the deployment!"
    echo "Check that your .env file contains uncommented KEY=VALUE pairs"
    echo "=================================================================================="
    exit 1
fi

echo "Extracted environment variables: $list_of_vars"

update="n"
update_resource_name="not_available"

if [[ $# -eq 1 ]]; then
  update="y"
  update_resource_name=$1
fi

echo "Copying ../server directory to current directory"
cp -r ../server .

echo "Copying libs directory to agent directory for ADK staging"
cp -r ../libs ./agents/google_mcp_security_agent/

echo "Running AE deployment ..."

python ae_remote_deployment_sec.py $list_of_vars $update $update_resource_name

deploy_status=$? #get the status

# Check the status of the deployment
if [ "$deploy_status" -eq 0 ]; then
  # Deleting temporarily files in the top level directory
  echo "Deleting temporarily copied server directory."
  rm -Rf ./server
  echo "Deleting temporarily copied libs directory."
  rm -Rf ./agents/google_mcp_security_agent/libs
  echo "Successfully deployed the agent."
else
  rm -Rf ./server
  rm -Rf ./agents/google_mcp_security_agent/libs
  echo "Failed to deploy the agent."
  exit 1
fi



