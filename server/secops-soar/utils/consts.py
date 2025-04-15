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
"""Constants used in the SOAR integration."""

ENV_SOAR_URL = "SOAR_URL"
ENV_SOAR_APP_KEY = "SOAR_APP_KEY"


class Endpoints:
    """Endpoints for SOAR."""

    EXECUTE_MANUAL_ACTION = "/api/external/v1/cases/ExecuteManualAction"
    LIST_INTEGRATION_INSTANCES = "/api/1p/external/v1/integrations/{INTEGRATION_NAME}/integrationInstances?$select=identifier"
    BASE_CASE_URL = "/api/1p/external/v1/cases"
    BASE_SPECIFIC_CASE_URL = BASE_CASE_URL + "/{CASE_ID}"
    BASE_CASE_COMMENTS_URL = BASE_SPECIFIC_CASE_URL + "/comments"
    BASE_ALERT_URL = "/api/1p/external/v1.0/cases/{CASE_ID}/alerts"
    LIST_ALERT_GROUP_IDENTIFIERS_BY_CASE = (
        BASE_ALERT_URL + "?$select=alertGroupIdentifier"
    )
    BASE_SPECIFIC_ALERT_URL = BASE_ALERT_URL + "/{ALERT_ID}"
    LIST_INVOLVED_EVENTS_BY_ALERT = BASE_SPECIFIC_ALERT_URL + "/involvedEvents"
    FETCH_FULL_UNIQUE_ENTITY = "/api/external/v1/entities/GetEntityData"
    SEARCH_ENTITY = "/api/external/v1.0/entity-search/entities"
    GET_SCOPES = "/api/external/v1/settings/GetScopes"
    GET_ALERT_GROUP_IDENTIFIERS_ENTITIES = (
        "/api/external/v1/case-overview/GetAlertsEntities"
    )
