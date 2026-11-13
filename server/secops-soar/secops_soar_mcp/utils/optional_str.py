# Copyright 2026 Google LLC
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
"""Annotation for optional string tool parameters."""

import json
from typing import Annotated, Any

from pydantic import BeforeValidator


def _json_back_to_text(value: Any) -> Any:
    """Re-encode a JSON object or array that FastMCP decoded from a string.

    FastMCP decodes a string argument that holds a JSON object or array
    whenever the parameter is not annotated exactly `str`, so '{"a": 1}'
    sent to a `str | None` parameter arrives here as a dict and would fail
    string validation.
    """
    if isinstance(value, dict | list):
        return json.dumps(value, ensure_ascii=False)
    return value


# A `str | None` parameter that still accepts JSON text such as '{"a": 1}'.
# The text is re-encoded, so whitespace may differ from what the client sent.
# The string "null" is decoded to None before validation, so it arrives as None.
OptionalStr = Annotated[str | None, BeforeValidator(_json_back_to_text)]
