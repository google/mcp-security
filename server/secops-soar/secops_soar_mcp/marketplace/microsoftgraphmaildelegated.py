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
    # This function registers all tools (actions) for the MicrosoftGraphMailDelegated integration.

    @mcp.tool()
    async def microsoft_graph_mail_delegated_send_vote_email(case_id: Annotated[str, Field(..., description="The ID of the case.")], alert_group_identifiers: Annotated[List[str], Field(..., description="Identifiers for the alert groups.")], send_from: Annotated[str, Field(..., description="An optional email address from which to send an email if permissions allow it. By default, the email is sent from the default mailbox that is specified in the integration configuration.")], subject: Annotated[str, Field(..., description="The email subject.")], send_to: Annotated[str, Field(..., description="A comma-separated list of email addresses for the email recipients, such as user1@example.com, user2@example.com.")], email_html_template: Annotated[EmailContent, Field(..., description="The type of the HTML template to use. The default value is Email HTML Template.")], structure_of_voting_options: Annotated[List[str], Field(..., description="The structure of the vote to send to recipients. The possible values are Yes/No or Approve/Reject. The default value is Yes/No.")], attachment_location: Annotated[List[str], Field(..., description="A location where the attachments are stored. By default, the action attempts to upload attachments from the Cloud Storage bucket. The possible values are GCP Bucket or Local File System. The default value is GCP Bucket.")], cc: Annotated[str, Field(default=None, description="A comma-separated list of email addresses for the email CC field, such as user1@example.com, user2@example.com.")], bcc: Annotated[str, Field(default=None, description="A comma-separated list of email addresses for the email BCC field, such as user1@example.com, user2@example.com.")], attachments_paths: Annotated[str, Field(default=None, description="A comma-separated list of paths for file attachments stored on the server, for example, /{FILE_DIRECTORY}/file.pdf, /{FILE_DIRECTORY}/image.jpg.")], reply_to_recipients: Annotated[str, Field(default=None, description="A comma-separated list of recipients to use in the Reply-To header. Use the Reply-To header to redirect reply emails to the specific email address instead of the sender address that is stated in the From field.")], target_entities: Annotated[List[TargetEntity], PydanticListField(TargetEntity, description="Optional list of specific target entities (Identifier, EntityType) to run the action on.")], scope: Annotated[str, Field(default="All entities", description="Defines the scope for the action.")]) -> dict:
        """Use the Send Vote Email action to send emails with the predefined answering options. This action uses Google SecOps HTML templates to format the email. With appropriate permissions, the Send Vote Email action can send emails from a mailbox other than the default one. This action doesn't run on Google SecOps entities.

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
                Endpoints.LIST_INTEGRATION_INSTANCES.format(INTEGRATION_NAME="MicrosoftGraphMailDelegated")
            )
            instances = instance_response.get("integration_instances", [])
        except Exception as e:
            print(f"Error fetching instance for MicrosoftGraphMailDelegated: {e}")
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
                actionName="MicrosoftGraphMailDelegated_Send Vote Email",
                properties={
                    "IntegrationInstance": instance_identifier,
                    "ScriptName": "MicrosoftGraphMailDelegated_Send Vote Email",
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
                print(f"Error executing action MicrosoftGraphMailDelegated_Send Vote Email for MicrosoftGraphMailDelegated: {e}")
                return {"Status": "Failed", "Message": f"Error executing action: {e}"}
        else:
            print(f"Warning: No active integration instance found for MicrosoftGraphMailDelegated")
            return {"Status": "Failed", "Message": "No active instance found."}

    @mcp.tool()
    async def microsoft_graph_mail_delegated_mark_email_as_not_junk(case_id: Annotated[str, Field(..., description="The ID of the case.")], alert_group_identifiers: Annotated[List[str], Field(..., description="Identifiers for the alert groups.")], search_in_mailbox: Annotated[str, Field(..., description="A mailbox to search for an email in. By default, the action attempts to search for the email in the default mailbox that you specified in the integration configuration. To execute a search in other mailboxes, configure appropriate permissions for the action. This parameter accepts multiple values as a comma-separated string.")], folder_name: Annotated[str, Field(..., description="A mailbox folder in which to search for an email. To specify a subfolder, use the \u201c/\u201d forward slash, such as {Inbox/Subfolder}.")], mail_i_ds: Annotated[str, Field(..., description="A comma-separated string of the mail IDs or internetMessageId values of the emails to mark as not junk.")], target_entities: Annotated[List[TargetEntity], PydanticListField(TargetEntity, description="Optional list of specific target entities (Identifier, EntityType) to run the action on.")], scope: Annotated[str, Field(default="All entities", description="Defines the scope for the action.")]) -> dict:
        """Use the Mark Email as Not Junk action to mark emails as not junk in a specific mailbox. This action removes the sender from the list of blocked senders and moves the message to the Inbox folder. The Mark Email as Not Junk action uses the beta version of Microsoft Graph API. This action doesn't run on Google SecOps entities.

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
                Endpoints.LIST_INTEGRATION_INSTANCES.format(INTEGRATION_NAME="MicrosoftGraphMailDelegated")
            )
            instances = instance_response.get("integration_instances", [])
        except Exception as e:
            print(f"Error fetching instance for MicrosoftGraphMailDelegated: {e}")
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
                actionName="MicrosoftGraphMailDelegated_Mark Email as Not Junk",
                properties={
                    "IntegrationInstance": instance_identifier,
                    "ScriptName": "MicrosoftGraphMailDelegated_Mark Email as Not Junk",
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
                print(f"Error executing action MicrosoftGraphMailDelegated_Mark Email as Not Junk for MicrosoftGraphMailDelegated: {e}")
                return {"Status": "Failed", "Message": f"Error executing action: {e}"}
        else:
            print(f"Warning: No active integration instance found for MicrosoftGraphMailDelegated")
            return {"Status": "Failed", "Message": "No active instance found."}

    @mcp.tool()
    async def microsoft_graph_mail_delegated_send_thread_reply(case_id: Annotated[str, Field(..., description="The ID of the case.")], alert_group_identifiers: Annotated[List[str], Field(..., description="Identifiers for the alert groups.")], send_from: Annotated[str, Field(..., description="An optional email address from which to send emails if permissions allow it. By default, the action sends emails from the default mailbox that is specified in the integration configuration.")], mail_id: Annotated[str, Field(..., description="The email ID or the internetMessageId value of the email to reply to.")], folder_name: Annotated[str, Field(..., description="A mailbox folder in which to search for an email. To specify a subfolder, use the \u201c/\u201d forward slash, such as {Inbox/Subfolder}.")], mail_content: Annotated[str, Field(..., description="The email body.")], attachment_location: Annotated[List[str], Field(..., description="A location where the attachments are stored. By default, the action attempts to upload attachments from the Cloud Storage bucket. The possible values are GCP Bucket or Local File System. The default value is GCP Bucket.")], attachments_paths: Annotated[str, Field(default=None, description="A comma-separated list of paths for file attachments stored on the server, for example, /{FILE_DIRECTORY}/file.pdf, /{FILE_DIRECTORY}/image.jpg.")], reply_all: Annotated[bool, Field(default=None, description="If selected, the action sends a reply to all recipients related to the original email. Not selected by default. This parameter has priority over the Reply To parameter.")], reply_to: Annotated[str, Field(default=None, description="A comma-separated list of emails to reply to. If you don't set a value and the Reply All checkbox is clear, the action only sends a reply to the original email sender. If you select the Reply All checkbox, the action ignores this parameter.")], target_entities: Annotated[List[TargetEntity], PydanticListField(TargetEntity, description="Optional list of specific target entities (Identifier, EntityType) to run the action on.")], scope: Annotated[str, Field(default="All entities", description="Defines the scope for the action.")]) -> dict:
        """Use the Send Thread Reply action to send a message as a reply to the email thread. With appropriate permissions, the action can send emails from a mailbox other than the one specified in the integration configuration. This action doesn't run on Google SecOps entities.

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
                Endpoints.LIST_INTEGRATION_INSTANCES.format(INTEGRATION_NAME="MicrosoftGraphMailDelegated")
            )
            instances = instance_response.get("integration_instances", [])
        except Exception as e:
            print(f"Error fetching instance for MicrosoftGraphMailDelegated: {e}")
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
                actionName="MicrosoftGraphMailDelegated_Send Thread Reply",
                properties={
                    "IntegrationInstance": instance_identifier,
                    "ScriptName": "MicrosoftGraphMailDelegated_Send Thread Reply",
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
                print(f"Error executing action MicrosoftGraphMailDelegated_Send Thread Reply for MicrosoftGraphMailDelegated: {e}")
                return {"Status": "Failed", "Message": f"Error executing action: {e}"}
        else:
            print(f"Warning: No active integration instance found for MicrosoftGraphMailDelegated")
            return {"Status": "Failed", "Message": "No active instance found."}

    @mcp.tool()
    async def microsoft_graph_mail_delegated_wait_for_email_from_user(case_id: Annotated[str, Field(..., description="The ID of the case.")], alert_group_identifiers: Annotated[List[str], Field(..., description="Identifiers for the alert groups.")], mail_id: Annotated[str, Field(..., description="The ID of the email. If you used the Send Mail action to send emails, set the parameter value to the {SendEmail.JSONResult|id} or {SendEmail.JSONResult|internetMessageId} placeholder.")], wait_for_all_recipients_to_reply: Annotated[bool, Field(default=None, description="If selected, the action waits for responses from all recipients until reaching timeout or proceeding with the first reply.")], wait_stage_exclude_pattern: Annotated[str, Field(default=None, description="A regular expression to exclude specific replies from the wait stage. This parameter works with the email body. For example, if you configure the \u201cOut of Office.*\u201d regular expression, the action doesn't consider automatic out-of-office messages as recipient replies and waits for an actual user reply.")], folder_to_check_for_reply: Annotated[str, Field(default=None, description="A mailbox email folder to search for the user reply in. The search is run in the mailbox which the email containing a question was sent from. This parameter accepts a comma-separated list of folders to check the user response in multiple folders. This parameter is case-sensitive. The default value is Inbox.")], fetch_response_attachments: Annotated[bool, Field(default=None, description="If selected and the recipient reply contains attachments, the action fetches the reply and adds it as an attachment to the action result.")], limit_the_amount_of_information_returned_in_the_json_result: Annotated[bool, Field(default=None, description="If enabled, the amount of information returned by the action will be limited only to the key email fields.")], disable_the_action_json_result: Annotated[bool, Field(default=None, description="If enabled, action will not return JSON result.")], target_entities: Annotated[List[TargetEntity], PydanticListField(TargetEntity, description="Optional list of specific target entities (Identifier, EntityType) to run the action on.")], scope: Annotated[str, Field(default="All entities", description="Defines the scope for the action.")]) -> dict:
        """Use the Wait For Email From User action to wait for the user's response that is based on an email sent using the Send Email action. This action is asynchronous. Adjust the action timeout in the Google SecOps IDE accordingly. This action doesn't run on Google SecOps entities.

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
                Endpoints.LIST_INTEGRATION_INSTANCES.format(INTEGRATION_NAME="MicrosoftGraphMailDelegated")
            )
            instances = instance_response.get("integration_instances", [])
        except Exception as e:
            print(f"Error fetching instance for MicrosoftGraphMailDelegated: {e}")
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
                actionName="MicrosoftGraphMailDelegated_Wait For Email From User",
                properties={
                    "IntegrationInstance": instance_identifier,
                    "ScriptName": "MicrosoftGraphMailDelegated_Wait For Email From User",
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
                print(f"Error executing action MicrosoftGraphMailDelegated_Wait For Email From User for MicrosoftGraphMailDelegated: {e}")
                return {"Status": "Failed", "Message": f"Error executing action: {e}"}
        else:
            print(f"Warning: No active integration instance found for MicrosoftGraphMailDelegated")
            return {"Status": "Failed", "Message": "No active instance found."}

    @mcp.tool()
    async def microsoft_graph_mail_delegated_forward_email(case_id: Annotated[str, Field(..., description="The ID of the case.")], alert_group_identifiers: Annotated[List[str], Field(..., description="Identifiers for the alert groups.")], send_from: Annotated[str, Field(..., description="An optional email address from which to send an email if permissions allow it. By default, the email is sent from the default mailbox that is specified in the integration configuration.")], mail_id: Annotated[str, Field(..., description="The email ID or the internetMessageId value of the email to forward.")], subject: Annotated[str, Field(..., description="The email subject.")], send_to: Annotated[str, Field(..., description="A comma-separated list of email addresses for the email recipients, such as user1@example.com, user2@example.com.")], mail_content: Annotated[str, Field(..., description="The email body.")], attachment_location: Annotated[List[str], Field(..., description="A location where the attachments are stored. By default, the action attempts to upload attachments from the Cloud Storage bucket. The possible values are GCP Bucket or Local File System. The default value is GCP Bucket.")], folder_name: Annotated[str, Field(default=None, description="A mailbox folder in which to search for an email. To specify a subfolder, use the \u201c/\u201d forward slash, such as {Inbox/Subfolder}.")], cc: Annotated[str, Field(default=None, description="A comma-separated list of email addresses for the email CC field, such as user1@example.com, user2@example.com.")], bcc: Annotated[str, Field(default=None, description="A comma-separated list of email addresses for the email BCC field, such as user1@example.com, user2@example.com.")], attachments_paths: Annotated[str, Field(default=None, description="A comma-separated list of paths for file attachments stored on the server, for example, /{FILE_DIRECTORY}/file.pdf, /{FILE_DIRECTORY}/image.jpg.")], target_entities: Annotated[List[TargetEntity], PydanticListField(TargetEntity, description="Optional list of specific target entities (Identifier, EntityType) to run the action on.")], scope: Annotated[str, Field(default="All entities", description="Defines the scope for the action.")]) -> dict:
        """Use the Forward Email action to forward emails that include previous threads. With the appropriate permissions, this action can send emails from a mailbox different than the one specified in the integration configuration. This action doesn't run on Google SecOps entities.

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
                Endpoints.LIST_INTEGRATION_INSTANCES.format(INTEGRATION_NAME="MicrosoftGraphMailDelegated")
            )
            instances = instance_response.get("integration_instances", [])
        except Exception as e:
            print(f"Error fetching instance for MicrosoftGraphMailDelegated: {e}")
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
                actionName="MicrosoftGraphMailDelegated_Forward Email",
                properties={
                    "IntegrationInstance": instance_identifier,
                    "ScriptName": "MicrosoftGraphMailDelegated_Forward Email",
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
                print(f"Error executing action MicrosoftGraphMailDelegated_Forward Email for MicrosoftGraphMailDelegated: {e}")
                return {"Status": "Failed", "Message": f"Error executing action: {e}"}
        else:
            print(f"Warning: No active integration instance found for MicrosoftGraphMailDelegated")
            return {"Status": "Failed", "Message": "No active instance found."}

    @mcp.tool()
    async def microsoft_graph_mail_delegated_generate_token(case_id: Annotated[str, Field(..., description="The ID of the case.")], alert_group_identifiers: Annotated[List[str], Field(..., description="Identifiers for the alert groups.")], authorization_url: Annotated[str, Field(..., description="An authorization URL that you received in the Get Authorization action. The URL is required to request a refresh token.")], target_entities: Annotated[List[TargetEntity], PydanticListField(TargetEntity, description="Optional list of specific target entities (Identifier, EntityType) to run the action on.")], scope: Annotated[str, Field(default="All entities", description="Defines the scope for the action.")]) -> dict:
        """Use the Generate Token action to obtain a refresh token for the integration configuration with delegated authentication. Use the authorization URL that you received in the Get Authorization action. This action doesn't run on Google SecOps entities. After you generate the refresh token for the first time, we recommend you to configure and activate the Refresh Token Renewal Job so the job automatically renews and keeps the refresh token valid.

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
                Endpoints.LIST_INTEGRATION_INSTANCES.format(INTEGRATION_NAME="MicrosoftGraphMailDelegated")
            )
            instances = instance_response.get("integration_instances", [])
        except Exception as e:
            print(f"Error fetching instance for MicrosoftGraphMailDelegated: {e}")
            return {"Status": "Failed", "Message": f"Error fetching instance: {e}"}
    
        if instances:
            instance_identifier = instances[0].get("identifier")
            if not instance_identifier:
                return {"Status": "Failed", "Message": "Instance found but identifier is missing."}
    
            script_params = {}
            script_params["Authorization URL"] = authorization_url
    
            # Prepare data model for the API request
            action_data = ApiManualActionDataModel(
                alertGroupIdentifiers=alert_group_identifiers,
                caseId=case_id,
                targetEntities=final_target_entities,
                scope=final_scope,
                isPredefinedScope=is_predefined_scope,
                actionProvider="Scripts",
                actionName="MicrosoftGraphMailDelegated_Generate Token",
                properties={
                    "IntegrationInstance": instance_identifier,
                    "ScriptName": "MicrosoftGraphMailDelegated_Generate Token",
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
                print(f"Error executing action MicrosoftGraphMailDelegated_Generate Token for MicrosoftGraphMailDelegated: {e}")
                return {"Status": "Failed", "Message": f"Error executing action: {e}"}
        else:
            print(f"Warning: No active integration instance found for MicrosoftGraphMailDelegated")
            return {"Status": "Failed", "Message": "No active instance found."}

    @mcp.tool()
    async def microsoft_graph_mail_delegated_move_email_to_folder(case_id: Annotated[str, Field(..., description="The ID of the case.")], alert_group_identifiers: Annotated[List[str], Field(..., description="Identifiers for the alert groups.")], move_in_mailbox: Annotated[str, Field(..., description="The default mailbox to execute the move operation in. If permissions allow it, the action can search in other mailboxes as well. This parameter accepts multiple values as a comma-separated string.")], source_folder_name: Annotated[str, Field(..., description="A source folder from which to move the email. To specify a subfolder, use the \u201c/\u201d forward slash, such as {Inbox/Subfolder}.")], destination_folder_name: Annotated[str, Field(..., description="A destination folder to move the email to. Provide the parameter value in the following format: {Inbox/folder_name/subfolder_name}. This parameter is case-insensitive.")], mail_i_ds: Annotated[str, Field(default=None, description="A filter condition to search for emails with specific email IDs. This parameter accepts a comma-separated list of email IDs to search for. If you configure this parameter, the search ignores the Subject Filter and Sender Filter parameters.")], subject_filter: Annotated[str, Field(default=None, description="A filter condition that specifies the email subject to search for. This filter uses the contains logic.")], sender_filter: Annotated[str, Field(default=None, description="A filter condition that specifies the sender of requested emails. This filter uses the equals logic.")], time_frame_minutes: Annotated[str, Field(default=None, description="A filter condition that specifies the period in minutes to search for emails.")], only_unread: Annotated[bool, Field(default=None, description="If selected, the action searches only for unread emails.")], how_many_mailboxes_to_process_in_a_single_batch: Annotated[str, Field(default=None, description="The number of mailboxes to process in a single batch (a single connection to the Microsoft 365 server). The default value is 25.")], limit_the_amount_of_information_returned_in_the_json_result: Annotated[bool, Field(default=None, description="If enabled, the amount of information returned by the action will be limited only to the key email fields.")], disable_the_action_json_result: Annotated[bool, Field(default=None, description="If enabled, action will not return JSON result.")], target_entities: Annotated[List[TargetEntity], PydanticListField(TargetEntity, description="Optional list of specific target entities (Identifier, EntityType) to run the action on.")], scope: Annotated[str, Field(default="All entities", description="Defines the scope for the action.")]) -> dict:
        """Use the Move Email To Folder action to move one or multiple emails from the source email folder to the other folder in the mailbox. With the appropriate permissions, this action can move emails to other mailboxes different from the one that is provided in the integration configuration. This action is asynchronous. Adjust the action timeout in the Google SecOps IDE accordingly. This action doesn't run on Google SecOps entities.

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
                Endpoints.LIST_INTEGRATION_INSTANCES.format(INTEGRATION_NAME="MicrosoftGraphMailDelegated")
            )
            instances = instance_response.get("integration_instances", [])
        except Exception as e:
            print(f"Error fetching instance for MicrosoftGraphMailDelegated: {e}")
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
                actionName="MicrosoftGraphMailDelegated_Move Email To Folder",
                properties={
                    "IntegrationInstance": instance_identifier,
                    "ScriptName": "MicrosoftGraphMailDelegated_Move Email To Folder",
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
                print(f"Error executing action MicrosoftGraphMailDelegated_Move Email To Folder for MicrosoftGraphMailDelegated: {e}")
                return {"Status": "Failed", "Message": f"Error executing action: {e}"}
        else:
            print(f"Warning: No active integration instance found for MicrosoftGraphMailDelegated")
            return {"Status": "Failed", "Message": "No active instance found."}

    @mcp.tool()
    async def microsoft_graph_mail_delegated_wait_for_vote_email_results(case_id: Annotated[str, Field(..., description="The ID of the case.")], alert_group_identifiers: Annotated[List[str], Field(..., description="Identifiers for the alert groups.")], vote_mail_sent_from: Annotated[str, Field(..., description="The mailbox from which an email is sent using the Send Vote Email action. The default value is the mailbox that you specified in the integration configuration. Optionally, you can set a different value for this parameter if the vote mail is sent from a different mailbox.")], mail_id: Annotated[str, Field(..., description="The ID of the email. If the email is sent using the Send Vote Email action, set the parameter value to the SendVoteEmail.JSONResult|id or SendEmail.JSONResult|internetMessageId placeholder. To return email IDs, you can use the Search Emails action.")], wait_for_all_recipients_to_reply: Annotated[bool, Field(default=None, description="If selected, the action waits for responses from all recipients until reaching timeout or proceeding with the first reply. Selected by default.")], wait_stage_exclude_pattern: Annotated[str, Field(default=None, description="A regular expression to exclude specific replies from the wait stage. This parameter works with the email body. For example, if you configure the \u201cOut of Office.*\u201d regular expression, the action doesn't consider automatic out-of-office messages as recipient replies and waits for an actual user reply.")], folder_to_check_for_reply: Annotated[str, Field(default=None, description="A mailbox email folder to search for the user reply. The action searches in the mailbox from which you sent the email with a question. This parameter accepts a comma-separated list of folders to check the user response in multiple folders. To specify a subfolder, use the \u201c/\u201d forward slash, such as {Inbox/Subfolder}. This parameter is case-sensitive. The default value is Inbox.")], folder_to_check_for_sent_mail: Annotated[str, Field(default=None, description="A mailbox folder to search for the sent mail. The action searches in the mailbox from which you sent the email with a question. This parameter accepts a comma-separated list of folders to check the user response in multiple folders. To specify a subfolder, use the \u201c/\u201d forward slash, such as {Inbox/Subfolder}. This parameter is case-sensitive. The default value is Sent Items.")], fetch_response_attachments: Annotated[bool, Field(default=None, description="If selected and the recipient reply contains attachments, the action fetches the reply and adds it as an attachment to the action result.")], target_entities: Annotated[List[TargetEntity], PydanticListField(TargetEntity, description="Optional list of specific target entities (Identifier, EntityType) to run the action on.")], scope: Annotated[str, Field(default="All entities", description="Defines the scope for the action.")]) -> dict:
        """Use the Wait For Vote Email Results action to wait for the user response based on the vote email sent using the Send Vote Email action. This action is asynchronous. Adjust the action timeout in the Google SecOps IDE accordingly. This action doesn't run on Google SecOps entities.

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
                Endpoints.LIST_INTEGRATION_INSTANCES.format(INTEGRATION_NAME="MicrosoftGraphMailDelegated")
            )
            instances = instance_response.get("integration_instances", [])
        except Exception as e:
            print(f"Error fetching instance for MicrosoftGraphMailDelegated: {e}")
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
                actionName="MicrosoftGraphMailDelegated_Wait For Vote Email Results",
                properties={
                    "IntegrationInstance": instance_identifier,
                    "ScriptName": "MicrosoftGraphMailDelegated_Wait For Vote Email Results",
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
                print(f"Error executing action MicrosoftGraphMailDelegated_Wait For Vote Email Results for MicrosoftGraphMailDelegated: {e}")
                return {"Status": "Failed", "Message": f"Error executing action: {e}"}
        else:
            print(f"Warning: No active integration instance found for MicrosoftGraphMailDelegated")
            return {"Status": "Failed", "Message": "No active instance found."}

    @mcp.tool()
    async def microsoft_graph_mail_delegated_send_email_html(case_id: Annotated[str, Field(..., description="The ID of the case.")], alert_group_identifiers: Annotated[List[str], Field(..., description="Identifiers for the alert groups.")], send_from: Annotated[str, Field(..., description="An optional email address from which to send an email if permissions allow it. By default, the email is sent from the default mailbox that is specified in the integration configuration")], subject: Annotated[str, Field(..., description="The email subject.")], send_to: Annotated[str, Field(..., description="A comma-separated list of email addresses for the email recipients, such as user1@example.com, user2@example.com.")], email_html_template: Annotated[EmailContent, Field(..., description="The type of the HTML template to use. The default value is Email HTML Template.")], attachment_location: Annotated[List[str], Field(..., description="A location where the attachments are stored. By default, the action attempts to upload attachments from the Cloud Storage bucket. The possible values are GCP Bucket or Local File System. The default value is GCP Bucket.")], cc: Annotated[str, Field(default=None, description="A comma-separated list of email addresses for the email CC field, such as user1@example.com, user2@example.com.")], bcc: Annotated[str, Field(default=None, description="A comma-separated list of email addresses for the email BCC field, such as user1@example.com, user2@example.com.")], attachments_paths: Annotated[str, Field(default=None, description="A comma-separated list of paths for file attachments stored on the server, for example, /{FILE_DIRECTORY}/file.pdf, /{FILE_DIRECTORY}/image.jpg.")], reply_to_recipients: Annotated[str, Field(default=None, description="A comma-separated list of recipients to use in the Reply-To header. Use the Reply-To header to redirect reply emails to the specific email address instead of the sender address that is stated in the From field.")], target_entities: Annotated[List[TargetEntity], PydanticListField(TargetEntity, description="Optional list of specific target entities (Identifier, EntityType) to run the action on.")], scope: Annotated[str, Field(default="All entities", description="Defines the scope for the action.")]) -> dict:
        """Use the Send Email HTML action to send emails you use the Google SecOps HTML template from a specific mailbox to an arbitrary list of recipients. With appropriate permissions, the action can send emails from a mailbox other than the default one. This action doesn't run on Google SecOps entities.

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
                Endpoints.LIST_INTEGRATION_INSTANCES.format(INTEGRATION_NAME="MicrosoftGraphMailDelegated")
            )
            instances = instance_response.get("integration_instances", [])
        except Exception as e:
            print(f"Error fetching instance for MicrosoftGraphMailDelegated: {e}")
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
                actionName="MicrosoftGraphMailDelegated_Send Email HTML",
                properties={
                    "IntegrationInstance": instance_identifier,
                    "ScriptName": "MicrosoftGraphMailDelegated_Send Email HTML",
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
                print(f"Error executing action MicrosoftGraphMailDelegated_Send Email HTML for MicrosoftGraphMailDelegated: {e}")
                return {"Status": "Failed", "Message": f"Error executing action: {e}"}
        else:
            print(f"Warning: No active integration instance found for MicrosoftGraphMailDelegated")
            return {"Status": "Failed", "Message": "No active instance found."}

    @mcp.tool()
    async def microsoft_graph_mail_delegated_ping(case_id: Annotated[str, Field(..., description="The ID of the case.")], alert_group_identifiers: Annotated[List[str], Field(..., description="Identifiers for the alert groups.")], target_entities: Annotated[List[TargetEntity], PydanticListField(TargetEntity, description="Optional list of specific target entities (Identifier, EntityType) to run the action on.")], scope: Annotated[str, Field(default="All entities", description="Defines the scope for the action.")]) -> dict:
        """Use the Ping action to test connectivity to the Microsoft Graph mail service. This action doesn't run on Google SecOps entities.

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
                Endpoints.LIST_INTEGRATION_INSTANCES.format(INTEGRATION_NAME="MicrosoftGraphMailDelegated")
            )
            instances = instance_response.get("integration_instances", [])
        except Exception as e:
            print(f"Error fetching instance for MicrosoftGraphMailDelegated: {e}")
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
                actionName="MicrosoftGraphMailDelegated_Ping",
                properties={
                    "IntegrationInstance": instance_identifier,
                    "ScriptName": "MicrosoftGraphMailDelegated_Ping",
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
                print(f"Error executing action MicrosoftGraphMailDelegated_Ping for MicrosoftGraphMailDelegated: {e}")
                return {"Status": "Failed", "Message": f"Error executing action: {e}"}
        else:
            print(f"Warning: No active integration instance found for MicrosoftGraphMailDelegated")
            return {"Status": "Failed", "Message": "No active instance found."}

    @mcp.tool()
    async def microsoft_graph_mail_delegated_search_emails(case_id: Annotated[str, Field(..., description="The ID of the case.")], alert_group_identifiers: Annotated[List[str], Field(..., description="Identifiers for the alert groups.")], search_in_mailbox: Annotated[str, Field(..., description="The default mailbox to execute the search operation in. If permissions allow it, the action can search in other mailboxes. This parameter accepts multiple values as a comma-separated string. For complex searches against a significant number of mailboxes, use the Exchange Extension Pack integration.")], folder_name: Annotated[str, Field(..., description="A mailbox folder to execute the search in. To specify a subfolder, use the \u201c/\u201d forward slash, such as {Inbox/Subfolder}.")], subject_filter: Annotated[str, Field(default=None, description="A filter condition that specifies the email subject to search for. This filter uses the contains logic.")], sender_filter: Annotated[str, Field(default=None, description="A filter condition that specifies the sender of requested emails. This filter uses the equals logic.")], time_frame_minutes: Annotated[str, Field(default=None, description="A filter condition that specifies the period in minutes to search for emails.")], max_emails_to_return: Annotated[str, Field(default=None, description="The number of emails for the action to return. If you don't set a value, the action uses the API default value. The default value is 10.")], only_unread: Annotated[bool, Field(default=None, description="If selected, the action searches only for unread emails.")], select_all_fields_for_return: Annotated[bool, Field(default=None, description="If selected, the action returns all available fields for the obtained email.")], how_many_mailboxes_to_process_in_a_single_batch: Annotated[str, Field(default=None, description="The number of mailboxes to process in a single batch (a single connection to the Microsoft 365 server). The default value is 25.")], limit_the_amount_of_information_returned_in_the_json_result: Annotated[bool, Field(default=None, description="If enabled, the amount of information returned by the action will be limited only to the key email fields.")], disable_the_action_json_result: Annotated[bool, Field(default=None, description="If enabled, action will not return JSON result.")], target_entities: Annotated[List[TargetEntity], PydanticListField(TargetEntity, description="Optional list of specific target entities (Identifier, EntityType) to run the action on.")], scope: Annotated[str, Field(default="All entities", description="Defines the scope for the action.")]) -> dict:
        """Use the Search Emails action to execute email search in the default mailbox based on the provided search criteria. With appropriate permissions, this action can run a search in other mailboxes. This action is asynchronous. Adjust the action timeout in the Google SeOps IDE accordingly. This action doesn't run on Google SecOps entities.

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
                Endpoints.LIST_INTEGRATION_INSTANCES.format(INTEGRATION_NAME="MicrosoftGraphMailDelegated")
            )
            instances = instance_response.get("integration_instances", [])
        except Exception as e:
            print(f"Error fetching instance for MicrosoftGraphMailDelegated: {e}")
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
                actionName="MicrosoftGraphMailDelegated_Search Emails",
                properties={
                    "IntegrationInstance": instance_identifier,
                    "ScriptName": "MicrosoftGraphMailDelegated_Search Emails",
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
                print(f"Error executing action MicrosoftGraphMailDelegated_Search Emails for MicrosoftGraphMailDelegated: {e}")
                return {"Status": "Failed", "Message": f"Error executing action: {e}"}
        else:
            print(f"Warning: No active integration instance found for MicrosoftGraphMailDelegated")
            return {"Status": "Failed", "Message": "No active instance found."}

    @mcp.tool()
    async def microsoft_graph_mail_delegated_save_email_to_the_case(case_id: Annotated[str, Field(..., description="The ID of the case.")], alert_group_identifiers: Annotated[List[str], Field(..., description="Identifiers for the alert groups.")], search_in_mailbox: Annotated[str, Field(..., description="The default mailbox in which to execute the search operation. If permissions allow it, the action can search in other mailboxes.")], mail_id: Annotated[str, Field(..., description="The email ID or the internetMessageId value to search for. This parameter accepts a comma-separated list of email IDs to search for. If you used the Send Mail action to send emails, set the parameter value to the {SendEmail.JSONResult|id} or {SendEmail.JSONResult|internetMessageId}  placeholder.")], folder_name: Annotated[str, Field(default=None, description="A mailbox folder in which to search for an email. To specify a subfolder, use the \u201c/\u201d forward slash, such as {Inbox/Subfolder}.")], save_only_email_attachments: Annotated[bool, Field(default=None, description="If selected, the action saves only attachments from the specified email.")], attachment_to_save: Annotated[str, Field(default=None, description="If you select the Save Only Email Attachments parameter, the action only saves attachments specified by this parameter. This parameter accepts multiple values as a comma-separated string.")], base64_encode: Annotated[bool, Field(default=None, description="If selected, the action encodes the email file into the base64 format.")], save_email_to_the_case_wall: Annotated[bool, Field(default=None, description="If selected, the action saves the specified email to the action Case Wall in Google Secops.")], target_entities: Annotated[List[TargetEntity], PydanticListField(TargetEntity, description="Optional list of specific target entities (Identifier, EntityType) to run the action on.")], scope: Annotated[str, Field(default="All entities", description="Defines the scope for the action.")]) -> dict:
        """Use the Save Email To The Case action to save emails or email attachments to the Google SecOps Case Wall. With the appropriate permissions, this action can save emails from mailboxes other than the one provided in the integration configuration. This action doesn't run on Google SecOps entities.

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
                Endpoints.LIST_INTEGRATION_INSTANCES.format(INTEGRATION_NAME="MicrosoftGraphMailDelegated")
            )
            instances = instance_response.get("integration_instances", [])
        except Exception as e:
            print(f"Error fetching instance for MicrosoftGraphMailDelegated: {e}")
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
                actionName="MicrosoftGraphMailDelegated_Save Email to the Case",
                properties={
                    "IntegrationInstance": instance_identifier,
                    "ScriptName": "MicrosoftGraphMailDelegated_Save Email to the Case",
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
                print(f"Error executing action MicrosoftGraphMailDelegated_Save Email to the Case for MicrosoftGraphMailDelegated: {e}")
                return {"Status": "Failed", "Message": f"Error executing action: {e}"}
        else:
            print(f"Warning: No active integration instance found for MicrosoftGraphMailDelegated")
            return {"Status": "Failed", "Message": "No active instance found."}

    @mcp.tool()
    async def microsoft_graph_mail_delegated_send_email(case_id: Annotated[str, Field(..., description="The ID of the case.")], alert_group_identifiers: Annotated[List[str], Field(..., description="Identifiers for the alert groups.")], send_from: Annotated[str, Field(..., description="An optional email address from which to send emails if permissions allow it. By default, the action sends emails from the default mailbox specified in the integration configuration.")], subject: Annotated[str, Field(..., description="The email subject.")], send_to: Annotated[str, Field(..., description="A comma-separated list of email addresses for the email recipients, such as user1@example.com, user2@example.com.")], mail_content: Annotated[str, Field(..., description="The email body.")], attachment_location: Annotated[List[str], Field(..., description="A location where the attachments are stored. By default, the action attempts to upload attachments from the Cloud Storage bucket. The possible values are GCP Bucket or Local File System. The default value is GCP Bucket.")], cc: Annotated[str, Field(default=None, description="A comma-separated list of email addresses for the email CC field, such as user1@example.com, user2@example.com.")], bcc: Annotated[str, Field(default=None, description="A comma-separated list of email addresses for the email BCC field, such as user1@example.com, user2@example.com.")], attachments_paths: Annotated[str, Field(default=None, description="A comma-separated list of paths for file attachments stored on the server, for example, /{FILE_DIRECTORY}/file.pdf, /{FILE_DIRECTORY}/image.jpg.")], mail_content_type: Annotated[List[str], Field(default=None, description="The type of the email content. The default value is Text.")], reply_to_recipients: Annotated[str, Field(default=None, description="A comma-separated list of recipients to use in the Reply-To header. Use the Reply-To header to redirect reply emails to the specific email address instead of the sender address that is stated in the From field.")], target_entities: Annotated[List[TargetEntity], PydanticListField(TargetEntity, description="Optional list of specific target entities (Identifier, EntityType) to run the action on.")], scope: Annotated[str, Field(default="All entities", description="Defines the scope for the action.")]) -> dict:
        """Use the Send Email action to send emails from a specific mailbox to an arbitrary list of recipients. This action can send either plain text or HTML-formatted emails. With appropriate permissions, the action can send emails from a mailbox different than the one specified in the integration configuration. This action doesn't run on Google SecOps entities.

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
                Endpoints.LIST_INTEGRATION_INSTANCES.format(INTEGRATION_NAME="MicrosoftGraphMailDelegated")
            )
            instances = instance_response.get("integration_instances", [])
        except Exception as e:
            print(f"Error fetching instance for MicrosoftGraphMailDelegated: {e}")
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
                actionName="MicrosoftGraphMailDelegated_Send Email",
                properties={
                    "IntegrationInstance": instance_identifier,
                    "ScriptName": "MicrosoftGraphMailDelegated_Send Email",
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
                print(f"Error executing action MicrosoftGraphMailDelegated_Send Email for MicrosoftGraphMailDelegated: {e}")
                return {"Status": "Failed", "Message": f"Error executing action: {e}"}
        else:
            print(f"Warning: No active integration instance found for MicrosoftGraphMailDelegated")
            return {"Status": "Failed", "Message": "No active instance found."}

    @mcp.tool()
    async def microsoft_graph_mail_delegated_get_mailbox_account_out_of_facility_settings(case_id: Annotated[str, Field(..., description="The ID of the case.")], alert_group_identifiers: Annotated[List[str], Field(..., description="Identifiers for the alert groups.")], target_entities: Annotated[List[TargetEntity], PydanticListField(TargetEntity, description="Optional list of specific target entities (Identifier, EntityType) to run the action on.")], scope: Annotated[str, Field(default="All entities", description="Defines the scope for the action.")]) -> dict:
        """Use the Get Mailbox Account Out Of Facility Settings action to retrieve the mailbox account out of facility (OOF) settings for the Google SecOps User entity provided. The Get Mailbox Account Out Of Facility Settings action uses the beta version of Microsoft Graph API. This action runs on the Google SecOps User entity.

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
                Endpoints.LIST_INTEGRATION_INSTANCES.format(INTEGRATION_NAME="MicrosoftGraphMailDelegated")
            )
            instances = instance_response.get("integration_instances", [])
        except Exception as e:
            print(f"Error fetching instance for MicrosoftGraphMailDelegated: {e}")
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
                actionName="MicrosoftGraphMailDelegated_Get Mailbox Account Out Of Facility Settings",
                properties={
                    "IntegrationInstance": instance_identifier,
                    "ScriptName": "MicrosoftGraphMailDelegated_Get Mailbox Account Out Of Facility Settings",
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
                print(f"Error executing action MicrosoftGraphMailDelegated_Get Mailbox Account Out Of Facility Settings for MicrosoftGraphMailDelegated: {e}")
                return {"Status": "Failed", "Message": f"Error executing action: {e}"}
        else:
            print(f"Warning: No active integration instance found for MicrosoftGraphMailDelegated")
            return {"Status": "Failed", "Message": "No active instance found."}

    @mcp.tool()
    async def microsoft_graph_mail_delegated_download_attachments_from_email(case_id: Annotated[str, Field(..., description="The ID of the case.")], alert_group_identifiers: Annotated[List[str], Field(..., description="Identifiers for the alert groups.")], search_in_mailbox: Annotated[str, Field(..., description="The default mailbox to execute the search operation in. If permissions allow it, the action can search in other mailboxes. This parameter accepts multiple values as a comma-separated string.")], download_destination: Annotated[List[str], Field(..., description="A location to save the downloaded attachments. By default, the action attempts to save the attachment to the Cloud Storage bucket. Saving an attachment to the local file system is a fallback option. The possible values are GCP Bucket and Local File System. The default value is GCP Bucket.")], download_path: Annotated[str, Field(..., description="A path to download attachments to. When saving attachments to the Cloud Storage bucket or a local file system, the action expects you to specify the download path in the Unix-like format, such as\"/tmp/test\"")], folder_name: Annotated[str, Field(default=None, description="A mailbox folder in which to search for an email. To specify a subfolder, use the \u201c/\u201d forward slash, such as {Inbox/Subfolder}.")], mail_i_ds: Annotated[str, Field(default=None, description="A filter condition to search for emails with specific email IDs or internetMessageId values. This parameter accepts a comma-separated list of email IDs to search for. If this parameter is provided, the search ignores the Subject Filter and Sender Filter parameters.")], subject_filter: Annotated[str, Field(default=None, description="A filter condition that specifies the email subject to search for. This filter uses the contains logic.")], sender_filter: Annotated[str, Field(default=None, description="A filter condition that specifies the sender of requested emails. This filter uses the equals logic.")], download_attachments_from_eml: Annotated[bool, Field(default=None, description="If selected, the action downloads attachments from EML files.")], download_attachments_to_unique_path: Annotated[bool, Field(default=None, description="If selected, the action downloads attachments to the unique path provided in the Download Path parameter to avoid overwriting any previously downloaded attachments.")], how_many_mailboxes_to_process_in_a_single_batch: Annotated[str, Field(default=None, description="The number of mailboxes to process in a single batch (a single connection to the Microsoft 365 server). The default value is 25.")], target_entities: Annotated[List[TargetEntity], PydanticListField(TargetEntity, description="Optional list of specific target entities (Identifier, EntityType) to run the action on.")], scope: Annotated[str, Field(default="All entities", description="Defines the scope for the action.")]) -> dict:
        """Use the Download Attachments From Email action to download attachments from emails based on the criteria provided. This action doesn't run on Google SecOps entities. This action is asynchronous. Adjust the script timeout value in the Google SecOps IDE. The action replaces the “/” forward slash and “\”  backslash characters in the names of the downloaded attachments with the “_” underscore character.

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
                Endpoints.LIST_INTEGRATION_INSTANCES.format(INTEGRATION_NAME="MicrosoftGraphMailDelegated")
            )
            instances = instance_response.get("integration_instances", [])
        except Exception as e:
            print(f"Error fetching instance for MicrosoftGraphMailDelegated: {e}")
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
                actionName="MicrosoftGraphMailDelegated_Download Attachments from Email",
                properties={
                    "IntegrationInstance": instance_identifier,
                    "ScriptName": "MicrosoftGraphMailDelegated_Download Attachments from Email",
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
                print(f"Error executing action MicrosoftGraphMailDelegated_Download Attachments from Email for MicrosoftGraphMailDelegated: {e}")
                return {"Status": "Failed", "Message": f"Error executing action: {e}"}
        else:
            print(f"Warning: No active integration instance found for MicrosoftGraphMailDelegated")
            return {"Status": "Failed", "Message": "No active instance found."}

    @mcp.tool()
    async def microsoft_graph_mail_delegated_delete_email(case_id: Annotated[str, Field(..., description="The ID of the case.")], alert_group_identifiers: Annotated[List[str], Field(..., description="Identifiers for the alert groups.")], delete_in_mailbox: Annotated[str, Field(..., description="The default mailbox to execute the delete operation in. If permissions allow it, the action executes search in other mailboxes. This parameter accepts multiple values as a comma-separated string.")], folder_name: Annotated[str, Field(..., description="A mailbox folder in which to search for an email. To specify a subfolder, use the \u201c/\u201d forward slash, such as {Inbox/Subfolder}.")], mail_i_ds: Annotated[str, Field(default=None, description="A filter condition to search for emails with specific email IDs. This parameter accepts a comma-separated list of email IDs to search for. If this parameter is provided, the search ignores the Subject Filter and Sender Filter parameters.")], subject_filter: Annotated[str, Field(default=None, description="A filter condition that specifies the email subject to search for. This filter uses the contains logic.")], sender_filter: Annotated[str, Field(default=None, description="A filter condition that specifies the sender of requested emails. This filter uses the equals logic.")], time_frame_minutes: Annotated[str, Field(default=None, description="A filter condition that specifies the period in minutes to search for emails.")], only_unread: Annotated[bool, Field(default=None, description="If selected, the action searches only for unread emails.")], how_many_mailboxes_to_process_in_a_single_batch: Annotated[str, Field(default=None, description="The number of mailboxes to process in a single batch (a single connection to the Microsoft 365 server). The default value is 25.")], limit_the_amount_of_information_returned_in_the_json_result: Annotated[bool, Field(default=None, description="If enabled, the amount of information returned by the action will be limited only to the key email fields.")], disable_the_action_json_result: Annotated[bool, Field(default=None, description="If enabled, action will not return JSON result.")], target_entities: Annotated[List[TargetEntity], PydanticListField(TargetEntity, description="Optional list of specific target entities (Identifier, EntityType) to run the action on.")], scope: Annotated[str, Field(default="All entities", description="Defines the scope for the action.")]) -> dict:
        """You can use the Delete Email action to delete one or more emails from a mailbox. This action deletes emails based on your search criteria. With the appropriate permissions, the Delete Email action can move emails into different mailboxes. This action is asynchronous. Adjust the action timeout in the Google SecOps IDE accordingly. This action doesn't run on Google SecOps entities.

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
                Endpoints.LIST_INTEGRATION_INSTANCES.format(INTEGRATION_NAME="MicrosoftGraphMailDelegated")
            )
            instances = instance_response.get("integration_instances", [])
        except Exception as e:
            print(f"Error fetching instance for MicrosoftGraphMailDelegated: {e}")
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
                actionName="MicrosoftGraphMailDelegated_Delete Email",
                properties={
                    "IntegrationInstance": instance_identifier,
                    "ScriptName": "MicrosoftGraphMailDelegated_Delete Email",
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
                print(f"Error executing action MicrosoftGraphMailDelegated_Delete Email for MicrosoftGraphMailDelegated: {e}")
                return {"Status": "Failed", "Message": f"Error executing action: {e}"}
        else:
            print(f"Warning: No active integration instance found for MicrosoftGraphMailDelegated")
            return {"Status": "Failed", "Message": "No active instance found."}

    @mcp.tool()
    async def microsoft_graph_mail_delegated_mark_email_as_junk(case_id: Annotated[str, Field(..., description="The ID of the case.")], alert_group_identifiers: Annotated[List[str], Field(..., description="Identifiers for the alert groups.")], search_in_mailbox: Annotated[str, Field(..., description="A mailbox to search for an email in. By default, the action attempts to search for the email in the default mailbox that you specified in the integration configuration. To execute a search in other mailboxes, configure appropriate permissions for the action. This parameter accepts multiple values as a comma-separated string.")], folder_name: Annotated[str, Field(..., description="A mailbox folder in which to search for an email. To specify a subfolder, use the \u201c/\u201d forward slash, such as {Inbox/Subfolder}.")], mail_i_ds: Annotated[str, Field(..., description="A comma-separated string of the mail IDs or internetMessageId values of the emails to mark as junk.")], target_entities: Annotated[List[TargetEntity], PydanticListField(TargetEntity, description="Optional list of specific target entities (Identifier, EntityType) to run the action on.")], scope: Annotated[str, Field(default="All entities", description="Defines the scope for the action.")]) -> dict:
        """Use the Mark Email as Junk action to mark emails as junk in a specified mailbox. This action adds the email sender to the list of blocked senders and moves the message to the Junk Email folder. The Mark Email as Junk action uses the beta version of Microsoft Graph API. This action doesn't run on Google SecOps entities.

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
                Endpoints.LIST_INTEGRATION_INSTANCES.format(INTEGRATION_NAME="MicrosoftGraphMailDelegated")
            )
            instances = instance_response.get("integration_instances", [])
        except Exception as e:
            print(f"Error fetching instance for MicrosoftGraphMailDelegated: {e}")
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
                actionName="MicrosoftGraphMailDelegated_Mark Email as Junk",
                properties={
                    "IntegrationInstance": instance_identifier,
                    "ScriptName": "MicrosoftGraphMailDelegated_Mark Email as Junk",
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
                print(f"Error executing action MicrosoftGraphMailDelegated_Mark Email as Junk for MicrosoftGraphMailDelegated: {e}")
                return {"Status": "Failed", "Message": f"Error executing action: {e}"}
        else:
            print(f"Warning: No active integration instance found for MicrosoftGraphMailDelegated")
            return {"Status": "Failed", "Message": "No active instance found."}

    @mcp.tool()
    async def microsoft_graph_mail_delegated_extract_data_from_attached_eml(case_id: Annotated[str, Field(..., description="The ID of the case.")], alert_group_identifiers: Annotated[List[str], Field(..., description="Identifiers for the alert groups.")], search_in_mailbox: Annotated[str, Field(..., description="The default mailbox to execute the search operation in. If permissions allow it, the action can search in other mailboxes. This parameter accepts multiple values as a comma-separated string.")], mail_i_ds: Annotated[str, Field(..., description="A filter condition to search for emails with specific email IDs or internetMessageId values. This parameter accepts a comma-separated list of email IDs to search for.")], folder_name: Annotated[str, Field(default=None, description="A mailbox folder in which to search for an email. To specify a subfolder, use the \u201c/\u201d forward slash, such as {Inbox/Subfolder}.")], regex_map_json: Annotated[Union[str, dict], Field(default=None, description="A JSON definition that contains regular expressions to apply to the attached email file and generate additional key values in the action JSON result. The example of this parameter value is as follows: {ips: \\b\\\\d{1,3}\\\\.\\\\d{1,3}\\\\.\\\\d{1,3}\\\\.\\\\d{1,3}\\b}")], target_entities: Annotated[List[TargetEntity], PydanticListField(TargetEntity, description="Optional list of specific target entities (Identifier, EntityType) to run the action on.")], scope: Annotated[str, Field(default="All entities", description="Defines the scope for the action.")]) -> dict:
        """Use the Extract Data From Attached EML action to retrieve data from the email EML attachments and return it in the action results. This action supports the .eml, .msg, and .ics file formats. This action doesn't run on Google SecOps entities.

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
                Endpoints.LIST_INTEGRATION_INSTANCES.format(INTEGRATION_NAME="MicrosoftGraphMailDelegated")
            )
            instances = instance_response.get("integration_instances", [])
        except Exception as e:
            print(f"Error fetching instance for MicrosoftGraphMailDelegated: {e}")
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
                actionName="MicrosoftGraphMailDelegated_Extract Data from Attached EML",
                properties={
                    "IntegrationInstance": instance_identifier,
                    "ScriptName": "MicrosoftGraphMailDelegated_Extract Data from Attached EML",
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
                print(f"Error executing action MicrosoftGraphMailDelegated_Extract Data from Attached EML for MicrosoftGraphMailDelegated: {e}")
                return {"Status": "Failed", "Message": f"Error executing action: {e}"}
        else:
            print(f"Warning: No active integration instance found for MicrosoftGraphMailDelegated")
            return {"Status": "Failed", "Message": "No active instance found."}

    @mcp.tool()
    async def microsoft_graph_mail_delegated_get_authorization(case_id: Annotated[str, Field(..., description="The ID of the case.")], alert_group_identifiers: Annotated[List[str], Field(..., description="Identifiers for the alert groups.")], target_entities: Annotated[List[TargetEntity], PydanticListField(TargetEntity, description="Optional list of specific target entities (Identifier, EntityType) to run the action on.")], scope: Annotated[str, Field(default="All entities", description="Defines the scope for the action.")]) -> dict:
        """Use the Get Authorization action to obtain a link with the access code for the integration configuration with delegated authentication. Copy the whole link and use it in the Generate Token action to get the refresh token. This action doesn't run on Google SecOps entities.

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
                Endpoints.LIST_INTEGRATION_INSTANCES.format(INTEGRATION_NAME="MicrosoftGraphMailDelegated")
            )
            instances = instance_response.get("integration_instances", [])
        except Exception as e:
            print(f"Error fetching instance for MicrosoftGraphMailDelegated: {e}")
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
                actionName="MicrosoftGraphMailDelegated_Get Authorization",
                properties={
                    "IntegrationInstance": instance_identifier,
                    "ScriptName": "MicrosoftGraphMailDelegated_Get Authorization",
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
                print(f"Error executing action MicrosoftGraphMailDelegated_Get Authorization for MicrosoftGraphMailDelegated: {e}")
                return {"Status": "Failed", "Message": f"Error executing action: {e}"}
        else:
            print(f"Warning: No active integration instance found for MicrosoftGraphMailDelegated")
            return {"Status": "Failed", "Message": "No active instance found."}

    @mcp.tool()
    async def microsoft_graph_mail_delegated_run_microsoft_search_query(case_id: Annotated[str, Field(..., description="The ID of the case.")], alert_group_identifiers: Annotated[List[str], Field(..., description="Identifiers for the alert groups.")], entity_types_to_search: Annotated[str, Field(default=None, description="A comma-separated list of expected resource types for the search response. The possible values are as follows: event, message, driveItem, externalItem, site, list, listItem, drive, chatMessage, person, acronym, bookmark.")], fields_to_return: Annotated[str, Field(default=None, description="The fields to return in the search response. If you don\u2019t configure this parameter, the action returns all available fields.")], search_query: Annotated[str, Field(default=None, description="The query to run the search. For more information about the search query examples, see Use the Microsoft Search API to search Outlook messages(https://learn.microsoft.com/en-us/graph/search-concept-messages).")], max_rows_to_return: Annotated[str, Field(default=None, description="The maximum number of rows for the action to return. If you don\u2019t configure this parameter, the action uses the default value. The default value is 25.")], advanced_query: Annotated[str, Field(default=None, description="The full search payload to use instead of constructing the search query with other action parameters. Format the search payload as a JSON string. If you configure this parameter, the action ignores all other parameters.")], target_entities: Annotated[List[TargetEntity], PydanticListField(TargetEntity, description="Optional list of specific target entities (Identifier, EntityType) to run the action on.")], scope: Annotated[str, Field(default="All entities", description="Defines the scope for the action.")]) -> dict:
        """Use the Run Microsoft Search Query action to perform a search using Microsoft Search engine. The search bases on the constructed basic or advanced query that you specify. For more information about Microsoft Search, see Overview of the Microsoft Search API in Microsoft Graph (https://learn.microsoft.com/en-us/graph/search-concept-overview). This action doesn’t run on Google SecOps entities.

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
                Endpoints.LIST_INTEGRATION_INSTANCES.format(INTEGRATION_NAME="MicrosoftGraphMailDelegated")
            )
            instances = instance_response.get("integration_instances", [])
        except Exception as e:
            print(f"Error fetching instance for MicrosoftGraphMailDelegated: {e}")
            return {"Status": "Failed", "Message": f"Error fetching instance: {e}"}
    
        if instances:
            instance_identifier = instances[0].get("identifier")
            if not instance_identifier:
                return {"Status": "Failed", "Message": "Instance found but identifier is missing."}
    
            script_params = {}
            if entity_types_to_search is not None:
                script_params["Entity Types To Search"] = entity_types_to_search
            if fields_to_return is not None:
                script_params["Fields To Return"] = fields_to_return
            if search_query is not None:
                script_params["Search Query"] = search_query
            if max_rows_to_return is not None:
                script_params["Max Rows To Return"] = max_rows_to_return
            if advanced_query is not None:
                script_params["Advanced Query"] = advanced_query
    
            # Prepare data model for the API request
            action_data = ApiManualActionDataModel(
                alertGroupIdentifiers=alert_group_identifiers,
                caseId=case_id,
                targetEntities=final_target_entities,
                scope=final_scope,
                isPredefinedScope=is_predefined_scope,
                actionProvider="Scripts",
                actionName="MicrosoftGraphMailDelegated_Run Microsoft Search Query",
                properties={
                    "IntegrationInstance": instance_identifier,
                    "ScriptName": "MicrosoftGraphMailDelegated_Run Microsoft Search Query",
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
                print(f"Error executing action MicrosoftGraphMailDelegated_Run Microsoft Search Query for MicrosoftGraphMailDelegated: {e}")
                return {"Status": "Failed", "Message": f"Error executing action: {e}"}
        else:
            print(f"Warning: No active integration instance found for MicrosoftGraphMailDelegated")
            return {"Status": "Failed", "Message": "No active instance found."}
