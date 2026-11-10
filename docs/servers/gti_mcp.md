# Google Threat Intelligence MCP server

The `gti-mcp` server connects MCP clients to the Google Threat Intelligence (GTI) and VirusTotal v3 APIs (`vt-py`) for threat actor and malware research, indicator enrichment, sandbox behavior analysis, Digital Threat Monitoring (DTM), Threat Profiles, and standard YARA hunting rulesets.

## Configuration

### API key setup

Obtain an API key from your profile in Google Threat Intelligence or [VirusTotal](https://www.virustotal.com) and expose it as `VT_APIKEY`.

On macOS and Linux:

```bash
export VT_APIKEY="your-vt-api-key"
```

On Windows PowerShell:

```powershell
$Env:VT_APIKEY = "your-vt-api-key"
```

See [Setting up environment variables](../usage_guide.md#setting-up-environment-variables) for persistent shell and `.env` setup.

### MCP client configuration

Run the published package from PyPI with `uvx`:

```json
{
  "mcpServers": {
    "gti": {
      "command": "uvx",
      "args": [
        "--from",
        "gti-mcp",
        "gti_mcp"
      ],
      "env": {
        "VT_APIKEY": "your-vt-api-key"
      }
    }
  }
}
```

Or run from a local Git clone and load `VT_APIKEY` from an `.env` file via `uv --env-file`:

```json
{
  "mcpServers": {
    "gti": {
      "command": "uv",
      "args": [
        "--directory",
        "/path/to/mcp-security/server/gti/gti_mcp",
        "run",
        "--env-file",
        "/path/to/mcp-security/.env",
        "server.py"
      ],
      "env": {}
    }
  }
}
```

For corporate proxy and custom TLS CA configuration (`HTTP_PROXY`, `HTTPS_PROXY`, and `SSL_CERT_FILE`), see [Corporate proxies and custom TLS certificates](../usage_guide.md#corporate-proxies-and-custom-tls-certificates).

## Tools

`gti-mcp` registers 36 tools across 6 capability groups.

### Collections and threats (17 tools)

GTI models threat actors, malware families, campaigns, software toolkits, threat reports, vulnerabilities, and curated IOC sets as **collections**.

- **`get_collection_report(id)`**: Retrieves a collection object by GTI ID (such as `report--<id>` or `threat-actor--<id>`), including `collection_type` and threat attributes.
- **`get_entities_related_to_a_collection(id, relationship_name, limit=10, descriptors_only=True)`**: Lists related entities (`associations`, `attack_techniques`, `domains`, `files`, `ip_addresses`, `urls`, `campaigns`, `malware_families`, `threat_actors`, `software_toolkits`, `reports`, or `vulnerabilities`) for a collection ID. Set `descriptors_only=False` to fetch full entity attributes instead of lightweight descriptors.
- **`search_threats(query, collection_type=None, limit=5, order_by="relevance-")`**: Searches threat collections using GTI query syntax. Optional `collection_type` restricts results to `"campaign"`, `"malware-family"`, `"software-toolkit"`, `"threat-actor"`, `"report"`, or `"vulnerability"`.
- **`search_campaigns(query, limit=10, order_by="relevance-")`**: Searches collections of type `campaign`. Supports `order_by` values `"relevance-"`, `"relevance+"`, `"creation_date-"`, and `"creation_date+"`.
- **`search_threat_actors(query, limit=10, order_by="relevance-")`**: Searches collections of type `threat-actor`.
- **`search_malware_families(query, limit=10, order_by="relevance-")`**: Searches collections of type `malware-family`.
- **`search_software_toolkits(query, limit=10, order_by="relevance-")`**: Searches collections of type `software-toolkit`.
- **`search_threat_reports(query, limit=10, order_by="relevance-")`**: Searches collections of type `report`.
- **`search_vulnerabilities(query, limit=10, order_by="relevance-")`**: Searches vulnerability (CVE) collections of type `vulnerability`.
- **`get_collection_timeline_events(id)`**: Retrieves curated analyst timeline events for a campaign, threat actor, or other collection.
- **`get_collection_mitre_tree(id)`**: Retrieves MITRE ATT&CK tactics and techniques mapped to a collection.
- **`create_collection(name, description, iocs, private=True)`**: Creates a custom IOC collection from a non-empty list of domains, file hashes, IP addresses, or URLs. Defaults to `private=True`.
- **`update_collection_attributes(id, attributes)`**: Updates mutable collection fields (`name`, `description`, `private`, `tags`, or `alt_names`).
- **`update_iocs_in_collection(id, relationship, iocs, operation)`**: Adds or removes indicators on a custom collection. `relationship` accepts `"domains"`, `"files"`, `"ip_addresses"`, or `"urls"`; `operation` accepts `"add"` or `"remove"`.
- **`get_collection_feature_matches(collection_id, feature_type, feature_id, entity_type, search_space, entity_type_plural, descriptors_only=True)`**: Pivots from a shared commonality feature (such as a mutex, TLS certificate, embedded domain, or standard YARA rule match) to the matching IOCs inside `collection_id`.
- **`get_collections_commonalities(collection_id)`**: Summarizes shared attributes and structural relationships across the IOCs in `collection_id`.
- **`get_collection_rules(collection_id, top_n=4, rule_types=None)`**: Retrieves curated hunting rules and the top `top_n` community rules associated with `collection_id`. Optional `rule_types` filters by `"crowdsourced_ids"`, `"crowdsourced_sigma"`, `"crowdsourced_yara"`, and `"curated_yara_rule"` (note: these `yara` entries are standard YARA file and payload rules, distinct from Google SecOps YARA-L 2.0 UDM event detection rules).

### Files and Digital Threat Monitoring (6 tools)

- **`get_file_report(hash)`**: Retrieves detection verdicts, threat classifications, and file metadata for an MD5, SHA-1, or SHA-256 hash.
- **`get_entities_related_to_a_file(hash, relationship_name, descriptors_only, limit=10)`**: Lists entities linked to a file hash, including `behaviours`, `contacted_domains`, `contacted_ips`, `contacted_urls`, `dropped_files`, `embedded_domains`, `embedded_ips`, `embedded_urls`, `execution_parents`, and `associations`.
- **`get_file_behavior_report(file_behaviour_id)`**: Retrieves a single sandbox detonation report identified by `<file_hash>_<sandbox_name>`.
- **`get_file_behavior_summary(hash)`**: Aggregates behavioral observations (processes, registry keys, mutexes, DNS queries, and MITRE ATT&CK techniques) across all sandboxes for a file hash.
- **`analyse_file(file_path)`**: Uploads a local file (specified as an absolute path) to VirusTotal and returns the analysis report.

  > **Warning:** `analyse_file` uploads the raw file contents to VirusTotal, where samples are shared with the VirusTotal intelligence community according to your account tier. Do not pass confidential documents, credentials, or proprietary binaries unless your organization permits external submission. Use `get_file_report(hash)` for hash-only lookups.

- **`search_digital_threat_monitoring(query, size=10, since=None, until=None, page=None, truncate=None, sanitize=True)`**: Searches GTI Digital Threat Monitoring (DTM) surface, deep, and dark web records (forum posts, paste sites, shop listings, and Telegram channels) using Lucene syntax such as `(__type:forum_post) AND (label_threat:information-security/malware)`.

### IOC search and standard YARA hunting rulesets (3 tools)

GTI hunting rulesets use **standard YARA** syntax to match binary files and payloads across VirusTotal submissions (distinct from Google SecOps **YARA-L 2.0**, which evaluates UDM security event logs).

- **`search_iocs(query, limit=10, order_by="last_submission_date-")`**: Searches files, URLs, domains, and IP addresses using GTI / VirusTotal intelligence modifiers (for example, `entity:file p:10+ tag:ransomware` or `entity:ip country:RU`).
- **`get_hunting_ruleset(ruleset_id)`**: Retrieves a GTI Livehunt or Retrohunt ruleset object, including rule metadata and raw standard YARA rule definitions in the `rules` attribute.
- **`get_entities_related_to_a_hunting_ruleset(ruleset_id, relationship_name, limit=10)`**: Lists objects associated with a standard YARA hunting ruleset, such as `hunting_notification_files` (files that matched the ruleset).

### Threat profiles (4 tools)

Threat Profiles filter GTI intelligence by your organization's configured target industries, target regions, source regions, malware roles, and actor motivations.

- **`list_threat_profiles(limit=10)`**: Lists Threat Profiles configured in your GTI account. Check matching profiles first when scoping threat landscape questions to your organization.
- **`get_threat_profile(profile_id)`**: Retrieves a Threat Profile's configured interest filters (`INTEREST_TYPE_TARGETED_INDUSTRY`, `INTEREST_TYPE_TARGETED_REGION`, and related fields) and ML recommendation settings.
- **`get_threat_profile_recommendations(profile_id, limit=10)`**: Lists threat actors, malware families, toolkits, campaigns, IOC collections, reports, and vulnerabilities linked to `profile_id`.
- **`get_threat_profile_associations_timeline(profile_id, limit=10)`**: Retrieves first-seen and last-seen association timeline events for `profile_id`.

### Network locations: domains and IP addresses (4 tools)

- **`get_domain_report(domain)`**: Retrieves reputation verdicts, WHOIS details, DNS records, and categories for a domain.
- **`get_entities_related_to_a_domain(domain, relationship_name, descriptors_only, limit=10)`**: Lists related objects for a domain, such as `communicating_files`, `downloaded_files`, `referrer_files`, `resolutions`, `subdomains`, `siblings`, `urls`, and `associations`.
- **`get_ip_address_report(ip_address)`**: Retrieves reputation verdicts, ASN ownership, geolocation, and certificate context for an IPv4 or IPv6 address.
- **`get_entities_related_to_an_ip_address(ip_address, relationship_name, descriptors_only, limit=10)`**: Lists related objects for an IP address, such as `communicating_files`, `downloaded_files`, `referrer_files`, `resolutions`, `urls`, and `associations`.

### URLs (2 tools)

- **`get_url_report(url)`**: Retrieves scan verdicts, HTTP response metadata, categorization, and tracker details for a URL.
- **`get_entities_related_to_an_url(url, relationship_name, descriptors_only, limit=10)`**: Lists related objects for a URL, such as `downloaded_files`, `communicating_files`, `contacted_domains`, `contacted_ips`, `redirecting_urls`, `last_serving_ip_address`, and `associations`.

## Query syntax reference

Search tools (`search_threats`, `search_iocs`, and typed `search_*` helpers) accept GTI and VirusTotal intelligence search modifiers:

- Keyword search: `ransomware`
- Collection type and name: `collection_type:"malware-family" AND name:emotet`
- Date range filter: `collection_type:"threat-actor" AND last_modification_date:[2025-01-01 TO 2025-06-30]`
- Combined boolean filter: `collection_type:"campaign" AND targeted_industries:"financial" AND NOT name:emotet`
- IOC entity filter: `entity:ip country:RU positives:5+`

Full modifier catalogs:

- [VirusTotal file search modifiers](https://docs.virustotal.com/docs/file-search-modifiers)
- [VirusTotal domain search modifiers](https://docs.virustotal.com/docs/domain-search-modifiers)
- [VirusTotal IP address search modifiers](https://docs.virustotal.com/docs/ip-address-search-modifiers)
- [VirusTotal URL search modifiers](https://docs.virustotal.com/docs/url-search-modifiers)

## Usage examples

### Pivot from a suspicious SHA-256 hash to C2 infrastructure and YARA rules

1. Pull the file verdict and threat attribution:
   `get_file_report("e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855")`
2. Inspect sandbox execution behavior:
   `get_file_behavior_summary("e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855")`
3. Enumerate contacted C2 domains and associated threat collections:
   `get_entities_related_to_a_file("e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855", "contacted_domains", descriptors_only=True)`
   `get_entities_related_to_a_file("e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855", "associations", descriptors_only=True)`
4. Fetch curated standard YARA rules from a linked malware family collection:
   `get_collection_rules("malware-family--a1b2c3d4-e5f6-4321-abcd-ef1234567890", rule_types=["curated_yara_rule"])`

### Profile a threat actor and review MITRE ATT&CK coverage

1. Check your organization's configured Threat Profiles first:
   `list_threat_profiles(limit=10)`
2. Search for a specific actor collection:
   `search_threat_actors("APT41", limit=5)`
3. Retrieve the full report, analyst timeline, and MITRE ATT&CK matrix:
   `get_collection_report("threat-actor--a1b2c3d4-e5f6-4321-abcd-ef1234567890")`
   `get_collection_timeline_events("threat-actor--a1b2c3d4-e5f6-4321-abcd-ef1234567890")`
   `get_collection_mitre_tree("threat-actor--a1b2c3d4-e5f6-4321-abcd-ef1234567890")`
