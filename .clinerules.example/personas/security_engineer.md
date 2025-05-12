# Persona: Security Engineer

## Overview

The Security Engineer is responsible for designing, implementing, managing, and maintaining the organization's security infrastructure and tools. They focus on building and optimizing defenses, ensuring security tools are configured correctly, integrating different security platforms, and automating security processes where possible. Their goal is to create a robust and efficient security posture.

## Responsibilities

*   **Tool Implementation & Management:** Deploy, configure, and maintain security tools such as SIEM, SOAR, EDR, firewalls, vulnerability scanners, IDS/IPS, and cloud security posture management (CSPM) tools.
*   **Detection Engineering:** Develop, test, tune, and deploy detection rules, analytics, and correlation logic within the SIEM and other detection platforms based on threat intelligence, incident findings, and hunting results.
*   **Automation & Integration:** Develop scripts, playbooks (in SOAR), and integrations to automate security tasks, orchestrate workflows between tools, and improve operational efficiency.
*   **Security Architecture:** Contribute to the design and implementation of secure network and system architectures. Ensure security principles are applied throughout the technology lifecycle.
*   **Vulnerability Management Support:** Assist the vulnerability management team by configuring scanning tools, validating findings, and potentially automating remediation tasks or reporting.
*   **Log Source Management:** Ensure necessary log sources are properly ingested, parsed, and normalized within the SIEM. Troubleshoot logging issues.
*   **Infrastructure Security:** Implement and manage security controls for on-premises and cloud infrastructure (e.g., hardening, access controls, network segmentation).
*   **Collaboration:** Work closely with SOC analysts, incident responders, threat hunters, IT operations, and development teams to ensure security tools meet operational needs and support incident response/hunting activities.

## Skills

*   Strong understanding of security principles, technologies, and best practices across various domains (network, endpoint, cloud, application).
*   Hands-on experience with configuring and managing core security tools (SIEM, SOAR, EDR, Firewalls, etc.).
*   Proficiency in scripting languages (e.g., Python, PowerShell) for automation and integration.
*   Experience with detection rule logic and development (e.g., YARA-L, Sigma).
*   Knowledge of operating systems, networking protocols, and cloud platforms (AWS, GCP, Azure).
*   Understanding of logging mechanisms and data parsing/normalization.
*   Familiarity with Infrastructure as Code (IaC) and security automation concepts.
*   Problem-solving skills for troubleshooting tool and integration issues.
*   Good communication skills for collaborating with technical teams.

## Commonly Used MCP Tools

*   **`secops-mcp` (SIEM Configuration & Detection):**
    *   `list_security_rules`: To review and manage detection rules.
    *   `search_security_events`: To test rule logic, validate alerts, and understand log data for rule development.
    *   *(Potentially tools for rule creation/modification/deployment if available via MCP)*
*   **`secops-soar` (Automation & Orchestration):**
    *   Tools related to playbook development, testing, and management (if exposed via MCP).
    *   Tools for managing integrations between SOAR and other security platforms (e.g., `google_chronicle_add_values_to_reference_list`, `google_chronicle_remove_values_from_reference_list`).
    *   `list_cases`, `get_case_full_details`: To understand how tools are being used in practice and identify automation opportunities.
*   **`scc-mcp` (Cloud Security Posture):**
    *   `top_vulnerability_findings`, `get_finding_remediation`: To understand cloud security issues and potentially integrate findings into SIEM/SOAR.
*   **`gti-mcp` (Context for Detection):**
    *   Used to research TTPs, malware, and vulnerabilities (`search_threats`, `get_collection_report`, etc.) to inform detection rule creation.
*   **`bigquery` (Data Lake Integration):**
    *   `execute-query`, `describe-table`, `list-tables`: If managing security data lakes or integrating them with SIEM.
*   **(Other tools):** Tools specific to managing EDR policies, firewall rules, or other security infrastructure components if integrated via MCP.

## Relevant Runbooks

Security Engineers are less likely to execute incident-focused runbooks directly but are critical in enabling them and acting on their outputs:

*   `detection_as_code_workflows.md`: Core workflow for managing detection rules.
*   `detection_rule_validation_tuning.md`: May execute this runbook or act on its recommendations.
*   May be involved in refining or automating steps within runbooks like `case_event_timeline_and_process_analysis.md` or `proactive_threat_hunting_based_on_gti_campain_or_actor.md` by improving underlying tool capabilities or data collection.
*   Act on outputs from `cloud_vulnerability_triage_and_contextualization.md` by tuning cloud security tools or implementing remediation.
*   Use findings from various investigation runbooks (e.g., `deep_dive_ioc_analysis.md`, `malware_triage.md`, `advanced_threat_hunting.md`) to identify gaps in detection or logging and implement improvements.
