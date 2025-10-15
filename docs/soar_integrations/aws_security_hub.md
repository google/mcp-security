# AWS Security Hub Integration

The AWS Security Hub integration for Chronicle SOAR allows security teams to interact with findings within AWS Security Hub directly from the SOAR platform. This enables centralized visibility and streamlined response workflows for security issues identified across your AWS environment.

## Overview

AWS Security Hub provides a comprehensive view of your security state within AWS and helps you check your environment against security industry standards and best practices. It collects security data from across AWS accounts, services, and supported third-party partner products and helps you analyze your security trends and identify the highest priority security issues.

This integration facilitates:

*   **Ingestion of Findings:** Automatically pull findings from AWS Security Hub into Chronicle SOAR cases for investigation and triage.
*   **Finding Updates:** Update the status, severity, or workflow state of findings within Security Hub based on SOAR playbook actions or analyst decisions.
*   **Enrichment:** Gather details about specific Security Hub findings to enrich SOAR cases with context from AWS.
*   **Response Actions:** Trigger automated response actions within AWS based on Security Hub findings (though specific actions might depend on other AWS integrations like EC2, IAM, etc.).

## Key Actions

The following actions are available through the AWS Security Hub integration:

*   **Get Insight Details (`aws_security_hub_get_insight_details`)**
    *   Description: Return detailed information about an insight in AWS Security Hub.
    *   Parameters:
        *   `case_id` (string, required): The ID of the case.
        *   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
        *   `insight_arn` (string, required): Specify the ARN of the insight.
        *   `max_results_to_return` (string, optional): Specify how many results to return.
        *   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on.
        *   `scope` (string, optional, default="All entities"): Defines the scope for the action.

*   **Create Insight (`aws_security_hub_create_insight`)**
    *   Description: Create an insight in AWS Security Hub.
    *   Parameters:
        *   `case_id` (string, required): The ID of the case.
        *   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
        *   `insight_name` (string, required): Specify the name of the insight.
        *   `group_by_attribute` (List[str], required): Specify the name of the attribute by which findings should be grouped under one insight.
        *   `filter_json_object` (Union[str, dict], required): Specify a filter for the findings as a JSON object. Refer to action documentation for details.
        *   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on.
        *   `scope` (string, optional, default="All entities"): Defines the scope for the action.

*   **Ping (`aws_security_hub_ping`)**
    *   Description: Test connectivity to AWS Security Hub with parameters provided at the integration configuration page on Marketplace tab.
    *   Parameters:
        *   `case_id` (string, required): The ID of the case.
        *   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
        *   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on.
        *   `scope` (string, optional, default="All entities"): Defines the scope for the action.

*   **Update Finding (`aws_security_hub_update_finding`)**
    *   Description: Update findings in AWS Security Hub.
    *   Parameters:
        *   `case_id` (string, required): The ID of the case.
        *   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
        *   `id` (string, required): Specify ID of the finding that you want to update.
        *   `product_arn` (string, required): Specify the product ARN of the finding that you want to update.
        *   `note` (string, optional): Specify new text for the note on the finding. (Requires `note_author`).
        *   `note_author` (string, optional): Specify the author of the note. (Requires `note`).
        *   `severity` (List[str], optional): Specify new severity for the finding.
        *   `verification_state` (List[str], optional): Specify a new verification state for the finding.
        *   `confidence` (string, optional): Specify new confidence for the finding.
        *   `criticality` (string, optional): Specify new criticality for the finding.
        *   `types` (string, optional): Specify a comma-separated list of types for the finding (e.g., `type1,type2`).
        *   `workflow_status` (List[str], optional): Specify new workflow status for the finding.
        *   `custom_fields` (string, optional): Specify custom fields to update (Format: `Custom_field_1:value,Custom_field_2:value`).
        *   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on.
        *   `scope` (string, optional, default="All entities"): Defines the scope for the action.

*   **Update Insight (`aws_security_hub_update_insight`)**
    *   Description: Update an insight in AWS Security Hub.
    *   Parameters:
        *   `case_id` (string, required): The ID of the case.
        *   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
        *   `insight_arn` (string, required): Specify the ARN of the insight.
        *   `insight_name` (string, optional): Specify the new name of the insight.
        *   `group_by_attribute` (List[str], optional): Specify a new name of the attribute by which findings should be grouped.
        *   `filter_json_object` (Union[str, dict], optional): Specify a new filter for the findings as a JSON object.
        *   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on.
        *   `scope` (string, optional, default="All entities"): Defines the scope for the action.

## Use Cases

*   **Centralized Alert Triage:** Consolidate Security Hub findings alongside alerts from other security tools within Chronicle SOAR for unified investigation.
*   **Automated Response:** Trigger playbooks to automatically update findings (e.g., set `WorkflowState` to `SUPPRESSED` for known benign findings) or initiate remediation actions via other AWS integrations based on finding details.
*   **Contextual Enrichment:** Pull detailed finding information into SOAR cases to provide analysts with immediate context without needing to switch consoles.

## Configuration

*(Details on configuring the integration, including necessary AWS IAM permissions, API keys/credentials, and SOAR platform settings, should be added here.)*
