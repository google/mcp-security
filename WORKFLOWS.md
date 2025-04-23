

## Close duplicate/similar Cases Workflow

```{mermaid}
  sequenceDiagram
      participant User
      participant Cline as Cline (MCP Client)
      participant list_cases as list_cases (secops-soar)
      participant list_alerts_by_case as list_alerts_by_case (secops-soar)
      participant list_alert_group_identifiers_by_case as list_alert_group_identifiers_by_case (secops-soar)
      participant siemplify_get_similar_cases as siemplify_get_similar_cases (secops-soar)
      participant post_case_comment as post_case_comment (secops-soar)
      participant siemplify_close_case as siemplify_close_case (secops-soar)
      participant attempt_completion as attempt_completion (Cline)
      participant ask_followup_question as ask_followup_question (Cline)

      User->>Cline: Request case analysis and closure
      Cline->>list_cases: list_cases()
      list_cases-->>Cline: List of recent cases (IDs: C1, C2, ... CN)
      loop For each Case Ci
          Cline->>list_alerts_by_case: list_alerts_by_case(case_id=Ci)
          list_alerts_by_case-->>Cline: Alerts for Ci
          Cline->>list_alert_group_identifiers_by_case: list_alert_group_identifiers_by_case(case_id=Ci)
          list_alert_group_identifiers_by_case-->>Cline: Alert Group IDs for Ci
      end
      loop For each Case Cj
          Cline->>siemplify_get_similar_cases: siemplify_get_similar_cases(case_id=Cj, criteria=RuleGenerator, days_back=7, alert_group_ids=...)
          siemplify_get_similar_cases-->>Cline: List of similar case IDs for Cj
      end
      Cline->>User: Present potential duplicate cases (e.g., Ck, Cl are duplicates of Cm)
      Cline->>ask_followup_question: ask_followup_question(Confirm cases to close & provide reason/root_cause)
      User->>Cline: Confirmation (e.g., Close Ck, Cl. Reason: Duplicate)
      loop For each confirmed Case C_dup (Ck, Cl)
          Cline->>post_case_comment: post_case_comment(case_id=C_dup, comment="Closing as duplicate of Cm")
          post_case_comment-->>Cline: Comment confirmation
          Cline->>siemplify_close_case: siemplify_close_case(case_id=C_dup, reason="Duplicate", root_cause="Consolidated Investigation")
          siemplify_close_case-->>Cline: Closure confirmation
      end
      Cline->>attempt_completion: attempt_completion(Summary of closed cases)
      Note right of Cline: Slack notification not possible due to tool limitations.
```


### Create an Investigation Report

Create an Investigation Report of your investigation actions through multiple products	Perform an investigation (can be any set of actions) across SecOps, GTI, SCC, Okta, and Crowdstrike. Then, summarize all the actions, put it into a document, and add it as an attachment to the Case in SecOps. Redact/defang sensitive data from the document and (optionally and with confirmation) upload it to Google Drive or GCS Bucket.

Uses the MCP Tools:

 * List Cases
 * Get Alerts in a Case
 * Entity Lookup
 * GTI Lookup
 * OKTA User Lookup
 * SCC Findings Search
 * Attach Document to Case
 * Upload file to Google Drive"

```{mermaid}
sequenceDiagram
    participant User
    participant Cline as Cline (MCP Client)
    participant SOAR as secops-soar
    participant SIEM as secops-mcp
    participant GTI as gti-mcp
    participant SCC as scc-mcp
    participant Okta as okta-mcp
    participant CS as crowdstrike-mcp
    participant Drive as google-drive-mcp
    participant GCS as gcs-mcp

    User->>Cline: Request Investigation Report for Case X
    Cline->>SOAR: list_alerts_by_case(case_id=X)
    SOAR-->>Cline: Alerts for Case X (containing entities E1, E2...)
    loop For each relevant Entity Ei
        Cline->>SIEM: lookup_entity(entity_value=Ei)
        SIEM-->>Cline: SIEM context for Ei
        Cline->>GTI: get_file_report/get_domain_report(entity=Ei)
        GTI-->>Cline: GTI context for Ei
        Cline->>SCC: search_scc_findings(query=Ei)
        SCC-->>Cline: SCC findings for Ei
        Cline->>Okta: lookup_okta_user(user=Ei)
        Okta-->>Cline: Okta user details for Ei
        Cline->>CS: get_host_details(host=Ei)
        CS-->>Cline: CrowdStrike host details for Ei
    end
    Note over Cline: Synthesize findings, redact/defang sensitive data
    Cline->>Cline: Create report content (e.g., report_content)
    Cline->>Cline: write_to_file(path="investigation_report_case_X.md", content=report_content)
    Note over Cline: Report created locally
    Cline->>SOAR: siemplify_add_attachment_to_case(case_id=X, file_path="investigation_report_case_X.md")
    SOAR-->>Cline: Attachment confirmation
    Cline->>User: ask_followup_question(question="Upload redacted report to Drive/GCS?", options=["Yes, Drive", "Yes, GCS", "No"])
    User->>Cline: Response (e.g., "Yes, Drive")
    alt Upload Confirmed
        alt Upload to Drive
            Cline->>Drive: upload_to_drive(file_path="investigation_report_case_X.md", destination="Reports Folder")
            Drive-->>Cline: Drive upload confirmation
        else Upload to GCS
            Cline->>GCS: upload_to_gcs(file_path="investigation_report_case_X.md", bucket="security-reports", object_name="case_X_report.md")
            GCS-->>Cline: GCS upload confirmation
        end
    end
    Cline->>Cline: attempt_completion(result="Investigation report created, attached to Case X, and optionally uploaded.")

```



### Prioritize and Investigate a Case

From a list of cases, identify cases of the highest severity and potential impact based on underlying alerts and detections. Get rule logic to validate the detections in the cases. After identifying the highest N priority cases -> Explain the entirety of the case to the analyst in the context of the underlying rule logic (explain the rule logic and how it applies to this case). Get entity context to determine if there are additional alerts, detections, or events that may not have been included in the case but are potentially applicable.

Use the tools:


 * List Cases and include the environment
 * Get Alerts in a Case
 * Get Detections in a Case
 * Get Events from Alerts and/or Detections in a Case
 * Get rule logic
 * Evaluate Alert/Event against rule logic
 * UDM search for activity from principal or target

```{mermaid}
sequenceDiagram
    participant User
    participant Cline as Cline (MCP Client)
    participant SOAR as secops-soar
    participant SIEM as secops-mcp

    User->>Cline: Prioritize and investigate cases
    Cline->>SOAR: list_cases()
    SOAR-->>Cline: List of cases (C1, C2... Priority P1, P2...)
    Note over Cline: Analyze cases, identify high priority (e.g., Case X based on initial priority/alerts)
    Cline->>SOAR: get_case_full_details(case_id=X)
    SOAR-->>Cline: Full details for Case X (alerts, comments, etc.)
    Note over Cline: Confirm priority based on full details. May use change_case_priority if needed.
    Cline->>SOAR: list_alerts_by_case(case_id=X)
    SOAR-->>Cline: Alerts for Case X (A1, A2...)
    loop For each Alert Ai in Case X
        Cline->>SOAR: list_events_by_alert(case_id=X, alert_id=Ai)
        SOAR-->>Cline: Events for Alert Ai (containing rule_id, entities E1, E2...)
        Note over Cline: Extract rule_id from event/alert data
        Cline->>SIEM: list_security_rules(rule_id=rule_id)
        SIEM-->>Cline: Rule logic/definition for rule_id
        Cline->>SIEM: list_rule_detections(rule_id=rule_id)
        SIEM-->>Cline: Detections associated with rule_id
        Note over Cline: Analyze events/detections against rule logic
        loop For each relevant Entity Ej in Events
            Cline->>SIEM: lookup_entity(entity_value=Ej)
            SIEM-->>Cline: Entity context for Ej
            Cline->>SIEM: search_security_events(text="Events involving entity Ej", hours_back=...)
            SIEM-->>Cline: Broader UDM events for Ej
        end
    end
    Note over Cline: Synthesize findings, correlate rule logic with events/entities
    Cline->>SOAR: post_case_comment(case_id=X, comment="Investigation Summary: Case X involves rule [Rule Name] triggered by events [...]. Entities [...] investigated. Findings: [...]")
    SOAR-->>Cline: Comment confirmation
    Cline->>Cline: attempt_completion(result="Completed investigation for Case X. Summary posted as comment.")

```

### Investigate a Case + external tools

Using SecOps, GTI, and Okta. Start with a Case (anomalous login Alerts). Find the entities involved and look up any related indicators. Find any users involved and look up Okta information to determine any suspicious characteristics. If confident in disposition, disable that User. Finally, provide a report about any identified activity for security analyst consumption.

Uses tools:

 * List Cases
 * Get Alerts in a Case
 * Entity Lookup
 * GTI Lookup
 * Event Search
 * OKTA user information
 * OKTA action"


```{mermaid}
sequenceDiagram
    participant User
    participant Cline as Cline (MCP Client)
    participant SOAR as secops-soar
    participant SIEM as secops-mcp
    participant GTI as gti-mcp
    participant Okta as okta-mcp

    User->>Cline: Investigate Case Y (Anomalous Login)
    Cline->>SOAR: list_alerts_by_case(case_id=Y)
    SOAR-->>Cline: Alerts for Case Y (Entities: User U, IP I, Host H...)
    loop For each relevant Entity Ei (U, I, H...)
        Cline->>SIEM: lookup_entity(entity_value=Ei)
        SIEM-->>Cline: SIEM context for Ei
        Cline->>GTI: get_file_report/get_domain_report/get_ip_address_report(entity=Ei)
        GTI-->>Cline: GTI context for Ei
        Cline->>SIEM: search_security_events(text="Events involving entity Ei", hours_back=...)
        SIEM-->>Cline: Related UDM events for Ei
    end
    Note over Cline: Identify primary user entity (User U)
    Cline->>Okta: lookup_okta_user(user=U)
    Okta-->>Cline: Okta user details for User U
    Note over Cline: Analyze Okta details for suspicious activity/characteristics
    Cline->>User: ask_followup_question(question="Okta user U shows suspicious activity. Disable user?", options=["Yes", "No"])
    User->>Cline: Response (e.g., "Yes")
    alt Disable User Confirmed
        Cline->>Okta: disable_okta_user(user=U)
        Okta-->>Cline: Disable confirmation
    end
    Note over Cline: Synthesize all findings into a report summary
    Cline->>SOAR: post_case_comment(case_id=Y, comment="Investigation Summary: Anomalous login for User U from IP I. GTI/SIEM checks performed. Okta details reviewed. User disabled due to suspicious activity. Findings: [...]")
    SOAR-->>Cline: Comment confirmation
    Cline->>Cline: attempt_completion(result="Completed investigation for Case Y. User U potentially disabled. Summary posted as comment.")

```


### Compare GTI Collection to IoCs, Events in SecOps

From a GTI Collection (could be a Private Collection as well), search the past 3 days for any UDM events containing:
 1) Indicators of Compromise
 2) IOC++ (Modeled behvaioral data) (Would need to interpret relevant UDM fields)
 3) Get Chronicle SIEM IoC Matches (`get_ioc_matches`)
 4) Produce report on findings
 5) Add report to SOAR Case

Analyze results and compare against GTI Collection context (report or campaign). (Optional) Notable indicators are added to SQLite Table. Provide analyst report with prescribed follow on response actions.

Uses tools:

 * `gti-mcp.get_collection_report`
 * `secops-mcp.get_ioc_matches`
 * `secops-mcp.search_security_events`
 * `secops-mcp.get_security_alerts`
 * `gti-mcp.*` (various lookups like `get_file_report`, etc.)
 * (Optional) Add to SQLite Table
 * `secops-soar.post_case_comment`

```{mermaid}
sequenceDiagram
    participant User
    participant Cline as Cline (MCP Client)
    participant GTI as gti-mcp
    participant SIEM as secops-mcp
    participant SOAR as secops-soar

    User->>Cline: Sweep environment based on GTI Collection ID 'GTI-XYZ'
    Cline->>GTI: get_collection_report(id='GTI-XYZ')
    GTI-->>Cline: Collection details (Report/Campaign context, IOCs I1, I2...)
    Note over Cline: Extract IOCs (I1, I2...) and behavioral patterns (TTPs)
    Cline->>SIEM: get_ioc_matches(hours_back=...)
    SIEM-->>Cline: List of recent IOC matches in environment
    loop For each IOC Ii from Collection
        Cline->>SIEM: search_security_events(text="Events containing IOC Ii", hours_back=...)
        SIEM-->>Cline: UDM events related to IOC Ii
        Cline->>SIEM: get_security_alerts(query="alert contains Ii", hours_back=...)
        SIEM-->>Cline: Alerts related to IOC Ii
    end
    Note over Cline: Interpret behavioral patterns (TTPs) into UDM search queries
    loop For each Behavioral Pattern Bp
        Cline->>SIEM: search_security_events(text="Events matching pattern Bp", hours_back=...)
        SIEM-->>Cline: UDM events potentially matching pattern Bp
    end
    Note over Cline: Analyze results (IOC matches, events, alerts) against GTI context
    Note over Cline: Identify notable indicators (N1, N2...) found in environment
    loop For each Notable Indicator Ni
        Note over Cline: Add Ni to Chronicle Data Table (Conceptual Step - No direct tool)
        Cline->>SIEM: (Conceptual) Add Ni to Data Table 'Notable_Indicators'
    end
    Note over Cline: Synthesize report: Findings, GTI context correlation, Recommended Actions
    Cline->>SOAR: post_case_comment(case_id=[Relevant Case or New Case], comment="Sweep Report for GTI-XYZ: Found indicators [N1, N2...]. Events [...] observed. Recommended actions: [...]")
    SOAR-->>Cline: Comment confirmation
    Cline->>Cline: attempt_completion(result="Environment sweep based on GTI Collection 'GTI-XYZ' complete. Report posted.")

```

# Investigate Google Threat Intelligence Collection ID (Enhanced)

Objective: Investigate Google Threat Intelligence Collection ID provided by the user `${COLLECTION_ID}`. Enrich findings with detailed entity reports and correlate with the local environment (SIEM/SOAR). Create a timestamped markdown report summarizing findings, correlations, and recommended actions.

Instructions:

1.  **Initial Collection Context:**
    *   Use the `get_collection_report` tool from the `Google Threat Intelligence MCP server` (gti-mcp).
    *   Provide the argument: `id`: `${COLLECTION_ID}`.
    *   Record the collection details, especially the `collection_type`.

2.  **Define Relationships to Investigate:**
    *   Based on the `collection_type` (from Step 1), determine a prioritized list of relevant relationships. (Default: `["associations", "attack_techniques", "domains", "files", "ip_addresses", "urls", "threat_actors", "malware_families", "software_toolkits", "campaigns", "vulnerabilities", "reports", "suspected_threat_actors"]`, but can be narrowed). Let's call this `RELATIONSHIP_LIST`.

3.  **Iterative GTI Relationship Investigation:**
    *   Initialize an empty data structure (e.g., `gti_findings`) to store results.
    *   Loop through each `relationship_name` in `RELATIONSHIP_LIST`.
    *   Use the `get_entities_related_to_a_collection` tool (gti-mcp).
    *   Arguments: `id`: `${COLLECTION_ID}`, `relationship_name`: current relationship name.
    *   Store the results in `gti_findings` under the corresponding `relationship_name`.

4.  **Detailed GTI Entity Enrichment:**
    *   Initialize an empty data structure (e.g., `enriched_entities`) to store detailed reports.
    *   Iterate through key entity types found in `gti_findings` (e.g., domains, files, ip_addresses).
    *   For each entity found:
        *   If it's a domain, use `get_domain_report` (gti-mcp) with the domain name. Store the result.
        *   If it's a file (hash), use `get_file_report` (gti-mcp) with the hash. Store the result.
        *   If it's an IP address, use `get_ip_address_report` (gti-mcp) with the IP. Store the result.
        *   *(Add other relevant enrichment tools if needed, e.g., `get_url_report`)*.

5.  **Local Environment Correlation (SIEM/SOAR):**
    *   Initialize an empty data structure (e.g., `local_findings`) to store correlation results.
    *   Iterate through key IOCs found (domains, files, IPs from `gti_findings`).
    *   For each IOC:
        *   Use `lookup_entity` (secops-mcp) with `entity_value` = IOC. Store summary.
        *   Use `search_security_events` (secops-mcp) with `text` query related to the IOC (e.g., "Events involving IP 1.2.3.4"). Store key event findings.
    *   *(Optional: Check if related threat actors/campaigns match existing SOAR cases using `list_cases` (secops-soar) with appropriate filters)*.

6.  **Data Synthesis and Formatting:**
    *   Initialize an empty markdown string for the report content.
    *   Add a main title and summary section mentioning the Collection ID.
    *   **Add "Key Findings & Recommendations" section:** Summarize critical entities, highlight correlations between GTI and local findings, and list actionable next steps.
    *   Iterate through `gti_findings` and `enriched_entities`:
        *   Add sections for each relationship type investigated.
        *   List entities found. For enriched entities, include key details from their detailed reports (Step 4). Note relationships with no findings.
    *   Add a "Local Environment Correlation" section:
        *   Summarize results from `lookup_entity` and `search_security_events` for each checked IOC. Highlight any matches or significant activity.

7.  **Report Creation:**
    *   Generate a timestamp string (`yyyymmdd_hhmm`).
    *   Construct filename: `./reports/enhanced_report_${COLLECTION_ID}_${timestamp}.md`.
    *   Use the `write_to_file` tool.
    *   Arguments: `path`: constructed filename, `content`: complete formatted markdown string.

```{mermaid}
sequenceDiagram
    participant User
    participant Cline as Cline (MCP Client)
    participant GTI as gti-mcp
    participant SIEM as secops-mcp
    participant SOAR as secops-soar

    User->>Cline: Investigate GTI Collection ID `${COLLECTION_ID}` (Enhanced)

    %% Step 1: Initial Collection Context
    Cline->>GTI: get_collection_report(id=`${COLLECTION_ID}`)
    GTI-->>Cline: Collection Details (Type: T)

    %% Step 2 & 3: Define & Investigate Relationships
    Note over Cline: Determine RELATIONSHIP_LIST based on Type T
    loop For each relationship_name in RELATIONSHIP_LIST
        Cline->>GTI: get_entities_related_to_a_collection(id=`${COLLECTION_ID}`, relationship_name=...)
        GTI-->>Cline: Related Entities (E1, E2...) for relationship
        Note over Cline: Store entities in gti_findings
    end

    %% Step 4: Detailed GTI Entity Enrichment
    Note over Cline: Initialize enriched_entities
    loop For each key Entity Ei in gti_findings (Files, Domains, IPs)
        alt Entity is File (Hash H)
            Cline->>GTI: get_file_report(hash=H)
            GTI-->>Cline: File Report for H
            Note over Cline: Store in enriched_entities
        else Entity is Domain (D)
            Cline->>GTI: get_domain_report(domain=D)
            GTI-->>Cline: Domain Report for D
            Note over Cline: Store in enriched_entities
        else Entity is IP Address (IP)
            Cline->>GTI: get_ip_address_report(ip_address=IP)
            GTI-->>Cline: IP Report for IP
            Note over Cline: Store in enriched_entities
        end
    end

    %% Step 5: Local Environment Correlation
    Note over Cline: Initialize local_findings
    loop For each key IOC Ii from gti_findings (Files, Domains, IPs)
        Cline->>SIEM: lookup_entity(entity_value=Ii)
        SIEM-->>Cline: SIEM Entity Summary for Ii
        Note over Cline: Store in local_findings
        Cline->>SIEM: search_security_events(text="Events involving Ii")
        SIEM-->>Cline: Relevant SIEM Events for Ii
        Note over Cline: Store in local_findings
    end
    %% Optional SOAR Check (Conceptual)
    %% Cline->>SOAR: list_cases(filter="Related to Campaign/Actor from GTI")
    %% SOAR-->>Cline: Potentially related SOAR cases

    %% Step 6 & 7: Synthesize Report and Write File
    Note over Cline: Synthesize report content from gti_findings, enriched_entities, local_findings
    Note over Cline: Include Key Findings & Recommendations
    Cline->>Cline: write_to_file(path="./reports/enhanced_report_${COLLECTION_ID}_${timestamp}.md", content=...)
    Note over Cline: Report file created

    Cline->>User: attempt_completion(result="Enhanced investigation complete. Report generated.")

```



# Group Cases Workflow

From the last 5 cases, examine the underlying entities in the alerts and events and group the cases logically. Then, extract details from each case in each cluster to build a high fidelity understanding of each cases' disposition and involved entities. Make sure you have an in depth understanding of each case before moving on to the next step.

Then determine the priority of each case "grouping". Then for each grouping analyze and interpret the alerts to understand why each case might be relevant. Then assess the impact of each case grouping and prioritize the cases with the highest potentialy impact. Then for each case grouping examine the underlying entities and enrich any observables with GTI. Finally, search for any related security events that may be relevant to a case based on their entities (hostnames) and include those as part of your case analysis. Finally, create a comprehensive analysis report in markdown in which you present the prioritized case list, your justification, and your analysis of each case or case cluster.

Do not treat internal domains as indicators (such as those extracted from email addresses, or usernames)


# Graphviz Dotfile

```{graphviz}
digraph CaseAnalysisFlow {
    rankdir=TB;
    // Default node style (applied if not overridden)
    node [shape=box, style=rounded, fontname="Helvetica"];
    // --- Legend / Key ---
    subgraph cluster_legend {
        label = "Key / Legend";
        style = filled;
        fillcolor = whitesmoke; // Light background for the legend box
        fontsize = 10;
        fontcolor = darkslategray;
        node [shape=box, fontname="Helvetica", fontsize=9]; // Default style within legend
        key_step [label="Step / Action", shape=box, style=rounded];
        key_plan [label="Planning Step", shape=box, style="rounded,filled", fillcolor=lightyellow];
        key_tool [label="Tool Execution", shape=ellipse, style=filled, fillcolor=lightblue];
        key_result [label="Result / Summary", shape=note, align=left];
        key_report [label="Final Report", shape=note, style=filled, fillcolor=lightgrey];
        key_failed [label="Tool Not Found", shape=ellipse, style=filled, fillcolor=lightcoral]; // Added for completeness
        key_cluster [label="Phase / Grouping\n(Subgraph Border)", shape=box, style=dashed, color=gray];
        // Arrange legend items vertically using invisible edges
        key_step -> key_plan -> key_tool -> key_result -> key_report -> key_failed -> key_cluster [style=invis];
    }
    // --- End Legend ---
    // Start
    Start [label="Start Task:\nAnalyze Last 5 Cases"];
    // Planning Phase
    PlanMode1 [label="PLAN MODE:\nOutline 7-step analysis plan", shape=box, style="rounded,filled", fillcolor=lightyellow];
    PlanResponse1 [label="plan_mode_respond:\nPresent plan, request ACT MODE", shape=ellipse, style=filled, fillcolor=lightyellow]; // Style similar to plan
    PlanResult1 [label="User switches to ACT MODE", shape=note];
    Start -> PlanMode1;
    PlanMode1 -> PlanResponse1;
    PlanResponse1 -> PlanResult1;
    // Step 1: List Cases
    ListCases [label="Step 1: List Recent Cases"]; // Uses default style
    ListCasesTool [label="secops-soar.list_cases", shape=ellipse, style=filled, fillcolor=lightblue];
    ListCasesResult [label="Result:\nTop 5 Case IDs:\n553, 552, 551, 550, 549", shape=note];
    PlanResult1 -> ListCases;
    ListCases -> ListCasesTool;
    ListCasesTool -> ListCasesResult;
    // Step 2: Examine Cases (Parallel)
    Step2_Label [label="Step 2: Examine Cases (Parallel)", shape=box, style=rounded]; // Explicitly default style
    ListCasesResult -> Step2_Label;
    // Case 553 Examination
    subgraph cluster_case_553 {
        label = "Examine Case 553"; style=dashed; color=gray;
        Examine553_DetailsTool [label="Get Details (553)\nsecops-soar.get_case_full_details", shape=ellipse, style=filled, fillcolor=lightblue];
        Examine553_EntitiesTool [label="Get Entities (553)\nsecops-soar.get_entities_by_alert_group_identifiers", shape=ellipse, style=filled, fillcolor=lightblue];
        Examine553_EventsTool [label="List Events (553)\nsecops-soar.list_events_by_alert", shape=ellipse, style=filled, fillcolor=lightblue];
        Examine553_Summary [label="Summary (553):\nImpossible Travel", shape=note];
        Examine553_DetailsTool -> Examine553_EntitiesTool -> Examine553_EventsTool -> Examine553_Summary;
    }
    // Case 552 Examination
    subgraph cluster_case_552 {
        label = "Examine Case 552"; style=dashed; color=gray;
        Examine552_DetailsTool [label="Get Details (552)\nsecops-soar.get_case_full_details", shape=ellipse, style=filled, fillcolor=lightblue];
        Examine552_EntitiesTool [label="Get Entities (552)\nsecops-soar.get_entities_by_alert_group_identifiers", shape=ellipse, style=filled, fillcolor=lightblue];
        Examine552_Events1Tool [label="List Events (Alert 793)\nsecops-soar.list_events_by_alert", shape=ellipse, style=filled, fillcolor=lightblue];
        Examine552_Events2Tool [label="List Events (Alert 792)\nsecops-soar.list_events_by_alert", shape=ellipse, style=filled, fillcolor=lightblue];
        Examine552_Summary [label="Summary (552):\nChrome DLP", shape=note];
        Examine552_DetailsTool -> Examine552_EntitiesTool -> Examine552_Events1Tool -> Examine552_Events2Tool -> Examine552_Summary;
     }
     // Case 551 Examination
     subgraph cluster_case_551 {
        label = "Examine Case 551"; style=dashed; color=gray;
        Examine551_DetailsTool [label="Get Details (551)\nsecops-soar.get_case_full_details", shape=ellipse, style=filled, fillcolor=lightblue];
        Examine551_EntitiesTool [label="Get Entities (551)\nsecops-soar.get_entities_by_alert_group_identifiers", shape=ellipse, style=filled, fillcolor=lightblue];
        Examine551_Events1Tool [label="List Events (Alert 791)\nsecops-soar.list_events_by_alert", shape=ellipse, style=filled, fillcolor=lightblue];
        Examine551_Events2Tool [label="List Events (Alert 790)\nsecops-soar.list_events_by_alert", shape=ellipse, style=filled, fillcolor=lightblue];
        Examine551_Summary [label="Summary (551):\nSideload/Malware DL", shape=note];
        Examine551_DetailsTool -> Examine551_EntitiesTool -> Examine551_Events1Tool -> Examine551_Events2Tool -> Examine551_Summary;
     }
     // Case 550 Examination
     subgraph cluster_case_550 {
        label = "Examine Case 550"; style=dashed; color=gray;
        Examine550_DetailsTool [label="Get Details (550)\nsecops-soar.get_case_full_details", shape=ellipse, style=filled, fillcolor=lightblue];
        Examine550_EntitiesTool [label="Get Entities (550)\nsecops-soar.get_entities_by_alert_group_identifiers", shape=ellipse, style=filled, fillcolor=lightblue];
        Examine550_EventsTool [label="List Events (550)\nsecops-soar.list_events_by_alert", shape=ellipse, style=filled, fillcolor=lightblue];
        Examine550_Summary [label="Summary (550):\nJenkins CVE", shape=note];
        Examine550_DetailsTool -> Examine550_EntitiesTool -> Examine550_EventsTool -> Examine550_Summary;
     }
     // Case 549 Examination
     subgraph cluster_case_549 {
        label = "Examine Case 549"; style=dashed; color=gray;
        Examine549_DetailsTool [label="Get Details (549)\nsecops-soar.get_case_full_details", shape=ellipse, style=filled, fillcolor=lightblue];
        Examine549_EntitiesTool [label="Get Entities (549)\nsecops-soar.get_entities_by_alert_group_identifiers", shape=ellipse, style=filled, fillcolor=lightblue];
        Examine549_EventsTool [label="List Events (549)\nsecops-soar.list_events_by_alert", shape=ellipse, style=filled, fillcolor=lightblue];
        Examine549_Summary [label="Summary (549):\nPhishing Sim", shape=note];
        Examine549_DetailsTool -> Examine549_EntitiesTool -> Examine549_EventsTool -> Examine549_Summary;
     }
    // Edges for Parallel Step 2 - Fork
    Step2_Label -> Examine553_DetailsTool;
    Step2_Label -> Examine552_DetailsTool;
    Step2_Label -> Examine551_DetailsTool;
    Step2_Label -> Examine550_DetailsTool;
    Step2_Label -> Examine549_DetailsTool;
    // Step 3 & 4: Grouping and Prioritization
    GroupPrioritize [label="Steps 3 & 4:\nAnalyze Case Summaries,\nGroup Logically &\nPrioritize Groups"]; // Uses default style
    GroupPrioritizeResult [label="Prioritized Groups:\n1. CVE (550) - Critical\n2. Phishing (549) - High\n3. User Activity (551, 552) - Med\n4. Travel (553) - Low", shape=note, width=3];
    // Edges for Parallel Step 2 - Join
    Examine553_Summary -> GroupPrioritize;
    Examine552_Summary -> GroupPrioritize;
    Examine551_Summary -> GroupPrioritize;
    Examine550_Summary -> GroupPrioritize;
    Examine549_Summary -> GroupPrioritize;
    GroupPrioritize -> GroupPrioritizeResult;
    // Step 5: Enrichment (Iterative)
    Enrichment [label="Step 5: Enrich Indicators (Iterative)\n(Processing Groups 1 -> 2 -> 3 -> 4)"]; // Uses default style
    GroupPrioritizeResult -> Enrichment;
    // Group 1 Enrichment
    subgraph cluster_enrich_g1 {
        label = "Enrich Group 1 (CVE)"; style=dashed; color=gray;
        EnrichG1_IP_GTI [label="gti.get_ip_address_report\n(104.130.139.139)", shape=ellipse, style=filled, fillcolor=lightblue];
        EnrichG1_URL_GTI [label="gti.get_url_report\n(...:8080)", shape=ellipse, style=filled, fillcolor=lightblue];
        EnrichG1_CVE_GTI [label="gti.search_vulnerabilities\n(CVE-2024-23897)", shape=ellipse, style=filled, fillcolor=lightblue];
        EnrichG1_IP_Chron [label="secops.lookup_entity\n(104.130.139.139)", shape=ellipse, style=filled, fillcolor=lightblue];
        EnrichG1_Summary [label="Summary (G1):\nCVE Exploited, IP/URL Malicious", shape=note];
        EnrichG1_IP_GTI -> EnrichG1_URL_GTI -> EnrichG1_CVE_GTI -> EnrichG1_IP_Chron -> EnrichG1_Summary;
    }
     // Group 2 Enrichment
     subgraph cluster_enrich_g2 {
        label = "Enrich Group 2 (Phishing)"; style=dashed; color=gray;
        EnrichG2_Domain_GTI [label="gti.get_domain_report\n(bonesinoffensivebook.com)", shape=ellipse, style=filled, fillcolor=lightblue];
        EnrichG2_URL_GTI [label="gti.get_url_report\n(...invoke.js)", shape=ellipse, style=filled, fillcolor=lightblue];
        // Use specific color for failed/not found lookups
        EnrichG2_Hash1_GTI [label="gti.get_file_report\n(HTM hash) - Not Found", shape=ellipse, style=filled, fillcolor=lightcoral];
        EnrichG2_Hash2_GTI [label="gti.get_file_report\n(PNG hash) - Not Found", shape=ellipse, style=filled, fillcolor=lightcoral];
        EnrichG2_Domain_Chron [label="secops.lookup_entity\n(bonesinoffensivebook.com)", shape=ellipse, style=filled, fillcolor=lightblue];
        EnrichG2_Summary [label="Summary (G2):\nDomain/URL Malicious", shape=note];
        EnrichG2_Domain_GTI -> EnrichG2_URL_GTI -> EnrichG2_Hash1_GTI -> EnrichG2_Hash2_GTI -> EnrichG2_Domain_Chron -> EnrichG2_Summary;
     }
     // Group 3 Enrichment
     subgraph cluster_enrich_g3 {
        label = "Enrich Group 3 (User Activity)"; style=dashed; color=gray;
        EnrichG3_URL_GTI [label="gti.get_url_report\n(testsafebrowsing...)", shape=ellipse, style=filled, fillcolor=lightblue];
        EnrichG3_Hash_GTI [label="gti.get_file_report\n(test file hash)", shape=ellipse, style=filled, fillcolor=lightblue];
        EnrichG3_Summary [label="Summary (G3):\nSafe Browsing Test File/URL", shape=note];
        EnrichG3_URL_GTI -> EnrichG3_Hash_GTI -> EnrichG3_Summary;
     }
     // Group 4 Enrichment
     subgraph cluster_enrich_g4 {
        label = "Enrich Group 4 (Travel)"; style=dashed; color=gray;
        EnrichG4_IP1_GTI [label="gti.get_ip_address_report\n(SG IP)", shape=ellipse, style=filled, fillcolor=lightblue];
        EnrichG4_IP2_GTI [label="gti.get_ip_address_report\n(US IP)", shape=ellipse, style=filled, fillcolor=lightblue];
        EnrichG4_Summary [label="Summary (G4):\nIPs Benign", shape=note];
        EnrichG4_IP1_GTI -> EnrichG4_IP2_GTI -> EnrichG4_Summary;
     }
    // Edges for Enrichment Flow
    Enrichment -> EnrichG1_IP_GTI [label="Group 1"];
    EnrichG1_Summary -> EnrichG2_Domain_GTI [label="Group 2"];
    EnrichG2_Summary -> EnrichG3_URL_GTI [label="Group 3"];
    EnrichG3_Summary -> EnrichG4_IP1_GTI [label="Group 4"];
    // Step 6: Related Event Search
    RelatedEvents [label="Step 6: Search Related Events\n(Processing G3 - Host CYMBAL)"]; // Uses default style
    EnrichG4_Summary -> RelatedEvents;
    RelatedEvents_Tool [label="secops.search_security_events\n(hostname=CYMBAL, hours_back=72)", shape=ellipse, style=filled, fillcolor=lightblue];
    RelatedEvents_Result [label="Result: No events found", shape=note];
    RelatedEvents -> RelatedEvents_Tool;
    RelatedEvents_Tool -> RelatedEvents_Result;
    // Step 7: Generate Report
    GenerateReport [label="Step 7: Generate Final Report"]; // Uses default style
    RelatedEvents_Result -> GenerateReport;
    FinalReport [label="Final Markdown Report\n(attempt_completion)", shape=note, style=filled, fillcolor=lightgrey]; // Explicit style for report
    GenerateReport -> FinalReport;
}
```

---

## Proactive Threat Hunting based on GTI Campaign/Actor (Revised)

Objective: Given a GTI Campaign or Threat Actor Collection ID (`${GTI_COLLECTION_ID}`), proactively search the local environment (SIEM) for related IOCs and TTPs (approximated by searching related entities). Summarize findings and optionally create a SOAR case for tracking or generate a markdown report. *Optimization: Prioritize SIEM lookups for IOCs found in recent matches or limit checks if the IOC set is very large.*

Uses Tools:

*   `gti-mcp.get_collection_report`
*   `gti-mcp.get_entities_related_to_a_collection` (for IOCs like files, domains, IPs, URLs)
*   `gti-mcp.get_collection_timeline_events` (for TTP context)
*   `secops-mcp.lookup_entity`
*   `secops-mcp.search_security_events`
*   `secops-mcp.get_ioc_matches`
*   `write_to_file` (for report generation)
*   `secops-soar.post_case_comment` (optional)
*   `ask_followup_question`

```{mermaid}
sequenceDiagram
    participant User
    participant Cline as Cline (MCP Client)
    participant GTI as gti-mcp
    participant SIEM as secops-mcp
    participant SOAR as secops-soar

    User->>Cline: Hunt for Campaign/Actor: `${GTI_COLLECTION_ID}`
    Cline->>GTI: get_collection_report(id=`${GTI_COLLECTION_ID}`)
    GTI-->>Cline: Collection Details (Name, Type, Description)
    Cline->>GTI: get_collection_timeline_events(id=`${GTI_COLLECTION_ID}`)
    GTI-->>Cline: Timeline Events (TTP Context)

    Note over Cline: Identify relevant IOC relationships (files, domains, ips, urls)
    loop For each IOC Relationship R
        Cline->>GTI: get_entities_related_to_a_collection(id=`${GTI_COLLECTION_ID}`, relationship_name=R)
        GTI-->>Cline: List of IOCs (e.g., Hashes H1, Domains D1, IPs IP1...)
    end

    Note over Cline: Initialize local_hunt_findings
    Cline->>SIEM: get_ioc_matches(hours_back=72)
    SIEM-->>Cline: Recent IOC Matches in SIEM (Matches M1, M2...)
    Note over Cline: Identify key IOCs from GTI (I1, I2...) and SIEM matches (M1, M2...)

    Note over Cline: Phase 1: Lookup key/prioritized IOCs
    loop For each prioritized IOC Ii (from GTI/SIEM Matches)
        Cline->>SIEM: lookup_entity(entity_value=Ii, hours_back=72)
        SIEM-->>Cline: SIEM Summary for Ii
        Note over Cline: Record IOCs with confirmed presence (P1, P2...)
    end

    Note over Cline: Phase 2: Search events only for IOCs with confirmed presence
    loop For each Present IOC Pi
        Cline->>SIEM: search_security_events(text="Events involving Pi", hours_back=72)
        SIEM-->>Cline: Relevant SIEM Events for Pi
        Note over Cline: Store significant event findings
    end

    Note over Cline: Synthesize GTI context, IOCs, TTPs, and SIEM findings
    Cline->>User: ask_followup_question(question="Hunt found potential activity related to `${GTI_COLLECTION_ID}`. Create/Update SOAR Case or Generate Report?", options=["Create New Case", "Update Case [ID]", "Generate Report", "Do Nothing"])
    User->>Cline: Response (e.g., "Generate Report")

    alt Output Action Confirmed
        alt Create/Update Case
            Note over Cline: Prepare summary comment for SOAR
            Cline->>SOAR: post_case_comment(case_id=[New/Existing ID], comment="Proactive Hunt Summary for `${GTI_COLLECTION_ID}`: Found IOCs [...] in SIEM. Events [...] observed. GTI Context: [...].")
            SOAR-->>Cline: Comment confirmation
            Cline->>Cline: attempt_completion(result="Proactive threat hunt for `${GTI_COLLECTION_ID}` complete. Findings summarized. SOAR case created/updated.")
        else Generate Report
            Note over Cline: Synthesize report content
            Cline->>Cline: write_to_file(path="./reports/proactive_hunt_report_${GTI_COLLECTION_ID}_${timestamp}.md", content=...)
            Note over Cline: Report file created locally.
            Cline->>Cline: attempt_completion(result="Proactive threat hunt for `${GTI_COLLECTION_ID}` complete. Report generated.")
        else Do Nothing
             Cline->>Cline: attempt_completion(result="Proactive threat hunt for `${GTI_COLLECTION_ID}` complete. Findings summarized. No output action taken.")
        end
    end

```

---

## Cloud Vulnerability Triage & Contextualization

Objective: Triage top critical/high SCC vulnerability findings for a given project (`${PROJECT_ID}`). Enrich the CVEs with GTI, check for related exploitation activity in SIEM, and summarize findings for remediation prioritization, potentially adding context to a SOAR case.

Uses Tools:

*   `scc-mcp.top_vulnerability_findings`
*   `scc-mcp.get_finding_remediation`
*   `gti-mcp.search_vulnerabilities` (or `get_threat_intel` for CVE summary)
*   `secops-mcp.search_security_events`
*   `secops-mcp.lookup_entity` (for affected resource)
*   `secops-soar.post_case_comment` (optional)
*   `ask_followup_question` (optional)

```{mermaid}
sequenceDiagram
    participant User
    participant Cline as Cline (MCP Client)
    participant SCC as scc-mcp
    participant GTI as gti-mcp
    participant SIEM as secops-mcp
    participant SOAR as secops-soar

    User->>Cline: Triage top vulnerabilities for project `${PROJECT_ID}`
    Cline->>SCC: top_vulnerability_findings(project_id=`${PROJECT_ID}`, max_findings=5)
    SCC-->>Cline: List of Top Findings (F1, F2... with CVE, Resource, Score)

    Note over Cline: Initialize triage_report
    loop For each Finding Fi
        Note over Cline: Extract CVE Ci and Resource Ri from Finding Fi
        Cline->>SCC: get_finding_remediation(finding_id=Fi_ID)
        SCC-->>Cline: Remediation Steps for Fi
        Note over Cline: Add remediation to triage_report

        Cline->>GTI: search_vulnerabilities(query=Ci)
        GTI-->>Cline: GTI details for CVE Ci (Exploitation status, related threats)
        Note over Cline: Add GTI context to triage_report

        Cline->>SIEM: lookup_entity(entity_value=Ri, hours_back=168) %% Check resource activity (e.g., IP/hostname) for 7 days
        SIEM-->>Cline: SIEM Summary for Resource Ri
        Note over Cline: Add resource activity summary to triage_report

        Cline->>SIEM: search_security_events(text="Events related to CVE Ci or exploitation attempts on Ri", hours_back=168)
        SIEM-->>Cline: Potential exploitation events
        Note over Cline: Add relevant event findings to triage_report
    end

    Note over Cline: Synthesize triage_report with findings, context, and prioritization based on Score/GTI/SIEM data
    Cline->>User: ask_followup_question(question="Triage complete. Add summary to SOAR Case?", options=["Yes, Case [ID]", "No"])
    User->>Cline: Response (e.g., "Yes, Case 123")

    alt Add to SOAR Case
        Cline->>SOAR: post_case_comment(case_id=123, comment="SCC Vuln Triage Summary (${PROJECT_ID}): Top findings analyzed. CVE [...] on Resource [...] shows GTI risk [...], SIEM activity [...]. Remediation: [...]. Full report attached/available.")
        SOAR-->>Cline: Comment confirmation
    end

    Cline->>Cline: attempt_completion(result="Cloud vulnerability triage for project `${PROJECT_ID}` complete. Findings synthesized. SOAR case potentially updated.")

```
