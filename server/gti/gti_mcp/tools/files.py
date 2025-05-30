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
) -> typing.Dict[str, typing.Any]:
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
      List of objects related to the given file.
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
) -> typing.Dict[str, typing.Any]:
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
async def get_file_behavior_summary(hash: str, ctx: Context) -> typing.Dict[str, typing.Any]:
  """Retrieve a summary of all the file behavior reports from all the sandboxes.

  Args:
    hash (required): MD5/SHA1/SHA256) hash that identifies the file.
  Returns:
    The file behavior summary.
  """
  async with vt_client(ctx) as client:
    res = await client.get_async(f"/files/{hash}/behaviour_summary")
    res = await res.json_async()
  return utils.sanitize_response(res["data"])


@server.tool()
async def analyse_file(file_path: str, ctx: Context):
  """Upload and analyse the file in VirusTotal.

  The file will be uploaded to VirusTotal and shared with the community.

  Args:
    file_path (required): Path to the file for analysis. Use absolute path.
  Returns:
    The analysis report.
  """
  async with vt_client(ctx) as client:
    with open(file_path, "rb") as f:    
      analysis = await client.scan_file_async(file=f)
      logging.info(f"File {file_path} uploaded.")

    res = await client.wait_for_analysis_completion(analysis)
    logging.info(f"Analysis has completed with ID %s", res.id)
    return utils.sanitize_response(res.to_dict())
