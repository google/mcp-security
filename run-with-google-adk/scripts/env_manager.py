#!/usr/bin/env python3
"""
Environment Manager for Google MCP Security Agent

This script manages environment variables for the Google MCP Security Agent,
including validation, template generation, and configuration display.
"""

import os
import sys
import uuid
from pathlib import Path
from typing import Dict, List, Optional, Tuple

import typer
from typing_extensions import Annotated

app = typer.Typer(
    add_completion=False,
    help="Manage environment configuration for the Google MCP Security Agent.",
)

# Define base directory
BASE_DIR = Path(__file__).resolve().parent.parent


class EnvManager:
    """Manages environment configuration for the Google MCP Security Agent."""

    # Define required variables for different deployment scenarios
    REQUIRED_VARS = {
        "base": ["APP_NAME", "GOOGLE_CLOUD_PROJECT", "GOOGLE_CLOUD_LOCATION"],
        "mcp_servers": {
            "secops": [
                "CHRONICLE_PROJECT_ID",
                "CHRONICLE_CUSTOMER_ID",
                "CHRONICLE_REGION",
            ],
            "gti": ["VT_APIKEY"],
            "secops_soar": ["SOAR_URL", "SOAR_APP_KEY"],
            "scc": [],  # No additional vars needed
        },
        "agent_engine": [],
        "agentspace": [
            "AGENTSPACE_PROJECT_ID",
            "AGENTSPACE_PROJECT_NUMBER",
            "AGENTSPACE_APP_NAME",
            "AGENT_ENGINE_RESOURCE_NAME",
        ],
        "oauth": ["OAUTH_CLIENT_ID", "OAUTH_CLIENT_SECRET", "OAUTH_AUTH_ID"],
        "vertex_ai": ["GOOGLE_CLOUD_PROJECT", "GOOGLE_CLOUD_LOCATION"],
        "gemini_api": ["GOOGLE_API_KEY"],
    }

    # Sensitive variables that should be masked
    SENSITIVE_VARS = [
        "GOOGLE_API_KEY",
        "VT_APIKEY",
        "SOAR_APP_KEY",
        "OAUTH_CLIENT_SECRET",
        "XDR_CLIENT_SECRET",
        "IDP_CLIENT_SECRET",
    ]

    def __init__(self, env_file: Path):
        """
        Initialize the environment manager.

        Args:
            env_file: Path to the environment file.
        """
        self.env_file = env_file
        self.env_vars = self._load_env()

    def _is_uuid(self, value: str) -> bool:
        """Check if a string is a valid UUID."""
        try:
            uuid.UUID(value)
            return True
        except ValueError:
            return False

    def _load_env(self) -> Dict[str, str]:
        """Load environment variables from file and system environment."""
        env_vars = dict(os.environ)

        if self.env_file.exists():
            with open(self.env_file, "r") as f:
                for line in f:
                    line = line.strip()
                    if line and not line.startswith("#") and "=" in line:
                        key, value = line.split("=", 1)
                        if value.startswith("'") and value.endswith("'"):
                            value = value[1:-1]
                        elif value.startswith('"') and value.endswith('"'):
                            value = value[1:-1]
                        env_vars[key.strip()] = value.strip()
        return env_vars

    def validate(self, deployment_type: str = "base") -> Tuple[bool, List[str]]:
        """
        Validate required environment variables for a deployment type.

        Args:
            deployment_type: The deployment scenario to validate against.

        Returns:
            A tuple containing a boolean indicating validity and a list of missing variables.
        """
        missing_vars = []
        required = self.REQUIRED_VARS

        # Base requirements
        missing_vars.extend(
            v for v in required["base"] if not self.env_vars.get(v)
        )

        # MCP server requirements
        for server, variables in required["mcp_servers"].items():
            if self.env_vars.get(f"LOAD_{server.upper()}_MCP") == "true":
                for var in variables:
                    value = self.env_vars.get(var)
                    if not value or value == "NOT_SET":
                        missing_vars.append(var)
                    elif var == "CHRONICLE_CUSTOMER_ID" and not self._is_uuid(value):
                        missing_vars.append(f"{var} (must be a valid UUID4)")
                    elif var == "SOAR_URL" and not value.startswith("https://"):
                        missing_vars.append(f"{var} (must start with https://)")
                    elif var == "SOAR_APP_KEY" and not self._is_uuid(value):
                        missing_vars.append(f"{var} (must be a valid UUID)")

        # Deployment-specific requirements
        if deployment_type in required:
            missing_vars.extend(
                v for v in required[deployment_type] if not self.env_vars.get(v)
            )

        # LLM provider requirements
        if self.env_vars.get("GOOGLE_GENAI_USE_VERTEXAI") == "True":
            missing_vars.extend(
                v for v in required["vertex_ai"] if not self.env_vars.get(v)
            )
        else:
            missing_vars.extend(
                v
                for v in required["gemini_api"]
                if not self.env_vars.get(v) or self.env_vars.get(v) == "NOT_SET"
            )

        return not missing_vars, sorted(list(set(missing_vars)))

    def mask_value(self, key: str, value: str) -> str:
        """Mask sensitive values for display."""
        if key in self.SENSITIVE_VARS and value and value != "NOT_SET":
            return "*" * len(value)
        return value

    def display_config(self, show_all: bool = False) -> None:
        """Display current configuration with sensitive values masked."""
        typer.echo("=" * 60)
        typer.echo("Google MCP Security Agent Configuration")
        typer.echo("=" * 60)
        typer.echo()

        categories = {
            "Core Configuration": [
                "APP_NAME",
                "GOOGLE_CLOUD_PROJECT",
                "GOOGLE_CLOUD_LOCATION",
                "GOOGLE_MODEL",
                "GOOGLE_GENAI_USE_VERTEXAI",
            ],
            "MCP Servers": [
                "LOAD_SECOPS_MCP",
                "CHRONICLE_PROJECT_ID",
                "CHRONICLE_CUSTOMER_ID",
                "CHRONICLE_REGION",
                "LOAD_GTI_MCP",
                "VT_APIKEY",
                "LOAD_SECOPS_SOAR_MCP",
                "SOAR_URL",
                "SOAR_APP_KEY",
                "LOAD_SCC_MCP",
            ],
            "Agent Engine": [
                "AGENT_ENGINE_RESOURCE_NAME",
                "GCS_STAGING_BUCKET",
                "AGENT_DISPLAY_NAME",
                "AGENT_DESCRIPTION",
            ],
            "AgentSpace": [
                "AGENTSPACE_PROJECT_ID",
                "AGENTSPACE_PROJECT_NUMBER",
                "AGENTSPACE_APP_NAME",
                "AGENTSPACE_COLLECTION",
                "AGENTSPACE_ASSISTANT",
                "AGENTSPACE_AGENT_ID",
            ],
            "OAuth": [
                "OAUTH_CLIENT_ID",
                "OAUTH_CLIENT_SECRET",
                "OAUTH_AUTH_ID",
                "OAUTH_REDIRECT_URI",
                "OAUTH_TOKEN_URI",
            ],
        }

        for category, variables in categories.items():
            typer.echo(f"{category}:")
            typer.echo("-" * 40)
            displayed_any = False
            for var in variables:
                value = self.env_vars.get(var)
                if value or show_all:
                    masked_value = self.mask_value(var, value) if value else "<not set>"
                    typer.echo(f"  {var}: {masked_value}")
                    displayed_any = True
            if not displayed_any:
                typer.echo("  <no values set>")
            typer.echo()

    def update_env(self, key: str, value: str) -> None:
        """Update a single environment variable in the .env file."""
        self.env_vars[key] = value
        self._save_env()
        typer.echo(f"✓ Updated {key}")

    def _save_env(self) -> None:
        """Save environment variables back to the .env file."""
        lines = self.env_file.read_text().splitlines() if self.env_file.exists() else []

        updated_keys = set()
        new_lines = []

        for line in lines:
            stripped = line.strip()
            if stripped and not stripped.startswith("#") and "=" in stripped:
                line_key = stripped.split("=", 1)[0].strip()
                if line_key in self.env_vars:
                    if line_key == "DEFAULT_PROMPT":
                        new_lines.append(f"{line_key}='{self.env_vars[line_key]}'")
                    else:
                        new_lines.append(f"{line_key}={self.env_vars[line_key]}")
                    updated_keys.add(line_key)
                else:
                    new_lines.append(line)
            else:
                new_lines.append(line)

        for key, value in self.env_vars.items():
            if key not in updated_keys and not key.startswith("_") and key.isupper():
                if key == "DEFAULT_PROMPT":
                    new_lines.append(f"\n{key}='{value}'")
                else:
                    new_lines.append(f"\n{key}={value}")

        self.env_file.write_text("\n".join(new_lines) + "\n")


@app.command()
def check(
    deployment: Annotated[
        str,
        typer.Option(
            help="Deployment type to validate.",
            case_sensitive=False,
        ),
    ] = "base",
    env_file: Annotated[
        Path,
        typer.Option(help="Path to the environment file."),
    ] = BASE_DIR / "agents" / "google_mcp_security_agent" / ".env",
) -> None:
    """Validate the environment configuration for a given deployment type."""
    manager = EnvManager(env_file)
    is_valid, missing = manager.validate(deployment)
    if not is_valid:
        typer.secho(
            f"✗ Environment validation failed for {deployment}", fg=typer.colors.RED
        )
        typer.echo(f"  Missing variables: {', '.join(missing)}")
        raise typer.Exit(code=1)
    else:
        typer.secho(f"✓ Environment valid for {deployment}", fg=typer.colors.GREEN)


@app.command()
def show(
    all_vars: Annotated[
        bool,
        typer.Option("--all", help="Show all variables, including unset ones."),
    ] = False,
    env_file: Annotated[
        Path,
        typer.Option(help="Path to the environment file."),
    ] = BASE_DIR / "agents" / "google_mcp_security_agent" / ".env",
) -> None:
    """Display the current configuration, masking sensitive values."""
    manager = EnvManager(env_file)
    manager.display_config(all_vars)


@app.command()
def update(
    key: Annotated[str, typer.Option(help="Environment variable key to update.")],
    value: Annotated[str, typer.Option(help="New value for the variable.")],
    env_file: Annotated[
        Path,
        typer.Option(help="Path to the environment file."),
    ] = BASE_DIR / "agents" / "google_mcp_security_agent" / ".env",
) -> None:
    """Update a variable in the environment file."""
    manager = EnvManager(env_file)
    manager.update_env(key, value)


if __name__ == "__main__":
    app()
