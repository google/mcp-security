# Google Cloud Recommender

## Overview

This integration provides tools to interact with the Google Cloud Recommender service for listing, getting, updating, and applying recommendations, particularly focusing on IAM policy recommendations.

## Available Tools

### Get Recommendation

**Tool Name:** `google_cloud_recommender_get_recommendation`

**Description:** Get specific recommendation from the Google Cloud Recommender service. Note 1: This action doesn’t run on Chronicle SOAR entities.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `recommendation_name` (string, required): Specify the recommendation name to return. Action accepts multiple values as a comma separated string. Example of expected input: projects/projectname/locations/global/recommenders/google.iam.policy.Recommender/recommendations/0f262740-bf4a-4c3d-9573-0da3345cf3f7.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on. Defaults to empty list.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the result of the action execution.

---

### Ping

**Tool Name:** `google_cloud_recommender_ping`

**Description:** Test connectivity to the Google Recommender service with parameters provided at the integration configuration page on the Marketplace tab.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on. Defaults to empty list.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the result of the action execution.

---

### Apply IAM Recommendations

**Tool Name:** `google_cloud_recommender_apply_iam_recommendations`

**Description:** Apply IAM Recommendations based on provided input. Action works only with google.iam.policy.Recommender recommendations.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `iam_recommendations_json` (Union[str, dict], required): Specify the JSON of the recommendation to apply to. JSON can be provided as a placeholder from “List Recommendations” or “Get Recommendation” actions.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on. Defaults to empty list.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the result of the action execution.

---

### List Recommendations

**Tool Name:** `google_cloud_recommender_list_recommendations`

**Description:** List available recommendations in the Google Cloud Recommender service. Note 1: This action doesn’t run on Chronicle SOAR entities. Note 2: Currently action returns insights only from google.iam.policy.Recommender recommender.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `recommendation_location` (string, required): Specify the GCP location to fetch recommendations for.
*   `recommendation_filter` (string, optional): Specify the filter to fetch the recommendations for. Parameter expects a string of a format "<projects or organizations>/<project or organization name or id>" or "//cloudresourcemanager.googleapis.com/<projects or organizations>/<project or organization name or id>" for which to fetch the recommendations for. If nothing is provided - action will take the project id from the service account configured. Defaults to None.
*   `recommendation_state` (List[Any], optional): Specify the recommendation state to return. Defaults to None.
*   `recommendation_priority` (string, optional): Specify the recommender priority to return, multiple values can be specified as a comma separated string. Defaults to None.
*   `recommender_subtype` (List[Any], optional): Specify the recommender subtype to return. Defaults to None.
*   `max_records_to_return` (string, optional): Specify how many records to return. If nothing is provided, action will return 50 records. Defaults to None.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on. Defaults to empty list.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the result of the action execution.

---

### Update Recommendation

**Tool Name:** `google_cloud_recommender_update_recommendation`

**Description:** Update recommendation in the Google Cloud Recommender service. Note 1: This action doesn’t run on Chronicle SOAR entities.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `recommendation_name` (string, required): Specify the recommendation name to update. Action accepts multiple values as a comma separated string. Example of expected input: projects/projectname/locations/global/recommenders/google.iam.policy.Recommender/recommendations/0f262740-bf4a-4c3d-9573-0da3345cf3f7.
*   `recommendation_state` (List[Any], optional): Specify the state for the recommendation to change to. Defaults to None.
*   `recommendation_result` (List[Any], optional): Specify the result for the recommendation to change to. Defaults to None.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on. Defaults to empty list.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the result of the action execution.
