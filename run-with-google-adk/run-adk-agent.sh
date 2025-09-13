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

# Define the file paths
SAMPLE_ENV_FILE="./google_mcp_security_agent/sample.env.properties"
ENV_FILE="./google_mcp_security_agent/.env"

# Function to mask environment variable values
mask_env_value() {
  local value="$1"
  local length="${#value}"
  local max_length=30 # Define the maximum length

  if [ "$length" -gt 3 ]; then
    masked_value=$(printf "%.3s%${length}s" "$value" "" | sed "s/ /#/g")
    if [ ${#masked_value} -gt $max_length ]; then
      echo "${masked_value:0:$max_length}" # truncate to max length
    else
      echo "$masked_value"
    fi
  else
    echo "$value"
  fi
}

# Function to display the contents of the .env file with masked values
show_env_masked() {
  if [ -f "$ENV_FILE" ]; then
    echo "Contents of .env (with masked values):"
    while IFS='=' read -r key value; do
      if [[ "$key" != "#"* ]]; then # Ignore comments
        if [ -n "$key" ]; then #check if key is not empty
          masked_value=$(mask_env_value "$value")
          echo "$key=$masked_value"
        fi
      else
        echo "$key$value" # print comments as is
      fi
    done < "$ENV_FILE"
  else
    echo ".env file does not exist."
  fi
}


#!/bin/bash

# Define a function to display usage instructions
usage() {
    echo "Usage: $0 <command> [args...]"
    echo ""
    echo "Commands:"
    echo "  adk_web                  : Runs ADK Web for local agent."
    echo "  adk_web <session_uri>    : Runs ADK Web with a session service URI."
    echo "  adk_web <session_uri> <artifact_uri> : Runs ADK Web with session and artifact service URIs."
    echo "  custom_ui                : Runs Custom UI for local agent (uvicorn main:app --reload)."
    echo "  custom_ui_ae             : Runs Custom UI for Agent Engine Backend (uvicorn main_ae:app --reload)."
    echo ""
    echo "Examples:"
    echo "  $0 adk_web"
    echo "  $0 adk_web http://localhost:8000"
    echo "  $0 adk_web http://localhost:8000 http://localhost:8001"
    echo "  $0 custom_ui"
    echo "  $0 custom_ui_ae"
    echo "  $0 # (will show usage)"
    exit 1
}

# Get the first argument, which is the command.
# If no argument is provided, COMMAND will be an empty string.
COMMAND="$1"

# If no command is provided (i.e., zero arguments), or if the provided command is unknown,
# display the usage instructions.
if [ -z "$COMMAND" ]; then
    echo "No command provided, Checking environment file status..."
    COMMAND="env_files"
fi

# Use a case statement to handle different commands
case "$COMMAND" in
    adk_web)
        # If .env exists, display its contents with masked values and run the command
        show_env_masked
        # Handle adk_web command based on argument count
        if [ "$#" -eq 1 ]; then
            echo "Running ADK Web for local agent..."
            adk web
        elif [ "$#" -eq 2 ]; then
            echo "Running ADK Web with session service URI: $2"
            adk web --session_service_uri "$2"
        elif [ "$#" -eq 3 ]; then
            echo "Running ADK Web with session service URI: $2 and artifact service URI: $3"
            adk web --session_service_uri "$2" --artifact_service_uri "$3"
        else
            echo "Error: Incorrect number of arguments for 'adk_web'."
            usage
        fi
        ;;
    custom_ui)
        show_env_masked    
        # Ensure that 'custom_ui' and 'custom_ui_ae' are only called with 1 argument.
        if [ "$#" -ne 1 ]; then
            echo "Error: 'custom_ui' expects no additional arguments."
            usage
        fi
        echo "Running Custom UI for local agent ..."
        uvicorn main:app --reload
        ;;
    custom_ui_ae)
        show_env_masked
        # Ensure that 'custom_ui' and 'custom_ui_ae' are only called with 1 argument.
        if [ "$#" -ne 1 ]; then
            echo "Error: 'custom_ui_ae' expects no additional arguments."
            usage
        fi
        echo "Running Custom UI for Agent Engine Backend ..."
        uvicorn main_ae:app --reload
        ;;
    env_files)
        # Check for the existence of the files
        if [ ! -f "$SAMPLE_ENV_FILE" ] && [ ! -f "$ENV_FILE" ]; then
          echo "Error: Missing both $SAMPLE_ENV_FILE and $ENV_FILE files."
          exit 1
        elif [ -f "$SAMPLE_ENV_FILE" ] && [ ! -f "$ENV_FILE" ]; then
          echo "Copying $SAMPLE_ENV_FILE to $ENV_FILE..."
          cp "$SAMPLE_ENV_FILE" "$ENV_FILE"
          echo "Please update the environment variables in $ENV_FILE"
          exit 0
        else
          echo "Environment file ok, please check the usage below"
          usage
        fi    
        ;;
    *)
        # Default case for unknown commands when an argument *was* provided.
        echo "Error: Unknown command '$COMMAND'."
        usage  
        ;;
esac


