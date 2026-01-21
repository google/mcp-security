# Tool Mapping: Local vs. Remote

This document maps the tools defined in the local MCP server implementation (`server/secops` and `server/secops-soar`) to the tools available in the remote Google SecOps MCP server.

**Configuration & Selection Strategy:**
When executing a skill, the agent should first check which tools are available in the current environment.
1.  **Prioritize Remote Tools**: If a remote tool is available, use it.
2.  **Fallback to Local Tools**: If the remote tool is unavailable, use the corresponding local tool.
3.  **Adapt Workflow**: Some operations (like Natural Language Search) require a multi-step workflow in Remote (Translate -> Search) but a single step in Local.

| Category | Capability | Remote Tool (MCP Server) | Local Tool (Python) | Notes |
| :--- | :--- | :--- | :--- | :--- |
| **Case Management** | List Cases | `list_cases` | `list_cases` | |
| | Get Case Details | `get_case` | `get_case_full_details` | Local `get_case_full_details` aggregates alerts/comments. Remote `get_case` fetches the case object; use `expand='tasks,tags,products'` or call `list_case_alerts`/`list_case_comments` for full context. |
| | Comment on Case | `create_case_comment` | `post_case_comment` | |
| | Update Case | `update_case` | `change_case_priority` | Remote tool is general (priority, status, assignee). Local tool is specific to priority. |
| | Close Case | `execute_bulk_close_case` | *(No local tool)* | Only remote tool can close cases. |
| **Alerts (SOAR)** | List Alerts for Case | `list_case_alerts` | `list_alerts_by_case` | |
| | List Events for Alert | `list_connector_events` | `list_events_by_alert` | Remote tool lists "connector events". |
| | List Alert Groups | *(No direct equivalent)* | `list_alert_group_identifiers_by_case` | Remote `list_case_alerts` returns alert objects which may contain grouping info. |
| **Entities (SOAR)** | Search Entities | `search_entity` | `search_entity` | |
| | Get Involved Entities | `list_involved_entities` | `get_entities_by_alert_group_identifiers` | Remote tool lists involved entities for a specific case alert. |
| | Get Entity Details | *(No direct equivalent)* | `get_entity_details` | |
| **SIEM / UDM** | UDM Search (Query) | `udm_search` | `search_udm` | |
| | UDM Search (Nat. Lang.) | `translate_udm_query` -> `udm_search` | `search_security_events` | **Critical:** Remote requires 2 steps (Translate then Search). Local does both in one call. |
| | Entity Summary | `summarize_entity` | `lookup_entity` | Both provide a summary of entity activity in SIEM. |
| | IoC Matching | `get_ioc_match` | `get_ioc_matches` | |
| | Export Results | *(No direct equivalent)* | `export_udm_search_csv` | |
| **Alerts (SIEM)** | List SIEM Alerts | `list_security_alerts` | `list_security_alerts` | Lists alerts directly from SIEM (not SOAR cases). |
| | Get SIEM Alert | `get_security_alert` | `get_security_alert` | |
| | Update SIEM Alert | `update_security_alert` | `update_security_alert` | |
| **Rules** | List Rules | `list_rules` | `list_rules` | |
| | Get Rule | `get_rule` | `get_rule` | |
| | Create Rule | `create_rule` | `create_rule` | |
| | Validate Rule | `validate_rule` | `validate_rule` | |
| | Test/Run Rule | `list_rule_detections` | `list_rule_detections` | Use to see historical detections. |