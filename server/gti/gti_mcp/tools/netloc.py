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
import typing

from mcp.server.fastmcp import Context

from .. import utils
from ..server import server, vt_client


DOMAIN_RELATIONSHIPS = [
    "associations",
    "caa_records",
    "campaigns",
    "cname_records",
    "collections",
    "comments",
    "communicating_files",
    "downloaded_files",
    "graphs",
    "historical_ssl_certificates",
    "historical_whois",
    "immediate_parent",
    "malware_families",
    "memory_pattern_parents",
    "mx_records",
    "ns_records",
    "parent",
    "referrer_files",
    "related_comments",
    "related_reports",
    "related_threat_actors",
    "reports",
    "resolutions",
    "siblings",
    "soa_records",
    "software_toolkits",
    "subdomains",
    "urls",
    "user_votes",
    "votes",
    "vulnerabilities",
]

DOMAIN_KEY_RELATIONSHIPS = [
    "associations",
]


IP_RELATIONSHIPS = [
    "associations",
    "campaigns",
    "collections",
    "comments",
    "communicating_files",
    "downloaded_files",
    "graphs",
    "historical_ssl_certificates",
    "historical_whois",
    "malware_families",
    "memory_pattern_parents",
    "referrer_files",
    "related_comments",
    "related_reports",
    "related_threat_actors",
    "reports",
    "resolutions",
    "software_toolkits",
    "urls",
    "user_votes",
    "votes",
    "vulnerabilities",
]

IP_KEY_RELATIONSHIPS = [
    "associations",
]


@server.tool()
async def get_domain_report(domain: str, ctx: Context) -> typing.Dict[str, typing.Any]:
  """Get a comprehensive domain analysis report from Google Threat Intelligence.

  Args:
    domain (required): Domain to analyse.
  Returns:
    Report with insights about the domain.
  """
  res = await utils.fetch_object(
      vt_client(ctx),
      "domains",
      "domain",
      domain,
      relationships=DOMAIN_KEY_RELATIONSHIPS,
      params={"exclude_attributes": "last_analysis_results"})
  return res


@server.tool()
async def get_entities_related_to_a_domain(domain: str, relationship_name: str, ctx: Context) -> typing.Dict[str, typing.Any]:
  """Retrieve entities related to the the given domain.

    The following table shows a summary of available relationships for domain objects.

    | Relationship                | Description                                                |
    | :-------------------------- | :--------------------------------------------------------- |
    | associations                | Domain's associated objects (reports, campaigns, IoC collections, malware families, software toolkits, vulnerabilities, threat-actors), without filtering by the associated object type.                                                             | Everyone. | List of [reports](ref:report-object), [campaigns](ref:campaign-object), [IoC collections](ref:ioc-collection-object), [malware families](ref:malware-family-object), [software toolkits](ref:software-toolkit-object), [vulnerabilities](ref:vulnerability-object), [threat-actors](ref:threat-actor-object) objecs.|
    | caa_records                 | Records CAA for the domain.                                |
    | campaigns                   | Campaigns associated to the domain.                        |
    | cname_records               | Records CNAME for the domain.                              |
    | collections                 | IoC Collections associated to the domain.                  |
    | comments                    | Community posted comments about the domain.                |
    | communicating_files         | Files that communicate with the domain.                    |
    | downloaded_files            | Files downloaded from that domain.                         |
    | graphs                      | Graphs including the domain.                               |
    | historical_ssl_certificates | SSL certificates associated with the domain.               |
    | historical_whois            | WHOIS information for the domain.                          |
    | immediate_parent            | Domain's immediate parent.                                 |
    | malware_families            | Malware families associated to the domain.                 |
    | memory_pattern_parents      | Files having a domain as string on memory during sandbox execution.  |
    | mx_records                  | Records MX for the domain.                                 |
    | ns_records                  | Records NS for the domain.                                 |
    | parent                      | Domain's top parent.                                       |
    | referrer_files              | Files containing the domain.                               |
    | related_comments            | Community posted comments in the domain's related objects. |
    | related_reports             | Reports that are directly and indirectly related to the domain. |
    | related_threat_actors       | Threat actors related to the domain.                       |
    | reports                     | Reports directly associated to the domain.                 |
    | resolutions                 | DNS resolutions for the domain.                            |
    | siblings                    | Domain's sibling domains.                                  |
    | soa_records                 | Records SOA for the domain.                                |
    | software_toolkits           | Software and Toolkits associated to the domain.            |
    | subdomains                  | Domain's subdomains.                                       |
    | urls                        | URLs having this domain.                                   |
    | user_votes                  | Current user's votes.                                      |
    | votes                       | Domain's votes.                                            |
    | vulnerabilities             | Vulnerabilities associated to the domain.                  |

    Args:
      domain (required): Domain to analyse.
    Returns:
      List of entities related to the domain.
  """
  if not relationship_name in DOMAIN_RELATIONSHIPS:
    return {
       "error": f"Relationship {relationship_name} does not exist. "
                f"Available relationships are: {','.join(DOMAIN_RELATIONSHIPS)}"
    }

  res = await utils.fetch_object_relationships(
      vt_client(ctx), "domains", domain, [relationship_name])
  return res.get(relationship_name, [])


@server.tool()
async def get_ip_address_report(ip_address: str, ctx: Context) -> typing.Dict[str, typing.Any]:
  """Get a comprehensive IP Address analysis report from Google Threat Intelligence.

  Args:
    ip_address (required): IP Address to analyze. It can be IPv4 or IPv6.
  Returns:
    Report with insights about the IP address.
  """
  res = await utils.fetch_object(
      vt_client(ctx),
      "ip_addresses",
      "ip", ip_address,
      relationships=IP_KEY_RELATIONSHIPS,
      params={"exclude_attributes": "last_analysis_results"})
  return res


@server.tool()
async def get_entities_related_to_an_ip_address(ip_address: str, relationship_name: str, ctx: Context) -> typing.Dict[str, typing.Any]:
  """Retrieve entities related to the the given IP Address.

    The following table shows a summary of available relationships for IP Address objects.

    | Relationship                | Description                                            |
    | :-------------------------- | :----------------------------------------------------- |
    | associations                | IP's associated objects (reports, campaigns, IoC collections, malware families, software toolkits, vulnerabilities, threat-actors), without filtering by the associated object type.                                               |
    | campaigns                   | Campaigns associated to the IP address.                |
    | collections                 | IoC Collections associated to the IP address.          |
    | comments                    | Comments for the IP address.                           |
    | communicating_files         | Files that communicate with the IP address.            |
    | downloaded_files            | Files downloaded from the IP address.                  |
    | graphs                      | Graphs including the IP address.                       |
    | historical_ssl_certificates | SSL certificates associated with the IP.               |
    | historical_whois            | WHOIS information for the IP address.                  |
    | malware_families            | Malware families associated to the IP address.         |
    | memory_pattern_parents      | Files having an IP as string on memory during sandbox execution.         |
    | referrer_files              | Files containing the IP address.                       |
    | related_comments            | Community posted comments in the IP's related objects. |
    | related_reports             | Reports that are directly and indirectly related to the IP. |
    | related_threat_actors       | Threat actors related to the IP address.               |
    | reports                     | Reports directly associated to the IP.                 |
    | resolutions                 | IP address' resolutions                                |
    | software_toolkits           | Software and Toolkits associated to the IP address.    |
    | urls                        | URLs related to the IP address.                        |
    | user_votes                  | IP's votes made by current signed-in user.             |
    | votes                       | IP's votes.                                            |
    | vulnerabilities             | Vulnerabilities associated to the IP address.          |

    Args:
      ip_address (required): IP Addres to analyse.
    Returns:
      List of entities related to the IP Address.
  """
  if not relationship_name in IP_RELATIONSHIPS:
    return {
       "error": f"Relationship {relationship_name} does not exist. "
                f"Available relationships are: {','.join(IP_RELATIONSHIPS)}"
    }

  res = await utils.fetch_object_relationships(
      vt_client(ctx), "ip_addresses", ip_address, [relationship_name])
  return res.get(relationship_name, [])
