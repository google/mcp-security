# Prebuilt ADK Agent Usage Guide

This guide provides instructions on how to run the prebuilt ADK (Agent Development Kit) agent both locally and in Cloud Run (if necessary for demos).

> 🪧 **NOTE:**  
> With ADK 1.0.0 introducing some breaking changes, Please only use gemini-2.5 models (gemini-2.5-flash-preview-04-17 or gemini-2.5-pro-preview-05-06) when using this agent, till we sort these issues out. Also till that time we recommend setting `GOOGLE_GENAI_USE_VERTEXAI` to `False`, locally and when deploying.

## 1. Running Agent locally (Setup time - about 5 minutes)

### Prerequisites
You need the following to run the agent

1. `python` - v3.11+
2. `pip`
3. `gcloud` cli (If you ran on Google Cloud Console then gcloud is already installed)

### Setting up and running the agent
Please execute the following instructions

```bash
   # Clone the repo
   git clone https://github.com/google/mcp-security.git
   
   # Goto the agent directory
   cd mcp-security/run-with-google-adk
   
   # Create and activate the virtual environment
   python3 -m venv .venv
   . .venv/bin/activate

   # Install dependencies (google-adk and uv)
   pip install -r requirements.txt
   
   # Add exec permission to run-adk-agent.sh - which runs our agent
   chmod +x run-adk-agent.sh

   # Run the agent
   ./run-adk-agent.sh
```

For the very first run it creates a default .env file in `./google-mcp-security-agent/.env`

```bash
# sample output
$./run-adk-agent.sh 
Copying ./google-mcp-security-agent/sample.env to ./google-mcp-security-agent/.env...
Please update the environment variables in ./google-mcp-security-agent/.env
```

Use your favorite editor and update `./google-mcp-security-agent/.env`. 

The default `.env` file is shown below. 

1. Update the variables as needed in your favorite editor. You can choose to load some or all of the MCP servers available using the load environment variable at the start of each section. Don't use quotes for values except for `DEFAULT_PROMPT`. 
2. Make sure that variables in the `MANDATORY` section have proper values (make sure you get and update the `GOOGLE_API_KEY` using these [instructions](https://ai.google.dev/gemini-api/docs/api-key)) 
3. You can experiment with the prompt `DEFAULT_PROMPT`. Use single quotes for the prompt. If you plan to later deploy to a Cloud Run Service - avoid commas (or if you use them they will be converted to semicommas during deployment).
4. You can experiment with the Gemini Model (we recommend using one of the gemini-2.5 models). Based on the value of `GOOGLE_GENAI_USE_VERTEXAI` you can either use [Gemini API models](https://ai.google.dev/gemini-api/docs/models#model-variations) or [Vertex API models](https://cloud.google.com/vertex-ai/generative-ai/docs/models).


```bash
# Please do not use quotes / double quotes for values except for DEFAULT_PROMPT (use single quotes there)

# SecOps MCP
LOAD_SECOPS_MCP=Y
CHRONICLE_PROJECT_ID=NOT_SET
CHRONICLE_CUSTOMER_ID=NOT_SET
CHRONICLE_REGION=NOT_SET

# GTI MCP
LOAD_GTI_MCP=Y
VT_APIKEY=NOT_SET

# SECOPS_SOAR MCP
LOAD_SECOPS_SOAR_MCP=Y
SOAR_URL=NOT_SET
SOAR_APP_KEY=NOT_SET

# SCC MCP
LOAD_SCC_MCP=Y

# MANDATORY
GOOGLE_GENAI_USE_VERTEXAI=False
GOOGLE_API_KEY=NOT_SET
# If you plan to use Gemini API - Models list - https://ai.google.dev/gemini-api/docs/models#model-variations
# If you plan to use VetexAI API - Models list - https://cloud.google.com/vertex-ai/generative-ai/docs/models
GOOGLE_MODEL=gemini-2.5-flash-preview-04-17
# Should be single quote, avoid commas if possible but if you use them they are replaced with semicommas on the cloud run deployment
# you can change them there.
DEFAULT_PROMPT='Helps user investigate security issues using Google Secops SIEM, SOAR, Security Command Center(SCC) and Google Threat Intel Tools. All authentication actions are automatically approved. If the query is about a SOAR case try to provide a backlink to the user. A backlink is formed by adding /cases/<case id> to this URL when present in field ui_base_link of your input. If the user asks with only ? or are you there? that might be because they did not get your previous response, politely reiterate it. Try to respond in markdown whenever possible.'


# Following properties must be set when 
# 1. GOOGLE_GENAI_USE_VERTEXAI=True or 
# 2. When deploying to Cloud Run
GOOGLE_CLOUD_PROJECT=YOUR-CLOUD-RUN-PROJECT-ID
GOOGLE_CLOUD_LOCATION=us-central1

# HIGHLY RECOMMENDED TO SET Y AFTER INITIAL TESTING ON CLOUD RUN
MINIMAL_LOGGING=N




```

Once the variables are updated, run the agent again (make sure you are back in the `mcp-security/run-with-google-adk` directory).

```bash
   # Authenticate to use SecOps APIs
   # Skip if running in Google Cloud Shell
   gcloud auth application-default login
```

```bash
   # Run the agent again
   ./run-adk-agent.sh
```

You should get an output like following

```bash
# Sample output
$./run-adk-agent.sh 
Contents of .env (with masked values):
# Please do not use quotes / double quotes for values except for DEFAULT_PROMPT (use single quotes there)
# SecOps MCP
LOAD_SECOPS_MCP=Y
.
(output cropped)
.

Running adk web command...
INFO:     Started server process [1203693]
INFO:     Waiting for application startup.

+-----------------------------------------------------------------------------+
| ADK Web Server started                                                      |
|                                                                             |
| For local testing, access at http://localhost:8000.                         |
+-----------------------------------------------------------------------------+

INFO:     Application startup complete.
INFO:     Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)

```

Access the Agent 🤖 interface by going to `http://localhost:8000`

> 🪧 **NOTE:**  
> First response usually takes a bit longer as the agent is loading the tools from the MCP server(s).

> ⚠️ **CAUTION:**  
> In case the response seems stuck and/or there is an error on the console, create a new session in the ADK Web UI by clicking `+ New Session` in the top right corner. You can also ask a follow up question in the same session like `Are you still there?` or `Can you retry that?`. You can also try switching `Token Streaming` on.

> 🪧 **NOTE:**  
> When exiting, shut down the browser tab first and then use `ctrl+c` to exit on the console. 


<!-- #### Running agent without the web interface

You can also run the agent without the web interface (This version is more efficient than the web interface). A basic console based agent is provided. You can use the following command to run it. 

1. Make sure you have set up the environment variables in `./google-mcp-security-agent/.env` as explained above
2. To exit the agent, say `bye` (check sample output below)

```bash
# make sure you have updated the ./google-mcp-security-agent/.env file
python console-mcp-agent.py
```
Sample output 

```
$ python console-mcp-agent.py 
2025-04-30 12:15:48,681 - INFO - __main__ - main - Starting SecOps SOAR MCP server
2025-04-30 12:15:49,027 - INFO - __main__ - get_enabled_integrations_set - Found --integrations flag. Enabling only: {'csv', 'okta'}
2025-04-30 12:15:49,027 - INFO - __main__ - register_tools - Starting dynamic tool registration...
2025-04-30 12:15:49,031 - INFO - __main__ - register_tools -     Found register_tools in okta. Registering...
2025-04-30 12:15:49,090 - INFO - __main__ - register_tools -     Found register_tools in csv. Registering...
2025-04-30 12:15:49,109 - INFO - __main__ - register_tools - Finished scanning marketplace directory.
2025-04-30 12:15:49,128 - INFO - mcp.server.lowlevel.server - _handle_request - Processing request of type ListToolsRequest
[04/30/25 12:15:51] INFO     Successfully initialized Google Cloud Security Center Client.                                                                                       scc_mcp.py:45
2025-04-30 12:15:51,910 - scc-mcp - INFO - Successfully initialized Google Cloud Security Center Client.
[04/30/25 12:15:53] INFO     Successfully initialized Google Cloud Asset Inventory Client.                                                                                       scc_mcp.py:54
2025-04-30 12:15:53,457 - scc-mcp - INFO - Successfully initialized Google Cloud Asset Inventory Client.
                    INFO     Starting SCC MCP server...                                                                                                                         scc_mcp.py:324
2025-04-30 12:15:53,466 - scc-mcp - INFO - Starting SCC MCP server...
                    INFO     Processing request of type ListToolsRequest                                                                                                         server.py:534
2025-04-30 12:15:53,489 - mcp.server.lowlevel.server - INFO - Processing request of type ListToolsRequest
>Hello what can you do ?
[ET 1746015358.597346 PT 1746015366.3145175 R model T CTC]
Hello there! I am a security assistant that can help you investigate security issues using various tools.

Here are some of the things I can help you with:

*   **Search Security Events:** I can search for security events and logs in Chronicle SIEM based on natural language queries.
*   **Get Security Alerts:** I can retrieve recent security alerts directly from Chronicle SIEM.
*   **Look up Entities:** I can look up information about entities like IP addresses, domains, file hashes, or users in Chronicle SIEM for historical context and activity summaries.
*   **Get IOC Matches:** I can find if any known Indicators of Compromise (IoCs) from threat intelligence feeds have been observed in your Chronicle SIEM logs.
*   **Get Threat Intelligence:** I can provide summaries and answer questions about threat actors, malware, vulnerabilities (CVEs), tactics, techniques, and procedures (TTPs) using Google's threat intelligence.
*   **Investigate Cases:** I can list security cases from your SOAR platform, get their full details, list associated alerts and underlying events, and retrieve entities involved in specific alert groups.
*   **Manage Cases:** I can add comments to a SOAR case or change its priority.
*   **Get Entity Details:** I can fetch detailed information about entities known to your SOAR platform.
*   **Search for Threats:** I can search for specific threat actors, malware families, campaigns, reports, or vulnerabilities in Google Threat Intelligence. I can also retrieve details and related entities for these threats, including timelines and MITRE techniques where available.
*   **Analyze Files, Domains, IP Addresses, and URLs:** I can get comprehensive analysis reports and related entities for these indicators using Google Threat Intelligence and VirusTotal. I can also analyze a file you provide.
*   **Search for IOCs:** I can search for specific Indicators of Compromise (files, URLs, domains, IPs) in Google Threat Intelligence.
*   **Find Cloud Vulnerabilities:** I can list top vulnerability findings and get remediation steps for specific findings in your Google Cloud projects using Security Command Center.
*   **Perform Okta Actions:** Through the SOAR platform, I can perform actions related to Okta users (get, enable, disable, reset password, set password, list groups, list roles) and groups (get, add).
*   **Search/Save CSV Data:** Through the SOAR platform, I can search for entities or strings in CSV files and save JSON data to a CSV file.

How can I help you with your security investigation today?
>bye
[ET 1746015369.553427 PT 1746015371.908041 R model T CTC]
Goodbye! Let me know if you need help with any security investigations in the future.
Closing MCP server connection...
Cleanup complete.

``` -->



## 2. Running Agent as a Cloud Run Service

The agent with MCP servers can be deployed as a Cloud Run Service, right from within the source code directory.

Before you do this, please consider following

1. Do you really need it? Deployment is recommended in scenarios where you need to share agent with your team members who may not have access to all of the backend services (SCC, SecOps - SIEM, SecOps - SOAR, Google Threat Intelligence)
2. Make sure that after initial testing  
    1. Require authentication for your agent (steps provided [below](#restrict-service-to-known-developers--testers))
    2. Implement restrictive logging (steps provided [below](#adjust-logging-verbosity))

### Prerequisites

1. Must have locally run the ADK based agent successfully at least once. Environment variables `GOOGLE_CLOUD_PROJECT` and `GOOGLE_CLOUD_LOCATION` should have valid values.
2. Must have required APIs enabled and proper IAM access ([details](https://cloud.google.com/run/docs/deploying-source-code#before_you_begin))

### Costs
In addition to Gemini/ Vertex API costs, running agent will incur cloud costs. Please check [Cloud Run Pricing](https://cloud.google.com/run/pricing).

> ⚠️ **WARNING:**  
> It is not recommended to run the a Cloud Run service with unauthenticated invocations enabled (we do that initially for verification). Please follow steps to enable [IAM authentication](https://cloud.google.com/run/docs/authenticating/developers) on your service. You could also deploy it behind the [Identity Aware Proxy (IAP)](https://cloud.google.com/iap/docs/enabling-cloud-run) - but that is out of scope for this documentation.

### Deployment Steps
<!-- > 🪧 **NOTE:**  
> It is recommended to switch to Vertex AI (with `GOOGLE_GENAI_USE_VERTEXAI=True`) when deploying -->

```bash
# Please run these commands from the mcp-security directory
chmod +x ./run-with-google-adk/cloudrun_deploy_run.sh

bash ./run-with-google-adk/cloudrun_deploy_run.sh deploy
```
Sample output is provided below

```bash
# Sample output
$ bash ./run-with-google-adk/cloudrun_deploy_run.sh deploy
Starting deployment process...
Adding environment variable: LOAD_SECOPS_MCP
Adding environment variable: CHRONICLE_PROJECT_ID
Adding environment variable: CHRONICLE_CUSTOMER_ID
Adding environment variable: CHRONICLE_REGION
Adding environment variable: LOAD_GTI_MCP
Adding environment variable: VT_APIKEY
Adding environment variable: LOAD_SECOPS_SOAR_MCP
Adding environment variable: SOAR_URL
Adding environment variable: SOAR_APP_KEY
Adding environment variable: LOAD_SCC_MCP
Adding environment variable: GOOGLE_GENAI_USE_VERTEXAI
Adding environment variable: GOOGLE_API_KEY
Adding environment variable: GOOGLE_MODEL
Adding environment variable: DEFAULT_PROMPT
Adding environment variable: MINIMAL_LOGGING
Adding environment variable: GOOGLE_CLOUD_PROJECT
Adding environment variable: GOOGLE_CLOUD_LOCATION
Using environment variables: LOAD_SECOPS_MCP=Y,
.
.
[REDACTED]
.
.
Temporarily copying files in the top level directory for image creation.
Building using Dockerfile and deploying container to Cloud Run service [mcp-security-agent-service] in project [REDACTED] region [us-central1]
⠛ Building and deploying... Uploading sources.                                                                                                                                               
⠏ Building and deploying... Uploading sources.                                                                                                                                               
  ⠏ Uploading sources...                                                                                                                                                                     
  . Creating Revision...                                                                                                                                                                     
  . Routing traffic...                                                                                                                                                                       
  . Setting IAM Policy...                                                                                                                                                                    
Creating temporary archive of 581 file(s) totalling 11.2 MiB before compression.
Some files were not included in the source upload.
✓ Building and deploying... Done.                                                                                                                                                            
  ✓ Uploading sources...                                                                                                                                                                     
  ✓ Building Container... Logs are available at [REDACTED].          
  ✓ Creating Revision...                                                                                                                                                                     
  ✓ Routing traffic...                                                                                                                                                                       
  ✓ Setting IAM Policy...                                                                                                                                                                    
Done.                                                                                                                                                                                        
Service [mcp-security-agent-service] revision [mcp-security-agent-[REDACTED]] has been deployed and is serving 100 percent of traffic.
Service URL: [REDACTED]
Deleting temporarily copied files in the top level directory for image creation.
Successfully deployed the service.

```
Now, you can verify the service by browsing to the service endpoint.

### IAM access to use Chronicle and SCC

Please remember that Cloud Run uses default service account of compute engine service. Go to IAM and provide the service account access to "Chronicle API Viewer" (in the project associated with your SecOps instance) and appropriate role for SCC (roles starting with Security Center in IAM)


### Restrict Service To Known Developers / Testers

Summarizing the steps from [IAM authentication](https://cloud.google.com/run/docs/authenticating/developers)

1. Goto Cloud Run - Services - click `mcp-security-agent-service`
2. Click `Security`
3. In `Authentication`, `Use Cloud IAM to authenticate incoming requests` should be already selected.
4. Select the radio button `Require authentication`
5. Click `Save`
6. Cloud Run - Services - select `mcp-security-agent-service`
7. At the top click `permissions`, a pane `Permissions for mcp-security-agent-service` should open on the right hand side.
8. Click `Add principal`
9. Add the users you want to provide access to and provide them `Cloud Run Invoker` role.
10. Wait for some time.

### Accessing the restricted service

1. Ask your users to run the following command (replace project id and region with the project id & region in which you have deployed the service)

```bash
gcloud run services proxy mcp-security-agent-service --project PROJECT-ID --region YOUR-REGION

```
2. Now they can access the Cloud Run Service locally on `http://localhost:8080`


### Vertically scaling your container(s)
In case the Cloud Run logs show errors like below, you can consider increasing the resources for the individual containers

`Memory limit of 512 MiB exceeded with 543 MiB used. Consider increasing the memory limit, see https://cloud.google.com/run/docs/configuring/memory-limits`

##### Steps

1. Goto Cloud Run - Services - click `mcp-security-agent-service`
2. Click `Edit & deploy new revision`
3. In `Container(s)` - `Edit Container(s)` - `Settings`
4. Add resources by updating either Memory/ CPU or both.

### Adjust Logging Verbosity
Since the entire context and response from the LLM is printed as logs. You might end up logging some sensitive information. Setting the environment variable `MINIMAL_LOGGING` to `Y` should fix this issue. This should also reduce cloud logging costs. Please do this once you have verified the service initially. Changes to be made directly on Cloud Run service and it will result in restarting the service. Verify service logs after the change is made.