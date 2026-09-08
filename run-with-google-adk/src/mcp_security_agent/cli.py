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
"""Command-line interface for the MCP Security Agent."""

import asyncio
import os
import sys
from pathlib import Path
from typing import Optional
import typer
from rich.console import Console
from mcp_security_agent import __version__
from mcp_security_agent.config import AgentSettings

app = typer.Typer(
    help="Autonomous Security Operations Center (SOC) Agent powered by Google ADK v2 & MCP",
    no_args_is_help=True,
)
console = Console()


@app.command()
def info():
    """Display agent version and loaded configuration."""
    settings = AgentSettings()
    console.print(f"[bold green]MCP Security Agent v{__version__}[/bold green]")
    console.print(f"Model: [cyan]{settings.google_model}[/cyan]")
    console.print(f"Project: [cyan]{settings.google_cloud_project or os.environ.get('GOOGLE_CLOUD_PROJECT', 'Not set')}[/cyan]")
    console.print(f"ADC: [cyan]{settings.google_application_credentials or 'Default (~/.config/gcloud/...)'}[/cyan]")
    console.print(f"SecOps SIEM MCP: {'[green]Enabled[/green]' if settings.load_secops_mcp else '[dim]Disabled[/dim]'}")
    console.print(f"SCC MCP: {'[green]Enabled[/green]' if settings.load_scc_mcp else '[dim]Disabled[/dim]'}")
    console.print(f"GTI MCP: {'[green]Enabled[/green]' if settings.load_gti_mcp else '[dim]Disabled[/dim]'}")
    console.print(f"SecOps SOAR MCP: {'[green]Enabled[/green]' if settings.load_secops_soar_mcp else '[dim]Disabled[/dim]'}")



def _apply_cli_overrides(
    secops: Optional[bool] = None,
    scc: Optional[bool] = None,
    gti: Optional[bool] = None,
    soar: Optional[bool] = None,
    vertex: Optional[bool] = None,
    model: Optional[str] = None,
    project: Optional[str] = None,
    customer_id: Optional[str] = None,
) -> None:
    """Applies CLI flag overrides to environment variables before settings initialization."""
    if secops is not None:
        os.environ["LOAD_SECOPS_MCP"] = "Y" if secops else "N"
    if scc is not None:
        os.environ["LOAD_SCC_MCP"] = "Y" if scc else "N"
    if gti is not None:
        os.environ["LOAD_GTI_MCP"] = "Y" if gti else "N"
    if soar is not None:
        os.environ["LOAD_SECOPS_SOAR_MCP"] = "Y" if soar else "N"
    if vertex is not None:
        os.environ["GOOGLE_GENAI_USE_VERTEXAI"] = "TRUE" if vertex else "FALSE"
    if model:
        os.environ["GOOGLE_MODEL"] = model
    if project:
        os.environ["GOOGLE_CLOUD_PROJECT"] = project
        if "CHRONICLE_PROJECT_ID" not in os.environ:
            os.environ["CHRONICLE_PROJECT_ID"] = project
    if customer_id:
        os.environ["CHRONICLE_CUSTOMER_ID"] = customer_id


def _display_active_toolsets(settings: AgentSettings) -> None:
    enabled_tools = []
    if settings.load_secops_mcp:
        enabled_tools.append("SecOps SIEM")
    if settings.load_scc_mcp:
        enabled_tools.append("SCC")
    if settings.load_gti_mcp:
        enabled_tools.append("GTI")
    if settings.load_secops_soar_mcp:
        enabled_tools.append("SecOps SOAR")

    if not enabled_tools:
        console.print(
            "[bold yellow]Warning:[/bold yellow] No MCP tools are currently enabled.\n"
            "Enable tools using environment variables (e.g. [cyan]LOAD_SECOPS_MCP=Y[/cyan]), "
            "CLI flags ([cyan]--secops[/cyan], [cyan]--scc[/cyan]), or [cyan].env[/cyan].\n"
        )
    else:
        console.print(f"[bold green]Active MCP Toolsets:[/bold green] {', '.join(enabled_tools)}\n")


@app.command()
def chat(
    query: Optional[str] = typer.Argument(None, help="Optional single-turn investigation query to execute"),
    secops: Optional[bool] = typer.Option(None, "--secops/--no-secops", help="Enable or disable SecOps SIEM MCP"),
    scc: Optional[bool] = typer.Option(None, "--scc/--no-scc", help="Enable or disable SCC MCP"),
    gti: Optional[bool] = typer.Option(None, "--gti/--no-gti", help="Enable or disable GTI MCP"),
    soar: Optional[bool] = typer.Option(None, "--soar/--no-soar", help="Enable or disable SecOps SOAR MCP"),
    vertex: Optional[bool] = typer.Option(None, "--vertex/--no-vertex", help="Use Vertex AI for LLM requests"),
    model: Optional[str] = typer.Option(None, "--model", help="Gemini model to use (e.g. gemini-2.5-flash)"),
    project: Optional[str] = typer.Option(None, "--project", help="Google Cloud project ID"),
    customer_id: Optional[str] = typer.Option(None, "--customer-id", help="Chronicle Customer ID (UUID)"),
):
    """Start an interactive terminal chat session with the SOC agent powered by ADK v2."""
    _apply_cli_overrides(
        secops=secops,
        scc=scc,
        gti=gti,
        soar=soar,
        vertex=vertex,
        model=model,
        project=project,
        customer_id=customer_id,
    )

    settings = AgentSettings()
    _display_active_toolsets(settings)

    import mcp_security_agent.agent as agent_mod
    agent = agent_mod.create_security_agent(settings)
    agent_mod.root_agent = agent
    if "mcp_security_agent" in sys.modules:
        sys.modules["mcp_security_agent"].root_agent = agent

    try:
        from google.adk.cli.cli import run_cli, run_once_cli
    except (ImportError, ModuleNotFoundError):
        console.print("[red]Google ADK CLI runner is unavailable in this environment.[/red]")
        raise typer.Exit(code=1)

    pkg_root = Path(__file__).resolve().parents[2]
    src_dir = pkg_root / "src"

    if query:
        exit_code = asyncio.run(
            run_once_cli(
                agent_parent_dir=str(src_dir),
                agent_folder_name="mcp_security_agent",
                query=query,
                use_local_storage=True,
            )
        )
        raise typer.Exit(code=exit_code or 0)
    else:
        asyncio.run(
            run_cli(
                agent_parent_dir=str(src_dir),
                agent_folder_name="mcp_security_agent",
                save_session=False,
                use_local_storage=True,
            )
        )


@app.command()
def serve(
    host: str = typer.Option("0.0.0.0", help="Host address to bind"),
    port: Optional[int] = typer.Option(None, help="Port to listen on (defaults to $PORT or 8080)"),
    reload: bool = typer.Option(False, "--reload", help="Enable auto-reload for development"),
    secops: Optional[bool] = typer.Option(None, "--secops/--no-secops", help="Enable or disable SecOps SIEM MCP"),
    scc: Optional[bool] = typer.Option(None, "--scc/--no-scc", help="Enable or disable SCC MCP"),
    gti: Optional[bool] = typer.Option(None, "--gti/--no-gti", help="Enable or disable GTI MCP"),
    soar: Optional[bool] = typer.Option(None, "--soar/--no-soar", help="Enable or disable SecOps SOAR MCP"),
    vertex: Optional[bool] = typer.Option(None, "--vertex/--no-vertex", help="Use Vertex AI for LLM requests"),
    model: Optional[str] = typer.Option(None, "--model", help="Gemini model to use (e.g. gemini-2.5-flash)"),
    project: Optional[str] = typer.Option(None, "--project", help="Google Cloud project ID"),
    customer_id: Optional[str] = typer.Option(None, "--customer-id", help="Chronicle Customer ID (UUID)"),
):
    """Run the FastAPI web server and Cloud Run REST API."""
    _apply_cli_overrides(
        secops=secops,
        scc=scc,
        gti=gti,
        soar=soar,
        vertex=vertex,
        model=model,
        project=project,
        customer_id=customer_id,
    )

    settings = AgentSettings()
    _display_active_toolsets(settings)

    import mcp_security_agent.agent as agent_mod
    agent = agent_mod.create_security_agent(settings)
    agent_mod.root_agent = agent
    if "mcp_security_agent" in sys.modules:
        sys.modules["mcp_security_agent"].root_agent = agent

    bind_port = port if port is not None else int(os.environ.get("PORT", 8080))
    console.print(f"[bold green]Starting MCP Security Agent server on {host}:{bind_port}[/bold green]")

    import uvicorn
    if reload:
        uvicorn.run("mcp_security_agent.server.app:create_app", factory=True, host=host, port=bind_port, reload=True)
    else:
        from mcp_security_agent.server.app import create_app
        app_instance = create_app()
        uvicorn.run(app_instance, host=host, port=bind_port)


if __name__ == "__main__":
    app()
