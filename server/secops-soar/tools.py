import asyncio
from typing import Optional
import bindings
from fastmcp import FastMCP
from logger_utils import get_logger
from utils.consts import Endpoints
from utils.models import CasePriority

logger = get_logger(__name__)


def register_tools(mcp: FastMCP):
    """Registers the tools for the SecOps SOAR server."""

    @mcp.tool()
    async def list_cases() -> dict:
        """List cases."""
        return await bindings.http_client.get(Endpoints.BASE_CASE_URL)

    @mcp.tool()
    async def post_case_comment(case_id: str, comment: str) -> dict:
        """Post comment on a case."""
        return await bindings.http_client.post(
            Endpoints.BASE_CASE_COMMENTS_URL.format(CASE_ID=case_id),
            req={"Comment": comment},
        )

    @mcp.tool()
    async def list_alerts_by_case(case_id: str) -> dict:
        """List alerts by case id."""
        return await bindings.http_client.get(
            Endpoints.BASE_ALERT_URL.format(CASE_ID=case_id)
        )

    @mcp.tool()
    async def list_alert_group_identifiers_by_case(case_id: str):
        """List alert group identifiers by case id."""
        return await bindings.http_client.get(
            Endpoints.LIST_ALERT_GROUP_IDENTIFIERS_BY_CASE.format(CASE_ID=case_id)
        )

    @mcp.tool()
    async def list_events_by_alert(case_id: str, alert_id: str):
        """List events by case and alert."""
        return await bindings.http_client.get(
            Endpoints.LIST_INVOLVED_EVENTS_BY_ALERT.format(
                CASE_ID=case_id, ALERT_ID=alert_id
            )
        )

    @mcp.tool()
    async def change_case_priority(case_id: str, case_priority: CasePriority):
        """Change case priority."""
        return await bindings.http_client.patch(
            Endpoints.BASE_SPECIFIC_CASE_URL.format(CASE_ID=case_id),
            req={"Priority": case_priority.value},
        )

    @mcp.tool()
    async def get_entity_details(
        entity_identifier: str, entity_type: str, entity_environment: str
    ):
        """Get entity details."""
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
        term: Optional[str] = None,
        type: Optional[list[str]] = None,
        is_suspicious: Optional[bool] = None,
        is_internal_asset: Optional[bool] = None,
        is_enriched: Optional[bool] = None,
        network_name: Optional[list[str]] = None,
        environment_name: Optional[list[str]] = None,
    ):
        """Search for an entity."""
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
    async def get_case_full_details(case_id: str):
        """Get full details of a case."""
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
