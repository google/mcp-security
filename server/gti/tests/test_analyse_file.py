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
"""Unit tests for analyse_file and GTI_ALLOWED_UPLOAD_DIR."""

import logging
import os
import pathlib
import stat
from contextlib import asynccontextmanager
from unittest.mock import AsyncMock, MagicMock, patch

import aiohttp
import pytest
import vt
from gti_mcp import tools
from gti_mcp.server import server
from gti_mcp.tools import files
from mcp.server.fastmcp.exceptions import ToolError
from mcp.shared.memory import (
    create_connected_server_and_client_session as client_session,
)
from werkzeug.wrappers import Request, Response


@pytest.fixture(autouse=True)
def clean_environment():
  """Ensures GTI_ALLOWED_UPLOAD_DIR and tool registration state are restored."""
  original_env = os.environ.get("GTI_ALLOWED_UPLOAD_DIR")
  yield
  if original_env is None:
    os.environ.pop("GTI_ALLOWED_UPLOAD_DIR", None)
  else:
    os.environ["GTI_ALLOWED_UPLOAD_DIR"] = original_env
  files._register_upload_tools(server)


@pytest.mark.asyncio(loop_scope="session")
async def test_default_startup_analyse_file_unregistered():
  """By default without GTI_ALLOWED_UPLOAD_DIR, analyse_file must not be registered."""
  os.environ.pop("GTI_ALLOWED_UPLOAD_DIR", None)
  files._register_upload_tools(server)

  assert "analyse_file" not in server._tool_manager._tools

  async with client_session(server._mcp_server) as client:
    tools_result = await client.list_tools()
    tool_names = [tool.name for tool in tools_result.tools]
    assert "analyse_file" not in tool_names

    call_result = await client.call_tool("analyse_file", {"file_path": "test.bin"})
    assert call_result.isError
    assert "Unknown tool: analyse_file" in call_result.content[0].text


@pytest.mark.asyncio(loop_scope="session")
async def test_direct_call_when_unconfigured_returns_error_dict():
  """Direct call when GTI_ALLOWED_UPLOAD_DIR is unset returns descriptive error."""
  os.environ.pop("GTI_ALLOWED_UPLOAD_DIR", None)

  res = await files.analyse_file("sample.bin", ctx=MagicMock())
  assert "error" in res
  assert "analyse_file is disabled by default" in res["error"]
  assert "GTI_ALLOWED_UPLOAD_DIR" in res["error"]


def test_startup_validation_rejects_filesystem_root():
  """Filesystem root cannot be used as upload directory."""
  os.environ["GTI_ALLOWED_UPLOAD_DIR"] = "/"
  with pytest.raises(ValueError, match="cannot be the filesystem root"):
    files._register_upload_tools(server)


def test_startup_validation_rejects_relative_path():
  """Relative paths are rejected for GTI_ALLOWED_UPLOAD_DIR."""
  os.environ["GTI_ALLOWED_UPLOAD_DIR"] = "relative/upload_dir"
  with pytest.raises(ValueError, match="must be an absolute path"):
    files._register_upload_tools(server)


def test_startup_validation_rejects_nonexistent_path(tmp_path):
  """Non-existent directories are rejected."""
  missing_dir = tmp_path / "does_not_exist_upload_dir"
  os.environ["GTI_ALLOWED_UPLOAD_DIR"] = str(missing_dir)
  with pytest.raises(ValueError, match="does not exist or cannot be resolved"):
    files._register_upload_tools(server)


def test_startup_validation_rejects_regular_file(tmp_path):
  """Paths pointing to regular files instead of directories are rejected."""
  fake_file = tmp_path / "regular_file.txt"
  fake_file.write_text("not a directory")
  os.environ["GTI_ALLOWED_UPLOAD_DIR"] = str(fake_file)
  with pytest.raises(ValueError, match="must be a directory"):
    files._register_upload_tools(server)


def test_startup_validation_rejects_control_characters():
  """Paths containing control characters are rejected."""
  os.environ["GTI_ALLOWED_UPLOAD_DIR"] = "/tmp/upload\ndir"
  with pytest.raises(ValueError, match="must not contain control characters"):
    files._register_upload_tools(server)


def test_registration_lifecycle(tmp_path):
  """Tool registration toggles cleanly based on GTI_ALLOWED_UPLOAD_DIR."""
  os.environ["GTI_ALLOWED_UPLOAD_DIR"] = str(tmp_path)
  assert files._register_upload_tools(server) is True
  assert "analyse_file" in server._tool_manager._tools

  os.environ.pop("GTI_ALLOWED_UPLOAD_DIR", None)
  assert files._register_upload_tools(server) is False
  assert "analyse_file" not in server._tool_manager._tools


@pytest.mark.asyncio(loop_scope="session")
async def test_valid_upload_relative_path(tmp_path):
  """Valid file within upload_dir via relative path is uploaded with sanitized basename."""
  os.environ["GTI_ALLOWED_UPLOAD_DIR"] = str(tmp_path)
  files._register_upload_tools(server)

  sample_file = tmp_path / "sample.bin"
  sample_content = b"sample-payload"
  sample_file.write_bytes(sample_content)

  fake_analysis = MagicMock()
  fake_analysis_result = MagicMock()
  fake_analysis_result.id = "analysis-12345"
  fake_analysis_result.to_dict.return_value = {"id": "analysis-12345", "status": "completed"}

  captured_bytes = []

  async def fake_scan(file):
    captured_bytes.append(file.read())
    return fake_analysis

  mock_client = MagicMock()
  mock_client.scan_file_async = AsyncMock(side_effect=fake_scan)
  mock_client.wait_for_analysis_completion = AsyncMock(return_value=fake_analysis_result)

  @asynccontextmanager
  async def fake_vt_client(unused_ctx):
    yield mock_client

  with patch("gti_mcp.tools.files.vt_client", side_effect=fake_vt_client):
    res = await files.analyse_file("sample.bin", ctx=MagicMock())

  assert res == {"id": "analysis-12345", "status": "completed"}
  mock_client.scan_file_async.assert_awaited_once()
  uploaded_file_arg = mock_client.scan_file_async.call_args.kwargs["file"]
  assert uploaded_file_arg.name == "sample.bin"
  assert captured_bytes == [sample_content]


@pytest.mark.asyncio(loop_scope="session")
async def test_valid_upload_nested_relative_path(tmp_path):
  """Nested relative paths within upload_dir have their upload filename stripped to basename."""
  os.environ["GTI_ALLOWED_UPLOAD_DIR"] = str(tmp_path)
  files._register_upload_tools(server)

  nested_dir = tmp_path / "sub" / "uploads"
  nested_dir.mkdir(parents=True, exist_ok=True)
  sample_file = nested_dir / "target.exe"
  sample_file.write_bytes(b"nested-binary-data")

  fake_analysis = MagicMock()
  fake_analysis_result = MagicMock()
  fake_analysis_result.id = "analysis-nested-1"
  fake_analysis_result.to_dict.return_value = {"id": "analysis-nested-1"}

  mock_client = MagicMock()
  mock_client.scan_file_async = AsyncMock(return_value=fake_analysis)
  mock_client.wait_for_analysis_completion = AsyncMock(return_value=fake_analysis_result)

  @asynccontextmanager
  async def fake_vt_client(unused_ctx):
    yield mock_client

  with patch("gti_mcp.tools.files.vt_client", side_effect=fake_vt_client):
    res = await files.analyse_file("sub/uploads/target.exe", ctx=MagicMock())

  assert res == {"id": "analysis-nested-1"}
  uploaded_file_arg = mock_client.scan_file_async.call_args.kwargs["file"]
  assert uploaded_file_arg.name == "target.exe"


@pytest.mark.asyncio(loop_scope="session")
async def test_valid_upload_absolute_path_within_upload_dir(tmp_path):
  """Absolute paths within upload_dir are accepted and stripped to safe basename."""
  os.environ["GTI_ALLOWED_UPLOAD_DIR"] = str(tmp_path)
  files._register_upload_tools(server)

  sample_file = tmp_path / "abs_sample.dll"
  sample_file.write_bytes(b"dll-data")

  fake_analysis = MagicMock()
  fake_analysis_result = MagicMock()
  fake_analysis_result.id = "analysis-abs-1"
  fake_analysis_result.to_dict.return_value = {"id": "analysis-abs-1"}

  mock_client = MagicMock()
  mock_client.scan_file_async = AsyncMock(return_value=fake_analysis)
  mock_client.wait_for_analysis_completion = AsyncMock(return_value=fake_analysis_result)

  @asynccontextmanager
  async def fake_vt_client(unused_ctx):
    yield mock_client

  with patch("gti_mcp.tools.files.vt_client", side_effect=fake_vt_client):
    res = await files.analyse_file(str(sample_file), ctx=MagicMock())

  assert res == {"id": "analysis-abs-1"}
  uploaded_file_arg = mock_client.scan_file_async.call_args.kwargs["file"]
  assert uploaded_file_arg.name == "abs_sample.dll"


@pytest.mark.asyncio(loop_scope="session")
async def test_mcp_protocol_enabled_valid_upload(tmp_path):
  """Enabled MCP client call_tool uploads allowed file and keeps wrapped outputSchema."""
  os.environ["GTI_ALLOWED_UPLOAD_DIR"] = str(tmp_path)
  files._register_upload_tools(server)

  sample_file = tmp_path / "mcp_sample.bin"
  sample_content = b"mcp-protocol-payload"
  sample_file.write_bytes(sample_content)

  fake_analysis = MagicMock()
  fake_analysis_result = MagicMock()
  fake_analysis_result.id = "analysis-mcp-1"
  fake_analysis_result.to_dict.return_value = {
      "id": "analysis-mcp-1",
      "status": "completed",
  }

  captured_bytes = []

  async def fake_scan(file):
    captured_bytes.append(file.read())
    return fake_analysis

  mock_client = MagicMock()
  mock_client.scan_file_async = AsyncMock(side_effect=fake_scan)
  mock_client.wait_for_analysis_completion = AsyncMock(
      return_value=fake_analysis_result
  )

  @asynccontextmanager
  async def fake_vt_client(unused_ctx):
    yield mock_client

  with patch("gti_mcp.tools.files.vt_client", side_effect=fake_vt_client):
    async with client_session(server._mcp_server) as client:
      tools_result = await client.list_tools()
      schemas = {tool.name: tool.outputSchema for tool in tools_result.tools}
      assert "analyse_file" in schemas
      assert schemas["analyse_file"] is not None
      assert schemas["analyse_file"]["required"] == ["result"]
      assert schemas["analyse_file"]["properties"]["result"]["type"] == "object"

      result = await client.call_tool(
          "analyse_file", {"file_path": "mcp_sample.bin"}
      )

  assert not result.isError
  assert result.structuredContent is not None
  assert result.structuredContent["result"] == {
      "id": "analysis-mcp-1",
      "status": "completed",
  }
  assert captured_bytes == [sample_content]


@pytest.mark.asyncio(loop_scope="session")
async def test_mcp_protocol_enabled_rejects_outside_upload_dir(tmp_path):
  """Enabled MCP client call_tool rejects paths outside upload_dir via structured error."""
  upload_dir = tmp_path / "uploads"
  upload_dir.mkdir()
  outside_dir = tmp_path / "outside"
  outside_dir.mkdir()
  outside_file = outside_dir / "outside.bin"
  outside_file.write_bytes(b"outside")

  os.environ["GTI_ALLOWED_UPLOAD_DIR"] = str(upload_dir)
  files._register_upload_tools(server)

  with patch("gti_mcp.tools.files.vt_client") as mock_vt:
    async with client_session(server._mcp_server) as client:
      result = await client.call_tool(
          "analyse_file", {"file_path": str(outside_file)}
      )

  assert not result.isError
  assert result.structuredContent is not None
  payload = result.structuredContent["result"]
  assert "error" in payload
  assert "outside the allowed GTI_ALLOWED_UPLOAD_DIR directory" in payload["error"]
  assert str(upload_dir) not in payload["error"]
  mock_vt.assert_not_called()


@pytest.mark.asyncio(loop_scope="session")
@pytest.mark.parametrize("delete_dir", [True, False])
async def test_runtime_missing_or_deleted_upload_dir_redacts_host_path(
    tmp_path, delete_dir
):
  """If upload_dir becomes missing or deleted after startup, error redacts host path."""
  upload_dir = tmp_path / "ephemeral_upload_dir"
  upload_dir.mkdir()
  os.environ["GTI_ALLOWED_UPLOAD_DIR"] = str(upload_dir)
  assert files._register_upload_tools(server) is True

  if delete_dir:
    upload_dir.rmdir()
  else:
    os.environ["GTI_ALLOWED_UPLOAD_DIR"] = str(tmp_path / "missing_runtime_dir")

  with patch("gti_mcp.tools.files.vt_client") as mock_vt:
    res = await files.analyse_file("sample.bin", ctx=MagicMock())

  assert res == {
      "error": "Invalid GTI_ALLOWED_UPLOAD_DIR configuration; check server logs."
  }
  assert str(tmp_path) not in res["error"]
  mock_vt.assert_not_called()


@pytest.mark.asyncio(loop_scope="session")
async def test_rejects_absolute_path_outside_upload_dir(tmp_path):
  """Absolute paths outside upload_dir are rejected without upload or host path leak."""
  upload_dir = tmp_path / "uploads"
  upload_dir.mkdir()
  outside_dir = tmp_path / "outside"
  outside_dir.mkdir()
  outside_file = outside_dir / "outside.bin"
  outside_file.write_bytes(b"outside")

  os.environ["GTI_ALLOWED_UPLOAD_DIR"] = str(upload_dir)
  files._register_upload_tools(server)

  with patch("gti_mcp.tools.files.vt_client") as mock_vt:
    res = await files.analyse_file(str(outside_file), ctx=MagicMock())

  assert "error" in res
  assert "outside the allowed GTI_ALLOWED_UPLOAD_DIR directory" in res["error"]
  assert str(upload_dir) not in res["error"]
  mock_vt.assert_not_called()


@pytest.mark.asyncio(loop_scope="session")
async def test_rejects_parent_traversal(tmp_path):
  """Directory traversal using '..' is rejected."""
  os.environ["GTI_ALLOWED_UPLOAD_DIR"] = str(tmp_path)
  files._register_upload_tools(server)

  with patch("gti_mcp.tools.files.vt_client") as mock_vt:
    res = await files.analyse_file("../../outside.bin", ctx=MagicMock())

  assert "error" in res
  assert "Directory traversal with '..' is not allowed" in res["error"]
  mock_vt.assert_not_called()


@pytest.mark.asyncio(loop_scope="session")
@pytest.mark.parametrize(
    "bad_path",
    [
        "C:sample.bin",
        "\\sample.bin",
    ],
)
async def test_rejects_drive_qualified_or_rooted_relative_paths(
    tmp_path, bad_path
):
  """Drive-qualified or backslash-rooted non-absolute paths are rejected."""
  os.environ["GTI_ALLOWED_UPLOAD_DIR"] = str(tmp_path)
  files._register_upload_tools(server)

  with patch("gti_mcp.tools.files.vt_client") as mock_vt:
    res = await files.analyse_file(bad_path, ctx=MagicMock())

  assert res == {
      "error": "Drive-qualified or rooted relative paths are not allowed"
  }
  mock_vt.assert_not_called()


def test_rejects_configured_dir_with_parent_segments(tmp_path):
  """configured_dir containing '..' is never trusted as a confinement prefix."""
  upload_dir = tmp_path / "uploads"
  upload_dir.mkdir()
  outside = tmp_path / "outside"
  outside.mkdir()
  other_file = outside / "other.bin"
  other_file.write_text("other")

  dotdot_configured = pathlib.Path(f"{upload_dir}/../outside")
  with pytest.raises(
      PermissionError,
      match="outside the allowed GTI_ALLOWED_UPLOAD_DIR directory",
  ):
    files._open_confined_upload_file(
        str(other_file), upload_dir, configured_dir=dotdot_configured
    )


@pytest.mark.asyncio(loop_scope="session")
async def test_rejects_sibling_prefix_collision(tmp_path):
  """Sibling directory prefix match (e.g. /uploads vs /uploads_other) is rejected."""
  upload_dir = tmp_path / "uploads"
  sibling = tmp_path / "uploads_other"
  upload_dir.mkdir()
  sibling.mkdir()

  sibling_file = sibling / "other.bin"
  sibling_file.write_text("other")

  os.environ["GTI_ALLOWED_UPLOAD_DIR"] = str(upload_dir)
  files._register_upload_tools(server)

  with patch("gti_mcp.tools.files.vt_client") as mock_vt:
    res = await files.analyse_file(str(sibling_file), ctx=MagicMock())

  assert "error" in res
  assert "outside the allowed GTI_ALLOWED_UPLOAD_DIR directory" in res["error"]
  assert str(upload_dir) not in res["error"]
  mock_vt.assert_not_called()


@pytest.mark.asyncio(loop_scope="session")
async def test_rejects_symlink_inside_pointing_outside(tmp_path):
  """Symlinks inside upload_dir pointing outside are rejected."""
  outside_file = tmp_path / "outside.txt"
  outside_file.write_text("outside data")

  upload_dir = tmp_path / "uploads"
  upload_dir.mkdir()
  symlink_file = upload_dir / "linked.bin"
  symlink_file.symlink_to(outside_file)

  os.environ["GTI_ALLOWED_UPLOAD_DIR"] = str(upload_dir)
  files._register_upload_tools(server)

  with patch("gti_mcp.tools.files.vt_client") as mock_vt:
    res = await files.analyse_file("linked.bin", ctx=MagicMock())

  assert "error" in res
  assert "Symlinks are not allowed" in res["error"]
  mock_vt.assert_not_called()


@pytest.mark.asyncio(loop_scope="session")
async def test_rejects_symlink_inside_pointing_inside(tmp_path):
  """Even symlinks pointing within upload_dir are rejected to enforce canonical files."""
  upload_dir = tmp_path / "uploads"
  upload_dir.mkdir()
  real_file = upload_dir / "real.txt"
  real_file.write_text("real content")
  symlink_file = upload_dir / "symlink_inside.txt"
  symlink_file.symlink_to(real_file)

  os.environ["GTI_ALLOWED_UPLOAD_DIR"] = str(upload_dir)
  files._register_upload_tools(server)

  with patch("gti_mcp.tools.files.vt_client") as mock_vt:
    res = await files.analyse_file("symlink_inside.txt", ctx=MagicMock())

  assert "error" in res
  assert "Symlinks are not allowed" in res["error"]
  mock_vt.assert_not_called()


@pytest.mark.asyncio(loop_scope="session")
async def test_rejects_intermediate_directory_symlink(tmp_path):
  """Directory symlinks in the path hierarchy are rejected."""
  upload_dir = tmp_path / "uploads"
  upload_dir.mkdir()
  target_dir = tmp_path / "target_dir"
  target_dir.mkdir()
  target_file = target_dir / "target.txt"
  target_file.write_text("target")

  symlink_dir = upload_dir / "symlink_dir"
  symlink_dir.symlink_to(target_dir)

  os.environ["GTI_ALLOWED_UPLOAD_DIR"] = str(upload_dir)
  files._register_upload_tools(server)

  with patch("gti_mcp.tools.files.vt_client") as mock_vt:
    res = await files.analyse_file("symlink_dir/target.txt", ctx=MagicMock())

  assert "error" in res
  assert "Symlinks are not allowed in directory path" in res["error"]
  mock_vt.assert_not_called()


@pytest.mark.asyncio(loop_scope="session")
async def test_rejects_non_regular_file(tmp_path):
  """Non-regular files (such as named pipes/FIFOs) are rejected."""
  fifo_path = tmp_path / "test_fifo"
  try:
    os.mkfifo(str(fifo_path))
  except (AttributeError, OSError):
    pytest.skip("FIFOs not supported in this environment")

  os.environ["GTI_ALLOWED_UPLOAD_DIR"] = str(tmp_path)
  files._register_upload_tools(server)

  with patch("gti_mcp.tools.files.vt_client") as mock_vt:
    res = await files.analyse_file("test_fifo", ctx=MagicMock())

  assert "error" in res
  assert "Path is not a regular file" in res["error"]
  mock_vt.assert_not_called()


@pytest.mark.asyncio(loop_scope="session")
@pytest.mark.parametrize(
    "invalid_path",
    [
        "",
        "   ",
        "sample\x00.bin",
        "sample\n.bin",
        "sample\r.bin",
    ],
)
async def test_rejects_invalid_path_strings(tmp_path, invalid_path):
  """Empty, whitespace, NUL, or control-character paths are rejected."""
  os.environ["GTI_ALLOWED_UPLOAD_DIR"] = str(tmp_path)
  files._register_upload_tools(server)

  with patch("gti_mcp.tools.files.vt_client") as mock_vt:
    res = await files.analyse_file(invalid_path, ctx=MagicMock())

  assert "error" in res
  mock_vt.assert_not_called()


def test_sanitize_upload_filename_edge_cases():
  """Basename sanitizer replaces unsafe or invalid filenames with default."""
  assert files._sanitize_upload_filename("clean_name.exe") == "clean_name.exe"
  assert files._sanitize_upload_filename("nested/path/sample.bin") == "sample.bin"
  assert files._sanitize_upload_filename("C:\\Windows\\test.dll") == "test.dll"

  # Unsafe or invalid attempts fall back to default
  assert files._sanitize_upload_filename('file"with"quotes.bin') == "submission.bin"
  assert files._sanitize_upload_filename("file\x00null.bin") == "submission.bin"
  assert files._sanitize_upload_filename("file\nnewline.bin") == "submission.bin"
  assert files._sanitize_upload_filename(".") == "submission.bin"
  assert files._sanitize_upload_filename("..") == "submission.bin"
  assert files._sanitize_upload_filename("") == "submission.bin"
  assert files._sanitize_upload_filename("a" * 256) == "submission.bin"


@pytest.mark.asyncio(loop_scope="session")
async def test_virustotal_api_error_handling(tmp_path):
  """VirusTotal APIError during upload is caught and returned cleanly."""
  os.environ["GTI_ALLOWED_UPLOAD_DIR"] = str(tmp_path)
  files._register_upload_tools(server)

  sample_file = tmp_path / "sample.bin"
  sample_file.write_bytes(b"test-bytes")

  mock_client = MagicMock()
  mock_client.scan_file_async = AsyncMock(
      side_effect=vt.error.APIError("QuotaExceeded", "API quota exceeded")
  )

  @asynccontextmanager
  async def fake_vt_client(unused_ctx):
    yield mock_client

  with patch("gti_mcp.tools.files.vt_client", side_effect=fake_vt_client):
    res = await files.analyse_file("sample.bin", ctx=MagicMock())

  assert "error" in res
  assert "VirusTotal API Error:" in res["error"]
  assert "API quota exceeded" in res["error"]


@pytest.mark.asyncio(loop_scope="session")
async def test_configured_dir_via_symlinked_parent_prefix(tmp_path):
  """Absolute caller paths using a symlinked parent prefix (such as macOS /tmp -> /private/tmp) work while inside symlinks remain blocked."""
  real_upload_dir = tmp_path / "private_tmp" / "uploads"
  real_upload_dir.mkdir(parents=True)
  alias_upload_dir = tmp_path / "tmp_uploads_alias"
  alias_upload_dir.symlink_to(real_upload_dir)

  sample_file = real_upload_dir / "macos_sample.bin"
  sample_file.write_bytes(b"macos-test")

  outside_other = tmp_path / "other.json"
  outside_other.write_text('{"other": "value"}')
  inside_symlink = real_upload_dir / "linked.bin"
  inside_symlink.symlink_to(outside_other)

  os.environ["GTI_ALLOWED_UPLOAD_DIR"] = str(alias_upload_dir)
  files._register_upload_tools(server)

  fake_analysis = MagicMock()
  fake_analysis_result = MagicMock()
  fake_analysis_result.id = "analysis-alias-1"
  fake_analysis_result.to_dict.return_value = {"id": "analysis-alias-1"}

  mock_client = MagicMock()
  mock_client.scan_file_async = AsyncMock(return_value=fake_analysis)
  mock_client.wait_for_analysis_completion = AsyncMock(return_value=fake_analysis_result)

  @asynccontextmanager
  async def fake_vt_client(unused_ctx):
    yield mock_client

  with patch("gti_mcp.tools.files.vt_client", side_effect=fake_vt_client):
    ok_res = await files.analyse_file(
        str(alias_upload_dir / "macos_sample.bin"), ctx=MagicMock()
    )
  assert ok_res == {"id": "analysis-alias-1"}

  with patch("gti_mcp.tools.files.vt_client") as mock_vt_blocked:
    blocked_res = await files.analyse_file(
        str(alias_upload_dir / "linked.bin"), ctx=MagicMock()
    )
  assert "error" in blocked_res
  assert "Symlinks are not allowed" in blocked_res["error"]
  mock_vt_blocked.assert_not_called()


@pytest.mark.asyncio(loop_scope="session")
async def test_rejects_directory_targets(tmp_path):
  """Passing '.' or a subdirectory inside upload_dir is rejected cleanly."""
  sub_dir = tmp_path / "subdir"
  sub_dir.mkdir()
  os.environ["GTI_ALLOWED_UPLOAD_DIR"] = str(tmp_path)
  files._register_upload_tools(server)

  with patch("gti_mcp.tools.files.vt_client") as mock_vt:
    res_root = await files.analyse_file(".", ctx=MagicMock())
    res_sub = await files.analyse_file("subdir", ctx=MagicMock())

  assert "error" in res_root
  assert "error" in res_sub
  mock_vt.assert_not_called()


def test_fresh_module_startup_registration_unset_vs_set(tmp_path):
  """Fresh server.py startup omits analyse_file until GTI_ALLOWED_UPLOAD_DIR is set."""
  import runpy
  import sys

  import gti_mcp.server as server_mod

  server_path = os.path.abspath(server_mod.__file__)
  saved_modules = {
      name: mod
      for name, mod in list(sys.modules.items())
      if name == "gti_mcp" or name.startswith("gti_mcp.")
  }

  def _run_fresh_server(upload_dir_val):
    started = []

    def fake_run(self, *args, **kwargs):
      started.append(self)

    if upload_dir_val is None:
      os.environ.pop("GTI_ALLOWED_UPLOAD_DIR", None)
    else:
      os.environ["GTI_ALLOWED_UPLOAD_DIR"] = upload_dir_val

    try:
      for name in list(sys.modules):
        if name == "gti_mcp" or name.startswith("gti_mcp."):
          sys.modules.pop(name, None)
      with patch("mcp.server.fastmcp.FastMCP.run", new=fake_run):
        runpy.run_path(server_path, run_name="__main__")
      assert len(started) == 1
      return set(started[0]._tool_manager._tools.keys())
    finally:
      for name in list(sys.modules):
        if name == "gti_mcp" or name.startswith("gti_mcp."):
          sys.modules.pop(name, None)
      sys.modules.update(saved_modules)

  unset_tools = _run_fresh_server(None)
  assert "analyse_file" not in unset_tools

  set_tools = _run_fresh_server(str(tmp_path))
  assert "analyse_file" in set_tools
  assert set_tools - unset_tools == {"analyse_file"}


def test_basename_file_reader_aiohttp_payload_size_and_seek(tmp_path):
  """_BasenameFileReader delegates fileno/seekable/tell/seek so aiohttp computes Content-Length."""
  sample_content = b"payload-for-aiohttp-multipart-size-check"
  sample_file = tmp_path / "nested" / "artifact.bin"
  sample_file.parent.mkdir(parents=True)
  sample_file.write_bytes(sample_content)

  raw_file, safe_name = files._open_confined_upload_file(
      "nested/artifact.bin", tmp_path
  )
  wrapped = files._BasenameFileReader(raw_file, safe_name)
  with wrapped:
    assert wrapped.name == "artifact.bin"
    assert wrapped.readable() is True
    assert wrapped.seekable() is True
    assert wrapped.tell() == 0
    assert os.fstat(wrapped.fileno()).st_size == len(sample_content)

    part = aiohttp.get_payload(wrapped)
    assert part.size == len(sample_content)

    form = aiohttp.MultipartWriter("form-data")
    form.append_payload(part)
    assert form.size is not None
    assert form.size > len(sample_content)

    assert wrapped.read(7) == b"payload"
    assert wrapped.tell() == 7
    assert wrapped.seek(0) == 0
    assert wrapped.readline() == sample_content


@pytest.mark.asyncio(loop_scope="session")
async def test_end_to_end_scan_file_async_http_upload_and_redirect(
    tmp_path, make_httpserver_ipv4
):
  """Unmocked vt.Client.scan_file_async sends Content-Length, safe basename, and survives 307 redirect."""
  os.environ["GTI_ALLOWED_UPLOAD_DIR"] = str(tmp_path)
  files._register_upload_tools(server)

  nested_dir = tmp_path / "subdir"
  nested_dir.mkdir()
  sample_content = b"redirect-resilient-upload-bytes-0123456789"
  (nested_dir / "report_sample.bin").write_bytes(sample_content)

  observed_posts = []
  redirect_target = make_httpserver_ipv4.url_for("/upload_target_final")

  def redirect_handler(request: Request) -> Response:
    observed_posts.append({
        "path": request.path,
        "content_length": request.headers.get("Content-Length"),
        "transfer_encoding": request.headers.get("Transfer-Encoding"),
        "body": request.get_data(),
    })
    return Response("", status=307, headers={"Location": redirect_target})

  def final_upload_handler(request: Request) -> Response:
    observed_posts.append({
        "path": request.path,
        "content_length": request.headers.get("Content-Length"),
        "transfer_encoding": request.headers.get("Transfer-Encoding"),
        "body": request.get_data(),
    })
    return Response(
        '{"data": {"id": "u-analysis-307", "type": "analysis"}}',
        status=200,
        content_type="application/json",
    )

  make_httpserver_ipv4.expect_oneshot_request(
      "/api/v3/files/upload_url", method="GET"
  ).respond_with_json(
      {"data": make_httpserver_ipv4.url_for("/upload_step_1")}
  )
  make_httpserver_ipv4.expect_oneshot_request(
      "/upload_step_1", method="POST"
  ).respond_with_handler(redirect_handler)
  make_httpserver_ipv4.expect_oneshot_request(
      "/upload_target_final", method="POST"
  ).respond_with_handler(final_upload_handler)
  make_httpserver_ipv4.expect_oneshot_request(
      "/api/v3/analyses/u-analysis-307", method="GET"
  ).respond_with_json(
      {
          "data": {
              "id": "u-analysis-307",
              "type": "analysis",
              "attributes": {"status": "completed"},
          }
      }
  )

  res = await files.analyse_file("subdir/report_sample.bin", ctx=MagicMock())
  assert res == {
      "id": "u-analysis-307",
      "type": "analysis",
      "attributes": {"status": "completed"},
  }
  assert len(observed_posts) == 2
  for post in observed_posts:
    assert post["content_length"] is not None
    assert int(post["content_length"]) > len(sample_content)
    assert post["transfer_encoding"] is None
    assert b'filename="report_sample.bin"' in post["body"]
    assert str(tmp_path).encode() not in post["body"]
    assert b"subdir" not in post["body"]
    assert sample_content in post["body"]


@pytest.mark.asyncio(loop_scope="session")
async def test_rejects_trailing_separator_and_file_as_parent_dir(tmp_path):
  """Trailing separators and regular files used as parent directories fail closed with accurate errors."""
  os.environ["GTI_ALLOWED_UPLOAD_DIR"] = str(tmp_path)
  files._register_upload_tools(server)

  sample_file = tmp_path / "sample.bin"
  sample_file.write_bytes(b"data")
  sub_dir = tmp_path / "subdir"
  sub_dir.mkdir()

  with patch("gti_mcp.tools.files.vt_client") as mock_vt:
    for trailing in ("sample.bin/", "sample.bin\\", "subdir/"):
      res = await files.analyse_file(trailing, ctx=MagicMock())
      assert res == {"error": "Path must not end with a directory separator"}

    res_parent_file = await files.analyse_file(
        "sample.bin/child.bin", ctx=MagicMock()
    )
    assert res_parent_file == {
        "error": "Path component in directory path is not a directory"
    }

  mock_vt.assert_not_called()


def test_non_posix_fallback_branch_parity(tmp_path, monkeypatch):
  """Fallback branch without O_NOFOLLOW rejects parent symlinks/junctions, non-dir parents, and non-regular fds."""
  monkeypatch.delattr(files.os, "O_NOFOLLOW", raising=False)

  upload_dir = tmp_path / "uploads"
  upload_dir.mkdir()
  nested_dir = upload_dir / "real_sub"
  nested_dir.mkdir()
  inside_file = nested_dir / "inside.bin"
  inside_file.write_bytes(b"inside-bytes")

  # 1. Valid regular file works on fallback branch
  raw_ok, safe_ok = files._open_confined_upload_file(
      "real_sub/inside.bin", upload_dir
  )
  with raw_ok:
    assert safe_ok == "inside.bin"
    assert raw_ok.read() == b"inside-bytes"

  # 2. Intermediate symlink pointing inside allowed_dir is rejected
  sym_sub = upload_dir / "sym_sub"
  sym_sub.symlink_to(nested_dir)
  with pytest.raises(
      PermissionError, match="Symlinks are not allowed in directory path"
  ):
    files._open_confined_upload_file("sym_sub/inside.bin", upload_dir)

  # 3. Leaf symlink pointing inside allowed_dir is rejected
  sym_leaf = upload_dir / "sym_leaf.bin"
  sym_leaf.symlink_to(inside_file)
  with pytest.raises(PermissionError, match="Symlinks are not allowed"):
    files._open_confined_upload_file("sym_leaf.bin", upload_dir)

  # 4. Regular file used as parent directory is rejected accurately
  with pytest.raises(
      ValueError, match="Path component in directory path is not a directory"
  ):
    files._open_confined_upload_file(
        "real_sub/inside.bin/grandchild.bin", upload_dir
    )

  # 5. Simulated Windows junction reparse tag on intermediate directory is rejected
  real_lstat = os.lstat

  class _FakeJunctionStat:

    def __init__(self, orig):
      self.st_mode = orig.st_mode
      self.st_reparse_tag = 0xA0000003  # IO_REPARSE_TAG_MOUNT_POINT

  def fake_lstat(target_path, *args, **kwargs):
    orig = real_lstat(target_path, *args, **kwargs)
    if pathlib.Path(target_path) == nested_dir:
      return _FakeJunctionStat(orig)
    return orig

  with patch("gti_mcp.tools.files.os.lstat", side_effect=fake_lstat):
    with pytest.raises(
        PermissionError, match="Symlinks are not allowed in directory path"
    ):
      files._open_confined_upload_file("real_sub/inside.bin", upload_dir)

  # 6. Post-open fstat non-regular file closes handle and raises ValueError
  closed_handles = []
  real_open = open

  def tracking_open(*args, **kwargs):
    fh = real_open(*args, **kwargs)
    orig_close = fh.close

    def wrapped_close():
      closed_handles.append(True)
      return orig_close()

    fh.close = wrapped_close
    return fh

  fake_fifo_stat = MagicMock()
  fake_fifo_stat.st_mode = stat.S_IFIFO | 0o600
  with (
      patch("builtins.open", side_effect=tracking_open),
      patch("gti_mcp.tools.files.os.fstat", return_value=fake_fifo_stat),
  ):
    with pytest.raises(ValueError, match="Path is not a regular file"):
      files._open_confined_upload_file("real_sub/inside.bin", upload_dir)
  assert closed_handles == [True]


@pytest.mark.asyncio(loop_scope="session")
async def test_error_logging_emitted_at_default_server_log_level(
    tmp_path, caplog
):
  """Config and upload-rejection failures log at ERROR so default server logging emits them."""
  caplog.set_level(logging.ERROR, logger="gti_mcp.tools.files")

  os.environ["GTI_ALLOWED_UPLOAD_DIR"] = "relative/invalid"
  with pytest.raises(ValueError):
    files._register_upload_tools(server)
  assert any(
      rec.levelno == logging.ERROR and "Failed to configure" in rec.message
      for rec in caplog.records
  )
  caplog.clear()

  # Runtime invalid GTI_ALLOWED_UPLOAD_DIR emits ERROR matching "check server logs"
  res_cfg = await files.analyse_file("sample.bin", ctx=MagicMock())
  assert "check server logs" in res_cfg["error"]
  assert any(
      rec.levelno == logging.ERROR
      and "Invalid GTI_ALLOWED_UPLOAD_DIR configuration" in rec.message
      for rec in caplog.records
  )
  caplog.clear()

  # Rejected upload emits ERROR
  os.environ["GTI_ALLOWED_UPLOAD_DIR"] = str(tmp_path)
  files._register_upload_tools(server)
  await files.analyse_file("../outside.bin", ctx=MagicMock())
  assert any(
      rec.levelno == logging.ERROR and "Rejected upload attempt" in rec.message
      for rec in caplog.records
  )


def test_register_upload_tools_uses_public_fastmcp_methods(tmp_path):
  """_register_upload_tools uses public add_tool/remove_tool without touching _tool_manager."""

  class _PublicOnlyServerStub:

    def __init__(self):
      self.registered = {}

    def add_tool(self, fn):
      self.registered[fn.__name__] = fn

    def remove_tool(self, name: str):
      if name not in self.registered:
        raise ToolError(f"Unknown tool: {name}")
      del self.registered[name]

  stub = _PublicOnlyServerStub()
  assert not hasattr(stub, "_tool_manager")

  os.environ.pop("GTI_ALLOWED_UPLOAD_DIR", None)
  assert files._register_upload_tools(stub) is False
  assert "analyse_file" not in stub.registered

  os.environ["GTI_ALLOWED_UPLOAD_DIR"] = str(tmp_path)
  assert files._register_upload_tools(stub) is True
  assert "analyse_file" in stub.registered

  # Idempotent re-registration when already registered
  assert files._register_upload_tools(stub) is True
  assert "analyse_file" in stub.registered

  # Invalid config removes previously registered tool and raises ValueError
  os.environ["GTI_ALLOWED_UPLOAD_DIR"] = "relative/path"
  with pytest.raises(ValueError):
    files._register_upload_tools(stub)
  assert "analyse_file" not in stub.registered


def test_no_private_or_exception_symbols_reexported_in_tools_namespace():
  """Wildcard import in gti_mcp.tools does not leak ToolError or private upload helpers."""
  exported = set(dir(tools))
  assert "ToolError" not in exported
  assert "_BasenameFileReader" in dir(files)
  for helper in (
      "_BasenameFileReader",
      "_is_symlink_or_junction",
      "_open_confined_upload_file",
      "_register_upload_tools",
      "_remove_upload_tool",
      "_resolve_allowed_upload_dir",
      "_sanitize_upload_filename",
  ):
    assert helper not in [name for name in exported if not name.startswith("_")]
