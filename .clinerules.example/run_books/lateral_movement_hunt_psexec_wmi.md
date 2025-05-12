# Lateral Movement Detection Hunt (Example: PsExec/WMI)

## Objective

Proactively hunt for signs of lateral movement using common administrative tools like PsExec or WMI abuse, which attackers often leverage.

## Scope

This runbook provides a template for hunting specific lateral movement TTPs, focusing on PsExec and WMI examples using SIEM queries.

## Inputs

*   `${TIME_FRAME_HOURS}`: Lookback period in hours for SIEM searches (default: 72).
*   *(Optional) `${TARGET_SCOPE_QUERY}`: A UDM query fragment to narrow the scope (e.g., `principal.hostname = "server1"` or `target.hostname = "domain_controller"`).*
*   *(Optional) `${HUNT_HYPOTHESIS}`: Brief description of the reason for the hunt (e.g., "Hunting for PsExec usage originating from non-admin workstations").*

## Tools

*   `secops-mcp`: `get_threat_intel` (for technique understanding), `search_security_events` (core hunting tool), `lookup_entity` (for enriching findings).
*   `secops-soar`: `post_case_comment` (for documenting hunt/findings), `list_cases` (optional, check related cases).
*   `gti-mcp`: (Used for enriching findings if IOCs are discovered).
*   *(Optional: Identity Provider tools like `okta-mcp.lookup_okta_user`)*
*   **Common Steps:** `common_steps/find_relevant_soar_case.md`

## Workflow Steps & Diagram

1.  **Receive Input & Define Scope:** Obtain `${TIME_FRAME_HOURS}`, optionally `${TARGET_SCOPE_QUERY}` and `${HUNT_HYPOTHESIS}`.
2.  **Research Techniques (SIEM/External):**
    *   Use `secops-mcp.get_threat_intel` for TTPs like T1570 (Lateral Tool Transfer - PsExec often copied), T1021.002 (Remote Services: SMB/Windows Admin Shares - PsExec uses this), T1047 (Windows Management Instrumentation - WMI abuse).
    *   *(Manual Step: Review MITRE ATT&CK website for detailed procedures and detection guidance for these techniques).*
3.  **Develop SIEM Hunt Queries:**
    *   Based on research, formulate specific `secops-mcp.search_security_events` UDM queries targeting indicators. Examples:
        *   **PsExec Service Installation:** `metadata.product_event_type = "ServiceInstalled" AND target.process.file.full_path CONTAINS "PSEXESVC.exe"` (Requires appropriate Windows Event Log source - System Log Event ID 7045).
        *   **PsExec Execution (Indirect):** Look for `services.exe` spawning unusual processes, especially on remote machines shortly after potential SMB connection. `metadata.event_type = "PROCESS_LAUNCH" AND principal.process.file.full_path = "C:\Windows\System32\services.exe" AND target.process.file.full_path NOT IN ("standard_service_process1.exe", "standard_service_process2.exe")` (Needs significant tuning based on environment).
        *   **WMI Process Creation:** `metadata.event_type = "PROCESS_LAUNCH" AND principal.process.file.full_path = "C:\Windows\System32\wbem\WmiPrvSE.exe"` (Look for `WmiPrvSE.exe` spawning suspicious child processes like `cmd.exe`, `powershell.exe`).
        *   **WMI Command-Line Execution:** `metadata.event_type = "PROCESS_LAUNCH" AND principal.process.file.full_path = "C:\Windows\System32\cmd.exe" AND principal.process.command_line CONTAINS "wmic"` AND `principal.process.command_line CONTAINS "/node:"` AND `principal.process.command_line CONTAINS "process call create"`
        *   **WMI Event Subscription (Persistence T1546.003):** Search for events related to `__EventFilter`, `__EventConsumer`, `__FilterToConsumerBinding` creation/modification (Requires specific WMI event logging or EDR visibility). Example: `metadata.event_type = "WMI_ACTIVITY" AND description CONTAINS "__EventFilter"`
        *   **PowerShell WMI Methods:** Search for PowerShell scripts (`.ps1`) or command lines using `Invoke-WmiMethod`, `Get-WmiObject`, or `Invoke-CimMethod` for remote interaction. Example: `metadata.event_type = "PROCESS_LAUNCH" AND target.process.file.full_path CONTAINS "powershell.exe" AND target.process.command_line CONTAINS "Invoke-WmiMethod"`
    *   Combine technique-specific queries with `${TARGET_SCOPE_QUERY}` if provided.
4.  **Execute SIEM Searches:**
    *   Run the developed queries using `secops-mcp.search_security_events` with `hours_back=${TIME_FRAME_HOURS}`.
5.  **Network Correlation (Optional but Recommended):**
    *   If suspicious process activity is found on a target host, search for corresponding network connections (especially SMB port 445) originating from potential source hosts around the same time.
    *   Example Query: `metadata.event_type = "NETWORK_CONNECTION" AND target.port = 445 AND target.ip = "TARGET_IP" AND principal.ip = "SOURCE_IP"` (Adjust IPs and timeframe based on findings).
6.  **Analyze Results:**
    *   Review results for anomalous patterns: PsExec/WMI usage originating from unexpected sources (e.g., user workstations instead of admin servers), execution targeting a large number of hosts, execution of suspicious commands via WMI, correlation between network connections and remote process execution.
7.  **Enrich Findings:**
    *   If suspicious activity is found:
            *   Use `secops-mcp.lookup_entity` for involved source/destination hosts, users. Let these be `SUSPICIOUS_ENTITIES`.
            *   *(Optional)* If an Identity Provider tool is available (e.g., `okta-mcp.lookup_okta_user`), gather context on involved user accounts.
            *   Use `gti-mcp` tools to enrich any associated IPs, domains, or hashes if applicable. Let combined enrichment be `ENRICHMENT_RESULTS`.
8.  **Check Related SOAR Cases:**
    *   If `SUSPICIOUS_ENTITIES` were identified:
        *   Execute `common_steps/find_relevant_soar_case.md` with `SEARCH_TERMS=SUSPICIOUS_ENTITIES` and `CASE_STATUS_FILTER="Opened"`.
        *   Obtain `${RELATED_SOAR_CASES}` (list of potentially relevant open case summaries/IDs).
9.  **Document Hunt & Findings:**
    *   Use `secops-soar.post_case_comment` in a dedicated hunting case or relevant existing case.
    *   Document: Hunt Hypothesis/Objective, Techniques Hunted, Scope, Timeframe, Queries Used, Summary of Findings (**explicitly noting queries with negative results**), Details of suspicious activity, Enrichment results (`ENRICHMENT_RESULTS`), Related SOAR Cases (`${RELATED_SOAR_CASES}`).
    *   **Suggest Follow-on Actions:** Based on findings, suggest next steps like triggering `case_event_timeline_and_process_analysis.md` for suspicious processes or `compromised_user_account_response.md` for involved users.
10. **Escalate or Conclude:**
    *   If confirmed lateral movement or tool abuse is found, escalate by creating a new incident case or linking findings to an existing one.
    *   If no significant findings, conclude the hunt and document it thoroughly.
11. **Completion:** Conclude the runbook execution.

```{mermaid}
sequenceDiagram
    participant Analyst
    participant Cline as Cline (MCP Client)
    participant SecOpsMCP as secops-mcp
    participant SOAR as secops-soar
    participant MITRE as MITRE ATT&CK (External)
    participant IDP as Identity Provider (Optional)
    participant GTI as gti-mcp
    participant FindCase as common_steps/find_relevant_soar_case.md

    Analyst->>Cline: Start Lateral Movement Hunt (PsExec/WMI)\nInput: TIME_FRAME_HOURS, TARGET_SCOPE_QUERY (opt), HUNT_HYPOTHESIS (opt)

    %% Step 2: Research Techniques
    Cline->>SecOpsMCP: get_threat_intel(query="MITRE T1021.002")
    SecOpsMCP-->>Cline: Technique Context
    Cline->>SecOpsMCP: get_threat_intel(query="MITRE T1047")
    SecOpsMCP-->>Cline: Technique Context
    Cline->>MITRE: (Manual) Review ATT&CK Website
    MITRE-->>Cline: Detailed Procedures/Detections

    %% Step 3: Develop SIEM Queries
    Note over Cline: Formulate UDM queries for PsExec/WMI indicators (incl. new WMI examples)

    %% Step 4: Execute SIEM Searches
    loop For each developed Query Qi
        Cline->>SecOpsMCP: search_security_events(text=Qi, hours_back=TIME_FRAME_HOURS)
        SecOpsMCP-->>Cline: Search Results for Qi
    end

    %% Step 5: Network Correlation (Optional)
    opt Suspicious Activity Found
        Note over Cline: Construct Network Correlation Query Qn
        Cline->>SecOpsMCP: search_security_events(text=Qn, hours_back=...)
        SecOpsMCP-->>Cline: Network Correlation Results
    end

    %% Step 6: Analyze Results
    Note over Cline: Analyze results for anomalous PsExec/WMI usage & correlations

    %% Step 7: Enrich Findings
    opt Suspicious Activity Found
        Note over Cline: Identify SUSPICIOUS_ENTITIES (H1, U1...)
        loop For each Suspicious Entity Ei
            Cline->>SecOpsMCP: lookup_entity(entity_value=Ei)
            SecOpsMCP-->>Cline: SIEM Summary for Ei
            opt IDP Tool Available and Ei is User
                Cline->>IDP: lookup_user(user=Ei)
                IDP-->>Cline: User IDP Context
            end
            %% Potentially enrich related IOCs if found
            opt IOCs Found (I1, I2...)
                 loop For each IOC Ii
                     Cline->>GTI: get_..._report(ioc=Ii)
                     GTI-->>Cline: GTI Report for Ii
                 end
            end
        end
        Note over Cline: Store combined enrichment (ENRICHMENT_RESULTS)
    end

    %% Step 8: Check Related SOAR Cases
    opt Suspicious Activity Found
        Cline->>FindCase: Execute(Input: SEARCH_TERMS=SUSPICIOUS_ENTITIES, CASE_STATUS_FILTER="Opened")
        FindCase-->>Cline: Results: RELATED_SOAR_CASES
    end

    %% Step 9: Document Hunt
    Note over Cline: Prepare hunt summary comment (incl. negative results, related cases & suggested follow-ons)
    Cline->>SOAR: post_case_comment(case_id=[Hunt Case/Relevant Case], comment="Lateral Movement Hunt (PsExec/WMI) Summary: Scope [...], Queries [...], Findings [...], Enrichment [...], Related Cases: [...], Follow-on: [...]")
    SOAR-->>Cline: Comment Confirmation

    %% Step 10 & 11: Escalate or Conclude
    alt Confirmed Malicious Activity Found
        Note over Cline: Escalate findings (Create new case or link to existing)
        Cline->>Analyst: attempt_completion(result="Lateral Movement Hunt complete. Findings escalated.")
    else No Significant Findings
        Cline->>Analyst: attempt_completion(result="Lateral Movement Hunt complete. No significant findings. Hunt documented.")
    end
