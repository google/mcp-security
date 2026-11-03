# Run multi-turn investigations with GTI Agentic

GTI Agentic delegates multi-step threat intelligence and malware analysis questions to Google Threat Intelligence specialist agents (`/api/v3/agentspace/sessions`). Instead of returning raw VirusTotal v3 JSON payloads across dozens of manual calls, the agent executes the underlying graph pivots server-side and returns a synthesized markdown assessment, citations, structured widgets, and a stateful `session_id`.

## Prerequisites

GTI Agentic requires a `VT_APIKEY` belonging to an organization with **GTI Enterprise**, **GTI Enterprise+**, or an active **GTI Agentic PoC** entitlement. Standard free or public VirusTotal API keys return an authorization error on `/api/v3/agentspace/*` endpoints.

## Choose between local `gti-mcp` and the hosted endpoint

You can call the seven GTI Agentic session tools in two ways. Both paths authenticate with the same `VT_APIKEY` value and talk to the same Google Threat Intelligence backend.

![Topology diagram: an MCP client connects either to the local gti-mcp server over stdio (50 tools) or to the hosted GTI Agentic MCP endpoint over Streamable HTTP with an x-apikey header (7 session tools). Both reach the VirusTotal API v3 with a GTI Enterprise, Enterprise+, or PoC Agentic entitlement.](../img/gti_workflows/hosted_vs_local.svg)

1. **Local `gti-mcp` server (recommended when combining raw tools and agentic sessions).** Running `server/gti` gives your MCP client all 50 GTI tools in one server, including `ask_gti_agent`, non-blocking `submit_file` and `reanalyze_*` tools, custom collection CRUD, and deterministic indicator lookups. See [Google Threat Intelligence (GTI) MCP Server](../servers/gti_mcp.md).
2. **Hosted GTI Agentic remote MCP server (zero local runtime, 7 session tools only).** If your client only needs the seven GTI Agentic session tools (`ask_gti_agent`, `continue_chat`, `list_sessions`, `get_session_history`, `delete_session`, `share_session`, `copy_shared_session`), point a Streamable HTTP MCP client directly at `https://www.virustotal.com/api/v3/agentspace/mcp/` with an `x-apikey` header:

   ```json
   {
     "mcpServers": {
       "gti-agentic-hosted": {
         "url": "https://www.virustotal.com/api/v3/agentspace/mcp/",
         "headers": {
           "x-apikey": "${VT_APIKEY}"
         }
       }
     }
   }
   ```

   To verify your API key and entitlement against the hosted endpoint from a terminal, run:

   ```bash
   VT_APIKEY="your-gti-api-key"
   curl -sS -X POST "https://www.virustotal.com/api/v3/agentspace/mcp/" \
     -H "x-apikey: $VT_APIKEY" \
     -H "Content-Type: application/json" \
     -H "Accept: application/json, text/event-stream" \
     -d '{"jsonrpc":"2.0","id":1,"method":"tools/list","params":{}}'
   ```

## Start an investigation and pivot across turns

Use `ask_gti_agent` when a question spans multiple entity types, campaigns, or behavioral reports, then pass the returned `session_id` to `continue_chat` for follow-up pivots. The diagram below shows the whole session lifecycle, including the handoff to a second analyst described later on this page.

![Swimlane diagram: Analyst A calls ask_gti_agent, repeats continue_chat, reviews get_session_history, then calls share_session to get a share_token. Analyst B calls copy_shared_session with that token and gets a new session_id to continue independently. Analyst A lists sessions and deletes finished ones.](../img/gti_workflows/agentic_session_lifecycle.svg)

1. Open a new investigation session with `ask_gti_agent`:

   ```text
   ask_gti_agent(
     message="Assess SHA-256 24d004a104d4d54034dbcffc2a4b19a11f39008a575aa614ea04703480b1022c. Summarize attributed threat actors, primary execution behaviors, and network indicators."
   )
   ```

   Expected response shape:

   ```json
   {
     "session_id": "4f8b9c12-7d3a-4e21-9b60-1a2b3c4d5e6f",
     "title": "WannaCry Ransomware Assessment",
     "creation_date": 1730593000,
     "last_modification_date": 1730593028,
     "agent_id": "gti_orchestrator",
     "response": "## Executive Summary\n...",
     "citations": [
       {"id": "threat-actor--...", "type": "collection"}
     ]
   }
   ```

2. Ask follow-up questions in the same session with `continue_chat` so the GTI specialist agents retain the entities, reports, and sandbox traces gathered in turn 1:

   ```text
   continue_chat(
     session_id="4f8b9c12-7d3a-4e21-9b60-1a2b3c4d5e6f",
     message="List the MITRE ATT&CK techniques observed in those sandbox runs and suggest process and network telemetry fields to hunt in our SIEM."
   )
   ```

3. Combine agentic findings with deterministic tools when you move into action:
   - Pass cited collection IDs to `get_collection_rules` when you want exact standard YARA rules (for file and payload pattern matching), Sigma rules, or IDS signatures attached to that collection.
   - Use Google SecOps tools in `secops-mcp` when authoring or testing **YARA-L 2.0** event detection rules against Chronicle Unified Data Model (UDM) telemetry.

## Review session history and tool traces

When you resume work later or want to verify which backend lookups produced an agent's conclusion, list and inspect your sessions.

1. List recent sessions for your API key:

   ```text
   list_sessions(limit=5)
   ```

   If the response includes a non-empty `cursor`, pass `cursor` to `list_sessions` to fetch the next page.

2. Fetch the conversation transcript. By default, `include_intermediate_events=False` returns only `USER_MESSAGE` and `AGENT_FINAL_RESPONSE` turns so long multi-turn sessions stay compact:

   ```text
   get_session_history(
     session_id="4f8b9c12-7d3a-4e21-9b60-1a2b3c4d5e6f"
   )
   ```

3. Set `include_intermediate_events=True` when you need to audit the internal `AGENT_THOUGHT`, `FUNCTION_CALL`, and `FUNCTION_RESPONSE` trace events recorded during the session:

   ```text
   get_session_history(
     session_id="4f8b9c12-7d3a-4e21-9b60-1a2b3c4d5e6f",
     include_intermediate_events=True
   )
   ```

## Share an investigation across analysts and clean up

During shift handoffs or incident escalations from Tier 2 to Tier 3 or Incident Response, share a snapshot of the session rather than pasting long markdown transcripts into tickets.

1. Generate a share token from the originating session:

   ```text
   share_session(session_id="4f8b9c12-7d3a-4e21-9b60-1a2b3c4d5e6f")
   ```

   Expected response:

   ```json
   {
     "session_id": "4f8b9c12-7d3a-4e21-9b60-1a2b3c4d5e6f",
     "share_token": "eyJhbGciOi..."
   }
   ```

2. Record the `share_token` in the SOAR case comment (`post_case_comment`). The receiving analyst imports an independent copy into their own GTI workspace:

   ```text
   copy_shared_session(share_token="eyJhbGciOi...")
   ```

   `copy_shared_session` creates a new `session_id` owned by the recipient. Follow-up calls to `continue_chat` on the cloned `session_id` do not modify the original analyst's session.

3. Delete temporary or completed test sessions when they are no longer needed:

   ```text
   delete_session(session_id="4f8b9c12-7d3a-4e21-9b60-1a2b3c4d5e6f")
   ```
