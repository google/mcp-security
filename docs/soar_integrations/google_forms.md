# Google Forms

## Overview

This integration provides tools to interact with Google Forms. Currently, it only supports testing connectivity.

## Available Tools

### Ping

**Tool Name:** `google_forms_ping`

**Description:** Use the Ping action to test the connectivity to Google Forms.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on. Defaults to empty list.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the result of the action execution.
