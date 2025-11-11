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
import urllib.parse
import json
import asyncio

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
) -> list[dict[str, typing.Any]]:
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

@server.tool()
async def search_digital_threat_monitoring(
    query: str,
    ctx: Context,
    size: int = 10,
    since: str = None,
    until: str = None,
    page: str = None,
    truncate: str = None,
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
    params = {k: v for k, v in params.items() if v is not None}
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
    except (asyncio.TimeoutError, TimeoutError): # Catch both
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
