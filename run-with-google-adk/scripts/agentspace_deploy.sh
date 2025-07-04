#!/bin/bash
#
# AgentSpace Deployment Script for Google MCP Security Agent
# This script registers an agent with AgentSpace using environment variables
#

# Script directory
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ENV_FILE="${SCRIPT_DIR}/../google_mcp_security_agent/.env"

# Load environment variables
if [ -f "$ENV_FILE" ]; then
    # Export all variables from .env file
    export $(grep -v '^#' "$ENV_FILE" | xargs)
else
    echo "Error: Environment file not found: $ENV_FILE"
    echo "Please run 'make env-template' and configure your .env file"
    exit 1
fi

# Validate required environment variables
REQUIRED_VARS=(
    "AGENTSPACE_PROJECT_ID"
    "AGENTSPACE_PROJECT_NUMBER"
    "AGENTSPACE_APP_NAME"
    "AGENT_ENGINE_RESOURCE_NAME"
    "GOOGLE_CLOUD_LOCATION"
)

MISSING_VARS=()
for VAR in "${REQUIRED_VARS[@]}"; do
    if [ -z "${!VAR}" ]; then
        MISSING_VARS+=("$VAR")
    fi
done

if [ ${#MISSING_VARS[@]} -ne 0 ]; then
    echo "Error: Missing required environment variables:"
    for VAR in "${MISSING_VARS[@]}"; do
        echo "  - $VAR"
    done
    echo ""
    echo "Please set these variables in: $ENV_FILE"
    exit 1
fi

# Extract reasoning engine ID from full resource name
# Format: projects/PROJECT_NUMBER/locations/LOCATION/reasoningEngines/ENGINE_ID
REASONING_ENGINE_ID=$(echo "$AGENT_ENGINE_RESOURCE_NAME" | sed 's/.*reasoningEngines\///')

# Use environment variables with defaults
AGENT_DISPLAY_NAME="${AGENT_DISPLAY_NAME:-Google Security Agent}"
AGENT_DESCRIPTION="${AGENT_DESCRIPTION:-Allows security operations on Google Security Products}"
AGENT_TOOL_DESCRIPTION="${AGENT_TOOL_DESCRIPTION:-Various Tools from SIEM, SOAR and SCC}"
AGENTSPACE_COLLECTION="${AGENTSPACE_COLLECTION:-default_collection}"
AGENTSPACE_ASSISTANT="${AGENTSPACE_ASSISTANT:-default_assistant}"

# Construct API endpoint
TARGET_URL="https://discoveryengine.googleapis.com/v1alpha/projects/${AGENTSPACE_PROJECT_NUMBER}/locations/global/collections/${AGENTSPACE_COLLECTION}/engines/${AGENTSPACE_APP_NAME}/assistants/${AGENTSPACE_ASSISTANT}/agents"

# Build JSON payload
JSON_DATA=$(cat <<EOF
{
    "displayName": "${AGENT_DISPLAY_NAME}",
    "description": "${AGENT_DESCRIPTION}",
    "adk_agent_definition": {
        "tool_settings": {
            "tool_description": "${AGENT_TOOL_DESCRIPTION}"
        },
        "provisioned_reasoning_engine": {
            "reasoning_engine": "${AGENT_ENGINE_RESOURCE_NAME}"
        }
EOF
)

# Add OAuth authorization if configured
if [ -n "${OAUTH_AUTH_ID}" ]; then
    JSON_DATA="${JSON_DATA},
        \"authorizations\": [
            \"projects/${AGENTSPACE_PROJECT_NUMBER}/locations/global/authorizations/${OAUTH_AUTH_ID}\"
        ]"
fi

# Close the JSON structure
JSON_DATA="${JSON_DATA}
    }
}"

echo "AgentSpace Deployment Configuration:"
echo "===================================="
echo "Project ID: ${AGENTSPACE_PROJECT_ID}"
echo "Project Number: ${AGENTSPACE_PROJECT_NUMBER}"
echo "App Name: ${AGENTSPACE_APP_NAME}"
echo "Agent Display Name: ${AGENT_DISPLAY_NAME}"
echo "Agent Engine Resource: ${AGENT_ENGINE_RESOURCE_NAME}"
if [ -n "${OAUTH_AUTH_ID}" ]; then
    echo "OAuth Authorization: ${OAUTH_AUTH_ID}"
fi
echo ""
echo "API Endpoint: $TARGET_URL"
echo ""
echo "Request Body:"
echo "$JSON_DATA" | jq . 2>/dev/null || echo "$JSON_DATA"
echo ""

# Check if we're doing a dry run
if [ "$1" == "--dry-run" ]; then
    echo "DRY RUN: Would send the above request"
    exit 0
fi

echo "Sending POST request..."
echo ""

# Perform the POST request using curl
RESPONSE=$(curl -s -w "\n%{http_code}" -X POST \
     -H "Content-Type: application/json" \
     -H "Authorization: Bearer $(gcloud auth print-access-token)" \
     -H "X-Goog-User-Project: ${AGENTSPACE_PROJECT_ID}" \
     -d "$JSON_DATA" \
     "$TARGET_URL" 2>&1)

# Extract HTTP status code and response body
HTTP_CODE=$(echo "$RESPONSE" | tail -n1)
RESPONSE_BODY=$(echo "$RESPONSE" | sed '$d')

echo "HTTP Status Code: $HTTP_CODE"
echo ""

if [ "$HTTP_CODE" == "200" ]; then
    echo "✓ Agent registered successfully!"
    echo ""
    echo "Response:"
    echo "$RESPONSE_BODY" | jq . 2>/dev/null || echo "$RESPONSE_BODY"
    
    # Extract agent ID from response
    AGENT_ID=$(echo "$RESPONSE_BODY" | jq -r '.name' 2>/dev/null | sed 's/.*agents\///')
    if [ -n "$AGENT_ID" ] && [ "$AGENT_ID" != "null" ]; then
        echo ""
        echo "Agent ID: $AGENT_ID"
        echo ""
        echo "To save this ID to your environment:"
        echo "make env-update KEY=AGENTSPACE_AGENT_ID VALUE=$AGENT_ID"
    fi
else
    echo "✗ Failed to register agent"
    echo ""
    echo "Response:"
    echo "$RESPONSE_BODY" | jq . 2>/dev/null || echo "$RESPONSE_BODY"
    exit 1
fi

echo ""
echo "Next steps:"
echo "1. Open AgentSpace in Google Cloud Console"
echo "2. From left menu, click 'Integration'"
echo "3. Open the URL provided"
echo "4. From left menu, select your agent"
