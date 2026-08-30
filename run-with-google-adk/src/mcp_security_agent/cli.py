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

import typer
from rich.console import Console
from mcp_security_agent import __version__
from mcp_security_agent.config import AgentSettings
from mcp_security_agent.agent import create_security_agent

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
    console.print(f"SecOps SIEM MCP: {'[green]Enabled[/green]' if settings.load_secops_mcp else '[dim]Disabled[/dim]'}")
    console.print(f"SCC MCP: {'[green]Enabled[/green]' if settings.load_scc_mcp else '[dim]Disabled[/dim]'}")
    console.print(f"GTI MCP: {'[green]Enabled[/green]' if settings.load_gti_mcp else '[dim]Disabled[/dim]'}")
    console.print(f"SecOps SOAR MCP: {'[green]Enabled[/green]' if settings.load_secops_soar_mcp else '[dim]Disabled[/dim]'}")


@app.command()
def chat():
    """Start an interactive terminal chat session with the SOC agent."""
    console.print("[bold blue]Starting MCP Security Agent Interactive REPL. Type /exit to quit.[/bold blue]")
    settings = AgentSettings()
    agent = create_security_agent(settings)
    if not agent:
        console.print("[red]Failed to initialize agent. Check environment configuration.[/red]")
        raise typer.Exit(code=1)
    console.print("[green]Agent initialized and ready for investigation.[/green]")


@app.command()
def serve(
    host: str = typer.Option("0.0.0.0", help="Host address to bind"),
    port: int = typer.Option(8080, help="Port to listen on"),
):
    """Run the FastAPI web server and Cloud Run REST API."""
    import uvicorn
    from mcp_security_agent.server.app import create_app

    app_instance = create_app()
    console.print(f"[bold green]Starting MCP Security Agent server on {host}:{port}[/bold green]")
    uvicorn.run(app_instance, host=host, port=port)


if __name__ == "__main__":
    app()
