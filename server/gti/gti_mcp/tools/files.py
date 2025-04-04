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

# Load resources and tools.
@server.tool()
async def get_file_report(hash: str, ctx: Context) -> typing.Dict[str, typing.Any]:
  """Get a comprehensive file analysis report using its hash (MD5/SHA-1/SHA-256). 
  
  Returns a concise summary of key threat details including
  detection stats, threat classification, and important indicators.
  Parameters:
    hash (required): The MD5, SHA-1, or SHA-256 hash of the file to analyze.
  Example: '8ab2cf...', 'e4d909c290d0...', etc.
  """
  res = await utils.fetch_object(vt_client(ctx), "files", "file", hash, [
      "contacted_domains",
      "contacted_ips",
      "contacted_urls",
      "dropped_files",
      "embedded_domains",
      "embedded_ips",
      "embedded_urls",
      "associations",
  ])
  return res


@server.tool()
async def get_entities_related_to_a_file(hash: str, relationship_name: str, ctx: Context) -> typing.Dict[str, typing.Any]:
  """Retrieve entities related to the the given file hash.

    The following table shows a summary of available relationships for file objects.

    | Relationship           | Description                                                                       | Accessibility                                                         | Return object type                                      |
    | :--------------------- | :-------------------------------------------------------------------------------- | :-------------------------------------------------------------------- | :------------------------------------------------------ |
    | analyses               | Analyses for the file                                                             | Google TI users only.                                      | A list of [Analyses](ref:analyses-object)               |
    | associations           | File's associated objects (reports, campaigns, IoC collections, malware families, software toolkits, vulnerabilities, threat-actors), without filtering by the associated object type.                                                                                      | Everyone.                                      | A list of [reports](ref:report-object), [campaigns](ref:campaign-object), [IoC collections](ref:ioc-collection-object), [malware families](ref:malware-family-object), [software toolkits](ref:software-toolkit-object), [vulnerabilities](ref:vulnerability-object), [threat-actors](ref:threat-actor-object) objecs. |
    | behaviours             | Behaviour reports for the file. See [File behaviour](ref:file-behaviour-summary-object). | Everyone.                                                             | A list of [File behaviour](ref:file-behaviour-summary-object). |
    | attack_techniques              | Returns the Attack Techniques of the File.             | Google TI Enterprise and Enterprise Plus users only.                    | List of [Attack Techniques](ref:object-attack-techniques).             |
    | bundled_files          | Files bundled within the file.                                                    | Everyone.                                                             | A list of [Files](ref:file-object).                    |
    | campaigns              | Campaigns associated to the file.                                                 | Google TI Enterprise and Enterprise Plus users only.                                      | A list of collections of type [Campaign](ref:campaign-object).             |
    | carbonblack_children   | Files derived from the file according to Carbon Black.                            | Google TI users only.                                      | A list of [Files](ref:file-object).                    |
    | carbonblack_parents    | Files from where the file was derived according to Carbon Black.                  | Google TI users only.                                      | A list of [Files](ref:file-object).                           |
    | collections            | IoC Collections associated to the file.                                           | Everyone.                                                             | A list of collections of type [IoC Collection](ref:ioc-collection-object). |
    | comments               | Comments for the file.                                                            | Everyone.                                                             | A list of [Comments](ref:comment-object).               |
    | compressed_parents     | Compressed files that contain the file.                                           | Google TI users only.                                      | A list of [Files](ref:file-object).                    |
    | contacted_domains      | Domains contacted by the file.                                                    | Everyone.                                                             | A list of [Domains](ref:domains-object).                |
    | contacted_ips          | IP addresses contacted by the file.                                               | Everyone.                                                             | A list of [IP addresses](ref:ip-object).                |
    | contacted_urls         | URLs contacted by the file.                                                       | Everyone.                                                             | A list of [URLs](ref:url-object).                       |
    | dropped_files          | Files dropped by the file during its execution.                                   | Everyone.                                                             | A list of [Files](ref:file-object).                    |
    | email_attachments      | Files attached to the email.                                                      | Google TI users only.                                      | A list of [Files](ref:file-object).                    |
    | email_parents          | Email files that contained the file.                                              | Google TI users only.                                      | A list of [Files](ref:file-object).                    |
    | embedded_domains       | Domain names embedded in the file.                                                | Google TI users only.                                      | A list of [Domains](ref:domains-object).                |
    | embedded_ips           | IP addresses embedded in the file.                                                | Google TI users only.                                      | A list of [IP addresses](ref:ip-object).                |
    | embedded_urls          | URLs embedded in the file.                                                        | Google TI users only.                                      | A list of [URLs](ref:url-object).                       |
    | execution_parents      | Files that executed the file.                                                     | Everyone.                                                             | A list of [Files](ref:file-object).                    |
    | graphs                 | Graphs that include the file.                                                     | Everyone.                                                             | A list of [Graphs](ref:graph-object).                   |
    | itw_domains            | In the wild domain names from where the file has been downloaded.                 | Google TI users only.                                      | A list of [Domains](ref:domains-object).                |
    | itw_ips                | In the wild IP addresses from where the file has been downloaded.                 | Google TI users only.                                      | A list of [IP addresses](ref:ip-object).                |
    | itw_urls               | In the wild URLs from where the file has been downloaded.                         | Google TI users only.                                      | A list of [URLs](ref:url-object).                       |
    | malware_families       | Malware families associated to the file.                                          | Google TI Enterprise and Enterprise Plus users only.                                     | A list of collections of type [malware family](ref:malware-family-object).|
    | memory_pattern_domains       | Domain string patterns found in memory during sandbox execution.                   | Google TI users only.                                     | List of [Domains](ref:domains-object).|
    | memory_pattern_ips       | IP address string patterns found in memory during sandbox execution.                         | Google TI users only.                                     | List of [IP Addresses](ref:ip-object).|
    | memory_pattern_urls       | URL string patterns found in memory during sandbox execution.                                          | Google TI users only.                         | List of [URLs](ref:url-object).|
    | overlay_children       | Files contained by the file as an overlay.                                        | Google TI users only.                                      | List of [Files](ref:file-object).                    |
    | overlay_parents        | File that contain the file as an overlay.                                         | Google TI users only.                                     | A list of [Files](ref:file-object).                    |
    | pcap_children          | Files contained within the PCAP file.                                             | Google TI users only.                                      | A list of [Files](ref:file-object).                    |
    | pcap_parents           | PCAP files that contain the file.                                                 | Google TI users only.                                      | A list of [Files](ref:file-object).                    |
    | pe_resource_children   | Files contained by a PE file as a resource.                                       | Everyone.                                                             | A list of [Files](ref:file-object).                    |
    | pe_resource_parents    | PE files containing the file as a resource.                                       | Everyone.                                                             | A list of [Files](ref:file-object).                    |
    | related_attack_techniques    | Returns the Attack Techniques of the Collections containing this File.                  | Google TI Enterprise and Enterprise Plus users only.                   | List of [Attack Techniques](ref:object-attack-techniques).                    |
    | related_reports    | Reports that are directly and indirectly related to the file.                      | Google TI Enterprise and Enterprise Plus users only.                                                             | List of [Reports](ref:report-object).                   |
    | related_threat_actors    | File's related threat actors.                     | Google TI Enterprise and Enterprise Plus users only.                                                             | List of collections of type [Threat Actor](ref:threat-actor-object).                    |
    | reports                | Reports directly associated to the file.                                                  | Google TI Enterprise and Enterprise Plus users only.                                      | A list of collections of type [Report](ref:report-object).                 |
    | screenshots            | Screenshots related to the sandbox execution of the file.                         | Google TI users only.                                      | A list of [Screenshots](ref:screenshots-object).        |
    | similar_files          | Files that are similar to the file.                                               | Google TI users only.                                     | A list of [Files](ref:file-object).                    |
    | software_toolkits      | Software and Toolkits associated to the file.                                     | Google TI Enterprise and Enterprise Plus users only.                                    | A list of collections of type [Software and Toolkits](ref:software-toolkit-object).            |
    | submissions            | Submissions for the file.                                                         | Google TI users only.                                      | A list of [Submissions](ref:submission-object).         |
    | urls_for_embedded_js          | URLs where this (JS) file is embedded.                                              | Google TI users only.                                      | List of [URLs](ref:url-object).     |
    | user_votes          | File's votes made by current signed-in user.                                | Everyone.                                      | A list of [Votes](ref:vote-object).     |
    | votes                  | Votes for the file.                                                               | Everyone.                                                              | A list of [Votes](ref:vote-object).                     |
    | vulnerabilities        | Vulnerabilities associated to the file.                                           | Google TI Enterprise and Enterprise Plus users only.                                      | A list of collections of type [Vulnerability](ref:vulnerability-object).  |
  
    Args:
      hash (required): MD5/SHA1/SHA256) hash that identifies the file.
    Returns:
      List of user comments to the given file.
  """
  if not relationship_name in FILE_RELATIONSHIPS:
    return {
       "error": f"Relationship {relationship_name} does not exist. "
                f"Available relationships are: {','.join(FILE_RELATIONSHIPS)}"
    }

  res = await utils.fetch_object_relationships(
      vt_client(ctx), "files", hash, [relationship_name])
  return [obj.to_dict() for obj in res.get(relationship_name, [])]


@server.tool()
async def get_file_behavior_report(file_behaviour_id: str, ctx: Context) -> typing.Dict[str, typing.Any]:
  """Retrieve the file behaviour report of the given file behaviour identifier.

  You can get all the file behaviour of a given a file by calling `get_entities_related_to_a_file` as the file hash and the `behaviours` as relationship name.

  The file behaviour ID is composed using the following pattern: "{file hash}_{sandbox name}".
  
  Args:
    file_behaviour_id (required): File behaviour ID.
  Returns:
    The file behaviour report.
  """
  res = await utils.fetch_object(vt_client(ctx), "file_behaviours", "file_behaviour", file_behaviour_id, [
      "contacted_domains",
      "contacted_ips",
      "contacted_urls",
      "dropped_files",
      "embedded_domains",
      "embedded_ips",
      "embedded_urls",
      "associations",
  ])
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
