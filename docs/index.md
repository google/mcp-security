# Google MCP Security documentation

Google MCP Security connects Model Context Protocol (MCP) clients and AI coding agents to Google Cloud security products. You can connect to a managed remote endpoint for Google Security Operations or run four open-source Python MCP servers locally.

## Choose your setup

Pick the deployment model that matches your environment and product coverage:

- **[Remote MCP server for Google SecOps](remote_server.md)**: Managed Google Cloud endpoint (`chronicle.googleapis.com/mcp`) for SIEM search, detection rules, alerts, and migrated SOAR workflows. Uses Application Default Credentials (ADC), Google Cloud IAM, and Cloud Audit Logs with zero local server maintenance. Recommended for Google SecOps SIEM.
- **[Local PyPI or source MCP servers](usage_guide.md)**: Four standalone `stdio` MCP servers published on PyPI (`google-secops-mcp`, `secops-soar-mcp`, `gti-mcp`, and `scc-mcp`). Run them directly with `uvx` or from a local Git checkout in Gemini CLI, Antigravity, Goose, Claude Code, Claude Desktop, Cursor, VS Code, or custom Python agents.
- **[Google ADK security agent](adk_agent.md)**: Prebuilt security operations agent (`mcp-security-agent`) built on Google Agent Development Kit (ADK) v2 with an interactive terminal REPL, a FastAPI web console, and a Cloud Run container.
- **[Google SecOps extension](google_secops_extension.md)**: Portable agent skills (`secops-triage`, `secops-investigate`, `secops-hunt`, and client setup assistants) that route across remote and local SecOps MCP tools.

## MCP servers

| Server | Package | Coverage |
| :--- | :--- | :--- |
| [Remote MCP server for Google SecOps](remote_server.md) | Managed Google Cloud service | Hosted SIEM and migrated SOAR tools over Streamable HTTP with IAM and Model Armor governance |
| [Google SecOps SIEM server](servers/secops_mcp.md) | `google-secops-mcp` | 69 tools across UDM search, YARA-L 2.0 detection rules, retrohunts, curated rules, rule exclusions, alerts, entity lookup, data tables, reference lists, watchlists, investigations, log ingestion, feeds, and parsers |
| [Google SecOps SOAR server](servers/secops_soar_mcp.md) | `secops-soar-mcp` | 17 case and entity management tools plus dynamic tool loading across [SOAR marketplace integrations](soar_integrations/index.md) |
| [Google Threat Intelligence server](servers/gti_mcp.md) | `gti-mcp` | 36 tools across threat collections, MITRE ATT&CK trees, file and sandbox behavior reports, Digital Threat Monitoring, standard YARA hunting rulesets, threat profiles, domains, IPs, and URLs |
| [Security Command Center server](servers/scc_mcp.md) | `scc-mcp` | 6 tools on the SCC v2 and Cloud Asset Inventory APIs for project or organization findings, Attack Exposure Scores, compliance filtering, remediation steps, and mute state management |

## Quick links

- **[Install and configure MCP clients](usage_guide.md#getting-started)**: Connect Gemini CLI, Antigravity, Goose, Claude Code, Claude Desktop, or VS Code using `uvx` or a local checkout.
- **[Configure corporate proxies and custom TLS CAs](usage_guide.md#corporate-proxies-and-custom-tls-certificates)**: Pass proxy variables and trust bundles to each server runtime.
- **[Explore security personas](personas/index.md)**: Review role-focused workflows for SOC analysts, threat hunters, detection engineers, CTI researchers, and incident responders.
- **[Extend or test the servers](development_guide.md)**: Add FastMCP tools, run unit tests, lint Markdown, and run the Playwright and `axe-core` WCAG 2.1 AA accessibility suite.
- **[Browse the full table of contents](toc.md)**: View every guide, server reference, and SOAR integration page in one index.

## Contribute

Contributions to the servers, agent integrations, and documentation are welcome. Read the [contribution guidelines](https://github.com/google/mcp-security/blob/main/CONTRIBUTING) before opening a pull request, and see the [development guide](development_guide.md) for local build and test commands. Source code is hosted in the [google/mcp-security GitHub repository](https://github.com/google/mcp-security).

```{toctree}
:hidden:
:maxdepth: 2
:caption: Getting started

remote_server
usage_guide
adk_agent
google_secops_extension
```

```{toctree}
:hidden:
:maxdepth: 2
:caption: MCP servers

servers/secops_mcp
servers/secops_soar_mcp
servers/gti_mcp
servers/scc_mcp
soar_integrations/index
```

```{toctree}
:hidden:
:maxdepth: 2
:caption: Workflows and reference

personas/index
development_guide
toc
```
