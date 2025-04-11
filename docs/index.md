# Google MCP Security Documentation

Welcome to the documentation for the Google MCP Security project. This project provides Model Context Protocol (MCP) servers that enable MCP-compatible AI assistants like Claude to access Google's security products and services.

## Project Overview

This repository contains four MCP servers that provide access to different Google security products:

1. **Google Security Operations (Chronicle)** - For threat detection, investigation, and hunting
2. **Google Security Operations SOAR** - For security orchestration, automation, and response
3. **Google Threat Intelligence (GTI)** - For access to Google's threat intelligence data
4. **Security Command Center (SCC)** - For cloud security and risk management

These servers allow security professionals to leverage AI assistants for security tasks, enhancing productivity and enabling natural language interactions with security tools.

## Navigation

👉 Use the navigation menu on the left to explore the documentation.

If you're new to this project, we recommend starting with the [Usage Guide](usage_guide.md) to learn how to set up and configure the MCP servers.

## Quick Links

- **[Installation & Setup](usage_guide.md#getting-started)** - Get started quickly with installation instructions
- **[Configuration Reference](usage_guide.md#mcp-server-configuration-reference)** - Configure the MCP servers for your environment
- **[Usage Examples](usage_guide.md#usage-examples)** - See examples of how to interact with the MCP servers
- **[Development Guide](development_guide.md)** - Learn how to contribute to or extend the project

## MCP Servers

Each server provides different capabilities:

- [Google Threat Intelligence (GTI) Server](servers/gti_mcp.md) - Access threat intelligence about IoCs, malware, and threat actors
- [Security Command Center (SCC) Server](servers/scc_mcp.md) - Manage cloud security posture and vulnerabilities
- [Chronicle Security Operations (SecOps) Server](servers/secops_mcp.md) - Search and analyze security events and alerts
- [SecOps SOAR Server](servers/secops_soar_mcp.md) - Manage security cases and automate response actions

## Example Use Cases

- Investigate suspicious IPs, files, or domains using Google Threat Intelligence
- Identify and remediate critical vulnerabilities in your Google Cloud environment
- Search for security events across your enterprise using natural language
- Automate security response workflows and case management

## Contributing

We welcome contributions to improve these MCP servers and their documentation. Please review our [CONTRIBUTING](../CONTRIBUTING) file for guidelines on how to contribute to this project. For technical details on extending or modifying the servers, see the [Development Guide](development_guide.md).
