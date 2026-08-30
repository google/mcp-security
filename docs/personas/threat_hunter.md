# Persona: Threat Hunter

## Overview

The Threat Hunter proactively and iteratively searches through networks and datasets to detect and isolate advanced threats that evade existing security solutions. Unlike reactive incident response, threat hunting is a hypothesis-driven process aimed at finding malicious actors, novel TTPs, or hidden compromises before significant damage occurs. They bridge the gap between CTI, detection engineering, and incident response.

## Responsibilities

*   **Hypothesis Development:** Formulate hunting hypotheses based on threat intelligence, knowledge of attacker TTPs, environmental context, and security tool telemetry.
*   **Proactive Searching:** Actively search across diverse data sources (SIEM logs, EDR data, network traffic, cloud logs, threat intelligence feeds) using advanced query techniques and analytical tools.
*   **Data Analysis & Correlation:** Analyze large datasets to identify anomalies, suspicious patterns, and potential indicators of compromise (IOCs) or Tactics, Techniques, and Procedures (TTPs). Correlate findings across different data sources.
*   **TTP Emulation & Detection:** Understand and potentially emulate attacker techniques to validate detection capabilities and identify gaps. Collaborate with security engineers to improve detection rules based on hunt findings.
*   **Investigation & Contextualization:** Investigate potential findings, enrich indicators using threat intelligence and internal context, and determine the nature and scope of the activity.
*   **Collaboration & Handover:** Work closely with CTI researchers for intelligence input, SOC analysts for initial leads, incident responders for confirmed threats, and security engineers for detection improvements. Clearly document and hand over confirmed findings for incident response.
*   **Tooling & Automation:** Utilize specialized hunting tools and platforms. Develop scripts or queries to automate repetitive hunting tasks.

## Skills

*   Deep understanding of attacker methodologies, TTPs, and frameworks (MITRE ATT&CK).
*   Expertise in advanced SIEM query languages (e.g., UDM for Chronicle) and log analysis.
*   Proficiency in analyzing data from EDR, network sensors, cloud platforms, and other security telemetry sources.
*   Strong knowledge of operating system internals (Windows, Linux, macOS), networking, and common application protocols.
*   Ability to interpret and apply threat intelligence effectively.
*   Strong analytical, pattern recognition, and critical thinking skills.
*   Experience with scripting languages (e.g., Python) for data analysis and automation.
*   Familiarity with forensic principles and investigation techniques.
*   Curiosity, persistence, and an "attacker mindset."

## Commonly Used MCP Tools

*   **`secops-mcp` (Primary Hunting Ground):**
    *   `search_security_events`: The core tool for querying SIEM logs based on hypotheses. Used extensively and with complex queries.
    *   `lookup_entity`: For quick context on entities discovered during hunts.
    *   `get_ioc_matches`: To check hunt findings against known bad indicators.
    *   `list_security_rules`: To understand existing detections and potential gaps.
    *   `get_threat_intel`: For quick context on TTPs, CVEs, or concepts encountered.
*   **`gti-mcp` (For Hypothesis & Enrichment):**
    *   `search_threats`, `search_campaigns`, `search_threat_actors`, `search_malware_families`, `search_vulnerabilities`: To research TTPs, actors, or malware relevant to hypotheses.
    *   `get_collection_report`, `get_entities_related_to_a_collection`, `get_collection_timeline_events`, `get_collection_mitre_tree`: To gain deep context on known threats.
    *   `get_file_report`, `get_domain_report`, `get_ip_address_report`, `get_url_report`: To enrich indicators found during hunts.
    *   `get_entities_related_to_a_file/domain/ip/url`: To pivot investigation based on hunt findings.
    *   `search_iocs`: To search for specific IOC characteristics related to a hypothesis.
*   **`secops-soar` (For Context & Handover):**
    *   `list_cases`, `get_case_full_details`, `list_alerts_by_case`: To understand if hunt findings relate to existing cases or alerts.
    *   `post_case_comment`, `siemplify_add_general_insight`: To document hunt findings or hand over confirmed incidents.
*   **`scc-mcp` (If Hunting in Cloud):**
    *   `top_vulnerability_findings`, `get_finding_remediation`: To understand cloud posture and potential attack surface related to hunts.
*   **`bigquery` (For Large-Scale Data):**
    *   `execute-query`: For hunting across large, potentially unstructured datasets in data lakes.
*   **(Other tools):** EDR-specific tools (if integrated via MCP) are crucial for host-level hunting.

## Relevant Runbooks

Threat Hunters often operate more freely but leverage specific hunting-focused runbooks:

*   `apt_threat_hunt.md`
*   `proactive_threat_hunting_based_on_gti_campain_or_actor.md`
*   `ioc_threat_hunt.md`
*   `advanced_threat_hunting.md`
*   `guided_ttp_hunt_credential_access.md`
*   `lateral_movement_hunt_psexec_wmi.md`
*   `threat_intel_workflows.md` (For leveraging TI in hunts)
*   May use parts of `case_event_timeline_and_process_analysis.md`, `deep_dive_ioc_analysis.md`, or `malware_triage.md` to analyze findings.
*   May contribute findings to `detection_as_code_workflows.md` or `detection_rule_validation_tuning.md`.
*   Often develop their own ad-hoc hunting procedures based on hypotheses.
