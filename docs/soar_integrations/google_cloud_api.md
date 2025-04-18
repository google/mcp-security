# Google Cloud API

## Overview

This integration provides generic tools to interact with Google Cloud APIs by executing HTTP requests.

## Available Tools

### Ping

**Tool Name:** `google_cloud_api_ping`

**Description:** Test connectivity.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on. Defaults to empty list.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the result of the action execution.

---

### Execute HTTP Request

**Tool Name:** `google_cloud_api_execute_http_request`

**Description:** Execute HTTP request.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `method` (List[Any], required): Specify the method for the request.
*   `url_path` (string, required): Specify the URL that needs to be executed.
*   `fields_to_return` (string, required): Specify what fields to return. Possible values: response_data, redirects, response_code,response_cookies,response_headers,apparent_encoding.
*   `request_timeout` (string, required): How long to wait for the server to send data before giving up.
*   `url_params` (string, optional): Specify the parameters for the URL. Any value provided in this parameter will be used alongside the values that are directly provided in the URL path parameters. Defaults to None.
*   `headers` (string, optional): Specify headers for the HTTP request. Defaults to None.
*   `cookie` (string, optional): Specify the parameters that should be constructed into the "Cookie" header. This parameter will overwrite the cookie provided in the "Headers" parameter. Defaults to None.
*   `body_payload` (string, optional): Specify body for the HTTP request. Defaults to None.
*   `expected_response_values` (string, optional): Specify the expected response values. If this parameter is not empty, then action will work in ASYNC mode and action will execute until the expected values will be seen or until timeout. Defaults to None.
*   `follow_redirects` (boolean, optional): If enabled, action will follow the redirects. Defaults to None.
*   `fail_on_4xx_5xx` (boolean, optional): If enabled, action will fail, if the status code of the response is 4xx or 5xx. Defaults to None.
*   `base64_output` (boolean, optional): If enabled, action will convert the response to base64. This is useful when downloading files. Note: JSON result can't be bigger than 15 mb. Defaults to None.
*   `save_to_case_wall` (boolean, optional): If enabled, action will save the file and attach it to the case wall. Note: the file will be archived with ".zip" extension. This zip will not be password protected. Defaults to None.
*   `password_protect_zip` (boolean, optional): If enabled, action will add an "infected" password to the zip created with "Save To Case Wall" parameter. Use this, when you are dealing with suspicious files. Defaults to None.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on. Defaults to empty list.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the result of the action execution.
