# Agentspace App Setup Guide

This guide walks you through creating and configuring a Google Agentspace application, which is a prerequisite for deploying your MCP Security Agent with Agentspace integration.

## Overview

Agentspace is Google's platform for building and deploying conversational AI agents. Before you can integrate your MCP Security Agent with Agentspace, you need to:

1. Create an Agentspace application
2. Configure the necessary permissions and APIs
3. Obtain the required configuration values for your `.env` file

## Prerequisites

Before starting, ensure you have:
- A Google Cloud project with billing enabled
- Administrative access to your Google Cloud project
- Discovery Engine API enabled in your project
- Vertex AI API enabled in your project

## Step 1: Enable Required APIs

First, enable the necessary Google Cloud APIs:

```bash
# Enable Discovery Engine API (required for Agentspace)
gcloud services enable discoveryengine.googleapis.com

# Enable Vertex AI API (required for Agent Engine)
gcloud services enable aiplatform.googleapis.com

# Verify APIs are enabled
gcloud services list --enabled --filter="name:discoveryengine.googleapis.com OR name:aiplatform.googleapis.com"
```

## Step 2: Set Up IAM Permissions

Ensure your account has the necessary permissions:

```bash
# Check current permissions
gcloud projects get-iam-policy $GOOGLE_CLOUD_PROJECT

# Add necessary roles (if not already present)
gcloud projects add-iam-policy-binding $GOOGLE_CLOUD_PROJECT \
    --member="user:your-email@domain.com" \
    --role="roles/discoveryengine.admin"

gcloud projects add-iam-policy-binding $GOOGLE_CLOUD_PROJECT \
    --member="user:your-email@domain.com" \
    --role="roles/aiplatform.user"
```

**Required Roles:**
- `roles/discoveryengine.admin` - Create and manage Agentspace apps
- `roles/aiplatform.user` - Deploy and manage Agent Engine resources
- `roles/iam.serviceAccountTokenCreator` - Generate access tokens for API calls

## Step 3: Create Agentspace Application

### 3.1 Access the Agentspace Console

1. **Navigate to Discovery Engine Console**
   - Go to [Google Cloud Console - Agentspace](https://console.cloud.google.com/gen-app-builder/engines)
   - Ensure you're in the correct project

2. **Create a New App**
   - Click "Create App"
   - Choose "Agentspace (Preview)" as the app type and click Create
   - Select your preferred region (e.g., `global`, `us`, or `eu`)

### 3.2 Configure Your Agentspace App

**Basic Configuration:**
- **App Name**: Choose a descriptive App name (e.g., "MCP Security Agent")
- **App ID**: This will be auto-generated (e.g., `mcp-security-agent-app_1234567890`)
- **Location**: Choose the same region as your other resources


### 3.3 App Creation Results

After creating your app, note these important values:

1. **App Name**: The full app identifier (e.g., `mcp-security-agent-app_1234567890`)
2. **Project Number**: Your Google Cloud project number (numeric)
3. **Location**: The region where your app is deployed

## Step 4: Obtain Configuration Values

### 4.1 Get Project Number

```bash
# Get your project number
gcloud projects describe $GOOGLE_CLOUD_PROJECT --format="value(projectNumber)"
```

### 4.2 Get App Information

```bash
# List your Agentspace apps
gcloud alpha discovery-engine engines list --location=$LOCATION --project=$GOOGLE_CLOUD_PROJECT

# Get specific app details
gcloud alpha discovery-engine engines describe YOUR_APP_NAME \
    --location=$LOCATION \
    --project=$GOOGLE_CLOUD_PROJECT
```

### 4.3 Update Your .env File

Add the Agentspace configuration to your `.env` file:

```bash
# Agentspace Configuration
AGENTSPACE_PROJECT_NUMBER=1234567890                        # Your Google Cloud project number
AGENTSPACE_APP_NAME=mcp-security-agent-app_1234567890      # Agentspace app identifier
AGENTSPACE_AGENT_ID=                                        # Populated when agent is registered with Agentspace
```

**Using Make Commands:**

```bash
# Update project number
make env-update KEY=AGENTSPACE_PROJECT_NUMBER VALUE="1234567890"

# Update app name
make env-update KEY=AGENTSPACE_APP_NAME VALUE="mcp-security-agent-app_1234567890"
```

## Step 5: Verify Agentspace Setup

### 5.1 Test API Access

Verify you can access the Agentspace APIs:

```bash
# Test Discovery Engine API access
PROJECT_NUMBER=$(gcloud projects describe $(gcloud config get-value project) --format='value(projectNumber)')
LOCATION=global
curl -H "Authorization: Bearer $(gcloud auth print-access-token)" \
  -H "X-Goog-User-Project: $(gcloud config get-value project)" \
  "https://discoveryengine.googleapis.com/v1alpha/projects/$PROJECT_NUMBER/locations/$LOCATION/collections/default_collection/engines"
```

### 5.2 Validate Environment

Check your Agentspace configuration:

```bash
# Validate Agentspace environment variables
make env-validate-agentspace
```

## Understanding Agentspace Integration

### What Agentspace Actually Is

Agentspace is **not a separate platform** - it's a web UI service within Google Cloud's Discovery Engine that provides a chat interface for interacting with Agent Engine deployments.

### How It Works

1. **Agent Engine**: Your agent is deployed to Vertex AI Agent Engine (the actual compute/logic layer)
2. **Agentspace App**: A Discovery Engine configuration that provides a web UI
3. **Registration**: You register your Agent Engine deployment with your Agentspace App
4. **Access**: Users interact with your agent through the Agentspace web interface

### Simple Architecture

```
User → Agentspace Web UI → Agent Engine (your deployed agent)
```

**That's it!** Agentspace is essentially a UI wrapper around Agent Engine deployments.

## Common Agentspace URLs

After setup, you'll access your Agentspace app through these URLs:

- **Main Console**: `https://console.cloud.google.com/ai/discovery-engine/engines/YOUR_APP_NAME/overview`
- **Agent Management**: `https://console.cloud.google.com/ai/discovery-engine/engines/YOUR_APP_NAME/agents`
- **Integration URL**: Available after agent deployment (use `make agentspace-url`)

## Troubleshooting

### Common Issues

1. **"Permission denied" errors**
   - Verify IAM roles are properly assigned
   - Check that APIs are enabled
   - Ensure you're using the correct project

2. **"App not found" errors**
   - Verify app name is correct
   - Check that app was created in the expected region
   - Confirm project number matches your Google Cloud project

3. **API quota exceeded**
   - Check Discovery Engine API quotas in Cloud Console
   - Request quota increases if needed

### Debug Commands

```bash
# Check current project and permissions
gcloud config list
gcloud auth list

# Verify API enablement
gcloud services list --enabled | grep -E "(discoveryengine|aiplatform)"

# List Agentspace resources
gcloud alpha discovery-engine engines list --location=global

# Check environment configuration
make config-show
```

## Security Considerations

1. **Access Control**
   - Use least-privilege IAM policies
   - Regularly audit Agentspace access
   - Monitor API usage and costs

2. **Data Privacy**
   - Review data handling policies
   - Configure appropriate data retention
   - Understand data residency requirements

3. **API Security**
   - Use service accounts for production
   - Implement proper authentication
   - Monitor API access logs

## Next Steps

After completing Agentspace app setup:

1. **Deploy Agent Engine**: Follow the [Agent Engine Quickstart](agentspace_quickstart.md)
2. **Configure OAuth**: Set up OAuth authentication using the [OAuth Setup Guide](oauth_agentspace_setup.md)
3. **Register Agent**: Deploy your agent to Agentspace using `make agentspace-register`

## Environment Variables Summary

After completing this guide, your `.env` file should include:

```bash
# Google Cloud Configuration
GOOGLE_CLOUD_PROJECT=your-project-id
GOOGLE_CLOUD_LOCATION=us-central1

# Agentspace Configuration
AGENTSPACE_PROJECT_NUMBER=1234567890
AGENTSPACE_APP_NAME=mcp-security-agent-app_1234567890
AGENTSPACE_AGENT_ID=                # Populated after agent registration

# Agent Engine Configuration (from previous setup)
AGENT_ENGINE_RESOURCE_NAME=projects/PROJECT_NUMBER/locations/REGION/reasoningEngines/ENGINE_ID
```

These values are required for the OAuth setup and agent registration processes that follow.