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
SAMPLE_ENV_FILE="./google_mcp_security_agent/sample.env"
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

# Check for the existence of the files
if [ ! -f "$SAMPLE_ENV_FILE" ] && [ ! -f "$ENV_FILE" ]; then
  echo "Error: Missing both $SAMPLE_ENV_FILE and $ENV_FILE files."
  exit 1
elif [ -f "$SAMPLE_ENV_FILE" ] && [ ! -f "$ENV_FILE" ]; then
  echo "Copying $SAMPLE_ENV_FILE to $ENV_FILE..."
  cp "$SAMPLE_ENV_FILE" "$ENV_FILE"
  echo "Please update the environment variables in $ENV_FILE"
  exit 0
fi

# If .env exists, display its contents with masked values and run the command
show_env_masked

echo "Running adk web command..."
adk web # Execute the command
