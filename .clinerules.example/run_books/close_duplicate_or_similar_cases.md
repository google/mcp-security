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