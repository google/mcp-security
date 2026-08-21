# Copyright 2026 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""Unit tests for investigation management tools."""

import pytest

from secops_mcp.tools.investigation_management import list_investigations


@pytest.mark.asyncio
async def test_list_investigations_does_not_write_stdout(
    monkeypatch, capsys
) -> None:
    """Ensure list diagnostics cannot corrupt the MCP stdio transport."""

    class ChronicleStub:
        def list_investigations(self, **kwargs):
            return {"investigations": []}

    monkeypatch.setattr(
        "secops_mcp.tools.investigation_management.get_chronicle_client",
        lambda *args: ChronicleStub(),
    )

    assert await list_investigations(page_size=1) == {"investigations": []}
    assert capsys.readouterr().out == ""
