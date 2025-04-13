# Azure AD Identity Protection Integration

## Overview

This integration allows you to connect to Azure AD Identity Protection to manage user risk states, enrich user entities, and test connectivity.

## Configuration

To configure this integration within the SOAR platform, you typically need the following Azure Active Directory application registration details:

*   **Tenant ID:** Your Azure AD tenant identifier.
*   **Client ID:** The Application (client) ID of the registered application in Azure AD.
*   **Client Secret:** The client secret generated for the registered application.
*   **(Optional) API URL/Endpoint:** Sometimes needed if using a specific Azure cloud environment (e.g., Government Cloud), but often defaults to the standard Microsoft Graph API endpoint.

*(Note: The exact parameter names might vary slightly depending on the specific SOAR platform configuration interface. Ensure the registered application has the necessary Microsoft Graph API permissions granted for Identity Protection actions, such as `IdentityRiskEvent.Read.All`, `IdentityRiskyUser.ReadWrite.All`, etc.)*

## Actions

### Update User State

Update state of the user in Azure AD Identity Protection. Supported entities: Username, Email Address (user entity that matches email regex pattern).

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `state` (List[Any], optional): Specify the state for the users (e.g., `dismiss`, `confirmSafe`, `confirmCompromised`).
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on. Supports Username and Email Address entities.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the result of the action execution.

### Ping

Test connectivity to the Azure AD Identity Protection with parameters provided at the integration configuration page on the Marketplace tab.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the result of the ping action.

### Enrich Entities

Enrich entities using information from Azure AD Identity Protection. Supported entities: Username, Email Address (user entity that matches email regex pattern).

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `create_insights` (bool, optional): If enabled, action will create an insight containing all of the retrieved information about the entity.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on. Supports Username and Email Address entities.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing enrichment data (like risk state, risk level) for the specified user entities.

## Notes

*   Ensure the Azure AD Identity Protection integration is properly configured in the SOAR Marketplace tab with the correct Azure AD application credentials.
*   The registered Azure AD application requires appropriate Microsoft Graph API permissions for Identity Protection (e.g., `IdentityRiskEvent.Read.All`, `IdentityRiskyUser.ReadWrite.All`).
*   Actions primarily operate on User entities identified by Username or Email Address.
