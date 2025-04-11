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
import bindings
from mcp.server.fastmcp import FastMCP
from utils.consts import Endpoints
from utils.models import CasePriority
from logger_utils import get_logger
from typing import Annotated, Optional, List
from pydantic import Field

logger = get_logger(__name__)


def register_tools(mcp: FastMCP):
    @mcp.tool()
    async def list_cases() -> dict:
        """List cases"""
        return await bindings.http_client.get(Endpoints.BASE_CASE_URL)

    @mcp.tool()
    async def post_case_comment(
        case_id: Annotated[str, Field(..., description="The ID of the case.")],
        comment: Annotated[
            str, Field(..., description="The comment we wish to add to the case.")
        ],
    ) -> dict:
        """Post comment on a case"""
        return await bindings.http_client.post(
            Endpoints.BASE_CASE_COMMENTS_URL.format(CASE_ID=case_id),
            req={"Comment": comment},
        )

    @mcp.tool()
    async def list_alerts_by_case(
        case_id: Annotated[str, Field(..., description="The ID of the case.")],
    ) -> dict:
        """List alerts by case id"""
        return await bindings.http_client.get(
            Endpoints.BASE_ALERT_URL.format(CASE_ID=case_id)
        )

    @mcp.tool()
    async def list_alert_group_identifiers_by_case(
        case_id: Annotated[str, Field(..., description="The ID of the case.")],
    ):
        """List alert group identifiers by case id"""
        return await bindings.http_client.get(
            Endpoints.LIST_ALERT_GROUP_IDENTIFIERS_BY_CASE.format(CASE_ID=case_id)
        )

    @mcp.tool()
    async def list_events_by_alert(
        case_id: Annotated[str, Field(..., description="The ID of the case.")],
        alert_id: Annotated[str, Field(..., description="The ID of the alert.")],
    ):
        """List events by case and alert"""
        return await bindings.http_client.get(
            Endpoints.LIST_INVOLVED_EVENTS_BY_ALERT.format(
                CASE_ID=case_id, ALERT_ID=alert_id
            )
        )

    @mcp.tool()
    async def change_case_priority(
        case_id: Annotated[str, Field(..., description="The ID of the case.")],
        case_priority: Annotated[
            CasePriority, Field(..., description="The priority of the case.")
        ],
    ):
        """Change case priority"""
        return await bindings.http_client.patch(
            Endpoints.BASE_SPECIFIC_CASE_URL.format(CASE_ID=case_id),
            req={"Priority": case_priority.value},
        )

    @mcp.tool()
    async def get_entities_by_alert_group_identifiers(
        case_id: Annotated[str, Field(..., description="The ID of the case.")],
        alert_group_identifiers: Annotated[
            List[str], Field(..., description="Identifiers for the alert groups.")
        ],
    ):
        """Get alerts' involved entities. Can also be used to retrieve the target_entities for a manual action"""
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
        """Get entity details"""
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
        """Search for an entity"""
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
        """Get full details of a case"""
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
