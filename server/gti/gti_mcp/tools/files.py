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
import errno
import io
import json
import logging
import os
import pathlib
import stat
import typing
import unicodedata
import urllib.parse

import vt
from mcp.server.fastmcp import Context
from mcp.server.fastmcp.exceptions import ToolError as _ToolError

from .. import utils
from ..server import server, vt_client

_UPLOAD_DIR_ENV_VAR = "GTI_ALLOWED_UPLOAD_DIR"
_REPARSE_TAG_MOUNT_POINT = getattr(
    stat, "IO_REPARSE_TAG_MOUNT_POINT", 0xA0000003
)
_REPARSE_TAG_SYMLINK = getattr(stat, "IO_REPARSE_TAG_SYMLINK", 0xA000000C)
_logger = logging.getLogger(__name__)


def _is_symlink_or_junction(
    path_obj: pathlib.Path, st: os.stat_result
) -> bool:
  """Returns True if path_obj or its lstat result is a symlink or junction."""
  if stat.S_ISLNK(st.st_mode) or path_obj.is_symlink():
    return True
  reparse_tag = getattr(st, "st_reparse_tag", 0)
  if reparse_tag in (_REPARSE_TAG_MOUNT_POINT, _REPARSE_TAG_SYMLINK):
    return True
  is_junction = getattr(path_obj, "is_junction", None)
  if callable(is_junction) and is_junction():
    return True
  return False


def _sanitize_upload_filename(file_name: str, default: str = "submission.bin") -> str:
  """Normalizes an uploaded file name to a safe basename."""
  if not file_name:
    return default
  tail = file_name.replace("\\", "/").rsplit("/", maxsplit=1)[-1].strip()
  if (
      not tail
      or tail in {".", ".."}
      or len(tail) > 255
      or '"' in tail
      or "\\" in tail
      or any(unicodedata.category(ch).startswith("C") for ch in tail)
  ):
    return default
  return tail


class _BasenameFileReader(io.IOBase):
  """Binary file reader wrapper that exposes only a sanitized basename."""

  def __init__(self, raw_file: typing.BinaryIO, basename: str):
    super().__init__()
    self._raw = raw_file
    self.name = basename

  def readable(self) -> bool:
    return self._raw.readable()

  def seekable(self) -> bool:
    return self._raw.seekable()

  def fileno(self) -> int:
    return self._raw.fileno()

  def tell(self) -> int:
    return self._raw.tell()

  def seek(self, offset: int, whence: int = io.SEEK_SET) -> int:
    return self._raw.seek(offset, whence)

  def read(self, size: int = -1) -> bytes:
    return self._raw.read(size)

  def readline(self, size: int | None = -1) -> bytes:
    return self._raw.readline(-1 if size is None else size)

  def close(self) -> None:
    try:
      self._raw.close()
    finally:
      super().close()


def _resolve_allowed_upload_dir() -> pathlib.Path | None:
  """Resolves and validates the configured upload directory."""
  raw_dir = os.getenv(_UPLOAD_DIR_ENV_VAR, "").strip()
  if not raw_dir:
    return None

  if any(ord(ch) < 32 or ord(ch) == 127 for ch in raw_dir):
    raise ValueError(f"{_UPLOAD_DIR_ENV_VAR} must not contain control characters")

  expanded = pathlib.Path(raw_dir).expanduser()
  if not expanded.is_absolute():
    raise ValueError(
        f"{_UPLOAD_DIR_ENV_VAR} must be an absolute path to an existing directory: '{raw_dir}'"
    )

  try:
    resolved = expanded.resolve(strict=True)
  except (OSError, RuntimeError) as e:
    raise ValueError(
        f"{_UPLOAD_DIR_ENV_VAR} path does not exist or cannot be resolved: '{raw_dir}': {e}"
    ) from e

  if not resolved.is_dir():
    raise ValueError(f"{_UPLOAD_DIR_ENV_VAR} must be a directory: '{resolved}'")

  if resolved == resolved.parent or resolved == pathlib.Path(resolved.anchor):
    raise ValueError(f"{_UPLOAD_DIR_ENV_VAR} cannot be the filesystem root: '{resolved}'")

  return resolved


def _open_confined_upload_file(
    user_path_str: str,
    allowed_dir: pathlib.Path,
    configured_dir: pathlib.Path | None = None,
) -> tuple[typing.BinaryIO, str]:
  """Opens a regular file within allowed_dir without following symlinks."""
  if not isinstance(user_path_str, str) or not user_path_str.strip():
    raise ValueError("file_path cannot be empty")
  stripped = user_path_str.strip()
  if "\0" in stripped or any(ord(ch) < 32 or ord(ch) == 127 for ch in stripped):
    raise ValueError("file_path contains invalid control characters or null bytes")

  pure_posix = pathlib.PurePosixPath(stripped)
  pure_win = pathlib.PureWindowsPath(stripped)
  if ".." in pure_posix.parts or ".." in pure_win.parts:
    raise PermissionError("Directory traversal with '..' is not allowed")

  cand = pathlib.Path(stripped)
  if not cand.is_absolute() and (
      pure_win.drive or pure_win.root or pure_posix.root
  ):
    raise PermissionError(
        "Drive-qualified or rooted relative paths are not allowed"
    )

  if cand.is_absolute():
    if cand.is_relative_to(allowed_dir):
      rel = cand.relative_to(allowed_dir)
    elif (
        configured_dir is not None
        and ".." not in configured_dir.parts
        and cand.is_relative_to(configured_dir)
    ):
      rel = cand.relative_to(configured_dir)
    else:
      raise PermissionError(
          "File path is outside the allowed GTI_ALLOWED_UPLOAD_DIR directory"
      )
  else:
    rel = cand

  if not rel.parts or rel == pathlib.Path("."):
    raise ValueError("Path is the allowed directory itself, not a regular file")
  if ".." in rel.parts:
    raise PermissionError("Directory traversal with '..' is not allowed")
  if stripped.endswith(("/", "\\")):
    raise ValueError("Path must not end with a directory separator")

  if hasattr(os, "O_NOFOLLOW") and hasattr(os, "O_DIRECTORY"):
    try:
      current_fd = os.open(
          str(allowed_dir), os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW
      )
    except OSError as e:
      raise PermissionError("Failed to open allowed upload directory") from e

    open_dir_fds = [current_fd]
    try:
      for part in rel.parent.parts:
        if not part or part == ".":
          continue
        if part == "..":
          raise PermissionError("Directory traversal with '..' is not allowed")
        try:
          next_fd = os.open(
              part,
              os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW,
              dir_fd=current_fd,
          )
          open_dir_fds.append(next_fd)
          current_fd = next_fd
        except OSError as e:
          if e.errno in (errno.ELOOP, getattr(errno, "EMLINK", errno.ELOOP)):
            raise PermissionError(
                "Symlinks are not allowed in directory path"
            ) from e
          if e.errno == errno.ENOTDIR:
            try:
              st_part = os.stat(
                  part, dir_fd=current_fd, follow_symlinks=False
              )
            except OSError:
              raise PermissionError(
                  "Path component is not a directory or is a symlink"
              ) from e
            if stat.S_ISLNK(st_part.st_mode):
              raise PermissionError(
                  "Symlinks are not allowed in directory path"
              ) from e
            raise ValueError(
                "Path component in directory path is not a directory"
            ) from e
          raise

      try:
        file_fd = os.open(
            rel.name,
            os.O_RDONLY | os.O_NOFOLLOW | getattr(os, "O_NONBLOCK", 0),
            dir_fd=current_fd,
        )
      except OSError as e:
        if e.errno in (errno.ELOOP, getattr(errno, "EMLINK", errno.ELOOP)):
          raise PermissionError("Symlinks are not allowed") from e
        if e.errno == errno.EISDIR:
          raise ValueError("Path is not a regular file") from e
        raise

      fd_owned = True
      try:
        st = os.fstat(file_fd)
        if not stat.S_ISREG(st.st_mode):
          raise ValueError("Path is not a regular file")
        if hasattr(os, "set_blocking"):
          os.set_blocking(file_fd, True)
        raw_file = open(file_fd, "rb", closefd=True)
        fd_owned = False
      except Exception:
        if fd_owned:
          try:
            os.close(file_fd)
          except OSError:
            pass
        raise
    finally:
      for dfd in open_dir_fds:
        try:
          os.close(dfd)
        except OSError:
          pass
  else:
    try:
      st_root = os.lstat(allowed_dir)
    except OSError as e:
      raise PermissionError("Failed to open allowed upload directory") from e
    if _is_symlink_or_junction(allowed_dir, st_root) or not stat.S_ISDIR(
        st_root.st_mode
    ):
      raise PermissionError("Failed to open allowed upload directory")

    current_dir = allowed_dir
    for part in rel.parent.parts:
      if not part or part == ".":
        continue
      if part == "..":
        raise PermissionError("Directory traversal with '..' is not allowed")
      current_dir = current_dir / part
      try:
        st_part = os.lstat(current_dir)
      except OSError as e:
        if e.errno == errno.ENOTDIR:
          raise ValueError(
              "Path component in directory path is not a directory"
          ) from e
        raise
      if _is_symlink_or_junction(current_dir, st_part):
        raise PermissionError("Symlinks are not allowed in directory path")
      if not stat.S_ISDIR(st_part.st_mode):
        raise ValueError("Path component in directory path is not a directory")

    candidate_target = current_dir / rel.name
    try:
      st_leaf = os.lstat(candidate_target)
    except OSError as e:
      if e.errno == errno.ENOTDIR:
        raise ValueError(
            "Path component in directory path is not a directory"
        ) from e
      raise
    if _is_symlink_or_junction(candidate_target, st_leaf):
      raise PermissionError("Symlinks are not allowed")
    if not stat.S_ISREG(st_leaf.st_mode):
      raise ValueError("Path is not a regular file")

    target = candidate_target.resolve(strict=True)
    if not target.is_relative_to(allowed_dir):
      raise PermissionError(
          "File path is outside the allowed GTI_ALLOWED_UPLOAD_DIR directory"
      )
    if target == allowed_dir:
      raise ValueError("Path is not a regular file")

    raw_file = open(target, "rb")
    try:
      st_open = os.fstat(raw_file.fileno())
      if not stat.S_ISREG(st_open.st_mode):
        raise ValueError("Path is not a regular file")
    except Exception:
      try:
        raw_file.close()
      except OSError:
        pass
      raise

  safe_name = _sanitize_upload_filename(rel.name, default="submission.bin")
  return raw_file, safe_name


FILE_RELATIONSHIPS = [
    "analyses",
    "associations",
    "behaviours",
    "attack_techniques",
    "bundled_files",
    "campaigns",
    "carbonblack_children",
    "carbonblack_parents",
    "collections",
    "comments",
    "compressed_parents",
    "contacted_domains",
    "contacted_ips",
    "contacted_urls",
    "dropped_files",
    "email_attachments",
    "email_parents",
    "embedded_domains",
    "embedded_ips",
    "embedded_urls",
    "execution_parents",
    "graphs",
    "itw_domains",
    "itw_ips",
    "itw_urls",
    "malware_families",
    "memory_pattern_domains",
    "memory_pattern_ips",
    "memory_pattern_urls",
    "overlay_children",
    "overlay_parents",
    "pcap_children",
    "pcap_parents",
    "pe_resource_children",
    "pe_resource_parents",
    "related_attack_techniques",
    "related_reports",
    "related_threat_actors",
    "reports",
    "screenshots",
    "similar_files",
    "software_toolkits",
    "submissions",
    "urls_for_embedded_js",
    "user_votes",
    "votes",
    "vulnerabilities",
]

FILE_KEY_RELATIONSHIPS = [
    "contacted_domains",
    "contacted_ips",
    "contacted_urls",
    "dropped_files",
    "embedded_domains",
    "embedded_ips",
    "embedded_urls",
    "associations",
]


@server.tool()
async def get_file_report(hash: str, ctx: Context) -> typing.Dict[str, typing.Any]:  # noqa: UP006 - typing.Dict keeps FastMCP {"result": ...} outputSchema
  """Get a comprehensive file analysis report using its hash (MD5/SHA-1/SHA-256).

  Returns a concise summary of key threat details including
  detection stats, threat classification, and important indicators.
  Parameters:
    hash (required): The MD5, SHA-1, or SHA-256 hash of the file to analyze.
  Example: '8ab2cf...', 'e4d909c290d0...', etc.
  """
  async with vt_client(ctx) as client:
    res = await utils.fetch_object(
        client,
        "files",
        "file",
        hash,
        relationships=FILE_KEY_RELATIONSHIPS,
        params={"exclude_attributes": "last_analysis_results"}
    )
  return utils.sanitize_response(res)


@server.tool()
async def get_entities_related_to_a_file(
    hash: str, relationship_name: str, descriptors_only: bool, ctx: Context, limit: int = 10,
) -> list[dict[str, typing.Any]] | dict[str, str]:
    """Retrieve entities related to the the given file hash.

    The following table shows a summary of available relationships for file objects.

    | Relationship           | Description                                                                       | Return type |
    | ---------------------- | --------------------------------------------------------------------------------- | ----------- |
    | analyses               | Analyses for the file                                                             | analysis |
    | associations           | File's associated objects (reports, campaigns, IoC collections, malware families, software toolkits, vulnerabilities, threat-actors), without filtering by the associated object type.                                                                                      | collection |
    | behaviours             | Behaviour reports for the file.                                                   | file-behaviour |
    | attack_techniques      | Returns the Attack Techniques of the File.                                        | attack_technique |
    | bundled_files          | Files bundled within the file.                                                    | file |
    | campaigns              | Campaigns associated to the file.                                                 | collection |
    | carbonblack_children   | Files derived from the file according to Carbon Black.                            | file |
    | carbonblack_parents    | Files from where the file was derived according to Carbon Black.                  | file |
    | collections            | IoC Collections associated to the file.                                           | collection |
    | comments               | Comments for the file.                                                            | comment |
    | compressed_parents     | Compressed files that contain the file.                                           | file |
    | contacted_domains      | Domains contacted by the file.                                                    | domain |
    | contacted_ips          | IP addresses contacted by the file.                                               | ip_address |
    | contacted_urls         | URLs contacted by the file.                                                       | url |
    | dropped_files          | Files dropped by the file during its execution.                                   | file |
    | email_attachments      | Files attached to the email.                                                      | file |
    | email_parents          | Email files that contained the file.                                              | file |
    | embedded_domains       | Domain names embedded in the file.                                                | domain |
    | embedded_ips           | IP addresses embedded in the file.                                                | ip_address |
    | embedded_urls          | URLs embedded in the file.                                                        | url |
    | execution_parents      | Files that executed the file.                                                     | file |
    | graphs                 | Graphs that include the file.                                                     | graph |
    | itw_domains            | In the wild domain names from where the file has been downloaded.                 | domain |
    | itw_ips                | In the wild IP addresses from where the file has been downloaded.                 | ip_address |
    | itw_urls               | In the wild URLs from where the file has been downloaded.                         | url |
    | malware_families       | Malware families associated to the file.                                          | collection |
    | memory_pattern_domains | Domain string patterns found in memory during sandbox execution.                  | domain |
    | memory_pattern_ips     | IP address string patterns found in memory during sandbox execution.              | ip_address |
    | memory_pattern_urls    | URL string patterns found in memory during sandbox execution.                     | url |
    | overlay_children       | Files contained by the file as an overlay.                                        | file |
    | overlay_parents        | File that contain the file as an overlay.                                         | file |
    | pcap_children          | Files contained within the PCAP file.                                             | file |
    | pcap_parents           | PCAP files that contain the file.                                                 | file |
    | pe_resource_children   | Files contained by a PE file as a resource.                                       | file |
    | pe_resource_parents    | PE files containing the file as a resource.                                       | file |
    | related_attack_techniques    | Returns the Attack Techniques of the Collections containing this File.      | attack_technique |
    | related_reports        | Reports that are directly and indirectly related to the file.                     | collection |
    | related_threat_actors  | File's related threat actors.                                                     | collection |
    | reports                | Reports directly associated to the file.                                          | collection |
    | screenshots            | Screenshots related to the sandbox execution of the file.                         | screenshot |
    | similar_files          | Files that are similar to the file.                                               | file |
    | software_toolkits      | Software and Toolkits associated to the file.                                     | collection |
    | submissions            | Submissions for the file.                                                         | submission |
    | urls_for_embedded_js   | URLs where this (JS) file is embedded.                                            | url |
    | user_votes             | File's votes made by current signed-in user.                                      | vote |
    | votes                  | Votes for the file.                                                               | vote |
    | vulnerabilities        | Vulnerabilities associated to the file.                                           | collection |

    Args:
      hash (required): MD5/SHA1/SHA256) hash that identifies the file.
      relationship_name (required): Relationship name.
      descriptors_only (required): Bool. Must be True when the target object type is one of file, domain, url, ip_address or collection.
      limit: Limit the number of files to retrieve. 10 by default.
    Returns:
      List of objects related to the given file, or an error dictionary.
    """
    if not relationship_name in FILE_RELATIONSHIPS:
        return {
            "error": f"Relationship {relationship_name} does not exist. "
            f"Available relationships are: {','.join(FILE_RELATIONSHIPS)}"
        }

    async with vt_client(ctx) as client:
      res = await utils.fetch_object_relationships(
          client,
          "files",
          hash,
          relationships=[relationship_name],
          descriptors_only=descriptors_only,
          limit=limit)
    return utils.sanitize_response(res.get(relationship_name, []))


@server.tool()
async def get_file_behavior_report(
    file_behaviour_id: str, ctx: Context
) -> typing.Dict[str, typing.Any]:  # noqa: UP006 - typing.Dict keeps FastMCP {"result": ...} outputSchema
  """Retrieve the file behaviour report of the given file behaviour identifier.

  You can get all the file behaviour of a given a file by calling `get_entities_related_to_a_file` as the file hash and the `behaviours` as relationship name.

  The file behaviour ID is composed using the following pattern: "{file hash}_{sandbox name}".

  Args:
    file_behaviour_id (required): File behaviour ID.
  Returns:
    The file behaviour report.
  """
  async with vt_client(ctx) as client:
    res = await utils.fetch_object(
        client,
        "file_behaviours",
        "file_behaviour",
        file_behaviour_id,
        relationships=[
            "contacted_domains",
            "contacted_ips",
            "contacted_urls",
            "dropped_files",
            "embedded_domains",
            "embedded_ips",
            "embedded_urls",
            "associations",
        ],
    )
  return utils.sanitize_response(res)


@server.tool()
async def get_file_behavior_summary(hash: str, ctx: Context) -> typing.Dict[str, typing.Any]:  # noqa: UP006 - typing.Dict keeps FastMCP {"result": ...} outputSchema
  """Retrieve a summary of all the file behavior reports from all the sandboxes.

  Args:
    hash (required): MD5/SHA1/SHA256) hash that identifies the file.
  Returns:
    The file behavior summary.
  """
  async with vt_client(ctx) as client:
    res = await client.get_async(f"/files/{hash}/behaviour_summary")
    res = await res.json_async()

  if "data" not in res:
      if "error" in res:
          logging.warning(f"VirusTotal API Error: {res['error']}")
          return {"error": f"VirusTotal API Error: {res['error']}"}
      logging.warning(f"Unexpected response format from VirusTotal API: {res}")
      return {"error": f"Unexpected response format from VirusTotal API: {res}"}

  return utils.sanitize_response(res["data"])


async def analyse_file(
    file_path: str, ctx: Context
) -> typing.Dict[str, typing.Any]:  # noqa: UP006 - typing.Dict keeps FastMCP {"result": ...} outputSchema
  """Upload and analyse the file in VirusTotal.

  The file will be uploaded to VirusTotal and shared publicly with the community.
  Requires the GTI_ALLOWED_UPLOAD_DIR environment variable to be set to an
  allowed directory. Only regular files within this directory can be analyzed.

  Args:
    file_path (required): Path to the file for analysis, relative to or inside
      the allowed upload directory.
  Returns:
    The analysis report or an error dictionary.
  """
  try:
    allowed_dir = _resolve_allowed_upload_dir()
  except ValueError as e:
    _logger.error("Invalid %s configuration: %s", _UPLOAD_DIR_ENV_VAR, e)
    return {
        "error": (
            f"Invalid {_UPLOAD_DIR_ENV_VAR} configuration; check server logs."
        )
    }

  if allowed_dir is None:
    return {
        "error": (
            "analyse_file is disabled by default. Set the"
            f" {_UPLOAD_DIR_ENV_VAR} environment variable to an absolute"
            " directory path to enable file uploads."
        )
    }

  raw_configured = os.getenv(_UPLOAD_DIR_ENV_VAR, "").strip()
  configured_dir = (
      pathlib.Path(raw_configured).expanduser() if raw_configured else None
  )

  try:
    raw_file, safe_name = _open_confined_upload_file(
        file_path, allowed_dir, configured_dir=configured_dir
    )
  except (ValueError, PermissionError) as e:
    _logger.error("Rejected upload attempt: %s", e)
    return {"error": str(e)}
  except FileNotFoundError:
    _logger.error("Upload target not found within %s", _UPLOAD_DIR_ENV_VAR)
    return {"error": "File not found within GTI_ALLOWED_UPLOAD_DIR"}
  except OSError as e:
    _logger.error("OS error opening upload target: %s", e)
    return {"error": "Failed to open file for upload"}

  wrapped_reader = _BasenameFileReader(raw_file, safe_name)
  try:
    with wrapped_reader:
      async with vt_client(ctx) as client:
        try:
          analysis = await client.scan_file_async(file=wrapped_reader)
          _logger.info("File %s uploaded for analysis.", safe_name)
          res = await client.wait_for_analysis_completion(analysis)
          _logger.info("Analysis has completed with ID %s", res.id)
          return utils.sanitize_response(res.to_dict())
        except vt.error.APIError as e:
          _logger.error("VirusTotal API error during analysis: %s", e)
          return {"error": f"VirusTotal API Error: {e}"}
  finally:
    try:
      wrapped_reader.close()
    except Exception:
      pass

@server.tool()
async def search_digital_threat_monitoring(
    query: str,
    ctx: Context,
    size: int = 10,
    since: str | None = None,
    until: str | None = None,
    page: str | None = None,
    truncate: str | None = None,
    sanitize: bool = True,
) -> dict:
  """Search for historical data in Digital Threat Monitoring (DTM) using Lucene syntax.

  Digital theat monitoring is a collection of documents from surface, deep, and dark web sources.

  To filter by document type or threat type, include the conditions within the `query` string
  using the fields `__type` and `label_threat`, respectively. Combine multiple conditions
  using Lucene boolean operators (AND, OR, NOT).

  Examples of filtering in the query:
  - Single document type: `(__type:forum_post) AND (body:security)`
  - Multiple document types: `(__type:(forum_post OR paste)) AND (body:security)`
  - Single threat type: `(label_threat:information-security/malware) AND (body:exploit)`
  - Multiple threat types: `(label_threat:(information-security/malware OR information-security/phishing)) AND (body:exploit)`
  - Combined: `(__type:document_analysis) AND (label_threat:information-security/information-leak/credentials) AND (body:password)`

  Important Considerations for Effective Querying:

  -   **Date/Time Filtering (`since` and `until`)**:
    -   Input parameters `since` and `until` filter documents by their creation/modification time.
    -   These must be strings in RFC3339 format, specifically ending with 'Z' to denote UTC.
    -   Example: `'2025-04-23T00:00:00Z'`

  -   **Pagination for More Than 25 Results**:
      -   A single API call returns at most `size` results (maximum 25).
      -   To retrieve more results, you must paginate:
          1.  Make your initial search request.
          2.  The response dictionary will contain a key named `page`.
          3.  If this `page` key holds a non-empty string value, there are more results available.
          4.  To fetch the next page, make a subsequent API call. This call MUST include the *exact same parameters* as your original request (query, size, since, until, doc_type, etc.), PLUS the `page` parameter set to the token value received in the previous response's `page` field.
          5.  Continue this process, using the new `page` token from each response, until the `page` field is absent or empty in the response, indicating the end of the results.

  Tokenization:
  - DTM breaks documents into tokens.
  - Example: "some-domain.com" -> "some", "domain", "com".
  - Wildcard/Regex queries match single tokens, not phrases.

  Special Characters:
  - Escape with \: ` + - & | ! ( ) { } [ ] ^ " ~ * ? : / ` and space.
  - Example: To find "(1+1):2", query \(1\+1\)\:2

  Case Sensitivity:
  - DTM entity values are often lowercased.
  - Boolean operators (AND, OR, NOT) MUST be UPPERCASE.

  Domain Search Nuances:
  - Use wildcards/regex on fields like `doc.domain`.
  - Example: doc.domain:google.*.dev
  - Avoid pattern searches on `group_network`.

  Performance Limit:
  - Searches timeout after 60 seconds.
  - For broad or complex queries, it is highly recommended to use the `since` and `until` parameters to add time delimiters. This narrows the search scope and helps prevent timeouts.

  Noise Reduction:
  - Use typed entities for higher precision.
  - Example: organization:"Acme Corp"
  - Prefer typed entities over free text searches.
  
  The following fields and their meanings can be used to compose a query using Lucene syntax (including combining them with AND, OR, and NOT operators along with parentheses):
  * author.identity.name - The handle used by the forum post author
  * subject - The subject line of the forum post
  * body - The body text of the content
  * inet_location.url - What URL content was found 
  * language - The content language
  * title - The title of the web page 
  * channel.name - The Telegram channel name
  * domain - A DNS domain name
  * cve - A CVE entry by ID 

  __type: one of the following
  * web_content_publish - General website content
  * domain_discovery - Newly discovered domain names
  * forum_post - Darkweb forum posts
  * message - Chat messages like Telegram
  * paste - Paste site content like Pastebin
  * shop_listing - Items for sale on the dark web
  * email_analysis - Suspicious emails
  * tweet - Tweets from Twitter on cybersecurity topics.
  * document_analysis - Documents (PDF, Office, text) from VirusTotal, including malicious and corporate confidential files.

  label_threat: one of the following
  * information-security/anonymization - Anonymization
  * information-security/apt - Advanced Persistent Threat
  * information-security/botnet - Botnet
  * information-security/compromised - Compromised Infrastructure
  * information-security/doxing - Personal Information Disclosure
  * information-security/exploit - Exploits
  * information-security/phishing - Phishing
  * information-security/information-leak - Information Leak
  * information-security/information-leak/confidential - Confidential Information Leak
  * information-security/information-leak/credentials - Credential Leak
  * information-security/information-leak/payment-cards - Credit Card Leak
  * information-security/malicious-activity - Malicious Activity
  * information-security/malicious-infrastructure - Malicious Infrastructure
  * information-security/malware - Malware
  * information-security/malware/ransomware - Ransomware
  * information-security/malware/ransomware-victim-listing - Ransomware Victim Listing
  * information-security/security-research - Security Research
  * information-security/spam - Spam

  Args:
    query (required): The Lucene-like query string for your document search.
    size (optional): The number of results to return in each page (0 to 25). Defaults to 10.
    since (optional): The timestamp to search for documents since (RFC3339 format).
    until (optional): The timestamp to search for documents from (RFC3339 format).
    page (optional): The page ID to fetch the page for. This is only used when paginating through pages greater than the first page of results.
    truncate (optional): The number of characters (as a string) to truncate all documents fields in the response (e.g., '500').
    sanitize (optional): If true (default), any HTML content in the document fields are sanitized to remove links, scripts, etc.

  Returns:
    A dictionary containing the list of documents found and search metadata.
  """
  async with vt_client(ctx) as client:
    params = {
        "size": size,
        "since": since,
        "until": until,
        "page": page,
        "truncate": truncate,
        "sanitize": str(sanitize).lower(),
    }
    params = {k: v for k, v in params.items() if v is not None and v != ""}
    path = f"/dtm/docs/search?{urllib.parse.urlencode(params)}"

    try:
      res = await client.post_async(
          path=path, json_data={"query": query}
      )

      if "text/html" in res.headers.get("Content-Type", ""):
        response_text = await res.text_async()
        if "request timed out" in response_text.lower():
          return {"error": "The request timed out. Please try reducing the scope of your query by using `since` and `until` parameters to add time delimiters"}
        logging.error(response_text)
        return {"error": f"API returned an HTML error page instead of JSON: {response_text}"}
      
      res_json = await res.json_async()
    except TimeoutError:  # asyncio.TimeoutError is TimeoutError on Python 3.11+
      return {"error": "The request timed out. Please try reducing the scope of your query by using `since` and `until` parameters to add time delimiters"}
    except json.JSONDecodeError as json_error:
      logging.error(f"Failed to parse JSON response: {json_error}")
      return {"error": f"Failed to parse server response: {json_error}."}
    except Exception as e:
      logging.error(f"An unexpected error occurred: {e} (type: {type(e)})")
      return {"error": f"An unexpected error occurred: {e}"}

    # Remove unnecessary information
    if "docs" in res_json:
      for i in range(len(res_json["docs"])):
        res_json["docs"][i].pop("__meta", None)
        res_json["docs"][i].pop("entities", None)
       
    link_header = res.headers.get("link")
    if link_header and 'rel="next"' in link_header:
        try:
            url_part = link_header.split(';')[0].strip().strip('<>')
            query_string = urllib.parse.urlparse(url_part).query
            next_page = urllib.parse.parse_qs(query_string).get('page', [None])[0]
            if next_page:
                res_json["page"] = next_page
        except (IndexError, AttributeError):
            # Could not parse link header, proceed without it
            pass

    return utils.sanitize_response(res_json)


def _remove_upload_tool(target_server: typing.Any) -> None:
  """Removes analyse_file from target_server if currently registered."""
  try:
    target_server.remove_tool("analyse_file")
  except _ToolError:
    pass


def _register_upload_tools(target_server: typing.Any = server) -> bool:
  """Registers or unregisters upload tools based on GTI_ALLOWED_UPLOAD_DIR configuration."""
  try:
    allowed_dir = _resolve_allowed_upload_dir()
  except ValueError as e:
    _remove_upload_tool(target_server)
    _logger.error("Failed to configure %s: %s", _UPLOAD_DIR_ENV_VAR, e)
    raise

  _remove_upload_tool(target_server)
  if allowed_dir is not None:
    target_server.add_tool(analyse_file)
    _logger.info("Registered analyse_file tool confined to %s", allowed_dir)
    return True

  _logger.info(
      "analyse_file tool unregistered (set %s to enable)", _UPLOAD_DIR_ENV_VAR
  )
  return False


_register_upload_tools(server)
