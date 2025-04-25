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
import logging
import typing

from mcp.server.fastmcp import Context

from .. import utils
from ..server import server, vt_client


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
async def get_file_report(hash: str, ctx: Context) -> typing.Dict[str, typing.Any]:
  """Get a comprehensive file analysis report using its hash (MD5/SHA-1/SHA-256).

  Returns a concise summary of key threat details including
  detection stats, threat classification, and important indicators.
  Parameters:
    hash (required): The MD5, SHA-1, or SHA-256 hash of the file to analyze.
  Example: '8ab2cf...', 'e4d909c290d0...', etc.
  """
  res = await utils.fetch_object(
      vt_client(ctx),
      "files",
      "file",
      hash,
      relationships=FILE_KEY_RELATIONSHIPS,
      params={"exclude_attributes": "last_analysis_results"}
  )
  return res


@server.tool()
async def get_entities_related_to_a_file(
    hash: str, relationship_name: str, ctx: Context
) -> typing.Dict[str, typing.Any]:
    """Retrieve entities related to the the given file hash.

    The following table shows a summary of available relationships for file objects.

    | Relationship           | Description                                                                       |
    | :--------------------- | :-------------------------------------------------------------------------------- |
    | analyses               | Analyses for the file                                                             |
    | associations           | File's associated objects (reports, campaigns, IoC collections, malware families, software toolkits, vulnerabilities, threat-actors), without filtering by the associated object type.                                                                                      |
    | behaviours             | Behaviour reports for the file.                                                   |
    | attack_techniques      | Returns the Attack Techniques of the File.                                        |
    | bundled_files          | Files bundled within the file.                                                    |
    | campaigns              | Campaigns associated to the file.                                                 |
    | carbonblack_children   | Files derived from the file according to Carbon Black.                            |
    | carbonblack_parents    | Files from where the file was derived according to Carbon Black.                  |
    | collections            | IoC Collections associated to the file.                                           |
    | comments               | Comments for the file.                                                            |
    | compressed_parents     | Compressed files that contain the file.                                           |
    | contacted_domains      | Domains contacted by the file.                                                    |
    | contacted_ips          | IP addresses contacted by the file.                                               |
    | contacted_urls         | URLs contacted by the file.                                                       |
    | dropped_files          | Files dropped by the file during its execution.                                   |
    | email_attachments      | Files attached to the email.                                                      |
    | email_parents          | Email files that contained the file.                                              |
    | embedded_domains       | Domain names embedded in the file.                                                |
    | embedded_ips           | IP addresses embedded in the file.                                                |
    | embedded_urls          | URLs embedded in the file.                                                        |
    | execution_parents      | Files that executed the file.                                                     |
    | graphs                 | Graphs that include the file.                                                     |
    | itw_domains            | In the wild domain names from where the file has been downloaded.                 |
    | itw_ips                | In the wild IP addresses from where the file has been downloaded.                 |
    | itw_urls               | In the wild URLs from where the file has been downloaded.                         |
    | malware_families       | Malware families associated to the file.                                          |
    | memory_pattern_domains | Domain string patterns found in memory during sandbox execution.                  |
    | memory_pattern_ips     | IP address string patterns found in memory during sandbox execution.              |
    | memory_pattern_urls    | URL string patterns found in memory during sandbox execution.                     |
    | overlay_children       | Files contained by the file as an overlay.                                        |
    | overlay_parents        | File that contain the file as an overlay.                                         |
    | pcap_children          | Files contained within the PCAP file.                                             |
    | pcap_parents           | PCAP files that contain the file.                                                 |
    | pe_resource_children   | Files contained by a PE file as a resource.                                       |
    | pe_resource_parents    | PE files containing the file as a resource.                                       |
    | related_attack_techniques    | Returns the Attack Techniques of the Collections containing this File.      |
    | related_reports        | Reports that are directly and indirectly related to the file.                     |
    | related_threat_actors  | File's related threat actors.                                                     |
    | reports                | Reports directly associated to the file.                                          |
    | screenshots            | Screenshots related to the sandbox execution of the file.                         |
    | similar_files          | Files that are similar to the file.                                               |
    | software_toolkits      | Software and Toolkits associated to the file.                                     |
    | submissions            | Submissions for the file.                                                         |
    | urls_for_embedded_js   | URLs where this (JS) file is embedded.                                            |
    | user_votes             | File's votes made by current signed-in user.                                      |
    | votes                  | Votes for the file.                                                               |
    | vulnerabilities        | Vulnerabilities associated to the file.                                           |

    Args:
      hash (required): MD5/SHA1/SHA256) hash that identifies the file.
      relationship_name (required): Relationship name.
    Returns:
      List of objects related to the given file.
    """
    if not relationship_name in FILE_RELATIONSHIPS:
        return {
            "error": f"Relationship {relationship_name} does not exist. "
            f"Available relationships are: {','.join(FILE_RELATIONSHIPS)}"
        }

    res = await utils.fetch_object_relationships(
        vt_client(ctx), "files", hash, [relationship_name])
    return res.get(relationship_name, [])


@server.tool()
async def get_file_behavior_report(
    file_behaviour_id: str, ctx: Context
) -> typing.Dict[str, typing.Any]:
  """Retrieve the file behaviour report of the given file behaviour identifier.

  You can get all the file behaviour of a given a file by calling `get_entities_related_to_a_file` as the file hash and the `behaviours` as relationship name.

  The file behaviour ID is composed using the following pattern: "{file hash}_{sandbox name}".

  Args:
    file_behaviour_id (required): File behaviour ID.
  Returns:
    The file behaviour report.
  """
  res = await utils.fetch_object(
      vt_client(ctx),
      "file_behaviours",
      "file_behaviour",
      file_behaviour_id,
      [
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
  return res


@server.tool()
async def get_file_behavior_summary(hash: str, ctx: Context) -> typing.Dict[str, typing.Any]:
  """Retrieve a summary of all the file behaviour reports from all the sandboxes runned by VirusTotal.

  Args:
    hash (required): MD5/SHA1/SHA256) hash that identifies the file.
  Returns:
    The file behaviour summary.
  """

  res = await vt_client(ctx).get_async(f"/files/{hash}/behaviour_summary")
  res = await res.json_async()
  return res["data"]


@server.tool()
async def analyse_file(file_path: str, ctx: Context):
  """Upload and analyse the file in VirusTotal.

  The file will be uploaded to VirusTotal and shared with the community.

  Args:
    file_path (required): Path to the file for analysis. Use absolute path.
  Returns:
    The analysis report.
  """
  with open(file_path, "rb") as f:
    analysis = await vt_client(ctx).scan_file_async(file=f)
    logging.info(f"File {file_path} uploaded.")

  res = await vt_client(ctx).wait_for_analysis_completion(analysis)
  logging.info(f"Analysis has completed with ID %s", res.id)
  return res.to_dict()
