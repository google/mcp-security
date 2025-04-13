# AWSEC2 SOAR Integration

This document details the tools provided by the AWSEC2 SOAR integration.

## Tools

### `awsec2_terminate_instance`

When you've decided that you no longer need an instance, you can terminate it. Terminated instances cannot be started. Notice that you can only terminate instance store-backed instances.  For more information about instance store-backed instances, see https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/ComponentsAMIs.html#storage-for-the-root-device

**Parameters:**

*   `case_id` (str, required): The ID of the case.
*   `alert_group_identifiers` (List[str], required): Identifiers for the alert groups.
*   `instance_i_ds` (str, required): One or more instance IDs. Separated by comma.
*   `target_entities` (List[TargetEntity], optional, default=[]): Optional list of specific target entities (Identifier, EntityType) to run the action on.
*   `scope` (str, optional, default="All entities"): Defines the scope for the action.

### `awsec2_list_instances`

Describes the specified instances or all instances.

**Parameters:**

*   `case_id` (str, required): The ID of the case.
*   `alert_group_identifiers` (List[str], required): Identifiers for the alert groups.
*   `instance_i_ds` (Optional[str], optional, default=None): One or more instance IDs. specify instance IDs, the output includes information for only the specified instances. Please note that the parameter ‘Instance IDs’ cannot be used with the parameter ‘Max Results’. ‘Instance IDs’ has priority over the ‘Max Result’ parameter.
*   `tag_filters` (Optional[str], optional, default=None): The key/value combination of a tag assigned to the resource. For example, to find all resources that have a tag with the key Owner and the value TeamA , specify Owner:TeamA. Comma separated tag filters. E.g. Name:Name1,Owner:TeamA. Returned instances will be fit to all filters.
*   `max_results` (Optional[str], optional, default=None): Specify how many instances to return. Default is 50. Maximum is 1000. Please note that the parameters ‘Security Group IDs’ and ‘Security Group Names’ cannot be used with the parameter ‘Max Results’. ‘Security Group IDs’ has priority over the ‘Max Result’ parameter.
*   `target_entities` (List[TargetEntity], optional, default=[]): Optional list of specific target entities (Identifier, EntityType) to run the action on.
*   `scope` (str, optional, default="All entities"): Defines the scope for the action.

### `awsec2_take_snapshot`

Take snapshot of the instance

**Parameters:**

*   `case_id` (str, required): The ID of the case.
*   `alert_group_identifiers` (List[str], required): Identifiers for the alert groups.
*   `instance_id` (str, required): Instance ID. Specify the instance ID
*   `description` (Optional[str], optional, default=None): Specify the description of the snapshot
*   `target_entities` (List[TargetEntity], optional, default=[]): Optional list of specific target entities (Identifier, EntityType) to run the action on.
*   `scope` (str, optional, default="All entities"): Defines the scope for the action.

### `awsec2_revoke_security_group_egress`

Removes the specified egress rules (outbound rules) from a security group for use with a VPC. This action does not apply to security groups for use in EC2-Classic. To remove a rule, the values that you specify (for example, ports) must match the existing rule's values exactly. Rule changes are propagated to affected instances as quickly as possible. However, a small delay might occur. For more information about VPC security group limits, see https://docs.aws.amazon.com/vpc/latest/userguide/amazon-vpc-limits.html

**Parameters:**

*   `case_id` (str, required): The ID of the case.
*   `alert_group_identifiers` (List[str], required): Identifiers for the alert groups.
*   `security_group_i_ds` (str, required): One or more security group IDs. Separated by comma.
*   `ip_protocol` (Optional[List[Any]], optional, default=None): The IP protocol name. Use “all” to specify all protocols. Specifying “all” allows traffic on all ports, regardless of any port range you specify.
*   `from_port` (Optional[str], optional, default=None): The start of port range for the TCP and UDP protocols, or an ICMP type number.
*   `to_port` (Optional[str], optional, default=None): The end of port range for the TCP and UDP protocols allows traffic on all ports, regardless of any port range you specify.
*   `ip_ranges_cidr_ip` (Optional[str], optional, default=None): The IPv4 CIDR range. To specify a single IPv4 address, use the /32 prefix length.
*   `i_pv6_ranges_cidr_ip` (Optional[str], optional, default=None): The IPv6 CIDR range. To specify a single IPv6 address, use the /128 prefix length.
*   `target_entities` (List[TargetEntity], optional, default=[]): Optional list of specific target entities (Identifier, EntityType) to run the action on.
*   `scope` (str, optional, default="All entities"): Defines the scope for the action.

### `awsec2_authorize_security_group_ingress`

Adds the specified ingress rule to a security group. An inbound rule permits instances to receive traffic from the specified IPv4 or IPv6 CIDR address ranges. Rule changes are propagated to affected instances as quickly as possible. However, a small delay might occur. For more information about VPC security group limits, see https://docs.aws.amazon.com/vpc/latest/userguide/amazon-vpc-limits.html

**Parameters:**

*   `case_id` (str, required): The ID of the case.
*   `alert_group_identifiers` (List[str], required): Identifiers for the alert groups.
*   `security_group_i_ds` (str, required): One or more security group IDs. Separated by comma.
*   `ip_protocol` (Optional[List[Any]], optional, default=None): The IP protocol name. Use "all" to specify all protocols. Specifying "all" allows traffic on all ports, regardless of any port range you specify.
*   `from_port` (Optional[str], optional, default=None): The start of port range for the TCP and UDP protocols, or an ICMP type number.
*   `to_port` (Optional[str], optional, default=None): The end of port range for the TCP and UDP protocols allows traffic on all ports, regardless of any port range you specify.
*   `ip_ranges_cidr_ip` (Optional[str], optional, default=None): The IPv4 CIDR range. To specify a single IPv4 address, use the /32 prefix length.
*   `i_pv6_ranges_cidr_ip` (Optional[str], optional, default=None): The IPv6 CIDR range. To specify a single IPv6 address, use the /128 prefix length.
*   `target_entities` (List[TargetEntity], optional, default=[]): Optional list of specific target entities (Identifier, EntityType) to run the action on.
*   `scope` (str, optional, default="All entities"): Defines the scope for the action.

### `awsec2_revoke_security_group_ingress`

Removes the specified ingress rules (inbound rules) from a security group. To remove a rule, the values that you specify (for example, ports) must match the existing rule's values exactly. Rule changes are propagated to instances within the security group as quickly as possible. However, a small delay might occur.

**Parameters:**

*   `case_id` (str, required): The ID of the case.
*   `alert_group_identifiers` (List[str], required): Identifiers for the alert groups.
*   `security_group_i_ds` (str, required): One or more security group IDs. Separated by comma.
*   `ip_protocol` (Optional[List[Any]], optional, default=None): The IP protocol name. Use "all" to specify all protocols. Specifying "all" allowes traffic on all ports, regardless of any port range you specify.
*   `from_port` (Optional[str], optional, default=None): The start of port range for the TCP and UDP protocols, or an ICMP type number.
*   `to_port` (Optional[str], optional, default=None): The end of port range for the TCP and UDP protocols allows traffic on all ports, regardless of any port range you specify.
*   `ip_ranges_cidr_ip` (Optional[str], optional, default=None): The IPv4 address in  CIDR format. To specify a single IPv4 address, use the /32 prefix length.
*   `i_pv6_ranges_cidr_ip` (Optional[str], optional, default=None): The IPv6 CIDR range. To specify a single IPv6 address, use the /128 prefix length.
*   `target_entities` (List[TargetEntity], optional, default=[]): Optional list of specific target entities (Identifier, EntityType) to run the action on.
*   `scope` (str, optional, default="All entities"): Defines the scope for the action.

### `awsec2_stop_instance`

Stop an Amazon EBS-backed instance. When you stop an instance, we attempt to shut it down forcibly after a short while. It can take a few minutes for the instance to stop. The instance can be started at any time. Notice that you can't stop an instance store-backed instance.  For more information about instance store-backed instances, see https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/ComponentsAMIs.html#storage-for-the-root-device

**Parameters:**

*   `case_id` (str, required): The ID of the case.
*   `alert_group_identifiers` (List[str], required): Identifiers for the alert groups.
*   `instance_i_ds` (str, required): One or more instance IDs. Separated by comma.
*   `force` (Optional[bool], optional, default=None): Forces the instances to stop. The instances do not have an opportunity to flush file system caches or file system metadata. If you use this option, you must perform file system check and repair procedures. This option is not recommended for Windows instances.
*   `target_entities` (List[TargetEntity], optional, default=[]): Optional list of specific target entities (Identifier, EntityType) to run the action on.
*   `scope` (str, optional, default="All entities"): Defines the scope for the action.

### `awsec2_create_tags`

A tag is a label that you assign to an AWS resource. Each tag consists of a key and an optional value. You can use tags to search and filter your resources or track your AWS costs. Adds or overwrites only the specified tags for the specified Amazon EC2 resource or resources. When you specify an existing tag key, the value is overwritten with the new value. Each resource can have a maximum of 50 tags. Tag keys must be unique per resource. For more information about tags, see https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/Using_Tags.html in the Amazon Elastic Compute Cloud User Guide .

**Parameters:**

*   `case_id` (str, required): The ID of the case.
*   `alert_group_identifiers` (List[str], required): Identifiers for the alert groups.
*   `resource_i_ds` (str, required): One or more resource IDs. Separated by comma.
*   `tags` (str, required): The key/value combination of a tag to be assigned to the resource. For example, to add to all specified resources a tag with the key Owner and the value TeamA , specify Owner:TeamA. You can specify multiple key/value combinations by comma separation. You can add or overwrite the specified tags. Please note: tag keys must be unique per resource.
*   `target_entities` (List[TargetEntity], optional, default=[]): Optional list of specific target entities (Identifier, EntityType) to run the action on.
*   `scope` (str, optional, default="All entities"): Defines the scope for the action.

### `awsec2_ping`

Test connectivity to AWS EC2 with parameters provided at the integration configuration page on Marketplace tab.

**Parameters:**

*   `case_id` (str, required): The ID of the case.
*   `alert_group_identifiers` (List[str], required): Identifiers for the alert groups.
*   `target_entities` (List[TargetEntity], optional, default=[]): Optional list of specific target entities (Identifier, EntityType) to run the action on.
*   `scope` (str, optional, default="All entities"): Defines the scope for the action.
