# Google Cloud Compute

## Overview

This integration provides tools to interact with Google Cloud Compute Engine for managing virtual machine instances, firewall rules, network tags, labels, and IAM policies.

## Available Tools

### Remove IP From Firewall Rule

**Tool Name:** `google_cloud_compute_remove_ip_from_firewall_rule`

**Description:** Remove IP from firewall rule in Google Cloud Compute instance. Note: Action is running as async, please adjust script timeout value in Google SecOps IDE for action, as needed.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `type` (List[Any], required): Type of the IP range that will be removed.
*   `ip_ranges` (string, required): List of IP ranges that needs to be removed from the Firewall Rule.
*   `resource_name` (string, optional): Specify the full resource name for the firewall rule. Format: projects/{project_id}/global/firewalls/{firewall}. This parameter has higher priority over the combination of "Project ID", and "Firewall Rule". Defaults to None.
*   `project_id` (string, optional): Specify the name of the project of your firewall rule. If nothing is provided, the project will be extracted from integration configuration. Defaults to None.
*   `firewall_rule` (string, optional): Specify firewall rule name to update. Defaults to None.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on. Defaults to empty list.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the result of the action execution.

---

### Add Labels To Instance

**Tool Name:** `google_cloud_compute_add_labels_to_instance`

**Description:** Add labels to the Google Cloud Compute Instance.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `instance_labels` (string, required): Specify instance lables to add to instance. Lables should be provided in the following format - label_key_name:label_value, for example: vm_label_key:label1. Parameter accepts multiple values as a comma separated string.
*   `resource_name` (string, optional): Specify the full resource name for the compute instance. Format: /projects/{project_id}/zones/{zone id}/instances/{instance id}. This parameter has higher priority over the combination of "Project ID", "Instance Zone" and "Instance ID". Defaults to None.
*   `project_id` (string, optional): Specify the name of the project of your compute instance. If nothing is provided, the project will be extracted from integration configuration. Defaults to None.
*   `instance_zone` (string, optional): Specify instance zone name to search for instances in. Defaults to None.
*   `instance_id` (string, optional): Specify instance id to add labels to. Instance id can be found with the "List Instances" action. Defaults to None.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on. Defaults to empty list.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the result of the action execution.

---

### List Instances

**Tool Name:** `google_cloud_compute_list_instances`

**Description:** List Google Cloud Compute instances based on the specified search criteria. Note that action is not working on Siemplify entities.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `project_id` (string, optional): Specify the name of the project of your compute instance. If nothing is provided, the project will be extracted from integration configuration. Defaults to None.
*   `instance_zone` (string, optional): Specify instance zone name to search for instances in. Defaults to None.
*   `instance_name` (string, optional): Specify instance name to search for. Parameter accepts multiple values as a comma separated string. Defaults to None.
*   `instance_status` (string, optional): Specify instance status to search for. Parameter accepts multiple values as a comma separated string. Defaults to None.
*   `instance_labels` (string, optional): Specify instance labels to search for in the format label_key_name:label_value, for example vm_label_key:label1. Parameter accepts multiple values as a comma separated string. Defaults to None.
*   `max_rows_to_return` (string, optional): Specify how many instances action should return. Defaults to None.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on. Defaults to empty list.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the result of the action execution.

---

### Delete Instance

**Tool Name:** `google_cloud_compute_delete_instance`

**Description:** Delete the specified Google Cloud Compute instance.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `resource_name` (string, optional): Specify the full resource name for the compute instance. Format: /projects/{project_id}/zones/{zone id}/instances/{instance id}. This parameter has higher priority over the combination of "Project ID", "Instance Zone" and "Instance ID". Defaults to None.
*   `project_id` (string, optional): Specify the name of the project of your compute instance. If nothing is provided, the project will be extracted from integration configuration. Defaults to None.
*   `instance_zone` (string, optional): Specify instance zone name to search for instances in. Defaults to None.
*   `instance_id` (string, optional): Specify instance id to delete. Instance id can be found in "List Instances" action. Defaults to None.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on. Defaults to empty list.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the result of the action execution.

---

### Start Instance

**Tool Name:** `google_cloud_compute_start_instance`

**Description:** Start a previously stopped Google Cloud Compute Instance. Note that it can take a few minutes for the instance to enter the running status.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `resource_name` (string, optional): Specify the full resource name for the compute instance. Format: /projects/{project_id}/zones/{zone id}/instances/{instance id}. This parameter has higher priority over the combination of "Project ID", "Instance Zone" and "Instance ID". Defaults to None.
*   `project_id` (string, optional): Specify the name of the project of your compute instance. If nothing is provided, the project will be extracted from integration configuration. Defaults to None.
*   `instance_zone` (string, optional): Specify instance zone name to search for instances in. Defaults to None.
*   `instance_id` (string, optional): Specify instance id to start. Instance id can be found in "List Instances" action. Defaults to None.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on. Defaults to empty list.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the result of the action execution.

---

### Execute VM Patch Job

**Tool Name:** `google_cloud_compute_execute_vm_patch_job`

**Description:** Execute a VM patch job on Compute Engine instances. This action is asynchronous. Adjust the script timeout value in the Google SecOps IDE for the action as needed. This action requires you to enable the OS Config API.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `instance_filter_object` (string, required): A JSON object to set an instance filter.
*   `name` (string, required): The name for the patching job.
*   `patch_duration_timeout` (string, required): The timeout value in minutes for a patching job.
*   `disruption_budget` (string, required): The disruption budget for a patching job. You can use a specific number or a percentage like 10%.
*   `description` (string, optional): The description for the patching job. Defaults to None.
*   `patching_config_object` (string, optional): A JSON object that specifies the steps for the patching job to execute. If you don’t set a value, the action patches Compute Engine instances using the default value. To configure this parameter, use the following format: {"key": "value"}. Defaults to None.
*   `rollout_strategy` (List[Any], optional): The rollout strategy for a patching job. Defaults to None.
*   `wait_for_completion` (boolean, optional): If selected, the action waits for the patching job to complete. Defaults to None.
*   `fail_if_completed_with_errors` (boolean, optional): If selected and the patching job status is “Completed with errors” or the action reaches a timeout, the action fails. If you didn’t select the “Wait For Completion” parameter, the action ignores this parameter. Defaults to None.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on. Defaults to empty list.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the result of the action execution.

---

### Add Network Tags

**Tool Name:** `google_cloud_compute_add_network_tags`

**Description:** Add network tags to the Compute Engine instance. This action is asynchronous. Adjust the script timeout value in the Google SecOps IDE for the action as needed.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `network_tags` (string, required): A comma-separated list of network tags to add to the Compute Engine instance. This parameter only accepts tags that contain lowercase letters, numbers, and hyphens.
*   `resource_name` (string, optional): The full resource name for the Compute Engine instance, such as /projects/{project_id}/zones/{zone id}/instances/{instance id}. This parameter has a priority over the “Project ID”, “Instance Zone”, and “Instance ID” parameters. Defaults to None.
*   `project_id` (string, optional): The project name of the Compute Engine instance. If you don’t set a value,, the action retrieves the project name from the integration configuration. Defaults to None.
*   `instance_zone` (string, optional): The zone name of the Compute Engine instance. This parameter is required if you configure the Compute Engine instance using the “Instance Zone” and “Instance ID” parameters. Defaults to None.
*   `instance_id` (string, optional): The Compute Engine instance ID. This parameter is required if you configure the Compute Engine instance using the “Instance Zone” and “Instance ID” parameters. Defaults to None.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on. Defaults to empty list.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the result of the action execution.

---

### Get Instance IAM Policy

**Tool Name:** `google_cloud_compute_get_instance_iam_policy`

**Description:** Gets the access control policy for the resource. Note that policy may be empty if no policy is assigned to the resource.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `resource_name` (string, optional): Specify the full resource name for the compute instance. Format: /projects/{project_id}/zones/{zone id}/instances/{instance id}. This parameter has higher priority over the combination of "Project ID", "Instance Zone" and "Instance ID". Defaults to None.
*   `project_id` (string, optional): Specify the name of the project of your compute instance. If nothing is provided, the project will be extracted from integration configuration. Defaults to None.
*   `instance_zone` (string, optional): Specify instance zone name to search for instances in. Defaults to None.
*   `instance_id` (string, optional): Specify instance id to get policy for. Intsance id can be found in "List Instances" action. Defaults to None.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on. Defaults to empty list.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the result of the action execution.

---

### Ping

**Tool Name:** `google_cloud_compute_ping`

**Description:** Test connectivity to the Google Cloud Compute service with parameters provided at the integration configuration page on the Marketplace tab.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on. Defaults to empty list.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the result of the action execution.

---

### Remove External IP Addresses

**Tool Name:** `google_cloud_compute_remove_external_ip_addresses`

**Description:** Remove external IP addresses on a Google Cloud Compute instance. Note: Action is running as async, please adjust script timeout value in Google SecOps IDE for action, as needed.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `resource_name` (string, optional): Specify the full resource name for the compute instance. Format: projects/{project_id}/zones/{zone_id}/instances/{instance_id}. This parameter has higher priority over the combination of "Project ID", "Instance Zone" and "Instance ID". Defaults to None.
*   `project_id` (string, optional): Specify the name of the project of your compute instance. If nothing is provided, the project will be extracted from integration configuration. Defaults to None.
*   `instance_zone` (string, optional): Specify instance zone name to search for instances in. Defaults to None.
*   `instance_id` (string, optional): Specify instance id to modify. Instance id can be found in "List Instances" action. Defaults to None.
*   `network_interfaces` (string, optional): Specify a comma-separated list of network interfaces to modify. If this parameter is left empty or “*” is provided then all of the network interfaces will be updated. Defaults to None.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on. Defaults to empty list.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the result of the action execution.

---

### Remove Network Tags

**Tool Name:** `google_cloud_compute_remove_network_tags`

**Description:** Remove network tags from the Compute Engine instance. This action is asynchronous. Adjust the sript timeout value in the Google SecOps IDE for the action as needed.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `network_tags` (string, required): A comma-separated list of network tags to remove from the Compute Engine instance. This parameter only accepts tags that contain lowercase letters, numbers, and hyphens.
*   `resource_name` (string, optional): The full resource name for the Compute Engine instance, such as /projects/{project_id}/zones/{zone id}/instances/{instance id}. This parameter has a priority over the “Project ID”, “Instance Zone”, and “Instance ID” parameters. Defaults to None.
*   `project_id` (string, optional): The project name of your Compute Engine instance. If you don’t set a value, the action retrieves the project name from the integration configuration. Defaults to None.
*   `instance_zone` (string, optional): The zone name of the Compute Engine instance. This parameter is required if you configure the Compute Engine instance using the “Instance Zone” and “Instance ID” parameters. Defaults to None.
*   `instance_id` (string, optional): The Compute Engine instance ID. This parameter is required if you configure the Compute Engine instance using the “Instance Zone” and “Instance ID” parameters. Defaults to None.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on. Defaults to empty list.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the result of the action execution.

---

### Set Instance IAM Policy

**Tool Name:** `google_cloud_compute_set_instance_iam_policy`

**Description:** Sets the access control policy on the specified resource. Note that policy provided in action replaces any existing policy.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `policy` (string, required): Specify JSON policy document to set for instance.
*   `resource_name` (string, optional): Specify the full resource name for the compute instance. Format: /projects/{project_id}/zones/{zone id}/instances/{instance id}. This parameter has higher priority over the combination of "Project ID", "Instance Zone" and "Instance ID". Defaults to None.
*   `project_id` (string, optional): Specify the name of the project of your compute instance. If nothing is provided, the project will be extracted from integration configuration. Defaults to None.
*   `instance_zone` (string, optional): Specify instance zone name to search for instances in. Defaults to None.
*   `instance_id` (string, optional): Specify instance id to set policy for. Intsance id can be found in "List Instances" action. Defaults to None.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on. Defaults to empty list.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the result of the action execution.

---

### Enrich Entities

**Tool Name:** `google_cloud_compute_enrich_entities`

**Description:** Enrich Siemplify IP entities with instance information from Google Cloud Compute.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `project_id` (string, optional): Specify the name of the project of your compute instance. If nothing is provided, the project will be extracted from integration configuration. Defaults to None.
*   `instance_zone` (string, optional): Specify instance zone name to search for instances in. Defaults to None.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on. Defaults to empty list.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the result of the action execution.

---

### Update Firewall Rule

**Tool Name:** `google_cloud_compute_update_firewall_rule`

**Description:** Update a firewall rule with given parameters in Google Cloud Compute. Note: Action is running as async, please adjust script timeout value in Google SecOps IDE for action, as needed.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `resource_name` (string, optional): Specify the full resource name for the firewall rule. Format: projects/{project_id}/global/firewalls/{firewall}. This parameter has higher priority over the combination of "Project ID", and "Firewall Rule". Defaults to None.
*   `project_id` (string, optional): Specify the name of the project of your firewall rule. If nothing is provided, the project will be extracted from integration configuration. Defaults to None.
*   `firewall_rule` (string, optional): Specify firewall rule name to update. Defaults to None.
*   `source_ip_ranges` (string, optional): Specify a comma-separated list of source IP ranges. Parameter supports 'none' value. If "none" value is provided, then the action will delete existing values for the firewall rule. If nothing is provided for the parameter, action will not update the existing value. Defaults to None.
*   `source_tags` (string, optional): Specify a comma-separated list of source tags. Parameter supports 'none' value. If "none" value is provided, then the action will delete existing values for the firewall rule. If nothing is provided for the parameter, action will not update the existing value. Defaults to None.
*   `source_service_accounts` (string, optional): Specify a comma-separated list of source service accounts. Parameter supports 'none' value. If "none" value is provided, then the action will delete existing values for the firewall rule. If nothing is provided for the parameter, action will not update the existing value. Defaults to None.
*   `tcp_ports` (string, optional): Specify a comma-separated list of TCP ports. If specified, action will use it to update determine allow / deny lists. Parameter supports 'all' and 'none' values. Defaults to None.
*   `udp_ports` (string, optional): Specify a comma-separated list of UDP ports. If specified, action will use it to update determine allow / deny lists. Parameter supports 'all' and 'none' values. Defaults to None.
*   `other_protocols` (string, optional): Specify a comma-separated list of other protocols. Parameter supports 'none' value. If 'all' specified, the action will allow all protocols including tcp and udp. Defaults to None.
*   `destination_ip_ranges` (string, optional): Specify a comma-separated list of destination IP ranges. Parameter supports 'none' value. If "none" value is provided, then the action will delete existing values for the firewall rule. If nothing is provided for the parameter, action will not update the existing value. Defaults to None.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on. Defaults to empty list.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the result of the action execution.

---

### Add IP To Firewall Rule

**Tool Name:** `google_cloud_compute_add_ip_to_firewall_rule`

**Description:** Add IP range to firewall rule in Google Cloud Compute instance. Note: Action is running as async, please adjust script timeout value in Google SecOps IDE for action, as needed.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `type` (List[Any], required): Type of the IP range that will be added.
*   `ip_ranges` (string, required): List of IP ranges that needs to be added to the Firewall Rule.
*   `resource_name` (string, optional): Specify the full resource name for the firewall rule. Format: projects/{project_id}/global/firewalls/{firewall}. This parameter has higher priority over the combination of "Project ID", and "Firewall Rule". Defaults to None.
*   `project_id` (string, optional): Specify the name of the project of your firewall rule. If nothing is provided, the project will be extracted from integration configuration. Defaults to None.
*   `firewall_rule` (string, optional): Specify firewall rule name to update. Defaults to None.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on. Defaults to empty list.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the result of the action execution.

---

### Stop Instance

**Tool Name:** `google_cloud_compute_stop_instance`

**Description:** Stops a running instance, shutting it down cleanly, and allows you to restart the instance at a later time. Stopped instances do not incur VM usage charges while they are stopped. However, resources that the VM is using, such as persistent disks and static IP addresses, will continue to be charged until they are deleted.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `resource_name` (string, optional): Specify the full resource name for the compute instance. Format: /projects/{project_id}/zones/{zone id}/instances/{instance id}. This parameter has higher priority over the combination of "Project ID", "Instance Zone" and "Instance ID". Defaults to None.
*   `project_id` (string, optional): Specify the name of the project of your compute instance. If nothing is provided, the project will be extracted from integration configuration. Defaults to None.
*   `instance_zone` (string, optional): Specify instance zone name to search for instances in. Defaults to None.
*   `instance_id` (string, optional): Specify instance id to stop. Instance id can be found in "List Instances" action. Defaults to None.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on. Defaults to empty list.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the result of the action execution.
