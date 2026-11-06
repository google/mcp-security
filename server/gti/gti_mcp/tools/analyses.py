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
import io
import logging
import os
import typing

from mcp.server.fastmcp import Context
import vt

from .. import utils
from ..server import server, vt_client


logger = logging.getLogger(__name__)

__all__ = [
    "get_analysis",
    "reanalyze_domain",
    "reanalyze_file",
    "reanalyze_ip",
    "reanalyze_url",
    "submit_file",
    "submit_url",
]


class _BasenameFileReader(io.IOBase):
  """Streams a binary file while exposing only its basename on `.name`."""

  def __init__(self, raw_file: typing.BinaryIO, basename: str):
    self._raw = raw_file
    self.name = basename

  def read(self, size: int = -1) -> bytes:
    return self._raw.read(size)

  def readable(self) -> bool:
    return True

  def close(self) -> None:
    try:
      self._raw.close()
    finally:
      super().close()


async def _post_reanalysis(
    client: vt.Client, endpoint: str, resource_label: str, resource_id: str
) -> typing.Dict[str, typing.Any]:
  """Triggers a POST reanalysis endpoint and returns the analysis descriptor."""
  try:
    response = await client.post_async(endpoint)
    if 200 <= response.status < 300:
      payload = await response.json_async()
      data = payload.get("data", payload) if isinstance(payload, dict) else payload
      return utils.sanitize_response(data)

    api_error = await client.get_error_async(response)
    if api_error is not None:
      logger.warning(
          "VirusTotal API error reanalyzing %s %s: %s - %s",
          resource_label,
          resource_id,
          api_error.code,
          api_error.message,
      )
      return {
          "error": (
              f"VirusTotal API Error: {api_error.code} - {api_error.message}"
          )
      }

    body_text = await response.text_async()
    logger.warning(
        "Unexpected HTTP %s reanalyzing %s %s: %s",
        response.status,
        resource_label,
        resource_id,
        body_text,
    )
    return {
        "error": (
            f"Unexpected HTTP {response.status} while reanalyzing"
            f" {resource_label}."
        )
    }
  except vt.error.APIError as err:
    logger.warning(
        "VirusTotal API error reanalyzing %s %s: %s - %s",
        resource_label,
        resource_id,
        err.code,
        err.message,
    )
    return {"error": f"VirusTotal API Error: {err.code} - {err.message}"}
  except Exception as err:  # pylint: disable=broad-exception-caught
    logger.error(
        "Unexpected error reanalyzing %s %s: %s",
        resource_label,
        resource_id,
        err,
        exc_info=True,
    )
    return {"error": f"Unexpected error reanalyzing {resource_label}: {err}"}


def _serialize_analysis_descriptor(
    analysis: vt.Object,
) -> typing.Dict[str, typing.Any]:
  """Serializes a vt.Object analysis descriptor without empty attributes."""
  analysis_dict = analysis.to_dict()
  analysis_dict["id"] = analysis.id
  if not analysis_dict.get("attributes"):
    analysis_dict.pop("attributes", None)
  return utils.sanitize_response(analysis_dict)


@server.tool()
async def submit_file(
    file_path: str, ctx: Context
) -> typing.Dict[str, typing.Any]:
  """Upload a local file to Google Threat Intelligence / VirusTotal for scanning.

  Unlike `analyse_file`, this tool returns the queued analysis descriptor
  immediately without blocking on scan completion; pass the returned `id` to
  `get_analysis` to check progress and retrieve results.

  WARNING: Standard VirusTotal file submissions are shared with the security
  community. Confirm explicit authorization before uploading potentially
  sensitive or proprietary files.

  Args:
    file_path (required): Path to the local file to upload and scan.

  Returns:
    Analysis descriptor containing the `id` and `type` ("analysis").
  """
  resolved_path = os.path.expanduser(file_path)
  if not os.path.isfile(resolved_path):
    logger.warning("Cannot submit missing local file: %s", file_path)
    return {"error": f"File not found: {file_path}"}

  basename = os.path.basename(resolved_path)
  try:
    async with vt_client(ctx) as client:
      with open(resolved_path, "rb") as raw_file:
        wrapped = _BasenameFileReader(raw_file, basename)
        analysis = await client.scan_file_async(
            file=wrapped, wait_for_completion=False
        )
    return _serialize_analysis_descriptor(analysis)
  except vt.error.APIError as err:
    logger.warning(
        "VirusTotal API error submitting file %s: %s - %s",
        basename,
        err.code,
        err.message,
    )
    return {"error": f"VirusTotal API Error: {err.code} - {err.message}"}
  except OSError as err:
    logger.error("OS error reading file %s: %s", basename, err, exc_info=True)
    return {"error": f"Failed to read file '{file_path}': {err}"}
  except Exception as err:  # pylint: disable=broad-exception-caught
    logger.error(
        "Unexpected error submitting file %s: %s", basename, err, exc_info=True
    )
    return {"error": f"Unexpected error submitting file: {err}"}


@server.tool()
async def reanalyze_file(
    hash: str, ctx: Context
) -> typing.Dict[str, typing.Any]:
  """Request a fresh reanalysis of a file already present in VirusTotal by hash.

  Args:
    hash (required): MD5, SHA-1, or SHA-256 hash of the file to reanalyze.

  Returns:
    Analysis descriptor containing the queued analysis `id` for `get_analysis`.
  """
  async with vt_client(ctx) as client:
    return await _post_reanalysis(client, f"/files/{hash}/analyse", "file", hash)


@server.tool()
async def submit_url(url: str, ctx: Context) -> typing.Dict[str, typing.Any]:
  """Submit a URL to Google Threat Intelligence / VirusTotal for scanning.

  Returns the queued analysis descriptor immediately; pass the returned `id`
  to `get_analysis` to check scan status and verdicts.

  Args:
    url (required): The URL to submit for scanning.

  Returns:
    Analysis descriptor containing the `id` and `type` ("analysis").
  """
  try:
    async with vt_client(ctx) as client:
      analysis = await client.scan_url_async(url, wait_for_completion=False)
    return _serialize_analysis_descriptor(analysis)
  except vt.error.APIError as err:
    logger.warning(
        "VirusTotal API error submitting URL %s: %s - %s",
        url,
        err.code,
        err.message,
    )
    return {"error": f"VirusTotal API Error: {err.code} - {err.message}"}
  except Exception as err:  # pylint: disable=broad-exception-caught
    logger.error(
        "Unexpected error submitting URL %s: %s", url, err, exc_info=True
    )
    return {"error": f"Unexpected error submitting URL: {err}"}


@server.tool()
async def reanalyze_url(url: str, ctx: Context) -> typing.Dict[str, typing.Any]:
  """Request a fresh reanalysis of an existing URL in Google Threat Intelligence.

  Args:
    url (required): The URL to reanalyze.

  Returns:
    Analysis descriptor containing the queued analysis `id` for `get_analysis`.
  """
  encoded_id = vt.url_id(url)
  async with vt_client(ctx) as client:
    return await _post_reanalysis(
        client, f"/urls/{encoded_id}/analyse", "url", url
    )


@server.tool()
async def reanalyze_domain(
    domain: str, ctx: Context
) -> typing.Dict[str, typing.Any]:
  """Trigger a fresh reanalysis and reputation refresh for a domain.

  Args:
    domain (required): Domain name to reanalyze (e.g., 'example.com').

  Returns:
    Analysis descriptor containing the queued analysis `id` for `get_analysis`.
  """
  async with vt_client(ctx) as client:
    return await _post_reanalysis(
        client, f"/domains/{domain}/analyse", "domain", domain
    )


@server.tool()
async def reanalyze_ip(
    ip_address: str, ctx: Context
) -> typing.Dict[str, typing.Any]:
  """Trigger a fresh reanalysis and reputation refresh for an IPv4 or IPv6 address.

  Args:
    ip_address (required): IPv4 or IPv6 address to reanalyze.

  Returns:
    Analysis descriptor containing the queued analysis `id` for `get_analysis`.
  """
  async with vt_client(ctx) as client:
    return await _post_reanalysis(
        client, f"/ip_addresses/{ip_address}/analyse", "ip_address", ip_address
    )


@server.tool()
async def get_analysis(
    analysis_id: str, ctx: Context, include_engine_results: bool = False
) -> typing.Dict[str, typing.Any]:
  """Retrieve the status, summary stats, and metadata of a file or URL analysis.

  By default, per-engine AV/scanner entries (`attributes.results`) are omitted
  to keep responses concise while preserving `status` (`queued`, `in-progress`,
  or `completed`), `stats`, `date`, and `meta` (`file_info` / `url_info`).

  Args:
    analysis_id (required): Analysis identifier returned by `submit_file`,
      `submit_url`, or any `reanalyze_*` tool.
    include_engine_results: Set to True to include full per-engine `results`.
      Defaults to False.

  Returns:
    Analysis object dictionary with `id`, `type`, `attributes`, and `meta`.
  """
  try:
    async with vt_client(ctx) as client:
      payload = await client.get_json_async(f"/analyses/{analysis_id}")
  except vt.error.APIError as err:
    logger.warning(
        "VirusTotal API error fetching analysis %s: %s - %s",
        analysis_id,
        err.code,
        err.message,
    )
    return {
        "error": f"VirusTotal API Error: {err.code} - {err.message}",
        "details": (
            f"The requested analysis '{analysis_id}' could not be found or"
            " there was an issue with the API request."
        ),
    }
  except Exception as err:  # pylint: disable=broad-exception-caught
    logger.error(
        "Unexpected error fetching analysis %s: %s",
        analysis_id,
        err,
        exc_info=True,
    )
    return {"error": f"Unexpected error fetching analysis: {err}"}

  data = payload.get("data", {}) if isinstance(payload, dict) else {}
  if not isinstance(data, dict) or not data:
    logger.warning("Unexpected analysis response for %s: %s", analysis_id, payload)
    return {"error": "Unexpected response format from VirusTotal API."}

  attributes = dict(data.get("attributes", {}))
  if not include_engine_results:
    attributes.pop("results", None)

  result: typing.Dict[str, typing.Any] = {
      "id": data.get("id", analysis_id),
      "type": data.get("type", "analysis"),
      "attributes": attributes,
  }
  if isinstance(payload.get("meta"), dict) and payload["meta"]:
    result["meta"] = payload["meta"]

  return utils.sanitize_response(result)
