# Development Guide

This guide provides information for developers who want to extend or modify the MCP servers in this repository.

## Project Structure

The repository is organized as follows:

```
mcp-security/
├── docs/                 # Documentation
│   ├── servers/          # Server-specific documentation
│   └── img/              # Images for documentation
├── server/               # Server implementations
│   ├── gti/              # Google Threat Intelligence server
│   ├── scc/              # Security Command Center server
│   ├── secops/           # Security Operations server
│   └── secops-soar/      # SOAR server
└── README.md             # Repository README
```

## MCP Server Architecture

Each MCP server follows a similar structure:

1. **Server Entry Point**: The main server script that handles MCP protocol interactions
2. **Tools Module**: Contains the functions exposed as MCP tools
3. **Utilities**: Helper functions and API clients

### Example: GTI Server Structure

```
server/gti/
├── gti_mcp/             # Main package
│   ├── server.py        # MCP server implementation
│   ├── utils.py         # Utility functions
│   └── tools/           # Tool implementations
│       ├── __init__.py
│       ├── collections.py
│       ├── files.py
│       └── ...
├── pyproject.toml       # Project metadata
├── setup.py             # Installation script
└── README.md            # Server-specific README
```

## Adding a New Tool

To add a new tool to an existing server:

1. Identify the appropriate server and tools module
2. Add your tool function with proper type annotations
3. Register the tool in the server's tool registry
4. Update the documentation in the corresponding `docs/servers/*.md` file

### Example: Adding a Tool to GTI

```python
# In server/gti/gti_mcp/tools/files.py

def new_file_tool(file_hash: str) -> dict:
    """
    Description of what the new tool does.
    
    Args:
        file_hash: Description of the parameter
        
    Returns:
        A dictionary containing the relevant information
    """
    # Implementation goes here
    ...
    return result
```

Then register it in `__init__.py`:

```python
from .files import get_file_report, get_entities_related_to_a_file, new_file_tool

__all__ = [
    "get_file_report", 
    "get_entities_related_to_a_file",
    "new_file_tool"
]
```

## Creating a New MCP Server

To create a new MCP server:

1. Create a new directory under `server/`
2. Implement the server following the MCP specification
3. Create appropriate documentation in `docs/servers/`
4. Update the table of contents in `docs/toc.md`

## Testing

For each server, you should test:

1. **Tool Functionality**: Ensure each tool works as expected
2. **MCP Protocol Compliance**: Test compatibility with MCP clients
3. **Error Handling**: Verify graceful error handling

## Documentation Standards

When documenting tools:

1. Include clear descriptions of what each tool does
2. Document all parameters with types and descriptions
3. Explain the return values and any side effects
4. Provide examples of how to use the tool

## Building Documentation

The documentation uses Sphinx with MyST Markdown. To build the docs:

1. Install dependencies:
   ```bash
   cd docs
   pip install -r requirements.txt
   ```

2. Build the documentation:
   ```bash
   make html
   ```

3. The built documentation will be in `docs/_build/html/`

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Update documentation
5. Submit a pull request

## Best Practices

- Follow Python PEP 8 style guidelines
- Add type annotations to all functions
- Write clear docstrings
- Handle errors gracefully
- Keep MCP tools focused on a single responsibility 