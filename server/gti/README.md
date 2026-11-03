# Google Threat Intelligence MCP Server

`gti-mcp` is a Model Context Protocol (MCP) server exposing 50 tools for Google Threat Intelligence and VirusTotal v3 APIs.
See [MCP documentation](https://modelcontextprotocol.io/introduction), the [GTI MCP Server reference](../../docs/servers/gti_mcp.md), and [GTI workflow guides](../../docs/gti_workflows/index.md).

## Features

### Collections and Threats (17 tools)

- **`get_collection_report(id)`**: Retrieves a collection object by ID (`report--<id>`, `threat-actor--<id>`, `malware-family--<id>`, `campaign--<id>`, `vulnerability--<id>`, or `collection--<id>`).
- **`get_entities_related_to_a_collection(id, relationship_name, limit=10, descriptors_only=True)`**: Retrieves entities related to collection `id` (`associations`, `attack_techniques`, `domains`, `files`, `ip_addresses`, `urls`, `threat_actors`, `malware_families`, `software_toolkits`, `campaigns`, `vulnerabilities`, `reports`, `suspected_threat_actors`, `hunting_rulesets`). Pass `descriptors_only=False` for `attack_techniques`.
- **`search_threats(query, collection_type=None, limit=5, order_by="relevance-")`**: Searches threat collections using GTI query syntax and optional `collection_type`.
- **`search_campaigns(query, limit=10, order_by="relevance-")`**: Searches `campaign` collections.
- **`search_threat_actors(query, limit=10, order_by="relevance-")`**: Searches `threat-actor` collections.
- **`search_malware_families(query, limit=10, order_by="relevance-")`**: Searches `malware-family` collections.
- **`search_software_toolkits(query, limit=10, order_by="relevance-")`**: Searches `software-toolkit` collections.
- **`search_threat_reports(query, limit=10, order_by="relevance-")`**: Searches `report` collections.
- **`search_vulnerabilities(query, limit=10, order_by="relevance-")`**: Searches `vulnerability` (CVE) collections.
- **`get_collection_timeline_events(id)`**: Retrieves analyst-curated timeline events for collection `id`.
- **`get_collection_mitre_tree(id)`**: Retrieves MITRE ATT&CK tactics and techniques mapped to collection `id`.
- **`create_collection(name, description, iocs, private=True)`**: Creates a custom IOC collection from domains, file hashes, IP addresses, or URLs.
- **`update_collection_attributes(id, attributes)`**: Updates `name`, `description`, `private`, `tags`, or `alt_names` on collection `id`.
- **`update_iocs_in_collection(id, relationship, iocs, operation)`**: Adds or removes indicators (`domains`, `files`, `ip_addresses`, or `urls`) on collection `id` (`operation` is `"add"` or `"remove"`).
- **`get_collection_feature_matches(collection_id, feature_type, feature_id, entity_type, search_space, entity_type_plural, descriptors_only=True)`**: Pivots from a shared indicator feature across `"collection"` or `"corpus"`.
- **`get_collections_commonalities(collection_id)`**: Summarizes shared attributes and relationships across indicators in `collection_id`.
- **`get_collection_rules(collection_id, top_n=4, rule_types=None)`**: Retrieves curated standard YARA hunting rules (file and payload pattern matching) and top crowdsourced YARA, Sigma, and IDS rules for `collection_id`.

### Files and Digital Threat Monitoring (6 tools)

- **`get_file_report(hash)`**: Retrieves a file report by MD5, SHA-1, or SHA-256 `hash`.
- **`get_entities_related_to_a_file(hash, relationship_name, descriptors_only, limit=10)`**: Retrieves entities related to file `hash` (`descriptors_only=True` required for `file`, `domain`, `url`, `ip_address`, and `collection` targets).
- **`get_file_behavior_report(file_behaviour_id)`**: Retrieves a sandbox behavior report identified by `{file_hash}_{sandbox_name}`.
- **`get_file_behavior_summary(hash)`**: Retrieves the aggregated sandbox behavior summary for `hash`.
- **`analyse_file(file_path)`**: Uploads a local file to VirusTotal (shared with the public community corpus) and blocks until scan completion. Prefer non-blocking `submit_file` plus `get_analysis` to avoid client timeouts.
- **`search_digital_threat_monitoring(query, size=10, since=None, until=None, page=None, truncate=None, sanitize=True)`**: Searches Digital Threat Monitoring documents across surface, deep, and dark web sources using Lucene syntax.

### Intelligence Search and Hunting Rulesets (3 tools)

- **`search_iocs(query, limit=10, order_by="last_submission_date-")`**: Searches files, URLs, domains, and IP addresses using GTI search modifiers.
- **`get_hunting_ruleset(ruleset_id)`**: Retrieves a GTI Livehunt standard YARA ruleset object.
- **`get_entities_related_to_a_hunting_ruleset(ruleset_id, relationship_name, limit=10)`**: Retrieves entities matching `ruleset_id` (`"hunting_notification_files"`).

### Network Locations: Domains and IP Addresses (4 tools)

- **`get_domain_report(domain)`**: Retrieves the GTI domain analysis report for `domain`.
- **`get_entities_related_to_a_domain(domain, relationship_name, descriptors_only, limit=10)`**: Retrieves entities related to `domain`.
- **`get_ip_address_report(ip_address)`**: Retrieves the GTI analysis report for an IPv4 or IPv6 `ip_address`.
- **`get_entities_related_to_an_ip_address(ip_address, relationship_name, descriptors_only, limit=10)`**: Retrieves entities related to `ip_address`.

### URLs (2 tools)

- **`get_url_report(url)`**: Retrieves the GTI URL analysis report for `url`.
- **`get_entities_related_to_an_url(url, relationship_name, descriptors_only, limit=10)`**: Retrieves entities related to `url`.

### Threat Profiles (4 tools)

- **`list_threat_profiles(limit=10)`**: Lists organization Threat Profiles in Google Threat Intelligence.
- **`get_threat_profile(profile_id)`**: Retrieves a Threat Profile object and its configured target industries, regions, and actor motivations.
- **`get_threat_profile_recommendations(profile_id, limit=10)`**: Lists recommended and followed threat collections associated with `profile_id`.
- **`get_threat_profile_associations_timeline(profile_id, limit=10)`**: Retrieves the associations timeline for `profile_id`.

### Scanning, Reanalysis, and Analysis Status (7 tools)

- **`submit_file(file_path)`**: Uploads a local file to VirusTotal (sending only the file basename) and returns the queued analysis descriptor (`id` and `type`) immediately without blocking. Standard VirusTotal submissions are shared with the security community.
- **`reanalyze_file(hash)`**: Requests a fresh reanalysis of a file known to VirusTotal by MD5, SHA-1, or SHA-256 `hash`.
- **`submit_url(url)`**: Submits `url` for scanning and returns the queued analysis descriptor immediately.
- **`reanalyze_url(url)`**: Requests a fresh reanalysis of an existing `url`.
- **`reanalyze_domain(domain)`**: Triggers a fresh reanalysis and reputation refresh for `domain`.
- **`reanalyze_ip(ip_address)`**: Triggers a fresh reanalysis and reputation refresh for an IPv4 or IPv6 `ip_address`.
- **`get_analysis(analysis_id, include_engine_results=False)`**: Retrieves analysis `status` (`queued`, `in-progress`, `completed`), summary `stats`, and `meta` (`file_info` or `url_info`). Per-engine scanner results are omitted unless `include_engine_results=True`.

### GTI Agentic Investigation Sessions (7 tools)

Requires a Google Threat Intelligence API key with GTI Agentic entitlement (GTI Enterprise, GTI Enterprise+, or active PoC).

- **`ask_gti_agent(message)`**: Starts a stateful investigation session with GTI specialist agents and returns `session_id`, synthesized markdown `response`, `citations`, and `widgets`.
- **`continue_chat(session_id, message)`**: Sends a follow-up message to `session_id` while preserving prior turn context.
- **`list_sessions(limit=5, order=None, filter=None, cursor=None)`**: Lists GTI Agentic investigation sessions for the authenticated user.
- **`get_session_history(session_id, include_intermediate_events=False)`**: Retrieves turn-by-turn conversation history for `session_id` (set `include_intermediate_events=True` to include internal thought and tool call trace events).
- **`delete_session(session_id)`**: Deletes a GTI Agentic session by ID.
- **`share_session(session_id)`**: Generates a `share_token` so another analyst can clone `session_id`.
- **`copy_shared_session(share_token)`**: Clones a shared GTI Agentic session into the caller's workspace from `share_token`.

## Configuration

### Local MCP Server Configuration

Add `gti` to your MCP client settings file. On macOS with the standalone `uv` installer, specify the full binary path (such as `/Users/yourusername/.local/bin/uv`) if `uv` is not on your GUI application `PATH`.

```json
{
  "mcpServers": {
    "gti": {
      "command": "uv",
      "args": [
        "--env-file=/path/to/your/.env",
        "--directory",
        "/path/to/the/repo/server/gti/gti_mcp",
        "run",
        "server.py"
      ],
      "env": {
        "VT_APIKEY": "${VT_APIKEY}"
      }
    }
  }
}
```

### Hosted GTI Agentic Remote MCP Endpoint

Clients that only need the seven GTI Agentic session tools can also connect directly over Streamable HTTP:

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

### Environment Variable Setup

**macOS and Linux:**

```bash
VT_APIKEY="your-vt-api-key"
export VT_APIKEY
```

**Windows PowerShell:**

```powershell
$Env:VT_APIKEY = "your-vt-api-key"
```

## License

Apache 2.0

## Development

- `gti_mcp/server.py`: FastMCP server entry point and `vt.Client` lifecycle factory
- `gti_mcp/utils.py`: VirusTotal v3 object fetching, relationship pagination, and response sanitization helpers
- `gti_mcp/tools/`: Tool modules (`collections.py`, `files.py`, `intelligence.py`, `netloc.py`, `threat_profiles.py`, `urls.py`, `analyses.py`, `agentic.py`)
