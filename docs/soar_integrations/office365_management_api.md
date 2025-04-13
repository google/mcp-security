# Office 365 Management API Integration

## Overview

This integration allows you to connect to the Office 365 Management API to manage content subscriptions and test connectivity.

## Configuration

The configuration for this integration (Tenant ID, Client ID, Client Secret, etc.) is managed within the SOAR platform's Marketplace tab. The actions utilize these pre-configured settings.

## Actions

### Stop Subscription

Stop a subscription to a chosen Office 365 Management API content type. Note: When a subscription is stopped, you will no longer receive notifications and will not be able to retrieve available content. If the subscription is later restarted, you will have access to new content from that point forward, but content available between stopping and restarting will be lost.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `stop_a_subscription_for` (List[Any], required): Specify for which content type to stop a subscription (e.g., Audit.AzureActiveDirectory, Audit.Exchange, Audit.SharePoint).
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the result of the stop subscription operation.

### Ping

Test connectivity to the O365 Management API service with parameters provided at the integration configuration page on the Marketplace tab.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the result of the ping action.

### Start Subscription

Start a subscription to a chosen Office 365 Management API content type.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `start_a_subscription_for` (List[Any], required): Specify for which content type to start a subscription (e.g., Audit.AzureActiveDirectory, Audit.Exchange, Audit.SharePoint).
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the result of the start subscription operation.

## Notes

*   Ensure the Office 365 Management API integration is properly configured in the SOAR Marketplace tab with the necessary application permissions and credentials.
*   Stopping and restarting subscriptions can lead to data gaps for the period the subscription was inactive.
