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
    # This function registers all tools (actions) for the MicrosoftGraphMail integration.

    @mcp.tool()
    async def microsoft_graph_mail_send_vote_email(case_id: Annotated[str, Field(..., description="The ID of the case.")], alert_group_identifiers: Annotated[List[str], Field(..., description="Identifiers for the alert groups.")], send_from: Annotated[str, Field(..., description="Optional email address to send an email from (if permissions allow it). By default, the email is sent from the default mailbox specified in the integration configuration.")], subject: Annotated[str, Field(..., description="Email subject.")], send_to: Annotated[str, Field(..., description="Arbitrary comma-separated list of email addresses for the email recipients, for example, user1@company.co, user2@company.co.")], email_html_template: Annotated[EmailContent, Field(..., description="The question you would like to ask, or describe the decision you would like the recipient to be able to respond to")], structure_of_voting_options: Annotated[List[str], Field(..., description="Structure of the vote to send to the recipients.")], attachment_location: Annotated[List[str], Field(..., description="Location where the attachments to be added are stored. By default, the action attempts to get the attachment from the Google Cloud storage bucket, another option is to fetch it from the local file system.")], cc: Annotated[str, Field(default=None, description="Arbitrary comma-separated list of email addresses to use in the CC email field. Use the same format as for the \"Send to\" field.")], bcc: Annotated[str, Field(default=None, description="Arbitrary comma-separated list of email addresses to use in the BCC email field. Use the same format for the \"Send to\" field.")], attachments_paths: Annotated[str, Field(default=None, description="Specify the attachments to be added, parameter expects full paths to be provided, for example: /<work directory>/file1.pdf. Parameter accepts multiple values as a comma separated string.")], reply_to_recipients: Annotated[str, Field(default=None, description="Comma-separated list of recipients used in the Reply-To header. Note: The Reply-To header is added to force email replies to specific email addresses instead of the email sender address stated in the From field.")], target_entities: Annotated[List[TargetEntity], PydanticListField(TargetEntity, description="Optional list of specific target entities (Identifier, EntityType) to run the action on.")], scope: Annotated[str, Field(default="All entities", description="Defines the scope for the action.")]) -> dict:
        """Send email with easy answering options, to allow stakeholders to be included in workflow processes. This action uses Google SecOps HTML templates to format the email. If permissions allow, the action sends an email from a mailbox different than the one specified in the integration configuration. Note: This action is not running on Google SecOps entities.

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
                Endpoints.LIST_INTEGRATION_INSTANCES.format(INTEGRATION_NAME="MicrosoftGraphMail")
            )
            instances = instance_response.get("integration_instances", [])
        except Exception as e:
            print(f"Error fetching instance for MicrosoftGraphMail: {e}")
            return {"Status": "Failed", "Message": f"Error fetching instance: {e}"}
    
        if instances:
            instance_identifier = instances[0].get("identifier")
            if not instance_identifier:
                return {"Status": "Failed", "Message": "Instance found but identifier is missing."}
    
            script_params = {}
            script_params["Send From"] = send_from
            script_params["Subject"] = subject
            script_params["Send to"] = send_to
            if cc is not None:
                script_params["CC"] = cc
            if bcc is not None:
                script_params["BCC"] = bcc
            if attachments_paths is not None:
                script_params["Attachments Paths"] = attachments_paths
            email_html_template = email_html_template.model_dump()
            script_params["Email HTML Template"] = email_html_template
            script_params["Structure of voting options"] = structure_of_voting_options
            if reply_to_recipients is not None:
                script_params["Reply-To Recipients"] = reply_to_recipients
            script_params["Attachment Location"] = attachment_location
    
            # Prepare data model for the API request
            action_data = ApiManualActionDataModel(
                alertGroupIdentifiers=alert_group_identifiers,
                caseId=case_id,
                targetEntities=final_target_entities,
                scope=final_scope,
                isPredefinedScope=is_predefined_scope,
                actionProvider="Scripts",
                actionName="MicrosoftGraphMail_Send Vote Email",
                properties={
                    "IntegrationInstance": instance_identifier,
                    "ScriptName": "MicrosoftGraphMail_Send Vote Email",
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
                print(f"Error executing action MicrosoftGraphMail_Send Vote Email for MicrosoftGraphMail: {e}")
                return {"Status": "Failed", "Message": f"Error executing action: {e}"}
        else:
            print(f"Warning: No active integration instance found for MicrosoftGraphMail")
            return {"Status": "Failed", "Message": "No active instance found."}

    @mcp.tool()
    async def microsoft_graph_mail_mark_email_as_not_junk(case_id: Annotated[str, Field(..., description="The ID of the case.")], alert_group_identifiers: Annotated[List[str], Field(..., description="Identifiers for the alert groups.")], search_in_mailbox: Annotated[str, Field(..., description="A mailbox to search for an email in. By default, the action  attempts to search for the email in the default mailbox that you specified in the integration configuration. With correct permissions, the action can execute a search in other mailboxes. Parameter accepts multiple values as a comma separated string.")], folder_name: Annotated[str, Field(..., description="A mailbox folder to search in.")], mail_i_ds: Annotated[str, Field(..., description="Specify the mail ids or internetMessageIds to mark as not junk. Parameter accepts multiple values as a comma separated string.")], target_entities: Annotated[List[TargetEntity], PydanticListField(TargetEntity, description="Optional list of specific target entities (Identifier, EntityType) to run the action on.")], scope: Annotated[str, Field(default="All entities", description="Defines the scope for the action.")]) -> dict:
        """Mark an email as not junk for a specific mailbox. This action removes the sender from the list of blocked senders and moves the message to the Inbox folder. Note: This action uses the beta version of Microsoft Graph APIs and is not running on Google SecOps entities.

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
                Endpoints.LIST_INTEGRATION_INSTANCES.format(INTEGRATION_NAME="MicrosoftGraphMail")
            )
            instances = instance_response.get("integration_instances", [])
        except Exception as e:
            print(f"Error fetching instance for MicrosoftGraphMail: {e}")
            return {"Status": "Failed", "Message": f"Error fetching instance: {e}"}
    
        if instances:
            instance_identifier = instances[0].get("identifier")
            if not instance_identifier:
                return {"Status": "Failed", "Message": "Instance found but identifier is missing."}
    
            script_params = {}
            script_params["Search In Mailbox"] = search_in_mailbox
            script_params["Folder Name"] = folder_name
            script_params["Mail IDs"] = mail_i_ds
    
            # Prepare data model for the API request
            action_data = ApiManualActionDataModel(
                alertGroupIdentifiers=alert_group_identifiers,
                caseId=case_id,
                targetEntities=final_target_entities,
                scope=final_scope,
                isPredefinedScope=is_predefined_scope,
                actionProvider="Scripts",
                actionName="MicrosoftGraphMail_Mark Email as Not Junk",
                properties={
                    "IntegrationInstance": instance_identifier,
                    "ScriptName": "MicrosoftGraphMail_Mark Email as Not Junk",
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
                print(f"Error executing action MicrosoftGraphMail_Mark Email as Not Junk for MicrosoftGraphMail: {e}")
                return {"Status": "Failed", "Message": f"Error executing action: {e}"}
        else:
            print(f"Warning: No active integration instance found for MicrosoftGraphMail")
            return {"Status": "Failed", "Message": "No active instance found."}

    @mcp.tool()
    async def microsoft_graph_mail_send_thread_reply(case_id: Annotated[str, Field(..., description="The ID of the case.")], alert_group_identifiers: Annotated[List[str], Field(..., description="Identifiers for the alert groups.")], send_from: Annotated[str, Field(..., description="Specify the optional email address from which if permissions allow, email should be sent. By default, the email will be sent from the default mailbox specified in the integration configuration.")], mail_id: Annotated[str, Field(..., description="Specify the ID or internetMessageId of the message to which you want to send a reply.")], folder_name: Annotated[str, Field(..., description="Specify the mailbox folder to search in. '/' separator can be used to specify a subfolder to search in, example: Inbox/Subfolder")], mail_content: Annotated[str, Field(..., description="Specify the email body part.")], attachment_location: Annotated[List[str], Field(..., description="Location where the attachments to be added are stored. By default, the action attempts to get the attachment from the Google Cloud storage bucket, another option is to fetch it from the local file system.")], attachments_paths: Annotated[str, Field(default=None, description="Specify the attachments to be added, parameter expects full paths to be provided, for example: /<work directory>/file1.pdf. Parameter accepts multiple values as a comma separated string.")], reply_all: Annotated[bool, Field(default=None, description="If enabled, action will send a reply to all recipients related to the original email. Note: this parameter has priority over \u201cReply To\u201c parameter.")], reply_to: Annotated[str, Field(default=None, description="Specify a comma-separated list of emails to which you want to send this reply. If nothing is provided and \u201cReply All\u201c is disabled, action will only send a reply to the sender of the email. If \u201cReply All\u201c is enabled, action will ignore this parameter.")], target_entities: Annotated[List[TargetEntity], PydanticListField(TargetEntity, description="Optional list of specific target entities (Identifier, EntityType) to run the action on.")], scope: Annotated[str, Field(default="All entities", description="Defines the scope for the action.")]) -> dict:
        """Send a message as a reply to the email thread. If permissions allow, action can send an email from a mailbox different that is specified in the integration configuration. Note: Action is not running on Chronicle entities.

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
                Endpoints.LIST_INTEGRATION_INSTANCES.format(INTEGRATION_NAME="MicrosoftGraphMail")
            )
            instances = instance_response.get("integration_instances", [])
        except Exception as e:
            print(f"Error fetching instance for MicrosoftGraphMail: {e}")
            return {"Status": "Failed", "Message": f"Error fetching instance: {e}"}
    
        if instances:
            instance_identifier = instances[0].get("identifier")
            if not instance_identifier:
                return {"Status": "Failed", "Message": "Instance found but identifier is missing."}
    
            script_params = {}
            script_params["Send From"] = send_from
            script_params["Mail ID"] = mail_id
            script_params["Folder Name"] = folder_name
            if attachments_paths is not None:
                script_params["Attachments Paths"] = attachments_paths
            script_params["Mail Content"] = mail_content
            if reply_all is not None:
                script_params["Reply All"] = reply_all
            if reply_to is not None:
                script_params["Reply To"] = reply_to
            script_params["Attachment Location"] = attachment_location
    
            # Prepare data model for the API request
            action_data = ApiManualActionDataModel(
                alertGroupIdentifiers=alert_group_identifiers,
                caseId=case_id,
                targetEntities=final_target_entities,
                scope=final_scope,
                isPredefinedScope=is_predefined_scope,
                actionProvider="Scripts",
                actionName="MicrosoftGraphMail_Send Thread Reply",
                properties={
                    "IntegrationInstance": instance_identifier,
                    "ScriptName": "MicrosoftGraphMail_Send Thread Reply",
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
                print(f"Error executing action MicrosoftGraphMail_Send Thread Reply for MicrosoftGraphMail: {e}")
                return {"Status": "Failed", "Message": f"Error executing action: {e}"}
        else:
            print(f"Warning: No active integration instance found for MicrosoftGraphMail")
            return {"Status": "Failed", "Message": "No active instance found."}

    @mcp.tool()
    async def microsoft_graph_mail_wait_for_email_from_user(case_id: Annotated[str, Field(..., description="The ID of the case.")], alert_group_identifiers: Annotated[List[str], Field(..., description="Identifiers for the alert groups.")], mail_id: Annotated[str, Field(..., description="Specify the id or internetMessageId of the email, which current action would be waiting for. If the message has been sent using Send Email action, please select SendEmail.JSONResult|id or Send Email.JsonResult|internetMessageId field as a placeholder. Search Emails action also can return ids for emails.")], wait_for_all_recipients_to_reply: Annotated[bool, Field(default=None, description="If enabled,  the action will wait for responses from all of the recipients until timeout, and not finish upon getting the first response.")], wait_stage_exclude_pattern: Annotated[str, Field(default=None, description="Specify the regular expression to exclude specific replies from the wait stage. Works with subject and body parts of the email. Example is, to exclude automatic Out-Of-Office emails to be considered as recipient reply, and instead wait for actual user reply.")], folder_to_check_for_reply: Annotated[str, Field(default=None, description="Specify the mailbox email folder (mailbox that was used to send the email with question) to search for the user reply in this folder. '/' separator can be used to specify a subfolder to search in, example: Inbox/Subfolder")], fetch_response_attachments: Annotated[bool, Field(default=None, description="If enabled, if recipient replies with attachment - fetch recipient response and add it as attachment for the action result.")], limit_the_amount_of_information_returned_in_the_json_result: Annotated[bool, Field(default=None, description="If enabled, the amount of information returned by the action will be limited only to the key email fields.")], disable_the_action_json_result: Annotated[bool, Field(default=None, description="If enabled, action will not return JSON result.")], target_entities: Annotated[List[TargetEntity], PydanticListField(TargetEntity, description="Optional list of specific target entities (Identifier, EntityType) to run the action on.")], scope: Annotated[str, Field(default="All entities", description="Defines the scope for the action.")]) -> dict:
        """Wait for user's response based on an email sent via the "Send Mail" action. Action is async, please adjust action timeout in IDE accordingly. Action is not working on Chronicle entities.

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
                Endpoints.LIST_INTEGRATION_INSTANCES.format(INTEGRATION_NAME="MicrosoftGraphMail")
            )
            instances = instance_response.get("integration_instances", [])
        except Exception as e:
            print(f"Error fetching instance for MicrosoftGraphMail: {e}")
            return {"Status": "Failed", "Message": f"Error fetching instance: {e}"}
    
        if instances:
            instance_identifier = instances[0].get("identifier")
            if not instance_identifier:
                return {"Status": "Failed", "Message": "Instance found but identifier is missing."}
    
            script_params = {}
            script_params["Mail ID"] = mail_id
            if wait_for_all_recipients_to_reply is not None:
                script_params["Wait for All Recipients to Reply?"] = wait_for_all_recipients_to_reply
            if wait_stage_exclude_pattern is not None:
                script_params["Wait Stage Exclude pattern"] = wait_stage_exclude_pattern
            if folder_to_check_for_reply is not None:
                script_params["Folder to Check for Reply"] = folder_to_check_for_reply
            if fetch_response_attachments is not None:
                script_params["Fetch Response Attachments"] = fetch_response_attachments
            if limit_the_amount_of_information_returned_in_the_json_result is not None:
                script_params["Limit the Amount of Information Returned in the JSON Result"] = limit_the_amount_of_information_returned_in_the_json_result
            if disable_the_action_json_result is not None:
                script_params["Disable the Action JSON Result"] = disable_the_action_json_result
    
            # Prepare data model for the API request
            action_data = ApiManualActionDataModel(
                alertGroupIdentifiers=alert_group_identifiers,
                caseId=case_id,
                targetEntities=final_target_entities,
                scope=final_scope,
                isPredefinedScope=is_predefined_scope,
                actionProvider="Scripts",
                actionName="MicrosoftGraphMail_Wait For Email From User",
                properties={
                    "IntegrationInstance": instance_identifier,
                    "ScriptName": "MicrosoftGraphMail_Wait For Email From User",
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
                print(f"Error executing action MicrosoftGraphMail_Wait For Email From User for MicrosoftGraphMail: {e}")
                return {"Status": "Failed", "Message": f"Error executing action: {e}"}
        else:
            print(f"Warning: No active integration instance found for MicrosoftGraphMail")
            return {"Status": "Failed", "Message": "No active instance found."}

    @mcp.tool()
    async def microsoft_graph_mail_forward_email(case_id: Annotated[str, Field(..., description="The ID of the case.")], alert_group_identifiers: Annotated[List[str], Field(..., description="Identifiers for the alert groups.")], send_from: Annotated[str, Field(..., description="Specify the optional email address from which if permissions allow, email should be sent. By default, the email will be sent from the default mailbox specified in the integration configuration.")], mail_id: Annotated[str, Field(..., description="Specify the mail ids or internetMessageIds of the message that you want to forward.")], subject: Annotated[str, Field(..., description="Specify the mail subject part.")], send_to: Annotated[str, Field(..., description="Specify the arbitrary comma separated list of email addresses for the email recipients. For example: user1@company.co, user2@company.co")], mail_content: Annotated[str, Field(..., description="Specify the email body part.")], attachment_location: Annotated[List[str], Field(..., description="Location where the attachments to be added are stored. By default, the action attempts to get the attachment from the Google Cloud storage bucket, another option is to fetch it from the local file system.")], folder_name: Annotated[str, Field(default=None, description="Specify the mailbox folder to search in. '/' separator can be used to specify a subfolder to search in, example: Inbox/Subfolder")], cc: Annotated[str, Field(default=None, description="Specify the arbitrary comma separated list of email addresses to be put in the CC field of email. Format is the same as for the 'Send to' field.")], bcc: Annotated[str, Field(default=None, description="Arbitrary comma separated list of email addresses to be put in the BCC field of email. Format is the same as for the 'Send to' field.")], attachments_paths: Annotated[str, Field(default=None, description="Specify the attachments to be added, parameter expects full paths to be provided, for example: /<work directory>/file1.pdf. Parameter accepts multiple values as a comma separated string.")], target_entities: Annotated[List[TargetEntity], PydanticListField(TargetEntity, description="Optional list of specific target entities (Identifier, EntityType) to run the action on.")], scope: Annotated[str, Field(default="All entities", description="Defines the scope for the action.")]) -> dict:
        """Forward email including previous threads. If permissions allow, action can send an email from a mailbox different that is specified in the integration configuration. Note: Action is not running on Siemplify entities.

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
                Endpoints.LIST_INTEGRATION_INSTANCES.format(INTEGRATION_NAME="MicrosoftGraphMail")
            )
            instances = instance_response.get("integration_instances", [])
        except Exception as e:
            print(f"Error fetching instance for MicrosoftGraphMail: {e}")
            return {"Status": "Failed", "Message": f"Error fetching instance: {e}"}
    
        if instances:
            instance_identifier = instances[0].get("identifier")
            if not instance_identifier:
                return {"Status": "Failed", "Message": "Instance found but identifier is missing."}
    
            script_params = {}
            script_params["Send From"] = send_from
            script_params["Mail ID"] = mail_id
            if folder_name is not None:
                script_params["Folder Name"] = folder_name
            script_params["Subject"] = subject
            script_params["Send to"] = send_to
            if cc is not None:
                script_params["CC"] = cc
            if bcc is not None:
                script_params["BCC"] = bcc
            if attachments_paths is not None:
                script_params["Attachments Paths"] = attachments_paths
            script_params["Mail Content"] = mail_content
            script_params["Attachment Location"] = attachment_location
    
            # Prepare data model for the API request
            action_data = ApiManualActionDataModel(
                alertGroupIdentifiers=alert_group_identifiers,
                caseId=case_id,
                targetEntities=final_target_entities,
                scope=final_scope,
                isPredefinedScope=is_predefined_scope,
                actionProvider="Scripts",
                actionName="MicrosoftGraphMail_Forward Email",
                properties={
                    "IntegrationInstance": instance_identifier,
                    "ScriptName": "MicrosoftGraphMail_Forward Email",
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
                print(f"Error executing action MicrosoftGraphMail_Forward Email for MicrosoftGraphMail: {e}")
                return {"Status": "Failed", "Message": f"Error executing action: {e}"}
        else:
            print(f"Warning: No active integration instance found for MicrosoftGraphMail")
            return {"Status": "Failed", "Message": "No active instance found."}

    @mcp.tool()
    async def microsoft_graph_mail_move_email_to_folder(case_id: Annotated[str, Field(..., description="The ID of the case.")], alert_group_identifiers: Annotated[List[str], Field(..., description="Identifiers for the alert groups.")], move_in_mailbox: Annotated[str, Field(..., description="By default, move operation will be executed in the default mailbox specified in the integration configuration. If permissions allow, action can search in other mailboxes as well. If permissions allow, action can search in other mailboxes as well. Parameter accepts multiple values as a comma separated string.")], source_folder_name: Annotated[str, Field(..., description="Specify the source folder name to move mail from. '/' separator can be used to specify a subfolder to search in, example: Inbox/Subfolder")], destination_folder_name: Annotated[str, Field(..., description="Specify the destination folder name to move mail to. '/' separator can be used to specify a subfolder to search in, example: Inbox/Subfolder")], mail_i_ds: Annotated[str, Field(default=None, description="Specify the mail ids or internetMessageIds to search for. Parameter accepts multiple values as a comma separated string. If mail id or internet message id is provided, it takes priority for the search, subject and sender filters are ignored.")], subject_filter: Annotated[str, Field(default=None, description="Specify the subject of the email to search for. Filter works with \"contains\" logic.")], sender_filter: Annotated[str, Field(default=None, description="Specify the sender of the email to search for. Filter works with \"equals\" logic.")], time_frame_minutes: Annotated[str, Field(default=None, description="Specify time frame in minutes to search emails for.")], only_unread: Annotated[bool, Field(default=None, description="If enabled, action searches only for the unread emails.")], how_many_mailboxes_to_process_in_a_single_batch: Annotated[str, Field(default=None, description="Specify how many mailboxes action should process in a single batch (single connection to O365). If nothing is provided, default value of 25 will be used.")], limit_the_amount_of_information_returned_in_the_json_result: Annotated[bool, Field(default=None, description="If enabled, the amount of information returned by the action will be limited only to the key email fields.")], disable_the_action_json_result: Annotated[bool, Field(default=None, description="If enabled, action will not return JSON result.")], target_entities: Annotated[List[TargetEntity], PydanticListField(TargetEntity, description="Optional list of specific target entities (Identifier, EntityType) to run the action on.")], scope: Annotated[str, Field(default="All entities", description="Defines the scope for the action.")]) -> dict:
        """Move one or multiple emails from source email folder to another folder in the mailbox. If permissions allow, action can move emails in mailboxes other than the one provided in the integration configuration. Action is async, please adjust action timeout in IDE accordingly. Action is not working on Chronicle entities.

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
                Endpoints.LIST_INTEGRATION_INSTANCES.format(INTEGRATION_NAME="MicrosoftGraphMail")
            )
            instances = instance_response.get("integration_instances", [])
        except Exception as e:
            print(f"Error fetching instance for MicrosoftGraphMail: {e}")
            return {"Status": "Failed", "Message": f"Error fetching instance: {e}"}
    
        if instances:
            instance_identifier = instances[0].get("identifier")
            if not instance_identifier:
                return {"Status": "Failed", "Message": "Instance found but identifier is missing."}
    
            script_params = {}
            script_params["Move In Mailbox"] = move_in_mailbox
            script_params["Source Folder Name"] = source_folder_name
            script_params["Destination Folder Name"] = destination_folder_name
            if mail_i_ds is not None:
                script_params["Mail IDs"] = mail_i_ds
            if subject_filter is not None:
                script_params["Subject Filter"] = subject_filter
            if sender_filter is not None:
                script_params["Sender Filter"] = sender_filter
            if time_frame_minutes is not None:
                script_params["Time Frame (minutes)"] = time_frame_minutes
            if only_unread is not None:
                script_params["Only Unread"] = only_unread
            if how_many_mailboxes_to_process_in_a_single_batch is not None:
                script_params["How many mailboxes to process in a single batch"] = how_many_mailboxes_to_process_in_a_single_batch
            if limit_the_amount_of_information_returned_in_the_json_result is not None:
                script_params["Limit the Amount of Information Returned in the JSON Result"] = limit_the_amount_of_information_returned_in_the_json_result
            if disable_the_action_json_result is not None:
                script_params["Disable the Action JSON Result"] = disable_the_action_json_result
    
            # Prepare data model for the API request
            action_data = ApiManualActionDataModel(
                alertGroupIdentifiers=alert_group_identifiers,
                caseId=case_id,
                targetEntities=final_target_entities,
                scope=final_scope,
                isPredefinedScope=is_predefined_scope,
                actionProvider="Scripts",
                actionName="MicrosoftGraphMail_Move Email To Folder",
                properties={
                    "IntegrationInstance": instance_identifier,
                    "ScriptName": "MicrosoftGraphMail_Move Email To Folder",
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
                print(f"Error executing action MicrosoftGraphMail_Move Email To Folder for MicrosoftGraphMail: {e}")
                return {"Status": "Failed", "Message": f"Error executing action: {e}"}
        else:
            print(f"Warning: No active integration instance found for MicrosoftGraphMail")
            return {"Status": "Failed", "Message": "No active instance found."}

    @mcp.tool()
    async def microsoft_graph_mail_wait_for_vote_email_results(case_id: Annotated[str, Field(..., description="The ID of the case.")], alert_group_identifiers: Annotated[List[str], Field(..., description="Identifiers for the alert groups.")], vote_mail_sent_from: Annotated[str, Field(..., description="By default, the email is sent from the default mailbox specified in the integration configuration. In this parameter optionally a different value can be specified, if the vote mail was sent from a different mailbox.")], mail_id: Annotated[str, Field(..., description="ID or internetMessageId of the vote email that the action waits for. If the message was sent using Send Vote Email action, select SendVoteEmail.JSONResult|id or Send Email.JsonResult|internetMessageId field as a placeholder. The Search Emails action also can return email IDs.")], wait_for_all_recipients_to_reply: Annotated[bool, Field(default=None, description="If selected, the action waits for responses from all recipients until timeout and doesn't complete execution receiving the first response.")], wait_stage_exclude_pattern: Annotated[str, Field(default=None, description="Regular expression to exclude specific replies from the wait stage. The regular expression works with the email subject and body. For example, you can use this parameter to exclude  automatic Out of Office emails wait for an actual user reply.")], folder_to_check_for_reply: Annotated[str, Field(default=None, description="Email folder in the mailbox that was used to send the email with question to search for the user reply in. Parameter also accepts a comma separated list of folders to check the user response in multiple folders. '/' separator can be used to specify a subfolder to search in, example: Inbox/Subfolder")], folder_to_check_for_sent_mail: Annotated[str, Field(default=None, description="Parameter can be used to specify mailbox email folder (mailbox that was used to send the email with question) to search for the sent mail in this folder. Parameter also accepts a comma separated list of folders to check the user response in multiple folders. Parameter is case sensitive. '/' separator can be used to specify a subfolder to search in, example: Inbox/Subfolder")], fetch_response_attachments: Annotated[bool, Field(default=None, description="If selected and the recipient replies with an attachment, the action fetches the recipient response and adds it as an attachment for the action result.")], target_entities: Annotated[List[TargetEntity], PydanticListField(TargetEntity, description="Optional list of specific target entities (Identifier, EntityType) to run the action on.")], scope: Annotated[str, Field(default="All entities", description="Defines the scope for the action.")]) -> dict:
        """Wait for the user response based on the vote email sent using the Send Vote Email action. This action is asynchronous. Adjust the action timeout in the IDE accordingly. This action is not working on Google SecOps entities.

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
                Endpoints.LIST_INTEGRATION_INSTANCES.format(INTEGRATION_NAME="MicrosoftGraphMail")
            )
            instances = instance_response.get("integration_instances", [])
        except Exception as e:
            print(f"Error fetching instance for MicrosoftGraphMail: {e}")
            return {"Status": "Failed", "Message": f"Error fetching instance: {e}"}
    
        if instances:
            instance_identifier = instances[0].get("identifier")
            if not instance_identifier:
                return {"Status": "Failed", "Message": "Instance found but identifier is missing."}
    
            script_params = {}
            script_params["Vote Mail Sent From"] = vote_mail_sent_from
            script_params["Mail ID"] = mail_id
            if wait_for_all_recipients_to_reply is not None:
                script_params["Wait for All Recipients to Reply?"] = wait_for_all_recipients_to_reply
            if wait_stage_exclude_pattern is not None:
                script_params["Wait Stage Exclude pattern"] = wait_stage_exclude_pattern
            if folder_to_check_for_reply is not None:
                script_params["Folder to Check for Reply"] = folder_to_check_for_reply
            if folder_to_check_for_sent_mail is not None:
                script_params["Folder to check for Sent Mail"] = folder_to_check_for_sent_mail
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
                actionName="MicrosoftGraphMail_Wait For Vote Email Results",
                properties={
                    "IntegrationInstance": instance_identifier,
                    "ScriptName": "MicrosoftGraphMail_Wait For Vote Email Results",
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
                print(f"Error executing action MicrosoftGraphMail_Wait For Vote Email Results for MicrosoftGraphMail: {e}")
                return {"Status": "Failed", "Message": f"Error executing action: {e}"}
        else:
            print(f"Warning: No active integration instance found for MicrosoftGraphMail")
            return {"Status": "Failed", "Message": "No active instance found."}

    @mcp.tool()
    async def microsoft_graph_mail_send_email_html(case_id: Annotated[str, Field(..., description="The ID of the case.")], alert_group_identifiers: Annotated[List[str], Field(..., description="Identifiers for the alert groups.")], send_from: Annotated[str, Field(..., description="Optional email address to send an email from (if permissions allow it). By default, the email is sent from the default mailbox specified in the integration configuration.")], subject: Annotated[str, Field(..., description="Email subject.")], send_to: Annotated[str, Field(..., description="Specify the arbitrary comma-separated list of email addresses for the email recipients,for example, user1@company.co, user2@company.co.")], email_html_template: Annotated[EmailContent, Field(..., description="The question you would like to ask, or describe the decision you would like the recipient to be able to respond to")], attachment_location: Annotated[List[str], Field(..., description="Location where the attachments to be added are stored. By default, the action attempts to get the attachment from the Google Cloud storage bucket, another option is to fetch it from the local file system.")], cc: Annotated[str, Field(default=None, description="Arbitrary comma-separated list of email addresses to use in the CC email field. Use the same format as for the \"Send to\" field.")], bcc: Annotated[str, Field(default=None, description="Arbitrary comma-separated list of email addresses to use in the BCC email field. Use the same format for the \"Send to\" field.")], attachments_paths: Annotated[str, Field(default=None, description="Specify the attachments to be added, parameter expects full paths to be provided, for example: /<work directory>/file1.pdf. Parameter accepts multiple values as a comma separated string.")], reply_to_recipients: Annotated[str, Field(default=None, description="Comma-separated list of recipients used in the Reply-To header. Note: The Reply-To header is added to force email replies to specific email addresses instead of the email sender address stated in the From field.")], target_entities: Annotated[List[TargetEntity], PydanticListField(TargetEntity, description="Optional list of specific target entities (Identifier, EntityType) to run the action on.")], scope: Annotated[str, Field(default="All entities", description="Defines the scope for the action.")]) -> dict:
        """Send email with the Google SecOps HTML template from a specific mailbox to an arbitrary list of recipients. If permissions allow, the action sends an email from a mailbox different than the one specified in the integration configuration. Note: Action is not running on Google SecOps entities.

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
                Endpoints.LIST_INTEGRATION_INSTANCES.format(INTEGRATION_NAME="MicrosoftGraphMail")
            )
            instances = instance_response.get("integration_instances", [])
        except Exception as e:
            print(f"Error fetching instance for MicrosoftGraphMail: {e}")
            return {"Status": "Failed", "Message": f"Error fetching instance: {e}"}
    
        if instances:
            instance_identifier = instances[0].get("identifier")
            if not instance_identifier:
                return {"Status": "Failed", "Message": "Instance found but identifier is missing."}
    
            script_params = {}
            script_params["Send From"] = send_from
            script_params["Subject"] = subject
            script_params["Send to"] = send_to
            if cc is not None:
                script_params["CC"] = cc
            if bcc is not None:
                script_params["BCC"] = bcc
            if attachments_paths is not None:
                script_params["Attachments Paths"] = attachments_paths
            email_html_template = email_html_template.model_dump()
            script_params["Email HTML Template"] = email_html_template
            if reply_to_recipients is not None:
                script_params["Reply-To Recipients"] = reply_to_recipients
            script_params["Attachment Location"] = attachment_location
    
            # Prepare data model for the API request
            action_data = ApiManualActionDataModel(
                alertGroupIdentifiers=alert_group_identifiers,
                caseId=case_id,
                targetEntities=final_target_entities,
                scope=final_scope,
                isPredefinedScope=is_predefined_scope,
                actionProvider="Scripts",
                actionName="MicrosoftGraphMail_Send Email HTML",
                properties={
                    "IntegrationInstance": instance_identifier,
                    "ScriptName": "MicrosoftGraphMail_Send Email HTML",
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
                print(f"Error executing action MicrosoftGraphMail_Send Email HTML for MicrosoftGraphMail: {e}")
                return {"Status": "Failed", "Message": f"Error executing action: {e}"}
        else:
            print(f"Warning: No active integration instance found for MicrosoftGraphMail")
            return {"Status": "Failed", "Message": "No active instance found."}

    @mcp.tool()
    async def microsoft_graph_mail_ping(case_id: Annotated[str, Field(..., description="The ID of the case.")], alert_group_identifiers: Annotated[List[str], Field(..., description="Identifiers for the alert groups.")], target_entities: Annotated[List[TargetEntity], PydanticListField(TargetEntity, description="Optional list of specific target entities (Identifier, EntityType) to run the action on.")], scope: Annotated[str, Field(default="All entities", description="Defines the scope for the action.")]) -> dict:
        """Test Connectivity

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
                Endpoints.LIST_INTEGRATION_INSTANCES.format(INTEGRATION_NAME="MicrosoftGraphMail")
            )
            instances = instance_response.get("integration_instances", [])
        except Exception as e:
            print(f"Error fetching instance for MicrosoftGraphMail: {e}")
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
                actionName="MicrosoftGraphMail_Ping",
                properties={
                    "IntegrationInstance": instance_identifier,
                    "ScriptName": "MicrosoftGraphMail_Ping",
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
                print(f"Error executing action MicrosoftGraphMail_Ping for MicrosoftGraphMail: {e}")
                return {"Status": "Failed", "Message": f"Error executing action: {e}"}
        else:
            print(f"Warning: No active integration instance found for MicrosoftGraphMail")
            return {"Status": "Failed", "Message": "No active instance found."}

    @mcp.tool()
    async def microsoft_graph_mail_search_emails(case_id: Annotated[str, Field(..., description="The ID of the case.")], alert_group_identifiers: Annotated[List[str], Field(..., description="Identifiers for the alert groups.")], search_in_mailbox: Annotated[str, Field(..., description="By default, the search will be executed in the default mailbox specified in the integration configuration. If permissions allow, action can search in other mailboxes as well. Parameter accepts multiple values as a comma separated string. Note that it\u2019s not recommended to perform a search against a big number of mailboxes with this action, for complex searches it is recommended to use Exchange Extension Pack.")], folder_name: Annotated[str, Field(..., description="Specify the mailbox folder to search in. '/' separator can be used to specify a subfolder to search in, example: Inbox/Subfolder")], subject_filter: Annotated[str, Field(default=None, description="Specify the subject of the email to search for. Filter works with \u201ccontains\u201d logic.")], sender_filter: Annotated[str, Field(default=None, description="Specify the sender of the email to search for. Filter works with \u201cequals\u201d logic.")], time_frame_minutes: Annotated[str, Field(default=None, description="Specify time frame in minutes to search emails for.")], max_emails_to_return: Annotated[str, Field(default=None, description="Specify how many emails action should return. If value is not provided, API default is used.")], only_unread: Annotated[bool, Field(default=None, description="If enabled, action will search only for unread emails.")], select_all_fields_for_return: Annotated[bool, Field(default=None, description="If enabled, action will return all available fields for the found email.")], how_many_mailboxes_to_process_in_a_single_batch: Annotated[str, Field(default=None, description="Specify how many mailboxes action should process in a single batch (single connection to O365). If nothing is provided, default value of 25 will be used.")], limit_the_amount_of_information_returned_in_the_json_result: Annotated[bool, Field(default=None, description="If enabled, the amount of information returned by the action will be limited only to the key email fields.")], disable_the_action_json_result: Annotated[bool, Field(default=None, description="If enabled, action will not return JSON result.")], target_entities: Annotated[List[TargetEntity], PydanticListField(TargetEntity, description="Optional list of specific target entities (Identifier, EntityType) to run the action on.")], scope: Annotated[str, Field(default="All entities", description="Defines the scope for the action.")]) -> dict:
        """Execute email search in the configured mailbox based on provided search criteria. If permissions allow, action can search in mailboxes other than the one provided in the integration configuration. Action is async, please adjust action timeout in IDE accordingly. Action is not working on Chronicle entities. 

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
                Endpoints.LIST_INTEGRATION_INSTANCES.format(INTEGRATION_NAME="MicrosoftGraphMail")
            )
            instances = instance_response.get("integration_instances", [])
        except Exception as e:
            print(f"Error fetching instance for MicrosoftGraphMail: {e}")
            return {"Status": "Failed", "Message": f"Error fetching instance: {e}"}
    
        if instances:
            instance_identifier = instances[0].get("identifier")
            if not instance_identifier:
                return {"Status": "Failed", "Message": "Instance found but identifier is missing."}
    
            script_params = {}
            script_params["Search in Mailbox"] = search_in_mailbox
            script_params["Folder Name"] = folder_name
            if subject_filter is not None:
                script_params["Subject Filter"] = subject_filter
            if sender_filter is not None:
                script_params["Sender Filter"] = sender_filter
            if time_frame_minutes is not None:
                script_params["Time Frame (minutes)"] = time_frame_minutes
            if max_emails_to_return is not None:
                script_params["Max Emails To Return"] = max_emails_to_return
            if only_unread is not None:
                script_params["Only Unread"] = only_unread
            if select_all_fields_for_return is not None:
                script_params["Select All Fields For Return"] = select_all_fields_for_return
            if how_many_mailboxes_to_process_in_a_single_batch is not None:
                script_params["How many mailboxes to process in a single batch"] = how_many_mailboxes_to_process_in_a_single_batch
            if limit_the_amount_of_information_returned_in_the_json_result is not None:
                script_params["Limit the Amount of Information Returned in the JSON Result"] = limit_the_amount_of_information_returned_in_the_json_result
            if disable_the_action_json_result is not None:
                script_params["Disable the Action JSON Result"] = disable_the_action_json_result
    
            # Prepare data model for the API request
            action_data = ApiManualActionDataModel(
                alertGroupIdentifiers=alert_group_identifiers,
                caseId=case_id,
                targetEntities=final_target_entities,
                scope=final_scope,
                isPredefinedScope=is_predefined_scope,
                actionProvider="Scripts",
                actionName="MicrosoftGraphMail_Search Emails",
                properties={
                    "IntegrationInstance": instance_identifier,
                    "ScriptName": "MicrosoftGraphMail_Search Emails",
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
                print(f"Error executing action MicrosoftGraphMail_Search Emails for MicrosoftGraphMail: {e}")
                return {"Status": "Failed", "Message": f"Error executing action: {e}"}
        else:
            print(f"Warning: No active integration instance found for MicrosoftGraphMail")
            return {"Status": "Failed", "Message": "No active instance found."}

    @mcp.tool()
    async def microsoft_graph_mail_save_email_to_the_case(case_id: Annotated[str, Field(..., description="The ID of the case.")], alert_group_identifiers: Annotated[List[str], Field(..., description="Identifiers for the alert groups.")], search_in_mailbox: Annotated[str, Field(..., description="By default, action will try to search for email in the default mailbox specified in the integration configuration. If permissions allow, action can search in other mailboxes as well.")], mail_id: Annotated[str, Field(..., description="Specify the mail id or internetMessageId to save email and attachments to the case. If the message has been sent using Send Email action, please select SendEmail.JSONResult|id or Send Email.JsonResult|internetMessageId field as a placeholder. Search Emails action also can return ids for emails.")], folder_name: Annotated[str, Field(default=None, description="Specify the mailbox folder to search in. '/' separator can be used to specify a subfolder to search in, example: Inbox/Subfolder")], save_only_email_attachments: Annotated[bool, Field(default=None, description="If enabled, action will save only attachments of the specified email.")], attachment_to_save: Annotated[str, Field(default=None, description="If \"Save Only Email Attachments\" checkbox is enabled, action can save only specific attachments that are specified in this parameter. Parameter accepts multiple values as a comma-separated string.")], base64_encode: Annotated[bool, Field(default=None, description="If enabled, encode the email file to base64 encoding.")], save_email_to_the_case_wall: Annotated[bool, Field(default=None, description="If enabled, save the Email directly to the SecOps Case Wall.")], target_entities: Annotated[List[TargetEntity], PydanticListField(TargetEntity, description="Optional list of specific target entities (Identifier, EntityType) to run the action on.")], scope: Annotated[str, Field(default="All entities", description="Defines the scope for the action.")]) -> dict:
        """Save email or email attachments to the Chronicle Case Wall. If permissions allow, action can save emails from mailboxes other than the one provided in the integration configuration. Action is not working on Chronicle entities.

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
                Endpoints.LIST_INTEGRATION_INSTANCES.format(INTEGRATION_NAME="MicrosoftGraphMail")
            )
            instances = instance_response.get("integration_instances", [])
        except Exception as e:
            print(f"Error fetching instance for MicrosoftGraphMail: {e}")
            return {"Status": "Failed", "Message": f"Error fetching instance: {e}"}
    
        if instances:
            instance_identifier = instances[0].get("identifier")
            if not instance_identifier:
                return {"Status": "Failed", "Message": "Instance found but identifier is missing."}
    
            script_params = {}
            script_params["Search In Mailbox"] = search_in_mailbox
            if folder_name is not None:
                script_params["Folder Name"] = folder_name
            script_params["Mail ID"] = mail_id
            if save_only_email_attachments is not None:
                script_params["Save Only Email Attachments"] = save_only_email_attachments
            if attachment_to_save is not None:
                script_params["Attachment To Save"] = attachment_to_save
            if base64_encode is not None:
                script_params["Base64 Encode"] = base64_encode
            if save_email_to_the_case_wall is not None:
                script_params["Save Email to the Case Wall"] = save_email_to_the_case_wall
    
            # Prepare data model for the API request
            action_data = ApiManualActionDataModel(
                alertGroupIdentifiers=alert_group_identifiers,
                caseId=case_id,
                targetEntities=final_target_entities,
                scope=final_scope,
                isPredefinedScope=is_predefined_scope,
                actionProvider="Scripts",
                actionName="MicrosoftGraphMail_Save Email to the Case",
                properties={
                    "IntegrationInstance": instance_identifier,
                    "ScriptName": "MicrosoftGraphMail_Save Email to the Case",
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
                print(f"Error executing action MicrosoftGraphMail_Save Email to the Case for MicrosoftGraphMail: {e}")
                return {"Status": "Failed", "Message": f"Error executing action: {e}"}
        else:
            print(f"Warning: No active integration instance found for MicrosoftGraphMail")
            return {"Status": "Failed", "Message": "No active instance found."}

    @mcp.tool()
    async def microsoft_graph_mail_send_email(case_id: Annotated[str, Field(..., description="The ID of the case.")], alert_group_identifiers: Annotated[List[str], Field(..., description="Identifiers for the alert groups.")], send_from: Annotated[str, Field(..., description="Specify the optional email address from which if permissions allow, email should be sent. By default, the email will be sent from the default mailbox specified in the integration configuration.")], subject: Annotated[str, Field(..., description="Specify the mail subject part.")], send_to: Annotated[str, Field(..., description="Specify the arbitrary comma separated list of email addresses for the email recipients. For example: user1@company.co, user2@company.co")], mail_content: Annotated[str, Field(..., description="Specify the email body part.")], attachment_location: Annotated[List[str], Field(..., description="Location where the attachments to be added are stored. By default, the action attempts to get the attachment from the Google Cloud storage bucket, another option is to fetch it from the local file system.")], cc: Annotated[str, Field(default=None, description="Specify the arbitrary comma separated list of email addresses to be put in the CC field of email. Format is the same as for the \"Send to\" field.")], bcc: Annotated[str, Field(default=None, description="Arbitrary comma separated list of email addresses to be put in the BCC field of email. Format is the same as for the \"Send to\" field.")], attachments_paths: Annotated[str, Field(default=None, description="Specify the attachments to be added, parameter expects full paths to be provided, for example: /<work directory>/file1.pdf. Parameter accepts multiple values as a comma separated string.")], mail_content_type: Annotated[List[str], Field(default=None, description="Specify the type of email content: either plain text or html.")], reply_to_recipients: Annotated[str, Field(default=None, description="Specify a comma-separated list of recipients that will be used in the \"Reply-To\" header. Note: The Reply-To header is added when the originator of the message wants any replies to the message to go to that particular email address rather than the one in the \"From:\" address.")], target_entities: Annotated[List[TargetEntity], PydanticListField(TargetEntity, description="Optional list of specific target entities (Identifier, EntityType) to run the action on.")], scope: Annotated[str, Field(default="All entities", description="Defines the scope for the action.")]) -> dict:
        """Send email from a specific mailbox to an arbitrary list of recipients. Action can send either plain text or html emails. If permissions allow, action can send an email from a mailbox different that is specified in the integration configuration. Note: Action is not running on Chronicle entities.

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
                Endpoints.LIST_INTEGRATION_INSTANCES.format(INTEGRATION_NAME="MicrosoftGraphMail")
            )
            instances = instance_response.get("integration_instances", [])
        except Exception as e:
            print(f"Error fetching instance for MicrosoftGraphMail: {e}")
            return {"Status": "Failed", "Message": f"Error fetching instance: {e}"}
    
        if instances:
            instance_identifier = instances[0].get("identifier")
            if not instance_identifier:
                return {"Status": "Failed", "Message": "Instance found but identifier is missing."}
    
            script_params = {}
            script_params["Send From"] = send_from
            script_params["Subject"] = subject
            script_params["Send to"] = send_to
            if cc is not None:
                script_params["CC"] = cc
            if bcc is not None:
                script_params["BCC"] = bcc
            if attachments_paths is not None:
                script_params["Attachments Paths"] = attachments_paths
            if mail_content_type is not None:
                script_params["Mail Content Type"] = mail_content_type
            script_params["Mail Content"] = mail_content
            if reply_to_recipients is not None:
                script_params["Reply-To Recipients"] = reply_to_recipients
            script_params["Attachment Location"] = attachment_location
    
            # Prepare data model for the API request
            action_data = ApiManualActionDataModel(
                alertGroupIdentifiers=alert_group_identifiers,
                caseId=case_id,
                targetEntities=final_target_entities,
                scope=final_scope,
                isPredefinedScope=is_predefined_scope,
                actionProvider="Scripts",
                actionName="MicrosoftGraphMail_Send Email",
                properties={
                    "IntegrationInstance": instance_identifier,
                    "ScriptName": "MicrosoftGraphMail_Send Email",
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
                print(f"Error executing action MicrosoftGraphMail_Send Email for MicrosoftGraphMail: {e}")
                return {"Status": "Failed", "Message": f"Error executing action: {e}"}
        else:
            print(f"Warning: No active integration instance found for MicrosoftGraphMail")
            return {"Status": "Failed", "Message": "No active instance found."}

    @mcp.tool()
    async def microsoft_graph_mail_get_mailbox_account_out_of_facility_settings(case_id: Annotated[str, Field(..., description="The ID of the case.")], alert_group_identifiers: Annotated[List[str], Field(..., description="Identifiers for the alert groups.")], target_entities: Annotated[List[TargetEntity], PydanticListField(TargetEntity, description="Optional list of specific target entities (Identifier, EntityType) to run the action on.")], scope: Annotated[str, Field(default="All entities", description="Defines the scope for the action.")]) -> dict:
        """Get the mailbox account out of facility (OOF) settings for the provided Google SecOps User entity. Note: This action uses the beta version of Microsoft Graph APIs.

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
                Endpoints.LIST_INTEGRATION_INSTANCES.format(INTEGRATION_NAME="MicrosoftGraphMail")
            )
            instances = instance_response.get("integration_instances", [])
        except Exception as e:
            print(f"Error fetching instance for MicrosoftGraphMail: {e}")
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
                actionName="MicrosoftGraphMail_Get Mailbox Account Out Of Facility Settings",
                properties={
                    "IntegrationInstance": instance_identifier,
                    "ScriptName": "MicrosoftGraphMail_Get Mailbox Account Out Of Facility Settings",
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
                print(f"Error executing action MicrosoftGraphMail_Get Mailbox Account Out Of Facility Settings for MicrosoftGraphMail: {e}")
                return {"Status": "Failed", "Message": f"Error executing action: {e}"}
        else:
            print(f"Warning: No active integration instance found for MicrosoftGraphMail")
            return {"Status": "Failed", "Message": "No active instance found."}

    @mcp.tool()
    async def microsoft_graph_mail_download_attachments_from_email(case_id: Annotated[str, Field(..., description="The ID of the case.")], alert_group_identifiers: Annotated[List[str], Field(..., description="Identifiers for the alert groups.")], search_in_mailbox: Annotated[str, Field(..., description="By default, the action  attempts to search for an email in the default mailbox specified in the integration configuration. If permissions allow, the action can execute search in other mailboxes. This parameter accepts multiple values as a comma-separated string.")], download_destination: Annotated[List[str], Field(..., description="Destination to save the downloaded attachments to. By default, the action attempts to save the attachment to the Google Cloud storage bucket. Saving an attachment to the local file system is a fallback option.")], download_path: Annotated[str, Field(..., description="Path to download attachments to. When saving attachments to the Google Cloud bucket or a local file system, the action expects download path to be specified in the unix-like format, for example, \u201c/tmp/test\u201d.")], folder_name: Annotated[str, Field(default=None, description="Specify the mailbox folder to search in. '/' separator can be used to specify a subfolder to search in, example: Inbox/Subfolder")], mail_i_ds: Annotated[str, Field(default=None, description="Specify the mail ids or internetMessageIds to search for. Parameter accepts multiple values as a comma separated string. If mail id or internet message id is provided, it takes priority for the search, subject and sender filters are ignored.")], subject_filter: Annotated[str, Field(default=None, description="Specify the subject of the email to search for. Filter works with \"contains\" logic.")], sender_filter: Annotated[str, Field(default=None, description="Specify the sender of the email to search for. Filter works with \"equals\" logic.")], download_attachments_from_eml: Annotated[bool, Field(default=None, description="If checked, the action downloads attachments from attached EML files.")], download_attachments_to_unique_path: Annotated[bool, Field(default=None, description="If checked, the action downloads attachments to the unique path under the path value provided in the \u201cDownload Path\u201d parameter to avoid overwiting of previously downloaded attachments.")], how_many_mailboxes_to_process_in_a_single_batch: Annotated[str, Field(default=None, description="Number of  mailboxes to process in a single batch (single connection to O365). If no value is provided, the default value of 25 mailboxes is used.")], target_entities: Annotated[List[TargetEntity], PydanticListField(TargetEntity, description="Optional list of specific target entities (Identifier, EntityType) to run the action on.")], scope: Annotated[str, Field(default="All entities", description="Defines the scope for the action.")]) -> dict:
        """Download attachments from an email based on the provided criteria. Note: Action is not running on SecOps entities. Action is running asynchronously. Adjust the script timeout value in the SecOps IDE for action as needed. If the downloaded attachments contain "/" or "\" characters in their names, the characters will be replaced with the '_' character.

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
                Endpoints.LIST_INTEGRATION_INSTANCES.format(INTEGRATION_NAME="MicrosoftGraphMail")
            )
            instances = instance_response.get("integration_instances", [])
        except Exception as e:
            print(f"Error fetching instance for MicrosoftGraphMail: {e}")
            return {"Status": "Failed", "Message": f"Error fetching instance: {e}"}
    
        if instances:
            instance_identifier = instances[0].get("identifier")
            if not instance_identifier:
                return {"Status": "Failed", "Message": "Instance found but identifier is missing."}
    
            script_params = {}
            script_params["Search In Mailbox"] = search_in_mailbox
            if folder_name is not None:
                script_params["Folder Name"] = folder_name
            script_params["Download Destination"] = download_destination
            script_params["Download Path"] = download_path
            if mail_i_ds is not None:
                script_params["Mail IDs"] = mail_i_ds
            if subject_filter is not None:
                script_params["Subject Filter"] = subject_filter
            if sender_filter is not None:
                script_params["Sender Filter"] = sender_filter
            if download_attachments_from_eml is not None:
                script_params["Download Attachments from EML"] = download_attachments_from_eml
            if download_attachments_to_unique_path is not None:
                script_params["Download Attachments to unique path?"] = download_attachments_to_unique_path
            if how_many_mailboxes_to_process_in_a_single_batch is not None:
                script_params["How many mailboxes to process in a single batch"] = how_many_mailboxes_to_process_in_a_single_batch
    
            # Prepare data model for the API request
            action_data = ApiManualActionDataModel(
                alertGroupIdentifiers=alert_group_identifiers,
                caseId=case_id,
                targetEntities=final_target_entities,
                scope=final_scope,
                isPredefinedScope=is_predefined_scope,
                actionProvider="Scripts",
                actionName="MicrosoftGraphMail_Download Attachments from Email",
                properties={
                    "IntegrationInstance": instance_identifier,
                    "ScriptName": "MicrosoftGraphMail_Download Attachments from Email",
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
                print(f"Error executing action MicrosoftGraphMail_Download Attachments from Email for MicrosoftGraphMail: {e}")
                return {"Status": "Failed", "Message": f"Error executing action: {e}"}
        else:
            print(f"Warning: No active integration instance found for MicrosoftGraphMail")
            return {"Status": "Failed", "Message": "No active instance found."}

    @mcp.tool()
    async def microsoft_graph_mail_delete_email(case_id: Annotated[str, Field(..., description="The ID of the case.")], alert_group_identifiers: Annotated[List[str], Field(..., description="Identifiers for the alert groups.")], delete_in_mailbox: Annotated[str, Field(..., description="By default, delete operation will be executed in the default mailbox specified in the integration configuration. If permissions allow, action can search in other mailboxes as well. Parameter accepts multiple values as a comma separated string.")], folder_name: Annotated[str, Field(..., description="Specify the mailbox folder to search in. '/' separator can be used to specify a subfolder to search in, example: Inbox/Subfolder")], mail_i_ds: Annotated[str, Field(default=None, description="Specify the mail ids or internetMessageIds to search for. Parameter accepts multiple values as a comma separated string. If mail id or internet message id is provided, it takes priority for the search, subject and sender filters are ignored.")], subject_filter: Annotated[str, Field(default=None, description="Specify the subject of the email to search for. Filter works with \u201ccontains\u201d logic.")], sender_filter: Annotated[str, Field(default=None, description="Specify the sender of the email to search for. Filter works with \u201cequals\u201d logic.")], time_frame_minutes: Annotated[str, Field(default=None, description="Specify time frame in minutes to search emails for.")], only_unread: Annotated[bool, Field(default=None, description="If enabled, action searches only for the unread emails.")], how_many_mailboxes_to_process_in_a_single_batch: Annotated[str, Field(default=None, description="Specify how many mailboxes action should process in a single batch (single connection to O365). If nothing is provided, default value of 25 will be used.")], limit_the_amount_of_information_returned_in_the_json_result: Annotated[bool, Field(default=None, description="If enabled, the amount of information returned by the action will be limited only to the key email fields.")], disable_the_action_json_result: Annotated[bool, Field(default=None, description="If enabled, action will not return JSON result.")], target_entities: Annotated[List[TargetEntity], PydanticListField(TargetEntity, description="Optional list of specific target entities (Identifier, EntityType) to run the action on.")], scope: Annotated[str, Field(default="All entities", description="Defines the scope for the action.")]) -> dict:
        """Delete one or multiple emails from the mailbox based on provided search criteria. If permissions allow, action can move emails in mailboxes other than the one provided in the integration configuration. Action is async, please adjust action timeout in IDE accordingly. Action is not working on Chronicle entities.

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
                Endpoints.LIST_INTEGRATION_INSTANCES.format(INTEGRATION_NAME="MicrosoftGraphMail")
            )
            instances = instance_response.get("integration_instances", [])
        except Exception as e:
            print(f"Error fetching instance for MicrosoftGraphMail: {e}")
            return {"Status": "Failed", "Message": f"Error fetching instance: {e}"}
    
        if instances:
            instance_identifier = instances[0].get("identifier")
            if not instance_identifier:
                return {"Status": "Failed", "Message": "Instance found but identifier is missing."}
    
            script_params = {}
            script_params["Delete In Mailbox"] = delete_in_mailbox
            script_params["Folder Name"] = folder_name
            if mail_i_ds is not None:
                script_params["Mail IDs"] = mail_i_ds
            if subject_filter is not None:
                script_params["Subject Filter"] = subject_filter
            if sender_filter is not None:
                script_params["Sender Filter"] = sender_filter
            if time_frame_minutes is not None:
                script_params["Time Frame (minutes)"] = time_frame_minutes
            if only_unread is not None:
                script_params["Only Unread"] = only_unread
            if how_many_mailboxes_to_process_in_a_single_batch is not None:
                script_params["How many mailboxes to process in a single batch"] = how_many_mailboxes_to_process_in_a_single_batch
            if limit_the_amount_of_information_returned_in_the_json_result is not None:
                script_params["Limit the Amount of Information Returned in the JSON Result"] = limit_the_amount_of_information_returned_in_the_json_result
            if disable_the_action_json_result is not None:
                script_params["Disable the Action JSON Result"] = disable_the_action_json_result
    
            # Prepare data model for the API request
            action_data = ApiManualActionDataModel(
                alertGroupIdentifiers=alert_group_identifiers,
                caseId=case_id,
                targetEntities=final_target_entities,
                scope=final_scope,
                isPredefinedScope=is_predefined_scope,
                actionProvider="Scripts",
                actionName="MicrosoftGraphMail_Delete Email",
                properties={
                    "IntegrationInstance": instance_identifier,
                    "ScriptName": "MicrosoftGraphMail_Delete Email",
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
                print(f"Error executing action MicrosoftGraphMail_Delete Email for MicrosoftGraphMail: {e}")
                return {"Status": "Failed", "Message": f"Error executing action: {e}"}
        else:
            print(f"Warning: No active integration instance found for MicrosoftGraphMail")
            return {"Status": "Failed", "Message": "No active instance found."}

    @mcp.tool()
    async def microsoft_graph_mail_mark_email_as_junk(case_id: Annotated[str, Field(..., description="The ID of the case.")], alert_group_identifiers: Annotated[List[str], Field(..., description="Identifiers for the alert groups.")], search_in_mailbox: Annotated[str, Field(..., description="A mailbox to search for an email in. By default, the action  attempts to search for the email in the default mailbox that you specified in the integration configuration. With correct permissions, the action can execute a search in other mailboxes. Parameter accepts multiple values as a comma separated string.")], folder_name: Annotated[str, Field(..., description="A mailbox folder to search in.")], mail_i_ds: Annotated[str, Field(..., description="Specify the mail ids or internetMessageIds to mark as junk. Parameter accepts multiple values as a comma separated string.")], target_entities: Annotated[List[TargetEntity], PydanticListField(TargetEntity, description="Optional list of specific target entities (Identifier, EntityType) to run the action on.")], scope: Annotated[str, Field(default="All entities", description="Defines the scope for the action.")]) -> dict:
        """Mark an email as junk for a specific mailbox. This action adds the email sender to the list of blocked senders and moves the message to the Junk Email folder. Note: This action uses the beta version of Microsoft Graph APIs and is not running on Google SecOps entities.

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
                Endpoints.LIST_INTEGRATION_INSTANCES.format(INTEGRATION_NAME="MicrosoftGraphMail")
            )
            instances = instance_response.get("integration_instances", [])
        except Exception as e:
            print(f"Error fetching instance for MicrosoftGraphMail: {e}")
            return {"Status": "Failed", "Message": f"Error fetching instance: {e}"}
    
        if instances:
            instance_identifier = instances[0].get("identifier")
            if not instance_identifier:
                return {"Status": "Failed", "Message": "Instance found but identifier is missing."}
    
            script_params = {}
            script_params["Search In Mailbox"] = search_in_mailbox
            script_params["Folder Name"] = folder_name
            script_params["Mail IDs"] = mail_i_ds
    
            # Prepare data model for the API request
            action_data = ApiManualActionDataModel(
                alertGroupIdentifiers=alert_group_identifiers,
                caseId=case_id,
                targetEntities=final_target_entities,
                scope=final_scope,
                isPredefinedScope=is_predefined_scope,
                actionProvider="Scripts",
                actionName="MicrosoftGraphMail_Mark Email as Junk",
                properties={
                    "IntegrationInstance": instance_identifier,
                    "ScriptName": "MicrosoftGraphMail_Mark Email as Junk",
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
                print(f"Error executing action MicrosoftGraphMail_Mark Email as Junk for MicrosoftGraphMail: {e}")
                return {"Status": "Failed", "Message": f"Error executing action: {e}"}
        else:
            print(f"Warning: No active integration instance found for MicrosoftGraphMail")
            return {"Status": "Failed", "Message": "No active instance found."}

    @mcp.tool()
    async def microsoft_graph_mail_extract_data_from_attached_eml(case_id: Annotated[str, Field(..., description="The ID of the case.")], alert_group_identifiers: Annotated[List[str], Field(..., description="Identifiers for the alert groups.")], search_in_mailbox: Annotated[str, Field(..., description="By default, the action attempts to search for an email in the default mailbox specified in the integration configuration. If permissions allow, the action can execute search in other mailboxes. This parameter accepts multiple values as a comma-separated string.")], mail_i_ds: Annotated[str, Field(..., description="Specify the mail ids or internetMessageIds to search for. This parameter accepts multiple values as a comma-separated string.")], folder_name: Annotated[str, Field(default=None, description="Specify the mailbox folder to search in. '/' separator can be used to specify a subfolder to search in, example: Inbox/Subfolder")], regex_map_json: Annotated[Union[str, dict], Field(default=None, description="JSON definition containing regular expressions to apply to the attached email file and produce additional key values in the action JSON result. Example of the JSON definition is as follows: {ips: \\b\\\\d{1,3}\\\\.\\\\d{1,3}\\\\.\\\\d{1,3}\\\\.\\\\d{1,3}\\b}")], target_entities: Annotated[List[TargetEntity], PydanticListField(TargetEntity, description="Optional list of specific target entities (Identifier, EntityType) to run the action on.")], scope: Annotated[str, Field(default="All entities", description="Defines the scope for the action.")]) -> dict:
        """Extract data from the email EML attachments and return it in the actions JSON result. The action supports .eml, .msg, .ics file formats. Note: Action is not running on SecOps entities.

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
                Endpoints.LIST_INTEGRATION_INSTANCES.format(INTEGRATION_NAME="MicrosoftGraphMail")
            )
            instances = instance_response.get("integration_instances", [])
        except Exception as e:
            print(f"Error fetching instance for MicrosoftGraphMail: {e}")
            return {"Status": "Failed", "Message": f"Error fetching instance: {e}"}
    
        if instances:
            instance_identifier = instances[0].get("identifier")
            if not instance_identifier:
                return {"Status": "Failed", "Message": "Instance found but identifier is missing."}
    
            script_params = {}
            script_params["Search In Mailbox"] = search_in_mailbox
            if folder_name is not None:
                script_params["Folder Name"] = folder_name
            script_params["Mail IDs"] = mail_i_ds
            if regex_map_json is not None:
                script_params["Regex Map JSON"] = regex_map_json
    
            # Prepare data model for the API request
            action_data = ApiManualActionDataModel(
                alertGroupIdentifiers=alert_group_identifiers,
                caseId=case_id,
                targetEntities=final_target_entities,
                scope=final_scope,
                isPredefinedScope=is_predefined_scope,
                actionProvider="Scripts",
                actionName="MicrosoftGraphMail_Extract Data from Attached EML",
                properties={
                    "IntegrationInstance": instance_identifier,
                    "ScriptName": "MicrosoftGraphMail_Extract Data from Attached EML",
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
                print(f"Error executing action MicrosoftGraphMail_Extract Data from Attached EML for MicrosoftGraphMail: {e}")
                return {"Status": "Failed", "Message": f"Error executing action: {e}"}
        else:
            print(f"Warning: No active integration instance found for MicrosoftGraphMail")
            return {"Status": "Failed", "Message": "No active instance found."}
