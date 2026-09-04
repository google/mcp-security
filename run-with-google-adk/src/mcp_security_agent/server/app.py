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
"""FastAPI application factory for MCP Security Agent."""

from pathlib import Path
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from mcp_security_agent import __version__
from mcp_security_agent.server.routes import router


def create_app() -> FastAPI:
    """Creates and configures the FastAPI application.

    Returns:
        Configured FastAPI application instance.
    """
    app = FastAPI(
        title="MCP Security Agent API",
        version=__version__,
        description="Autonomous Security Operations Center (SOC) Agent API",
    )
    app.include_router(router)

    # Mount static assets if directory exists
    pkg_root = Path(__file__).resolve().parents[3]
    static_dir = pkg_root / "static"
    if static_dir.is_dir():
        app.mount("/static", StaticFiles(directory=str(static_dir)), name="static")

    return app
