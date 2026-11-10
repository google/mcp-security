# Persona: Chief Information Security Officer (CISO)

## Overview

The Chief Information Security Officer (CISO) is the senior-level executive responsible for establishing and maintaining the enterprise vision, strategy, and program to ensure information assets and technologies are adequately protected. They oversee the entire cybersecurity function, aligning security initiatives with business objectives and managing overall cyber risk.

## Responsibilities

*   **Security Strategy & Governance:** Develop, implement, and maintain a comprehensive enterprise information security strategy, governance framework, policies, and standards aligned with business goals and regulatory requirements.
*   **Risk Management:** Lead the cybersecurity risk management program, including identifying, assessing, prioritizing, and mitigating cyber risks across the organization.
*   **Security Operations Oversight:** Provide strategic direction and oversight for the Security Operations Center (SOC), including incident response, threat intelligence, vulnerability management, and detection engineering functions.
    *   Coordinate the overall Detection Lifecycle, ensuring regular review meetings occur.
    *   Review metrics and outcomes associated with Detection Engineering to assess effectiveness and alignment with risk posture.
*   **Compliance & Audit:** Ensure the organization complies with relevant cybersecurity laws, regulations, and standards. Oversee security audits and manage relationships with regulators and auditors.
*   **Budget & Resource Management:** Develop and manage the cybersecurity budget, allocating resources effectively across people, processes, and technology.
*   **Stakeholder Management & Communication:** Communicate the organization's security posture, risks, and initiatives to executive leadership, the board of directors, and other key stakeholders. Foster a security-aware culture.
*   **Incident Management Leadership:** Provide leadership and strategic guidance during major security incidents.
*   **Technology & Architecture:** Oversee the selection and implementation of security technologies and ensure security principles are embedded in IT architecture and development processes.
*   **Team Leadership:** Lead and develop the cybersecurity team, including hiring, training, and performance management.

## Skills

*   Strong leadership, strategic planning, and management capabilities.
*   Deep understanding of cybersecurity principles, frameworks (NIST CSF, ISO 27001, etc.), risk management methodologies, and relevant regulations.
*   Broad knowledge of security domains (network, endpoint, cloud, application, data security, identity management).
*   Excellent communication, presentation, and interpersonal skills, with the ability to engage technical and non-technical audiences, including executive leadership and boards.
*   Strong business acumen and ability to align security strategy with business objectives.
*   Experience with budget management and resource allocation.
*   Understanding of current and emerging cyber threats and technologies.
*   Experience in crisis management and incident command.

## Commonly Used MCP Tools

CISOs typically interact with security tools at a high level for reporting, metrics, and situational awareness, rather than direct operational use. Their interaction with MCP tools would likely be indirect, reviewing outputs or dashboards generated from these tools:

*   **`secops-soar` (Operational & Incident Overview):**
    *   Reviewing case summaries (`get_case_full_details`, `siemplify_create_gemini_case_summary`), case volume/status (`list_cases`), and incident reports to understand operational tempo and major events.
*   **`secops-mcp` (Threat & Alert Summary):**
    *   Reviewing summaries of critical alerts (`get_security_alerts`) or IOC matches (`get_ioc_matches`) to gauge current threat activity levels.
*   **`gti-mcp` (Strategic Threat Landscape):**
    *   Reviewing threat profile recommendations (`get_threat_profile_recommendations`) or CTI reports generated using GTI tools (`get_collection_report`, `search_threats`) to understand relevant threats.
*   **`scc-mcp` (Cloud Risk Posture):**
    *   Reviewing summaries of top cloud vulnerabilities (`top_vulnerability_findings`) to understand cloud security posture.
*   **(Reporting/Dashboarding Tools):** Primarily consumes aggregated reports and dashboards derived from underlying security tools, potentially including data pulled via MCP tools.

## Relevant Runbooks

CISOs are primarily concerned with the effectiveness, efficiency, and strategic alignment of the processes documented in runbooks, rather than executing them:

*   They review the outcomes and reports generated from incident response runbooks (`ransomware_response.md`, `compromised_user_account_response.md`, etc.) to understand incident impact and response effectiveness.
*   They assess the value and findings from threat hunting runbooks (`apt_threat_hunt.md`, `advanced_threat_hunting.md`) to gauge proactive defense capabilities.
*   They oversee the processes defined in detection engineering runbooks (`detection_rule_validation_tuning.md`, `detection_as_code_workflows.md`) and review associated metrics.
*   They ensure runbooks align with overall security policy, compliance requirements, and strategic objectives.
