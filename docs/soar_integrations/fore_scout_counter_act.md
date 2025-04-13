# ForeScout CounterACT

## Overview

This integration provides tools to interact with ForeScout CounterACT.

## Available Tools

### Ping

**Tool Name:** `fore_scout_counter_act_ping`

**Description:** Test connectivity to the ForeScout CounterACT with parameters provided at the integration configuration page on the Marketplace tab.

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
  "title": "fore_scout_counter_act_pingArguments"
}
```

**Returns:** `dict` - A dictionary containing the result of the action execution.

---

### Enrich Entities

**Tool Name:** `fore_scout_counter_act_enrich_entities`

**Description:** Enrich entities using information from ForeScout CounterACT. Supported entities: IP, Mac Address.

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
    "create_insight": {
      "anyOf": [
        {
          "type": "boolean"
        },
        {
          "type": "null"
        }
      ],
      "default": null,
      "description": "If enabled, action will create insights containing enrichment information.",
      "title": "Create Insight"
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
  "title": "fore_scout_counter_act_enrich_entitiesArguments"
}
```

**Returns:** `dict` - A dictionary containing the result of the action execution.
