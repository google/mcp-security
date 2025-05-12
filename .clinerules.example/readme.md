# .clinerules Directory Overview

This directory contains configuration files and documentation to provide context and guidance for LLM Agents operating within this security environment.

## Existing Components

### Personas (`./personas/`)

*   **Purpose:** These files define standard roles within the security operations team (e.g., SOC Analyst Tiers 1-3, Incident Responder, Threat Hunter, CTI Researcher, Security Engineer, Compliance Manager, SOC Manager).
*   **Content:** Each persona description outlines typical responsibilities, required skills, commonly used MCP tools, and relevant runbooks.
*   **Usage by LLM Agent:** Helps the agent understand user intent, tailor responses and actions to the user's likely role and perspective, and select appropriate tools and runbooks.

### Runbooks (`./run_books/`)

*   **Purpose:** These files contain documented, step-by-step procedures or workflows for specific security operations tasks (e.g., triaging alerts, investigating IOCs, hunting for threats, responding to phishing).
*   **Content:** They often include objectives, scope, required inputs, specific MCP tools to use, workflow steps (sometimes visualized with diagrams like Mermaid), and expected outcomes.
*   **Usage by LLM Agent:** Serves as a primary plan for executing common security workflows, ensuring adherence to established procedures, guiding tool selection and sequencing, and promoting consistency.
*   **IRP vs. Runbook Distinction:** While all files here serve as procedural guides, we differentiate between:
    *   **Incident Response Plans (IRPs):** Located in the `./run_books/irps/` subdirectory, these outline the *end-to-end strategy* for handling major incident types (e.g., malware, phishing) following the full PICERL lifecycle. They orchestrate multiple steps and often call other runbooks. Use these as the starting point for major incident types.
    *   **Runbooks:** Located directly within `./run_books/` or in `./run_books/common_steps/`, these provide detailed, *tactical steps* for specific tasks (e.g., enriching an IOC, triaging an alert, isolating an endpoint) or reusable procedures. They are often components within a larger IRP.

## Suggested Additional Context Files

The following types of files could further enhance an LLM Agent's effectiveness:

### 1. Environment & Infrastructure Context

*   **`network_map.md`**: Describes key network segments (e.g., DMZ, production servers, user subnets), their IP ranges, and primary functions. Helps in understanding the context of network events and potential lateral movement.
*   **`asset_inventory_guidelines.md`**: Outlines naming conventions for hosts/servers, common OS types, and potentially maps critical assets to their roles or owners. Helps contextualize alerts involving specific hosts.
*   **`critical_applications.md`**: Lists key business applications, their associated servers/IPs, and expected communication patterns. Useful for identifying anomalous behavior related to core services.
*   **`cloud_architecture.md`**: Provides an overview of the cloud environment structure (e.g., GCP project organization, key services like GKE, Cloud SQL), relevant for cloud-focused investigations (using SCC, etc.).

### 2. Tool Configuration & Usage

*   **`tool_configurations.md`**: Details specific configurations crucial for tool usage, like:
    *   Important Chronicle Reference List names (e.g., `IP_Blocklist`, `Domain_Allowlist`) and their purpose.
    *   Key SOAR playbook names/IDs and what triggers them.
    *   Default timeframes or limits preferred for certain searches.
*   **`mcp_tool_best_practices.md`**: Offers tips or preferred syntax for using specific MCP tools effectively (e.g., optimizing `search_security_events` queries, interpreting specific GTI fields).
*   **`tool_rate_limits.md`**: Explicitly lists known rate limits or quotas for tools (like the Chronicle UDM query limit mentioned for a SOAR action) to help manage usage.

### 3. Organizational Policies & Procedures

*   **`incident_severity_matrix.md`**: Defines how incident severity (Low, Medium, High, Critical) is determined based on impact and threat type. Aids in prioritization.
*   **`escalation_paths.md`**: Outlines who to notify or escalate to under specific circumstances (e.g., confirmed ransomware, PII exposure).
*   **`reporting_templates.md`**: Provides standard formats or key sections required for different types of reports (e.g., daily SOC summary, post-incident report).
*   **`approved_remediations.md`**: Lists standard, pre-approved containment or remediation actions for common, lower-severity findings.
*   **`key_contacts.md`**: Lists relevant teams or individuals for specific issues (e.g., Network Ops, Identity Team, Legal).

### 4. Threat Intelligence & Context

*   **`internal_threat_profile.md`**: Details specific threat actors, campaigns, or TTPs that are of high concern to *this specific organization*.
*   **`whitelists.md`**: Lists organization-specific known-good IPs, domains, file hashes, or process names that should generally be ignored unless context suggests otherwise.
*   **`common_benign_alerts.md`**: Describes alerts often triggered by known benign activity (e.g., vulnerability scans, specific admin scripts) and how to typically handle them.

Having these additional context files would allow the LLM Agent to perform more nuanced analysis, make better-informed decisions, adhere more closely to organizational standards, and require less clarification during complex tasks.
