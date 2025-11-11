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

ENV_FILE="./google_mcp_security_agent/.env"

list_of_vars=`cat $ENV_FILE  | grep = | grep -v ^# | cut -d "=" -f1 | tr "\n" "," | sed s/,$//g`

update="n"
update_resource_name="not_available"

if [[ $# -eq 1 ]]; then
  update="y"
  update_resource_name=$1
fi

echo "Copying ../server directory to current directory"
cp -r ../server .

echo "Running AE deployment ..."

python ae_remote_deployment_sec.py $list_of_vars $update $update_resource_name

deploy_status=$? #get the status

# Check the status of the deployment
if [ "$deploy_status" -eq 0 ]; then
  # Deleting temporarily files in the top level directory 
  echo "Deleting temporarily copied server directory."
  rm -Rf ./server
  echo "Successfully deployed the agent."
else
  rm -Rf ./server
  echo "Failed to deploy the agent."
  exit 1
fi



