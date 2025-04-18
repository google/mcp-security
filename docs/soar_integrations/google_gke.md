# Google Kubernetes Engine (GKE)

## Overview

This integration provides tools to interact with Google Kubernetes Engine (GKE) for managing clusters, node pools, addons, labels, and operations.

## Available Tools

### List Node Pools

**Tool Name:** `google_gke_list_node_pools`

**Description:** List node pools for the Google Kubernetes Engine cluster based on the specified search criteria. Note that action is not working on Siemplify entities. Additionally, filtering logic is working based on the node pool name field.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `cluster_location` (string, required): Specify Google Compute Engine location in which to search for clusters in. Example: europe-central2-a.
*   `cluster_name` (string, required): Specify Google Kubernetes Engine cluster name.
*   `project_id` (string, optional): Specify the name of the project in which to search for clusters in. If nothing is provided, the project will be extracted from integration configuration. Defaults to None.
*   `filter_logic` (List[Any], optional): Specify what filter logic should be applied. Filtering logic is working based on the node pool name field. Defaults to None.
*   `filter_value` (string, optional): Specify what value should be used in the filter. If "Equal" is selected, action should will try to find the exact match among results and if "Contains" is selected, action will try to find results that contain the substring. If nothing is provided in this parameter, the filter will not be applied. Filtering logic is working based on the node pool name field. Defaults to None.
*   `max_records_to_return` (string, optional): Specify how many records to return. Defaults to None.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on. Defaults to empty list.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the result of the action execution.

---

### Set Cluster Addons

**Tool Name:** `google_gke_set_cluster_addons`

**Description:** Create an operation to set addons for the Google Kubernetes Engine cluster. Action is async. Note that action is not working on Siemplify entities. Additionally, if the target cluster is already going under configuration change, new configuration changes will not be accepted until current configuration changes finish.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `cluster_location` (string, required): Specify Google Compute Engine location in which to search for clusters in. Example: europe-central2-a.
*   `cluster_name` (string, required): Specify Google Kubernetes Engine cluster name.
*   `project_id` (string, optional): Specify the name of the project in which to search for clusters in. If nothing is provided, the project will be extracted from integration configuration. Defaults to None.
*   `http_load_balancing` (List[Any], optional): Specify the value for the HTTP Load Balancing addon configuration. Defaults to None.
*   `horizontal_pod_autoscaling` (List[Any], optional): Specify the value for the Horizontal Pod Autoscaling addon configuration. Defaults to None.
*   `network_policy_config` (List[Any], optional): Specify the value for the Network Policy Config addon configuration. Defaults to None.
*   `cloud_run_config` (List[Any], optional): Specify the value for the Cloud Run Config addon configuration. Defaults to None.
*   `dns_cache_config` (List[Any], optional): Specify the value for the DNS Cache Config addon configuration. Defaults to None.
*   `config_connector_config` (List[Any], optional): Specify the value for the Config Connector Config addon. Defaults to None.
*   `gce_persistent_disk_csi_driver_config` (List[Any], optional): Specify the value for the GCE Persistent Disk Csi Driver Config addon. Defaults to None.
*   `wait_for_cluster_configuration_change_operation_to_finish` (boolean, optional): If enabled, action will wait for the results of the cluster configuration change operation. Defaults to None.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on. Defaults to empty list.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the result of the action execution.

---

### List Operations

**Tool Name:** `google_gke_list_operations`

**Description:** List Google Kubernetes Engine operations for a location based on the specified search criteria. Note that action is not working on Siemplify entities. Additionally, filtering logic is working based on the operation name field.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `location` (string, required): Specify Google Compute Engine location for which to fetch the operations for. Example: europe-central2-a.
*   `project_id` (string, optional): Specify the name of the project for which to fetch the operations for. If nothing is provided, the project will be extracted from integration configuration. Defaults to None.
*   `filter_logic` (List[Any], optional): Specify what filter logic should be applied. Defaults to None.
*   `filter_value` (string, optional): Specify what value should be used in the filter. If "Equal" is selected, action should will try to find the exact match among results and if "Contains" is selected, action will try to find results that contain the substring. If nothing is provided in this parameter, the filter will not be applied. Filtering logic is working based on the operation name field. Defaults to None.
*   `max_records_to_return` (string, optional): Specify how many records to return. Default: 50. Defaults to None.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on. Defaults to empty list.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the result of the action execution.

---

### Set Node Pool Management

**Tool Name:** `google_gke_set_node_pool_management`

**Description:** Create an operation to set node pool management configuration for the Google Kubernetes Engine cluster. Action is async. Note that action is not working on Siemplify entities. Additionally, if the target cluster is already going under configuration change, new configuration changes will not be accepted until current configuration changes finish.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `cluster_location` (string, required): Specify Google Compute Engine location in which to search for clusters in. Example: europe-central2-a.
*   `cluster_name` (string, required): Specify Google Kubernetes Engine cluster name.
*   `node_pool_name` (string, required): Specify node pool name for the Google Kubernetes Engine cluster.
*   `project_id` (string, optional): Specify the name of the project in which to search for clusters in. If nothing is provided, the project will be extracted from integration configuration. Defaults to None.
*   `auto_upgrade` (List[Any], optional): Specify the status of auto upgrade management feature. Defaults to None.
*   `auto_repair` (List[Any], optional): Specify the status of auto repair management feature. Defaults to None.
*   `wait_for_cluster_configuration_change_operation_to_finish` (boolean, optional): If enabled, action will wait for the results of the cluster configuration change operation. Defaults to None.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on. Defaults to empty list.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the result of the action execution.

---

### Ping

**Tool Name:** `google_gke_ping`

**Description:** Test connectivity to the Google Kubernetes Engine service with parameters provided at the integration configuration page on the Marketplace tab.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on. Defaults to empty list.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the result of the action execution.

---

### Set Cluster Labels

**Tool Name:** `google_gke_set_cluster_labels`

**Description:** Create an operation to set labels for the Google Kubernetes Engine cluster. Action is async. Action appends new labels to any existing cluster labels. Note that action is not working on Siemplify entities. Additionally, if the target cluster is already going under configuration change, new configuration changes will not be accepted until current configuration changes finish.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `cluster_location` (string, required): Specify Google Compute Engine location in which to search for clusters in. Example: europe-central2-a.
*   `cluster_name` (string, required): Specify Google Kubernetes Engine cluster name.
*   `cluster_labels` (string, required): Specify a JSON object that contains labels to add to the cluster. Please consider default value for the format reference. Action appends new labels to any existing cluster labels.
*   `project_id` (string, optional): Specify the name of the project in which to search for clusters in. If nothing is provided, the project will be extracted from integration configuration. Defaults to None.
*   `wait_for_cluster_configuration_change_operation_to_finish` (boolean, optional): If enabled, action will wait for the results of the cluster configuration change operation. Defaults to None.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on. Defaults to empty list.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the result of the action execution.

---

### Get Operation Status

**Tool Name:** `google_gke_get_operation_status`

**Description:** Get the Google Kubernetes Engine operation status. Action is async. Note that action is not working on Siemplify entities.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `location` (string, required): Specify Google Compute Engine location for which to fetch operation status for. Example: europe-central2-a.
*   `operation_name` (string, required): Specify Google Compute Engine operation to fetch.
*   `project_id` (string, optional): Specify the name of the project for which to fetch operation status for. If nothing is provided, the project will be extracted from integration configuration. Defaults to None.
*   `wait_for_cluster_configuration_change_operation_to_finish` (boolean, optional): If enabled, action will wait for the results of the cluster configuration change operation. Defaults to None.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on. Defaults to empty list.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the result of the action execution.

---

### List Clusters

**Tool Name:** `google_gke_list_clusters`

**Description:** List Google Kubernetes Engine clusters based on the specified search criteria. Note that action is not working on Siemplify entities. Additionally, filtering logic is working based on the cluster name field.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `cluster_location` (string, required): Specify Google Compute Engine location in which to search for clusters in. Example: europe-central2-a.
*   `project_id` (string, optional): Specify the name of the project in which to search for clusters in. If nothing is provided, the project will be extracted from integration configuration. Defaults to None.
*   `filter_logic` (List[Any], optional): Specify what filter logic should be applied. Filtering logic is working based on the cluster name field. Defaults to None.
*   `filter_value` (string, optional): Specify what value should be used in the filter. If "Equal" is selected, action should will try to find the exact match among results and if "Contains" is selected, action will try to find results that contain the substring. If nothing is provided in this parameter, the filter will not be applied. Filtering logic is working based on the cluster name field. Defaults to None.
*   `max_records_to_return` (string, optional): Specify how many records to return. Defaults to None.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on. Defaults to empty list.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the result of the action execution.

---

### Set Node Autoscaling

**Tool Name:** `google_gke_set_node_autoscaling`

**Description:** Create an operation to set node pool autoscaling configuration for the Google Kubernetes Engine cluster. Action is async. Note that action is not working on Siemplify entities. Additionally, if the target cluster is already going under configuration change, new configuration changes will not be accepted until current configuration changes finish.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `cluster_location` (string, required): Specify Google Compute Engine location in which to search for clusters in. Example: europe-central2-a.
*   `cluster_name` (string, required): Specify Google Kubernetes Engine cluster name.
*   `node_pool_name` (string, required): Specify node pool name for the Google Kubernetes Engine cluster.
*   `project_id` (string, optional): Specify the name of the project in which to search for clusters in. If nothing is provided, the project will be extracted from integration configuration. Defaults to None.
*   `autoscaling_mode` (List[Any], optional): Specify autoscaling mode status for the node pool. Defaults to None.
*   `minimum_node_count` (string, optional): Specify minimum node count for the node pool configuration. Defaults to None.
*   `maximum_node_count` (string, optional): Specify maximum node count for the node pool configuration. Defaults to None.
*   `wait_for_cluster_configuration_change_operation_to_finish` (boolean, optional): If enabled, action will wait for the results of the cluster configuration change operation. Defaults to None.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on. Defaults to empty list.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the result of the action execution.

---

### Set Node Count

**Tool Name:** `google_gke_set_node_count`

**Description:** Create an operation to set node count for the Google Kubernetes Engine cluster node pool. Action is async. Note that action is not working on Siemplify entities. Additionally, if the target cluster is already going under configuration change, new configuration changes will not be accepted until current configuration changes finish.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `cluster_location` (string, required): Specify Google Compute Engine location in which to search for clusters in. Example: europe-central2-a.
*   `cluster_name` (string, required): Specify Google Kubernetes Engine cluster name.
*   `node_pool_name` (string, required): Specify node pool name for the Google Kubernetes Engine cluster.
*   `node_count` (string, required): Specify node count for the Google Kubernetes Engine cluster node pool.
*   `project_id` (string, optional): Specify the name of the project in which to search for clusters in. If nothing is provided, the project will be extracted from integration configuration. Defaults to None.
*   `wait_for_cluster_configuration_change_operation_to_finish` (boolean, optional): If enabled, action will wait for the results of the cluster configuration change operation. Defaults to None.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on. Defaults to empty list.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the result of the action execution.
