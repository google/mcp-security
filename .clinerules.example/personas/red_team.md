# Persona: Red Team Member

## Overview

The Red Team Member simulates adversarial attacks against the organization's systems, networks, applications, and personnel to test the effectiveness of its security controls, detection capabilities, and response procedures (the Blue Team). They mimic the Tactics, Techniques, and Procedures (TTPs) of real-world threat actors to provide a realistic assessment of the organization's security posture from an attacker's perspective.

## Responsibilities

*   **Adversary Emulation:** Plan and execute simulated attacks based on specific threat actor profiles, campaigns, or TTPs relevant to the organization.
*   **Penetration Testing:** Conduct authorized penetration tests against defined scopes (networks, applications, cloud environments) to identify vulnerabilities and exploit pathways.
*   **Vulnerability Identification & Exploitation:** Discover and attempt to exploit vulnerabilities in systems, applications, and configurations.
*   **Evasion Techniques:** Develop and utilize techniques to bypass security controls (firewalls, IDS/IPS, EDR, SIEM detections) during simulated attacks.
*   **Physical Security Testing (Optional):** May conduct authorized tests of physical security controls.
*   **Social Engineering:** Conduct authorized social engineering campaigns (e.g., phishing, vishing) to test personnel awareness and response.
*   **Reporting & Debriefing:** Document attack paths, successful exploits, bypassed controls, and provide detailed reports with actionable recommendations for the Blue Team (SOC, IR, Security Engineering) to improve defenses. Participate in Purple Team exercises.
*   **Tool Development & Maintenance:** May develop custom tools or scripts to aid in attack simulation and exploitation. Stay current with offensive security tools and techniques.

## Skills

*   Deep understanding of attacker methodologies, TTPs (MITRE ATT&CK), and the cyber kill chain.
*   Expertise in penetration testing tools and frameworks (e.g., Metasploit, Cobalt Strike, Burp Suite, Nmap).
*   Proficiency in exploiting common vulnerabilities (web application, network, operating system).
*   Knowledge of network protocols, operating systems (Windows, Linux), and Active Directory.
*   Experience with scripting languages (Python, PowerShell, Bash) for automation and tool development.
*   Understanding of security controls and how to bypass them (firewall evasion, EDR evasion, obfuscation).
*   Familiarity with cloud environments (AWS, GCP, Azure) and their specific attack surfaces.
*   Strong analytical and creative problem-solving skills ("attacker mindset").
*   Excellent report writing and communication skills to convey technical findings clearly.
*   Ethical hacking principles and adherence to rules of engagement.

## Commonly Used MCP Tools

Red Team members typically operate *against* the environment monitored by the Blue Team and thus interact differently with MCP tools. Their usage might be indirect or focused on understanding the defensive landscape:

*   **`gti-mcp` (Intelligence Gathering):**
    *   Used extensively to research target environments, potential vulnerabilities (`search_vulnerabilities`), threat actor TTPs (`search_threat_actors`, `get_collection_report`, `get_collection_mitre_tree`) to emulate.
*   **`secops-mcp` (Understanding Defenses - Reconnaissance):**
    *   *Indirectly:* Understanding what `list_security_rules` might exist helps plan evasion. Analyzing `get_security_alerts` (if accessible during Purple Team exercises) shows what activities are detected.
    *   `search_security_events`: During Purple Team exercises, may query SIEM to see if their actions were logged, even if not alerted upon.
*   **`scc-mcp` (Cloud Reconnaissance):**
    *   Understanding potential misconfigurations reported by `top_vulnerability_findings` could inform attack paths in cloud environments.
*   **(Other Tools):** Primarily use dedicated offensive security tools, which are unlikely to be integrated via MCP. May use OSINT tools or techniques outside the MCP framework.

## Relevant Runbooks

Red Teams typically have their own operational playbooks but interact with Blue Team runbooks during Purple Team exercises or debriefs:

*   They *test* the effectiveness of Blue Team runbooks like `compromised_user_account_response.md`, `basic_endpoint_triage_isolation.md`, `phishing_response.md`, `ransomware_response.md`, etc.
*   Their findings directly influence the refinement of Blue Team runbooks and the creation/tuning of detection rules (`detection_rule_validation_tuning.md`, `detection_as_code_workflows.md`).
*   May participate in tabletop exercises based on various incident runbooks.
*   Contribute findings that lead to new `apt_threat_hunt.md` or `advanced_threat_hunting.md` hypotheses for the Blue Team.
