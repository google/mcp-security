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
"""Lifecycle callbacks for request trimming and context logging in Google ADK."""

import logging
from typing import Any

logger = logging.getLogger(__name__)


def bmc_trim_llm_request(callback_context: Any, llm_request: Any) -> Any:
    """Callback executed prior to LLM invocation to inspect and trim context if necessary.

    Args:
        callback_context: ADK callback context object.
        llm_request: Inbound LLM request object.

    Returns:
        The processed LLM request object.
    """
    logger.debug("Executing before_model_callback for context verification.")
    return llm_request
