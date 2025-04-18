# HTTP

## Overview

This integration provides basic tools for making HTTP GET and POST requests. For more advanced HTTP operations, consider using the HTTP V2 integration.

## Available Tools

### Get Data

**Tool Name:** `http_get_data`

**Description:** Send HTTP GET request.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `url` (string, required): The url to send the request to.
*   `username` (string, optional): Username for basic authentication. Defaults to None.
*   `password` (string, optional): Password for basic authentication. Defaults to None.
*   `ssl_verification` (boolean, optional): Whether to verify the SSL certificate of the destination server. Defaults to None.
*   `ignore_http_error_codes` (boolean, optional): If enabled, action should ignore 4xx or 5xx HTTP error codes and not return error. Defaults to None.
*   `headers_json` (Union[str, dict], optional): JSON object of HTTP headers to be sent with the request. Defaults to None.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on. Defaults to empty list.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the result of the action execution, typically the response body.

---

### Get URL Data

**Tool Name:** `http_get_url_data`

**Description:** Send HTTP GET request to URL entities.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `username` (string, optional): Username for basic authentication. Optional. Defaults to None.
*   `password` (string, optional): Password for basic authentication. Optional. Defaults to None.
*   `ssl_verification` (boolean, optional): Whether to verify the SSL certificate of the destination server. Defaults to None.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on. This action typically runs on URL entities. Defaults to empty list.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the result of the action execution for each URL entity.

---

### Ping

**Tool Name:** `http_ping`

**Description:** Test Connectivity.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on. Defaults to empty list.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the result of the ping action.

---

### Post Data

**Tool Name:** `http_post_data`

**Description:** Send HTTP POST requests.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `url` (string, required): The url to send the request to.
*   `data` (string, required): The data to send with the request.
*   `username` (string, optional): Username for basic authentication. Defaults to None.
*   `password` (string, optional): Password for basic authentication. Defaults to None.
*   `ssl_verification` (boolean, optional): Whether to verify the SSL certificate of the destination server. Defaults to None.
*   `headers_json` (Union[str, dict], optional): JSON object of HTTP headers to be sent with the request. Defaults to None.
*   `content_type` (List[Any], optional): Content Type. If set to application/json the input data must be JSON string. Defaults to None.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on. Defaults to empty list.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the result of the action execution, typically the response body.
