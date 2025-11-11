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
    # This function registers all tools (actions) for the Exchange integration.

    @mcp.tool()
    async def exchange_unblock_sender_by_message_id(case_id: Annotated[str, Field(..., description="The ID of the case.")], alert_group_identifiers: Annotated[List[str], Field(..., description="Identifiers for the alert groups.")], move_items_back_to_inbox: Annotated[bool, Field(..., description="Should the action move the specified messages back to the inbox folder")], message_i_ds: Annotated[str, Field(default=None, description="Filter condition, specify emails with which email ids to find. Should accept comma separated list of message ids to unmark as junk. If message id is provided, subject, sender and recipient filters are ignored.")], mailboxes_list_to_perform_on: Annotated[str, Field(default=None, description="Filter condition, If you have a specific list of mailboxes you would like to conduct the operation on, for better timing, please provide them here. Should accept a comma separated list of mail addresses to unmark the messages as junk in. If a mailboxes list is provided, \"Perform Action in all Mailboxes\" parameter will be ignored.")], folder_name: Annotated[str, Field(default=None, description="Parameter can be used to specify email folder on the mailbox to search for the emails. Parameter should also accept comma separated list of folders to check the user response in multiple folders. Parameter is case sensitive. '/' separator can be used to specify a subfolder to search in, example: Inbox/Subfolder")], subject_filter: Annotated[str, Field(default=None, description="Filter condition, specify subject to search for emails")], sender_filter: Annotated[str, Field(default=None, description="Filter condition, specify who should be the sender of needed emails")], recipient_filter: Annotated[str, Field(default=None, description="Filter condition, specify who should be the recipient of needed emails")], unmark_all_matching_emails: Annotated[bool, Field(default=None, description="Filter condition, specify if action should Unmark all matched by criteria emails from the mailbox or Unmark only first match.")], perform_action_in_all_mailboxes: Annotated[bool, Field(default=None, description="If checked, move to junk and block sender emails in all mailboxes accessible with current impersonalization settings. If delegated access is used, implicitly specify the mailboxes to search in the \"Mailboxes\" parameter.")], how_many_mailboxes_to_process_in_a_single_batch: Annotated[str, Field(default=None, description="In case \"Perform action  in all mailboxes\" is checked, action works in batches, this parameter controls how many mailboxes action should process in single batch (single connection to mail server).")], time_frame_minutes: Annotated[str, Field(default=None, description="Filter condition, specify in what time frame in minutes should action look for emails.")], target_entities: Annotated[List[TargetEntity], PydanticListField(TargetEntity, description="Optional list of specific target entities (Identifier, EntityType) to run the action on.")], scope: Annotated[str, Field(default="All entities", description="Defines the scope for the action.")]) -> dict:
        """Action will get as a parameter a list of message IDs, and will be able to unmark it as junk. Unmarking an item as junk using this action will remove the item sender's mail address from the "Blocked Senders List". To move it back to the inbox, please tick the appropriate checkbox in the action parameters. NOTICE - to unmark emails in all mailboxes, please configure impersonation permissions: https://docs.microsoft.com/en-us/exchange/client-developer/exchange-web-services/impersonation-and-ews-in-exchange. NOTE: Action is running as async, please adjust script timeout value in Siemplify IDE for action as needed. NOTE: Action is supported only from Exchange Server version 2013 and newer, if a lower version is used, action will fail with the appropriate message.

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
                Endpoints.LIST_INTEGRATION_INSTANCES.format(INTEGRATION_NAME="Exchange")
            )
            instances = instance_response.get("integration_instances", [])
        except Exception as e:
            print(f"Error fetching instance for Exchange: {e}")
            return {"Status": "Failed", "Message": f"Error fetching instance: {e}"}
    
        if instances:
            instance_identifier = instances[0].get("identifier")
            if not instance_identifier:
                return {"Status": "Failed", "Message": "Instance found but identifier is missing."}
    
            script_params = {}
            script_params["Move items back to Inbox?"] = move_items_back_to_inbox
            if message_i_ds is not None:
                script_params["Message IDs"] = message_i_ds
            if mailboxes_list_to_perform_on is not None:
                script_params["Mailboxes list to perform on"] = mailboxes_list_to_perform_on
            if folder_name is not None:
                script_params["Folder Name"] = folder_name
            if subject_filter is not None:
                script_params["Subject Filter"] = subject_filter
            if sender_filter is not None:
                script_params["Sender Filter"] = sender_filter
            if recipient_filter is not None:
                script_params["Recipient Filter"] = recipient_filter
            if unmark_all_matching_emails is not None:
                script_params["Unmark All Matching Emails"] = unmark_all_matching_emails
            if perform_action_in_all_mailboxes is not None:
                script_params["Perform action in all mailboxes"] = perform_action_in_all_mailboxes
            if how_many_mailboxes_to_process_in_a_single_batch is not None:
                script_params["How many mailboxes to process in a single batch"] = how_many_mailboxes_to_process_in_a_single_batch
            if time_frame_minutes is not None:
                script_params["Time Frame (minutes)"] = time_frame_minutes
    
            # Prepare data model for the API request
            action_data = ApiManualActionDataModel(
                alertGroupIdentifiers=alert_group_identifiers,
                caseId=case_id,
                targetEntities=final_target_entities,
                scope=final_scope,
                isPredefinedScope=is_predefined_scope,
                actionProvider="Scripts",
                actionName="Exchange_Unblock Sender by Message ID",
                properties={
                    "IntegrationInstance": instance_identifier,
                    "ScriptName": "Exchange_Unblock Sender by Message ID",
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
                print(f"Error executing action Exchange_Unblock Sender by Message ID for Exchange: {e}")
                return {"Status": "Failed", "Message": f"Error executing action: {e}"}
        else:
            print(f"Warning: No active integration instance found for Exchange")
            return {"Status": "Failed", "Message": "No active instance found."}

    @mcp.tool()
    async def exchange_send_mail(case_id: Annotated[str, Field(..., description="The ID of the case.")], alert_group_identifiers: Annotated[List[str], Field(..., description="Identifiers for the alert groups.")], subject: Annotated[str, Field(..., description="The mail subject part")], send_to: Annotated[str, Field(..., description="Arbitrary comma separated list of email addresses for the email recipients. For example: user1@company.co, user2@company.co")], mail_content: Annotated[EmailContent, Field(..., description="The email body part")], cc: Annotated[str, Field(default=None, description="Arbitrary comma separated list of email addresses to be put in the CC field of email. Format is the same as for the \"Send to\" field")], bcc: Annotated[str, Field(default=None, description="Arbitrary comma separated list of email addresses to be put in the BCC field of email. Format is the same as for the \"Send to\" field")], attachments_paths: Annotated[str, Field(default=None, description="Comma separated list of attachments file paths stored on the server for addition to the email. For example: C:\\<Siemplify work dir>\\file1.pdf, C:\\<Siemplify work dir>\\image2.jpg")], reply_to_recipients: Annotated[str, Field(default=None, description="Specify a comma-separated list of recipients that will be used in the \"Reply-To\" header. Note: The Reply-To header is added when the originator of the message wants any replies to the message to go to that particular email address rather than the one in the \"From:\" address.")], base64_encoded_certificate: Annotated[str, Field(default=None, description="Specify a base64 encoded certificate that will be used to either encrypt or sign the email. Note: for signing you need to also provide \"Base64 Encoded Signature\". For encryption, only this parameter needs to have a value.")], base64_encoded_signature: Annotated[str, Field(default=None, description="Specify a base64 encoded signature that will be used to sign the email. Note: \"Base64 Encoded Certificate\" needs to be provided as well for signature to work and contain the signing certificate.")], target_entities: Annotated[List[TargetEntity], PydanticListField(TargetEntity, description="Optional list of specific target entities (Identifier, EntityType) to run the action on.")], scope: Annotated[str, Field(default="All entities", description="Defines the scope for the action.")]) -> dict:
        """Send Email from specific mailbox to an arbitrary list of recipients. Action can be used to inform users about specific alerts created in the Siemplify or inform about the results of processing of specific alerts.

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
                Endpoints.LIST_INTEGRATION_INSTANCES.format(INTEGRATION_NAME="Exchange")
            )
            instances = instance_response.get("integration_instances", [])
        except Exception as e:
            print(f"Error fetching instance for Exchange: {e}")
            return {"Status": "Failed", "Message": f"Error fetching instance: {e}"}
    
        if instances:
            instance_identifier = instances[0].get("identifier")
            if not instance_identifier:
                return {"Status": "Failed", "Message": "Instance found but identifier is missing."}
    
            script_params = {}
            script_params["Subject"] = subject
            script_params["Send to"] = send_to
            if cc is not None:
                script_params["CC"] = cc
            if bcc is not None:
                script_params["BCC"] = bcc
            if attachments_paths is not None:
                script_params["Attachments Paths"] = attachments_paths
            mail_content = mail_content.model_dump()
            script_params["Mail content"] = mail_content
            if reply_to_recipients is not None:
                script_params["Reply-To Recipients"] = reply_to_recipients
            if base64_encoded_certificate is not None:
                script_params["Base64 Encoded Certificate"] = base64_encoded_certificate
            if base64_encoded_signature is not None:
                script_params["Base64 Encoded Signature"] = base64_encoded_signature
    
            # Prepare data model for the API request
            action_data = ApiManualActionDataModel(
                alertGroupIdentifiers=alert_group_identifiers,
                caseId=case_id,
                targetEntities=final_target_entities,
                scope=final_scope,
                isPredefinedScope=is_predefined_scope,
                actionProvider="Scripts",
                actionName="Exchange_Send Mail",
                properties={
                    "IntegrationInstance": instance_identifier,
                    "ScriptName": "Exchange_Send Mail",
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
                print(f"Error executing action Exchange_Send Mail for Exchange: {e}")
                return {"Status": "Failed", "Message": f"Error executing action: {e}"}
        else:
            print(f"Warning: No active integration instance found for Exchange")
            return {"Status": "Failed", "Message": "No active instance found."}

    @mcp.tool()
    async def exchange_add_domains_to_exchange_siemplify_inbox_rules(case_id: Annotated[str, Field(..., description="The ID of the case.")], alert_group_identifiers: Annotated[List[str], Field(..., description="Identifiers for the alert groups.")], rule_to_add_domains_to: Annotated[List[str], Field(..., description="Specify the rule to add the Domains to. If the rule doesn't exist - action will create it where it's missing.")], domains: Annotated[str, Field(default=None, description="Specify the Domains you would like to add to the rule, in a comma separated list.")], perform_action_in_all_mailboxes: Annotated[bool, Field(default=None, description="If checked, action will be performed in all mailboxes accessible with current impersonalization settings. If delegated access is used, implicitly specify the mailboxes to search in the \"Mailboxes\" parameter.")], how_many_mailboxes_to_process_in_a_single_batch: Annotated[str, Field(default=None, description="In case \"Perform action in all mailboxes\" is checked, action works in batches, this parameter controls how many mailboxes action should process in single batch (single connection to mail server).")], target_entities: Annotated[List[TargetEntity], PydanticListField(TargetEntity, description="Optional list of specific target entities (Identifier, EntityType) to run the action on.")], scope: Annotated[str, Field(default="All entities", description="Defines the scope for the action.")]) -> dict:
        """Action will get as a parameter a list of Domains, and will be able to create or update a rule, filtering the domains from your mailboxes. Actions can be modified in the parameters using rule parameter. WARNING: Action will modify your current users inbox rules, using EWS. NOTICE - to perform operation, please configure EDiscovery Group and Author permissions. For full details, please visit: https://cloud.google.com/chronicle/docs/soar/marketplace-integrations/exchang. NOTE: Action is running as async, please adjust script timeout value in Siemplify IDE for action as needed.

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
                Endpoints.LIST_INTEGRATION_INSTANCES.format(INTEGRATION_NAME="Exchange")
            )
            instances = instance_response.get("integration_instances", [])
        except Exception as e:
            print(f"Error fetching instance for Exchange: {e}")
            return {"Status": "Failed", "Message": f"Error fetching instance: {e}"}
    
        if instances:
            instance_identifier = instances[0].get("identifier")
            if not instance_identifier:
                return {"Status": "Failed", "Message": "Instance found but identifier is missing."}
    
            script_params = {}
            if domains is not None:
                script_params["Domains"] = domains
            script_params["Rule to add Domains to"] = rule_to_add_domains_to
            if perform_action_in_all_mailboxes is not None:
                script_params["Perform action in all mailboxes"] = perform_action_in_all_mailboxes
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
                actionName="Exchange_Add Domains to Exchange-Siemplify Inbox Rules",
                properties={
                    "IntegrationInstance": instance_identifier,
                    "ScriptName": "Exchange_Add Domains to Exchange-Siemplify Inbox Rules",
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
                print(f"Error executing action Exchange_Add Domains to Exchange-Siemplify Inbox Rules for Exchange: {e}")
                return {"Status": "Failed", "Message": f"Error executing action: {e}"}
        else:
            print(f"Warning: No active integration instance found for Exchange")
            return {"Status": "Failed", "Message": "No active instance found."}

    @mcp.tool()
    async def exchange_send_thread_reply(case_id: Annotated[str, Field(..., description="The ID of the case.")], alert_group_identifiers: Annotated[List[str], Field(..., description="Identifiers for the alert groups.")], message_id: Annotated[str, Field(..., description="Specify the ID of the message to which you want to send a reply.")], folder_name: Annotated[str, Field(..., description="Parameter can be used to specify email folder on the mailbox to search for the emails. Parameter should also accept comma separated list of folders to check the user response in multiple folders. Parameter is case sensitive. '/' separator can be used to specify a subfolder to search in, example: Inbox/Subfolder")], content: Annotated[EmailContent, Field(..., description="Specify the content of the reply.")], reply_all: Annotated[bool, Field(..., description="If enabled, action will send a reply to all recipients related to the original email. Note: this parameter has priority over \u201cReply To\u201c parameter.")], attachments_paths: Annotated[str, Field(default=None, description="Specify a comma separated list of attachments file paths stored on the server for addition to the email.")], reply_to: Annotated[str, Field(default=None, description="Specify a comma-separated list of emails to which you want to send this reply. If nothing is provided and \u201cReply All\u201c is disabled, action will only send a reply to the sender of the email. If \u201cReply All\u201c is enabled, action will ignore this parameter.")], target_entities: Annotated[List[TargetEntity], PydanticListField(TargetEntity, description="Optional list of specific target entities (Identifier, EntityType) to run the action on.")], scope: Annotated[str, Field(default="All entities", description="Defines the scope for the action.")]) -> dict:
        """
Send a message as a reply to the email thread.

Action Parameters: Message ID: Required The ID of the message to send a reply to., Folder Name: Required A comma-separated list of mailbox folders in which to run a search for an email.You can set mail-specific folders, for example, Gmail/All Mail to run a search in all of the Gmail mailbox folders. Additionally, the folder name must match the IMAP folder. If the folder name contains spaces, wrap spaces in double quotes. The Exchange integration uses backslashes as separators to specify subfolders, such as folder/subfolder1/subfolder2. To avoid the timeout error or action failure, replace backslashes in folder or subfolder names with other characters like underscore., Content: Required A content of the reply., Attachment Paths: Optional A comma-separated list of paths to file attachments stored on the server., Reply All: Optional If selected, the action sends a reply to all recipients related to the original email and the ignores the Reply To parameter.Selected by default., Reply To: Required A comma-separated list of emails to send the reply to. If you don't set a value and don't select the Reply All parameter, the action only sends a reply to the sender of the email. If you select the Reply All parameter, the action ignores this parameter.

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
                Endpoints.LIST_INTEGRATION_INSTANCES.format(INTEGRATION_NAME="Exchange")
            )
            instances = instance_response.get("integration_instances", [])
        except Exception as e:
            print(f"Error fetching instance for Exchange: {e}")
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
            if attachments_paths is not None:
                script_params["Attachments Paths"] = attachments_paths
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
                actionName="Exchange_Send Thread Reply",
                properties={
                    "IntegrationInstance": instance_identifier,
                    "ScriptName": "Exchange_Send Thread Reply",
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
                print(f"Error executing action Exchange_Send Thread Reply for Exchange: {e}")
                return {"Status": "Failed", "Message": f"Error executing action: {e}"}
        else:
            print(f"Warning: No active integration instance found for Exchange")
            return {"Status": "Failed", "Message": "No active instance found."}

    @mcp.tool()
    async def exchange_search_mails(case_id: Annotated[str, Field(..., description="The ID of the case.")], alert_group_identifiers: Annotated[List[str], Field(..., description="Identifiers for the alert groups.")], folder_name: Annotated[str, Field(default=None, description="Parameter can be used to specify email folder on the mailbox to search for the emails. Parameter should also accept comma separated list of folders to check the user response in multiple folders. Parameter is case sensitive. '/' separator can be used to specify a subfolder to search in, example: Inbox/Subfolder")], message_i_ds: Annotated[str, Field(default=None, description="Specify a comma-separated list of message ids that need to be searched. Note: this filter has priority over the other ones.")], subject_filter: Annotated[str, Field(default=None, description="Filter condition, specify what subject to search for emails")], sender_filter: Annotated[str, Field(default=None, description="Filter condition, specify who should be the sender of needed emails")], recipient_filter: Annotated[str, Field(default=None, description="Filter condition, specify who should be the recipient of needed emails")], time_frame_minutes: Annotated[str, Field(default=None, description="Filter condition, specify in what time frame in minutes should action look for emails")], only_unread: Annotated[bool, Field(default=None, description="Filter condition, specify if search should look only for unread emails")], max_emails_to_return: Annotated[str, Field(default=None, description="Return max X emails as an action result")], search_in_all_mailboxes: Annotated[bool, Field(default=None, description="If checked, search in all mailboxes accessible with current impersonalization settings. If delegated access is used, implicitly specify the mailboxes to search in the \"Mailboxes\" parameter.")], how_many_mailboxes_to_process_in_a_single_batch: Annotated[str, Field(default=None, description="In case \"Search in all mailboxes\" is checked, action works in batches, this parameter controls how many mailboxes action should process in single batch (single connection to mail server).")], mailboxes: Annotated[str, Field(default=None, description="Specify a comma-separated list of mailboxes that need to be searched. This parameter has priority over \"Search in all mailboxes\".")], start_time: Annotated[str, Field(default=None, description="Specify the start time for the email search. Format: ISO 8601. This parameter has a priority over \"Time Frame (minutes)\".")], end_time: Annotated[str, Field(default=None, description="Specify the end time for the email search. Format: ISO 8601. If nothing is provided and \"Start Time\" is valid then this parameter will use current time.")], body_regex_filter: Annotated[str, Field(default=None, description="Specify a regex pattern that needs to be searched in body part of the email.")], target_entities: Annotated[List[TargetEntity], PydanticListField(TargetEntity, description="Optional list of specific target entities (Identifier, EntityType) to run the action on.")], scope: Annotated[str, Field(default="All entities", description="Defines the scope for the action.")]) -> dict:
        """
Search for specific emails in configured mailbox using multiple provided search criteria. Action return information on found in mailbox emails in JSON format. NOTICE - to search for an email in all mailboxes, please configure impersonation permissions. https://docs.microsoft.com/en-us/exchange/client-developer/exchange-web-services/impersonation-and-ews-in-exchange. Note: Action is running as async, please adjust script timeout value in Siemplify IDE for action as needed.

Action Parameters: Folder Name: Optional A mailbox folder to search an email in.This parameter accepts a comma-separated list of folders.The Exchange integration uses backslashes as separators to specify subfolders, such as folder/subfolder1/subfolder2. To avoid the timeout error or action failure, replace backslashes in folder or subfolder names with other characters like underscore., Subject Filter: Optional A filter condition which specifies the email subject to search for., Sender Filter: Optional A filter condition to specify the sender of requested emails., Recipient Filter: Optional A filter condition to specify the recipient of requested emails., Time Frame (minutes): Optional A period in minutes to search for emails., Only Unread: Optional If selected, the action searches only for unread emails. Not selected by default., Max Emails To Return: OptionalThe maximum number of emails to return in the action result., Search in all mailboxes: OptionalIf selected, the action runs a search in all mailboxes that are accessible using current impersonation settings. Not selected by default., How many mailboxes to process in a single batch: Required The number of mailboxes to process in a single batch (single connection to the mail server).If you select the Search in all mailboxes parameter, the action works in batches. The default value is 25., Start Time: OptionalThe start time for running the email search. The format to use is ISO 8601. This parameter has a priority over the Time Frame (minutes) parameter., End Time: OptionalThe end time for running the email search. The format to use is ISO 8601. If you don't set a value and the Start Time parameter is valid, the action sets the End Time value to the current time., Mailboxes: Optional A comma-separated list of mailboxes to run a search through.This parameter has priority over the Search in all mailboxes parameter., Message IDs: Optional A comma-separated list of message IDs to search for. This filter has priority over other filter conditions., Body Regex Filter: OptionalA regular expression pattern to search for in the email body.

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
                Endpoints.LIST_INTEGRATION_INSTANCES.format(INTEGRATION_NAME="Exchange")
            )
            instances = instance_response.get("integration_instances", [])
        except Exception as e:
            print(f"Error fetching instance for Exchange: {e}")
            return {"Status": "Failed", "Message": f"Error fetching instance: {e}"}
    
        if instances:
            instance_identifier = instances[0].get("identifier")
            if not instance_identifier:
                return {"Status": "Failed", "Message": "Instance found but identifier is missing."}
    
            script_params = {}
            if folder_name is not None:
                script_params["Folder Name"] = folder_name
            if message_i_ds is not None:
                script_params["Message IDs"] = message_i_ds
            if subject_filter is not None:
                script_params["Subject Filter"] = subject_filter
            if sender_filter is not None:
                script_params["Sender Filter"] = sender_filter
            if recipient_filter is not None:
                script_params["Recipient Filter"] = recipient_filter
            if time_frame_minutes is not None:
                script_params["Time Frame (minutes)"] = time_frame_minutes
            if only_unread is not None:
                script_params["Only Unread"] = only_unread
            if max_emails_to_return is not None:
                script_params["Max Emails To Return"] = max_emails_to_return
            if search_in_all_mailboxes is not None:
                script_params["Search in all mailboxes"] = search_in_all_mailboxes
            if how_many_mailboxes_to_process_in_a_single_batch is not None:
                script_params["How many mailboxes to process in a single batch"] = how_many_mailboxes_to_process_in_a_single_batch
            if mailboxes is not None:
                script_params["Mailboxes"] = mailboxes
            if start_time is not None:
                script_params["Start Time"] = start_time
            if end_time is not None:
                script_params["End Time"] = end_time
            if body_regex_filter is not None:
                script_params["Body Regex Filter"] = body_regex_filter
    
            # Prepare data model for the API request
            action_data = ApiManualActionDataModel(
                alertGroupIdentifiers=alert_group_identifiers,
                caseId=case_id,
                targetEntities=final_target_entities,
                scope=final_scope,
                isPredefinedScope=is_predefined_scope,
                actionProvider="Scripts",
                actionName="Exchange_Search Mails",
                properties={
                    "IntegrationInstance": instance_identifier,
                    "ScriptName": "Exchange_Search Mails",
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
                print(f"Error executing action Exchange_Search Mails for Exchange: {e}")
                return {"Status": "Failed", "Message": f"Error executing action: {e}"}
        else:
            print(f"Warning: No active integration instance found for Exchange")
            return {"Status": "Failed", "Message": "No active instance found."}

    @mcp.tool()
    async def exchange_wait_for_vote_mail_results(case_id: Annotated[str, Field(..., description="The ID of the case.")], alert_group_identifiers: Annotated[List[str], Field(..., description="Identifiers for the alert groups.")], vote_mail_message_id: Annotated[str, Field(..., description="Message_id of the vote email, which current action would be waiting for. If message has been sent using Send Vote Mail action, please select SendVoteMail.JSONResult|message_id field as a placeholder.")], mail_recipients: Annotated[str, Field(..., description="Comma-separated list of recipient emails, response from which current action would be waiting for. Please select SendVoteMail.JSONResult|to_recipients field as a placeholder.")], folder_to_check_for_reply: Annotated[str, Field(..., description="Parameter can be used to specify mailbox email folder (mailbox that was used to send the email with question) to search for the user reply in this folder. Parameter should also accept comma separated list of folders to check the user response in multiple folders. Parameter is case sensitive. '/' separator can be used to specify a subfolder to search in, example: Inbox/Subfolder")], folder_to_check_for_sent_mail: Annotated[str, Field(..., description="Parameter can be used to specify mailbox email folder (mailbox that was used to send the email with question) to search for the sent mail in this folder. Parameter should also accept comma separated list of folders to check the user response in multiple folders. Parameter is case sensitive.")], how_long_to_wait_for_recipient_reply_minutes: Annotated[str, Field(..., description="How long in minutes to wait for the user's reply before marking it timed out.")], wait_for_all_recipients_to_reply: Annotated[bool, Field(default=None, description="Parameter can be used to define if there are multiple recipients - should the Action wait for responses from all of recipients until timeout, or Action should wait for first reply to proceed.")], target_entities: Annotated[List[TargetEntity], PydanticListField(TargetEntity, description="Optional list of specific target entities (Identifier, EntityType) to run the action on.")], scope: Annotated[str, Field(default="All entities", description="Defines the scope for the action.")]) -> dict:
        """
Use this action to fetch the responses of a vote mail sent by the "Send Vote Mail" action, in order to wait for the responses and get them inside Siemplify.

Action Parameters: Vote Mail message_id: Required The message ID of the vote email.If the message is sent using the Send Vote Mail action, select the SendVoteMail.JSONResult|message_id field as a placeholder., Mail Recipients: Required A comma-separated list of recipient emails the current action awaits the response from.Select the SendVoteMail.JSONResult|to_recipients field as a placeholder., Folder to Check for Reply: Required A mailbox folder to search for the user reply in. The action runs a search in the mailbox which the email containing a question was sent from.This parameter also accepts a comma-separated list of folders. The Exchange integration uses backslashes as separators to specify subfolders, such as folder/subfolder1/subfolder2. To avoid the timeout error or action failure, replace backslashes in folder or subfolder names with other characters like underscore. This parameter is case-sensitive. The default value is Inbox., Folder to Check for Sent Mail: Required A mailbox folder to search for the sent mail in. The action runs a search in the mailbox which the email containing a question was sent from. This parameter also accepts a comma-separated list of folders. The Exchange integration uses backslashes as separators to specify subfolders, such as folder/subfolder1/subfolder2. To avoid the timeout error or action failure, replace backslashes in folder or subfolder names with other characters like underscore.This parameter is case-sensitive. The default value is Sent Items., How long to wait for recipient reply (minutes): Required A period for the action to wait for the user reply before marking it as timed out.The default value is 1440 minutes., Wait for All Recipients to Reply?: Optional If selected, the action waits for responses from all recipients until reaching a timeout or proceeding with the first reply. Selected by default.

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
                Endpoints.LIST_INTEGRATION_INSTANCES.format(INTEGRATION_NAME="Exchange")
            )
            instances = instance_response.get("integration_instances", [])
        except Exception as e:
            print(f"Error fetching instance for Exchange: {e}")
            return {"Status": "Failed", "Message": f"Error fetching instance: {e}"}
    
        if instances:
            instance_identifier = instances[0].get("identifier")
            if not instance_identifier:
                return {"Status": "Failed", "Message": "Instance found but identifier is missing."}
    
            script_params = {}
            script_params["Vote Mail message_id"] = vote_mail_message_id
            script_params["Mail Recipients"] = mail_recipients
            script_params["Folder to Check for Reply"] = folder_to_check_for_reply
            script_params["Folder to check for Sent Mail"] = folder_to_check_for_sent_mail
            script_params["How long to wait for recipient reply (minutes)"] = how_long_to_wait_for_recipient_reply_minutes
            if wait_for_all_recipients_to_reply is not None:
                script_params["Wait for All Recipients to Reply?"] = wait_for_all_recipients_to_reply
    
            # Prepare data model for the API request
            action_data = ApiManualActionDataModel(
                alertGroupIdentifiers=alert_group_identifiers,
                caseId=case_id,
                targetEntities=final_target_entities,
                scope=final_scope,
                isPredefinedScope=is_predefined_scope,
                actionProvider="Scripts",
                actionName="Exchange_Wait for Vote Mail Results",
                properties={
                    "IntegrationInstance": instance_identifier,
                    "ScriptName": "Exchange_Wait for Vote Mail Results",
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
                print(f"Error executing action Exchange_Wait for Vote Mail Results for Exchange: {e}")
                return {"Status": "Failed", "Message": f"Error executing action: {e}"}
        else:
            print(f"Warning: No active integration instance found for Exchange")
            return {"Status": "Failed", "Message": "No active instance found."}

    @mcp.tool()
    async def exchange_generate_token(case_id: Annotated[str, Field(..., description="The ID of the case.")], alert_group_identifiers: Annotated[List[str], Field(..., description="Identifiers for the alert groups.")], authorization_url: Annotated[str, Field(..., description="Use the authorization URL received in the Get Authorization URL action to request a refresh token.")], target_entities: Annotated[List[TargetEntity], PydanticListField(TargetEntity, description="Optional list of specific target entities (Identifier, EntityType) to run the action on.")], scope: Annotated[str, Field(default="All entities", description="Defines the scope for the action.")]) -> dict:
        """For integration configuration with Oauth authentication, get a refresh token using the authorization URL received in the Get Authorization action.

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
                Endpoints.LIST_INTEGRATION_INSTANCES.format(INTEGRATION_NAME="Exchange")
            )
            instances = instance_response.get("integration_instances", [])
        except Exception as e:
            print(f"Error fetching instance for Exchange: {e}")
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
                actionName="Exchange_Generate Token",
                properties={
                    "IntegrationInstance": instance_identifier,
                    "ScriptName": "Exchange_Generate Token",
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
                print(f"Error executing action Exchange_Generate Token for Exchange: {e}")
                return {"Status": "Failed", "Message": f"Error executing action: {e}"}
        else:
            print(f"Warning: No active integration instance found for Exchange")
            return {"Status": "Failed", "Message": "No active instance found."}

    @mcp.tool()
    async def exchange_send_vote_mail(case_id: Annotated[str, Field(..., description="The ID of the case.")], alert_group_identifiers: Annotated[List[str], Field(..., description="Identifiers for the alert groups.")], subject: Annotated[str, Field(..., description="The mail subject part")], send_to: Annotated[str, Field(..., description="Arbitrary comma separated list of email addresses for the email recipients. For example: user1@company.co, user2@company.co")], question_or_decision_description: Annotated[EmailContent, Field(..., description="The question you would like to ask, or describe the decision you would like the recipient to be able to respond to")], structure_of_voting_options: Annotated[List[str], Field(..., description="Choose the structure of the vote to be sent to the recipients")], cc: Annotated[str, Field(default=None, description="Arbitrary comma separated list of email addresses to be put in the CC field of email. Format is the same as for the \"Send to\" field")], bcc: Annotated[str, Field(default=None, description="Arbitrary comma separated list of email addresses to be put in the BCC field of email. Format is the same as for the \"Send to\" field")], attachments_paths: Annotated[str, Field(default=None, description="Comma separated list of attachments file paths stored on the server for addition to the email. For example: C:\\<Siemplify work dir>\\file1.pdf, C:\\<Siemplify work dir>\\image2.jpg")], target_entities: Annotated[List[TargetEntity], PydanticListField(TargetEntity, description="Optional list of specific target entities (Identifier, EntityType) to run the action on.")], scope: Annotated[str, Field(default="All entities", description="Defines the scope for the action.")]) -> dict:
        """Send emails with easy answering options, to allow stakeholders to be combined in the automated processes without accessing the Siemplify UI.

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
                Endpoints.LIST_INTEGRATION_INSTANCES.format(INTEGRATION_NAME="Exchange")
            )
            instances = instance_response.get("integration_instances", [])
        except Exception as e:
            print(f"Error fetching instance for Exchange: {e}")
            return {"Status": "Failed", "Message": f"Error fetching instance: {e}"}
    
        if instances:
            instance_identifier = instances[0].get("identifier")
            if not instance_identifier:
                return {"Status": "Failed", "Message": "Instance found but identifier is missing."}
    
            script_params = {}
            script_params["Subject"] = subject
            script_params["Send To"] = send_to
            if cc is not None:
                script_params["CC"] = cc
            if bcc is not None:
                script_params["BCC"] = bcc
            if attachments_paths is not None:
                script_params["Attachments Paths"] = attachments_paths
            question_or_decision_description = question_or_decision_description.model_dump()
            script_params["Question or Decision Description"] = question_or_decision_description
            script_params["Structure of voting options"] = structure_of_voting_options
    
            # Prepare data model for the API request
            action_data = ApiManualActionDataModel(
                alertGroupIdentifiers=alert_group_identifiers,
                caseId=case_id,
                targetEntities=final_target_entities,
                scope=final_scope,
                isPredefinedScope=is_predefined_scope,
                actionProvider="Scripts",
                actionName="Exchange_Send Vote Mail",
                properties={
                    "IntegrationInstance": instance_identifier,
                    "ScriptName": "Exchange_Send Vote Mail",
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
                print(f"Error executing action Exchange_Send Vote Mail for Exchange: {e}")
                return {"Status": "Failed", "Message": f"Error executing action: {e}"}
        else:
            print(f"Warning: No active integration instance found for Exchange")
            return {"Status": "Failed", "Message": "No active instance found."}

    @mcp.tool()
    async def exchange_list_exchange_siemplify_inbox_rules(case_id: Annotated[str, Field(..., description="The ID of the case.")], alert_group_identifiers: Annotated[List[str], Field(..., description="Identifiers for the alert groups.")], rule_name_to_list: Annotated[List[str], Field(..., description="Specify the Rule name you would like to list from the relevant mailboxes")], mailboxes_list_to_perform_on: Annotated[str, Field(default=None, description="Filter condition, If you have a specific list of mailboxes you would like to conduct the operation on, for better timing, please provide them here. Should accept a comma separated list of mail addresses to list the rules from. If a mailboxes list is provided, \"Perform Action in all Mailboxes\" parameter will be ignored.")], perform_action_in_all_mailboxes: Annotated[bool, Field(default=None, description="If checked, action will be performed in all mailboxes accessible with current impersonalization settings. If delegated access is used, implicitly specify the mailboxes to search in the \"Mailboxes\" parameter.")], how_many_mailboxes_to_process_in_a_single_batch: Annotated[str, Field(default=None, description="In case \"Perform action in all mailboxes\" is checked, action works in batches, this parameter controls how many mailboxes action should process in single batch (single connection to mail server).")], target_entities: Annotated[List[TargetEntity], PydanticListField(TargetEntity, description="Optional list of specific target entities (Identifier, EntityType) to run the action on.")], scope: Annotated[str, Field(default="All entities", description="Defines the scope for the action.")]) -> dict:
        """Action will get as a parameter a rule name, from the Exchange-Siemplify Inbox rules, and will list it. If no mailboxes to list for will be provided, the rules for the logged in user will be listed. NOTICE - to perform operation, please configure EDiscovery Group and Author permissions. For full details, please visit: https://cloud.google.com/chronicle/docs/soar/marketplace-integrations/exchang. NOTE: Action is running as async, please adjust script timeout value in Siemplify IDE for action as needed.

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
                Endpoints.LIST_INTEGRATION_INSTANCES.format(INTEGRATION_NAME="Exchange")
            )
            instances = instance_response.get("integration_instances", [])
        except Exception as e:
            print(f"Error fetching instance for Exchange: {e}")
            return {"Status": "Failed", "Message": f"Error fetching instance: {e}"}
    
        if instances:
            instance_identifier = instances[0].get("identifier")
            if not instance_identifier:
                return {"Status": "Failed", "Message": "Instance found but identifier is missing."}
    
            script_params = {}
            script_params["Rule Name To List"] = rule_name_to_list
            if mailboxes_list_to_perform_on is not None:
                script_params["Mailboxes list to perform on"] = mailboxes_list_to_perform_on
            if perform_action_in_all_mailboxes is not None:
                script_params["Perform action in all mailboxes"] = perform_action_in_all_mailboxes
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
                actionName="Exchange_List Exchange-Siemplify Inbox Rules",
                properties={
                    "IntegrationInstance": instance_identifier,
                    "ScriptName": "Exchange_List Exchange-Siemplify Inbox Rules",
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
                print(f"Error executing action Exchange_List Exchange-Siemplify Inbox Rules for Exchange: {e}")
                return {"Status": "Failed", "Message": f"Error executing action: {e}"}
        else:
            print(f"Warning: No active integration instance found for Exchange")
            return {"Status": "Failed", "Message": "No active instance found."}

    @mcp.tool()
    async def exchange_delete_exchange_siemplify_inbox_rules(case_id: Annotated[str, Field(..., description="The ID of the case.")], alert_group_identifiers: Annotated[List[str], Field(..., description="Identifiers for the alert groups.")], rule_name_to_delete: Annotated[List[str], Field(..., description="Specify the Rule name you would like to completely delete from the relevant mailboxes")], perform_action_in_all_mailboxes: Annotated[bool, Field(default=None, description="If checked, action will be performed in all mailboxes accessible with current impersonalization settings. If delegated access is used, implicitly specify the mailboxes to search in the \"Mailboxes\" parameter.")], how_many_mailboxes_to_process_in_a_single_batch: Annotated[str, Field(default=None, description="In case \"Perform action in all mailboxes\" is checked, action works in batches, this parameter controls how many mailboxes action should process in single batch (single connection to mail server).")], target_entities: Annotated[List[TargetEntity], PydanticListField(TargetEntity, description="Optional list of specific target entities (Identifier, EntityType) to run the action on.")], scope: Annotated[str, Field(default="All entities", description="Defines the scope for the action.")]) -> dict:
        """Action will get as a parameter a rule name and will delete it from all the specified mailboxes. WARNING: Action will modify your current users inbox rules, using EWS. NOTICE - to perform operation, please configure EDiscovery Group and Author permissions. For full details, please visit: https://cloud.google.com/chronicle/docs/soar/marketplace-integrations/exchang. NOTE: Action is running as async, please adjust script timeout value in Siemplify IDE for action as needed.

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
                Endpoints.LIST_INTEGRATION_INSTANCES.format(INTEGRATION_NAME="Exchange")
            )
            instances = instance_response.get("integration_instances", [])
        except Exception as e:
            print(f"Error fetching instance for Exchange: {e}")
            return {"Status": "Failed", "Message": f"Error fetching instance: {e}"}
    
        if instances:
            instance_identifier = instances[0].get("identifier")
            if not instance_identifier:
                return {"Status": "Failed", "Message": "Instance found but identifier is missing."}
    
            script_params = {}
            script_params["Rule Name To Delete"] = rule_name_to_delete
            if perform_action_in_all_mailboxes is not None:
                script_params["Perform action in all mailboxes"] = perform_action_in_all_mailboxes
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
                actionName="Exchange_Delete Exchange-Siemplify Inbox Rules",
                properties={
                    "IntegrationInstance": instance_identifier,
                    "ScriptName": "Exchange_Delete Exchange-Siemplify Inbox Rules",
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
                print(f"Error executing action Exchange_Delete Exchange-Siemplify Inbox Rules for Exchange: {e}")
                return {"Status": "Failed", "Message": f"Error executing action: {e}"}
        else:
            print(f"Warning: No active integration instance found for Exchange")
            return {"Status": "Failed", "Message": "No active instance found."}

    @mcp.tool()
    async def exchange_move_mail_to_folder(case_id: Annotated[str, Field(..., description="The ID of the case.")], alert_group_identifiers: Annotated[List[str], Field(..., description="Identifiers for the alert groups.")], source_folder_name: Annotated[str, Field(..., description="Source folder to move emails from. '/' separator can be used to specify a subfolder to search in, example: Inbox/Subfolder")], destination_folder_name: Annotated[str, Field(..., description="Destination folder to move emails to. '/' separator can be used to specify a subfolder to search in, example: Inbox/Subfolder")], source_mailbox: Annotated[str, Field(default=None, description="Specify the source mailbox to move the email from. Parameter accepts multiple values as a comma-separated string. If multiple values are provided, matching emails are copied from every accessible specified mailbox")], destination_mailbox: Annotated[str, Field(default=None, description="Specify the destination mailbox to move the matching emails to")], message_i_ds: Annotated[str, Field(default=None, description="Filter condition, specify emails with which email ids to find. Should accept comma separated multiple message ids. If message id is provided, subject filter is ignored")], subject_filter: Annotated[str, Field(default=None, description="Filter condition, specify what subject to search for emails")], only_unread: Annotated[bool, Field(default=None, description="Filter condition, specify if search should look only for unread emails")], move_in_all_mailboxes: Annotated[bool, Field(default=None, description="If checked, search and move emails in all mailboxes accessible with current impersonalization settings. If the source or destination mailbox is specified, this parameter is ignored. If delegated access is used, implicitly specify the mailboxes to search in the \"Mailboxes\" parameter.")], how_many_mailboxes_to_process_in_a_single_batch: Annotated[str, Field(default=None, description="In case \"Move in all mailboxes\" is checked, action works in batches, this parameter controls how many mailboxes action should process in single batch (single connection to mail server).")], time_frame_minutes: Annotated[str, Field(default=None, description="Filter condition, specify in what time frame in minutes should action look for emails")], limit_the_amount_of_information_returned_in_the_json_result: Annotated[bool, Field(default=None, description="If enabled, the amount of information returned by the action will be limited only to the key email fields.")], disable_the_action_json_result: Annotated[bool, Field(default=None, description="If enabled, action will not return JSON result.")], target_entities: Annotated[List[TargetEntity], PydanticListField(TargetEntity, description="Optional list of specific target entities (Identifier, EntityType) to run the action on.")], scope: Annotated[str, Field(default="All entities", description="Defines the scope for the action.")]) -> dict:
        """
Move one or multiple emails from source email folder to another folder in mailbox. NOTICE - to search and move emails in all mailboxes, please configure impersonation permissions. https://docs.microsoft.com/en-us/exchange/client-developer/exchange-web-services/impersonation-and-ews-in-exchange. Note: Action is running as async, please adjust script timeout value in Siemplify IDE for action as needed.

Action Parameters: Source Folder Name: Required A source folder to move emails from., Destination Folder Name: Required A destination folder to move emails to., Subject Filter: Optional A filter condition to search emails by specific subject., Message IDs: Optional A filter condition to search for emails with specific email IDs. This parameter also accepts a comma-separated list of message IDs to search for. If you provide the message ID, the action ignores the Subject Filter parameter., Only Unread: Optional A filter condition to search only for unread emails. Not selected by default., Move In All Mailboxes: Optional If selected, the action searches and moves emails in all mailboxes accessible through current impersonalization settings. Not selected by default., How many mailboxes to process in a single batch: Required The number of mailboxes to process in a single batch (single connection to the mail server).If you select the Move In All Mailboxes parameter, the action works in batches. The default value is 25., Time Frame (minutes): Optional A period in minutes to search for emails., Limit the Amount of Information Returned in the JSON Result: Optional If selected, the action returns information only about the key email fields. If not selected, the action returns information about all email fields.Selected by default., Disable the Action JSON Result: Optional If selected, the action doesn't return the JSON result. Not selected by default.

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
                Endpoints.LIST_INTEGRATION_INSTANCES.format(INTEGRATION_NAME="Exchange")
            )
            instances = instance_response.get("integration_instances", [])
        except Exception as e:
            print(f"Error fetching instance for Exchange: {e}")
            return {"Status": "Failed", "Message": f"Error fetching instance: {e}"}
    
        if instances:
            instance_identifier = instances[0].get("identifier")
            if not instance_identifier:
                return {"Status": "Failed", "Message": "Instance found but identifier is missing."}
    
            script_params = {}
            script_params["Source Folder Name"] = source_folder_name
            script_params["Destination Folder Name"] = destination_folder_name
            if source_mailbox is not None:
                script_params["Source Mailbox"] = source_mailbox
            if destination_mailbox is not None:
                script_params["Destination Mailbox"] = destination_mailbox
            if message_i_ds is not None:
                script_params["Message IDs"] = message_i_ds
            if subject_filter is not None:
                script_params["Subject Filter"] = subject_filter
            if only_unread is not None:
                script_params["Only Unread"] = only_unread
            if move_in_all_mailboxes is not None:
                script_params["Move in all mailboxes"] = move_in_all_mailboxes
            if how_many_mailboxes_to_process_in_a_single_batch is not None:
                script_params["How many mailboxes to process in a single batch"] = how_many_mailboxes_to_process_in_a_single_batch
            if time_frame_minutes is not None:
                script_params["Time Frame (minutes)"] = time_frame_minutes
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
                actionName="Exchange_Move Mail To Folder",
                properties={
                    "IntegrationInstance": instance_identifier,
                    "ScriptName": "Exchange_Move Mail To Folder",
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
                print(f"Error executing action Exchange_Move Mail To Folder for Exchange: {e}")
                return {"Status": "Failed", "Message": f"Error executing action: {e}"}
        else:
            print(f"Warning: No active integration instance found for Exchange")
            return {"Status": "Failed", "Message": "No active instance found."}

    @mcp.tool()
    async def exchange_send_email_and_wait(case_id: Annotated[str, Field(..., description="The ID of the case.")], alert_group_identifiers: Annotated[List[str], Field(..., description="Identifiers for the alert groups.")], subject: Annotated[str, Field(..., description="The subject of the email")], send_to: Annotated[str, Field(..., description="Recipient email address. Multiple addresses can be separated by commas")], mail_content: Annotated[EmailContent, Field(..., description="Email body")], cc: Annotated[str, Field(default=None, description="CC email address. Multiple addresses can be separated by commas")], bcc: Annotated[str, Field(default=None, description="bcc email address. Multiple addresses can be separated by commas")], fetch_response_attachments: Annotated[bool, Field(default=None, description="Allows attachment of files from response mail.")], folder_to_check_for_reply: Annotated[str, Field(default=None, description="Parameter can be used to specify mailbox email folder (mailbox that was used to send the email with question) to search for the user reply in this folder. Parameter should also accept comma separated list of folders to check the user response in multiple folders. Parameter is case sensitive. '/' separator can be used to specify a subfolder to search in, example: Inbox/Subfolder")], target_entities: Annotated[List[TargetEntity], PydanticListField(TargetEntity, description="Optional list of specific target entities (Identifier, EntityType) to run the action on.")], scope: Annotated[str, Field(default="All entities", description="Defines the scope for the action.")]) -> dict:
        """Send email and wait action, Send to field is comma separated. Note: Sender's display name can be configured in the client under the account settings

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
                Endpoints.LIST_INTEGRATION_INSTANCES.format(INTEGRATION_NAME="Exchange")
            )
            instances = instance_response.get("integration_instances", [])
        except Exception as e:
            print(f"Error fetching instance for Exchange: {e}")
            return {"Status": "Failed", "Message": f"Error fetching instance: {e}"}
    
        if instances:
            instance_identifier = instances[0].get("identifier")
            if not instance_identifier:
                return {"Status": "Failed", "Message": "Instance found but identifier is missing."}
    
            script_params = {}
            script_params["Subject"] = subject
            script_params["Send to"] = send_to
            if cc is not None:
                script_params["CC"] = cc
            if bcc is not None:
                script_params["BCC"] = bcc
            mail_content = mail_content.model_dump()
            script_params["Mail content"] = mail_content
            if fetch_response_attachments is not None:
                script_params["Fetch Response Attachments"] = fetch_response_attachments
            if folder_to_check_for_reply is not None:
                script_params["Folder to Check for Reply"] = folder_to_check_for_reply
    
            # Prepare data model for the API request
            action_data = ApiManualActionDataModel(
                alertGroupIdentifiers=alert_group_identifiers,
                caseId=case_id,
                targetEntities=final_target_entities,
                scope=final_scope,
                isPredefinedScope=is_predefined_scope,
                actionProvider="Scripts",
                actionName="Exchange_Send Email And Wait",
                properties={
                    "IntegrationInstance": instance_identifier,
                    "ScriptName": "Exchange_Send Email And Wait",
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
                print(f"Error executing action Exchange_Send Email And Wait for Exchange: {e}")
                return {"Status": "Failed", "Message": f"Error executing action: {e}"}
        else:
            print(f"Warning: No active integration instance found for Exchange")
            return {"Status": "Failed", "Message": "No active instance found."}

    @mcp.tool()
    async def exchange_ping(case_id: Annotated[str, Field(..., description="The ID of the case.")], alert_group_identifiers: Annotated[List[str], Field(..., description="Identifiers for the alert groups.")], target_entities: Annotated[List[TargetEntity], PydanticListField(TargetEntity, description="Optional list of specific target entities (Identifier, EntityType) to run the action on.")], scope: Annotated[str, Field(default="All entities", description="Defines the scope for the action.")]) -> dict:
        """Test connectivity to Microsoft Exchange instance with parameters provided at the integration configuration page on Marketplace tab.

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
                Endpoints.LIST_INTEGRATION_INSTANCES.format(INTEGRATION_NAME="Exchange")
            )
            instances = instance_response.get("integration_instances", [])
        except Exception as e:
            print(f"Error fetching instance for Exchange: {e}")
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
                actionName="Exchange_Ping",
                properties={
                    "IntegrationInstance": instance_identifier,
                    "ScriptName": "Exchange_Ping",
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
                print(f"Error executing action Exchange_Ping for Exchange: {e}")
                return {"Status": "Failed", "Message": f"Error executing action: {e}"}
        else:
            print(f"Warning: No active integration instance found for Exchange")
            return {"Status": "Failed", "Message": "No active instance found."}

    @mcp.tool()
    async def exchange_extract_eml_data(case_id: Annotated[str, Field(..., description="The ID of the case.")], alert_group_identifiers: Annotated[List[str], Field(..., description="Identifiers for the alert groups.")], message_id: Annotated[str, Field(..., description="e.g. <1701cf01ba314032b2f1df43262a7723@gmail.com>")], folder_name: Annotated[str, Field(default=None, description="Folder to fetch from. Default is Inbox. '/' separator can be used to specify a subfolder to search in, example: Inbox/Subfolder")], regex_map_json: Annotated[Union[str, dict], Field(default=None, description="e.g. {ips: \\b\\\\d{1,3}\\\\.\\\\d{1,3}\\\\.\\\\d{1,3}\\\\.\\\\d{1,3}\\b}")], target_entities: Annotated[List[TargetEntity], PydanticListField(TargetEntity, description="Optional list of specific target entities (Identifier, EntityType) to run the action on.")], scope: Annotated[str, Field(default="All entities", description="Defines the scope for the action.")]) -> dict:
        """
Extract data from email's EML attachments.

Action Parameters: Folder Name: Optional Folder to fetch an email from.Default value is Inbox. The Exchange integration uses backslashes as separators to specify subfolders, such as folder/subfolder1/subfolder2. To avoid the timeout error or action failure, replace backslashes in folder or subfolder names with other characters like underscore., Message ID: Required Message ID, such as 1701cf01ba314032b2f1df43262a7723@example.com., Regex Map JSON: Optional Regular expression to select emails based on matching the email body part, for example, {ips: \b\\d{1,3}\\.\\d{1,3}\\.\\d{1,3}\\.\\d{1,3}\b}.

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
                Endpoints.LIST_INTEGRATION_INSTANCES.format(INTEGRATION_NAME="Exchange")
            )
            instances = instance_response.get("integration_instances", [])
        except Exception as e:
            print(f"Error fetching instance for Exchange: {e}")
            return {"Status": "Failed", "Message": f"Error fetching instance: {e}"}
    
        if instances:
            instance_identifier = instances[0].get("identifier")
            if not instance_identifier:
                return {"Status": "Failed", "Message": "Instance found but identifier is missing."}
    
            script_params = {}
            if folder_name is not None:
                script_params["Folder Name"] = folder_name
            script_params["Message ID"] = message_id
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
                actionName="Exchange_Extract EML Data",
                properties={
                    "IntegrationInstance": instance_identifier,
                    "ScriptName": "Exchange_Extract EML Data",
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
                print(f"Error executing action Exchange_Extract EML Data for Exchange: {e}")
                return {"Status": "Failed", "Message": f"Error executing action: {e}"}
        else:
            print(f"Warning: No active integration instance found for Exchange")
            return {"Status": "Failed", "Message": "No active instance found."}

    @mcp.tool()
    async def exchange_remove_domains_from_exchange_siemplify_inbox_rules(case_id: Annotated[str, Field(..., description="The ID of the case.")], alert_group_identifiers: Annotated[List[str], Field(..., description="Identifiers for the alert groups.")], rule_to_remove_domains_from: Annotated[List[str], Field(..., description="Specify the rule to remove the Domains from. If the rule doesn\u2019t exist - action will do nothing.")], domains: Annotated[str, Field(default=None, description="Specify the Domains you would like to remove from the rule, in a comma separated list.")], remove_domains_from_all_available_rules: Annotated[bool, Field(default=None, description="Specify whether action should look for the provided domains in all of Siemplify inbox rules.")], perform_action_in_all_mailboxes: Annotated[bool, Field(default=None, description="If checked, action will be performed in all mailboxes accessible with current impersonalization settings. If delegated access is used, implicitly specify the mailboxes to search in the \"Mailboxes\" parameter.")], how_many_mailboxes_to_process_in_a_single_batch: Annotated[str, Field(default=None, description="In case \"Perform action in all mailboxes\" is checked, action works in batches, this parameter controls how many mailboxes action should process in single batch (single connection to mail server).")], target_entities: Annotated[List[TargetEntity], PydanticListField(TargetEntity, description="Optional list of specific target entities (Identifier, EntityType) to run the action on.")], scope: Annotated[str, Field(default="All entities", description="Defines the scope for the action.")]) -> dict:
        """Action will get as a parameter a list of Domains, and will be able to remove the provided domains from the existing rules. WARNING: Action will modify your current users inbox rules, using EWS. NOTICE - to perform operation, please configure EDiscovery Group and Author permissions. For full details, please visit: https://cloud.google.com/chronicle/docs/soar/marketplace-integrations/exchang. NOTE: Action is running as async, please adjust script timeout value in Siemplify IDE for action as needed.

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
                Endpoints.LIST_INTEGRATION_INSTANCES.format(INTEGRATION_NAME="Exchange")
            )
            instances = instance_response.get("integration_instances", [])
        except Exception as e:
            print(f"Error fetching instance for Exchange: {e}")
            return {"Status": "Failed", "Message": f"Error fetching instance: {e}"}
    
        if instances:
            instance_identifier = instances[0].get("identifier")
            if not instance_identifier:
                return {"Status": "Failed", "Message": "Instance found but identifier is missing."}
    
            script_params = {}
            if domains is not None:
                script_params["Domains"] = domains
            script_params["Rule to remove Domains from"] = rule_to_remove_domains_from
            if remove_domains_from_all_available_rules is not None:
                script_params["Remove Domains from all available Rules"] = remove_domains_from_all_available_rules
            if perform_action_in_all_mailboxes is not None:
                script_params["Perform action in all mailboxes"] = perform_action_in_all_mailboxes
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
                actionName="Exchange_Remove Domains from Exchange-Siemplify Inbox Rules",
                properties={
                    "IntegrationInstance": instance_identifier,
                    "ScriptName": "Exchange_Remove Domains from Exchange-Siemplify Inbox Rules",
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
                print(f"Error executing action Exchange_Remove Domains from Exchange-Siemplify Inbox Rules for Exchange: {e}")
                return {"Status": "Failed", "Message": f"Error executing action: {e}"}
        else:
            print(f"Warning: No active integration instance found for Exchange")
            return {"Status": "Failed", "Message": "No active instance found."}

    @mcp.tool()
    async def exchange_remove_senders_from_exchange_siemplify_inbox_rules(case_id: Annotated[str, Field(..., description="The ID of the case.")], alert_group_identifiers: Annotated[List[str], Field(..., description="Identifiers for the alert groups.")], rule_to_remove_senders_from: Annotated[List[str], Field(..., description="Specify the rule to remove the Senders from. If the rule doesn't exist - action will do nothing.")], senders: Annotated[str, Field(default=None, description="Specify the Senders you would like to remove from the rule, in a comma separated list. If no parameter will be provided, action will work with entities.")], remove_senders_from_all_available_rules: Annotated[bool, Field(default=None, description="Specify whether action should look for the provided Senders in all of Siemplify inbox rules.")], should_remove_senders_domains_from_the_corresponding_domains_list_rule_as_well: Annotated[bool, Field(default=None, description="Specify whether the action should automatically take the domains of the provided email addresses and remove them as well from the corresponding domain rules (same rule action for domains)")], perform_action_in_all_mailboxes: Annotated[bool, Field(default=None, description="If checked, action will be performed in all mailboxes accessible with current impersonalization settings. If delegated access is used, implicitly specify the mailboxes to search in the \"Mailboxes\" parameter.")], how_many_mailboxes_to_process_in_a_single_batch: Annotated[str, Field(default=None, description="In case \"Perform action in all mailboxes\" is checked, action works in batches, this parameter controls how many mailboxes action should process in single batch (single connection to mail server).")], target_entities: Annotated[List[TargetEntity], PydanticListField(TargetEntity, description="Optional list of specific target entities (Identifier, EntityType) to run the action on.")], scope: Annotated[str, Field(default="All entities", description="Defines the scope for the action.")]) -> dict:
        """Action will get as a parameter a list of Senders, or will work on User entities (if parameters are not provided), and will be able to remove the provided Senders from the existing rules. WARNING: Action will modify your current users inbox rules, using EWS. NOTICE - to perform operation, please configure EDiscovery Group and Author permissions. For full details, please visit: https://cloud.google.com/chronicle/docs/soar/marketplace-integrations/exchang. NOTE: Action is running as async, please adjust script timeout value in Siemplify IDE for action as needed.

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
                Endpoints.LIST_INTEGRATION_INSTANCES.format(INTEGRATION_NAME="Exchange")
            )
            instances = instance_response.get("integration_instances", [])
        except Exception as e:
            print(f"Error fetching instance for Exchange: {e}")
            return {"Status": "Failed", "Message": f"Error fetching instance: {e}"}
    
        if instances:
            instance_identifier = instances[0].get("identifier")
            if not instance_identifier:
                return {"Status": "Failed", "Message": "Instance found but identifier is missing."}
    
            script_params = {}
            if senders is not None:
                script_params["Senders"] = senders
            script_params["Rule to remove Senders from"] = rule_to_remove_senders_from
            if remove_senders_from_all_available_rules is not None:
                script_params["Remove Senders from all available Rules"] = remove_senders_from_all_available_rules
            if should_remove_senders_domains_from_the_corresponding_domains_list_rule_as_well is not None:
                script_params["Should remove senders' domains from the corresponding Domains List rule as well?"] = should_remove_senders_domains_from_the_corresponding_domains_list_rule_as_well
            if perform_action_in_all_mailboxes is not None:
                script_params["Perform action in all mailboxes"] = perform_action_in_all_mailboxes
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
                actionName="Exchange_Remove Senders from Exchange-Siemplify Inbox Rules",
                properties={
                    "IntegrationInstance": instance_identifier,
                    "ScriptName": "Exchange_Remove Senders from Exchange-Siemplify Inbox Rules",
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
                print(f"Error executing action Exchange_Remove Senders from Exchange-Siemplify Inbox Rules for Exchange: {e}")
                return {"Status": "Failed", "Message": f"Error executing action: {e}"}
        else:
            print(f"Warning: No active integration instance found for Exchange")
            return {"Status": "Failed", "Message": "No active instance found."}

    @mcp.tool()
    async def exchange_save_mail_attachments_to_the_case(case_id: Annotated[str, Field(..., description="The ID of the case.")], alert_group_identifiers: Annotated[List[str], Field(..., description="Identifiers for the alert groups.")], folder_name: Annotated[str, Field(..., description="Parameter can be used to specify email folder on the mailbox to search for the emails. Parameter should also accept comma separated list of folders to check the user response in multiple folders. Parameter is case sensitive. '/' separator can be used to specify a subfolder to search in, example: Inbox/Subfolder")], message_id: Annotated[str, Field(..., description="Message id to find an email to download attachments from.")], attachment_to_save: Annotated[str, Field(default=None, description="If parameter is not specified - save all email attachments to the case wall. If parameter specified - save only matching attachment to the case wall.")], target_entities: Annotated[List[TargetEntity], PydanticListField(TargetEntity, description="Optional list of specific target entities (Identifier, EntityType) to run the action on.")], scope: Annotated[str, Field(default="All entities", description="Defines the scope for the action.")]) -> dict:
        """
Save email attachments from email stored in monitored mailbox to the Case Wall.

Action Parameters: Folder Name: Required A mailbox folder to search an email in.This parameter also accepts a comma-separated list of folders.The Exchange integration uses backslashes as separators to specify subfolders, such as folder/subfolder1/subfolder2. To avoid the timeout error or action failure, replace backslashes in folder or subfolder names with other characters like underscore., Message IDs: Required The message ID to find a specific email and download attachments from it., Attachment To Save: Optional If you don't configure this parameter, the action saves all email attachments to the Case Wall by default. Otherwise, the action saves only the attachment which you specified to the Case Wall.

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
                Endpoints.LIST_INTEGRATION_INSTANCES.format(INTEGRATION_NAME="Exchange")
            )
            instances = instance_response.get("integration_instances", [])
        except Exception as e:
            print(f"Error fetching instance for Exchange: {e}")
            return {"Status": "Failed", "Message": f"Error fetching instance: {e}"}
    
        if instances:
            instance_identifier = instances[0].get("identifier")
            if not instance_identifier:
                return {"Status": "Failed", "Message": "Instance found but identifier is missing."}
    
            script_params = {}
            script_params["Folder Name"] = folder_name
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
                actionName="Exchange_Save Mail Attachments To The Case",
                properties={
                    "IntegrationInstance": instance_identifier,
                    "ScriptName": "Exchange_Save Mail Attachments To The Case",
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
                print(f"Error executing action Exchange_Save Mail Attachments To The Case for Exchange: {e}")
                return {"Status": "Failed", "Message": f"Error executing action: {e}"}
        else:
            print(f"Warning: No active integration instance found for Exchange")
            return {"Status": "Failed", "Message": "No active instance found."}

    @mcp.tool()
    async def exchange_download_attachments(case_id: Annotated[str, Field(..., description="The ID of the case.")], alert_group_identifiers: Annotated[List[str], Field(..., description="Identifiers for the alert groups.")], folder_name: Annotated[str, Field(..., description="Parameter can be used to specify email folder on the mailbox to search for the emails. Parameter should also accept comma separated list of folders to check the user response in multiple folders. Parameter is case sensitive. '/' separator can be used to specify a subfolder to search in, example: Inbox/Subfolder")], download_path: Annotated[str, Field(..., description="File path on the server where to download the email attachments")], message_i_ds: Annotated[str, Field(default=None, description="Filter condition, specify emails with which email ids to find. Should accept comma separated multiple message ids. If message id is provided, subject filter is ignored")], subject_filter: Annotated[str, Field(default=None, description="Filter condition to search emails by specific subject")], sender_filter: Annotated[str, Field(default=None, description="Filter condition to search emails by specific sender")], only_unread: Annotated[bool, Field(default=None, description="If checked, download attachments only from unread emails")], download_attachments_from_eml: Annotated[bool, Field(default=None, description="If checked, download attachments also from attached EML files")], download_attachments_to_unique_path: Annotated[bool, Field(default=None, description="If checked, download attachments to unique path  under file path provided in \u201cDownload Path\u201d parameter to avoid previously downloaded attachments overwrite.")], search_in_all_mailboxes: Annotated[bool, Field(default=None, description="If checked, search in all mailboxes accessible with current impersonalization settings. If delegated access is used, implicitly specify the mailboxes to search in the \"Mailboxes\" parameter.")], how_many_mailboxes_to_process_in_a_single_batch: Annotated[str, Field(default=None, description="In case \"Search in all mailboxes\" is checked, action works in batches, this parameter controls how many mailboxes action should process in single batch (single connection to mail server).")], mailboxes: Annotated[str, Field(default=None, description="Specify a comma-separated list of mailboxes that need to be searched. This parameter has priority over \"Search in all mailboxes\".")], target_entities: Annotated[List[TargetEntity], PydanticListField(TargetEntity, description="Optional list of specific target entities (Identifier, EntityType) to run the action on.")], scope: Annotated[str, Field(default="All entities", description="Defines the scope for the action.")]) -> dict:
        """
Download email attachments from email to specific file path on Siemplify server. NOTICE - to search for an email in all mailboxes, please configure impersonation permissions. https://docs.microsoft.com/en-us/exchange/client-developer/exchange-web-services/impersonation-and-ews-in-exchange. Note: Action is running as async, please adjust script timeout value in Siemplify IDE for action as needed. Additionally, please note that if the downloaded attachments have "/" or "" characters in the names, those will be replaced with the '_' character.

Action Parameters: Folder Name: Optional A mailbox folder to search an email in.This parameter accepts a comma-separated list of folders.The Exchange integration uses backslashes as separators to specify subfolders, such as folder/subfolder1/subfolder2. To avoid the timeout error or action failure, replace backslashes in folder or subfolder names with other characters like underscore., Download Path: Required A path on the {{google_secops_name_short}} server to download email attachments., Message IDs: Optional A filter condition to search for emails with specific email IDs. This parameter accepts a comma-separated list of message IDs to search for. If you provide the message ID, the action ignores the Subject Filter parameter., Subject Filter: Optional A filter condition that specifies the email subject to search for., Sender Filter: Optional A filter condition that specifies the email sender to search for., Only Unread: Optional If selected, the action downloads attachments only from unread emails. Not selected by default., Download Attachments from EML: Optional If selected, the action downloads attachments from attached EML files. Not selected by default., Download Attachments to unique path?: Optional If selected, the action downloads attachments to a unique path under the value provided in the Download Path parameter to avoid overwriting the previously downloaded attachments. Not selected by default., Search in all mailboxes: Optional If selected, the action runs a search in all mailboxes accessible using the current impersonation settings.Not selected by default., How many mailboxes to process in a single batch: Required The number of mailboxes to process in a single batch (single connection to the mail server). If you selected the Search in all mailboxes parameter, the action works in batches.The default value is 25., Mailboxes: Optional A comma-separated list of mailboxes to run a search through.This parameter has a priority over the Search in all mailboxes parameter.

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
                Endpoints.LIST_INTEGRATION_INSTANCES.format(INTEGRATION_NAME="Exchange")
            )
            instances = instance_response.get("integration_instances", [])
        except Exception as e:
            print(f"Error fetching instance for Exchange: {e}")
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
            if sender_filter is not None:
                script_params["Sender Filter"] = sender_filter
            if only_unread is not None:
                script_params["Only Unread"] = only_unread
            if download_attachments_from_eml is not None:
                script_params["Download Attachments from EML"] = download_attachments_from_eml
            if download_attachments_to_unique_path is not None:
                script_params["Download Attachments to unique path?"] = download_attachments_to_unique_path
            if search_in_all_mailboxes is not None:
                script_params["Search in all mailboxes"] = search_in_all_mailboxes
            if how_many_mailboxes_to_process_in_a_single_batch is not None:
                script_params["How many mailboxes to process in a single batch"] = how_many_mailboxes_to_process_in_a_single_batch
            if mailboxes is not None:
                script_params["Mailboxes"] = mailboxes
    
            # Prepare data model for the API request
            action_data = ApiManualActionDataModel(
                alertGroupIdentifiers=alert_group_identifiers,
                caseId=case_id,
                targetEntities=final_target_entities,
                scope=final_scope,
                isPredefinedScope=is_predefined_scope,
                actionProvider="Scripts",
                actionName="Exchange_Download Attachments",
                properties={
                    "IntegrationInstance": instance_identifier,
                    "ScriptName": "Exchange_Download Attachments",
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
                print(f"Error executing action Exchange_Download Attachments for Exchange: {e}")
                return {"Status": "Failed", "Message": f"Error executing action: {e}"}
        else:
            print(f"Warning: No active integration instance found for Exchange")
            return {"Status": "Failed", "Message": "No active instance found."}

    @mcp.tool()
    async def exchange_send_mail_html(case_id: Annotated[str, Field(..., description="The ID of the case.")], alert_group_identifiers: Annotated[List[str], Field(..., description="Identifiers for the alert groups.")], subject: Annotated[str, Field(..., description="The subject of the email")], send_to: Annotated[str, Field(..., description="Recipient email address. Multiple addresses can be separated by commas")], mail_content: Annotated[EmailContent, Field(..., description="Mail body")], cc: Annotated[str, Field(default=None, description="CC email address. Multiple addresses can be separated by commas")], bcc: Annotated[str, Field(default=None, description="BCC email address. Multiple addresses can be separated by commas")], attachments_paths: Annotated[str, Field(default=None, description="Full path to attachments to be uploaded. Comma sepreated. e.g. C:\\Desktop\\x.txt,C:\\Desktop\\sample.txt")], target_entities: Annotated[List[TargetEntity], PydanticListField(TargetEntity, description="Optional list of specific target entities (Identifier, EntityType) to run the action on.")], scope: Annotated[str, Field(default="All entities", description="Defines the scope for the action.")]) -> dict:
        """
Send an email with HTML template content, Send to field is comma separated. Note: Sender's display name can be configured in the client under the account settings

Action Parameters: Subject: Required The email subject., Send to: Required A comma-separated list of email addresses for the email recipients., CC: Optional A comma-separated list of email addresses for the email CC field., BCC: Optional A comma-separated list of email addresses for the email BCC field., Attachments Paths: Optional A comma-separated list of paths for file attachments stored on the server, for example, C:\FILE_DIRECTORY\file.pdf, C:\FILE_DIRECTORY\image.jpg., Mail content: Required The email body.

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
                Endpoints.LIST_INTEGRATION_INSTANCES.format(INTEGRATION_NAME="Exchange")
            )
            instances = instance_response.get("integration_instances", [])
        except Exception as e:
            print(f"Error fetching instance for Exchange: {e}")
            return {"Status": "Failed", "Message": f"Error fetching instance: {e}"}
    
        if instances:
            instance_identifier = instances[0].get("identifier")
            if not instance_identifier:
                return {"Status": "Failed", "Message": "Instance found but identifier is missing."}
    
            script_params = {}
            script_params["Subject"] = subject
            script_params["Send to"] = send_to
            if cc is not None:
                script_params["CC"] = cc
            if bcc is not None:
                script_params["BCC"] = bcc
            if attachments_paths is not None:
                script_params["Attachments Paths"] = attachments_paths
            mail_content = mail_content.model_dump()
            script_params["Mail content"] = mail_content
    
            # Prepare data model for the API request
            action_data = ApiManualActionDataModel(
                alertGroupIdentifiers=alert_group_identifiers,
                caseId=case_id,
                targetEntities=final_target_entities,
                scope=final_scope,
                isPredefinedScope=is_predefined_scope,
                actionProvider="Scripts",
                actionName="Exchange_Send Mail HTML",
                properties={
                    "IntegrationInstance": instance_identifier,
                    "ScriptName": "Exchange_Send Mail HTML",
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
                print(f"Error executing action Exchange_Send Mail HTML for Exchange: {e}")
                return {"Status": "Failed", "Message": f"Error executing action: {e}"}
        else:
            print(f"Warning: No active integration instance found for Exchange")
            return {"Status": "Failed", "Message": "No active instance found."}

    @mcp.tool()
    async def exchange_delete_mail(case_id: Annotated[str, Field(..., description="The ID of the case.")], alert_group_identifiers: Annotated[List[str], Field(..., description="Identifiers for the alert groups.")], folder_name: Annotated[str, Field(default=None, description="Parameter can be used to specify email folder on the mailbox to search for the emails. Parameter should also accept comma separated list of folders to check the user response in multiple folders. Parameter is case sensitive. '/' separator can be used to specify a subfolder to search in, example: Inbox/Subfolder")], message_i_ds: Annotated[str, Field(default=None, description="Filter condition, specify emails with which email ids to find. Should accept comma separated list of message ids to search for. If message id is provided, subject, sender and recipient filters are ignored.")], mailboxes: Annotated[str, Field(default=None, description="Specify a comma-separated list of mailboxes that need to be searched. This parameter has priority over \u201cDelete in all mailboxes\u201c.")], subject_filter: Annotated[str, Field(default=None, description="Filter condition, specify subject to search for emails")], sender_filter: Annotated[str, Field(default=None, description="Filter condition, specify who should be the sender of needed emails")], recipient_filter: Annotated[str, Field(default=None, description="Filter condition, specify who should be the recipient of needed emails")], delete_all_matching_emails: Annotated[bool, Field(default=None, description="Filter condition, specify if action should delete all matched by criteria emails from the mailbox or delete only first match.")], delete_from_all_mailboxes: Annotated[bool, Field(default=None, description="If checked, delete emails in all mailboxes accessible with current impersonalization settings. If delegated access is used, implicitly specify the mailboxes to search in the \"Mailboxes\" parameter.")], how_many_mailboxes_to_process_in_a_single_batch: Annotated[str, Field(default=None, description="In case \"Delete from all mailboxes\" is checked, action works in batches, this parameter controls how many mailboxes action should process in single batch (single connection to mail server).")], time_frame_minutes: Annotated[str, Field(default=None, description="Filter condition, specify in what time frame in minutes should action look for emails")], target_entities: Annotated[List[TargetEntity], PydanticListField(TargetEntity, description="Optional list of specific target entities (Identifier, EntityType) to run the action on.")], scope: Annotated[str, Field(default="All entities", description="Defines the scope for the action.")]) -> dict:
        """
Delete one or multiple email from the mailbox that matches search criterias. Delete can be done for the first email that matched the search criteria, or it can be done for all matching emails. NOTICE - to delete emails in all mailboxes, please configure impersonation permissions. https://docs.microsoft.com/en-us/exchange/client-developer/exchange-web-services/impersonation-and-ews-in-exchange. Note: Action is running as async, please adjust script timeout value in Siemplify IDE for action as needed.

Action Parameters: Folder Name: Optional A mailbox folder to search an email in.This parameter accepts a comma-separated list of folders.The Exchange integration uses backslashes as separators to specify subfolders, such as folder/subfolder1/subfolder2. To avoid the timeout error or action failure, replace backslashes in folder or subfolder names with other characters like underscore., Message IDs: Optional A filter condition to search for emails with specific email IDs. This parameter accepts a comma-separated list of message IDs to search for. If you provide the message ID, the action ignores the Subject Filter, Sender Filter, and Recipient Filter parameters., Subject Filter: Optional A filter condition that specifies the email subject to search for., Sender Filter: Optional A filter condition that specifies the sender of requested emails., Recipient Filter: Optional A filter condition that specifies the recipient of requested emails., Delete All Matching Emails: Optional If selected, the action deletes all emails that match the criteria. If not selected, the action deletes only the first matching email. Not selected by default., Delete from all mailboxes: Optional If selected, the action deletes emails in all mailboxes that are accessible using the current impersonation settings., How many mailboxes to process in a single batch: Required The number of mailboxes to process in a single batch (single connection to the mail server). If you selected the Delete from all mailboxes parameter, the action works in batches. The default value is 25., Time Frame (minutes): Optional The period in minutes to search for emails.

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
                Endpoints.LIST_INTEGRATION_INSTANCES.format(INTEGRATION_NAME="Exchange")
            )
            instances = instance_response.get("integration_instances", [])
        except Exception as e:
            print(f"Error fetching instance for Exchange: {e}")
            return {"Status": "Failed", "Message": f"Error fetching instance: {e}"}
    
        if instances:
            instance_identifier = instances[0].get("identifier")
            if not instance_identifier:
                return {"Status": "Failed", "Message": "Instance found but identifier is missing."}
    
            script_params = {}
            if folder_name is not None:
                script_params["Folder Name"] = folder_name
            if message_i_ds is not None:
                script_params["Message IDs"] = message_i_ds
            if mailboxes is not None:
                script_params["Mailboxes"] = mailboxes
            if subject_filter is not None:
                script_params["Subject Filter"] = subject_filter
            if sender_filter is not None:
                script_params["Sender Filter"] = sender_filter
            if recipient_filter is not None:
                script_params["Recipient Filter"] = recipient_filter
            if delete_all_matching_emails is not None:
                script_params["Delete All Matching Emails"] = delete_all_matching_emails
            if delete_from_all_mailboxes is not None:
                script_params["Delete from all mailboxes"] = delete_from_all_mailboxes
            if how_many_mailboxes_to_process_in_a_single_batch is not None:
                script_params["How many mailboxes to process in a single batch"] = how_many_mailboxes_to_process_in_a_single_batch
            if time_frame_minutes is not None:
                script_params["Time Frame (minutes)"] = time_frame_minutes
    
            # Prepare data model for the API request
            action_data = ApiManualActionDataModel(
                alertGroupIdentifiers=alert_group_identifiers,
                caseId=case_id,
                targetEntities=final_target_entities,
                scope=final_scope,
                isPredefinedScope=is_predefined_scope,
                actionProvider="Scripts",
                actionName="Exchange_Delete Mail",
                properties={
                    "IntegrationInstance": instance_identifier,
                    "ScriptName": "Exchange_Delete Mail",
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
                print(f"Error executing action Exchange_Delete Mail for Exchange: {e}")
                return {"Status": "Failed", "Message": f"Error executing action: {e}"}
        else:
            print(f"Warning: No active integration instance found for Exchange")
            return {"Status": "Failed", "Message": "No active instance found."}

    @mcp.tool()
    async def exchange_get_mail_eml_file(case_id: Annotated[str, Field(..., description="The ID of the case.")], alert_group_identifiers: Annotated[List[str], Field(..., description="Identifiers for the alert groups.")], message_id: Annotated[str, Field(..., description="")], base64_encode: Annotated[bool, Field(..., description="")], folder_name: Annotated[str, Field(default=None, description="Folder to fetch from. Default is Inbox. '/' separator can be used to specify a subfolder to search in, example: Inbox/Subfolder")], target_entities: Annotated[List[TargetEntity], PydanticListField(TargetEntity, description="Optional list of specific target entities (Identifier, EntityType) to run the action on.")], scope: Annotated[str, Field(default="All entities", description="Defines the scope for the action.")]) -> dict:
        """
Fetch message EML file.

Action Parameters: Folder Name: Optional A folder to fetch an email from.The Exchange integration uses backslashes as separators to specify subfolders, such as folder/subfolder1/subfolder2. To avoid the timeout error or action failure, replace backslashes in folder or subfolder names with other characters like underscore., Message ID: RequiredThe message ID, such as 1701cf01ba314032b2f1df43262a7723@example.com., Base64 Encode: Optional If selected, the action encodes the mail file with in a base64 format. Not selected by default.

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
                Endpoints.LIST_INTEGRATION_INSTANCES.format(INTEGRATION_NAME="Exchange")
            )
            instances = instance_response.get("integration_instances", [])
        except Exception as e:
            print(f"Error fetching instance for Exchange: {e}")
            return {"Status": "Failed", "Message": f"Error fetching instance: {e}"}
    
        if instances:
            instance_identifier = instances[0].get("identifier")
            if not instance_identifier:
                return {"Status": "Failed", "Message": "Instance found but identifier is missing."}
    
            script_params = {}
            if folder_name is not None:
                script_params["Folder Name"] = folder_name
            script_params["Message ID"] = message_id
            script_params["Base64 Encode"] = base64_encode
    
            # Prepare data model for the API request
            action_data = ApiManualActionDataModel(
                alertGroupIdentifiers=alert_group_identifiers,
                caseId=case_id,
                targetEntities=final_target_entities,
                scope=final_scope,
                isPredefinedScope=is_predefined_scope,
                actionProvider="Scripts",
                actionName="Exchange_Get Mail EML File",
                properties={
                    "IntegrationInstance": instance_identifier,
                    "ScriptName": "Exchange_Get Mail EML File",
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
                print(f"Error executing action Exchange_Get Mail EML File for Exchange: {e}")
                return {"Status": "Failed", "Message": f"Error executing action: {e}"}
        else:
            print(f"Warning: No active integration instance found for Exchange")
            return {"Status": "Failed", "Message": "No active instance found."}

    @mcp.tool()
    async def exchange_get_account_out_of_facility_settings(case_id: Annotated[str, Field(..., description="The ID of the case.")], alert_group_identifiers: Annotated[List[str], Field(..., description="Identifiers for the alert groups.")], target_entities: Annotated[List[TargetEntity], PydanticListField(TargetEntity, description="Optional list of specific target entities (Identifier, EntityType) to run the action on.")], scope: Annotated[str, Field(default="All entities", description="Defines the scope for the action.")]) -> dict:
        """
Get account out of facility (OOF) settings for the provided Siemplify User entity. Note 1: If the target User entity is a username, not a mail address, please run Enrich Entities from Active Directory integration first to try to use the information about User's mail stored in Active Directory. Note 2: For integration to return the information, it should have delegation or impersonation permissions to the target account mailbox. Link to impersonation permission configuration: https://docs.microsoft.com/en-us/exchange/client-developer/exchange-web-services/impersonation-and-ews-in-exchange

Action Parameters: None.

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
                Endpoints.LIST_INTEGRATION_INSTANCES.format(INTEGRATION_NAME="Exchange")
            )
            instances = instance_response.get("integration_instances", [])
        except Exception as e:
            print(f"Error fetching instance for Exchange: {e}")
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
                actionName="Exchange_Get Account Out Of Facility Settings",
                properties={
                    "IntegrationInstance": instance_identifier,
                    "ScriptName": "Exchange_Get Account Out Of Facility Settings",
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
                print(f"Error executing action Exchange_Get Account Out Of Facility Settings for Exchange: {e}")
                return {"Status": "Failed", "Message": f"Error executing action: {e}"}
        else:
            print(f"Warning: No active integration instance found for Exchange")
            return {"Status": "Failed", "Message": "No active instance found."}

    @mcp.tool()
    async def exchange_add_senders_to_exchange_siemplify_inbox_rule(case_id: Annotated[str, Field(..., description="The ID of the case.")], alert_group_identifiers: Annotated[List[str], Field(..., description="Identifiers for the alert groups.")], rule_to_add_senders_to: Annotated[List[str], Field(..., description="Specify the rule to add the sender to. If the rule doesn't exist - action will create it where it's missing.")], senders: Annotated[str, Field(default=None, description="Specify the Senders you would like to add to the rule, in a comma separated list. If no parameter will be provided, action will work with User entities.")], should_add_senders_domain_to_the_corresponding_domains_list_rule_as_well: Annotated[bool, Field(default=None, description="Specify whether the action should automatically take the domains of the provided email addresses and add them as well to the corresponding domain rules (same rule action for domains)")], perform_action_in_all_mailboxes: Annotated[bool, Field(default=None, description="If checked, action will be performed in all mailboxes accessible with current impersonalization settings. If delegated access is used, implicitly specify the mailboxes to search in the \"Mailboxes\" parameter.")], how_many_mailboxes_to_process_in_a_single_batch: Annotated[str, Field(default=None, description="In case \"Perform action in all mailboxes\" is checked, action works in batches, this parameter controls how many mailboxes action should process in single batch (single connection to mail server).")], target_entities: Annotated[List[TargetEntity], PydanticListField(TargetEntity, description="Optional list of specific target entities (Identifier, EntityType) to run the action on.")], scope: Annotated[str, Field(default="All entities", description="Defines the scope for the action.")]) -> dict:
        """Action will get as a parameter a list of Email Addresses, or will work on User entities with Email regexes (if parameters are not provided), and will be able to create a new rule, filtering the senders from your mailboxes. Actions can be modified in the parameters using the rule parameter. WARNING: Action will modify your current users inbox rules, using EWS. NOTICE - to perform operation, please configure EDiscovery Group and Author permissions. For full details, please visit: https://cloud.google.com/chronicle/docs/soar/marketplace-integrations/exchang. NOTE: Action is running as async, please adjust script timeout value in Siemplify IDE for action as needed.

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
                Endpoints.LIST_INTEGRATION_INSTANCES.format(INTEGRATION_NAME="Exchange")
            )
            instances = instance_response.get("integration_instances", [])
        except Exception as e:
            print(f"Error fetching instance for Exchange: {e}")
            return {"Status": "Failed", "Message": f"Error fetching instance: {e}"}
    
        if instances:
            instance_identifier = instances[0].get("identifier")
            if not instance_identifier:
                return {"Status": "Failed", "Message": "Instance found but identifier is missing."}
    
            script_params = {}
            if senders is not None:
                script_params["Senders"] = senders
            script_params["Rule to add senders to"] = rule_to_add_senders_to
            if should_add_senders_domain_to_the_corresponding_domains_list_rule_as_well is not None:
                script_params["Should add senders' domain to the corresponding Domains List rule as well?"] = should_add_senders_domain_to_the_corresponding_domains_list_rule_as_well
            if perform_action_in_all_mailboxes is not None:
                script_params["Perform action in all mailboxes"] = perform_action_in_all_mailboxes
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
                actionName="Exchange_Add Senders to Exchange-Siemplify Inbox Rule",
                properties={
                    "IntegrationInstance": instance_identifier,
                    "ScriptName": "Exchange_Add Senders to Exchange-Siemplify Inbox Rule",
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
                print(f"Error executing action Exchange_Add Senders to Exchange-Siemplify Inbox Rule for Exchange: {e}")
                return {"Status": "Failed", "Message": f"Error executing action: {e}"}
        else:
            print(f"Warning: No active integration instance found for Exchange")
            return {"Status": "Failed", "Message": "No active instance found."}

    @mcp.tool()
    async def exchange_get_authorization(case_id: Annotated[str, Field(..., description="The ID of the case.")], alert_group_identifiers: Annotated[List[str], Field(..., description="Identifiers for the alert groups.")], target_entities: Annotated[List[TargetEntity], PydanticListField(TargetEntity, description="Optional list of specific target entities (Identifier, EntityType) to run the action on.")], scope: Annotated[str, Field(default="All entities", description="Defines the scope for the action.")]) -> dict:
        """For integration configuration with Oauth authentication, run the action and browse to the received URL to get a link with access code. That link needs to be provided to the Generate Token action next to get the refresh token.

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
                Endpoints.LIST_INTEGRATION_INSTANCES.format(INTEGRATION_NAME="Exchange")
            )
            instances = instance_response.get("integration_instances", [])
        except Exception as e:
            print(f"Error fetching instance for Exchange: {e}")
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
                actionName="Exchange_Get Authorization",
                properties={
                    "IntegrationInstance": instance_identifier,
                    "ScriptName": "Exchange_Get Authorization",
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
                print(f"Error executing action Exchange_Get Authorization for Exchange: {e}")
                return {"Status": "Failed", "Message": f"Error executing action: {e}"}
        else:
            print(f"Warning: No active integration instance found for Exchange")
            return {"Status": "Failed", "Message": "No active instance found."}

    @mcp.tool()
    async def exchange_block_sender_by_message_id(case_id: Annotated[str, Field(..., description="The ID of the case.")], alert_group_identifiers: Annotated[List[str], Field(..., description="Identifiers for the alert groups.")], move_item_to_junk_folder: Annotated[bool, Field(..., description="Should the action move the specified messages to the junk folder")], message_i_ds: Annotated[str, Field(default=None, description="Filter condition, specify emails with which message ids to find. Should accept comma separated list of message ids to mark as junk. If message id is provided, subject, sender and recipient filters are ignored.")], mailboxes_list_to_perform_on: Annotated[str, Field(default=None, description="Filter condition, If you have a specific list of mailboxes you would like to conduct the operation on, for better timing, please provide them here. Should accept a comma separated list of mail addresses, to mark the messages as junk in. If a mailboxes list is provided, \"Perform Action in all Mailboxes\" parameter will be ignored.")], folder_name: Annotated[str, Field(default=None, description="Parameter can be used to specify email folder on the mailbox to search for the emails. Parameter should also accept comma separated list of folders to check the user response in multiple folders. Parameter is case sensitive. '/' separator can be used to specify a subfolder to search in, example: Inbox/Subfolder")], subject_filter: Annotated[str, Field(default=None, description="Filter condition, specify subject to search for emails")], sender_filter: Annotated[str, Field(default=None, description="Filter condition, specify who should be the sender of needed emails")], recipient_filter: Annotated[str, Field(default=None, description="Filter condition, specify who should be the recipient of needed emails")], mark_all_matching_emails: Annotated[bool, Field(default=None, description="Filter condition, specify if action should Mark all matched by criteria emails from the mailbox or Mark only first match.")], perform_action_in_all_mailboxes: Annotated[bool, Field(default=None, description="If checked, move to junk and block sender emails in all mailboxes accessible with current impersonalization settings. If delegated access is used, implicitly specify the mailboxes to search in the \"Mailboxes\" parameter.")], how_many_mailboxes_to_process_in_a_single_batch: Annotated[str, Field(default=None, description="In case \"Perform action in all mailboxes\" is checked, action works in batches, this parameter controls how many mailboxes action should process in single batch (single connection to mail server).")], time_frame_minutes: Annotated[str, Field(default=None, description="Filter condition, specify in what time frame in minutes should action look for emails.")], target_entities: Annotated[List[TargetEntity], PydanticListField(TargetEntity, description="Optional list of specific target entities (Identifier, EntityType) to run the action on.")], scope: Annotated[str, Field(default="All entities", description="Defines the scope for the action.")]) -> dict:
        """Action will get as a parameter a list of message IDs, and will be able to mark it as junk. Marking an item as junk using this action will add the item sender's mail address to the "Blocked Senders List", and will also move it to the "Junk" folder. NOTICE - to mark emails in all mailboxes, please configure impersonation permissions: https://docs.microsoft.com/en-us/exchange/client-developer/exchange-web-services/impersonation-and-ews-in-exchange. NOTE: Action is running as async, please adjust script timeout value in Siemplify IDE for action as needed. NOTE: Action is supported only from Exchange Server version 2013 and newer, if a lower version is used, action will fail with the appropriate message.

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
                Endpoints.LIST_INTEGRATION_INSTANCES.format(INTEGRATION_NAME="Exchange")
            )
            instances = instance_response.get("integration_instances", [])
        except Exception as e:
            print(f"Error fetching instance for Exchange: {e}")
            return {"Status": "Failed", "Message": f"Error fetching instance: {e}"}
    
        if instances:
            instance_identifier = instances[0].get("identifier")
            if not instance_identifier:
                return {"Status": "Failed", "Message": "Instance found but identifier is missing."}
    
            script_params = {}
            script_params["Move item to Junk folder?"] = move_item_to_junk_folder
            if message_i_ds is not None:
                script_params["Message IDs"] = message_i_ds
            if mailboxes_list_to_perform_on is not None:
                script_params["Mailboxes list to perform on"] = mailboxes_list_to_perform_on
            if folder_name is not None:
                script_params["Folder Name"] = folder_name
            if subject_filter is not None:
                script_params["Subject Filter"] = subject_filter
            if sender_filter is not None:
                script_params["Sender Filter"] = sender_filter
            if recipient_filter is not None:
                script_params["Recipient Filter"] = recipient_filter
            if mark_all_matching_emails is not None:
                script_params["Mark All Matching Emails"] = mark_all_matching_emails
            if perform_action_in_all_mailboxes is not None:
                script_params["Perform action in all mailboxes"] = perform_action_in_all_mailboxes
            if how_many_mailboxes_to_process_in_a_single_batch is not None:
                script_params["How many mailboxes to process in a single batch"] = how_many_mailboxes_to_process_in_a_single_batch
            if time_frame_minutes is not None:
                script_params["Time Frame (minutes)"] = time_frame_minutes
    
            # Prepare data model for the API request
            action_data = ApiManualActionDataModel(
                alertGroupIdentifiers=alert_group_identifiers,
                caseId=case_id,
                targetEntities=final_target_entities,
                scope=final_scope,
                isPredefinedScope=is_predefined_scope,
                actionProvider="Scripts",
                actionName="Exchange_Block Sender by Message ID",
                properties={
                    "IntegrationInstance": instance_identifier,
                    "ScriptName": "Exchange_Block Sender by Message ID",
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
                print(f"Error executing action Exchange_Block Sender by Message ID for Exchange: {e}")
                return {"Status": "Failed", "Message": f"Error executing action: {e}"}
        else:
            print(f"Warning: No active integration instance found for Exchange")
            return {"Status": "Failed", "Message": "No active instance found."}

    @mcp.tool()
    async def exchange_wait_for_mail_from_user(case_id: Annotated[str, Field(..., description="The ID of the case.")], alert_group_identifiers: Annotated[List[str], Field(..., description="Identifiers for the alert groups.")], mail_message_id: Annotated[str, Field(..., description="Message_id of the email, which current action would be waiting for. If message has been sent using Send Email action, please select SendEmail.JSONResult|message_id field as a placeholder.")], mail_date: Annotated[str, Field(..., description="Send timestamp of the email, which current action would be waiting for. If message has been sent using Send Email action, please select SendEmail.JSONResult|email_date field as a placeholder.")], mail_recipients: Annotated[str, Field(..., description="Comma-separated list of recipient emails, response from which current action would be waiting for. If message has been sent using Send Email action, please select Select SendEmail.JSONResult|to_recipients field as a placeholder.")], how_long_to_wait_for_recipient_reply_minutes: Annotated[str, Field(..., description="How long in minutes to wait for the user's reply before marking it timed out.")], wait_for_all_recipients_to_reply: Annotated[bool, Field(default=None, description="Parameter can be used to define if there are multiple recipients - should the Action wait for responses from all of recipients until timeout, or Action should wait for first reply to proceed.")], wait_stage_exclude_pattern: Annotated[str, Field(default=None, description="Regular expression to exclude specific replies from the wait stage. Works with body part of email. Example is, to exclude automatic Out-Of-Office emails to be considered as recipient reply, and instead wait for actual user reply.")], folder_to_check_for_reply: Annotated[str, Field(default=None, description="Parameter can be used to specify mailbox email folder (mailbox that was used to send the email with question) to search for the user reply in this folder. Parameter should also accept comma separated list of folders to check the user response in multiple folders. Parameter is case sensitive. '/' separator can be used to specify a subfolder to search in, example: Inbox/Subfolder")], fetch_response_attachments: Annotated[bool, Field(default=None, description="If selected, if recipient replies with attachment - fetch recipient response and add it as attachment for the action result")], target_entities: Annotated[List[TargetEntity], PydanticListField(TargetEntity, description="Optional list of specific target entities (Identifier, EntityType) to run the action on.")], scope: Annotated[str, Field(default="All entities", description="Defines the scope for the action.")]) -> dict:
        """Wait for user's response based on an email sent via Send Email action. Note: please adjust the async timeout for action (polling timeout) and global action timeout in Siemplify server configuration as needed. Action input parameter "How long to wait for recipient reply (minutes)" cant be bigger than Siemplify server global timeout value.

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
                Endpoints.LIST_INTEGRATION_INSTANCES.format(INTEGRATION_NAME="Exchange")
            )
            instances = instance_response.get("integration_instances", [])
        except Exception as e:
            print(f"Error fetching instance for Exchange: {e}")
            return {"Status": "Failed", "Message": f"Error fetching instance: {e}"}
    
        if instances:
            instance_identifier = instances[0].get("identifier")
            if not instance_identifier:
                return {"Status": "Failed", "Message": "Instance found but identifier is missing."}
    
            script_params = {}
            script_params["Mail message_id"] = mail_message_id
            script_params["Mail Date"] = mail_date
            script_params["Mail Recipients"] = mail_recipients
            script_params["How long to wait for recipient reply (minutes)"] = how_long_to_wait_for_recipient_reply_minutes
            if wait_for_all_recipients_to_reply is not None:
                script_params["Wait for All Recipients to Reply?"] = wait_for_all_recipients_to_reply
            if wait_stage_exclude_pattern is not None:
                script_params["Wait Stage Exclude pattern"] = wait_stage_exclude_pattern
            if folder_to_check_for_reply is not None:
                script_params["Folder to Check for Reply"] = folder_to_check_for_reply
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
                actionName="Exchange_Wait for mail from user",
                properties={
                    "IntegrationInstance": instance_identifier,
                    "ScriptName": "Exchange_Wait for mail from user",
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
                print(f"Error executing action Exchange_Wait for mail from user for Exchange: {e}")
                return {"Status": "Failed", "Message": f"Error executing action: {e}"}
        else:
            print(f"Warning: No active integration instance found for Exchange")
            return {"Status": "Failed", "Message": "No active instance found."}
