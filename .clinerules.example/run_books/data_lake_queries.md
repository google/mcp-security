# Runbook: Data Lake Queries (Placeholder)

## Objective

*(Define the goal, e.g., To query the security data lake for specific historical data, large-scale analysis, or information not readily available via standard SIEM searches.)*

## Scope

*(Define what is included/excluded, e.g., Focuses on constructing and executing BigQuery queries against specific datasets. Excludes real-time alerting.)*

## Inputs

*   `${QUERY_OBJECTIVE}`: Description of the data needed or the question to answer.
*   `${TARGET_DATASETS}`: Comma-separated list of BigQuery tables/datasets to query (e.g., `my_project.my_dataset.my_table`).
*   `${TIME_RANGE_START}`: Start timestamp for the query (e.g., ISO 8601 format).
*   `${TIME_RANGE_END}`: End timestamp for the query (e.g., ISO 8601 format).
*   *(Optional) `${SPECIFIC_FIELDS}`: Comma-separated list of specific fields to retrieve.*
*   *(Optional) `${FILTER_CONDITIONS}`: Specific WHERE clause conditions.*

## Tools

*   `bigquery`: `execute-query`, `describe-table`, `list-tables`
*   `write_to_file` (Optional, for saving results)
*   `secops-soar`: `post_case_comment` (Optional, for documenting query/results)

## Workflow Steps & Diagram

1.  **Define Query:** Based on `${QUERY_OBJECTIVE}`, `${TARGET_DATASETS}`, time range, and filters, construct the BigQuery SQL query. Use `describe-table` or `list-tables` if needed to confirm schema/table names.
2.  **Execute Query:** Run the query using `bigquery.execute-query`.
3.  **Analyze Results:** Review the query results.
4.  **Format/Save Results (Optional):** If needed, format the results and save them to a file using `write_to_file`.
5.  **Document (Optional):** Document the query executed and a summary of the results in a relevant SOAR case using `post_case_comment`.

```{mermaid}
sequenceDiagram
    participant Analyst/User
    participant Cline as Cline (MCP Client)
    participant BigQuery as bigquery
    participant SOAR as secops-soar (Optional)

    Analyst/User->>Cline: Start Data Lake Query\nInput: QUERY_OBJECTIVE, TARGET_DATASETS, TIME_RANGE...

    %% Step 1: Define Query
    opt Need Schema/Table Info
        Cline->>BigQuery: list-tables() / describe-table(table_name=...)
        BigQuery-->>Cline: Table/Schema Info
    end
    Note over Cline: Construct BigQuery SQL Query

    %% Step 2: Execute Query
    Cline->>BigQuery: execute-query(query=SQL_QUERY)
    BigQuery-->>Cline: Query Results

    %% Step 3: Analyze Results
    Note over Cline: Analyze query results

    %% Step 4: Format/Save Results (Optional)
    opt Save Results
        Note over Cline: Format results (e.g., CSV, JSON)
        Cline->>Cline: write_to_file(path="./query_results...", content=FormattedResults)
        Note over Cline: Results saved locally
    end

    %% Step 5: Document (Optional)
    opt Document in SOAR
        Cline->>SOAR: post_case_comment(case_id=..., comment="Data Lake Query Executed: [...], Summary: [...]")
        SOAR-->>Cline: Comment Confirmation
    end

    Cline->>Analyst/User: attempt_completion(result="Data lake query executed. Results analyzed/saved/documented as requested.")

```

## Completion Criteria

*(Define how successful completion is determined, e.g., Query successfully executed, results returned and analyzed/saved/documented as required.)*
