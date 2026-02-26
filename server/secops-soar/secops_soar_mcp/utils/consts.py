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

import platform
import sys

ENV_SOAR_URL = "SOAR_URL"
ENV_SOAR_APP_KEY = "SOAR_APP_KEY"

# Python version info for certifi fix instructions
_PYTHON_MINOR = f"{sys.version_info.major}.{sys.version_info.minor}"

SSL_CERTIFI_ERROR_MESSAGE = (
    "SSL certificate verification failed when connecting to SOAR.\n"
    "This is commonly caused by missing or outdated CA certificates in your "
    "Python installation.\n\n"
    "To fix this issue:\n"
    + (
        f"  macOS:  Run: /Applications/Python\\ {_PYTHON_MINOR}/Install\\ Certificates.command\n"
        if platform.system() == "Darwin"
        else ""
    )
    + "  All platforms: pip install --upgrade certifi\n"
    "  Then restart the MCP server.\n\n"
    "For more details, see: "
    "https://google.github.io/mcp-security/usage_guide.html"
    "#mcp-server-configuration-reference"
)

SSL_GENERIC_ERROR_MESSAGE = (
    "An SSL/TLS error occurred when connecting to SOAR: {error}\n"
    "Please verify that your SOAR_URL is correct and the server's "
    "SSL certificate is valid."
)

CONNECTION_ERROR_MESSAGE = (
    "Failed to connect to SOAR at '{url}'.\n"
    "Please verify that:\n"
    "  1. The SOAR_URL environment variable is set correctly.\n"
    "  2. The SOAR server is reachable from your network.\n"
    "  3. Any required VPN or proxy is active."
)

CREDENTIALS_ERROR_MESSAGE = (
    "Failed to fetch valid scopes from SOAR.\n"
    "Please make sure you have configured the right SOAR credentials:\n"
    "  1. SOAR_URL is set and correct.\n"
    "  2. SOAR_APP_KEY is set and valid.\n"
    "Shutting down..."
)


class Endpoints:
    """Endpoints for SOAR."""

    EXECUTE_MANUAL_ACTION = "/api/external/v1/cases/ExecuteManualAction"
    LIST_INTEGRATION_INSTANCES = "/api/1p/external/v1/integrations/{INTEGRATION_NAME}/integrationInstances?$select=identifier"
    BASE_CASE_URL = "/api/1p/external/v1/cases"
    BASE_SPECIFIC_CASE_URL = BASE_CASE_URL + "/{CASE_ID}"
    BASE_CASE_COMMENTS_URL = BASE_SPECIFIC_CASE_URL + "/comments"
    BASE_ALERT_URL = "/api/1p/external/v1.0/cases/{CASE_ID}/caseAlerts"
    LIST_ALERT_GROUP_IDENTIFIERS_BY_CASE = (
        BASE_ALERT_URL + "?$select=alertGroupIdentifier"
    )
    BASE_SPECIFIC_ALERT_URL = BASE_ALERT_URL + "/{ALERT_ID}"
    FETCH_FULL_UNIQUE_ENTITY = "/api/external/v1/entities/GetEntityData"
    SEARCH_ENTITY = "/api/external/v1.0/entity-search/entities"
    GET_SCOPES = "/api/external/v1/settings/GetScopes"
    GET_ALERT_GROUP_IDENTIFIERS_ENTITIES = (
        "/api/external/v1/case-overview/GetAlertsEntities"
    )
    # the below endpoint uses 'alerts' instead of 'caseAlerts', because of a bug that was introduced to the SOAR server
    LIST_INVOLVED_EVENTS_BY_ALERT = (
        "/api/1p/external/v1.0/cases/{CASE_ID}/alerts/{ALERT_ID}/involvedEvents"
    )
