# Have I Been Pwned

## Overview

This integration provides tools to interact with the Have I Been Pwned service to check for compromised accounts.

## Available Tools

### Ping

**Tool Name:** `have_i_been_pwned_ping`

**Description:** Check connectivity.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on. Defaults to empty list.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the result of the action execution.

---

### Check Account

**Tool Name:** `have_i_been_pwned_check_account`

**Description:** Retrieve all breaches an account has been involved in and public "pastes" an account was found in.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on. Defaults to empty list. The action typically runs on User or Email entities.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the result of the action execution, including lists of breaches and pastes associated with the account(s).
