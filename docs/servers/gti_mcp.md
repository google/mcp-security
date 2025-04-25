# Google Threat Intelligence (GTI) MCP Server

This server provides tools for interacting with the Google Threat Intelligence (VirusTotal) API.

## Configuration

To use this server, you need a VirusTotal API key:

1. Register for a VirusTotal account at [virustotal.com](https://www.virustotal.com)
2. Navigate to your profile and obtain your API key
3. Add the API key to your MCP server configuration using environment variables

### MCP Server Configuration

Add the following configuration to your MCP client's settings file:

```json
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
      },
      "disabled": false,
      "autoApprove": []
    }
```

#### `--env-file`

Recommended: use the `--env-file` option in `uv` to move your secrets to an `.env` file for environment variables. You can create this file or use system environment variables as described below.

Your revised config would then be:

```json
      ...
      "command": "uv",
      "args": [
        "--directory",
        "/path/to/the/repo/server/gti/gti_mcp",
        "run",
        "--env-file",
        "/path/to/the/repo/.env",
        "server.py"
      ],
      "env": {},
      ...
```

Example .env file:
```
VT_APIKEY=0123456789abcdef0123456789abcdef0123456789abcdef0123456789abcdef
```

### Environment Variable Setup

Set up the `VT_APIKEY` environment variable in your system:

**For macOS/Linux:**
```bash
export VT_APIKEY="your-vt-api-key"
```

**For Windows PowerShell:**
```powershell
$Env:VT_APIKEY = "your-vt-api-key"
```

For more detailed instructions on setting up environment variables, refer to the [usage guide](../usage_guide.md#setting-up-environment-variables).

## Tools

### Collections (Threats)

Threats like actors, malware, campaigns, reports, and vulnerabilities are modeled as "collections" in GTI.

- **`get_collection_report(id)`**: Retrieves a specific collection report by its ID (e.g., `report--<hash>`, `threat-actor--<hash>`).
- **`get_entities_related_to_a_collection(id, relationship_name)`**: Gets related entities (domains, files, IPs, URLs, other collections) for a given collection ID. Valid values for `relationship_name` include:
  - `related_reference`: Related references or documents
  - `execution_parents`: Parent processes/files
  - `dropped_files`: Files dropped by malware
  - `contacted_domains`: Domains contacted by a threat
  - `contacted_urls`: URLs accessed by a threat
  - `contacted_ips`: IP addresses contacted by a threat
  - `embedded_collections`: Other collections embedded within this one
- **`search_threats(query, limit=10, order_by="relevance-")`**: Performs a general search for threats (collections) using GTI query syntax. Supports filtering by `collection_type:"<type>"` within the query.
- **`search_campaigns(query, limit=10, order_by="relevance-")`**: Searches specifically for collections of type `campaign`.
- **`search_threat_actors(query, limit=10, order_by="relevance-")`**: Searches specifically for collections of type `threat-actor`.
- **`search_malware_families(query, limit=10, order_by="relevance-")`**: Searches specifically for collections of type `malware-family`.
- **`search_software_toolkits(query, limit=10, order_by="relevance-")`**: Searches specifically for collections of type `software-toolkit`.
- **`search_threat_reports(query, limit=10, order_by="relevance-")`**: Searches specifically for collections of type `report`.
- **`search_vulnerabilities(query, limit=10, order_by="relevance-")`**: Searches specifically for collections of type `vulnerability`.
- **`get_collection_timeline_events(id)`**: Retrieves curated timeline events for a collection (especially useful for campaigns and threat actors).

### Files

- **`get_file_report(hash)`**: Retrieves a comprehensive analysis report for a file based on its MD5, SHA1, or SHA256 hash.
- **`get_entities_related_to_a_file(hash, relationship_name)`**: Gets related entities (domains, IPs, URLs, behaviours, etc.) for a given file hash. Valid values for `relationship_name` include:
  - `contacted_domains`: Domains contacted by the file
  - `contacted_ips`: IP addresses contacted by the file
  - `contacted_urls`: URLs accessed by the file
  - `execution_parents`: Parent processes
  - `embedded_domains`: Domains embedded in the file
  - `execution_children`: Child processes spawned by this file
  - `behaviors`: Sandbox behavior reports
- **`get_file_behavior_report(file_behaviour_id)`**: Retrieves a specific sandbox behavior report for a file, identified by `{file_hash}_{sandbox_name}`.
- **`get_file_behavior_summary(hash)`**: Retrieves a summary of all sandbox behavior reports for a file hash.

### Intelligence Search

- **`search_iocs(query, limit=10, order_by="last_submission_date-")`**: Searches for Indicators of Compromise (files, URLs, domains, IPs) using advanced GTI query syntax. Supports entity-specific modifiers and ordering.

### Network Locations (Domains & IPs)

- **`get_domain_report(domain)`**: Retrieves a comprehensive analysis report for a domain.
- **`get_entities_related_to_a_domain(domain, relationship_name)`**: Gets related entities (files, resolutions, subdomains, URLs, etc.) for a given domain. Valid values for `relationship_name` include:
  - `communicating_files`: Files that communicate with this domain
  - `referrer_files`: Files that refer to this domain
  - `resolutions`: DNS resolutions for this domain
  - `siblings`: Sibling domains
  - `subdomains`: Subdomains of this domain
  - `urls`: URLs associated with this domain
- **`get_ip_address_report(ip_address)`**: Retrieves a comprehensive analysis report for an IPv4 or IPv6 address.
- **`get_entities_related_to_an_ip_address(ip_address, relationship_name)`**: Gets related entities (files, resolutions, URLs, etc.) for a given IP address. Valid values for `relationship_name` include:
  - `communicating_files`: Files that communicate with this IP
  - `downloaded_files`: Files downloaded from this IP
  - `referrer_files`: Files that refer to this IP
  - `resolutions`: DNS resolutions for this IP
  - `urls`: URLs associated with this IP

### URLs

- **`get_url_report(url)`**: Retrieves a comprehensive analysis report for a URL.
- **`get_entities_related_to_an_url(url, relationship_name)`**: Gets related entities (files, domains, IPs, redirects, etc.) for a given URL. Valid values for `relationship_name` include:
  - `downloaded_files`: Files downloaded from this URL
  - `communicating_files`: Files that communicate with this URL
  - `redirecting_urls`: URLs that redirect to this URL
  - `redirected_urls`: URLs that this URL redirects to

## Query Syntax Examples

GTI tools that accept a query parameter use specific syntax:

1. **Basic text search:**
   ```
   ransomware
   ```

2. **Type-specific filtering:**
   ```
   collection_type:"malware-family" AND name:emotet
   ```

3. **Date-based filtering:**
   ```
   collection_type:"threat-actor" AND last_modification_date:[2023-01-01 TO 2023-06-30]
   ```

4. **Combined filters:**
   ```
   collection_type:"campaign" AND targets:"financial" AND NOT name:emotet
   ```

5. **IOC search with specific attributes:**
   ```
   type:ip country:RU reputation:>7
   ```

For additional query syntax modifiers and search capabilities, refer to the VirusTotal documentation:
- File search modifiers: https://docs.virustotal.com/docs/file-search-modifiers
- Domain search modifiers: https://docs.virustotal.com/docs/domain-search-modifiers
- IP address search modifiers: https://docs.virustotal.com/docs/ip-address-search-modifiers
- URL search modifiers: https://docs.virustotal.com/docs/url-search-modifiers

## Usage Examples

### Example 1: Investigating a suspicious file

```
1. Get the file hash (MD5, SHA1, or SHA256)
2. Use get_file_report(hash) to retrieve analysis details
3. If malicious, use get_entities_related_to_a_file(hash, "contacted_domains") to see network connections
4. Check get_file_behavior_summary(hash) for sandbox behavior details
```

### Example 2: Researching a threat actor

```
1. Use search_threat_actors("APT28") to find the threat actor
2. Get the full report with get_collection_report(id) using the returned ID
3. View timeline events with get_collection_timeline_events(id)
4. Explore related malware with get_entities_related_to_a_collection(id, "embedded_collections")
```

### Example 3: Domain investigation

```
1. Use get_domain_report("suspicious-domain.com") to get basic information
2. Check for malware using get_entities_related_to_a_domain("suspicious-domain.com", "communicating_files")
3. Look for related subdomains with get_entities_related_to_a_domain("suspicious-domain.com", "subdomains")
```
