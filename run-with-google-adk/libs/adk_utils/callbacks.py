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

from google.adk.agents.callback_context import CallbackContext
import os
import logging

from google.genai import types

from typing import Optional
from google.adk.models import LlmResponse, LlmRequest


def bmc_trim_llm_request(
    callback_context: CallbackContext, llm_request: LlmRequest
) -> Optional[LlmResponse]:

    max_prev_user_interactions = int(os.environ.get("MAX_PREV_USER_INTERACTIONS","-1"))

    # Everytime the entire new / full list comes from Execution Logic
    logging.info(f"Number of contents going to LLM - {len(llm_request.contents)}, MAX_PREV_USER_INTERACTIONS = {max_prev_user_interactions}")

    temp_processed_list = []
    
    if max_prev_user_interactions == -1:
        return None 
    else:
        user_message_count = 0
        # Iterate in reverse order
        for i in range(len(llm_request.contents) - 1, -1, -1):
            item = llm_request.contents[i]
            
            # Check if the item is a user message and has text content
            if item.role == "user" and item.parts[0] and item.parts[0].text and item.parts[0].text != "For context:":
                logging.info(f"Encountered a user message => {item.parts[0].text}")
                user_message_count += 1

            if user_message_count > max_prev_user_interactions:
                logging.info(f"Breaking at user_message_count => {user_message_count}")
                temp_processed_list.append(item) # make sure we add this user message.
                break
            
            temp_processed_list.append(item)

        # Reverse the temp_processed_list to restore the original chronological order
        final_list = temp_processed_list[::-1]

        # If user_message_count didn't reach the limit, the list remains unchanged.
        if user_message_count < max_prev_user_interactions:
            logging.info("User message count did not reach the allowed limit. List remains unchanged.")
        else:
            logging.info(f"User message count reached {max_prev_user_interactions}. List truncated.")
            llm_request.contents = final_list


    # we still want LLM to be called, only sometimes with reduced number of contents.    
    return None 


def bac_setup_state_variable(callback_context: CallbackContext) -> Optional[types.Content]:
    current_state = callback_context.state.to_dict()  

    # Only applicable for ADK WEB UI. 
    # As we can provide state in when we have access to the session (in custom runner).
    # keeping it consistent with the ADK web as user_name is defaulted to 'user'
   
    if "user_name" not in current_state:
      logging.info("Creating default state to update the prompt")
      user_name = "user"

      if os.environ.get("AE_RUN","N") == "Y":
          user_name = callback_context._invocation_context.session.user_id

      initial_state = {
        "user_name":user_name
      }      
      callback_context.state.update(initial_state)
    else:
      logging.info(f"Found user_name with value {current_state['user_name']}...")
    return None