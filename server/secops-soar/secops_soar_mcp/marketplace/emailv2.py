# Copyright 2025 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
from secops_soar_mcp import bindings
from mcp.server.fastmcp import FastMCP
from secops_soar_mcp.utils.consts import Endpoints
from secops_soar_mcp.utils.models import ApiManualActionDataModel, EmailContent, TargetEntity
import json
from typing import Optional, List, Dict, Union, Annotated
from pydantic import Field
from secops_soar_mcp.utils.pydantic_list_field import PydanticListField


def register_tools(mcp: FastMCP):
    # This function registers all tools (actions) for the EmailV2 integration.

    @mcp.tool()
    async def email_v2_send_thread_reply(case_id: Annotated[str, Field(..., description="The ID of the case.")], alert_group_identifiers: Annotated[List[str], Field(..., description="Identifiers for the alert groups.")], message_id: Annotated[str, Field(..., description="Specify the ID of the message to which you want to send a reply.")], folder_name: Annotated[str, Field(..., description="Specify a comma-separated list of mailbox folders in which action should search for email. Note: you can set mail-specific folders, for example, \"[Gmail]/All Mail\" to search in all of the folders of Gmail mailbox. Additionally, folder name should match exactly the IMAP folder. If folder contains spaces, folder must be wrapped in double quotes.")], content: Annotated[EmailContent, Field(..., description="Specify the content of the reply.")], attachment_paths: Annotated[str, Field(default=None, description="Specify a comma separated list of attachments file paths stored on the server for addition to the email.")], reply_all: Annotated[bool, Field(default=None, description="If enabled, action will send a reply to all recipients related to the original email. Note: this parameter has priority over \"Reply To\" parameter.")], reply_to: Annotated[str, Field(default=None, description="Specify a comma-separated list of emails to which you want to send this reply. If nothing is provided and \"Reply All\" is disabled, action will only send a reply to the sender of the email. If \"Reply All\" is enabled, action will ignore this parameter.")], target_entities: Annotated[List[TargetEntity], PydanticListField(TargetEntity, description="Optional list of specific target entities (Identifier, EntityType) to run the action on.")], scope: Annotated[str, Field(default="All entities", description="Defines the scope for the action.")]) -> dict:
        """Send a message as a reply to the email thread.

        Returns:
            dict: A dictionary containing the result of the action execution.
        """
        final_target_entities: Optional[List[TargetEntity]] = None
        final_scope: Optional[str] = None
        is_predefined_scope: Optional[bool] = None
    
        if target_entities:
            # Specific target entities provided, ignore scope parameter
            final_target_entities = target_entities
            final_scope = None
            is_predefined_scope = False
        else:
            # Check if the provided scope is valid
            if scope not in bindings.valid_scopes:
                allowed_values_str = ", ".join(sorted(list(bindings.valid_scopes)))
                return {
                    "Status": "Failed",
                    "Message": f"Invalid scope '{scope}'. Allowed values are: {allowed_values_str}",
                }
            final_target_entities = [] # Pass empty list for entities when using scope
            final_scope = scope
            is_predefined_scope = True
    
        # Fetch integration instance identifier
        try:
            instance_response = await bindings.http_client.get(
                Endpoints.LIST_INTEGRATION_INSTANCES.format(INTEGRATION_NAME="EmailV2")
            )
            instances = instance_response.get("integration_instances", [])
        except Exception as e:
            print(f"Error fetching instance for EmailV2: {e}")
            return {"Status": "Failed", "Message": f"Error fetching instance: {e}"}
    
        if instances:
            instance_identifier = instances[0].get("identifier")
            if not instance_identifier:
                return {"Status": "Failed", "Message": "Instance found but identifier is missing."}
    
            script_params = {}
            script_params["Message ID"] = message_id
            script_params["Folder Name"] = folder_name
            content = content.model_dump()
            script_params["Content"] = content
            if attachment_paths is not None:
                script_params["Attachment Paths"] = attachment_paths
            if reply_all is not None:
                script_params["Reply All"] = reply_all
            if reply_to is not None:
                script_params["Reply To"] = reply_to
    
            # Prepare data model for the API request
            action_data = ApiManualActionDataModel(
                alertGroupIdentifiers=alert_group_identifiers,
                caseId=case_id,
                targetEntities=final_target_entities,
                scope=final_scope,
                isPredefinedScope=is_predefined_scope,
                actionProvider="Scripts",
                actionName="EmailV2_Send Thread Reply",
                properties={
                    "IntegrationInstance": instance_identifier,
                    "ScriptName": "EmailV2_Send Thread Reply",
                    "ScriptParametersEntityFields": json.dumps(script_params)
                }
            )
    
            try:
                execution_response = await bindings.http_client.post(
                    Endpoints.EXECUTE_MANUAL_ACTION,
                    req=action_data.model_dump()
                )
                return execution_response
            except Exception as e:
                print(f"Error executing action EmailV2_Send Thread Reply for EmailV2: {e}")
                return {"Status": "Failed", "Message": f"Error executing action: {e}"}
        else:
            print(f"Warning: No active integration instance found for EmailV2")
            return {"Status": "Failed", "Message": "No active instance found."}

    @mcp.tool()
    async def email_v2_wait_for_email_from_user(case_id: Annotated[str, Field(..., description="The ID of the case.")], alert_group_identifiers: Annotated[List[str], Field(..., description="Identifiers for the alert groups.")], email_message_id: Annotated[str, Field(..., description="Message_id of the email, which current action would be waiting for. If message has been sent using Send Email action, please select SendEmail.JSONResult.message_id field as a placeholder.")], email_date: Annotated[str, Field(..., description="Send timestamp of the email, which current action would be waiting for. If message has been sent using Send Email action, please select SendEmail.JSONResult.email_date field as a placeholder.")], email_recipients: Annotated[str, Field(..., description="Comma-separated list of recipient emails, response from which current action would be waiting for. If message has been sent using Send Email action, please select Select SendEmail.JSONResult.recipients field as a placeholder.")], wait_stage_timeout_minutes: Annotated[str, Field(..., description="How long in minutes to wait for the user\u2019s reply before marking it timed out.")], wait_for_all_recipients_to_reply: Annotated[bool, Field(default=None, description="Parameter can be used to define if there are multiple recipients - should the Action wait for responses from all of recipients until timeout, or Action should wait for first reply to proceed.")], wait_stage_exclude_pattern: Annotated[str, Field(default=None, description="Regular expression to exclude specific replies from the wait stage. Works with body part of email. Example is, to exclude automatic Out-Of-Office emails to be considered as recipient reply, and instead wait for actual user reply")], folder_to_check_for_reply: Annotated[str, Field(default=None, description="Parameter can be used to specify mailbox email folder (mailbox that was used to send the email with question) to search for the user reply in this folder. Parameter should also accept comma separated list of folders to check the user response in multiple folders. Parameter is case sensitive.")], fetch_response_attachments: Annotated[bool, Field(default=None, description="If selected, if recipient replies with attachment \u2013 fetch recipient response and add it as attachment for the action result.")], target_entities: Annotated[List[TargetEntity], PydanticListField(TargetEntity, description="Optional list of specific target entities (Identifier, EntityType) to run the action on.")], scope: Annotated[str, Field(default="All entities", description="Defines the scope for the action.")]) -> dict:
        """Wait for user's response based on an email sent via Send Email action. Note: This is a Siemplify async action, if required, please adjust the async timeout for action (polling timeout) and global action timeout as needed. Action input parameter “Wait stage timeout (minutes)“ cant be larger than global timeout. Note: Please make sure to set IDE timeout as well, as the IDE timeout will override the action’s timeout if the IDE timeout will be shorter. Requires: IMAP configuration

        Returns:
            dict: A dictionary containing the result of the action execution.
        """
        final_target_entities: Optional[List[TargetEntity]] = None
        final_scope: Optional[str] = None
        is_predefined_scope: Optional[bool] = None
    
        if target_entities:
            # Specific target entities provided, ignore scope parameter
            final_target_entities = target_entities
            final_scope = None
            is_predefined_scope = False
        else:
            # Check if the provided scope is valid
            if scope not in bindings.valid_scopes:
                allowed_values_str = ", ".join(sorted(list(bindings.valid_scopes)))
                return {
                    "Status": "Failed",
                    "Message": f"Invalid scope '{scope}'. Allowed values are: {allowed_values_str}",
                }
            final_target_entities = [] # Pass empty list for entities when using scope
            final_scope = scope
            is_predefined_scope = True
    
        # Fetch integration instance identifier
        try:
            instance_response = await bindings.http_client.get(
                Endpoints.LIST_INTEGRATION_INSTANCES.format(INTEGRATION_NAME="EmailV2")
            )
            instances = instance_response.get("integration_instances", [])
        except Exception as e:
            print(f"Error fetching instance for EmailV2: {e}")
            return {"Status": "Failed", "Message": f"Error fetching instance: {e}"}
    
        if instances:
            instance_identifier = instances[0].get("identifier")
            if not instance_identifier:
                return {"Status": "Failed", "Message": "Instance found but identifier is missing."}
    
            script_params = {}
            script_params["Email Message_id"] = email_message_id
            script_params["Email Date"] = email_date
            script_params["Email Recipients"] = email_recipients
            script_params["Wait stage timeout (minutes)"] = wait_stage_timeout_minutes
            if wait_for_all_recipients_to_reply is not None:
                script_params["Wait for all recipients to reply?"] = wait_for_all_recipients_to_reply
            if wait_stage_exclude_pattern is not None:
                script_params["Wait stage exclude pattern"] = wait_stage_exclude_pattern
            if folder_to_check_for_reply is not None:
                script_params["Folder to check for reply"] = folder_to_check_for_reply
            if fetch_response_attachments is not None:
                script_params["Fetch Response Attachments"] = fetch_response_attachments
    
            # Prepare data model for the API request
            action_data = ApiManualActionDataModel(
                alertGroupIdentifiers=alert_group_identifiers,
                caseId=case_id,
                targetEntities=final_target_entities,
                scope=final_scope,
                isPredefinedScope=is_predefined_scope,
                actionProvider="Scripts",
                actionName="EmailV2_Wait for Email from User",
                properties={
                    "IntegrationInstance": instance_identifier,
                    "ScriptName": "EmailV2_Wait for Email from User",
                    "ScriptParametersEntityFields": json.dumps(script_params)
                }
            )
    
            try:
                execution_response = await bindings.http_client.post(
                    Endpoints.EXECUTE_MANUAL_ACTION,
                    req=action_data.model_dump()
                )
                return execution_response
            except Exception as e:
                print(f"Error executing action EmailV2_Wait for Email from User for EmailV2: {e}")
                return {"Status": "Failed", "Message": f"Error executing action: {e}"}
        else:
            print(f"Warning: No active integration instance found for EmailV2")
            return {"Status": "Failed", "Message": "No active instance found."}

    @mcp.tool()
    async def email_v2_forward_email(case_id: Annotated[str, Field(..., description="The ID of the case.")], alert_group_identifiers: Annotated[List[str], Field(..., description="Identifiers for the alert groups.")], folder_name: Annotated[str, Field(..., description="Mailbox folder to search email in. Parameter should also accept comma separated list of folders. Note that you can set mail-specific folders, for example \"[Gmail]/All Mail\"  to search in all of the folders of Gmail mailbox. Additionally, folder name should match exactly the IMAP folder. If folder contains spaces, folder must be wrapped in double quotes.")], message_id_of_email_to_forward: Annotated[str, Field(..., description="message_id value of the email to forward.")], recipients: Annotated[str, Field(..., description="Arbitrary comma separated list of email addresses for the email recipients.")], subject: Annotated[str, Field(..., description="The email subject part.")], cc: Annotated[str, Field(default=None, description="Arbitrary comma separated list of email addresses to be put in the CC field of email.")], bcc: Annotated[str, Field(default=None, description="BCC email address. Multiple addresses can be separated by commas.")], content: Annotated[EmailContent, Field(default=None, description="The email body part, if Email HTML Template is set, action should support definition of body of the email with provided HTML template.")], return_message_id_for_the_forwarded_email: Annotated[bool, Field(default=None, description="If selected, action returns the message id for the sent email in JSON technical result.")], attachments_paths: Annotated[str, Field(default=None, description="Comma separated list of attachments file paths stored on the server for addition to the email.")], target_entities: Annotated[List[TargetEntity], PydanticListField(TargetEntity, description="Optional list of specific target entities (Identifier, EntityType) to run the action on.")], scope: Annotated[str, Field(default="All entities", description="Defines the scope for the action.")]) -> dict:
        """Forward email including previous messages. Message_id of the email to forward needs to be provided as an action input parameter.

        Returns:
            dict: A dictionary containing the result of the action execution.
        """
        final_target_entities: Optional[List[TargetEntity]] = None
        final_scope: Optional[str] = None
        is_predefined_scope: Optional[bool] = None
    
        if target_entities:
            # Specific target entities provided, ignore scope parameter
            final_target_entities = target_entities
            final_scope = None
            is_predefined_scope = False
        else:
            # Check if the provided scope is valid
            if scope not in bindings.valid_scopes:
                allowed_values_str = ", ".join(sorted(list(bindings.valid_scopes)))
                return {
                    "Status": "Failed",
                    "Message": f"Invalid scope '{scope}'. Allowed values are: {allowed_values_str}",
                }
            final_target_entities = [] # Pass empty list for entities when using scope
            final_scope = scope
            is_predefined_scope = True
    
        # Fetch integration instance identifier
        try:
            instance_response = await bindings.http_client.get(
                Endpoints.LIST_INTEGRATION_INSTANCES.format(INTEGRATION_NAME="EmailV2")
            )
            instances = instance_response.get("integration_instances", [])
        except Exception as e:
            print(f"Error fetching instance for EmailV2: {e}")
            return {"Status": "Failed", "Message": f"Error fetching instance: {e}"}
    
        if instances:
            instance_identifier = instances[0].get("identifier")
            if not instance_identifier:
                return {"Status": "Failed", "Message": "Instance found but identifier is missing."}
    
            script_params = {}
            script_params["Folder Name"] = folder_name
            script_params["Message ID of email to forward"] = message_id_of_email_to_forward
            script_params["Recipients"] = recipients
            if cc is not None:
                script_params["CC"] = cc
            if bcc is not None:
                script_params["BCC"] = bcc
            script_params["Subject"] = subject
            content = content.model_dump()
            if content is not None:
                script_params["Content"] = content
            if return_message_id_for_the_forwarded_email is not None:
                script_params["Return message id for the forwarded email"] = return_message_id_for_the_forwarded_email
            if attachments_paths is not None:
                script_params["Attachments Paths"] = attachments_paths
    
            # Prepare data model for the API request
            action_data = ApiManualActionDataModel(
                alertGroupIdentifiers=alert_group_identifiers,
                caseId=case_id,
                targetEntities=final_target_entities,
                scope=final_scope,
                isPredefinedScope=is_predefined_scope,
                actionProvider="Scripts",
                actionName="EmailV2_Forward Email",
                properties={
                    "IntegrationInstance": instance_identifier,
                    "ScriptName": "EmailV2_Forward Email",
                    "ScriptParametersEntityFields": json.dumps(script_params)
                }
            )
    
            try:
                execution_response = await bindings.http_client.post(
                    Endpoints.EXECUTE_MANUAL_ACTION,
                    req=action_data.model_dump()
                )
                return execution_response
            except Exception as e:
                print(f"Error executing action EmailV2_Forward Email for EmailV2: {e}")
                return {"Status": "Failed", "Message": f"Error executing action: {e}"}
        else:
            print(f"Warning: No active integration instance found for EmailV2")
            return {"Status": "Failed", "Message": "No active instance found."}

    @mcp.tool()
    async def email_v2_save_email_attachments_to_case(case_id: Annotated[str, Field(..., description="The ID of the case.")], alert_group_identifiers: Annotated[List[str], Field(..., description="Identifiers for the alert groups.")], folder_name: Annotated[str, Field(..., description="Mailbox folder to search email in. Parameter should also accept comma separated list of folders to check the user response in multiple folders.")], message_id: Annotated[str, Field(default=None, description="Message id to find an email to download attachments from.")], attachment_to_save: Annotated[str, Field(default=None, description="If parameter is not specified - save all email attachments to the case wall. If parameter specified - save only matching attachment to the case wall.")], target_entities: Annotated[List[TargetEntity], PydanticListField(TargetEntity, description="Optional list of specific target entities (Identifier, EntityType) to run the action on.")], scope: Annotated[str, Field(default="All entities", description="Defines the scope for the action.")]) -> dict:
        """Save email attachments from email stored in monitored mailbox to the Case Wall. Requires: IMAP configuration

        Returns:
            dict: A dictionary containing the result of the action execution.
        """
        final_target_entities: Optional[List[TargetEntity]] = None
        final_scope: Optional[str] = None
        is_predefined_scope: Optional[bool] = None
    
        if target_entities:
            # Specific target entities provided, ignore scope parameter
            final_target_entities = target_entities
            final_scope = None
            is_predefined_scope = False
        else:
            # Check if the provided scope is valid
            if scope not in bindings.valid_scopes:
                allowed_values_str = ", ".join(sorted(list(bindings.valid_scopes)))
                return {
                    "Status": "Failed",
                    "Message": f"Invalid scope '{scope}'. Allowed values are: {allowed_values_str}",
                }
            final_target_entities = [] # Pass empty list for entities when using scope
            final_scope = scope
            is_predefined_scope = True
    
        # Fetch integration instance identifier
        try:
            instance_response = await bindings.http_client.get(
                Endpoints.LIST_INTEGRATION_INSTANCES.format(INTEGRATION_NAME="EmailV2")
            )
            instances = instance_response.get("integration_instances", [])
        except Exception as e:
            print(f"Error fetching instance for EmailV2: {e}")
            return {"Status": "Failed", "Message": f"Error fetching instance: {e}"}
    
        if instances:
            instance_identifier = instances[0].get("identifier")
            if not instance_identifier:
                return {"Status": "Failed", "Message": "Instance found but identifier is missing."}
    
            script_params = {}
            script_params["Folder Name"] = folder_name
            if message_id is not None:
                script_params["Message ID"] = message_id
            if attachment_to_save is not None:
                script_params["Attachment To Save"] = attachment_to_save
    
            # Prepare data model for the API request
            action_data = ApiManualActionDataModel(
                alertGroupIdentifiers=alert_group_identifiers,
                caseId=case_id,
                targetEntities=final_target_entities,
                scope=final_scope,
                isPredefinedScope=is_predefined_scope,
                actionProvider="Scripts",
                actionName="EmailV2_Save Email Attachments To Case",
                properties={
                    "IntegrationInstance": instance_identifier,
                    "ScriptName": "EmailV2_Save Email Attachments To Case",
                    "ScriptParametersEntityFields": json.dumps(script_params)
                }
            )
    
            try:
                execution_response = await bindings.http_client.post(
                    Endpoints.EXECUTE_MANUAL_ACTION,
                    req=action_data.model_dump()
                )
                return execution_response
            except Exception as e:
                print(f"Error executing action EmailV2_Save Email Attachments To Case for EmailV2: {e}")
                return {"Status": "Failed", "Message": f"Error executing action: {e}"}
        else:
            print(f"Warning: No active integration instance found for EmailV2")
            return {"Status": "Failed", "Message": "No active instance found."}

    @mcp.tool()
    async def email_v2_move_email_to_folder(case_id: Annotated[str, Field(..., description="The ID of the case.")], alert_group_identifiers: Annotated[List[str], Field(..., description="Identifiers for the alert groups.")], source_folder_name: Annotated[str, Field(..., description="Mailbox folder to search email in. Parameter should also accept comma separated list of folders to check the user response in multiple folders.")], destination_folder_name: Annotated[str, Field(..., description="Destination folder to move emails to")], message_i_ds: Annotated[str, Field(default=None, description="Filter condition, specify emails with which email ids to find. Should accept comma separated multiple message ids. If message id is provided, subject filter is ignored.")], subject_filter: Annotated[str, Field(default=None, description="Filter condition, specify what subject to search for emails")], only_unread: Annotated[bool, Field(default=None, description="Filter condition, specify if search should look only for unread emails")], target_entities: Annotated[List[TargetEntity], PydanticListField(TargetEntity, description="Optional list of specific target entities (Identifier, EntityType) to run the action on.")], scope: Annotated[str, Field(default="All entities", description="Defines the scope for the action.")]) -> dict:
        """Searches for emails in the source folder, then moves emails matching the search criteria to the target folder. Requires: IMAP configuration

        Returns:
            dict: A dictionary containing the result of the action execution.
        """
        final_target_entities: Optional[List[TargetEntity]] = None
        final_scope: Optional[str] = None
        is_predefined_scope: Optional[bool] = None
    
        if target_entities:
            # Specific target entities provided, ignore scope parameter
            final_target_entities = target_entities
            final_scope = None
            is_predefined_scope = False
        else:
            # Check if the provided scope is valid
            if scope not in bindings.valid_scopes:
                allowed_values_str = ", ".join(sorted(list(bindings.valid_scopes)))
                return {
                    "Status": "Failed",
                    "Message": f"Invalid scope '{scope}'. Allowed values are: {allowed_values_str}",
                }
            final_target_entities = [] # Pass empty list for entities when using scope
            final_scope = scope
            is_predefined_scope = True
    
        # Fetch integration instance identifier
        try:
            instance_response = await bindings.http_client.get(
                Endpoints.LIST_INTEGRATION_INSTANCES.format(INTEGRATION_NAME="EmailV2")
            )
            instances = instance_response.get("integration_instances", [])
        except Exception as e:
            print(f"Error fetching instance for EmailV2: {e}")
            return {"Status": "Failed", "Message": f"Error fetching instance: {e}"}
    
        if instances:
            instance_identifier = instances[0].get("identifier")
            if not instance_identifier:
                return {"Status": "Failed", "Message": "Instance found but identifier is missing."}
    
            script_params = {}
            script_params["Source Folder Name"] = source_folder_name
            script_params["Destination Folder Name"] = destination_folder_name
            if message_i_ds is not None:
                script_params["Message IDs"] = message_i_ds
            if subject_filter is not None:
                script_params["Subject Filter"] = subject_filter
            if only_unread is not None:
                script_params["Only Unread"] = only_unread
    
            # Prepare data model for the API request
            action_data = ApiManualActionDataModel(
                alertGroupIdentifiers=alert_group_identifiers,
                caseId=case_id,
                targetEntities=final_target_entities,
                scope=final_scope,
                isPredefinedScope=is_predefined_scope,
                actionProvider="Scripts",
                actionName="EmailV2_Move Email To Folder",
                properties={
                    "IntegrationInstance": instance_identifier,
                    "ScriptName": "EmailV2_Move Email To Folder",
                    "ScriptParametersEntityFields": json.dumps(script_params)
                }
            )
    
            try:
                execution_response = await bindings.http_client.post(
                    Endpoints.EXECUTE_MANUAL_ACTION,
                    req=action_data.model_dump()
                )
                return execution_response
            except Exception as e:
                print(f"Error executing action EmailV2_Move Email To Folder for EmailV2: {e}")
                return {"Status": "Failed", "Message": f"Error executing action: {e}"}
        else:
            print(f"Warning: No active integration instance found for EmailV2")
            return {"Status": "Failed", "Message": "No active instance found."}

    @mcp.tool()
    async def email_v2_ping(case_id: Annotated[str, Field(..., description="The ID of the case.")], alert_group_identifiers: Annotated[List[str], Field(..., description="Identifiers for the alert groups.")], target_entities: Annotated[List[TargetEntity], PydanticListField(TargetEntity, description="Optional list of specific target entities (Identifier, EntityType) to run the action on.")], scope: Annotated[str, Field(default="All entities", description="Defines the scope for the action.")]) -> dict:
        """Test Connectivity. Requires: IMAP or SMTP configuration

        Returns:
            dict: A dictionary containing the result of the action execution.
        """
        final_target_entities: Optional[List[TargetEntity]] = None
        final_scope: Optional[str] = None
        is_predefined_scope: Optional[bool] = None
    
        if target_entities:
            # Specific target entities provided, ignore scope parameter
            final_target_entities = target_entities
            final_scope = None
            is_predefined_scope = False
        else:
            # Check if the provided scope is valid
            if scope not in bindings.valid_scopes:
                allowed_values_str = ", ".join(sorted(list(bindings.valid_scopes)))
                return {
                    "Status": "Failed",
                    "Message": f"Invalid scope '{scope}'. Allowed values are: {allowed_values_str}",
                }
            final_target_entities = [] # Pass empty list for entities when using scope
            final_scope = scope
            is_predefined_scope = True
    
        # Fetch integration instance identifier
        try:
            instance_response = await bindings.http_client.get(
                Endpoints.LIST_INTEGRATION_INSTANCES.format(INTEGRATION_NAME="EmailV2")
            )
            instances = instance_response.get("integration_instances", [])
        except Exception as e:
            print(f"Error fetching instance for EmailV2: {e}")
            return {"Status": "Failed", "Message": f"Error fetching instance: {e}"}
    
        if instances:
            instance_identifier = instances[0].get("identifier")
            if not instance_identifier:
                return {"Status": "Failed", "Message": "Instance found but identifier is missing."}
    
            script_params = {}
    
            # Prepare data model for the API request
            action_data = ApiManualActionDataModel(
                alertGroupIdentifiers=alert_group_identifiers,
                caseId=case_id,
                targetEntities=final_target_entities,
                scope=final_scope,
                isPredefinedScope=is_predefined_scope,
                actionProvider="Scripts",
                actionName="EmailV2_Ping",
                properties={
                    "IntegrationInstance": instance_identifier,
                    "ScriptName": "EmailV2_Ping",
                    "ScriptParametersEntityFields": json.dumps(script_params)
                }
            )
    
            try:
                execution_response = await bindings.http_client.post(
                    Endpoints.EXECUTE_MANUAL_ACTION,
                    req=action_data.model_dump()
                )
                return execution_response
            except Exception as e:
                print(f"Error executing action EmailV2_Ping for EmailV2: {e}")
                return {"Status": "Failed", "Message": f"Error executing action: {e}"}
        else:
            print(f"Warning: No active integration instance found for EmailV2")
            return {"Status": "Failed", "Message": "No active instance found."}

    @mcp.tool()
    async def email_v2_send_email(case_id: Annotated[str, Field(..., description="The ID of the case.")], alert_group_identifiers: Annotated[List[str], Field(..., description="Identifiers for the alert groups.")], recipients: Annotated[str, Field(..., description="Arbitrary comma separated list of email addresses for the email recipients")], subject: Annotated[str, Field(..., description="The email subject part")], content: Annotated[EmailContent, Field(..., description="The email body part, if Email HTML Template is set, action should support definition of body of the email with provided HTML template.")], cc: Annotated[str, Field(default=None, description="Arbitrary comma separated list of email addresses to be put in the CC field of email")], bcc: Annotated[str, Field(default=None, description="BCC email address. Multiple addresses can be separated by commas")], return_message_id_for_the_sent_email: Annotated[bool, Field(default=None, description="If selected, action returns the message id for the sent email in JSON technical result. This message id when can be used for the 'Wait for Email from user' action to process user response")], attachments_paths: Annotated[str, Field(default=None, description="Comma separated list of attachments file paths stored on the server for addition to the email.")], target_entities: Annotated[List[TargetEntity], PydanticListField(TargetEntity, description="Optional list of specific target entities (Identifier, EntityType) to run the action on.")], scope: Annotated[str, Field(default="All entities", description="Defines the scope for the action.")]) -> dict:
        """Send email message. Requires: SMTP configuration

        Returns:
            dict: A dictionary containing the result of the action execution.
        """
        final_target_entities: Optional[List[TargetEntity]] = None
        final_scope: Optional[str] = None
        is_predefined_scope: Optional[bool] = None
    
        if target_entities:
            # Specific target entities provided, ignore scope parameter
            final_target_entities = target_entities
            final_scope = None
            is_predefined_scope = False
        else:
            # Check if the provided scope is valid
            if scope not in bindings.valid_scopes:
                allowed_values_str = ", ".join(sorted(list(bindings.valid_scopes)))
                return {
                    "Status": "Failed",
                    "Message": f"Invalid scope '{scope}'. Allowed values are: {allowed_values_str}",
                }
            final_target_entities = [] # Pass empty list for entities when using scope
            final_scope = scope
            is_predefined_scope = True
    
        # Fetch integration instance identifier
        try:
            instance_response = await bindings.http_client.get(
                Endpoints.LIST_INTEGRATION_INSTANCES.format(INTEGRATION_NAME="EmailV2")
            )
            instances = instance_response.get("integration_instances", [])
        except Exception as e:
            print(f"Error fetching instance for EmailV2: {e}")
            return {"Status": "Failed", "Message": f"Error fetching instance: {e}"}
    
        if instances:
            instance_identifier = instances[0].get("identifier")
            if not instance_identifier:
                return {"Status": "Failed", "Message": "Instance found but identifier is missing."}
    
            script_params = {}
            script_params["Recipients"] = recipients
            if cc is not None:
                script_params["CC"] = cc
            if bcc is not None:
                script_params["BCC"] = bcc
            script_params["Subject"] = subject
            content = content.model_dump()
            script_params["Content"] = content
            if return_message_id_for_the_sent_email is not None:
                script_params["Return message id for the sent email"] = return_message_id_for_the_sent_email
            if attachments_paths is not None:
                script_params["Attachments Paths"] = attachments_paths
    
            # Prepare data model for the API request
            action_data = ApiManualActionDataModel(
                alertGroupIdentifiers=alert_group_identifiers,
                caseId=case_id,
                targetEntities=final_target_entities,
                scope=final_scope,
                isPredefinedScope=is_predefined_scope,
                actionProvider="Scripts",
                actionName="EmailV2_Send Email",
                properties={
                    "IntegrationInstance": instance_identifier,
                    "ScriptName": "EmailV2_Send Email",
                    "ScriptParametersEntityFields": json.dumps(script_params)
                }
            )
    
            try:
                execution_response = await bindings.http_client.post(
                    Endpoints.EXECUTE_MANUAL_ACTION,
                    req=action_data.model_dump()
                )
                return execution_response
            except Exception as e:
                print(f"Error executing action EmailV2_Send Email for EmailV2: {e}")
                return {"Status": "Failed", "Message": f"Error executing action: {e}"}
        else:
            print(f"Warning: No active integration instance found for EmailV2")
            return {"Status": "Failed", "Message": "No active instance found."}

    @mcp.tool()
    async def email_v2_download_email_attachments(case_id: Annotated[str, Field(..., description="The ID of the case.")], alert_group_identifiers: Annotated[List[str], Field(..., description="Identifiers for the alert groups.")], folder_name: Annotated[str, Field(..., description="Mailbox folder to search email in. Parameter should also accept comma separated list of folders to check the user response in multiple folders")], download_path: Annotated[str, Field(..., description="File path on the server where to download the email attachments")], message_i_ds: Annotated[str, Field(default=None, description="Filter condition, specify emails with which email ids to find. Should accept comma separated multiple message ids. If message id is provided, subject filter is ignored")], subject_filter: Annotated[str, Field(default=None, description="Filter condition to search emails by specific subject")], target_entities: Annotated[List[TargetEntity], PydanticListField(TargetEntity, description="Optional list of specific target entities (Identifier, EntityType) to run the action on.")], scope: Annotated[str, Field(default="All entities", description="Defines the scope for the action.")]) -> dict:
        """Download email attachments from email to specific file path on Siemplify server. Requires: IMAP configuration

        Returns:
            dict: A dictionary containing the result of the action execution.
        """
        final_target_entities: Optional[List[TargetEntity]] = None
        final_scope: Optional[str] = None
        is_predefined_scope: Optional[bool] = None
    
        if target_entities:
            # Specific target entities provided, ignore scope parameter
            final_target_entities = target_entities
            final_scope = None
            is_predefined_scope = False
        else:
            # Check if the provided scope is valid
            if scope not in bindings.valid_scopes:
                allowed_values_str = ", ".join(sorted(list(bindings.valid_scopes)))
                return {
                    "Status": "Failed",
                    "Message": f"Invalid scope '{scope}'. Allowed values are: {allowed_values_str}",
                }
            final_target_entities = [] # Pass empty list for entities when using scope
            final_scope = scope
            is_predefined_scope = True
    
        # Fetch integration instance identifier
        try:
            instance_response = await bindings.http_client.get(
                Endpoints.LIST_INTEGRATION_INSTANCES.format(INTEGRATION_NAME="EmailV2")
            )
            instances = instance_response.get("integration_instances", [])
        except Exception as e:
            print(f"Error fetching instance for EmailV2: {e}")
            return {"Status": "Failed", "Message": f"Error fetching instance: {e}"}
    
        if instances:
            instance_identifier = instances[0].get("identifier")
            if not instance_identifier:
                return {"Status": "Failed", "Message": "Instance found but identifier is missing."}
    
            script_params = {}
            script_params["Folder Name"] = folder_name
            script_params["Download Path"] = download_path
            if message_i_ds is not None:
                script_params["Message IDs"] = message_i_ds
            if subject_filter is not None:
                script_params["Subject Filter"] = subject_filter
    
            # Prepare data model for the API request
            action_data = ApiManualActionDataModel(
                alertGroupIdentifiers=alert_group_identifiers,
                caseId=case_id,
                targetEntities=final_target_entities,
                scope=final_scope,
                isPredefinedScope=is_predefined_scope,
                actionProvider="Scripts",
                actionName="EmailV2_DownloadEmailAttachments",
                properties={
                    "IntegrationInstance": instance_identifier,
                    "ScriptName": "EmailV2_DownloadEmailAttachments",
                    "ScriptParametersEntityFields": json.dumps(script_params)
                }
            )
    
            try:
                execution_response = await bindings.http_client.post(
                    Endpoints.EXECUTE_MANUAL_ACTION,
                    req=action_data.model_dump()
                )
                return execution_response
            except Exception as e:
                print(f"Error executing action EmailV2_DownloadEmailAttachments for EmailV2: {e}")
                return {"Status": "Failed", "Message": f"Error executing action: {e}"}
        else:
            print(f"Warning: No active integration instance found for EmailV2")
            return {"Status": "Failed", "Message": "No active instance found."}

    @mcp.tool()
    async def email_v2_delete_email(case_id: Annotated[str, Field(..., description="The ID of the case.")], alert_group_identifiers: Annotated[List[str], Field(..., description="Identifiers for the alert groups.")], folder_name: Annotated[str, Field(..., description="Mailbox folder to search email in. Parameter should also accept comma separated list of folders to check the user response in multiple folders.")], message_i_ds: Annotated[str, Field(default=None, description="Filter condition, specify emails with which email ids to find. Should accept comma separated list of message ids to search for. If message id is provided, subject, sender, recipient and time filters are ignored.")], subject_filter: Annotated[str, Field(default=None, description="Filter condition, specify subject to search for emails.")], sender_filter: Annotated[str, Field(default=None, description="Filter condition, specify who should be the sender of needed emails")], recipient_filter: Annotated[str, Field(default=None, description="Filter condition, specify who should be the recipient of needed emails")], days_back: Annotated[str, Field(default=None, description="Filter condition, specify in what time frame in days should action look for emails to delete. Note - Action works in days granularity only. 0 means it will search for mails from today.")], delete_all_matching_emails: Annotated[bool, Field(default=None, description="Filter condition, specify if action should delete all matched by criteria emails from the mailbox or delete only first match.")], target_entities: Annotated[List[TargetEntity], PydanticListField(TargetEntity, description="Optional list of specific target entities (Identifier, EntityType) to run the action on.")], scope: Annotated[str, Field(default="All entities", description="Defines the scope for the action.")]) -> dict:
        """Delete one or multiple email from the mailbox that matches search criteria. Delete can be done for the first email that matched the search criteria, or it can be done for all matching emails. Requires: IMAP configuration

        Returns:
            dict: A dictionary containing the result of the action execution.
        """
        final_target_entities: Optional[List[TargetEntity]] = None
        final_scope: Optional[str] = None
        is_predefined_scope: Optional[bool] = None
    
        if target_entities:
            # Specific target entities provided, ignore scope parameter
            final_target_entities = target_entities
            final_scope = None
            is_predefined_scope = False
        else:
            # Check if the provided scope is valid
            if scope not in bindings.valid_scopes:
                allowed_values_str = ", ".join(sorted(list(bindings.valid_scopes)))
                return {
                    "Status": "Failed",
                    "Message": f"Invalid scope '{scope}'. Allowed values are: {allowed_values_str}",
                }
            final_target_entities = [] # Pass empty list for entities when using scope
            final_scope = scope
            is_predefined_scope = True
    
        # Fetch integration instance identifier
        try:
            instance_response = await bindings.http_client.get(
                Endpoints.LIST_INTEGRATION_INSTANCES.format(INTEGRATION_NAME="EmailV2")
            )
            instances = instance_response.get("integration_instances", [])
        except Exception as e:
            print(f"Error fetching instance for EmailV2: {e}")
            return {"Status": "Failed", "Message": f"Error fetching instance: {e}"}
    
        if instances:
            instance_identifier = instances[0].get("identifier")
            if not instance_identifier:
                return {"Status": "Failed", "Message": "Instance found but identifier is missing."}
    
            script_params = {}
            script_params["Folder Name"] = folder_name
            if message_i_ds is not None:
                script_params["Message IDs"] = message_i_ds
            if subject_filter is not None:
                script_params["Subject Filter"] = subject_filter
            if sender_filter is not None:
                script_params["Sender Filter"] = sender_filter
            if recipient_filter is not None:
                script_params["Recipient Filter"] = recipient_filter
            if days_back is not None:
                script_params["Days Back"] = days_back
            if delete_all_matching_emails is not None:
                script_params["Delete All Matching Emails"] = delete_all_matching_emails
    
            # Prepare data model for the API request
            action_data = ApiManualActionDataModel(
                alertGroupIdentifiers=alert_group_identifiers,
                caseId=case_id,
                targetEntities=final_target_entities,
                scope=final_scope,
                isPredefinedScope=is_predefined_scope,
                actionProvider="Scripts",
                actionName="EmailV2_Delete Email",
                properties={
                    "IntegrationInstance": instance_identifier,
                    "ScriptName": "EmailV2_Delete Email",
                    "ScriptParametersEntityFields": json.dumps(script_params)
                }
            )
    
            try:
                execution_response = await bindings.http_client.post(
                    Endpoints.EXECUTE_MANUAL_ACTION,
                    req=action_data.model_dump()
                )
                return execution_response
            except Exception as e:
                print(f"Error executing action EmailV2_Delete Email for EmailV2: {e}")
                return {"Status": "Failed", "Message": f"Error executing action: {e}"}
        else:
            print(f"Warning: No active integration instance found for EmailV2")
            return {"Status": "Failed", "Message": "No active instance found."}

    @mcp.tool()
    async def email_v2_search_email(case_id: Annotated[str, Field(..., description="The ID of the case.")], alert_group_identifiers: Annotated[List[str], Field(..., description="Identifiers for the alert groups.")], folder_name: Annotated[str, Field(..., description="Mailbox folder to search email in. Parameter should also accept comma separated list of folders to check the user response in multiple folders.")], time_frame_minutes: Annotated[str, Field(..., description="Filter condition, specify in what time frame in minutes should search look for emails")], max_emails_to_return: Annotated[str, Field(..., description="Return max X emails as an action result.")], subject_filter: Annotated[str, Field(default=None, description="Filter condition, specify what subject to search for emails")], sender_filter: Annotated[str, Field(default=None, description="Filter condition, specify who should be the sender of needed emails")], recipient_filter: Annotated[str, Field(default=None, description="Filter condition, specify who should be the recipient of needed emails")], only_unread: Annotated[bool, Field(default=None, description="Filter condition, specify if search should look only for unread emails")], target_entities: Annotated[List[TargetEntity], PydanticListField(TargetEntity, description="Optional list of specific target entities (Identifier, EntityType) to run the action on.")], scope: Annotated[str, Field(default="All entities", description="Defines the scope for the action.")]) -> dict:
        """Search email messages. Requires: IMAP configuration

        Returns:
            dict: A dictionary containing the result of the action execution.
        """
        final_target_entities: Optional[List[TargetEntity]] = None
        final_scope: Optional[str] = None
        is_predefined_scope: Optional[bool] = None
    
        if target_entities:
            # Specific target entities provided, ignore scope parameter
            final_target_entities = target_entities
            final_scope = None
            is_predefined_scope = False
        else:
            # Check if the provided scope is valid
            if scope not in bindings.valid_scopes:
                allowed_values_str = ", ".join(sorted(list(bindings.valid_scopes)))
                return {
                    "Status": "Failed",
                    "Message": f"Invalid scope '{scope}'. Allowed values are: {allowed_values_str}",
                }
            final_target_entities = [] # Pass empty list for entities when using scope
            final_scope = scope
            is_predefined_scope = True
    
        # Fetch integration instance identifier
        try:
            instance_response = await bindings.http_client.get(
                Endpoints.LIST_INTEGRATION_INSTANCES.format(INTEGRATION_NAME="EmailV2")
            )
            instances = instance_response.get("integration_instances", [])
        except Exception as e:
            print(f"Error fetching instance for EmailV2: {e}")
            return {"Status": "Failed", "Message": f"Error fetching instance: {e}"}
    
        if instances:
            instance_identifier = instances[0].get("identifier")
            if not instance_identifier:
                return {"Status": "Failed", "Message": "Instance found but identifier is missing."}
    
            script_params = {}
            script_params["Folder Name"] = folder_name
            if subject_filter is not None:
                script_params["Subject Filter"] = subject_filter
            if sender_filter is not None:
                script_params["Sender Filter"] = sender_filter
            if recipient_filter is not None:
                script_params["Recipient Filter"] = recipient_filter
            script_params["Time frame (minutes)"] = time_frame_minutes
            if only_unread is not None:
                script_params["Only Unread"] = only_unread
            script_params["Max Emails To Return"] = max_emails_to_return
    
            # Prepare data model for the API request
            action_data = ApiManualActionDataModel(
                alertGroupIdentifiers=alert_group_identifiers,
                caseId=case_id,
                targetEntities=final_target_entities,
                scope=final_scope,
                isPredefinedScope=is_predefined_scope,
                actionProvider="Scripts",
                actionName="EmailV2_Search Email",
                properties={
                    "IntegrationInstance": instance_identifier,
                    "ScriptName": "EmailV2_Search Email",
                    "ScriptParametersEntityFields": json.dumps(script_params)
                }
            )
    
            try:
                execution_response = await bindings.http_client.post(
                    Endpoints.EXECUTE_MANUAL_ACTION,
                    req=action_data.model_dump()
                )
                return execution_response
            except Exception as e:
                print(f"Error executing action EmailV2_Search Email for EmailV2: {e}")
                return {"Status": "Failed", "Message": f"Error executing action: {e}"}
        else:
            print(f"Warning: No active integration instance found for EmailV2")
            return {"Status": "Failed", "Message": "No active instance found."}
