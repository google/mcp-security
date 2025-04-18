# HashiCorp Vault

## Overview

This integration provides tools to interact with HashiCorp Vault for managing AWS credentials and Key-Value secrets.

## Available Tools

### Generate AWS Credentials

**Tool Name:** `hashi_corp_vault_generate_aws_credentials`

**Description:** Generate credentials based on AWS role stored in HashiCorp Vault. Note: This action doesn’t run on Chronicle SOAR entities.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `aws_role_name` (string, required): Specify the role name to generate credentials for.
*   `aws_secret_engine_path` (string, optional): Specify the path used for the aws secret storage. Parameter is used to interact with secrets stored in storage, it is used to construct the urls like https://x.x.x.x:8200/v1/aws/roles/. Defaults to None.
*   `aws_role_arn` (string, optional): Specify the ARN of the role to assume if credential_type on the Vault role is assumed_role. Must match one of the allowed role ARNs in the Vault role. Defaults to None.
*   `aws_role_session_name` (string, optional): Specify the role session name to attach to the assumed role ARN. If not provided it will be generated dynamically by default. Defaults to None.
*   `ttl_seconds` (string, optional): Specifies the TTL in seconds for the use of the STS token. This is specified as a string with a duration suffix. Valid only when AWS role credential_type in Vault is assumed_role or federation_token. When not specified, the default_sts_ttl set for the role will be used. If that is also not set, then the default value of 3600 seconds will be used. Defaults to None.
*   `json_expression_builder` (Union[str, dict], optional): Specify a JSON Expression Builder expression to filter a specific subset of data from secret, for example: | “data” | “data” | “key0”. Defaults to None.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on. Defaults to empty list.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the result of the action execution.

---

### Ping

**Tool Name:** `hashi_corp_vault_ping`

**Description:** Test connectivity to the HashiCorp Vault installation with parameters provided at the integration configuration page on the Marketplace tab.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on. Defaults to empty list.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the result of the action execution.

---

### List Key-Value Secret Keys

**Tool Name:** `hashi_corp_vault_list_key_value_secret_keys`

**Description:** List secrets keys available in the HashiCorp Vault based on provided criteria. Action returns key names stored in secret path without values. Folder names should be specified for secret path, action does not work if secret key is provided. Note: This action doesn't run on Chronicle SOAR entities.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `key_value_secret_engine_path` (string, optional): Specify the path used for the key-value secret storage. Currently only version 2 is supported. Parameter is used to interact with secrets stored in storage, it is used to construct the urls like https://x.x.x.x:8200/v1/secret/data/<secret to fetch from kv store>. Defaults to None.
*   `secret_path` (string, optional): Specify secret path to fetch, action accept folder names, example secret path folder name is my-secret, key-value store path is secret, so full path to fetch would be "https://x.x.x.x:8200/v1/secret/data/my-secret". If not provided, action will return all secret keys stored in the secret engine. Defaults to None.
*   `max_records_to_return` (string, optional): Specify how many records to return. If nothing is provided, action will return 50 records. Defaults to None.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on. Defaults to empty list.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the result of the action execution.

---

### List AWS Roles

**Tool Name:** `hashi_corp_vault_list_aws_roles`

**Description:** List AWS roles available in the HashiCorp Vault based on provided criteria. Note: This action doesn’t run on Chronicle SOAR entities.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `aws_secret_engine_path` (string, optional): Specify the path used for the aws secret storage. Parameter is used to interact with secrets stored in storage, it is used to construct the urls like https://x.x.x.x:8200/v1/aws/roles/. Defaults to None.
*   `max_records_to_return` (string, optional): Specify how many records to return. If nothing is provided, action will return 50 records. Defaults to None.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on. Defaults to empty list.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the result of the action execution.

---

### Read Key-Value Secret

**Tool Name:** `hashi_corp_vault_read_key_value_secret`

**Description:** Read Key-Value secret stored in HashiCorp Vault based on provided criteria. Note: This action doesn't run on Chronicle SOAR entities.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `secret_path` (string, required): Specify secret path to fetch, example secret path is my-secret, key-value store path is secret, so full path to fetch would be "https://x.x.x.x:8200/v1/secret/data/my-secret".
*   `key_value_secret_engine_path` (string, optional): Specify the path used for the key-value secret storage. Currently only version 2 is supported. Parameter is used to interact with secrets stored in storage, it is used to construct the urls like https://x.x.x.x:8200/v1/secret/data/<secret to fetch from kv store>. Defaults to None.
*   `secret_version` (string, optional): Specify a secret version to fetch. Defaults to None.
*   `json_expression_builder` (Union[str, dict], optional): Specify a JSON Expression Builder expression to filter a specific subset of data from secret, for example: data | data | key0. Defaults to None.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on. Defaults to empty list.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the result of the action execution.
