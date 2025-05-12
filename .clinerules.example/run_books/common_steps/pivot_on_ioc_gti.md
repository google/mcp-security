# Common Step: Pivot on IOC using GTI Relationships

## Objective

Explore relationships connected to a specific Indicator of Compromise (IOC) within Google Threat Intelligence (GTI) to discover related entities (other IOCs, threats, etc.).

## Scope

This sub-runbook executes the appropriate `gti-mcp.get_entities_related_to_a_...` tool based on the input IOC type and desired relationship(s). It returns the discovered related entities.

## Inputs

*   `${IOC_VALUE}`: The specific IOC value (e.g., "198.51.100.10", "evil-domain.com", "abcdef123456...", "http://bad.url/path").
*   `${IOC_TYPE}`: The type of IOC ("IP Address", "Domain", "File Hash", "URL", "Collection"). *Note: Added "Collection" type.*
*   `${RELATIONSHIP_NAMES}`: A list of relationship names to query (e.g., ["resolutions", "communicating_files"], ["malware_families", "attack_techniques"]). The available relationships depend on the `${IOC_TYPE}`.

## Outputs

*   `${RELATED_ENTITIES}`: A structured dictionary or list containing the entities found for each queried relationship.
*   `${PIVOT_STATUS}`: Confirmation or status of the pivoting attempt(s).

## Tools

*   `gti-mcp`: `get_entities_related_to_an_ip_address`, `get_entities_related_to_a_domain`, `get_entities_related_to_a_file`, `get_entities_related_to_an_url`, `get_entities_related_to_a_collection`

## Workflow Steps & Diagram

1.  **Receive Input:** Obtain `${IOC_VALUE}`, `${IOC_TYPE}`, and `${RELATIONSHIP_NAMES}` from the calling runbook. Initialize `${RELATED_ENTITIES}` as an empty structure.
2.  **Determine GTI Tool:** Based on `${IOC_TYPE}`, select the correct `gti-mcp` tool (e.g., `get_entities_related_to_an_ip_address` for "IP Address").
3.  **Iterate Relationships:** Loop through each `relationship` in `${RELATIONSHIP_NAMES}`.
    *   Call the selected GTI tool with the appropriate identifier (`ip_address`, `domain`, `hash`, `url`, `id`) set to `${IOC_VALUE}` and `relationship_name=relationship`.
    *   Store the results under the `relationship` key within `${RELATED_ENTITIES}`.
4.  **Return Results:** Set `${PIVOT_STATUS}` based on the success/failure of the API calls. Return `${RELATED_ENTITIES}` and `${PIVOT_STATUS}` to the calling runbook.

```{mermaid}
sequenceDiagram
    participant CallingRunbook
    participant PivotOnIOC as pivot_on_ioc_gti.md (This Runbook)
    participant GTI as gti-mcp

    CallingRunbook->>PivotOnIOC: Execute GTI Pivot\nInput: IOC_VALUE, IOC_TYPE, RELATIONSHIP_NAMES

    %% Step 2: Determine Tool
    Note over PivotOnIOC: Select GTI tool based on IOC_TYPE

    %% Step 3: Iterate Relationships
    loop For each relationship R in RELATIONSHIP_NAMES
        PivotOnIOC->>GTI: [Selected Tool](identifier=IOC_VALUE, relationship_name=R)
        GTI-->>PivotOnIOC: Related Entities List for R
        Note over PivotOnIOC: Store results in RELATED_ENTITIES[R]
    end

    %% Step 4: Return Results
    Note over PivotOnIOC: Set PIVOT_STATUS
    PivotOnIOC-->>CallingRunbook: Return Results:\nRELATED_ENTITIES,\nPIVOT_STATUS

```

## Completion Criteria

The relevant GTI relationship queries have been attempted for the specified IOC. The discovered related entities (`${RELATED_ENTITIES}`) and status (`${PIVOT_STATUS}`) are available.
