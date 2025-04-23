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
from typing import Optional, Any, List, Dict, Union, Annotated
from pydantic import Field


def register_tools(mcp: FastMCP):
    # This function registers all tools (actions) for the Gmail integration.

    @mcp.tool()
    async def gmail_send_thread_reply(case_id: Annotated[str, Field(..., description="The ID of the case.")], alert_group_identifiers: Annotated[List[str], Field(..., description="Identifiers for the alert groups.")], mailbox: Annotated[str, Field(..., description="A mailbox to search the email in, such as user@example.com. By default, the action uses the default mailbox that you configured for the integration.")], internet_message_id: Annotated[str, Field(..., description="An internet message ID of the email to search for.")], mail_content: Annotated[EmailContent, Field(..., description="The body of an email.")], reply_to: Annotated[Optional[str], Field(default=None, description="A comma-separated list of emails to send the reply to. If you don\u2019t provide any value and the Reply All checkbox is clear, the action only sends a reply to the original email sender. If you select the Reply All parameter, the action ignores this parameter.")], reply_all: Annotated[Optional[bool], Field(default=None, description="If selected, the action sends a reply to all recipients related to the original email. Not selected by default. This parameter has a priority over the Reply To parameter.")], attachments_paths: Annotated[Optional[str], Field(default=None, description="A comma-separated string of paths for file attachments stored on the Google SecOps server.")], target_entities: Annotated[List[TargetEntity], Field(default_factory=list, description="Optional list of specific target entities (Identifier, EntityType) to run the action on.")], scope: Annotated[str, Field(default="All entities", description="Defines the scope for the action.")]) -> dict:
        """Use the Send Thread Reply action to send a message as a reply to the email thread. This action doesn’t run on Google SecOps entities.

        Returns:
            dict: A dictionary containing the result of the action execution.
        """
        # --- Determine scope and target entities for API call ---
        final_target_entities: Optional[List[TargetEntity]] = None
        final_scope: Optional[str] = None
        is_predefined_scope: Optional[bool] = None
    
        if target_entities:
            # Specific target entities provided, ignore scope parameter
            final_target_entities = target_entities
            final_scope = None # Scope is ignored when specific entities are given
            is_predefined_scope = False
        else:
            # No specific target entities, use scope parameter
            # Check if the provided scope is valid
            if scope not in bindings.valid_scopes:
                allowed_values_str = ", ".join(sorted(list(bindings.valid_scopes)))
                return {
                    "Status": "Failed",
                    "Message": f"Invalid scope '{scope}'. Allowed values are: {allowed_values_str}",
                }
            # Scope is valid or validation is not configured
            final_target_entities = [] # Pass empty list for entities when using scope
            final_scope = scope
            is_predefined_scope = True
        # --- End scope/entity logic ---
    
        # Fetch integration instance identifier (assuming this pattern)
        try:
            instance_response = await bindings.http_client.get(
                Endpoints.LIST_INTEGRATION_INSTANCES.format(INTEGRATION_NAME="Gmail")
            )
            instances = instance_response.get("integration_instances", [])
        except Exception as e:
            # Log error appropriately in real code
            print(f"Error fetching instance for Gmail: {e}")
            return {"Status": "Failed", "Message": f"Error fetching instance: {e}"}
    
        if instances:
            instance_identifier = instances[0].get("identifier")
            if not instance_identifier:
                # Log error or handle missing identifier
                return {"Status": "Failed", "Message": "Instance found but identifier is missing."}
    
            # Construct parameters dictionary for the API call
            script_params = {}
            script_params["Mailbox"] = mailbox
            script_params["Internet Message ID"] = internet_message_id
            if reply_to is not None:
                script_params["Reply To"] = reply_to
            if reply_all is not None:
                script_params["Reply All"] = reply_all
            if attachments_paths is not None:
                script_params["Attachments Paths"] = attachments_paths
            mail_content = mail_content.model_dump()
            script_params["Mail Content"] = mail_content
    
            # Prepare data model for the API request
            action_data = ApiManualActionDataModel(
                alertGroupIdentifiers=alert_group_identifiers,
                caseId=case_id,
                targetEntities=final_target_entities,
                scope=final_scope,
                isPredefinedScope=is_predefined_scope, # Pass the is_predefined_scope parameter
                actionProvider="Scripts", # Assuming constant based on example
                actionName="Gmail_Send Thread Reply",
                properties={
                    "IntegrationInstance": instance_identifier,
                    "ScriptName": "Gmail_Send Thread Reply", # Assuming same as actionName
                    "ScriptParametersEntityFields": json.dumps(script_params)
                }
            )
    
            # Execute the action via HTTP POST
            try:
                execution_response = await bindings.http_client.post(
                    Endpoints.EXECUTE_MANUAL_ACTION,
                    req=action_data.model_dump()
                )
                return execution_response
            except Exception as e:
                # Log error appropriately
                print(f"Error executing action Gmail_Send Thread Reply for Gmail: {e}")
                return {"Status": "Failed", "Message": f"Error executing action: {e}"}
        else:
            print(f"Warning: No active integration instance found for Gmail")
            return {"Status": "Failed", "Message": "No active instance found."}

    @mcp.tool()
    async def gmail_add_email_label(case_id: Annotated[str, Field(..., description="The ID of the case.")], alert_group_identifiers: Annotated[List[str], Field(..., description="Identifiers for the alert groups.")], mailbox: Annotated[str, Field(..., description="A mailbox to search the email in, such as user@example.com. By default, the action uses the default mailbox that you configured for the integration.")], label: Annotated[str, Field(..., description="A label to update the email with. This parameter accepts multiple values as a comma-separated list. Action will create labels, if they don\u2019t exist in the mailbox.")], labels_filter: Annotated[Optional[str], Field(default=None, description="A filter condition that specifies the email labels to search for. This parameter accepts multiple values as a comma-separated string. You can search for emails with specific labels, such as label1, label2. To search for emails that don\u2019t possess the specific label, use the following format: -label1. You can configure this parameter to search for emails with and without specific labels in one string, such as label1, -label2, label3.")], internet_message_id: Annotated[Optional[str], Field(default=None, description="An internet message ID of the email to search for. This parameter accepts multiple values as a comma-separated string. If you provide the internet message ID, the action ignores the Labels Filter, Subject Filter, Sender Filter, and Time Frame (minutes) parameters.")], subject_filter: Annotated[Optional[str], Field(default=None, description="A filter condition that specifies the email subject to search for. This filter uses the \u201ccontains\u201d logic and requires you to specify search items in full words. This filter doesn\u2019t support partial matches.")], sender_filter: Annotated[Optional[str], Field(default=None, description="A filter condition that specifies the email sender to search for. This filter uses the \u201cequals\u201d logic.")], time_frame_minutes: Annotated[Optional[str], Field(default=None, description="A filter condition that specifies the timeframe in minutes to search for emails.")], email_status: Annotated[Optional[List[Any]], Field(default=None, description="A status of the email to search for.")], target_entities: Annotated[List[TargetEntity], Field(default_factory=list, description="Optional list of specific target entities (Identifier, EntityType) to run the action on.")], scope: Annotated[str, Field(default="All entities", description="Defines the scope for the action.")]) -> dict:
        """Use the Add Email Label action to add a label to the specified email. Adjust the action timeout in the Google SecOps IDE accordingly. This action doesn't run on Google SecOps entities.

        Returns:
            dict: A dictionary containing the result of the action execution.
        """
        # --- Determine scope and target entities for API call ---
        final_target_entities: Optional[List[TargetEntity]] = None
        final_scope: Optional[str] = None
        is_predefined_scope: Optional[bool] = None
    
        if target_entities:
            # Specific target entities provided, ignore scope parameter
            final_target_entities = target_entities
            final_scope = None # Scope is ignored when specific entities are given
            is_predefined_scope = False
        else:
            # No specific target entities, use scope parameter
            # Check if the provided scope is valid
            if scope not in bindings.valid_scopes:
                allowed_values_str = ", ".join(sorted(list(bindings.valid_scopes)))
                return {
                    "Status": "Failed",
                    "Message": f"Invalid scope '{scope}'. Allowed values are: {allowed_values_str}",
                }
            # Scope is valid or validation is not configured
            final_target_entities = [] # Pass empty list for entities when using scope
            final_scope = scope
            is_predefined_scope = True
        # --- End scope/entity logic ---
    
        # Fetch integration instance identifier (assuming this pattern)
        try:
            instance_response = await bindings.http_client.get(
                Endpoints.LIST_INTEGRATION_INSTANCES.format(INTEGRATION_NAME="Gmail")
            )
            instances = instance_response.get("integration_instances", [])
        except Exception as e:
            # Log error appropriately in real code
            print(f"Error fetching instance for Gmail: {e}")
            return {"Status": "Failed", "Message": f"Error fetching instance: {e}"}
    
        if instances:
            instance_identifier = instances[0].get("identifier")
            if not instance_identifier:
                # Log error or handle missing identifier
                return {"Status": "Failed", "Message": "Instance found but identifier is missing."}
    
            # Construct parameters dictionary for the API call
            script_params = {}
            script_params["Mailbox"] = mailbox
            if labels_filter is not None:
                script_params["Labels Filter"] = labels_filter
            if internet_message_id is not None:
                script_params["Internet Message ID"] = internet_message_id
            if subject_filter is not None:
                script_params["Subject Filter"] = subject_filter
            if sender_filter is not None:
                script_params["Sender Filter"] = sender_filter
            if time_frame_minutes is not None:
                script_params["Time Frame (minutes)"] = time_frame_minutes
            if email_status is not None:
                script_params["Email Status"] = email_status
            script_params["Label"] = label
    
            # Prepare data model for the API request
            action_data = ApiManualActionDataModel(
                alertGroupIdentifiers=alert_group_identifiers,
                caseId=case_id,
                targetEntities=final_target_entities,
                scope=final_scope,
                isPredefinedScope=is_predefined_scope, # Pass the is_predefined_scope parameter
                actionProvider="Scripts", # Assuming constant based on example
                actionName="Gmail_Add Email Label",
                properties={
                    "IntegrationInstance": instance_identifier,
                    "ScriptName": "Gmail_Add Email Label", # Assuming same as actionName
                    "ScriptParametersEntityFields": json.dumps(script_params)
                }
            )
    
            # Execute the action via HTTP POST
            try:
                execution_response = await bindings.http_client.post(
                    Endpoints.EXECUTE_MANUAL_ACTION,
                    req=action_data.model_dump()
                )
                return execution_response
            except Exception as e:
                # Log error appropriately
                print(f"Error executing action Gmail_Add Email Label for Gmail: {e}")
                return {"Status": "Failed", "Message": f"Error executing action: {e}"}
        else:
            print(f"Warning: No active integration instance found for Gmail")
            return {"Status": "Failed", "Message": "No active instance found."}

    @mcp.tool()
    async def gmail_forward_email(case_id: Annotated[str, Field(..., description="The ID of the case.")], alert_group_identifiers: Annotated[List[str], Field(..., description="Identifiers for the alert groups.")], mailbox: Annotated[str, Field(..., description="A mailbox to search the email in, such as user@example.com. By default, the action uses the default mailbox that you configured for the integration.")], internet_message_id: Annotated[str, Field(..., description="An internet message ID of the email to search for.")], send_to: Annotated[str, Field(..., description="A comma-separated list of email addresses for the email recipients, such as user1@example.com, user2@example.com.")], subject: Annotated[str, Field(..., description="A new subject for the email to forward.")], mail_content: Annotated[EmailContent, Field(..., description="The body of an email.")], cc: Annotated[Optional[str], Field(default=None, description="A comma-separated string of email addresses for the carbon copy (CC) email recipients, such as user1@example.com, user2@example.com.")], bcc: Annotated[Optional[str], Field(default=None, description="A comma-separated string of email addresses for the blind carbon copy (BCC) email recipients, such as user1@example.com, user2@example.com.")], attachments_paths: Annotated[Optional[str], Field(default=None, description="A comma-separated string of paths for file attachments stored on the Google SecOps server.")], target_entities: Annotated[List[TargetEntity], Field(default_factory=list, description="Optional list of specific target entities (Identifier, EntityType) to run the action on.")], scope: Annotated[str, Field(default="All entities", description="Defines the scope for the action.")]) -> dict:
        """Use the Forward Email action to forward emails, including emails with previous threads. This action doesn’t run on Google SecOps entities

        Returns:
            dict: A dictionary containing the result of the action execution.
        """
        # --- Determine scope and target entities for API call ---
        final_target_entities: Optional[List[TargetEntity]] = None
        final_scope: Optional[str] = None
        is_predefined_scope: Optional[bool] = None
    
        if target_entities:
            # Specific target entities provided, ignore scope parameter
            final_target_entities = target_entities
            final_scope = None # Scope is ignored when specific entities are given
            is_predefined_scope = False
        else:
            # No specific target entities, use scope parameter
            # Check if the provided scope is valid
            if scope not in bindings.valid_scopes:
                allowed_values_str = ", ".join(sorted(list(bindings.valid_scopes)))
                return {
                    "Status": "Failed",
                    "Message": f"Invalid scope '{scope}'. Allowed values are: {allowed_values_str}",
                }
            # Scope is valid or validation is not configured
            final_target_entities = [] # Pass empty list for entities when using scope
            final_scope = scope
            is_predefined_scope = True
        # --- End scope/entity logic ---
    
        # Fetch integration instance identifier (assuming this pattern)
        try:
            instance_response = await bindings.http_client.get(
                Endpoints.LIST_INTEGRATION_INSTANCES.format(INTEGRATION_NAME="Gmail")
            )
            instances = instance_response.get("integration_instances", [])
        except Exception as e:
            # Log error appropriately in real code
            print(f"Error fetching instance for Gmail: {e}")
            return {"Status": "Failed", "Message": f"Error fetching instance: {e}"}
    
        if instances:
            instance_identifier = instances[0].get("identifier")
            if not instance_identifier:
                # Log error or handle missing identifier
                return {"Status": "Failed", "Message": "Instance found but identifier is missing."}
    
            # Construct parameters dictionary for the API call
            script_params = {}
            script_params["Mailbox"] = mailbox
            script_params["Internet Message ID"] = internet_message_id
            script_params["Send To"] = send_to
            if cc is not None:
                script_params["CC"] = cc
            if bcc is not None:
                script_params["BCC"] = bcc
            script_params["Subject"] = subject
            if attachments_paths is not None:
                script_params["Attachments Paths"] = attachments_paths
            mail_content = mail_content.model_dump()
            script_params["Mail Content"] = mail_content
    
            # Prepare data model for the API request
            action_data = ApiManualActionDataModel(
                alertGroupIdentifiers=alert_group_identifiers,
                caseId=case_id,
                targetEntities=final_target_entities,
                scope=final_scope,
                isPredefinedScope=is_predefined_scope, # Pass the is_predefined_scope parameter
                actionProvider="Scripts", # Assuming constant based on example
                actionName="Gmail_Forward Email",
                properties={
                    "IntegrationInstance": instance_identifier,
                    "ScriptName": "Gmail_Forward Email", # Assuming same as actionName
                    "ScriptParametersEntityFields": json.dumps(script_params)
                }
            )
    
            # Execute the action via HTTP POST
            try:
                execution_response = await bindings.http_client.post(
                    Endpoints.EXECUTE_MANUAL_ACTION,
                    req=action_data.model_dump()
                )
                return execution_response
            except Exception as e:
                # Log error appropriately
                print(f"Error executing action Gmail_Forward Email for Gmail: {e}")
                return {"Status": "Failed", "Message": f"Error executing action: {e}"}
        else:
            print(f"Warning: No active integration instance found for Gmail")
            return {"Status": "Failed", "Message": "No active instance found."}

    @mcp.tool()
    async def gmail_search_for_emails(case_id: Annotated[str, Field(..., description="The ID of the case.")], alert_group_identifiers: Annotated[List[str], Field(..., description="Identifiers for the alert groups.")], mailbox: Annotated[str, Field(..., description="A mailbox to search the email in, such as user@example.com. By default, the action uses the default mailbox that you configured for the integration. This parameter accepts multiple values as a comma-separated string.")], labels_filter: Annotated[Optional[str], Field(default=None, description="A filter condition that specifies the email labels to search for. This parameter accepts multiple values as a comma-separated string. You can search for emails with specific labels, such as label1, label2. To search for emails that don\u2019t possess the specific label, use the following format: -label1. You can configure this parameter to search for emails with and without specific labels in one string, such as label1, -label2, label3.")], internet_message_id: Annotated[Optional[str], Field(default=None, description="An internet message ID of the email to search for. This parameter accepts multiple values as a comma-separated string. If you provide the internet message ID, the action ignores the Subject Filter, Sender Filter, Labels Filter, Recipient Filter, Time Frame (minutes), and Email Status parameters.")], subject_filter: Annotated[Optional[str], Field(default=None, description="A filter condition that specifies the email subject to search for.")], sender_filter: Annotated[Optional[str], Field(default=None, description="A filter condition that specifies the email sender to search for.")], recipient_filter: Annotated[Optional[str], Field(default=None, description="A filter condition that specifies the email recipient to search for.")], time_frame_minutes: Annotated[Optional[str], Field(default=None, description="A filter condition that specifies the timeframe in minutes to search for emails.")], email_status: Annotated[Optional[List[Any]], Field(default=None, description="A status of the email to search for.")], headers_to_return: Annotated[Optional[str], Field(default=None, description="A comma-separated list of headers to return in the action output. The action always returns the following headers: date, from, to, cc, bcc, in-reply-to, reply-to, message-id and subject headers. If you don\u2019t provide any value, the action returns all headers.This parameter is case sensitive.")], return_email_body: Annotated[Optional[bool], Field(default=None, description="If selected, the action returns the full body content of an email in the action output. If not selected, the information about the attachment names in the email is unavailable")], max_emails_to_return: Annotated[Optional[str], Field(default=None, description="The maximum number of emails for the action to return.")], target_entities: Annotated[List[TargetEntity], Field(default_factory=list, description="Optional list of specific target entities (Identifier, EntityType) to run the action on.")], scope: Annotated[str, Field(default="All entities", description="Defines the scope for the action.")]) -> dict:
        """Use the Search for Emails action to execute email search in a specified mailbox using the provided search criteria. With appropriate permissions, this action can run a search in other mailboxes. This action is asynchronous. Adjust the action timeout in the Google SecOps IDE accordingly. This action doesn't run on Google SecOps entities.

        Returns:
            dict: A dictionary containing the result of the action execution.
        """
        # --- Determine scope and target entities for API call ---
        final_target_entities: Optional[List[TargetEntity]] = None
        final_scope: Optional[str] = None
        is_predefined_scope: Optional[bool] = None
    
        if target_entities:
            # Specific target entities provided, ignore scope parameter
            final_target_entities = target_entities
            final_scope = None # Scope is ignored when specific entities are given
            is_predefined_scope = False
        else:
            # No specific target entities, use scope parameter
            # Check if the provided scope is valid
            if scope not in bindings.valid_scopes:
                allowed_values_str = ", ".join(sorted(list(bindings.valid_scopes)))
                return {
                    "Status": "Failed",
                    "Message": f"Invalid scope '{scope}'. Allowed values are: {allowed_values_str}",
                }
            # Scope is valid or validation is not configured
            final_target_entities = [] # Pass empty list for entities when using scope
            final_scope = scope
            is_predefined_scope = True
        # --- End scope/entity logic ---
    
        # Fetch integration instance identifier (assuming this pattern)
        try:
            instance_response = await bindings.http_client.get(
                Endpoints.LIST_INTEGRATION_INSTANCES.format(INTEGRATION_NAME="Gmail")
            )
            instances = instance_response.get("integration_instances", [])
        except Exception as e:
            # Log error appropriately in real code
            print(f"Error fetching instance for Gmail: {e}")
            return {"Status": "Failed", "Message": f"Error fetching instance: {e}"}
    
        if instances:
            instance_identifier = instances[0].get("identifier")
            if not instance_identifier:
                # Log error or handle missing identifier
                return {"Status": "Failed", "Message": "Instance found but identifier is missing."}
    
            # Construct parameters dictionary for the API call
            script_params = {}
            script_params["Mailbox"] = mailbox
            if labels_filter is not None:
                script_params["Labels Filter"] = labels_filter
            if internet_message_id is not None:
                script_params["Internet Message ID"] = internet_message_id
            if subject_filter is not None:
                script_params["Subject Filter"] = subject_filter
            if sender_filter is not None:
                script_params["Sender Filter"] = sender_filter
            if recipient_filter is not None:
                script_params["Recipient Filter"] = recipient_filter
            if time_frame_minutes is not None:
                script_params["Time Frame (minutes)"] = time_frame_minutes
            if email_status is not None:
                script_params["Email Status"] = email_status
            if headers_to_return is not None:
                script_params["Headers To Return"] = headers_to_return
            if return_email_body is not None:
                script_params["Return Email Body"] = return_email_body
            if max_emails_to_return is not None:
                script_params["Max Emails To Return"] = max_emails_to_return
    
            # Prepare data model for the API request
            action_data = ApiManualActionDataModel(
                alertGroupIdentifiers=alert_group_identifiers,
                caseId=case_id,
                targetEntities=final_target_entities,
                scope=final_scope,
                isPredefinedScope=is_predefined_scope, # Pass the is_predefined_scope parameter
                actionProvider="Scripts", # Assuming constant based on example
                actionName="Gmail_Search For Emails",
                properties={
                    "IntegrationInstance": instance_identifier,
                    "ScriptName": "Gmail_Search For Emails", # Assuming same as actionName
                    "ScriptParametersEntityFields": json.dumps(script_params)
                }
            )
    
            # Execute the action via HTTP POST
            try:
                execution_response = await bindings.http_client.post(
                    Endpoints.EXECUTE_MANUAL_ACTION,
                    req=action_data.model_dump()
                )
                return execution_response
            except Exception as e:
                # Log error appropriately
                print(f"Error executing action Gmail_Search For Emails for Gmail: {e}")
                return {"Status": "Failed", "Message": f"Error executing action: {e}"}
        else:
            print(f"Warning: No active integration instance found for Gmail")
            return {"Status": "Failed", "Message": "No active instance found."}

    @mcp.tool()
    async def gmail_wait_for_thread_reply(case_id: Annotated[str, Field(..., description="The ID of the case.")], alert_group_identifiers: Annotated[List[str], Field(..., description="Identifiers for the alert groups.")], mailbox: Annotated[str, Field(..., description="A mailbox to wait for a reply in, such as user@example.com. By default, the action uses the default mailbox that you configured for the integration.")], internet_message_id: Annotated[str, Field(..., description="The internet message ID of an email for the action to wait for. If the message was sent using the Send Email action, configure this parameter using the following placeholder: SendEmail.JSONResult|message_id. To retrieve an internet message ID, use the Search for Emails action.")], wait_for_all_recipients_to_reply: Annotated[Optional[bool], Field(default=None, description="If selected, the action waits for responses from all recipients until reaching timeout. Not selected by default.")], fetch_response_attachments: Annotated[Optional[bool], Field(default=None, description="If selected and the recipient reply contains attachments, the action retrieves email attachments and adds them as an attachment to the Case Wall in Google SecOps. Not selected by default.")], target_entities: Annotated[List[TargetEntity], Field(default_factory=list, description="Optional list of specific target entities (Identifier, EntityType) to run the action on.")], scope: Annotated[str, Field(default="All entities", description="Defines the scope for the action.")]) -> dict:
        """Use the Wait For Thread Reply action to wait for the user's reply based on an email sent using the Send Email action. This action is asynchronous. Adjust the action timeout in the Google SecOps IDE accordingly. This action doesn't run on Google SecOps entities.

        Returns:
            dict: A dictionary containing the result of the action execution.
        """
        # --- Determine scope and target entities for API call ---
        final_target_entities: Optional[List[TargetEntity]] = None
        final_scope: Optional[str] = None
        is_predefined_scope: Optional[bool] = None
    
        if target_entities:
            # Specific target entities provided, ignore scope parameter
            final_target_entities = target_entities
            final_scope = None # Scope is ignored when specific entities are given
            is_predefined_scope = False
        else:
            # No specific target entities, use scope parameter
            # Check if the provided scope is valid
            if scope not in bindings.valid_scopes:
                allowed_values_str = ", ".join(sorted(list(bindings.valid_scopes)))
                return {
                    "Status": "Failed",
                    "Message": f"Invalid scope '{scope}'. Allowed values are: {allowed_values_str}",
                }
            # Scope is valid or validation is not configured
            final_target_entities = [] # Pass empty list for entities when using scope
            final_scope = scope
            is_predefined_scope = True
        # --- End scope/entity logic ---
    
        # Fetch integration instance identifier (assuming this pattern)
        try:
            instance_response = await bindings.http_client.get(
                Endpoints.LIST_INTEGRATION_INSTANCES.format(INTEGRATION_NAME="Gmail")
            )
            instances = instance_response.get("integration_instances", [])
        except Exception as e:
            # Log error appropriately in real code
            print(f"Error fetching instance for Gmail: {e}")
            return {"Status": "Failed", "Message": f"Error fetching instance: {e}"}
    
        if instances:
            instance_identifier = instances[0].get("identifier")
            if not instance_identifier:
                # Log error or handle missing identifier
                return {"Status": "Failed", "Message": "Instance found but identifier is missing."}
    
            # Construct parameters dictionary for the API call
            script_params = {}
            script_params["Mailbox"] = mailbox
            script_params["Internet Message ID"] = internet_message_id
            if wait_for_all_recipients_to_reply is not None:
                script_params["Wait for All Recipients to Reply"] = wait_for_all_recipients_to_reply
            if fetch_response_attachments is not None:
                script_params["Fetch Response Attachments"] = fetch_response_attachments
    
            # Prepare data model for the API request
            action_data = ApiManualActionDataModel(
                alertGroupIdentifiers=alert_group_identifiers,
                caseId=case_id,
                targetEntities=final_target_entities,
                scope=final_scope,
                isPredefinedScope=is_predefined_scope, # Pass the is_predefined_scope parameter
                actionProvider="Scripts", # Assuming constant based on example
                actionName="Gmail_Wait For Thread Reply",
                properties={
                    "IntegrationInstance": instance_identifier,
                    "ScriptName": "Gmail_Wait For Thread Reply", # Assuming same as actionName
                    "ScriptParametersEntityFields": json.dumps(script_params)
                }
            )
    
            # Execute the action via HTTP POST
            try:
                execution_response = await bindings.http_client.post(
                    Endpoints.EXECUTE_MANUAL_ACTION,
                    req=action_data.model_dump()
                )
                return execution_response
            except Exception as e:
                # Log error appropriately
                print(f"Error executing action Gmail_Wait For Thread Reply for Gmail: {e}")
                return {"Status": "Failed", "Message": f"Error executing action: {e}"}
        else:
            print(f"Warning: No active integration instance found for Gmail")
            return {"Status": "Failed", "Message": "No active instance found."}

    @mcp.tool()
    async def gmail_remove_email_label(case_id: Annotated[str, Field(..., description="The ID of the case.")], alert_group_identifiers: Annotated[List[str], Field(..., description="Identifiers for the alert groups.")], mailbox: Annotated[str, Field(..., description="A mailbox to search the email in, such as user@example.com. By default, the action uses the default mailbox that you configured for the integration.")], label: Annotated[str, Field(..., description="A label to remove from an email. This parameter accepts multiple values as a comma-separated list.")], labels_filter: Annotated[Optional[str], Field(default=None, description="A filter condition that specifies the email labels to search for. This parameter accepts multiple values as a comma-separated string. You can search for emails with specific labels, such as label1, label2. To search for emails that don\u2019t possess the specific label, use the following format: -label1. You can configure this parameter to search for emails with and without specific labels in one string, such as label1, -label2, label3.")], internet_message_id: Annotated[Optional[str], Field(default=None, description="An internet message ID of the email to search for. This parameter accepts multiple values as a comma-separated string. If you provide the internet message ID, the action ignores the Labels Filter, Subject Filter, Sender Filter, and Time Frame (minutes) parameters.")], subject_filter: Annotated[Optional[str], Field(default=None, description="A filter condition that specifies the email subject to search for. This filter uses the \u201ccontains\u201d logic and requires you to specify search items in full words. This filter doesn\u2019t support partial matches.")], sender_filter: Annotated[Optional[str], Field(default=None, description="A filter condition that specifies the email sender to search for. This filter uses the \u201cequals\u201d logic.")], time_frame_minutes: Annotated[Optional[str], Field(default=None, description="A filter condition that specifies the timeframe in minutes to search for emails.")], email_status: Annotated[Optional[List[Any]], Field(default=None, description="A status of the email to search for.")], target_entities: Annotated[List[TargetEntity], Field(default_factory=list, description="Optional list of specific target entities (Identifier, EntityType) to run the action on.")], scope: Annotated[str, Field(default="All entities", description="Defines the scope for the action.")]) -> dict:
        """Use the Remove Email Label action to remove a label from the specified email. Adjust the action timeout in the Google SecOps IDE accordingly. This action doesn't run on Google SecOps entities.

        Returns:
            dict: A dictionary containing the result of the action execution.
        """
        # --- Determine scope and target entities for API call ---
        final_target_entities: Optional[List[TargetEntity]] = None
        final_scope: Optional[str] = None
        is_predefined_scope: Optional[bool] = None
    
        if target_entities:
            # Specific target entities provided, ignore scope parameter
            final_target_entities = target_entities
            final_scope = None # Scope is ignored when specific entities are given
            is_predefined_scope = False
        else:
            # No specific target entities, use scope parameter
            # Check if the provided scope is valid
            if scope not in bindings.valid_scopes:
                allowed_values_str = ", ".join(sorted(list(bindings.valid_scopes)))
                return {
                    "Status": "Failed",
                    "Message": f"Invalid scope '{scope}'. Allowed values are: {allowed_values_str}",
                }
            # Scope is valid or validation is not configured
            final_target_entities = [] # Pass empty list for entities when using scope
            final_scope = scope
            is_predefined_scope = True
        # --- End scope/entity logic ---
    
        # Fetch integration instance identifier (assuming this pattern)
        try:
            instance_response = await bindings.http_client.get(
                Endpoints.LIST_INTEGRATION_INSTANCES.format(INTEGRATION_NAME="Gmail")
            )
            instances = instance_response.get("integration_instances", [])
        except Exception as e:
            # Log error appropriately in real code
            print(f"Error fetching instance for Gmail: {e}")
            return {"Status": "Failed", "Message": f"Error fetching instance: {e}"}
    
        if instances:
            instance_identifier = instances[0].get("identifier")
            if not instance_identifier:
                # Log error or handle missing identifier
                return {"Status": "Failed", "Message": "Instance found but identifier is missing."}
    
            # Construct parameters dictionary for the API call
            script_params = {}
            script_params["Mailbox"] = mailbox
            if labels_filter is not None:
                script_params["Labels Filter"] = labels_filter
            if internet_message_id is not None:
                script_params["Internet Message ID"] = internet_message_id
            if subject_filter is not None:
                script_params["Subject Filter"] = subject_filter
            if sender_filter is not None:
                script_params["Sender Filter"] = sender_filter
            if time_frame_minutes is not None:
                script_params["Time Frame (minutes)"] = time_frame_minutes
            if email_status is not None:
                script_params["Email Status"] = email_status
            script_params["Label"] = label
    
            # Prepare data model for the API request
            action_data = ApiManualActionDataModel(
                alertGroupIdentifiers=alert_group_identifiers,
                caseId=case_id,
                targetEntities=final_target_entities,
                scope=final_scope,
                isPredefinedScope=is_predefined_scope, # Pass the is_predefined_scope parameter
                actionProvider="Scripts", # Assuming constant based on example
                actionName="Gmail_Remove Email Label",
                properties={
                    "IntegrationInstance": instance_identifier,
                    "ScriptName": "Gmail_Remove Email Label", # Assuming same as actionName
                    "ScriptParametersEntityFields": json.dumps(script_params)
                }
            )
    
            # Execute the action via HTTP POST
            try:
                execution_response = await bindings.http_client.post(
                    Endpoints.EXECUTE_MANUAL_ACTION,
                    req=action_data.model_dump()
                )
                return execution_response
            except Exception as e:
                # Log error appropriately
                print(f"Error executing action Gmail_Remove Email Label for Gmail: {e}")
                return {"Status": "Failed", "Message": f"Error executing action: {e}"}
        else:
            print(f"Warning: No active integration instance found for Gmail")
            return {"Status": "Failed", "Message": "No active instance found."}

    @mcp.tool()
    async def gmail_ping(case_id: Annotated[str, Field(..., description="The ID of the case.")], alert_group_identifiers: Annotated[List[str], Field(..., description="Identifiers for the alert groups.")], target_entities: Annotated[List[TargetEntity], Field(default_factory=list, description="Optional list of specific target entities (Identifier, EntityType) to run the action on.")], scope: Annotated[str, Field(default="All entities", description="Defines the scope for the action.")]) -> dict:
        """Use the Ping action to test connectivity to Gmail.

        Returns:
            dict: A dictionary containing the result of the action execution.
        """
        # --- Determine scope and target entities for API call ---
        final_target_entities: Optional[List[TargetEntity]] = None
        final_scope: Optional[str] = None
        is_predefined_scope: Optional[bool] = None
    
        if target_entities:
            # Specific target entities provided, ignore scope parameter
            final_target_entities = target_entities
            final_scope = None # Scope is ignored when specific entities are given
            is_predefined_scope = False
        else:
            # No specific target entities, use scope parameter
            # Check if the provided scope is valid
            if scope not in bindings.valid_scopes:
                allowed_values_str = ", ".join(sorted(list(bindings.valid_scopes)))
                return {
                    "Status": "Failed",
                    "Message": f"Invalid scope '{scope}'. Allowed values are: {allowed_values_str}",
                }
            # Scope is valid or validation is not configured
            final_target_entities = [] # Pass empty list for entities when using scope
            final_scope = scope
            is_predefined_scope = True
        # --- End scope/entity logic ---
    
        # Fetch integration instance identifier (assuming this pattern)
        try:
            instance_response = await bindings.http_client.get(
                Endpoints.LIST_INTEGRATION_INSTANCES.format(INTEGRATION_NAME="Gmail")
            )
            instances = instance_response.get("integration_instances", [])
        except Exception as e:
            # Log error appropriately in real code
            print(f"Error fetching instance for Gmail: {e}")
            return {"Status": "Failed", "Message": f"Error fetching instance: {e}"}
    
        if instances:
            instance_identifier = instances[0].get("identifier")
            if not instance_identifier:
                # Log error or handle missing identifier
                return {"Status": "Failed", "Message": "Instance found but identifier is missing."}
    
            # Construct parameters dictionary for the API call
            script_params = {}
    
            # Prepare data model for the API request
            action_data = ApiManualActionDataModel(
                alertGroupIdentifiers=alert_group_identifiers,
                caseId=case_id,
                targetEntities=final_target_entities,
                scope=final_scope,
                isPredefinedScope=is_predefined_scope, # Pass the is_predefined_scope parameter
                actionProvider="Scripts", # Assuming constant based on example
                actionName="Gmail_Ping",
                properties={
                    "IntegrationInstance": instance_identifier,
                    "ScriptName": "Gmail_Ping", # Assuming same as actionName
                    "ScriptParametersEntityFields": json.dumps(script_params)
                }
            )
    
            # Execute the action via HTTP POST
            try:
                execution_response = await bindings.http_client.post(
                    Endpoints.EXECUTE_MANUAL_ACTION,
                    req=action_data.model_dump()
                )
                return execution_response
            except Exception as e:
                # Log error appropriately
                print(f"Error executing action Gmail_Ping for Gmail: {e}")
                return {"Status": "Failed", "Message": f"Error executing action: {e}"}
        else:
            print(f"Warning: No active integration instance found for Gmail")
            return {"Status": "Failed", "Message": "No active instance found."}

    @mcp.tool()
    async def gmail_save_email_to_the_case(case_id: Annotated[str, Field(..., description="The ID of the case.")], alert_group_identifiers: Annotated[List[str], Field(..., description="Identifiers for the alert groups.")], mailbox: Annotated[str, Field(..., description="A mailbox to search the email in, such as user@example.com. By default, the action uses the default mailbox that you configured for the integration.")], internet_message_id: Annotated[str, Field(..., description="An internet message ID of the email to search for.")], save_only_email_attachments: Annotated[Optional[bool], Field(default=None, description="If selected, the action saves only attachments from the specified email. Not selected by default.")], attachment_to_save: Annotated[Optional[str], Field(default=None, description="If you selected the \u201cSave Only Email Attachments\u201d parameter, the action only saves attachments that this parameter specifies. This parameter accepts multiple values as a comma-separated string.")], base64_encode: Annotated[Optional[bool], Field(default=None, description="If selected, the action encodes the email file into a base64 format.")], target_entities: Annotated[List[TargetEntity], Field(default_factory=list, description="Optional list of specific target entities (Identifier, EntityType) to run the action on.")], scope: Annotated[str, Field(default="All entities", description="Defines the scope for the action.")]) -> dict:
        """Use the Save Email To The Case action to save email or email attachments to the action Case Wall in Google SecOps. This action doesn’t run on Google SecOps entities.

        Returns:
            dict: A dictionary containing the result of the action execution.
        """
        # --- Determine scope and target entities for API call ---
        final_target_entities: Optional[List[TargetEntity]] = None
        final_scope: Optional[str] = None
        is_predefined_scope: Optional[bool] = None
    
        if target_entities:
            # Specific target entities provided, ignore scope parameter
            final_target_entities = target_entities
            final_scope = None # Scope is ignored when specific entities are given
            is_predefined_scope = False
        else:
            # No specific target entities, use scope parameter
            # Check if the provided scope is valid
            if scope not in bindings.valid_scopes:
                allowed_values_str = ", ".join(sorted(list(bindings.valid_scopes)))
                return {
                    "Status": "Failed",
                    "Message": f"Invalid scope '{scope}'. Allowed values are: {allowed_values_str}",
                }
            # Scope is valid or validation is not configured
            final_target_entities = [] # Pass empty list for entities when using scope
            final_scope = scope
            is_predefined_scope = True
        # --- End scope/entity logic ---
    
        # Fetch integration instance identifier (assuming this pattern)
        try:
            instance_response = await bindings.http_client.get(
                Endpoints.LIST_INTEGRATION_INSTANCES.format(INTEGRATION_NAME="Gmail")
            )
            instances = instance_response.get("integration_instances", [])
        except Exception as e:
            # Log error appropriately in real code
            print(f"Error fetching instance for Gmail: {e}")
            return {"Status": "Failed", "Message": f"Error fetching instance: {e}"}
    
        if instances:
            instance_identifier = instances[0].get("identifier")
            if not instance_identifier:
                # Log error or handle missing identifier
                return {"Status": "Failed", "Message": "Instance found but identifier is missing."}
    
            # Construct parameters dictionary for the API call
            script_params = {}
            script_params["Mailbox"] = mailbox
            script_params["Internet Message ID"] = internet_message_id
            if save_only_email_attachments is not None:
                script_params["Save Only Email Attachments"] = save_only_email_attachments
            if attachment_to_save is not None:
                script_params["Attachment To Save"] = attachment_to_save
            if base64_encode is not None:
                script_params["Base64 Encode"] = base64_encode
    
            # Prepare data model for the API request
            action_data = ApiManualActionDataModel(
                alertGroupIdentifiers=alert_group_identifiers,
                caseId=case_id,
                targetEntities=final_target_entities,
                scope=final_scope,
                isPredefinedScope=is_predefined_scope, # Pass the is_predefined_scope parameter
                actionProvider="Scripts", # Assuming constant based on example
                actionName="Gmail_Save Email To The Case",
                properties={
                    "IntegrationInstance": instance_identifier,
                    "ScriptName": "Gmail_Save Email To The Case", # Assuming same as actionName
                    "ScriptParametersEntityFields": json.dumps(script_params)
                }
            )
    
            # Execute the action via HTTP POST
            try:
                execution_response = await bindings.http_client.post(
                    Endpoints.EXECUTE_MANUAL_ACTION,
                    req=action_data.model_dump()
                )
                return execution_response
            except Exception as e:
                # Log error appropriately
                print(f"Error executing action Gmail_Save Email To The Case for Gmail: {e}")
                return {"Status": "Failed", "Message": f"Error executing action: {e}"}
        else:
            print(f"Warning: No active integration instance found for Gmail")
            return {"Status": "Failed", "Message": "No active instance found."}

    @mcp.tool()
    async def gmail_send_email(case_id: Annotated[str, Field(..., description="The ID of the case.")], alert_group_identifiers: Annotated[List[str], Field(..., description="Identifiers for the alert groups.")], mailbox: Annotated[str, Field(..., description="A mailbox to send an email from, such as user@example.com. By default, the action uses the default mailbox that you configured for the integration.")], subject: Annotated[str, Field(..., description="The subject for an email to send.")], send_to: Annotated[str, Field(..., description="A comma-separated string of email addresses for the email recipients, such as user1@example.com, user2@example.com.")], mail_content: Annotated[EmailContent, Field(..., description="The body of an email.")], cc: Annotated[Optional[str], Field(default=None, description="A comma-separated string of email addresses for the carbon copy (CC) email recipients, such as user1@example.com, user2@example.com.")], bcc: Annotated[Optional[str], Field(default=None, description="A comma-separated string of email addresses for the blind carbon copy (BCC) email recipients, such as user1@example.com, user2@example.com.")], attachments_paths: Annotated[Optional[str], Field(default=None, description="A comma-separated string of paths for file attachments stored on the Google SecOps server.")], reply_to_recipients: Annotated[Optional[str], Field(default=None, description="A comma-separated list of recipients to use in the \u201cReply-To\u201d header. Use the \u201cReply-To\u201d header to redirect reply emails to the specific email address instead of the sender address that is stated in the \u201cFrom\u201d field.")], target_entities: Annotated[List[TargetEntity], Field(default_factory=list, description="Optional list of specific target entities (Identifier, EntityType) to run the action on.")], scope: Annotated[str, Field(default="All entities", description="Defines the scope for the action.")]) -> dict:
        """Use the Send Email action to send an email based on the provided parameters. This action is not running on Google SecOps entities.

        Returns:
            dict: A dictionary containing the result of the action execution.
        """
        # --- Determine scope and target entities for API call ---
        final_target_entities: Optional[List[TargetEntity]] = None
        final_scope: Optional[str] = None
        is_predefined_scope: Optional[bool] = None
    
        if target_entities:
            # Specific target entities provided, ignore scope parameter
            final_target_entities = target_entities
            final_scope = None # Scope is ignored when specific entities are given
            is_predefined_scope = False
        else:
            # No specific target entities, use scope parameter
            # Check if the provided scope is valid
            if scope not in bindings.valid_scopes:
                allowed_values_str = ", ".join(sorted(list(bindings.valid_scopes)))
                return {
                    "Status": "Failed",
                    "Message": f"Invalid scope '{scope}'. Allowed values are: {allowed_values_str}",
                }
            # Scope is valid or validation is not configured
            final_target_entities = [] # Pass empty list for entities when using scope
            final_scope = scope
            is_predefined_scope = True
        # --- End scope/entity logic ---
    
        # Fetch integration instance identifier (assuming this pattern)
        try:
            instance_response = await bindings.http_client.get(
                Endpoints.LIST_INTEGRATION_INSTANCES.format(INTEGRATION_NAME="Gmail")
            )
            instances = instance_response.get("integration_instances", [])
        except Exception as e:
            # Log error appropriately in real code
            print(f"Error fetching instance for Gmail: {e}")
            return {"Status": "Failed", "Message": f"Error fetching instance: {e}"}
    
        if instances:
            instance_identifier = instances[0].get("identifier")
            if not instance_identifier:
                # Log error or handle missing identifier
                return {"Status": "Failed", "Message": "Instance found but identifier is missing."}
    
            # Construct parameters dictionary for the API call
            script_params = {}
            script_params["Mailbox"] = mailbox
            script_params["Subject"] = subject
            script_params["Send To"] = send_to
            if cc is not None:
                script_params["CC"] = cc
            if bcc is not None:
                script_params["BCC"] = bcc
            if attachments_paths is not None:
                script_params["Attachments Paths"] = attachments_paths
            mail_content = mail_content.model_dump()
            script_params["Mail Content"] = mail_content
            if reply_to_recipients is not None:
                script_params["Reply-To Recipients"] = reply_to_recipients
    
            # Prepare data model for the API request
            action_data = ApiManualActionDataModel(
                alertGroupIdentifiers=alert_group_identifiers,
                caseId=case_id,
                targetEntities=final_target_entities,
                scope=final_scope,
                isPredefinedScope=is_predefined_scope, # Pass the is_predefined_scope parameter
                actionProvider="Scripts", # Assuming constant based on example
                actionName="Gmail_Send Email",
                properties={
                    "IntegrationInstance": instance_identifier,
                    "ScriptName": "Gmail_Send Email", # Assuming same as actionName
                    "ScriptParametersEntityFields": json.dumps(script_params)
                }
            )
    
            # Execute the action via HTTP POST
            try:
                execution_response = await bindings.http_client.post(
                    Endpoints.EXECUTE_MANUAL_ACTION,
                    req=action_data.model_dump()
                )
                return execution_response
            except Exception as e:
                # Log error appropriately
                print(f"Error executing action Gmail_Send Email for Gmail: {e}")
                return {"Status": "Failed", "Message": f"Error executing action: {e}"}
        else:
            print(f"Warning: No active integration instance found for Gmail")
            return {"Status": "Failed", "Message": "No active instance found."}

    @mcp.tool()
    async def gmail_delete_email(case_id: Annotated[str, Field(..., description="The ID of the case.")], alert_group_identifiers: Annotated[List[str], Field(..., description="Identifiers for the alert groups.")], mailbox: Annotated[str, Field(..., description="A mailbox to search the email in, such as user@example.com. By default, the action uses the default mailbox that you configured for the integration. This parameter accepts multiple values as a comma-separated string.")], labels_filter: Annotated[Optional[str], Field(default=None, description="A filter condition that specifies the email labels to search for. This parameter accepts multiple values as a comma-separated string. You can search for emails with specific labels, such as label1, label2. To search for emails that don\u2019t possess the specific label, use the following format: -label1. You can configure this parameter to search for emails with and without specific labels in one string, such as label1, -label2, label3.")], internet_message_id: Annotated[Optional[str], Field(default=None, description="An internet message ID of the email to search for. This parameter accepts multiple values as a comma-separated string. If you provide the internet message ID, the action ignores the Subject Filter, Sender Filter, Labels Filter, and Time Frame (minutes) parameters.")], subject_filter: Annotated[Optional[str], Field(default=None, description="A filter condition that specifies the email subject to search for. This filter uses the \u201ccontains\u201d logic and requires you to specify search items in full words. This filter doesn\u2019t support partial matches.")], sender_filter: Annotated[Optional[str], Field(default=None, description="A filter condition that specifies the email sender to search for. This filter uses the \u201cequals\u201d logic.")], time_frame_minutes: Annotated[Optional[str], Field(default=None, description="A filter condition that specifies the timeframe in minutes to search for emails.")], email_status: Annotated[Optional[List[Any]], Field(default=None, description="A status of the email to search for.")], move_to_trash: Annotated[Optional[bool], Field(default=None, description="If selected, the action moves emails to Trash and doesn\u2019t search through emails with the Trash label unless you configure the Labels Filter parameter to include the following label: Trash. If not selected, the action executes search across the whole mailbox and deletes emails forever. Selected by default.")], target_entities: Annotated[List[TargetEntity], Field(default_factory=list, description="Optional list of specific target entities (Identifier, EntityType) to run the action on.")], scope: Annotated[str, Field(default="All entities", description="Defines the scope for the action.")]) -> dict:
        """Use the Delete Email action to delete one or multiple emails from the mailbox based on the provided search criteria. By default, this action moves emails to Trash. You can configure the action to delete emails forever instead of moving them to Trash. The Delete Email action is asynchronous. Adjust the action timeout in the Google SecOps IDE accordingly. This action doesn’t run on Google SecOps entities.

        Returns:
            dict: A dictionary containing the result of the action execution.
        """
        # --- Determine scope and target entities for API call ---
        final_target_entities: Optional[List[TargetEntity]] = None
        final_scope: Optional[str] = None
        is_predefined_scope: Optional[bool] = None
    
        if target_entities:
            # Specific target entities provided, ignore scope parameter
            final_target_entities = target_entities
            final_scope = None # Scope is ignored when specific entities are given
            is_predefined_scope = False
        else:
            # No specific target entities, use scope parameter
            # Check if the provided scope is valid
            if scope not in bindings.valid_scopes:
                allowed_values_str = ", ".join(sorted(list(bindings.valid_scopes)))
                return {
                    "Status": "Failed",
                    "Message": f"Invalid scope '{scope}'. Allowed values are: {allowed_values_str}",
                }
            # Scope is valid or validation is not configured
            final_target_entities = [] # Pass empty list for entities when using scope
            final_scope = scope
            is_predefined_scope = True
        # --- End scope/entity logic ---
    
        # Fetch integration instance identifier (assuming this pattern)
        try:
            instance_response = await bindings.http_client.get(
                Endpoints.LIST_INTEGRATION_INSTANCES.format(INTEGRATION_NAME="Gmail")
            )
            instances = instance_response.get("integration_instances", [])
        except Exception as e:
            # Log error appropriately in real code
            print(f"Error fetching instance for Gmail: {e}")
            return {"Status": "Failed", "Message": f"Error fetching instance: {e}"}
    
        if instances:
            instance_identifier = instances[0].get("identifier")
            if not instance_identifier:
                # Log error or handle missing identifier
                return {"Status": "Failed", "Message": "Instance found but identifier is missing."}
    
            # Construct parameters dictionary for the API call
            script_params = {}
            script_params["Mailbox"] = mailbox
            if labels_filter is not None:
                script_params["Labels Filter"] = labels_filter
            if internet_message_id is not None:
                script_params["Internet Message ID"] = internet_message_id
            if subject_filter is not None:
                script_params["Subject Filter"] = subject_filter
            if sender_filter is not None:
                script_params["Sender Filter"] = sender_filter
            if time_frame_minutes is not None:
                script_params["Time Frame (minutes)"] = time_frame_minutes
            if email_status is not None:
                script_params["Email Status"] = email_status
            if move_to_trash is not None:
                script_params["Move to Trash"] = move_to_trash
    
            # Prepare data model for the API request
            action_data = ApiManualActionDataModel(
                alertGroupIdentifiers=alert_group_identifiers,
                caseId=case_id,
                targetEntities=final_target_entities,
                scope=final_scope,
                isPredefinedScope=is_predefined_scope, # Pass the is_predefined_scope parameter
                actionProvider="Scripts", # Assuming constant based on example
                actionName="Gmail_Delete Email",
                properties={
                    "IntegrationInstance": instance_identifier,
                    "ScriptName": "Gmail_Delete Email", # Assuming same as actionName
                    "ScriptParametersEntityFields": json.dumps(script_params)
                }
            )
    
            # Execute the action via HTTP POST
            try:
                execution_response = await bindings.http_client.post(
                    Endpoints.EXECUTE_MANUAL_ACTION,
                    req=action_data.model_dump()
                )
                return execution_response
            except Exception as e:
                # Log error appropriately
                print(f"Error executing action Gmail_Delete Email for Gmail: {e}")
                return {"Status": "Failed", "Message": f"Error executing action: {e}"}
        else:
            print(f"Warning: No active integration instance found for Gmail")
            return {"Status": "Failed", "Message": "No active instance found."}
