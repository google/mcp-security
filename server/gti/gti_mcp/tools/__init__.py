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
"""Google Threat Intelligence MCP tools package."""

from .collections import (
    COLLECTION_EXCLUDED_ATTRS,
    COLLECTION_KEY_RELATIONSHIPS,
    COLLECTION_RELATIONSHIPS,
    COLLECTION_TYPES,
    create_collection,
    get_collection_feature_matches,
    get_collection_mitre_tree,
    get_collection_report,
    get_collection_rules,
    get_collection_timeline_events,
    get_collections_commonalities,
    get_entities_related_to_a_collection,
    search_campaigns,
    search_malware_families,
    search_software_toolkits,
    search_threat_actors,
    search_threat_reports,
    search_threats,
    search_vulnerabilities,
    update_collection_attributes,
    update_iocs_in_collection,
)
from .files import (
    FILE_KEY_RELATIONSHIPS,
    FILE_RELATIONSHIPS,
    analyse_file,
    get_entities_related_to_a_file,
    get_file_behavior_report,
    get_file_behavior_summary,
    get_file_report,
    search_digital_threat_monitoring,
)
from .intelligence import (
    HUNTING_RULESET_RELATIONSHIPS,
    get_entities_related_to_a_hunting_ruleset,
    get_hunting_ruleset,
    search_iocs,
)
from .netloc import (
    DOMAIN_KEY_RELATIONSHIPS,
    DOMAIN_RELATIONSHIPS,
    IP_KEY_RELATIONSHIPS,
    IP_RELATIONSHIPS,
    get_domain_report,
    get_entities_related_to_a_domain,
    get_entities_related_to_an_ip_address,
    get_ip_address_report,
)
from .threat_profiles import (
    get_threat_profile,
    get_threat_profile_associations_timeline,
    get_threat_profile_recommendations,
    list_threat_profiles,
)
from .urls import (
    URL_KEY_RELATIONSHIPS,
    URL_RELATIONSHIPS,
    get_entities_related_to_an_url,
    get_url_report,
    url_to_base64,
)

__all__ = [
    "COLLECTION_EXCLUDED_ATTRS",
    "COLLECTION_KEY_RELATIONSHIPS",
    "COLLECTION_RELATIONSHIPS",
    "COLLECTION_TYPES",
    "DOMAIN_KEY_RELATIONSHIPS",
    "DOMAIN_RELATIONSHIPS",
    "FILE_KEY_RELATIONSHIPS",
    "FILE_RELATIONSHIPS",
    "HUNTING_RULESET_RELATIONSHIPS",
    "IP_KEY_RELATIONSHIPS",
    "IP_RELATIONSHIPS",
    "URL_KEY_RELATIONSHIPS",
    "URL_RELATIONSHIPS",
    "analyse_file",
    "create_collection",
    "get_collection_feature_matches",
    "get_collection_mitre_tree",
    "get_collection_report",
    "get_collection_rules",
    "get_collection_timeline_events",
    "get_collections_commonalities",
    "get_domain_report",
    "get_entities_related_to_a_collection",
    "get_entities_related_to_a_domain",
    "get_entities_related_to_a_file",
    "get_entities_related_to_a_hunting_ruleset",
    "get_entities_related_to_an_ip_address",
    "get_entities_related_to_an_url",
    "get_file_behavior_report",
    "get_file_behavior_summary",
    "get_file_report",
    "get_hunting_ruleset",
    "get_ip_address_report",
    "get_threat_profile",
    "get_threat_profile_associations_timeline",
    "get_threat_profile_recommendations",
    "get_url_report",
    "list_threat_profiles",
    "search_campaigns",
    "search_digital_threat_monitoring",
    "search_iocs",
    "search_malware_families",
    "search_software_toolkits",
    "search_threat_actors",
    "search_threat_reports",
    "search_threats",
    "search_vulnerabilities",
    "update_collection_attributes",
    "update_iocs_in_collection",
    "url_to_base64",
]
