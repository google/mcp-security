# Azure Security Center Integration

## Overview

This integration allows you to connect to Azure Security Center (now part of Microsoft Defender for Cloud) to manage security alerts, list regulatory compliance standards and controls, and handle OAuth tokens for configuration.

## Configuration

To configure this integration within the SOAR platform, you typically need the following Azure details:

*   **Tenant ID:** Your Azure AD tenant identifier.
*   **Client ID:** The Application (client) ID of the registered application in Azure AD.
*   **Client Secret:** The client secret generated for the registered application.
*   **Subscription ID:** The ID of the Azure subscription containing the Security Center resources you want to manage.
*   **(Optional) API URL/Endpoint:** Sometimes needed if using a specific Azure cloud environment (e.g., Government Cloud), but often defaults to the standard Azure Resource Manager endpoint.
*   **(Optional) Refresh Token:** For OAuth authentication flows, a refresh token might be required. Use the `Get OAuth Refresh Token` action to generate this if needed.

*(Note: The exact parameter names might vary slightly depending on the specific SOAR platform configuration interface. Ensure the registered application has the necessary permissions granted within the target subscription for Azure Security Center actions, such as `SecurityEvents.ReadWrite.All`.)*

## Actions

### Get OAuth Refresh Token

Generate the refresh token that is needed for the integration configuration. Authorization code can be generated using "Get OAuth Authorization Code". Please refer to the documentation portal for more information.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `redirect_url` (string, required): Specify the redirect URL that was used when the app was created.
*   `authorization_code` (string, required): Specify the authorization code from action "Get OAuth Authorization Code".
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the refresh token and related details.

### Ping

Test connectivity to Azure Security Center with parameters provided at the integration configuration page on Marketplace tab.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the result of the ping action.

### List Regulatory Standards

List available regulatory standards in Microsoft Azure Security Center.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `subscription_id` (string, optional): Specify the ID of the subscription. Overrides integration-level setting if provided.
*   `state_filter` (string, optional): Comma-separated list of states to filter by (Passed, Failed, Unsupported, Skipped).
*   `max_standards_to_return` (string, optional): Specify how many standards to return.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the list of regulatory standards matching the criteria.

### Update Alert Status

Update status of the alert in Microsoft Azure Security Center.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `alert_id` (string, required): Specify an ID of the alert, where you want to update status.
*   `location` (string, required): Specify the location of the alert. Example: centralus.
*   `status` (List[Any], required): Specify the status for the alert (e.g., Dismissed, Activated).
*   `subscription_id` (string, optional): Specify the ID of the subscription. Overrides integration-level setting if provided.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the result of the alert update operation.

### List Regulatory Standard Controls

List available controls related to standards in Microsoft Azure Security Center.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `standard_names` (string, required): Specify a comma-separated list of standard names for which you want to retrieve details. Example: Azure-CIS-1.1.0
*   `subscription_id` (string, optional): Specify the ID of the subscription. Overrides integration-level setting if provided.
*   `state_filter` (string, optional): Specify the comma-separated list of states (Passed, Failed, Unsupported, Skipped).
*   `max_standards_to_return` (string, optional): Specify how many controls to return per standard.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the list of controls for the specified standards.

### Get OAuth Authorization Code

Generate an OAuth authorization code in Azure Security Center. Please refer to the documentation portal for more information.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `redirect_url` (string, required): Specify the redirect URL that was used when the app was created.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the authorization URL to initiate the OAuth flow.

## Notes

*   Ensure the Azure Security Center integration is properly configured in the SOAR Marketplace tab with the correct Azure AD application credentials and Subscription ID.
*   The registered Azure AD application requires appropriate permissions for Azure Security Center / Microsoft Defender for Cloud.
*   The `Get OAuth Authorization Code` and `Get OAuth Refresh Token` actions are typically used once during setup to obtain the necessary token for the integration configuration if using OAuth.
