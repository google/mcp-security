# FortiAnalyzer

## Overview

This integration provides tools to interact with FortiAnalyzer.

## Available Tools

### Update Alert

**Tool Name:** `forti_analyzer_update_alert`

**Description:** Update an alert in FortiAnalyzer.

**Input Schema:**

```json
{
  "type": "object",
  "properties": {
    "case_id": {
      "description": "The ID of the case.",
      "title": "Case Id",
      "type": "string"
    },
    "alert_group_identifiers": {
      "description": "Identifiers for the alert groups.",
      "items": {
        "type": "string"
      },
      "title": "Alert Group Identifiers",
      "type": "array"
    },
    "alert_id": {
      "description": "Specify the ID of the alert that needs to be updated.",
      "title": "Alert Id",
      "type": "string"
    },
    "acknowledge_status": {
      "anyOf": [
        {
          "items": {},
          "type": "array"
        },
        {
          "type": "null"
        }
      ],
      "default": null,
      "description": "Specify the acknowledgment status for alert.",
      "title": "Acknowledge Status"
    },
    "mark_as_read": {
      "anyOf": [
        {
          "type": "boolean"
        },
        {
          "type": "null"
        }
      ],
      "default": null,
      "description": "If enabled, the action marks the alert as read.",
      "title": "Mark As Read"
    },
    "assign_to": {
      "anyOf": [
        {
          "type": "string"
        },
        {
          "type": "null"
        }
      ],
      "default": null,
      "description": "Specify to whom the alert needs to be assigned.",
      "title": "Assign To"
    },
    "target_entities": {
      "description": "Optional list of specific target entities (Identifier, EntityType) to run the action on.",
      "items": {
        "$ref": "#/$defs/TargetEntity"
      },
      "title": "Target Entities",
      "type": "array",
      "default": []
    },
    "scope": {
      "default": "All entities",
      "description": "Defines the scope for the action.",
      "title": "Scope",
      "type": "string"
    }
  },
  "$defs": {
    "TargetEntity": {
      "properties": {
        "Identifier": {
          "title": "Identifier",
          "type": "string"
        },
        "EntityType": {
          "title": "Entitytype",
          "type": "string"
        }
      },
      "required": [
        "Identifier",
        "EntityType"
      ],
      "title": "TargetEntity",
      "type": "object"
    }
  },
  "required": [
    "case_id",
    "alert_group_identifiers",
    "alert_id"
  ],
  "title": "forti_analyzer_update_alertArguments"
}
```

**Returns:** `dict` - A dictionary containing the result of the action execution.

---

### Search Logs

**Tool Name:** `forti_analyzer_search_logs`

**Description:** Search logs in FortiAnalyzer. Note: Action is running as async, adjust the script timeout value in Siemplify IDE for action as needed.

**Input Schema:**

```json
{
  "type": "object",
  "properties": {
    "case_id": {
      "description": "The ID of the case.",
      "title": "Case Id",
      "type": "string"
    },
    "alert_group_identifiers": {
      "description": "Identifiers for the alert groups.",
      "items": {
        "type": "string"
      },
      "title": "Alert Group Identifiers",
      "type": "array"
    },
    "log_type": {
      "anyOf": [
        {
          "items": {},
          "type": "array"
        },
        {
          "type": "null"
        }
      ],
      "default": null,
      "description": "Specify the log type that needs to be searched.",
      "title": "Log Type"
    },
    "case_sensitive_filter": {
      "anyOf": [
        {
          "type": "boolean"
        },
        {
          "type": "null"
        }
      ],
      "default": null,
      "description": "If enabled, the filter is case sensitive.",
      "title": "Case Sensitive Filter"
    },
    "query_filter": {
      "anyOf": [
        {
          "type": "string"
        },
        {
          "type": "null"
        }
      ],
      "default": null,
      "description": "Specify the query filter for the search.",
      "title": "Query Filter"
    },
    "device_id": {
      "anyOf": [
        {
          "type": "string"
        },
        {
          "type": "null"
        }
      ],
      "default": null,
      "description": "Specify the ID of the device that needs to be searched. If nothing is provided, the action searches in All_Fortigate. Examples of values: All_FortiGate, All_FortiMail, All_FortiWeb, All_FortiManager, All_Syslog, All_FortiClient, All_FortiCache, All_FortiProxy, All_FortiAnalyzer, All_FortiSandbox, All_FortiAuthenticator, All_FortiDDoS.",
      "title": "Device Id"
    },
    "time_frame": {
      "anyOf": [
        {
          "items": {},
          "type": "array"
        },
        {
          "type": "null"
        }
      ],
      "default": null,
      "description": "Specify a time frame for the results. If \"Custom\" is selected, you also need to provide the \"Start Time\" parameter.",
      "title": "Time Frame"
    },
    "start_time": {
      "anyOf": [
        {
          "type": "string"
        },
        {
          "type": "null"
        }
      ],
      "default": null,
      "description": "Specify the start time for the results. This parameter is mandatory, if \"Custom\" is selected for the \"Time Frame\" parameter. Format: ISO 8601",
      "title": "Start Time"
    },
    "end_time": {
      "anyOf": [
        {
          "type": "string"
        },
        {
          "type": "null"
        }
      ],
      "default": null,
      "description": "Specify the end time for the results. Format: ISO 8601. If nothing is provided and \"Custom\" is selected for the \"Time Frame\" parameter then this parameter uses current time.",
      "title": "End Time"
    },
    "time_order": {
      "anyOf": [
        {
          "items": {},
          "type": "array"
        },
        {
          "type": "null"
        }
      ],
      "default": null,
      "description": "Specify the time ordering in the search.",
      "title": "Time Order"
    },
    "max_logs_to_return": {
      "anyOf": [
        {
          "type": "string"
        },
        {
          "type": "null"
        }
      ],
      "default": null,
      "description": "Specify the number of logs you want to return. Default: 20. Maximum: 1000.",
      "title": "Max Logs To Return"
    },
    "target_entities": {
      "description": "Optional list of specific target entities (Identifier, EntityType) to run the action on.",
      "items": {
        "$ref": "#/$defs/TargetEntity"
      },
      "title": "Target Entities",
      "type": "array",
      "default": []
    },
    "scope": {
      "default": "All entities",
      "description": "Defines the scope for the action.",
      "title": "Scope",
      "type": "string"
    }
  },
  "$defs": {
    "TargetEntity": {
      "properties": {
        "Identifier": {
          "title": "Identifier",
          "type": "string"
        },
        "EntityType": {
          "title": "Entitytype",
          "type": "string"
        }
      },
      "required": [
        "Identifier",
        "EntityType"
      ],
      "title": "TargetEntity",
      "type": "object"
    }
  },
  "required": [
    "case_id",
    "alert_group_identifiers"
  ],
  "title": "forti_analyzer_search_logsArguments"
}
```

**Returns:** `dict` - A dictionary containing the result of the action execution.

---

### Ping

**Tool Name:** `forti_analyzer_ping`

**Description:** Test connectivity to the FortiAnalyzer with parameters provided at the integration configuration page on the Marketplace tab.

**Input Schema:**

```json
{
  "type": "object",
  "properties": {
    "case_id": {
      "description": "The ID of the case.",
      "title": "Case Id",
      "type": "string"
    },
    "alert_group_identifiers": {
      "description": "Identifiers for the alert groups.",
      "items": {
        "type": "string"
      },
      "title": "Alert Group Identifiers",
      "type": "array"
    },
    "target_entities": {
      "description": "Optional list of specific target entities (Identifier, EntityType) to run the action on.",
      "items": {
        "$ref": "#/$defs/TargetEntity"
      },
      "title": "Target Entities",
      "type": "array",
      "default": []
    },
    "scope": {
      "default": "All entities",
      "description": "Defines the scope for the action.",
      "title": "Scope",
      "type": "string"
    }
  },
  "$defs": {
    "TargetEntity": {
      "properties": {
        "Identifier": {
          "title": "Identifier",
          "type": "string"
        },
        "EntityType": {
          "title": "Entitytype",
          "type": "string"
        }
      },
      "required": [
        "Identifier",
        "EntityType"
      ],
      "title": "TargetEntity",
      "type": "object"
    }
  },
  "required": [
    "case_id",
    "alert_group_identifiers"
  ],
  "title": "forti_analyzer_pingArguments"
}
```

**Returns:** `dict` - A dictionary containing the result of the action execution.

---

### Add Comment To Alert

**Tool Name:** `forti_analyzer_add_comment_to_alert`

**Description:** Add a comment to alert in FortiAnalyzer.

**Input Schema:**

```json
{
  "type": "object",
  "properties": {
    "case_id": {
      "description": "The ID of the case.",
      "title": "Case Id",
      "type": "string"
    },
    "alert_group_identifiers": {
      "description": "Identifiers for the alert groups.",
      "items": {
        "type": "string"
      },
      "title": "Alert Group Identifiers",
      "type": "array"
    },
    "alert_id": {
      "description": "Specify the ID of the alert that needs to be updated.",
      "title": "Alert Id",
      "type": "string"
    },
    "comment": {
      "description": "Specify the comment for the alert.",
      "title": "Comment",
      "type": "string"
    },
    "target_entities": {
      "description": "Optional list of specific target entities (Identifier, EntityType) to run the action on.",
      "items": {
        "$ref": "#/$defs/TargetEntity"
      },
      "title": "Target Entities",
      "type": "array",
      "default": []
    },
    "scope": {
      "default": "All entities",
      "description": "Defines the scope for the action.",
      "title": "Scope",
      "type": "string"
    }
  },
  "$defs": {
    "TargetEntity": {
      "properties": {
        "Identifier": {
          "title": "Identifier",
          "type": "string"
        },
        "EntityType": {
          "title": "Entitytype",
          "type": "string"
        }
      },
      "required": [
        "Identifier",
        "EntityType"
      ],
      "title": "TargetEntity",
      "type": "object"
    }
  },
  "required": [
    "case_id",
    "alert_group_identifiers",
    "alert_id",
    "comment"
  ],
  "title": "forti_analyzer_add_comment_to_alertArguments"
}
```

**Returns:** `dict` - A dictionary containing the result of the action execution.

---

### Enrich Entities

**Tool Name:** `forti_analyzer_enrich_entities`

**Description:** Enrich entities using information from FortiAnalyzer. Supported entities: Hostname, IP Address.

**Input Schema:**

```json
{
  "type": "object",
  "properties": {
    "case_id": {
      "description": "The ID of the case.",
      "title": "Case Id",
      "type": "string"
    },
    "alert_group_identifiers": {
      "description": "Identifiers for the alert groups.",
      "items": {
        "type": "string"
      },
      "title": "Alert Group Identifiers",
      "type": "array"
    },
    "target_entities": {
      "description": "Optional list of specific target entities (Identifier, EntityType) to run the action on.",
      "items": {
        "$ref": "#/$defs/TargetEntity"
      },
      "title": "Target Entities",
      "type": "array",
      "default": []
    },
    "scope": {
      "default": "All entities",
      "description": "Defines the scope for the action.",
      "title": "Scope",
      "type": "string"
    }
  },
  "$defs": {
    "TargetEntity": {
      "properties": {
        "Identifier": {
          "title": "Identifier",
          "type": "string"
        },
        "EntityType": {
          "title": "Entitytype",
          "type": "string"
        }
      },
      "required": [
        "Identifier",
        "EntityType"
      ],
      "title": "TargetEntity",
      "type": "object"
    }
  },
  "required": [
    "case_id",
    "alert_group_identifiers"
  ],
  "title": "forti_analyzer_enrich_entitiesArguments"
}
```

**Returns:** `dict` - A dictionary containing the result of the action execution.
