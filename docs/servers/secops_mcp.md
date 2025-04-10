# Chronicle Security Operations (SecOps) MCP Server

This server provides tools for interacting with Chronicle Security Operations using the `secops-py` library.

**Note:** This server requires Chronicle API credentials (Project ID, Customer ID) to be configured, typically via environment variables (`CHRONICLE_PROJECT_ID`, `CHRONICLE_CUSTOMER_ID`, `CHRONICLE_REGION`).

## Tools

- **`search_security_events(text, project_id=None, customer_id=None, hours_back=24, max_events=100, region=None)`**
    - **Description:** Searches for security events in Chronicle using natural language. Translates the natural language query (`text`) into a UDM query and executes it.
    - **Parameters:**
        - `text` (required): Natural language description of the events to find.
        - `project_id` (optional): Google Cloud project ID (defaults to environment config).
        - `customer_id` (optional): Chronicle customer ID (defaults to environment config).
        - `hours_back` (optional): How many hours to look back (default: 24).
        - `max_events` (optional): Maximum number of events to return (default: 100).
        - `region` (optional): Chronicle region (defaults to environment config or 'us').
    - **Returns:** Dictionary containing the generated `udm_query` and the `events` results.

- **`get_security_alerts(project_id=None, customer_id=None, hours_back=24, max_alerts=10, status_filter='feedback_summary.status != "CLOSED"', region=None)`**
    - **Description:** Retrieves security alerts from Chronicle, filtered by time range and status.
    - **Parameters:**
        - `project_id` (optional): Google Cloud project ID (defaults to environment config).
        - `customer_id` (optional): Chronicle customer ID (defaults to environment config).
        - `hours_back` (optional): How many hours to look back (default: 24).
        - `max_alerts` (optional): Maximum number of alerts to return (default: 10).
        - `status_filter` (optional): Query string to filter alerts by status (default: excludes closed alerts).
        - `region` (optional): Chronicle region (defaults to environment config or 'us').
    - **Returns:** Formatted string listing the found security alerts.

- **`lookup_entity(entity_value, project_id=None, customer_id=None, hours_back=24, region=None)`**
    - **Description:** Looks up an entity (IP, domain, hash, etc.) in Chronicle.
    - **Parameters:**
        - `entity_value` (required): Value to look up (IP, domain, hash, etc.).
        - `project_id` (optional): Google Cloud project ID (defaults to environment config).
        - `customer_id` (optional): Chronicle customer ID (defaults to environment config).
        - `hours_back` (optional): How many hours to look back (default: 24).
        - `region` (optional): Chronicle region (defaults to environment config or 'us').
    - **Returns:** Formatted string summarizing the entity information and associated alerts.

- **`list_security_rules(project_id=None, customer_id=None, region=None)`**
    - **Description:** Lists security detection rules from Chronicle.
    - **Parameters:**
        - `project_id` (optional): Google Cloud project ID (defaults to environment config).
        - `customer_id` (optional): Chronicle customer ID (defaults to environment config).
        - `region` (optional): Chronicle region (defaults to environment config or 'us').
    - **Returns:** Dictionary containing the raw API response with the list of rules.

- **`get_ioc_matches(project_id=None, customer_id=None, hours_back=24, max_matches=20, region=None)`**
    - **Description:** Retrieves Indicators of Compromise (IoCs) matches from Chronicle within a specified time range.
    - **Parameters:**
        - `project_id` (optional): Google Cloud project ID (defaults to environment config).
        - `customer_id` (optional): Chronicle customer ID (defaults to environment config).
        - `hours_back` (optional): How many hours to look back (default: 24).
        - `max_matches` (optional): Maximum number of matches to return (default: 20).
        - `region` (optional): Chronicle region (defaults to environment config or 'us').
    - **Returns:** Formatted string listing the found IoC matches.
