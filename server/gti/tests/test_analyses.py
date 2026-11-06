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
import json
import logging
from pathlib import Path
from unittest import mock

import mcp
from mcp.shared.memory import (
    create_connected_server_and_client_session as client_session,
)
import pytest
import pytest_httpserver
import vt
from werkzeug.wrappers import Request, Response

from gti_mcp.server import server


SAMPLE_SHA256 = (
    "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855"
)
SAMPLE_URL = "https://example.org/login?id=42&mode=test"
SAMPLE_URL_ID = vt.url_id(SAMPLE_URL)


@pytest.fixture(autouse=True)
def fresh_vt_client_factory(
    make_httpserver_ipv4: pytest_httpserver.HTTPServer,
    monkeypatch: pytest.MonkeyPatch,
):
  """Returns a fresh vt.Client per request so close_async() stays isolated."""
  host = f"http://{make_httpserver_ipv4.host}:{make_httpserver_ipv4.port}"
  monkeypatch.setattr(
      "gti_mcp.server.vt_client_factory",
      lambda _ctx: vt.Client("dummy_api_key", host=host, timeout=30),
  )


async def _call_json_tool(name: str, arguments: dict) -> dict:
  async with client_session(server._mcp_server) as client:
    result = await client.call_tool(name, arguments=arguments)
  assert not result.isError, result.content[0].text
  assert len(result.content) == 1
  return json.loads(result.content[0].text)


@pytest.mark.asyncio(loop_scope="session")
async def test_analysis_tools_registered():
  """All 7 scan, reanalysis, and analysis tools are exposed on the MCP server."""
  async with client_session(server._mcp_server) as client:
    tools_result = await client.list_tools()

  assert isinstance(tools_result, mcp.ListToolsResult)
  tool_names = {tool.name for tool in tools_result.tools}
  expected = {
      "submit_file",
      "reanalyze_file",
      "submit_url",
      "reanalyze_url",
      "reanalyze_domain",
      "reanalyze_ip",
      "get_analysis",
  }
  assert expected.issubset(tool_names)


@pytest.mark.asyncio(loop_scope="session")
async def test_submit_file_uploads_basename_only(
    make_httpserver_ipv4: pytest_httpserver.HTTPServer,
    tmp_path: Path,
):
  """submit_file uploads multipart content using only the file basename."""
  nested_dir = tmp_path / "sensitive_parent_dir"
  nested_dir.mkdir()
  sample_file = nested_dir / "payload.bin"
  sample_file.write_bytes(b"MZ-benign-test-bytes")

  upload_path = "/custom_upload/slot-1"
  upload_url = (
      f"http://{make_httpserver_ipv4.host}:{make_httpserver_ipv4.port}"
      f"{upload_path}"
  )
  make_httpserver_ipv4.expect_oneshot_request(
      "/api/v3/files/upload_url",
      method="GET",
      headers={"X-Apikey": "dummy_api_key"},
  ).respond_with_json({"data": upload_url})

  captured = {}

  def _handle_upload(request: Request) -> Response:
    captured["content_type"] = request.headers.get("Content-Type", "")
    captured["raw_body"] = request.get_data()
    return Response(
        json.dumps({
            "data": {
                "id": "NjY0MjRlOTFjMDIyZjkyNWM0NjU2NWQzOjE3MDAwMDAwMDA=",
                "type": "analysis",
                "links": {"self": "https://www.virustotal.com/api/v3/analyses/x"},
            }
        }),
        status=200,
        content_type="application/json",
    )

  make_httpserver_ipv4.expect_oneshot_request(
      upload_path,
      method="POST",
  ).respond_with_handler(_handle_upload)

  data = await _call_json_tool(
      "submit_file", {"file_path": str(sample_file)}
  )

  assert data["id"] == "NjY0MjRlOTFjMDIyZjkyNWM0NjU2NWQzOjE3MDAwMDAwMDA="
  assert data["type"] == "analysis"
  assert captured["content_type"].startswith("multipart/form-data")
  assert b'filename="payload.bin"' in captured["raw_body"]
  assert b"sensitive_parent_dir" not in captured["raw_body"]
  assert b"MZ-benign-test-bytes" in captured["raw_body"]


@pytest.mark.asyncio(loop_scope="session")
async def test_submit_file_missing_path_returns_error(tmp_path: Path):
  """submit_file returns a structured error dict when the file does not exist."""
  missing = tmp_path / "does_not_exist.exe"
  data = await _call_json_tool("submit_file", {"file_path": str(missing)})
  assert "error" in data
  assert "File not found" in data["error"]


@pytest.mark.asyncio(loop_scope="session")
async def test_submit_url(make_httpserver_ipv4: pytest_httpserver.HTTPServer):
  """submit_url posts the URL for scanning and returns the analysis descriptor."""
  captured = {}

  def _handle_url_scan(request: Request) -> Response:
    captured["form_url"] = request.form.get("url")
    return Response(
        json.dumps({
            "data": {
                "id": f"u-{SAMPLE_SHA256}-1700000000",
                "type": "analysis",
            }
        }),
        status=200,
        content_type="application/json",
    )

  make_httpserver_ipv4.expect_oneshot_request(
      "/api/v3/urls",
      method="POST",
      headers={"X-Apikey": "dummy_api_key"},
  ).respond_with_handler(_handle_url_scan)

  data = await _call_json_tool("submit_url", {"url": SAMPLE_URL})
  assert captured["form_url"] == SAMPLE_URL
  assert data == {
      "id": f"u-{SAMPLE_SHA256}-1700000000",
      "type": "analysis",
  }


@pytest.mark.asyncio(loop_scope="session")
@pytest.mark.parametrize(
    ("tool_name", "tool_args", "expected_path", "analysis_id"),
    [
        (
            "reanalyze_file",
            {"hash": SAMPLE_SHA256},
            f"/api/v3/files/{SAMPLE_SHA256}/analyse",
            "f-analysis-001",
        ),
        (
            "reanalyze_url",
            {"url": SAMPLE_URL},
            f"/api/v3/urls/{SAMPLE_URL_ID}/analyse",
            "u-analysis-002",
        ),
        (
            "reanalyze_domain",
            {"domain": "example.org"},
            "/api/v3/domains/example.org/analyse",
            "d-analysis-003",
        ),
        (
            "reanalyze_ip",
            {"ip_address": "198.51.100.42"},
            "/api/v3/ip_addresses/198.51.100.42/analyse",
            "ip-analysis-004",
        ),
    ],
)
async def test_reanalyze_endpoints(
    make_httpserver_ipv4: pytest_httpserver.HTTPServer,
    tool_name: str,
    tool_args: dict,
    expected_path: str,
    analysis_id: str,
):
  """All 4 reanalyze_* tools trigger POST .../analyse and unwrap data."""
  make_httpserver_ipv4.expect_oneshot_request(
      expected_path,
      method="POST",
      headers={"X-Apikey": "dummy_api_key"},
  ).respond_with_json({
      "data": {
          "id": analysis_id,
          "type": "analysis",
      }
  })

  data = await _call_json_tool(tool_name, tool_args)
  assert data == {"id": analysis_id, "type": "analysis"}


@pytest.mark.asyncio(loop_scope="session")
async def test_get_analysis_strips_engine_results_by_default(
    make_httpserver_ipv4: pytest_httpserver.HTTPServer,
):
  """get_analysis omits per-engine results by default while keeping stats & meta."""
  analysis_id = f"u-{SAMPLE_SHA256}-1700000099"
  api_payload = {
      "data": {
          "id": analysis_id,
          "type": "analysis",
          "attributes": {
              "status": "completed",
              "date": 1700000099,
              "stats": {
                  "malicious": 2,
                  "suspicious": 1,
                  "undetected": 65,
                  "harmless": 12,
              },
              "results": {
                  "EngineAlpha": {
                      "category": "malicious",
                      "result": "Phishing",
                      "engine_name": "EngineAlpha",
                  },
                  "EngineBeta": {
                      "category": "undetected",
                      "result": None,
                      "engine_name": "EngineBeta",
                  },
              },
          },
      },
      "meta": {
          "file_info": {
              "sha256": SAMPLE_SHA256,
              "size": 1024,
          }
      },
  }

  make_httpserver_ipv4.expect_oneshot_request(
      f"/api/v3/analyses/{analysis_id}",
      method="GET",
      headers={"X-Apikey": "dummy_api_key"},
  ).respond_with_json(api_payload)

  compact = await _call_json_tool(
      "get_analysis", {"analysis_id": analysis_id}
  )
  assert compact["id"] == analysis_id
  assert compact["type"] == "analysis"
  assert compact["attributes"]["status"] == "completed"
  assert compact["attributes"]["stats"]["malicious"] == 2
  assert "results" not in compact["attributes"]
  assert compact["meta"]["file_info"]["sha256"] == SAMPLE_SHA256

  make_httpserver_ipv4.expect_oneshot_request(
      f"/api/v3/analyses/{analysis_id}",
      method="GET",
      headers={"X-Apikey": "dummy_api_key"},
  ).respond_with_json(api_payload)

  full = await _call_json_tool(
      "get_analysis",
      {"analysis_id": analysis_id, "include_engine_results": True},
  )
  assert "results" in full["attributes"]
  assert full["attributes"]["results"]["EngineAlpha"]["category"] == "malicious"


@pytest.mark.asyncio(loop_scope="session")
async def test_reanalyze_api_error_uses_lazy_logging(
    make_httpserver_ipv4: pytest_httpserver.HTTPServer,
    caplog: pytest.LogCaptureFixture,
):
  """API errors return a structured error dict and use lazy %s logger args."""
  make_httpserver_ipv4.expect_oneshot_request(
      "/api/v3/domains/nonexistent-domain.invalid/analyse",
      method="POST",
      headers={"X-Apikey": "dummy_api_key"},
  ).respond_with_json(
      {"error": {"code": "NotFoundError", "message": "Domain not found"}},
      status=404,
  )

  with caplog.at_level(logging.WARNING, logger="gti_mcp.tools.analyses"):
    data = await _call_json_tool(
        "reanalyze_domain", {"domain": "nonexistent-domain.invalid"}
    )

  assert "error" in data
  assert "NotFoundError" in data["error"]
  assert "Domain not found" in data["error"]
  assert caplog.records
  assert all(record.args for record in caplog.records)
