

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


 * List Cases
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


### New Report to Environment Sweep

From a GTI Collection (could be a Private Collection as well), search for any UDM events containing:
 1) Indicators of Compromise
 2) IOC++ (Modeled behvaioral data) (Would need to interpret relevant UDM fields)

Analyze results and compare against GTI Collection context (report or campaign). Notable indicators are added to Data Table. Provide analyst report with prescribed follow on response actions.

Uses tools:

 * `gti-mcp.get_collection_report`
 * `secops-mcp.get_ioc_matches`
 * `secops-mcp.search_security_events`
 * `secops-mcp.get_security_alerts`
 * `gti-mcp.*` (various lookups like `get_file_report`, etc.)
 * (Conceptual) Add to Data Table
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
