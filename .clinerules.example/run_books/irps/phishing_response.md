# Phishing Incident Response Plan (IRP) / Runbook

## Objective

Provide a structured workflow for responding to reported phishing emails, coordinating investigation, containment, eradication, and recovery efforts using available tools and procedures. This runbook orchestrates various specialized runbooks.

## Scope

This runbook covers the end-to-end response lifecycle for phishing incidents. It relies on specific sub-runbooks for detailed execution steps.

## Phases (PICERL Model)

1.  **Preparation:** *(Ongoing)* Ensure tools are operational, user reporting mechanisms are clear, communication templates exist, and relevant detections (e.g., for known bad domains/URLs) are active.
2.  **Identification:** Detect/Receive the report, perform initial triage, analyze email artifacts, enrich IOCs, and identify initial impact.
3.  **Containment:** Limit the spread and impact by blocking malicious IOCs and isolating/containing affected users or endpoints.
4.  **Eradication:** Remove malicious artifacts (e.g., delete similar emails, potentially remove malware if dropped).
5.  **Recovery:** Restore affected user accounts or systems to normal operation.
6.  **Lessons Learned (Post-Incident):** Review the incident and response to identify improvements.

## Inputs

*   `${CASE_ID}`: The SOAR case ID created for or associated with the initial report/alert(s).
*   `${ALERT_GROUP_IDENTIFIERS}`: Relevant alert group identifiers from the SOAR case.
*   `${REPORTED_EMAIL_ARTIFACTS}`: Information about the reported email, which could include:
    *   Email headers (as text or file).
    *   Email body (as text or file).
    *   Attached files (hashes or potentially file content if available safely).
    *   Reported URLs within the email.
    *   Recipient user ID(s).
    *   Sender address/domain.
*   *(Optional) `${EMAIL_GATEWAY_LOG_ID}`: Identifier for the email in the gateway logs.*

## Tools

*   **Email Analysis Tools (Conceptual/External):** Tools to parse headers, extract URLs/attachments, detonate URLs/attachments safely (sandbox). *MCP might not have direct tools for deep EML parsing/detonation.*
*   `gti-mcp`: `get_domain_report`, `get_ip_address_report`, `get_url_report`, `get_file_report`, `search_iocs`.
*   `secops-mcp`: `search_security_events`, `lookup_entity`.
*   `secops-soar`: `post_case_comment`, `get_case_full_details`.
*   **IOC Containment Runbook:** `../ioc_containment.md`
*   **Compromised User Account Response Runbook:** `../compromised_user_account_response.md`
*   **Basic Endpoint Triage & Isolation Runbook:** `../basic_endpoint_triage_isolation.md`
*   `ask_followup_question` (To confirm actions).
*   *(Potentially Email Gateway tools if integrated via MCP for searching/deleting emails)*
*   **Common Steps:** `common_steps/check_duplicate_cases.md`, `common_steps/enrich_ioc.md`, `common_steps/find_relevant_soar_case.md`, `common_steps/document_in_soar.md`

## Workflow Steps & Diagram

```{mermaid}
sequenceDiagram
    participant Analyst
    participant IRP as phishing_response.md (This Runbook)
    participant Preparation as Phase 1: Preparation
    participant Identification as Phase 2: Identification
    participant Containment as Phase 3: Containment
    participant Eradication as Phase 4: Eradication
    participant Recovery as Phase 5: Recovery
    participant LessonsLearned as Phase 6: Lessons Learned

    Analyst->>IRP: Start Phishing Response\nInput: CASE_ID, ALERT_GROUP_IDS, REPORTED_EMAIL_ARTIFACTS

    IRP->>Preparation: Verify Prerequisites (Ongoing)
    Preparation-->>IRP: Readiness Confirmed

    IRP->>Identification: Execute Identification Steps
    Identification-->>IRP: Initial Findings, Malicious IOCs, Affected Users/Endpoints

    IRP->>Containment: Execute Containment Steps
    Containment-->>IRP: Containment Status (IOCs, Users, Endpoints)

    IRP->>Eradication: Execute Eradication Steps
    Eradication-->>IRP: Eradication Status (e.g., Emails Deleted)

    IRP->>Recovery: Execute Recovery Steps
    Recovery-->>IRP: Recovery Status (Users/Endpoints)

    IRP->>LessonsLearned: Execute Post-Incident Steps
    LessonsLearned-->>IRP: Review Complete

    IRP-->>Analyst: Incident Response Complete
```

---

### Phase 1: Preparation (Ongoing)

*   **Objective:** Ensure readiness to respond effectively to phishing reports.
*   **Actions:**
    *   Verify tool connectivity (SIEM, SOAR, GTI, Email Gateway).
    *   Ensure user reporting mechanisms (e.g., "Report Phish" button) are functional and users are aware.
    *   **Maintain Lists:**
        *   List of all domains owned by the organization (to prevent accidental takedowns).
        *   List of personnel authorized to register domains.
    *   **Maintain Communication Templates:**
        *   Template for notifying employees of ongoing campaigns.
        *   Template for contacting hosting providers for domain takedowns.
        *   Template for informing third parties (e.g., impersonated brands) of abuse.
        *   Template for user warnings/guidance post-incident.
    *   Ensure relevant detections for known phishing indicators (domains, IPs, TTPs) are active in SIEM/Email Gateway.
    *   Familiarity with escalation paths (`.clinerules/escalation_paths.md`).
    *   *(Consider periodic phishing firedrills/simulations).*

---

### Phase 2: Identification

*   **Objective:** Analyze the reported email, identify malicious indicators, and determine the initial scope of impact.
*   **Sub-Runbooks/Steps:**
    1.  **Receive Input & Context:** Obtain email artifacts, `${CASE_ID}`, `${ALERT_GROUP_IDENTIFIERS}`. Get case details via `secops-soar.get_case_full_details`. Check for duplicates (`../common_steps/check_duplicate_cases.md`).
    2.  **Analyze Email Artifacts:**
        *   *(Conceptual/Manual Step or External Tool)* Parse headers to identify true sender, path, etc.
        *   Extract all URLs, sender domains/IPs, and attachment hashes (`EXTRACTED_IOCs`) from the email body and headers.
        *   *(Conceptual/Manual Step: If attachments are present, submit hashes to GTI/sandbox. If safe detonation is possible, analyze behavior).*
    3.  **Enrich Extracted IOCs:**
        *   Initialize `ENRICHMENT_RESULTS`. For each IOC `Ii` in `EXTRACTED_IOCs`:
            *   Execute `../common_steps/enrich_ioc.md` with `IOC_VALUE=Ii` and appropriate `IOC_TYPE`.
            *   Store results in `ENRICHMENT_RESULTS[Ii]`.
        *   Identify IOCs confirmed or strongly suspected to be malicious (`MALICIOUS_IOCs`).
    4.  **Categorize Phishing Type:**
        *   Based on sender, recipients, content, language, and enriched IOCs, determine the likely phishing category:
            *   **Generic Credential Phish:** Broad targeting, often impersonating large brands (e.g., Microsoft, Google, banks).
            *   **Spear Phishing:** Targeted towards specific individuals or roles, often using personalized information.
            *   **Whaling:** Spear phishing specifically targeting senior executives.
            *   **Business Email Compromise (BEC):** Typically involves impersonation to request fraudulent wire transfers, gift card purchases, or sensitive data. Often lacks malicious links/attachments.
            *   **Brand Impersonation:** Mimicking a known brand (e.g., shipping companies, software vendors).
            *   **Malware Delivery:** Primary goal is to get the user to open a malicious attachment or download malware via a link.
        *   Document the assessed category (`PHISHING_CATEGORY`). This helps prioritize and guide further investigation.
    5.  **(Optional) Verify Initial Findings:**
        *   *(Consider consulting with a Tier 2/3 analyst or senior team member to verify the initial assessment, enrichment findings, and categorization before proceeding with broader searches, especially for potentially high-impact categories like BEC or Whaling).*
    6.  **Search for Related Activity (SIEM):**
        *   Use `secops-mcp.search_security_events` to search for:
            *   Other emails with the same subject, sender, or key body phrases (requires email log source).
            *   Network connections or DNS lookups to `MALICIOUS_IOCs` (Domains/IPs).
            *   URL clicks involving `MALICIOUS_IOCs` (URLs) (requires proxy/DNS logs).
            *   File execution events involving `MALICIOUS_IOCs` (Hashes) (requires endpoint logs).
            *   Logins or other suspicious activity from recipient users around the time the email was received/clicked.
        *   Record findings (`SIEM_FINDINGS`).
    7.  **Identify Initial Impact:**
        *   Based on `SIEM_FINDINGS` and recipient lists, identify:
            *   Users who received similar emails (`SIMILAR_EMAIL_RECIPIENTS`).
            *   Users who potentially clicked/opened/interacted (`POTENTIAL_COMPROMISED_USERS`).
            *   Endpoints exhibiting suspicious activity related to the phish (`SUSPICIOUS_ENDPOINTS`).
    8.  **Check Related SOAR Cases:**
        *   Prepare list of key entities: `SEARCH_TERMS = POTENTIAL_COMPROMISED_USERS + SUSPICIOUS_ENDPOINTS + MALICIOUS_IOCs`.
        *   Execute `../common_steps/find_relevant_soar_case.md` with `SEARCH_TERMS` and `CASE_STATUS_FILTER="Opened"`.
        *   Obtain `${RELATED_SOAR_CASES}` (list of potentially relevant open case summaries/IDs).
    9.  **Document Identification Phase:**
        *   Document findings (including `PHISHING_CATEGORY` and `${RELATED_SOAR_CASES}`) using `../common_steps/document_in_soar.md`.

---

### Phase 3: Containment

*   **Objective:** Prevent further impact from the phishing campaign and contain any resulting compromises.
*   **Sub-Runbooks/Steps:**
    1.  **Network IOC Containment:**
        *   For each IOC `MIi` in `MALICIOUS_IOCs` (IPs, Domains, URLs):
            *   Execute `../ioc_containment.md` with `IOC_VALUE=MIi`, appropriate `IOC_TYPE`, and `${CASE_ID}`. **Confirm action with analyst.** Record status (`CONTAINMENT_STATUS[MIi]`).
            *   *(Optional/Manual Step): Submit malicious URLs/Domains to third-party blocklists (e.g., Google Safe Browsing, PhishTank) if appropriate.*
    2.  **User Account Containment:**
        *   For each user `Ui` in `POTENTIAL_COMPROMISED_USERS`:
            *   Execute `../compromised_user_account_response.md` for `USER_ID=Ui`. **Confirm actions with analyst.** Record status (`USER_TRIAGE_STATUS[Ui]`).
    3.  **Endpoint Isolation:**
        *   For each endpoint `Ei` in `SUSPICIOUS_ENDPOINTS`:
            *   Execute `../basic_endpoint_triage_isolation.md` for `ENDPOINT_ID=Ei`. **Confirm action with analyst.** Record status (`ENDPOINT_TRIAGE_STATUS[Ei]`).
    4.  **Verify Containment:**
        *   Monitor SIEM (`secops-mcp.search_security_events`) for continued activity related to `MALICIOUS_IOCs` or contained users/endpoints.
        *   Document containment status using `../common_steps/document_in_soar.md`.

---

### Phase 4: Eradication

*   **Objective:** Remove malicious artifacts related to the phishing campaign.
*   **Sub-Runbooks/Steps:**
    1.  **Delete Malicious Emails:**
        *   *(Requires Email Gateway/Platform integration or manual action)*
        *   Identify all recipients of the malicious email or similar variants (`SIMILAR_EMAIL_RECIPIENTS` from Phase 2).
        *   Use available tools (e.g., Email Gateway console, PowerShell scripts for Exchange/O365) to search mailboxes for emails matching key indicators (Subject, Sender, specific URLs/Hashes).
        *   Execute deletion/quarantine action for identified malicious emails. Document the number of emails deleted/quarantined.
    2.  **Address Malware (If Applicable):**
        *   If the phishing email led to malware execution (identified in Phase 2/3), follow the Eradication steps outlined in the `malware_incident_response.md` runbook for the affected endpoints.
    3.  **Document Eradication:**
        *   Document actions taken (e.g., email deletion counts) using `../common_steps/document_in_soar.md`.

---

### Phase 5: Recovery

*   **Objective:** Restore affected user accounts or systems to normal operation safely.
*   **Sub-Runbooks/Steps:**
    1.  **User Account Recovery:**
        *   If user accounts were disabled/passwords reset during Containment, follow procedures to safely re-enable them after confirming the threat is removed (potentially involves re-imaging user endpoint).
    2.  **Endpoint Recovery:**
        *   If endpoints were isolated and potentially infected with malware, follow the Recovery steps outlined in the `malware_incident_response.md` runbook or a dedicated system recovery runbook.
    3.  **Lift Containment:**
        *   Gradually remove IOC blocks or endpoint/user containment measures once confidence in recovery is high. Monitor closely.
    4.  **Validate Countermeasures:**
        *   After lifting containment or adjusting filters/blocks, verify that legitimate emails or network traffic are not inadvertently blocked by the measures implemented during the incident. Adjust rules/filters as necessary.
    5.  **Document Recovery:**
        *   Document steps taken (including validation) using `../common_steps/document_in_soar.md`.

---

### Phase 6: Lessons Learned (Post-Incident)

*   **Objective:** Review the incident and response to identify areas for improvement in prevention, detection, and response.
*   **Sub-Runbooks/Steps:** *(Consider creating a dedicated Post-Incident Review runbook)*
    1.  **Incident Review Meeting:** Convene relevant stakeholders (SOC, IR, Email Security, potentially affected user's manager) to discuss the incident timeline, root cause (how the phish bypassed defenses, why the user clicked/reported), response actions, and their effectiveness.
    2.  **Analyze Response & Identify Gaps:**
        *   Review the timeline: Was detection timely? Was response initiated promptly? Were containment actions effective?
        *   Review tool effectiveness: Did email filters miss the phish? Did SIEM/EDR alerts trigger appropriately? Were enrichment tools helpful?
        *   Review runbook adherence and effectiveness: Was the IRP followed? Were there gaps or unclear steps?
        *   Identify gaps in prevention (filtering, user awareness), detection (rules, IOC feeds), and response procedures.
    3.  **Develop Recommendations:** Based on identified gaps, formulate specific, actionable recommendations:
        *   **Prevention:** Update email filter rules, block sender domains/IPs permanently if warranted, improve DMARC/DKIM/SPF checks, enhance user awareness training (potentially targeted based on affected users/departments).
        *   **Detection:** Develop new SIEM/EDR rules based on observed TTPs or IOC patterns, update IOC feeds, tune existing rules that may have missed activity.
        *   **Response:** Update this IRP or related runbooks, improve tool integrations, clarify escalation paths.
    4.  **Update Defenses & Documentation:**
        *   Implement approved technical recommendations (e.g., update email filters, SIEM rules).
        *   Update relevant runbooks, policies, and procedures based on lessons learned.
    5.  **User Awareness Follow-up:**
        *   Ensure affected users receive appropriate follow-up and potentially targeted phishing awareness training.
    6.  **Track Recommendations:** Assign owners and deadlines for implementing recommendations and track them to completion.
    7.  **Final Report:** Generate a comprehensive post-incident report using guidelines from `.clinerules/reporting_templates.md` and `../report_writing.md`.
    8.  **Document Review:** Document the review meeting, findings, and recommendations using `../common_steps/document_in_soar.md` or a dedicated reporting system.

---

### Phase 7: Lessons Learned / Runbook Feedback

*   **Objective:** Capture feedback on the runbook's effectiveness and identify areas for improvement based on this incident.
*   **Actions:**
    1.  **Runbook Effectiveness:**
        *   Did this runbook accurately guide the response?
        *   Were there any unclear or missing steps?
        *   Did the tools function as expected based on the runbook steps?
    2.  **Tool Performance:**
        *   Were there any issues with specific MCP tool calls (errors, unexpected results, rate limits)?
        *   Did the tool outputs provide the necessary information?
    3.  **Process Gaps:**
        *   Did the incident reveal gaps in detection, prevention, or other related processes?
    4.  **Suggestions for Improvement:**
        *   Specific recommendations for updating this runbook.
        *   Suggestions for new detection rules or tuning existing ones.
        *   Recommendations for tool configuration changes or new tool requirements.
    5.  **Documentation:** Record this feedback within the SOAR case (`${CASE_ID}`) using `common_steps/document_in_soar.md` or a dedicated lessons learned repository.


## References
  1. [SOCFortress - Phishing IRP](https://github.com/socfortress/Playbooks/blob/main/IRP-Phishing/README.md)
