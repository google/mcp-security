# Copyright 2026 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""Unit tests for threat intelligence tool return types and serialization."""

import json
from unittest.mock import MagicMock, patch

import pytest
from secops_mcp.tools.threat_intel import get_threat_intel


@pytest.fixture
def chronicle_client():
    with patch("secops_mcp.tools.threat_intel.get_chronicle_client") as mock_get_client:
        client = MagicMock()
        mock_get_client.return_value = client
        yield client


@pytest.mark.asyncio
async def test_get_threat_intel_gemini_response_object(chronicle_client):
    mock_resp = MagicMock()
    mock_resp.get_text_content.return_value = "APT41 is a prolific cyber threat group."
    chronicle_client.gemini.return_value = mock_resp

    result = await get_threat_intel(query="Summarize APT41")

    assert isinstance(result, str)
    assert result == "APT41 is a prolific cyber threat group."


@pytest.mark.asyncio
async def test_get_threat_intel_blocks_format(chronicle_client):
    block1 = MagicMock()
    block1.block_type = "TEXT"
    block1.content = "Paragraph 1"

    block2 = MagicMock()
    block2.block_type = "TEXT"
    block2.content = "Paragraph 2"

    mock_resp = MagicMock(spec=["blocks"])
    mock_resp.blocks = [block1, block2]
    chronicle_client.gemini.return_value = mock_resp

    result = await get_threat_intel(query="Test query")

    assert isinstance(result, str)
    assert result == "Paragraph 1\n\nParagraph 2"


@pytest.mark.asyncio
async def test_get_threat_intel_dict_with_str_answer(chronicle_client):
    chronicle_client.gemini.return_value = {"answer": "Threat intel summary."}

    result = await get_threat_intel(query="Test query")

    assert isinstance(result, str)
    assert result == "Threat intel summary."


@pytest.mark.asyncio
async def test_get_threat_intel_dict_with_nested_dict_answer(chronicle_client):
    chronicle_client.gemini.return_value = {
        "answer": {"summary": "Nested dict content", "risk_level": "High"}
    }

    result = await get_threat_intel(query="Test query")

    assert isinstance(result, str)
    parsed = json.loads(result)
    assert parsed == {"summary": "Nested dict content", "risk_level": "High"}


@pytest.mark.asyncio
async def test_get_threat_intel_direct_str(chronicle_client):
    chronicle_client.gemini.return_value = "Direct string response"

    result = await get_threat_intel(query="Test query")

    assert isinstance(result, str)
    assert result == "Direct string response"


@pytest.mark.asyncio
async def test_get_threat_intel_unexpected_format_serializes_to_json(chronicle_client):
    unexpected_response = {
        "results": [{"actor": "APT29", "confidence": 95}],
        "metadata": {"total": 1},
    }
    chronicle_client.gemini.return_value = unexpected_response

    result = await get_threat_intel(query="Test query")

    assert isinstance(result, str)
    parsed = json.loads(result)
    assert parsed == unexpected_response


@pytest.mark.asyncio
async def test_get_threat_intel_handles_exception(chronicle_client):
    chronicle_client.gemini.side_effect = RuntimeError("Chronicle API unavailable")

    result = await get_threat_intel(query="Test query")

    assert isinstance(result, str)
    assert "Error retrieving threat intelligence: Chronicle API unavailable" in result
