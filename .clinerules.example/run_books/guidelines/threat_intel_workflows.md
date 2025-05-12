# Runbook: Threat Intelligence Workflows (Placeholder)

## Objective

*(Define the goal, e.g., To outline common workflows for CTI Researchers, such as researching a new threat actor, analyzing a malware family, or disseminating intelligence.)*

## Scope

*(Define what is included/excluded, e.g., Covers typical CTI tasks using GTI, SIEM, and SOAR tools. May link to specific hunting or analysis runbooks.)*

## Inputs

*(Define typical inputs, e.g., `${THREAT_NAME}`, `${IOC_VALUE}`, `${GTI_COLLECTION_ID}`, `${INTELLIGENCE_REQUIREMENT}`)*

## Tools

*   `gti-mcp`: (List relevant tools, likely most of them)
*   `secops-mcp`: `search_security_events`, `lookup_entity`, `get_ioc_matches`
*   `secops-soar`: `post_case_comment`, `list_cases`, `siemplify_add_general_insight`
*   `write_to_file` (For reports)
*   *(External OSINT tools/feeds - Manual)*

## Workflow Steps & Diagram

*(This section would outline common CTI processes, potentially branching based on the type of intelligence task.)*

**Example Workflow: Researching a Threat Actor**

1.  **Receive Input:** Obtain Threat Actor Name or ID (`${THREAT_ACTOR_ID}`).
2.  **Initial GTI Lookup:** Use `gti-mcp.search_threat_actors` or `gti-mcp.get_collection_report`.
3.  **Explore Relationships:** Use `gti-mcp.get_entities_related_to_a_collection` to find associated malware, campaigns, TTPs, IOCs.
4.  **Analyze TTPs:** Use `gti-mcp.get_collection_mitre_tree`.
5.  **Review Timelines:** Use `gti-mcp.get_collection_timeline_events`.
6.  **Correlate Locally (Optional):** Use `secops-mcp` tools (`search_security_events`, `lookup_entity`) to search for related IOCs/TTPs in the environment.
7.  **Synthesize & Report:** Compile findings into a threat actor profile using `write_to_file`.
8.  **Disseminate:** Share findings via `secops-soar.post_case_comment` or other channels.

```{mermaid}
sequenceDiagram
    participant Researcher
    participant Cline as Cline (MCP Client)
    participant GTI as gti-mcp
    participant SIEM as secops-mcp
    participant SOAR as secops-soar

    Researcher->>Cline: Research Threat Actor\nInput: THREAT_ACTOR_ID

    %% Step 2: Initial GTI Lookup
    Cline->>GTI: get_collection_report(id=THREAT_ACTOR_ID)
    GTI-->>Cline: Actor Details

    %% Step 3: Explore Relationships
    Cline->>GTI: get_entities_related_to_a_collection(id=THREAT_ACTOR_ID, relationship_name="malware_families")
    GTI-->>Cline: Related Malware
    Cline->>GTI: get_entities_related_to_a_collection(id=THREAT_ACTOR_ID, relationship_name="attack_techniques")
    GTI-->>Cline: Related TTPs
    %% Add other relationship calls

    %% Step 4: Analyze TTPs
    Cline->>GTI: get_collection_mitre_tree(id=THREAT_ACTOR_ID)
    GTI-->>Cline: MITRE TTP Tree

    %% Step 5: Review Timelines
    Cline->>GTI: get_collection_timeline_events(id=THREAT_ACTOR_ID)
    GTI-->>Cline: Timeline Events

    %% Step 6: Correlate Locally (Optional)
    opt Correlate Locally
        Note over Cline: Extract key IOCs/TTPs
        loop For each IOC/TTP Indicator Ii
            Cline->>SIEM: search_security_events(text="Search for Ii")
            SIEM-->>Cline: Local Activity Results
        end
    end

    %% Step 7: Synthesize & Report
    Note over Cline: Compile Threat Actor Profile
    Cline->>Cline: write_to_file(path="./reports/actor_profile_...", content=ReportMarkdown)
    Note over Cline: Report Saved

    %% Step 8: Disseminate
    Cline->>SOAR: post_case_comment(case_id=..., comment="Threat Actor Profile for THREAT_ACTOR_ID available: ...")
    SOAR-->>Cline: Comment Confirmation

    Cline->>Researcher: attempt_completion(result="Threat Actor research complete. Profile generated.")

```

## Completion Criteria

*(Define how successful completion is determined, e.g., Intelligence gathered, analyzed, correlated, and disseminated according to the specific task.)*
