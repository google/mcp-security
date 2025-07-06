# OAuth Setup for AgentSpace Integration

This guide walks you through the complete process of setting up OAuth authentication for your MCP Security Agent with Google's AgentSpace platform. This enables your agent to access Google services on behalf of users while maintaining secure authentication.

## Overview

AgentSpace OAuth integration allows your deployed agent to:
- Access Google services (Drive, Calendar, etc.) on behalf of users
- Maintain secure authentication without exposing credentials
- Provide seamless user experience with proper authorization flows

## Prerequisites

Before starting, ensure you have:
- A Google Cloud project with billing enabled
- Agent Engine deployment completed (see [Agent Engine Quickstart](agentspace_quickstart.md))
- **AgentSpace app created and configured** (see [AgentSpace App Setup](agentspace_app_setup.md))
- Proper IAM permissions for OAuth client creation

## Step 1: Create OAuth Client

### 1.1 Generate OAuth Client Guide

Run the guided setup to create your OAuth client:

```bash
make oauth-client
```

**Expected Output:**
```
Starting OAuth client creation guide...
DEBUG: Loading env file from: /Users/your-user/path/to/.env
============================================================
OAuth Client Creation Guide
============================================================

Steps to create an OAuth 2.0 client:

1. Open the Google Cloud Console:
   https://console.cloud.google.com/apis/credentials
   (Make sure you're in project: your-project-id)

2. Click '+ CREATE CREDENTIALS' → 'OAuth client ID'

3. If prompted to configure consent screen:
   - Choose 'Internal' for organization use
   - Fill in required fields
   - Add scopes if needed

4. For Application type, select 'Web application'

5. Configure the client:
   - Name: 'AgentSpace MCP Security Agent' (or similar)
   - Authorized redirect URIs:
     https://vertexaisearch.cloud.google.com/oauth-redirect

6. Click 'CREATE'

7. Download the client configuration:
   - Click the download button (⬇) next to your new client
   - Save as 'client_secret.json' in this directory

Would you like to open the Google Cloud Console now? (y/n):
```

**What This Command Does:**

1. **Environment Loading**: The script loads your `.env` file to read the current project configuration
2. **Project Detection**: It automatically detects your Google Cloud project ID from the environment variables
3. **Interactive Guide**: Provides a step-by-step guide with specific instructions for your project
4. **Console Link**: Offers to open the Google Cloud Console directly to the credentials page
5. **Specific Configuration**: Provides exact values you need to enter, including the critical redirect URI

**Key Points About the Output:**

- **Project-Specific URL**: The console URL includes your specific project ID, taking you directly to the right place
- **Redirect URI**: The most critical piece - `https://vertexaisearch.cloud.google.com/oauth-redirect` - this must be exact
- **Application Type**: Must be "Web application" for AgentSpace integration
- **File Location**: Tells you exactly where to save the downloaded `client_secret.json` file

**Following the Interactive Prompts:**

1. **Answer "y" to open the console**: If you respond with "y", the script will attempt to open your browser to the Google Cloud Console
2. **Answer "n" to continue manually**: If you respond with "n", you can manually navigate to the URL provided

**After Creating the OAuth Client:**

Once you complete the steps in the Google Cloud Console, you'll have:

1. **OAuth Client ID**: A string like `1234567890-abc123def456.apps.googleusercontent.com`
2. **OAuth Client Secret**: A string like `GOCSPX-AbC123DeF456GhI789JkL012`
3. **Downloaded JSON file**: Contains both the client ID and secret in JSON format

**What to Do with the client_secret.json:**

The downloaded file will look like this:
```json
{
  "web": {
    "client_id": "1234567890-abc123def456.apps.googleusercontent.com",
    "project_id": "your-project-id",
    "auth_uri": "https://accounts.google.com/o/oauth2/auth",
    "token_uri": "https://oauth2.googleapis.com/token",
    "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
    "client_secret": "[redacted]",
    "redirect_uris": ["https://vertexaisearch.cloud.google.com/oauth-redirect"]
  }
}
```

**Important:** Save this file in your project's root directory (same level as the Makefile) and **never commit it to version control**.

### 1.1.2 Extracting Credentials to .env File

After downloading the `client_secret.json` file, you need to extract the OAuth credentials and add them to your `.env` file.

**Method 1: Using Make Command (Recommended)**

You can automatically extract and add the OAuth credentials using:

```bash
make env-update KEY=OAUTH_CLIENT_ID VALUE="your-client-id-from-json"
make env-update KEY=OAUTH_CLIENT_SECRET VALUE="your-client-secret-from-json"
```

**Method 2: Manual Extraction**

1. **Open the client_secret.json file** and locate these values:
   ```json
   {
     "web": {
       "client_id": "1234567890-abc123def456.apps.googleusercontent.com",
       "client_secret": "[redacted]",
       "token_uri": "https://oauth2.googleapis.com/token"
     }
   }
   ```

2. **Add these variables to your `.env` file**:
   ```bash
   # OAuth Client Configuration
   OAUTH_CLIENT_ID=1234567890-abc123def456.apps.googleusercontent.com
   OAUTH_CLIENT_SECRET=[redacted]
   OAUTH_TOKEN_URI=https://oauth2.googleapis.com/token
   ```

**Where to Find Each Value:**

- **OAUTH_CLIENT_ID**: Located at `web.client_id` in the JSON file
- **OAUTH_CLIENT_SECRET**: Located at `web.client_secret` in the JSON file  
- **OAUTH_TOKEN_URI**: Located at `web.token_uri` in the JSON file (usually `https://oauth2.googleapis.com/token`)

**Example of Complete .env OAuth Section:**

After adding the OAuth credentials, your `.env` file should include:

```bash
# OAuth Client Configuration (added manually)
OAUTH_CLIENT_ID=1002894625780-a65bv4jgplu1pk1ljc2pkki6kjsocqjr.apps.googleusercontent.com
OAUTH_CLIENT_SECRET=[redacted]
OAUTH_TOKEN_URI=https://oauth2.googleapis.com/token

# OAuth Session Variables (auto-generated in next steps)
OAUTH_AUTH_ID=mcp-agent-20250704-104439    # Auto-generated unique identifier
OAUTH_AUTH_URI=https://accounts.google.com/o/oauth2/auth?client_id=...
```

**Important Note About OAUTH_AUTH_ID:**

The `OAUTH_AUTH_ID` is **not** from Google or the JSON file. It's a **unique identifier that we make up** to name our OAuth authorization in AgentSpace. The system automatically generates one with the format `mcp-agent-YYYYMMDD-HHMMSS` (e.g., `mcp-agent-20250704-104439`) when you run `make oauth-uri` for the first time.

- **You don't need to create this manually** - it's auto-generated
- **You can customize it** if you want a more descriptive name (e.g., `my-security-agent-oauth`)
- **It must be unique** within your AgentSpace project
- **It's used internally** by AgentSpace to track your OAuth authorization

**Verification:**

You can verify your OAuth configuration is loaded correctly:

```bash
# Check current OAuth configuration (secrets will be masked)
make config-show

# Validate OAuth environment variables
make env-validate-oauth
```

### 1.1.1 OAuth Consent Screen Configuration

If this is your first time creating an OAuth client in your project, you'll be prompted to configure the OAuth consent screen. Here's what to expect:

**Step 1: Choose User Type**
- **Internal**: For Google Workspace organizations - only users in your organization can use the app
- **External**: For any Google account - requires app verification for production use

**Step 2: App Information**
Fill in the required fields:
- **App name**: "AgentSpace MCP Security Agent" or similar
- **User support email**: Your email address
- **App logo**: Optional, but helps with branding
- **App domain**: Your organization's domain (if applicable)
- **Developer contact information**: Your email address

**Step 3: Scopes**
The most common scopes for AgentSpace integration:
- `https://www.googleapis.com/auth/cloud-platform` - Access to Google Cloud services
- `https://www.googleapis.com/auth/generative-language.retriever` - Vertex AI Search access

**Step 4: Test Users** (External apps only)
- Add email addresses of users who can test your app before verification
- You can add up to 100 test users during development

**Note**: For internal apps in Google Workspace organizations, users must be in the same organization. For external apps intended for broad use, you'll need to submit for verification once ready for production.

### 1.2 Manual OAuth Client Creation

If you prefer to create the client manually:

1. **Open Google Cloud Console**
   - Navigate to [Google Cloud Console - Credentials](https://console.cloud.google.com/apis/credentials)
   - Ensure you're in the correct project (check project ID in your `.env` file)

2. **Configure OAuth Consent Screen** (if not already done)
   - Click "Configure Consent Screen"
   - Choose "Internal" for organization use or "External" for broader access
   - Fill in required application information:
     - Application name: "AgentSpace MCP Security Agent"
     - User support email: Your email
     - Developer contact information: Your email
   - Add necessary scopes (e.g., `https://www.googleapis.com/auth/cloud-platform`)

3. **Create OAuth Client**
   - Click "+ CREATE CREDENTIALS" → "OAuth client ID"
   - Select "Web application" as the application type
   - Configure the client:
     - **Name**: "AgentSpace MCP Security Agent"
     - **Authorized redirect URIs**: `https://vertexaisearch.cloud.google.com/oauth-redirect`

4. **Download Client Secret**
   - Click "CREATE"
   - Download the client configuration as `client_secret.json`
   - Save this file securely (do not commit to version control)

## Step 2: Generate OAuth Authorization URI

### 2.1 Using Make Target

Generate the OAuth authorization URL:

```bash
make oauth-uri
```

This will:
- Read your OAuth client configuration from your `.env` file
- Generate a properly formatted authorization URL with the default scopes:
  - `https://www.googleapis.com/auth/cloud-platform`
  - `https://www.googleapis.com/auth/generative-language.retriever`
- Update your `.env` file with the authorization URI

**Customizing OAuth Scopes:**

If you need different scopes, you can set them in your `.env` file before running `make oauth-uri`:

```bash
# Custom scopes (comma-separated)
OAUTH_SCOPES=https://www.googleapis.com/auth/cloud-platform,https://www.googleapis.com/auth/drive.readonly,https://www.googleapis.com/auth/calendar.readonly
```

The system will use your custom scopes instead of the defaults.

### 2.2 Manual URI Generation

If you need to generate the URI manually, you can use Python:

```python
import google_auth_oauthlib.flow

# Load your client secret file
flow = google_auth_oauthlib.flow.Flow.from_client_secrets_file(
    'client_secret.json',
    scopes=[
        'https://www.googleapis.com/auth/cloud-platform',
        'https://www.googleapis.com/auth/generative-language.retriever'
    ]  # These are the same default scopes used by make oauth-uri
)

# Set the redirect URI
flow.redirect_uri = 'https://vertexaisearch.cloud.google.com/oauth-redirect'

# Generate the authorization URL
authorization_url, state = flow.authorization_url(
    access_type='offline',
    include_granted_scopes='true',
    prompt='consent'
)

print('Visit this URL to authorize:', authorization_url)
```

## Step 3: User Authorization

### 3.1 Visit Authorization URL

1. **Get the Authorization URL**
   - From Step 2, copy the generated `OAUTH_AUTH_URI` from your `.env` file
   - Or check the output from `make oauth-uri`

2. **Complete Authorization**
   - Visit the authorization URL in your browser
   - Sign in with your Google account
   - Review the requested permissions
   - Click "Allow" to grant access

3. **Note the Redirect**
   - After authorization, you'll be redirected to the AgentSpace OAuth redirect URL
   - The URL will contain an authorization code (this is handled automatically)

## Step 4: Link OAuth to AgentSpace

### 4.1 Environment Validation

First, ensure your environment has all required OAuth variables:

```bash
make env-validate-oauth
```

### 4.2 Link Authorization

Link your OAuth configuration to AgentSpace:

```bash
make oauth-link
```

This command will:
- Create an OAuth authorization record in AgentSpace
- Link your OAuth client to your AgentSpace project
- Configure the authorization for your agent

### 4.3 Manual Linking Process

The linking process performs the following API call:

```bash
curl -X POST \
  -H "Authorization: Bearer $(gcloud auth print-access-token)" \
  -H "Content-Type: application/json" \
  -H "X-Goog-User-Project: ${PROJECT_NUMBER}" \
https://discoveryengine.googleapis.com/v1alpha/projects/${PROJECT_NUMBER}/locations/global/authorizations?authorizationId=${AUTH_ID} \
  -d '{
  "name": "projects/'"${PROJECT_NUMBER}"'/locations/global/authorizations/'"${AUTH_ID}"'",
  "serverSideOauth2": {
      "clientId": "'"${OAUTH_CLIENT_ID}"'",
      "clientSecret": "'"${OAUTH_CLIENT_SECRET}"'",
      "authorizationUri": "'"${OAUTH_AUTH_URI}"'",
      "tokenUri": "'"${OAUTH_TOKEN_URI}"'"
    }
  }'
```

## Step 5: Register Agent with AgentSpace

### 5.1 Agent Registration

Register your agent with AgentSpace and link the OAuth authorization:

```bash
make agentspace-register
```

This will:
- Create an agent record in AgentSpace
- Link your deployed Agent Engine resource
- Associate the OAuth authorization with your agent

### 5.2 Update Existing Registration

If you need to update an existing agent registration:

```bash
make agentspace-update
```

## Step 6: Verify OAuth Setup

### 6.1 Verify Configuration

Check that your OAuth setup is working correctly:

```bash
make oauth-verify
```

### 6.2 Verify AgentSpace Integration

Verify the complete AgentSpace integration:

```bash
make agentspace-verify
```

### 6.3 Get AgentSpace URL

Get the URL to access your agent in AgentSpace:

```bash
make agentspace-url
```

## Environment Variables Reference

Your `.env` file should contain these OAuth-related variables:

```bash
# OAuth Client Configuration (from client_secret.json)
OAUTH_CLIENT_ID=your-client-id.apps.googleusercontent.com         # From JSON: web.client_id
OAUTH_CLIENT_SECRET=your-client-secret                            # From JSON: web.client_secret
OAUTH_TOKEN_URI=https://oauth2.googleapis.com/token               # From JSON: web.token_uri

# OAuth Session Variables (auto-generated by make commands)
OAUTH_AUTH_ID=mcp-agent-YYYYMMDD-HHMMSS                          # Auto-generated unique ID (can be customized)
OAUTH_AUTH_URI=https://accounts.google.com/o/oauth2/auth?...      # Generated authorization URL

# AgentSpace Configuration
AGENTSPACE_PROJECT_NUMBER=your-project-number
AGENTSPACE_APP_NAME=your-app-name
AGENTSPACE_AGENT_ID=your-agent-id

# Agent Engine Configuration
AGENT_ENGINE_RESOURCE_NAME=projects/PROJECT_NUMBER/locations/REGION/reasoningEngines/ENGINE_ID
```

**Variable Sources:**
- **OAUTH_CLIENT_ID/SECRET/TOKEN_URI**: Come from the `client_secret.json` file you download from Google Cloud Console
- **OAUTH_AUTH_ID**: A unique name we create to identify this OAuth authorization in AgentSpace (auto-generated or custom)
- **OAUTH_AUTH_URI**: Generated by combining your client ID with proper scopes and redirect URI
- **AGENTSPACE_***: Configuration specific to your AgentSpace app
- **AGENT_ENGINE_RESOURCE_NAME**: The resource name of your deployed Agent Engine

## Common OAuth Scopes

Depending on your agent's functionality, you may need these scopes:

- `https://www.googleapis.com/auth/cloud-platform` - Full Google Cloud access
- `https://www.googleapis.com/auth/generative-language.retriever` - Vertex AI Search access
- `https://www.googleapis.com/auth/drive.readonly` - Google Drive read access
- `https://www.googleapis.com/auth/calendar.readonly` - Google Calendar read access
- `https://www.googleapis.com/auth/gmail.readonly` - Gmail read access

## Troubleshooting

### Common Issues

1. **"redirect_uri_mismatch" Error**
   - Ensure the redirect URI in your OAuth client matches exactly: `https://vertexaisearch.cloud.google.com/oauth-redirect`
   - Check for trailing slashes or typos

2. **"invalid_client" Error**
   - Verify your `OAUTH_CLIENT_ID` and `OAUTH_CLIENT_SECRET` are correct
   - Ensure the OAuth client is properly configured in Google Cloud Console

3. **Authorization Not Found**
   - Check that `OAUTH_AUTH_ID` is unique and properly formatted
   - Verify your project number is correct

4. **Permission Denied**
   - Ensure your Google Cloud account has proper permissions
   - Check that Discovery Engine API is enabled
   - Verify the service account has necessary IAM roles

### Debug Commands

Check your OAuth configuration:

```bash
# Show current configuration (masks secrets)
make config-show

# Validate OAuth-specific environment
make env-validate-oauth

# List all AgentSpace agents
make agents-list

# Verify AgentSpace integration
make agentspace-verify
```

## Security Best Practices

1. **Client Secret Protection**
   - Never commit `client_secret.json` to version control
   - Store OAuth client secrets securely
   - Rotate client secrets regularly

2. **Scope Minimization**
   - Only request the minimum scopes needed
   - Review and audit scope usage regularly

3. **Environment Management**
   - Use separate OAuth clients for different environments
   - Implement proper secret management for production

4. **Monitoring**
   - Monitor OAuth usage and token refresh patterns
   - Set up alerts for authentication failures

## Complete Setup Workflow

Here's the complete workflow summary:

```bash
# 0. Prerequisites (complete these first)
# - Create AgentSpace app (see AgentSpace App Setup guide)
# - Deploy Agent Engine (see Agent Engine Quickstart guide)

# 1. Create OAuth client (follow guided setup)
make oauth-client

# 2. Generate authorization URI
make oauth-uri

# 3. Visit the authorization URI in browser and authorize

# 4. Link OAuth to AgentSpace
make oauth-link

# 5. Register agent with AgentSpace
make agentspace-register

# 6. Verify setup
make oauth-verify
make agentspace-verify

# 7. Get AgentSpace URL
make agentspace-url
```

After completing these steps, your agent will be accessible through AgentSpace with proper OAuth authentication, allowing users to securely access Google services through your MCP Security Agent.