# Google Threat Intelligence workflows

The local `gti-mcp` server exposes 50 tools covering indicator reports, threat collections, sandbox behaviors, hunting rules, non-blocking scans, and multi-turn GTI Agentic sessions. Pick the workflow below that matches your task.

## Choose the right tool group

| Goal | Recommended tools | Guide |
| :--- | :--- | :--- |
| Check a known hash, URL, domain, or IP address | `get_file_report`, `get_url_report`, `get_domain_report`, `get_ip_address_report` | [GTI MCP Server reference](../servers/gti_mcp.md) |
| Upload a local file, detonate a URL, or refresh a stale verdict without blocking | `submit_file`, `submit_url`, `reanalyze_file`, `reanalyze_url`, `reanalyze_domain`, `reanalyze_ip`, `get_analysis` | [Scan and reanalyze artifacts](scanning_and_reanalysis.md) |
| Delegate an open-ended threat or malware investigation across multiple turns | `ask_gti_agent`, `continue_chat`, `get_session_history`, `share_session`, `copy_shared_session` | [Run multi-turn investigations with GTI Agentic](agentic_investigations.md) |
| Map campaigns to MITRE ATT&CK, extract YARA or Sigma rules, curate collections, or search dark web leaks | `list_threat_profiles`, `get_collection_mitre_tree`, `get_collection_rules`, `create_collection`, `search_digital_threat_monitoring` | [Curate threat collections, hunting rules, and Digital Threat Monitoring](collections_and_hunting.md) |

## Workflow guides

- [Scan and reanalyze files, URLs, domains, and IP addresses](scanning_and_reanalysis.md): Submit artifacts asynchronously, poll scan progress, inspect per-engine verdicts when needed, and respect community-sharing boundaries.
- [Run multi-turn investigations with GTI Agentic](agentic_investigations.md): Start stateful sessions with Google Threat Intelligence specialist agents, audit intermediate tool traces, share sessions across analysts, or connect directly to the hosted GTI Agentic MCP endpoint.
- [Curate threat collections, hunting rules, and Digital Threat Monitoring](collections_and_hunting.md): Filter threats with Threat Profiles, extract standard YARA file-matching rules and Sigma rules, pivot across IOC commonalities, build custom collections, and query Digital Threat Monitoring.

```{toctree}
:maxdepth: 2
:caption: GTI Workflow Guides

scanning_and_reanalysis
agentic_investigations
collections_and_hunting
```
