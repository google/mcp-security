# Copyright 2025 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""Security Operations MCP tools package."""

from .curated_rules_management import (
    get_curated_rule,
    get_curated_rule_by_name,
    get_curated_rule_set,
    list_curated_rule_set_deployments,
    list_curated_rule_sets,
    list_curated_rules,
    search_curated_detections,
    update_curated_rule_set_deployment,
)
from .data_table_management import (
    add_rows_to_data_table,
    create_data_table,
    delete_data_table_rows,
    list_data_table_rows,
)
from .entity_lookup import lookup_entity
from .feed_management import (
    create_feed,
    delete_feed,
    disable_feed,
    enable_feed,
    generate_feed_secret,
    get_feed,
    list_feeds,
    update_feed,
)
from .investigation_management import (
    fetch_associated_investigations,
    get_investigation,
    list_investigations,
    trigger_investigation,
)
from .ioc_matches import get_ioc_matches
from .log_ingestion import (
    get_available_log_types,
    ingest_raw_log,
    ingest_udm_events,
)
from .parser_management import (
    activate_parser,
    create_parser,
    deactivate_parser,
    get_parser,
    list_parsers,
    run_parser_against_sample_logs,
)
from .reference_list_management import (
    create_reference_list,
    get_reference_list,
    update_reference_list,
)
from .rule_exclusions import (
    compute_rule_exclusion_activity,
    create_rule_exclusion,
    get_rule_exclusion,
    list_rule_exclusions,
    patch_rule_exclusion,
    update_rule_exclusion_deployment,
)
from .search import search_udm
from .security_alerts import (
    do_update_security_alert,
    get_security_alert_by_id,
    get_security_alerts,
)
from .security_events import search_security_events
from .security_rules import (
    create_retrohunt,
    create_rule,
    get_detection_rule,
    get_retrohunt,
    get_rule_detections,
    list_rule_errors,
    list_security_rules,
    search_rule_alerts,
    search_security_rules,
    test_rule,
    update_rule,
    validate_rule,
)
from .threat_intel import get_threat_intel
from .udm_search import (
    export_udm_search_csv,
    find_udm_field_values,
)
from .watchlist_management import (
    create_watchlist,
    delete_watchlist,
    get_watchlist,
    list_watchlists,
    update_watchlist,
)

__all__ = [
    "activate_parser",
    "add_rows_to_data_table",
    "compute_rule_exclusion_activity",
    "create_data_table",
    "create_feed",
    "create_parser",
    "create_reference_list",
    "create_retrohunt",
    "create_rule",
    "create_rule_exclusion",
    "create_watchlist",
    "deactivate_parser",
    "delete_data_table_rows",
    "delete_feed",
    "delete_watchlist",
    "disable_feed",
    "do_update_security_alert",
    "enable_feed",
    "export_udm_search_csv",
    "fetch_associated_investigations",
    "find_udm_field_values",
    "generate_feed_secret",
    "get_available_log_types",
    "get_curated_rule",
    "get_curated_rule_by_name",
    "get_curated_rule_set",
    "get_detection_rule",
    "get_feed",
    "get_investigation",
    "get_ioc_matches",
    "get_parser",
    "get_reference_list",
    "get_retrohunt",
    "get_rule_detections",
    "get_rule_exclusion",
    "get_security_alert_by_id",
    "get_security_alerts",
    "get_threat_intel",
    "get_watchlist",
    "ingest_raw_log",
    "ingest_udm_events",
    "list_curated_rule_set_deployments",
    "list_curated_rule_sets",
    "list_curated_rules",
    "list_data_table_rows",
    "list_feeds",
    "list_investigations",
    "list_parsers",
    "list_rule_errors",
    "list_rule_exclusions",
    "list_security_rules",
    "list_watchlists",
    "lookup_entity",
    "patch_rule_exclusion",
    "run_parser_against_sample_logs",
    "search_curated_detections",
    "search_rule_alerts",
    "search_security_events",
    "search_security_rules",
    "search_udm",
    "test_rule",
    "trigger_investigation",
    "update_curated_rule_set_deployment",
    "update_feed",
    "update_reference_list",
    "update_rule",
    "update_rule_exclusion_deployment",
    "update_watchlist",
    "validate_rule",
]
