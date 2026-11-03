# Google Threat Intelligence (GTI) MCP Server

`gti-mcp` exposes 50 Model Context Protocol (MCP) tools for Google Threat Intelligence and VirusTotal v3 APIs, covering threat collections, indicator reports, sandbox behaviors, hunting rulesets, Digital Threat Monitoring (DTM), Threat Profiles, non-blocking scans and reanalysis, and stateful GTI Agentic sessions.

For task-oriented procedures, see [Google Threat Intelligence workflows](../gti_workflows/index.md).

## Configuration

To run `gti-mcp`, obtain a VirusTotal or Google Threat Intelligence API key:

1. Sign in to [virustotal.com](https://www.virustotal.com).
2. Open your profile menu and copy your API key.
3. Supply `VT_APIKEY` to your MCP client configuration.

### Local MCP Server Configuration

Add `gti` to your MCP client settings file:

```json
{
  "mcpServers": {
    "gti": {
      "command": "uv",
      "args": [
        "--directory",
        "/path/to/the/repo/server/gti/gti_mcp",
        "run",
        "server.py"
      ],
      "env": {
        "VT_APIKEY": "0123456789abcdef0123456789abcdef0123456789abcdef0123456789abcdef"
      }
    }
  }
}
```

#### `--env-file`

To keep credentials out of your MCP client settings JSON, pass `--env-file` to `uv`:

```json
{
  "mcpServers": {
    "gti": {
      "command": "uv",
      "args": [
        "--directory",
        "/path/to/the/repo/server/gti/gti_mcp",
        "run",
        "--env-file",
        "/path/to/the/repo/.env",
        "server.py"
      ],
      "env": {}
    }
  }
}
```

Example `.env` file:

```text
VT_APIKEY=0123456789abcdef0123456789abcdef0123456789abcdef0123456789abcdef
```

### Hosted GTI Agentic Remote MCP Endpoint

If your client only needs the seven stateful GTI Agentic session tools (`ask_gti_agent`, `continue_chat`, `list_sessions`, `get_session_history`, `delete_session`, `share_session`, `copy_shared_session`) and your API key has GTI Enterprise, GTI Enterprise+, or PoC Agentic entitlement, you can connect directly over Streamable HTTP without running Python locally:

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

Use the local `gti` server configuration above whenever you want all 50 GTI tools in one server.

### Environment Variable Setup

Set `VT_APIKEY` in your shell environment:

**macOS and Linux:**

```bash
VT_APIKEY="your-vt-api-key"
export VT_APIKEY
```

**Windows PowerShell:**

```powershell
$Env:VT_APIKEY = "your-vt-api-key"
```

For proxy variables (`HTTP_PROXY`, `HTTPS_PROXY`, `SSL_CERT_FILE`) and client setup details, see the [usage guide](../usage_guide.md).

## Tools

### Collections and Threats (17 tools)

Google Threat Intelligence models threat actors, malware families, campaigns, software toolkits, reports, vulnerabilities, and custom indicator sets as collections.

- **`get_collection_report(id)`**: Retrieves a collection object by ID (such as `report--<id>`, `threat-actor--<id>`, `malware-family--<id>`, `campaign--<id>`, `vulnerability--<id>`, or `collection--<id>`) with `associations` included.
- **`get_entities_related_to_a_collection(id, relationship_name, limit=10, descriptors_only=True)`**: Retrieves entities linked to collection `id`. Set `descriptors_only=False` when `relationship_name` is `"attack_techniques"`. Supported `relationship_name` values:
  - `associations`: Associated threat collections across types
  - `attack_techniques`: MITRE ATT&CK technique objects (`descriptors_only` must be `False`)
  - `domains`: Associated domains
  - `files`: Associated file hashes
  - `ip_addresses`: Associated IPv4 and IPv6 addresses
  - `urls`: Associated URLs
  - `threat_actors`: Related threat actor collections
  - `malware_families`: Related malware family collections
  - `software_toolkits`: Related toolkit collections
  - `campaigns`: Related campaign collections
  - `vulnerabilities`: Related vulnerability collections
  - `reports`: Related threat intelligence reports
  - `suspected_threat_actors`: Suspected threat actor collections
  - `hunting_rulesets`: GTI standard YARA hunting rulesets linked to the collection
- **`search_threats(query, collection_type=None, limit=5, order_by="relevance-")`**: Searches threat collections using GTI filter syntax. Optional `collection_type` accepts `"threat-actor"`, `"malware-family"`, `"campaign"`, `"report"`, `"software-toolkit"`, `"vulnerability"`, or `"collection"`. `order_by` supports `"relevance-"`, `"relevance+"`, `"creation_date-"`, and `"creation_date+"`.
- **`search_campaigns(query, limit=10, order_by="relevance-")`**: Searches collections with `collection_type:campaign`.
- **`search_threat_actors(query, limit=10, order_by="relevance-")`**: Searches collections with `collection_type:threat-actor`.
- **`search_malware_families(query, limit=10, order_by="relevance-")`**: Searches collections with `collection_type:malware-family`.
- **`search_software_toolkits(query, limit=10, order_by="relevance-")`**: Searches collections with `collection_type:software-toolkit`.
- **`search_threat_reports(query, limit=10, order_by="relevance-")`**: Searches collections with `collection_type:report`.
- **`search_vulnerabilities(query, limit=10, order_by="relevance-")`**: Searches CVE and vulnerability collections with `collection_type:vulnerability`.
- **`get_collection_timeline_events(id)`**: Retrieves analyst-curated timeline events for collection `id`.
- **`get_collection_mitre_tree(id)`**: Retrieves MITRE ATT&CK tactics and techniques mapped to collection `id`.
- **`create_collection(name, description, iocs, private=True)`**: Creates a custom IOC collection from a non-empty list of domains, file hashes, IP addresses, or URLs. Defaults to `private=True`.
- **`update_collection_attributes(id, attributes)`**: Updates mutable collection fields on `id` (`name`, `description`, `private`, `tags`, `alt_names`).
- **`update_iocs_in_collection(id, relationship, iocs, operation)`**: Adds or removes indicators on collection `id`. `relationship` must be `"domains"`, `"files"`, `"ip_addresses"`, or `"urls"`. `operation` must be `"add"` or `"remove"`.
- **`get_collection_feature_matches(collection_id, feature_type, feature_id, entity_type, search_space, entity_type_plural, descriptors_only=True)`**: Pivots from a shared feature (`feature_type` and `feature_id`, such as `imphash` or `favicon_dhash`) to matching indicators. `search_space` accepts `"collection"` (within `collection_id` only) or `"corpus"` (across the VirusTotal dataset).
- **`get_collections_commonalities(collection_id)`**: Computes shared attributes and relationships across indicators in `collection_id` and returns a formatted markdown summary.
- **`get_collection_rules(collection_id, top_n=4, rule_types=None)`**: Retrieves curated standard YARA hunting rules and the top `top_n` crowdsourced detection rules matching files in `collection_id`. Optional `rule_types` filters on `"crowdsourced_ids"`, `"crowdsourced_sigma"`, `"crowdsourced_yara"`, and `"curated_yara_rule"`. Note that YARA rules returned here are standard YARA rules for file and payload pattern matching, not Chronicle SIEM YARA-L 2.0 event rules.

### Files and Digital Threat Monitoring (6 tools)

- **`get_file_report(hash)`**: Retrieves the file report for an MD5, SHA-1, or SHA-256 `hash`, including key network and association relationships while omitting raw per-engine `last_analysis_results`.
- **`get_entities_related_to_a_file(hash, relationship_name, descriptors_only, limit=10)`**: Retrieves entities related to file `hash`. `descriptors_only` is required and must be `True` when the target object type is `file`, `domain`, `url`, `ip_address`, or `collection`. Common `relationship_name` values include `behaviours`, `contacted_domains`, `contacted_ips`, `contacted_urls`, `dropped_files`, `embedded_domains`, `embedded_ips`, `embedded_urls`, `execution_parents`, `itw_domains`, `itw_ips`, `itw_urls`, `malware_families`, `related_threat_actors`, `reports`, `similar_files`, and `vulnerabilities` (47 supported relationships in `FILE_RELATIONSHIPS`).
- **`get_file_behavior_report(file_behaviour_id)`**: Retrieves a single sandbox execution report identified by `{file_hash}_{sandbox_name}`.
- **`get_file_behavior_summary(hash)`**: Retrieves the aggregated sandbox behavior summary across all sandbox runs for `hash`.
- **`analyse_file(file_path)`**: Uploads a local file to VirusTotal (shared with the public VirusTotal community corpus) and blocks until analysis finishes. Prefer non-blocking `submit_file` plus `get_analysis` to avoid client tool-call timeouts.
- **`search_digital_threat_monitoring(query, size=10, since=None, until=None, page=None, truncate=None, sanitize=True)`**: Searches Digital Threat Monitoring (DTM) documents from surface, deep, and dark web sources using Lucene syntax (`__type`, `label_threat`, `AND`, `OR`, `NOT`). `size` accepts `0` to `25`. `since` and `until` take RFC3339 UTC timestamps ending in `Z`. Pass the returned `page` token with identical parameters to paginate.

### Intelligence Search and Hunting Rulesets (3 tools)

- **`search_iocs(query, limit=10, order_by="last_submission_date-")`**: Searches files, URLs, domains, and IP addresses via `/intelligence/search` using GTI modifiers (such as `entity:file`, `entity:url`, `entity:domain`, or `entity:ip`).
- **`get_hunting_ruleset(ruleset_id)`**: Retrieves a GTI Livehunt ruleset object, including standard YARA `rules` text, `rule_names`, `number_of_rules`, and `tags`.
- **`get_entities_related_to_a_hunting_ruleset(ruleset_id, relationship_name, limit=10)`**: Retrieves objects related to `ruleset_id`. Supported `relationship_name`: `"hunting_notification_files"`.

### Network Locations: Domains and IP Addresses (4 tools)

- **`get_domain_report(domain)`**: Retrieves the GTI domain analysis report and `associations` for `domain`.
- **`get_entities_related_to_a_domain(domain, relationship_name, descriptors_only, limit=10)`**: Retrieves entities related to `domain`. `descriptors_only` is required (`True` when the target type is `file`, `domain`, `url`, `ip_address`, or `collection`). Common `relationship_name` values include `associations`, `communicating_files`, `downloaded_files`, `historical_ssl_certificates`, `historical_whois`, `malware_families`, `referrer_files`, `related_threat_actors`, `resolutions`, `siblings`, `subdomains`, and `urls` (32 supported relationships in `DOMAIN_RELATIONSHIPS`).
- **`get_ip_address_report(ip_address)`**: Retrieves the GTI IPv4 or IPv6 analysis report and `associations` for `ip_address`.
- **`get_entities_related_to_an_ip_address(ip_address, relationship_name, descriptors_only, limit=10)`**: Retrieves entities related to `ip_address`. `descriptors_only` is required (`True` when the target type is `file`, `domain`, `url`, `ip_address`, or `collection`). Common `relationship_name` values include `associations`, `communicating_files`, `downloaded_files`, `historical_ssl_certificates`, `historical_whois`, `malware_families`, `referrer_files`, `related_threat_actors`, `resolutions`, and `urls` (23 supported relationships in `IP_RELATIONSHIPS`).

### URLs (2 tools)

- **`get_url_report(url)`**: Encodes `url` as unpadded base64 and retrieves its GTI URL analysis report and `associations`.
- **`get_entities_related_to_an_url(url, relationship_name, descriptors_only, limit=10)`**: Retrieves entities related to `url`. `descriptors_only` is required (`True` when the target type is `file`, `domain`, `url`, `ip_address`, or `collection`). Common `relationship_name` values include `associations`, `communicating_files`, `contacted_domains`, `contacted_ips`, `downloaded_files`, `embedded_js_files`, `last_serving_ip_address`, `network_location`, `redirecting_urls`, `redirects_to`, `referrer_files`, and `related_threat_actors` (32 supported relationships in `URL_RELATIONSHIPS`).

### Threat Profiles (4 tools)

- **`list_threat_profiles(limit=10)`**: Lists organization Threat Profiles configured in Google Threat Intelligence.
- **`get_threat_profile(profile_id)`**: Retrieves a Threat Profile object, including configured `interests` (target industries, target regions, source regions, malware roles, and actor motivations).
- **`get_threat_profile_recommendations(profile_id, limit=10)`**: Lists threat collection descriptors linked to `profile_id` via ML recommendations (`SOURCE_RECOMMENDATION`) or manual follows (`SOURCE_DIRECT_FOLLOW`).
- **`get_threat_profile_associations_timeline(profile_id, limit=10)`**: Retrieves the chronological associations timeline for `profile_id`.

### Scanning, Reanalysis, and Analysis Status (7 tools)

- **`submit_file(file_path)`**: Uploads a local file to VirusTotal using only `os.path.basename(file_path)` in the upload metadata and returns the queued analysis descriptor (`id` and `type`) immediately without blocking. Standard VirusTotal file uploads are shared with the security community; confirm authorization before uploading local files.
- **`reanalyze_file(hash)`**: Requests a fresh reanalysis of an existing file in VirusTotal by MD5, SHA-1, or SHA-256 `hash` and returns the queued analysis descriptor.
- **`submit_url(url)`**: Submits `url` for live scanning and returns the queued analysis descriptor (`id` and `type`).
- **`reanalyze_url(url)`**: Requests a fresh reanalysis of an existing `url` and returns the queued analysis descriptor.
- **`reanalyze_domain(domain)`**: Triggers a fresh reanalysis and reputation refresh for `domain`.
- **`reanalyze_ip(ip_address)`**: Triggers a fresh reanalysis and reputation refresh for an IPv4 or IPv6 `ip_address`.
- **`get_analysis(analysis_id, include_engine_results=False)`**: Retrieves `status` (`queued`, `in-progress`, or `completed`), summary `stats`, `date`, and `meta` (`file_info` or `url_info`) for `analysis_id`. Per-engine scanner entries (`attributes.results`) are omitted unless `include_engine_results=True`.

### GTI Agentic Investigation Sessions (7 tools)

These tools interact with `/api/v3/agentspace/sessions` and require a `VT_APIKEY` with GTI Enterprise, GTI Enterprise+, or active PoC Agentic entitlement.

- **`ask_gti_agent(message)`**: Starts a new multi-step investigation session with GTI specialist agents and returns `session_id`, `title`, synthesized markdown `response`, and optional `citations`, `widgets`, and `agent_id`.
- **`continue_chat(session_id, message)`**: Sends a follow-up prompt to `session_id` while preserving prior turn context.
- **`list_sessions(limit=5, order=None, filter=None, cursor=None)`**: Lists GTI Agentic sessions for the authenticated user with optional `cursor` pagination.
- **`get_session_history(session_id, include_intermediate_events=False)`**: Retrieves session conversation turns (`USER_MESSAGE` and `AGENT_FINAL_RESPONSE` by default; set `include_intermediate_events=True` to include `AGENT_THOUGHT`, `FUNCTION_CALL`, and `FUNCTION_RESPONSE` trace events).
- **`delete_session(session_id)`**: Deletes a GTI Agentic session and returns `{"deleted": True, "session_id": ...}`.
- **`share_session(session_id)`**: Generates a `share_token` so another user can clone `session_id`.
- **`copy_shared_session(share_token)`**: Clones a shared session from `share_token` into the caller's workspace and returns the new `session_id` and latest turn summary.

## Query Syntax Reference

Tools that accept a GTI `query` string (`search_threats` and `search_iocs`) use entity and collection search modifiers:

1. **Keyword search (`search_threats`):**

   ```text
   ransomware
   ```

2. **Collection type filter (`search_threats`):**

   ```text
   collection_type:"malware-family" name:emotet
   ```

3. **Targeted campaign filter (`search_threats`):**

   ```text
   collection_type:"campaign" targeted_industries:"financial"
   ```

4. **File IOC search (`search_iocs`):**

   ```text
   entity:file p:20+ tag:peexe size:500kb-
   ```

5. **IP IOC search (`search_iocs`):**

   ```text
   entity:ip country:RU p:5+
   ```

Modifier reference documentation:

- File search modifiers: https://gtidocs.virustotal.com/docs/file-search-modifiers
- URL search modifiers: https://gtidocs.virustotal.com/docs/url-search-modifiers
- Domain search modifiers: https://gtidocs.virustotal.com/docs/domain-search-modifiers
- IP address search modifiers: https://gtidocs.virustotal.com/docs/ip-address-search-modifiers

## Workflow Guides

For end-to-end step sequences, expected outputs, and operational guardrails, see the dedicated workflow pages:

- [Google Threat Intelligence workflows overview](../gti_workflows/index.md)
- [Scan and reanalyze files, URLs, domains, and IP addresses](../gti_workflows/scanning_and_reanalysis.md)
- [Run multi-turn investigations with GTI Agentic](../gti_workflows/agentic_investigations.md)
- [Curate threat collections, hunting rules, and Digital Threat Monitoring](../gti_workflows/collections_and_hunting.md)

```{toctree}
:hidden:
:maxdepth: 2

../gti_workflows/index
```
