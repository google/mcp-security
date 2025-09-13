# Copyright 2025 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""Security Operations MCP tools for data table management."""

import logging
from typing import Any, Dict, List, Optional

from secops_mcp.server import get_chronicle_client, server


# Configure logging
logger = logging.getLogger('secops-mcp')

@server.tool()
async def create_data_table(
    name: str,
    description: str,
    header: Dict[str, str],
    project_id: str = None,
    customer_id: str = None,
    region: str = None,
    rows: Optional[List[List[str]]] = None,
) -> str:
    """Create a new data table in Chronicle SIEM.

    Creates a structured data table that can be referenced in detection rules to enhance
    detections with additional context. Data tables support multiple column types and
    can store structured information like IP ranges, user mappings, or threat intelligence.



    **Workflow Integration:**
    - Use to store structured security data that enhances detection rule logic.
    - Essential for maintaining context data used in threat detection and investigation.
    - Enables dynamic rule behavior based on curated datasets without hardcoding values.
    - Supports threat intelligence integration by storing IOC lists and contextual data.

    **Use Cases:**
    - Create tables of known malicious IP addresses with severity and description context.
    - Store asset inventories with criticality ratings for enhanced alert prioritization.
    - Maintain user role mappings for behavior-based detection rules.
    - Build threat intelligence feeds with IOC metadata for detection enhancement.
    - Create exception lists for reducing false positives in detection rules.

    **Column Types:**
    - STRING: Text values
    - CIDR: IP address ranges (e.g., "192.168.1.0/24")
    - INT64: Integer values
    - BOOL: Boolean values (true/false)

    Args:
        name (str): Unique name for the data table (used to reference in detection rules).
        description (str): Description of the data table's purpose and contents.
        header (Dict[str, str]): Column definitions mapping column names to their data types.
                                Valid types: "STRING", "CIDR", "INT64", "BOOL".
        project_id (str): Google Cloud project ID (required).
        customer_id (str): Chronicle customer ID (required).
        region (str): Chronicle region (e.g., "us", "europe") (required).
        rows (Optional[List[List[str]]]): Initial rows to populate the table. Each row should match the header columns.

    Returns:
        str: Success message with the created data table details.
             Returns error message if table creation fails.

    Example Usage:
        # Create a table for suspicious IP addresses
        create_data_table(
            name="suspicious_ips",
            description="Known suspicious IP addresses with context",
            header={
                "ip_address": "CIDR",
                "severity": "STRING",
                "description": "STRING",
                "is_active": "BOOL"
            },
            project_id="my-project",
            customer_id="my-customer",
            region="us",
            rows=[
                ["192.168.1.100", "High", "Scanning activity", "true"],
                ["10.0.0.5", "Medium", "Suspicious login attempts", "true"]
            ]
        )

        # Create a table for user roles
        create_data_table(
            name="user_roles",
            description="User role mappings for privilege analysis",
            header={
                "username": "STRING",
                "role": "STRING",
                "privilege_level": "INT64"
            },
            project_id="my-project",
            customer_id="my-customer",
            region="us"
        )

    Next Steps (using MCP-enabled tools):
        - Add more rows using `add_rows_to_data_table` as your dataset grows.
        - Reference the table in detection rules using the table name (e.g., data_table.suspicious_ips).
        - List table contents using `list_data_table_rows` to verify data integrity.
        - Update or remove specific rows using data table row management tools.
        - Use the table data to enhance detection logic and reduce false positives.
    """
    try:
        logger.info(f'Creating data table: {name}')

        
        
        chronicle = get_chronicle_client(project_id, customer_id, region)

        # Create the data table
        data_table = chronicle.create_data_table(
            name=name,
            description=description,
            header=header,
            rows=rows or []
        )

        # Extract table details from the response
        table_name = data_table.get("name", "").split("/")[-1]
        create_time = data_table.get("createTime", "Unknown")
        column_count = len(data_table.get("columnInfo", []))
        
        result = f'Successfully created data table: {name}\n'
        result += f'Table ID: {table_name}\n'
        result += f'Description: {description}\n'
        result += f'Created: {create_time}\n'
        result += f'Columns: {column_count}\n'
        
        # Show column details
        column_info = data_table.get("columnInfo", [])
        if column_info:
            result += '\nColumn Details:\n'
            for col in column_info:
                col_name = col.get("name", "Unknown")
                col_type = col.get("type", "Unknown")
                result += f'  - {col_name}: {col_type}\n'
        
        # Show initial row count if rows were provided
        if rows:
            result += f'\nInitial rows added: {len(rows)}'
        
        result += f'\nThe table can now be referenced in detection rules as: data_table.{name}'
        
        return result

    except Exception as e:
        logger.error(f'Error creating data table {name}: {str(e)}', exc_info=True)
        return f'Error creating data table {name}: {str(e)}'

@server.tool()
async def add_rows_to_data_table(
    table_name: str,
    rows: List[List[str]],
    project_id: str = None,
    customer_id: str = None,
    region: str = None,
) -> str:
    """Add rows to an existing data table in Chronicle SIEM.

    Adds new data rows to an existing data table, expanding the dataset available for
    detection rules. This is useful for maintaining and growing your threat intelligence,
    asset inventories, or other contextual data used in security detection.



    **Workflow Integration:**
    - Use to continuously update data tables with new threat intelligence or asset information.
    - Essential for maintaining current and accurate contextual data for detection rules.
    - Enables automated data table updates as part of threat intelligence feeds.
    - Supports operational workflows that add new entities or update security contexts.

    **Use Cases:**
    - Add newly discovered malicious IP addresses to threat intelligence tables.
    - Update asset inventories with new systems or changed criticality ratings.
    - Expand user role mappings as organizational structure changes.
    - Add new IOCs from threat intelligence feeds to detection enhancement tables.
    - Populate exception lists to reduce false positives in detection rules.

    **Data Consistency:**
    - Ensure new rows match the table's column schema and data types.
    - Validate data quality to maintain detection rule effectiveness.
    - Consider deduplication to avoid redundant entries in the table.

    Args:
        table_name (str): Name of the existing data table to add rows to.
        rows (List[List[str]]): List of rows to add. Each row should match the table's column schema.
        project_id (str): Google Cloud project ID (required).
        customer_id (str): Chronicle customer ID (required).
        region (str): Chronicle region (e.g., "us", "europe") (required).

    Returns:
        str: Success message with details about the added rows.
             Returns error message if row addition fails.

    Example Usage:
        # Add new suspicious IP addresses
        add_rows_to_data_table(
            table_name="suspicious_ips",
            rows=[
                ["172.16.0.1", "Low", "Unusual outbound connection", "true"],
                ["192.168.2.200", "Critical", "Data exfiltration attempt", "true"],
                ["203.0.113.50", "Medium", "Port scanning activity", "false"]
            ],
            project_id="my-project",
            customer_id="my-customer",
            region="us"
        )

        # Add new user role mappings
        add_rows_to_data_table(
            table_name="user_roles",
            rows=[
                ["john.doe", "admin", "5"],
                ["jane.smith", "analyst", "3"],
                ["bob.wilson", "viewer", "1"]
            ],
            project_id="my-project",
            customer_id="my-customer",
            region="us"
        )

    Next Steps (using MCP-enabled tools):
        - Verify the rows were added correctly using `list_data_table_rows`.
        - Test detection rules that reference the updated table to ensure they work as expected.
        - Monitor detection rule performance to assess the impact of the new data.
        - Consider setting up automated processes to regularly update the table.
        - Document the data sources and update procedures for operational teams.
    """
    try:
        logger.info(f'Adding {len(rows)} rows to data table: {table_name}')

        
        
        chronicle = get_chronicle_client(project_id, customer_id, region)

        # Add rows to the data table
        result_response = chronicle.create_data_table_rows(table_name, rows)

        result = f'Successfully added rows to data table: {table_name}\n'
        result += f'Rows added: {len(rows)}\n'
        
        # Show sample of added data
        if rows:
            result += '\nSample of added data:\n'
            for i, row in enumerate(rows[:3]):  # Show first 3 rows
                result += f'  Row {i+1}: {row}\n'
            
            if len(rows) > 3:
                result += f'  ... and {len(rows) - 3} more rows\n'
        
        result += f'\nThe updated table can be used in detection rules as: data_table.{table_name}'
        
        return result

    except Exception as e:
        logger.error(f'Error adding rows to data table {table_name}: {str(e)}', exc_info=True)
        return f'Error adding rows to data table {table_name}: {str(e)}'

@server.tool()
async def list_data_table_rows(
    table_name: str,
    project_id: str = None,
    customer_id: str = None,
    region: str = None,
    max_rows: int = 50,
) -> str:
    """List rows in a data table in Chronicle SIEM.

    Retrieves and displays the contents of a data table, showing all rows and their data.
    This is useful for reviewing table contents, verifying data integrity, and understanding
    what data is available for detection rules.



    **Workflow Integration:**
    - Use to verify data table contents after creation or updates.
    - Essential for auditing data quality and consistency in security context tables.
    - Helps understand available data when developing or troubleshooting detection rules.
    - Supports data governance by providing visibility into managed security datasets.

    **Use Cases:**
    - Review threat intelligence data before creating detection rules.
    - Verify that asset inventory data is current and accurate.
    - Audit user role mappings for consistency and completeness.
    - Troubleshoot detection rule issues by examining referenced table data.
    - Generate reports on security context data for compliance or operational reviews.

    Args:
        table_name (str): Name of the data table to list rows from.
        project_id (str): Google Cloud project ID (required).
        customer_id (str): Chronicle customer ID (required).
        region (str): Chronicle region (e.g., "us", "europe") (required).
        max_rows (int): Maximum number of rows to return. Defaults to 50.

    Returns:
        str: Formatted list of table rows with their data values.
             Returns error message if listing fails.

    Example Usage:
        # List contents of suspicious IP table
        list_data_table_rows(
            table_name="suspicious_ips",
            project_id="my-project",
            customer_id="my-customer",
            region="us",
            max_rows=25
        )

        # Review user role mappings
        list_data_table_rows(
            table_name="user_roles",
            project_id="my-project",
            customer_id="my-customer",
            region="us"
        )

    Next Steps (using MCP-enabled tools):
        - Add more rows using `add_rows_to_data_table` if the table needs additional data.
        - Delete specific rows using `delete_data_table_rows` if outdated or incorrect data is found.
        - Reference the table data in detection rules to enhance security monitoring.
        - Export the data for analysis or integration with other security tools.
        - Set up regular reviews to maintain data quality and relevance.
    """
    try:
        logger.info(f'Listing rows in data table: {table_name}')

        
        
        chronicle = get_chronicle_client(project_id, customer_id, region)

        # List rows in the data table
        rows = chronicle.list_data_table_rows(table_name)

        if not rows:
            return f'Data table "{table_name}" has no rows or was not found.'

        result = f'Data Table: {table_name}\n'
        result += f'Total rows found: {len(rows)}\n'
        
        # Limit rows displayed
        displayed_rows = rows[:max_rows]
        result += f'Displaying: {len(displayed_rows)} row(s)\n\n'

        # Show rows with their IDs and values
        for i, row in enumerate(displayed_rows):
            row_id = row.get("name", "").split("/")[-1]
            values = row.get("values", [])
            
            result += f'Row {i+1} (ID: {row_id}):\n'
            result += f'  Values: {values}\n\n'

        if len(rows) > max_rows:
            result += f'Note: Showing first {max_rows} rows out of {len(rows)} total rows.\n'
            result += f'Increase max_rows parameter to see more rows.'
        
        return result

    except Exception as e:
        logger.error(f'Error listing rows in data table {table_name}: {str(e)}', exc_info=True)
        return f'Error listing rows in data table {table_name}: {str(e)}'

@server.tool()
async def delete_data_table_rows(
    table_name: str,
    row_ids: List[str],
    project_id: str = None,
    customer_id: str = None,
    region: str = None,
) -> str:
    """Delete specific rows from a data table in Chronicle SIEM.

    Removes specific rows from a data table based on their row IDs. This is useful for
    maintaining data quality by removing outdated, incorrect, or no-longer-relevant entries
    from tables used in detection rules.



    **Workflow Integration:**
    - Use to maintain data quality by removing obsolete or incorrect entries.
    - Essential for keeping threat intelligence and context data current and accurate.
    - Supports data lifecycle management for security-relevant datasets.
    - Enables correction of data entry errors or removal of false positive triggers.

    **Use Cases:**
    - Remove IP addresses that are no longer considered suspicious.
    - Delete outdated asset inventory entries for decommissioned systems.
    - Remove user role mappings for employees who have left the organization.
    - Clean up threat intelligence data that has been invalidated or superseded.
    - Remove exception list entries that are no longer needed.

    **Safety Considerations:**
    - Ensure row IDs are correct before deletion as this operation cannot be undone.
    - Consider the impact on existing detection rules that reference the deleted data.
    - Coordinate deletions with detection rule updates if necessary.
    - Maintain backups or logs of deleted data for audit purposes.

    Args:
        table_name (str): Name of the data table to delete rows from.
        row_ids (List[str]): List of row IDs to delete. Use `list_data_table_rows` to get row IDs.
        project_id (str): Google Cloud project ID (required).
        customer_id (str): Chronicle customer ID (required).
        region (str): Chronicle region (e.g., "us", "europe") (required).

    Returns:
        str: Success message confirming the deletion of specified rows.
             Returns error message if deletion fails.

    Example Usage:
        # First, list rows to get their IDs
        # (Use list_data_table_rows to see row IDs)
        
        # Then delete specific rows
        delete_data_table_rows(
            table_name="suspicious_ips",
            row_ids=["row_12345", "row_67890"],
            project_id="my-project",
            customer_id="my-customer",
            region="us"
        )

        # Delete obsolete user role mappings
        delete_data_table_rows(
            table_name="user_roles",
            row_ids=["row_abc123", "row_def456", "row_ghi789"],
            project_id="my-project",
            customer_id="my-customer",
            region="us"
        )

    Next Steps (using MCP-enabled tools):
        - Verify the deletions using `list_data_table_rows` to confirm rows were removed.
        - Test detection rules that reference the table to ensure they still work correctly.
        - Add replacement data using `add_rows_to_data_table` if new entries are needed.
        - Document the reason for deletions for audit and operational tracking.
        - Review and update any documentation that references the deleted data.
    """
    try:
        logger.info(f'Deleting {len(row_ids)} rows from data table: {table_name}')

        
        
        chronicle = get_chronicle_client(project_id, customer_id, region)

        # Delete rows from the data table
        chronicle.delete_data_table_rows(table_name, row_ids)

        result = f'Successfully deleted rows from data table: {table_name}\n'
        result += f'Rows deleted: {len(row_ids)}\n'
        
        # Show the deleted row IDs
        result += '\nDeleted row IDs:\n'
        for row_id in row_ids:
            result += f'  - {row_id}\n'
        
        result += f'\nWarning: This operation cannot be undone. '
        result += f'Verify the table contents using list_data_table_rows if needed.'
        
        return result

    except Exception as e:
        logger.error(f'Error deleting rows from data table {table_name}: {str(e)}', exc_info=True)
        return f'Error deleting rows from data table {table_name}: {str(e)}' 