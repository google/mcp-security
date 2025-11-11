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
import asyncio
from secops_soar_mcp import bindings
from mcp.server.fastmcp import FastMCP
from secops_soar_mcp.utils.consts import Endpoints
from secops_soar_mcp.utils.models import CasePriority
from logger_utils import get_logger
from typing import Annotated, Optional, List
from pydantic import Field
from secops_soar_mcp.utils.pydantic_list_field import PydanticListField

logger = get_logger(__name__)


def register_tools(mcp: FastMCP):
    @mcp.tool()
    async def list_cases(
        next_page_token: Annotated[
            Optional[str],
            Field(
                default=None,
                description="The nextPageToken to fetch the next page of results.",
            ),
        ],
    ) -> dict:
        """List cases available in the Security Orchestration, Automation, and Response (SOAR) platform.

        In a SOAR context, a 'case' typically represents a security incident, investigation,
        or a container for related alerts and response actions. Listing cases provides an
        overview of ongoing or past security events being managed by the platform.
        This is useful for getting a high-level list of recent security issues or finding
        a specific incident to investigate further.

        Returns:
            dict: A dictionary representing the raw API response from the SOAR platform,
                  usually containing a list of case objects with their summary details (e.g., ID, name, status, priority).
                  **Important Triage Note:** Case priority is only an initial indicator. True importance must be assessed by examining the full context (alerts, entities, potential impact, threat intelligence) using tools like `get_case_full_details`.

        **Workflow Integration:**
        - Often the FIRST step in a triage workflow to understand the current incident queue within the SOAR platform.
        - Use the output as a STARTING point, not an end, for cases needing attention.

        **Next Steps (using MCP-enabled tools):**
        - Identify specific `case_id` values from the response for further investigation.
        - Use a tool to get comprehensive details for a specific case (like `get_case_full_details`).
        - Use a tool to list the alerts associated with a specific case (like `list_alerts_by_case`).
        - Use a tool to change the case priority if initial assessment suggests it's warranted (like `change_case_priority`).
        - Begin enrichment by extracting key indicators from the case summary and using appropriate SIEM, TI, or other security tool MCP integrations.
        """
        if next_page_token:
            return await bindings.http_client.get(
                Endpoints.BASE_CASE_URL,
                params={"$expand": "tags", "pageToken": next_page_token},
            )
        return await bindings.http_client.get(Endpoints.BASE_CASE_URL)

    @mcp.tool()
    async def post_case_comment(
        case_id: Annotated[str, Field(..., description="The ID of the case.")],
        comment: Annotated[
            str, Field(..., description="The comment we wish to add to the case.")
        ],
    ) -> dict:
        """Post a comment to a specific case within the SOAR platform.

        Cases are used to track security incidents and investigations. Adding comments
        is essential for documenting findings, communication between analysts, recording
        actions taken, or providing updates on the investigation progress.

        Args:
            case_id (str): The unique identifier (ID) of the specific case to which
                           this comment should be added. This ID is typically obtained
                           by listing cases or from an alert associated with the case. (Example: "523")
            comment (str): The textual content of the comment to be recorded within the case history. (Example: "Investigating potential impact.")

        Returns:
            dict: A dictionary representing the raw API response, usually confirming
                  the successful posting of the comment or indicating any errors.

        **Workflow Integration:**
        - Use this throughout an investigation to document findings, analyst actions,
          or conclusions derived from other MCP-enabled tools (e.g., SIEM lookups,
          TI enrichment, EDR details, Cloud posture checks).
        - Essential for collaboration and maintaining an audit trail within the SOAR case.

        **Next Steps (using MCP-enabled tools):**
        - Continue investigation based on the information documented.
        - Use comments to justify changes in case priority (using a case priority tool) or status.
        - Share key comments or findings with other relevant systems if needed (e.g., ticketing, reporting).
        """
        return await bindings.http_client.post(
            Endpoints.BASE_CASE_COMMENTS_URL.format(CASE_ID=case_id),
            req={"Comment": comment},
        )

    @mcp.tool()
    async def list_alerts_by_case(
        case_id: Annotated[str, Field(..., description="The ID of the case.")],
        next_page_token: Annotated[
            Optional[str],
            Field(
                default=None,
                description="The nextPageToken to fetch the next page of results.",
            ),
        ],
    ) -> dict:
        """List the security alerts associated with a specific case ID in the SOAR platform.

        Alerts are notifications generated by security tools (like SIEMs, EDRs) indicating
        potential security issues. In SOAR, alerts are often grouped into cases for
        investigation and response. Listing alerts for a case helps understand the
        scope of the incident, the specific events that triggered it, and the evidence collected.

        Args:
            case_id (str): The unique identifier (ID) of the case for which associated
                           alerts should be retrieved. (Example: "523")

        Returns:
            dict: A dictionary representing the raw API response, typically containing
                  a list of alert objects linked to the specified case, including details
                  like alert name, source, severity, and timestamp. Alert severity provides
                  initial guidance, but the actual risk depends on the context and evidence
                  within the associated events.

        **Workflow Integration:**
        - Use after identifying a case of interest (e.g., via `list_cases` or `get_case_full_details`).
        - Helps understand the specific triggers (alerts) and scope of the incident represented by the SOAR case.

        **Next Steps (using MCP-enabled tools):**
        - Identify specific `alert_id` values for deeper investigation.
        - Use a tool to get the raw events underlying a specific alert (like `list_events_by_alert`).
        - Use tools to understand how alerts are grouped within the case (like `list_alert_group_identifiers_by_case`)
          and find entities associated with those groups (like `get_entities_by_alert_group_identifiers`).
        - Extract indicators from alert details and use SIEM entity lookup or event search tools for enrichment.
        - Correlate alert details with findings from other security tools (EDR, Network, Cloud, TI) via their MCP tools.
        """
        if next_page_token:
            return await bindings.http_client.get(
                Endpoints.BASE_ALERT_URL.format(CASE_ID=case_id),
                params={"pageToken": next_page_token},
            )
        return await bindings.http_client.get(
            Endpoints.BASE_ALERT_URL.format(CASE_ID=case_id)
        )

    @mcp.tool()
    async def list_alert_group_identifiers_by_case(
        case_id: Annotated[str, Field(..., description="The ID of the case.")],
        next_page_token: Annotated[
            Optional[str],
            Field(
                default=None,
                description="The nextPageToken to fetch the next page of results.",
            ),
        ],
    ):
        """List alert group identifiers associated with a specific case ID in the SOAR platform.

        In this SOAR implementation, alerts within a case can be grouped using identifiers,
        potentially for correlation, playbook execution stages, or analyst assignment.
        Retrieving these identifiers helps understand the internal structure of a case
        or target specific alert groupings for automation or analysis.

        Args:
            case_id (str): The unique identifier (ID) of the case for which alert group
                           identifiers should be retrieved. (Example: "523")

        Returns:
            dict: A dictionary representing the raw API response from the SOAR platform.
                  The exact structure depends on the API, but it typically contains
                  a list of strings, where each string is an alert group identifier
                  associated with the specified case.

        **Workflow Integration:**
        - Use after identifying a case and its associated alerts within the SOAR platform.
        - Helps understand how alerts are grouped within the case, which might be relevant
          for understanding playbook logic or identifying related sets of alerts for targeted actions.

        **Next Steps (using MCP-enabled tools):**
        - Use the retrieved identifiers with a tool to find entities specifically related
          to these groups (like `get_entities_by_alert_group_identifiers`).
        - Use the identifiers as parameters for certain playbook actions or integrations
          (potentially from various security tools connected via MCP) if they operate on alert groups.
        """
        if next_page_token:
            return await bindings.http_client.get(
                Endpoints.LIST_ALERT_GROUP_IDENTIFIERS_BY_CASE.format(CASE_ID=case_id),
                params={"pageToken": next_page_token},
            )
        return await bindings.http_client.get(
            Endpoints.LIST_ALERT_GROUP_IDENTIFIERS_BY_CASE.format(CASE_ID=case_id)
        )

    @mcp.tool()
    async def list_events_by_alert(
        case_id: Annotated[str, Field(..., description="The ID of the case.")],
        alert_id: Annotated[str, Field(..., description="The ID of the alert.")],
        next_page_token: Annotated[
            Optional[str],
            Field(
                default=None,
                description="The nextPageToken to fetch the next page of results.",
            ),
        ],
    ):
        """List the underlying security events associated with a specific alert within a given case.

        Security alerts (often derived from detection rules or IoC matches) are typically
        triggered by one or more underlying events ingested into the security platform
        (e.g., Chronicle). These events provide the raw data (likely in UDM format)
        needed to validate the alert, understand the specific activity, and perform deep-dive investigations.

        Args:
            case_id (str): The unique identifier (ID) of the case containing the alert. (Example: "523")
            alert_id (str): The unique identifier (ID) of the specific alert whose
                            associated events are to be listed. (Example: "751")

        Returns:
            dict: A dictionary representing the raw API response from the SOAR platform,
                  typically containing a list of event objects (potentially in UDM format)
                  related to the specified alert.

        **Workflow Integration:**
        - Use after identifying a specific alert of interest within a SOAR case (e.g., via `list_alerts_by_case`).
        - Provides the ground truth event data (often from the SIEM) needed to validate the alert
          and understand the exact actions that occurred.

        **Next Steps (using MCP-enabled tools):**
        - Analyze the event data (e.g., UDM format) for specific details like command lines,
          network connections, file hashes, user activity, etc.
        - Extract new indicators from the events.
        - Use entity lookup or threat intelligence tools to enrich newly found indicators.
        - Correlate event details with other related events using SIEM event search tools.
        - Document findings in the relevant case management system using a commenting tool.
        """
        if next_page_token:
            return await bindings.http_client.get(
                Endpoints.LIST_INVOLVED_EVENTS_BY_ALERT.format(
                    CASE_ID=case_id, ALERT_ID=alert_id
                ),
                params={"pageToken": next_page_token},
            )
        return await bindings.http_client.get(
            Endpoints.LIST_INVOLVED_EVENTS_BY_ALERT.format(
                CASE_ID=case_id, ALERT_ID=alert_id
            )
        )

    @mcp.tool()
    async def change_case_priority(
        case_id: Annotated[str, Field(..., description="The ID of the case.")],
        case_priority: Annotated[
        str,
        Field(
            ...,
            description="The priority of the case.",
            json_schema_extra={
                "enum": [
                    "PriorityUnspecified",
                    "PriorityInfo",
                    "PriorityLow",
                    "PriorityMedium",
                    "PriorityHigh",
                    "PriorityCritical",
                ]
            }
        )],
    ):
        """Change the priority level of a specific case in the SOAR platform.

        Case priority (e.g., PriorityUnspecified, PriorityInfo, PriorityLow, PriorityMedium,
        PriorityHigh, PriorityCritical) helps security teams triage incidents and focus
        on the most urgent threats based on the *currently available information*. Remember that priority can change as more context is
        gathered during the investigation. The priority might be adjusted during the
        investigation lifecycle based on new findings.

        Args:
            case_id (str): The unique identifier (ID) of the case whose priority needs
                           to be updated. (Example: "523")
            case_priority (CasePriority): The new priority level to assign to the case.
                                          Must be one of the predefined enum values from
                                          `utils.models.CasePriority`.

        Returns:
            dict: A dictionary representing the raw API response from the SOAR platform,
                  usually confirming the successful update of the case priority or
                  indicating any errors encountered.

        **Workflow Integration:**
        - Use during triage or investigation when new information (from any connected MCP tool like SIEM, TI, EDR, etc.)
          suggests the initial case priority is incorrect.
        - Helps ensure analyst focus aligns with the actual risk posed by the incident as understood from multiple data sources.

        **Next Steps (using MCP-enabled tools):**
        - Document the reason for the priority change using a case commenting tool.
        - Adjust investigation efforts based on the new priority level.
        """
        return await bindings.http_client.patch(
            Endpoints.BASE_SPECIFIC_CASE_URL.format(CASE_ID=case_id),
            req={"Priority": case_priority},
        )

    @mcp.tool()
    async def get_entities_by_alert_group_identifiers(
        case_id: Annotated[str, Field(..., description="The ID of the case.")],
        alert_group_identifiers: Annotated[
            List[str], Field(..., description="Identifiers for the alert groups.")
        ],
    ):
        """Retrieve entities (e.g., IP addresses, hostnames, users) involved in specific alert groups within a case.

        Understanding which entities are associated with alerts is fundamental for incident
        investigation and response. This tool allows fetching entities linked to one or
        more alert groups, which can be crucial for identifying affected assets, potential
        attack vectors, or compromised accounts. The description also notes it can be used
        to get target entities for manual actions, implying these entities might be inputs
        for subsequent response playbooks or manual interventions.

        Args:
            case_id (str): The unique identifier (ID) of the case containing the alert groups. (Example: "523")
            alert_group_identifiers (List[str]): A list of identifiers for the specific
                                                 alert groups whose involved entities are
                                                 to be retrieved. (Example: ["rule_name_hash_guid"])

        Returns:
            dict: A dictionary representing the raw API response from the SOAR platform.
                  This typically contains a list or structure detailing the entities
                  (with identifiers, types, etc.) associated with the specified alert groups.

        **Workflow Integration:**
        - Use after identifying relevant alert group identifiers within a SOAR case (e.g., via `list_alert_group_identifiers_by_case`).
        - Crucial for pinpointing the specific assets, users, or indicators involved in a particular stage or aspect of an incident managed within the SOAR platform.

        **Next Steps (using MCP-enabled tools):**
        - Analyze the list of entities to understand the scope of impact.
        - Use a SOAR entity details tool (like `get_entity_details`) to get more SOAR-specific context on individual entities.
        - Use SIEM entity lookup tools to get broader historical context for these entities from logs.
        - Use SIEM event search tools to find detailed logs related to these entities' activities.
        - Use threat intelligence tools to enrich the identified entities.
        - Use the entity list as input for targeted response actions via SOAR playbooks or other security tool integrations (e.g., EDR, firewall).
        """
        return await bindings.http_client.post(
            Endpoints.GET_ALERT_GROUP_IDENTIFIERS_ENTITIES,
            req={"caseId": case_id, "alertGroupIdentifiers": alert_group_identifiers},
        )

    @mcp.tool()
    async def get_entity_details(
        entity_identifier: Annotated[
            str, Field(..., description="The identifier of the entity.")
        ],
        entity_type: Annotated[str, Field(..., description="The type of the entity.")],
        entity_environment: Annotated[
            str, Field(..., description="The environment of the entity.")
        ],
    ):
        """Fetch detailed information about a specific entity known to the SOAR platform.

        Entities (like IPs, domains, users, assets) are central to security investigations.
        This tool retrieves comprehensive details about a specific entity based on its
        identifier, type, and environment. This information might include enrichment data
        (e.g., threat intelligence, asset inventory details), related alerts or cases,
        observed activity, and risk scores, providing crucial context for analysis.

        Args:
            entity_identifier (str): The unique identifier of the entity. (Example: "192.168.1.100")
            entity_type (str): The type of the entity. The specific types supported depend
                               on the SOAR platform's entity model. (Example: "IP Address")
            entity_environment (str): The environment context for the entity, which might
                                      influence how it's identified or enriched. (Example: "Production")

        Returns:
            dict: A dictionary representing the raw API response from the SOAR platform,
                  containing detailed attributes and related information for the specified entity.

        **Workflow Integration:**
        - Use after identifying a specific entity of interest within the SOAR platform
          (e.g., via `get_entities_by_alert_group_identifiers` or `search_entity`).
        - Provides the SOAR platform's specific view of the entity, including enrichments
          performed by SOAR playbooks or integrations connected to this SOAR instance.

        **Next Steps (using MCP-enabled tools):**
        - Analyze the enrichment data provided by the SOAR platform (e.g., threat intel scores, asset details).
        - Compare SOAR entity details with broader context from SIEM entity lookup tools.
        - Use findings to inform risk assessment and response decisions within the SOAR workflow.
        - Document key details using a case commenting tool.
        - Correlate with information from other security tools (EDR, Network, Cloud, TI) via their MCP tools.
        """
        return await bindings.http_client.post(
            Endpoints.FETCH_FULL_UNIQUE_ENTITY,
            req={
                "EntityIdentifier": entity_identifier,
                "EntityType": entity_type,
                "EntityEnvironment": entity_environment,
                "LastCaseType": 0,
                "CaseDistributionType": 0,
            },
        )

    @mcp.tool()
    async def search_entity(
        term: Annotated[
            Optional[str],
            Field(
                default=None,
                description="The term to search for",
            ),
        ],
        type: Annotated[
            Optional[List[str]],
            Field(
                default=None,
                description="The type of the entity",
            ),
        ],
        is_suspicious: Annotated[
            Optional[bool],
            Field(
                default=None,
                description="A boolean that states if the entity is suspicious",
            ),
        ],
        is_internal_asset: Annotated[
            Optional[bool],
            Field(
                default=None,
                description="A boolean that states if the entity is an internal asset",
            ),
        ],
        is_enriched: Annotated[
            Optional[bool],
            Field(
                default=None,
                description="A boolean that states if the entity is enriched",
            ),
        ],
        network_name: Annotated[
            Optional[List[str]],
            Field(
                default=None,
                description="The network name",
            ),
        ],
        environment_name: Annotated[
            Optional[List[str]],
            Field(
                default=None,
                description="The environment name",
            ),
        ],
    ):
        """Search for entities within the SOAR platform based on various criteria.

        This tool provides a flexible way to find entities (assets, users, IOCs, etc.)
        matching specific attributes. It allows searching by term (e.g., part of a hostname),
        entity type, suspicion status, asset status (internal/external), enrichment status,
        network, or environment. This is useful for exploring the entity database, finding
        potentially related entities during an investigation, or identifying assets with
        specific characteristics.

        Args:
            term (Optional[str]): A search term (e.g., partial IP, hostname fragment) to match against entity identifiers or names.
            type (Optional[List[str]]): A list of entity types to filter by (e.g., ['IP Address', 'Hostname']).
            is_suspicious (Optional[bool]): Filter for entities marked as suspicious.
            is_internal_asset (Optional[bool]): Filter for entities identified as internal assets.
            is_enriched (Optional[bool]): Filter for entities that have undergone enrichment processes.
            network_name (Optional[List[str]]): Filter entities belonging to specific networks.
            environment_name (Optional[List[str]]): Filter entities belonging to specific environments.

        Returns:
            dict: A dictionary representing the raw API response from the SOAR platform,
                  typically containing a list of entity objects matching the search criteria.

        **Workflow Integration:**
        - Useful for exploratory analysis within the SOAR platform's entity database,
          especially when you don't have a specific identifier from an alert or case.
        - Can help identify potentially related entities based on partial information or
          shared characteristics (e.g., finding all suspicious hosts in a specific environment
          as known by the SOAR).

        **Next Steps (using MCP-enabled tools):**
        - Analyze the list of returned entities.
        - Use a SOAR entity details tool (like `get_entity_details`) for more SOAR-specific information on entities found.
        - Use SIEM entity lookup tools for broader historical context on interesting entities.
        - Use threat intelligence tools to enrich findings.
        """
        return await bindings.http_client.post(
            Endpoints.SEARCH_ENTITY,
            req={
                "Term": term,
                "Type": type,
                "IsSuspicious": is_suspicious,
                "IsInternalAsset": is_internal_asset,
                "IsEnriched": is_enriched,
                "NetworkName": network_name,
                "EnvironmentName": environment_name,
            },
        )

    @mcp.tool()
    async def get_case_full_details(
        case_id: Annotated[str, Field(..., description="The ID of the case.")],
    ):
        """Retrieve comprehensive details for a specific case by aggregating its core information, associated alerts, and comments.

        This tool provides a consolidated view of a security case by fetching its primary details
        (like status, priority, description), all linked security alerts, and the full history
        of comments added by analysts or automation. This aggregated information is essential
        for getting a complete understanding of an incident's context, scope, investigation
        progress, and collaborative notes without making multiple separate API calls.

        Args:
            case_id (str): The unique identifier (ID) of the case for which full details
                           are required. (Example: "523")

        Returns:
            dict: A dictionary containing the aggregated results from three separate API calls:
                  - 'case_details': The raw API response for the basic case information.
                  - 'case_alerts': The raw API response containing the list of alerts associated with the case.
                  - 'case_comments': The raw API response containing the list of comments for the case.
                  **Triage Note:** Use the `priority` field as an initial guide only. Analyze the combined details (alerts, comments, entities involved, potential impact, related threat intelligence) gathered by this tool and others to determine the true importance and urgency of the case.

        **Workflow Integration:**
        - A primary tool for *starting* the investigation of a specific case identified within the SOAR platform (e.g., via `list_cases`).
        - Provides a comprehensive *initial overview* by gathering core SOAR case data, associated alerts, and comments in one call. **Crucially, this is a starting point; a full investigation requires deeper analysis using subsequent tools.**

        **Next Steps (using MCP-enabled tools - Essential for Full Investigation):**
        - Analyze the `case_details` for status, priority, and description.
        - Examine `case_alerts` to understand the triggers. **Use alert event tools (like `list_events_by_alert`) for underlying event data.**
        - Review `case_comments` for analyst notes or previous actions.
        - Identify key entities from alerts or comments.
        - **Use tools to find entities associated with the case or specific alert groups within it (like `get_entities_by_alert_group_identifiers`).**
        - **Enrich findings using SIEM (`lookup_entity`, `search_security_events`), TI (`get_threat_intel`), EDR, Cloud, or other relevant security tool MCP integrations.**
        - Document investigation progress using a case commenting tool.
        - Consider adjusting case priority using a priority management tool based on findings.
        """
        case_coro = bindings.http_client.get(
            Endpoints.BASE_SPECIFIC_CASE_URL.format(CASE_ID=case_id)
        )
        case_alerts_coro = bindings.http_client.get(
            Endpoints.BASE_ALERT_URL.format(CASE_ID=case_id)
        )
        case_comments_coro = bindings.http_client.get(
            Endpoints.BASE_CASE_COMMENTS_URL.format(CASE_ID=case_id)
        )
        results = await asyncio.gather(case_coro, case_alerts_coro, case_comments_coro)
        return {
            "case_details:": results[0],
            "case_alerts": results[1],
            "case_comments": results[2],
        }
