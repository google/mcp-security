#!/usr/bin/env python3
"""
AgentSpace Manager for Google MCP Security Agent

This script manages AgentSpace operations including registration, updates,
verification, and deletion of agents in AgentSpace.
"""

import json
import sys
from pathlib import Path
from typing import Any, Dict, Optional, Tuple

import google.auth
from google.auth.transport import requests as google_requests
import requests
import typer
from typing_extensions import Annotated

# Add parent directory to path for imports
sys.path.append(str(Path(__file__).parent.parent))
from scripts.env_manager import EnvManager

app = typer.Typer(
    add_completion=False,
    help="Manage AgentSpace operations for the Google MCP Security Agent.",
)

DISCOVERY_ENGINE_API_BASE = "https://discoveryengine.googleapis.com/v1alpha"


class AgentSpaceManager:
    """Manages AgentSpace configuration and operations."""

    def __init__(self, env_file: Path):
        """
        Initialize the AgentSpace manager.

        Args:
            env_file: Path to the environment file.
        """
        self.env_manager = EnvManager(env_file)
        self.env_vars = self.env_manager.env_vars
        self.creds, self.project = google.auth.default()

    def _get_access_token(self) -> Optional[str]:
        """Get Google Cloud access token."""
        if not self.creds.valid:
            self.creds.refresh(google_requests.Request())
        return self.creds.token

    def _validate_environment(self) -> Tuple[bool, list]:
        """Validate required environment variables for AgentSpace operations."""
        required_vars = [
            "AGENTSPACE_PROJECT_ID",
            "AGENTSPACE_PROJECT_NUMBER",
            "AGENTSPACE_APP_NAME",
            "AGENT_ENGINE_RESOURCE_NAME",
            "GOOGLE_CLOUD_LOCATION",
        ]
        missing = [var for var in required_vars if not self.env_vars.get(var)]
        return not missing, missing

    def _make_request(
        self, method: str, url: str, **kwargs: Any
    ) -> Optional[requests.Response]:
        """Make an authenticated request to the Discovery Engine API."""
        access_token = self._get_access_token()
        if not access_token:
            return None

        headers = {
            "Authorization": f"Bearer {access_token}",
            "Content-Type": "application/json",
            "X-Goog-User-Project": self.env_vars["AGENTSPACE_PROJECT_ID"],
        }
        headers.update(kwargs.pop("headers", {}))

        try:
            response = requests.request(method, url, headers=headers, **kwargs)
            response.raise_for_status()
            return response
        except requests.exceptions.RequestException as e:
            typer.secho(f"✗ API request failed: {e}", fg=typer.colors.RED)
            if e.response is not None:
                typer.echo(f"  Response: {e.response.text}")
            return None

    def _get_agent_api_url(self, agent_id: Optional[str] = None) -> str:
        """Construct the API URL for AgentSpace agents."""
        project_number = self.env_vars["AGENTSPACE_PROJECT_NUMBER"]
        app_name = self.env_vars["AGENTSPACE_APP_NAME"]
        collection = self.env_vars.get("AGENTSPACE_COLLECTION", "default_collection")
        assistant = self.env_vars.get("AGENTSPACE_ASSISTANT", "default_assistant")

        url = (
            f"{DISCOVERY_ENGINE_API_BASE}/projects/{project_number}/"
            f"locations/global/collections/{collection}/engines/{app_name}/"
            f"assistants/{assistant}/agents"
        )
        if agent_id:
            url += f"/{agent_id}"
        return url

    def _build_agent_config(self) -> Dict[str, Any]:
        """Build the agent configuration payload."""
        config = {
            "displayName": self.env_vars.get(
                "AGENT_DISPLAY_NAME", "Google Security Agent"
            ),
            "description": self.env_vars.get(
                "AGENT_DESCRIPTION",
                "Allows security operations on Google Security Products",
            ),
            "adk_agent_definition": {
                "tool_settings": {
                    "tool_description": self.env_vars.get(
                        "AGENT_TOOL_DESCRIPTION", "Various Tools from SIEM, SOAR and SCC"
                    )
                },
                "provisioned_reasoning_engine": {
                    "reasoning_engine": self.env_vars["AGENT_ENGINE_RESOURCE_NAME"]
                },
            },
        }
        if oauth_auth_id := self.env_vars.get("OAUTH_AUTH_ID"):
            config["adk_agent_definition"]["authorizations"] = [
                f"projects/{self.env_vars['AGENTSPACE_PROJECT_NUMBER']}/locations/global/authorizations/{oauth_auth_id}"
            ]
        return config

    def register_agent(self, force: bool = False) -> bool:
        """Register agent with AgentSpace."""
        typer.echo("Registering agent with AgentSpace...")
        is_valid, missing = self._validate_environment()
        if not is_valid:
            typer.secho(
                f"✗ Missing required variables: {', '.join(missing)}",
                fg=typer.colors.RED,
            )
            return False

        if self.env_vars.get("AGENTSPACE_AGENT_ID") and not force:
            typer.secho(
                "⚠️ Agent already registered. Use --force to re-register.",
                fg=typer.colors.YELLOW,
            )
            return False

        api_url = self._get_agent_api_url()
        agent_config = self._build_agent_config()

        response = self._make_request("POST", api_url, json=agent_config)
        if response and response.status_code == 200:
            result = response.json()
            agent_name = result.get("name", "")
            agent_id = agent_name.split("/")[-1] if agent_name else ""
            typer.secho("✓ Agent registered successfully!", fg=typer.colors.GREEN)
            typer.echo(f"  Agent Name: {agent_name}")
            typer.echo(f"  Agent ID: {agent_id}")
            if agent_id:
                self.env_manager.update_env("AGENTSPACE_AGENT_ID", agent_id)
            return True
        return False

    def update_agent(self) -> bool:
        """Update existing AgentSpace agent configuration."""
        typer.echo("Updating AgentSpace agent...")
        agent_id = self.env_vars.get("AGENTSPACE_AGENT_ID")
        if not agent_id:
            typer.secho(
                "✗ No agent registered yet. Run 'register' first.", fg=typer.colors.RED
            )
            return False

        api_url = self._get_agent_api_url(agent_id)
        agent_config = self._build_agent_config()

        response = self._make_request("PATCH", api_url, json=agent_config)
        if response and response.status_code == 200:
            typer.secho("✓ Agent updated successfully!", fg=typer.colors.GREEN)
            return True
        return False

    def verify_agent(self) -> bool:
        """Verify AgentSpace agent configuration and status."""
        typer.echo("Verifying AgentSpace configuration...")
        is_valid, missing = self._validate_environment()
        if not is_valid:
            typer.secho(
                f"✗ Missing required variables: {', '.join(missing)}",
                fg=typer.colors.RED,
            )
            return False

        agent_id = self.env_vars.get("AGENTSPACE_AGENT_ID")
        if not agent_id:
            typer.secho("⚠️ No agent registered yet.", fg=typer.colors.YELLOW)
            return False

        api_url = self._get_agent_api_url(agent_id)
        response = self._make_request("GET", api_url)
        if response and response.status_code == 200:
            typer.secho("✓ AgentSpace agent verified successfully!", fg=typer.colors.GREEN)
            return True
        return False

    def delete_agent(self, force: bool = False) -> bool:
        """Delete agent from AgentSpace."""
        agent_id = self.env_vars.get("AGENTSPACE_AGENT_ID")
        if not agent_id:
            typer.secho("✗ No agent registered to delete.", fg=typer.colors.RED)
            return True

        if not force and not typer.confirm(
            f"Are you sure you want to delete agent {agent_id}?"
        ):
            typer.echo("Cancelled.")
            return False

        api_url = self._get_agent_api_url(agent_id)
        response = self._make_request("DELETE", api_url)
        if response and response.status_code in [200, 204]:
            typer.secho("✓ Agent deleted successfully!", fg=typer.colors.GREEN)
            self.env_manager.update_env("AGENTSPACE_AGENT_ID", "")
            return True
        return False

    def display_url(self) -> None:
        """Display AgentSpace UI URL."""
        project_id = self.env_vars.get("AGENTSPACE_PROJECT_ID")
        app_name = self.env_vars.get("AGENTSPACE_APP_NAME")
        if not all([project_id, app_name]):
            typer.secho("✗ Cannot generate URL - missing configuration.", fg=typer.colors.RED)
            return

        url = f"https://console.cloud.google.com/gen-ai-studio/agentspace/apps/{app_name}?project={project_id}"
        typer.echo("AgentSpace UI URL:")
        typer.echo("=" * 80)
        typer.echo(url)
        typer.echo("=" * 80)


@app.command()
def register(
    force: Annotated[
        bool, typer.Option("--force", help="Force re-registration if agent exists.")
    ] = False,
    env_file: Annotated[
        Path, typer.Option(help="Path to the environment file.")
    ] = Path("google_mcp_security_agent/.env"),
) -> None:
    """Register the agent with AgentSpace."""
    manager = AgentSpaceManager(env_file)
    if not manager.register_agent(force):
        raise typer.Exit(code=1)


@app.command()
def update(
    env_file: Annotated[
        Path, typer.Option(help="Path to the environment file.")
    ] = Path("google_mcp_security_agent/.env"),
) -> None:
    """Update the existing AgentSpace agent configuration."""
    manager = AgentSpaceManager(env_file)
    if not manager.update_agent():
        raise typer.Exit(code=1)


@app.command()
def verify(
    env_file: Annotated[
        Path, typer.Option(help="Path to the environment file.")
    ] = Path("google_mcp_security_agent/.env"),
) -> None:
    """Verify the AgentSpace agent configuration and status."""
    manager = AgentSpaceManager(env_file)
    if not manager.verify_agent():
        raise typer.Exit(code=1)


@app.command()
def delete(
    force: Annotated[
        bool, typer.Option("--force", help="Force deletion without confirmation.")
    ] = False,
    env_file: Annotated[
        Path, typer.Option(help="Path to the environment file.")
    ] = Path("google_mcp_security_agent/.env"),
) -> None:
    """Delete the agent from AgentSpace."""
    manager = AgentSpaceManager(env_file)
    if not manager.delete_agent(force):
        raise typer.Exit(code=1)


@app.command()
def url(
    env_file: Annotated[
        Path, typer.Option(help="Path to the environment file.")
    ] = Path("google_mcp_security_agent/.env"),
) -> None:
    """Display the AgentSpace UI URL."""
    manager = AgentSpaceManager(env_file)
    manager.display_url()


if __name__ == "__main__":
    app()
