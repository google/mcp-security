# Google Threat Intelligence (GTI) MCP Server

This server provides tools for interacting with the Google Threat Intelligence (VirusTotal) API.

## Tools

### Collections (Threats)

Threats like actors, malware, campaigns, reports, and vulnerabilities are modeled as "collections" in GTI.

- **`get_collection_report(id)`**: Retrieves a specific collection report by its ID (e.g., `report--<hash>`, `threat-actor--<hash>`).
- **`get_entities_related_to_a_collection(id, relationship_name)`**: Gets related entities (domains, files, IPs, URLs, other collections) for a given collection ID. See tool description for available `relationship_name` values.
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
- **`get_entities_related_to_a_file(hash, relationship_name)`**: Gets related entities (domains, IPs, URLs, behaviours, etc.) for a given file hash. See tool description for available `relationship_name` values.
- **`get_file_behavior_report(file_behaviour_id)`**: Retrieves a specific sandbox behavior report for a file, identified by `{file_hash}_{sandbox_name}`.
- **`get_file_behavior_summary(hash)`**: Retrieves a summary of all sandbox behavior reports for a file hash.

### Intelligence Search

- **`search_iocs(query, limit=10, order_by="last_submission_date-")`**: Searches for Indicators of Compromise (files, URLs, domains, IPs) using advanced GTI query syntax. Supports entity-specific modifiers and ordering.

### Network Locations (Domains & IPs)

- **`get_domain_report(domain)`**: Retrieves a comprehensive analysis report for a domain.
- **`get_entities_related_to_a_domain(domain, relationship_name)`**: Gets related entities (files, resolutions, subdomains, URLs, etc.) for a given domain. See tool description for available `relationship_name` values.
- **`get_ip_address_report(ip_address)`**: Retrieves a comprehensive analysis report for an IPv4 or IPv6 address.
- **`get_entities_related_to_an_ip_address(ip_address, relationship_name)`**: Gets related entities (files, resolutions, URLs, etc.) for a given IP address. See tool description for available `relationship_name` values.

### URLs

- **`get_url_report(url)`**: Retrieves a comprehensive analysis report for a URL.
- **`get_entities_related_to_an_url(url, relationship_name)`**: Gets related entities (files, domains, IPs, redirects, etc.) for a given URL. See tool description for available `relationship_name` values.
