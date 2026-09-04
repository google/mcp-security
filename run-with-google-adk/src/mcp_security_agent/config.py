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
"""Centralized configuration and settings for MCP Security Agent."""

from typing import Optional
from pydantic import Field, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class AgentSettings(BaseSettings):
    """Configuration settings loaded from environment variables or .env file."""
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
        populate_by_name=True,
    )

    # Google Cloud & LLM Settings
    google_cloud_project: Optional[str] = Field(default=None, alias="GOOGLE_CLOUD_PROJECT")
    google_cloud_location: str = Field(default="us-central1", alias="GOOGLE_CLOUD_LOCATION")
    use_vertex_ai: bool = Field(default=False, alias="GOOGLE_GENAI_USE_VERTEXAI")
    google_api_key: Optional[str] = Field(default=None, alias="GOOGLE_API_KEY")
    google_model: str = Field(default="gemini-2.5-flash", alias="GOOGLE_MODEL")

    # MCP Server Enablement Flags
    load_secops_mcp: bool = Field(default=False, alias="LOAD_SECOPS_MCP")
    load_scc_mcp: bool = Field(default=False, alias="LOAD_SCC_MCP")
    load_gti_mcp: bool = Field(default=False, alias="LOAD_GTI_MCP")
    load_secops_soar_mcp: bool = Field(default=False, alias="LOAD_SECOPS_SOAR_MCP")

    # Remote MCP URLs (for SSE/HTTP remote endpoints)
    secops_mcp_url: Optional[str] = Field(default=None, alias="SECOPS_MCP_URL")
    scc_mcp_url: Optional[str] = Field(default=None, alias="SCC_MCP_URL")
    gti_mcp_url: Optional[str] = Field(default=None, alias="GTI_MCP_URL")
    secops_soar_mcp_url: Optional[str] = Field(default=None, alias="SECOPS_SOAR_MCP_URL")

    # Credentials & Impersonation
    secops_sa_path: Optional[str] = Field(default=None, alias="SECOPS_SA_PATH")
    google_application_credentials: Optional[str] = Field(default=None, alias="GOOGLE_APPLICATION_CREDENTIALS")
    secops_impersonate_service_account: Optional[str] = Field(default=None, alias="SECOPS_IMPERSONATE_SERVICE_ACCOUNT")
    
    # Chronicle SIEM Params
    chronicle_project_id: Optional[str] = Field(default=None, alias="CHRONICLE_PROJECT_ID")
    chronicle_customer_id: Optional[str] = Field(default=None, alias="CHRONICLE_CUSTOMER_ID")
    chronicle_region: str = Field(default="us", alias="CHRONICLE_REGION")
    
    # GTI & SOAR Params
    vt_apikey: Optional[str] = Field(default=None, alias="VT_APIKEY")
    soar_url: Optional[str] = Field(default=None, alias="SOAR_URL")
    soar_app_key: Optional[str] = Field(default=None, alias="SOAR_APP_KEY")

    # Runtime & Logging Settings
    minimal_logging: bool = Field(default=False, alias="MINIMAL_LOGGING")
    stdio_timeout_seconds: float = Field(default=60.0, alias="STDIO_PARAM_TIMEOUT")
    default_prompt: Optional[str] = Field(default=None, alias="DEFAULT_PROMPT")

    @field_validator(
        "load_secops_mcp", "load_scc_mcp", "load_gti_mcp", "load_secops_soar_mcp",
        "use_vertex_ai", "minimal_logging",
        mode="before"
    )
    @classmethod
    def parse_bool_env(cls, value: object) -> bool:
        if isinstance(value, str):
            return value.strip().upper() in ("Y", "YES", "TRUE", "1")
        return bool(value)
