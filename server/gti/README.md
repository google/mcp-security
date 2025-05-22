# Google Threat Intelligence MCP Server

This is an MCP (Model Context Protocol) server for interacting with Google's
Threat Intelligence suite.
[MCP Info](https://modelcontextprotocol.io/introduction)

## Features

### Collections (Threats)

- **`get_collection_report(id)`**: Retrieves a specific collection report by its ID (e.g., `report--<hash>`, `threat-actor--<hash>`).
- **`get_entities_related_to_a_collection(id, relationship_name)`**: Gets related entities (domains, files, IPs, URLs, other collections) for a given collection ID.
- **`search_threats(query, limit=10, order_by="relevance-")`**: Performs a general search for threats (collections) using GTI query syntax.
- **`search_campaigns(query, limit=10, order_by="relevance-")`**: Searches specifically for collections of type `campaign`.
- **`search_threat_actors(query, limit=10, order_by="relevance-")`**: Searches specifically for collections of type `threat-actor`.
- **`search_malware_families(query, limit=10, order_by="relevance-")`**: Searches specifically for collections of type `malware-family`.
- **`search_software_toolkits(query, limit=10, order_by="relevance-")`**: Searches specifically for collections of type `software-toolkit`.
- **`search_threat_reports(query, limit=10, order_by="relevance-")`**: Searches specifically for collections of type `report`.
- **`search_vulnerabilities(query, limit=10, order_by="relevance-")`**: Searches specifically for collections of type `vulnerability`.
- **`get_collection_timeline_events(id)`**: Retrieves curated timeline events for a collection.

### Files

- **`get_file_report(hash)`**: Retrieves a comprehensive analysis report for a file based on its MD5, SHA1, or SHA256 hash.
- **`get_entities_related_to_a_file(hash, relationship_name)`**: Gets related entities (domains, IPs, URLs, behaviours, etc.) for a given file hash.
- **`get_file_behavior_report(file_behaviour_id)`**: Retrieves a specific sandbox behavior report for a file.
- **`get_file_behavior_summary(hash)`**: Retrieves a summary of all sandbox behavior reports for a file hash.

### Intelligence Search

- **`search_iocs(query, limit=10, order_by="last_submission_date-")`**: Searches for Indicators of Compromise (files, URLs, domains, IPs) using advanced GTI query syntax.

### Network Locations (Domains & IPs)

- **`get_domain_report(domain)`**: Retrieves a comprehensive analysis report for a domain.
- **`get_entities_related_to_a_domain(domain, relationship_name)`**: Gets related entities for a given domain.
- **`get_ip_address_report(ip_address)`**: Retrieves a comprehensive analysis report for an IPv4 or IPv6 address.
- **`get_entities_related_to_an_ip_address(ip_address, relationship_name)`**: Gets related entities for a given IP address.

### URLs

- **`get_url_report(url)`**: Retrieves a comprehensive analysis report for a URL.
- **`get_entities_related_to_an_url(url, relationship_name)`**: Gets related entities for a given URL.

### Hunting

- **`get_hunting_ruleset`**: Get a Hunting Ruleset object from Google Threat Intelligence
- **`get_entities_related_to_a_hunting_ruleset`**:  Retrieve entities related to the the given Hunting Ruleset.

### Threat Profiles

- **`list_threat_profiles`**: List your Threat Profiles at Google Threat Intelligence.
- **`get_threat_profile(profile_id)`**: Get Threat Profile object.
- **`get_threat_profile_recommendations(profile_id)`**: Returns the list of objects associated to the given Threat Profile.
- **`get_threat_profile_associations_timeline(profile_id)`**: Retrieves the associations timeline for the given Threat Profile.

## Configuration

### MCP Server Configuration

Add the following configuration to your MCP client's settings file:

**NOTE:** For OSX users, if you used [this one-liner](https://docs.astral.sh/uv/getting-started/installation/#standalone-installer) to install uv, use the full path to the uv binary for the "command" value below, as uv will not be placed in the system path for Claude to use! For example: `/Users/yourusername/.local/bin/uv` instead of just `uv`.

```json
{
  "mcpServers": {
    "gti": {
      "command": "uv",
      "args": [
        "--env-file=/path/to/your/env",
        "--directory",
        "/path/to/the/repo/server/gti/gti_mcp",
        "run",
        "server.py"
      ],
      "env": {
        "VT_APIKEY": "${VT_APIKEY}"
      },
      "disabled": false,
      "autoApprove": []
    }
  }
}
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

## License

Apache 2.0

## Development

The project is structured as follows:

- `gti_mcp/server.py`: Main MCP server implementation
- `gti_mcp/utils.py`: Utils to consume VirusTotal API using vt-py library.
- `gti_mcp/tools/`: Folder containing tools.
