# Google Threat Intelligence MCP Server

This is an MCP (Model Context Protocol) server for interacting with Google's
Threat Intelligence suite.
[MCP Info](https://modelcontextprotocol.io/introduction)

## Features

### IOC Reports

- `get_file_report`: Get the file's report.
- `get_entitites_related_to_a_file`: Retrieve [entities related](https://gtidocs.virustotal.com/reference/file-object) to the given file.
- `get_file_behavior_report`: Retrieves a particular file's behavioural report
- `get_file_behavior_summary`: Retrieve a summary of all the file behaviour reports from all the sandboxes runned by VirusTotal.

### Threat Actors, Malware & Tools, Campaigns, IoC Collections

- `get_collection_report`: At Google Threat Intelligence, threats are modeled as "collections". This tool retrieves them from the platform.
- `search_threats`: Search threats.

## Integration with Cline

```json
{
  "mcpServers": {
    "Google Threat Intelligence MCP server": {
      "command": "python3",
      "args": ["-m", "gti_mcp.server"],
      "env": {
        "VT_APIKEY": "$VT_APIKEY"
      },
      "disabled": false,
      "autoApprove": []
    }
  }
}
```

## License

Apache 2.0

## Development

The project is structured as follows:

- `gti_mcp/server.py`: Main MCP server implementation
- `gti_mcp/utils.py`: Utils to consume VirusTotal API using vt-py library.
- `gti_mcp/tools/`: Folder containing tools.
