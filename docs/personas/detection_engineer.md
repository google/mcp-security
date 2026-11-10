# Persona: Detection Engineer

## Overview

The Detection Engineer, sometimes referred to as a Content Developer, is responsible for the lifecycle of security detections within the organization's monitoring tools (primarily SIEM and EDR). They translate threat intelligence, incident findings, hunting results, and security requirements into effective detection logic. Their goal is to continuously improve the organization's ability to detect threats accurately and efficiently, balancing detection coverage with alert fidelity.

## Responsibilities

*   **Detection Development:** Design, draft, and implement detection logic (e.g., SIEM rules, EDR queries) based on security use cases, threat models (MITRE ATT&CK), available logs/telemetry, and input from CTI, Threat Hunting, and SOC Analysts.
*   **Testing & Validation:** Develop and execute test plans for new detections using historical data, simulated attacks, or controlled environment testing. Validate rule logic and ensure it triggers as expected.
*   **Tuning & Optimization:** Analyze the performance of existing detections, identify false positives/negatives, and tune rule logic, thresholds, or exceptions to improve accuracy and reduce alert fatigue. Respond to tuning requests from SOC Analysts.
*   **Deployment & Lifecycle Management:** Deploy tested and approved detections into production environments following established processes (potentially including Detection-as-Code workflows). Maintain a detection catalog and track the evolution and performance of detections.
*   **Collaboration:** Work closely with SOC Analysts (feedback on alerts), Threat Hunters (new detection ideas), CTI Researchers (intelligence requirements), Incident Responders (post-incident detection gaps), and Security Platform Engineers (tool capabilities/limitations). Participate in Detection Engineering meetings.
*   **Documentation & Training:** Document detection logic, purpose, expected behavior, and response guidance. Develop training materials or runbooks for new detections to aid SOC Analysts.
*   **Metric Tracking:** Track metrics related to detection development, performance (TP/FP rates), and coverage.

## Skills

*   Strong understanding of security principles, common attack vectors, TTPs (MITRE ATT&CK), and threat actor methodologies.
*   Proficiency in SIEM query languages (e.g., YARA-L for Chronicle) and potentially EDR query languages.
*   Experience with log analysis across various platforms (OS, network, cloud, applications).
*   Ability to translate threat intelligence and attack techniques into specific detection logic.
*   Experience with detection rule testing, validation, and tuning methodologies.
*   Understanding of security tool capabilities and limitations (SIEM, EDR).
*   Scripting skills (e.g., Python) for automation, testing, or analysis are a plus.
*   Strong analytical and problem-solving skills.
*   Good documentation and communication skills.

## Commonly Used MCP Tools

*   **`secops-mcp` (Primary Toolset):**
    *   `search_security_events`: Essential for testing rule logic against historical data, analyzing alert context, understanding log formats, and validating potential false positives/negatives.
    *   `list_security_rules`: To review existing rules, identify overlaps, and understand current coverage.
    *   `get_security_alerts`: To analyze the performance and triggering patterns of specific rules.
    *   `lookup_entity`: To quickly gather context on entities involved in test alerts or potential FPs/FNs.
    *   *(Potentially tools for rule creation/modification/deployment if available via MCP, e.g., `create_detection_rule`, `update_detection_rule`)*
    *   *(Potentially `validate_udm_query` if available)*
*   **`gti-mcp` (For Context & Rule Ideas):**
    *   `search_threats`, `get_collection_report`, `get_collection_mitre_tree`, `get_threat_intel`: To research threats, TTPs, and vulnerabilities that require detection coverage.
    *   `get_file_report`, `get_domain_report`, etc.: To understand IOC characteristics for rule development.
*   **`secops-soar` (For Context & Workflow):**
    *   `get_case_full_details`, `list_alerts_by_case`, `list_events_by_alert`: To understand how existing detections perform in real incidents and gather feedback/tuning requests from analysts' comments.
    *   May interact with SOAR playbooks related to detection deployment or validation if they exist.
*   **`scc-mcp` (For Cloud Detections):**
    *   Used to understand cloud configurations and logs when developing cloud-specific detections.
*   **`bigquery` (For Large-Scale Testing):**
    *   `execute-query`: For testing rules against large historical datasets in data lakes.

## Relevant Runbooks

Detection Engineers are central to the detection lifecycle and related processes:

*   `detection_rule_validation_tuning.md`: Core workflow for analyzing and tuning rules.
*   `detection_as_code_workflows.md`: Defines the process for developing and deploying rules if using DaC.
*   `detection_report.md`: Used to document the performance and logic of specific detections.
*   Actively consume findings from hunting runbooks (`apt_threat_hunt.md`, `ioc_threat_hunt.md`, `advanced_threat_hunting.md`, etc.) as input for new detection ideas.
*   Review investigation runbooks (`case_event_timeline_and_process_analysis.md`, `malware_triage.md`, `ransomware_response.md`, etc.) to identify detection gaps revealed during incidents.
*   Collaborate on runbooks that require specific detection steps or context.

## References

*   [OSSOCDOCS - PRO - Detection Engineering](https://github.com/madirish/ossocdocs/blob/main/Detection%20Engineering/PRO%20-%20Detection%20Engineering.md)
