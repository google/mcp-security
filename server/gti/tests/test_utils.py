
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
import pytest
import vt
from unittest.mock import MagicMock, AsyncMock
from gti_mcp import utils

@pytest.mark.asyncio
async def test_fetch_object_handles_api_error():
    """Test that fetch_object catches vt.error.APIError and returns an error dict."""
    # Mock vt.Client
    mock_client = MagicMock(spec=vt.Client)
    
    # Configure get_object_async to raise vt.error.APIError
    error_code = 'NotFoundError'
    error_message = 'Domain "test.com" not found'
    mock_client.get_object_async = AsyncMock(side_effect=vt.error.APIError(error_code, error_message))
    
    # Call fetch_object
    result = await utils.fetch_object(
        mock_client,
        "domains",
        "domain",
        "test.com"
    )
    
    # Assertions
    assert "error" in result
    assert f"VirusTotal API Error: {error_code} - {error_message}" in result["error"]
    assert "details" in result
    assert "The requested domain 'test.com' could not be found" in result["details"]
