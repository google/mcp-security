# Development guide

This guide covers the repository layout, FastMCP tool registration conventions, unit testing, and documentation accessibility checks for contributors extending Google MCP Security.

## Repository structure

```text
mcp-security/
├── docs/                       # Sphinx + Furo documentation site
│   ├── _templates/             # Accessible Furo HTML landmark overrides
│   ├── img/                    # Logos and documentation diagrams
│   ├── personas/               # Role-focused SOC workflow guides
│   ├── servers/                # MCP server tool reference pages
│   ├── soar_integrations/      # Generated SOAR marketplace tool pages
│   ├── tests/                  # Static HTML + Playwright axe-core WCAG AA tests
│   ├── Makefile                # Build, Markdown lint, and accessibility targets
│   └── conf.py                 # Sphinx configuration and HTML post-processing
├── extensions/
│   └── google-secops/          # Portable Agent Skills and remote/local tool map
├── run-with-google-adk/        # Google ADK v2 security agent (mcp-security-agent)
│   ├── src/mcp_security_agent/ # CLI, FastAPI server, and MCP toolset wiring
│   ├── sample_servers_to_integrate/
│   └── tests/                  # Hermetic ADK agent unit tests
└── server/                     # Standalone Python FastMCP servers
    ├── gti/                    # Google Threat Intelligence (gti-mcp)
    ├── scc/                    # Security Command Center v2 (scc-mcp)
    ├── secops/                 # Google SecOps SIEM (google-secops-mcp)
    └── secops-soar/            # Google SecOps SOAR (secops-soar-mcp)
```

## MCP server architecture

All four servers under `server/` use `FastMCP` (`mcp>=1.x,<2.0`) over `stdio` transport:

1. **Server instance (`server.py` or `scc_mcp.py`)**: Instantiates `FastMCP`, configures logging to `stderr`, builds authenticated API clients, and calls `server.run(transport="stdio")`.
2. **Tool modules (`tools/*.py` or `case_management.py` + `marketplace/*.py`)**: Decorate functions with `@server.tool()` (or `@mcp.tool()`) and expose typed parameters and Google-style docstrings that FastMCP compiles into MCP JSON Schemas.
3. **Package metadata (`pyproject.toml` and `setup.py`)**: Declares dependencies (keeping `mcp<2.0` pinned across both files) and console script entry points (`secops_mcp`, `gti_mcp`, `scc_mcp`, and `secops_soar_mcp`).

### Example: Add a tool to `server/gti`

1. Define an async or sync function decorated with `@server.tool()` in the appropriate module under `server/gti/gti_mcp/tools/`. Use `Optional[T] = None` whenever a parameter defaults to `None` so FastMCP emits a valid nullable JSON Schema:

   ```python
   from typing import Any, Dict, Optional

   from gti_mcp.server import server, vt_client
   from mcp.server.fastmcp import Context


   @server.tool()
   async def get_domain_subdomains(
       domain: str,
       ctx: Context,
       limit: int = 10,
       cursor: Optional[str] = None,
   ) -> Dict[str, Any]:
       """Retrieve subdomains associated with a domain in Google Threat Intelligence.

       Args:
           domain: Root domain name to query (for example, "example.com").
           limit: Maximum number of subdomains to return (default: 10).
           cursor: Optional pagination cursor from a previous response.
       """
       params: Dict[str, Any] = {"limit": limit}
       if cursor:
           params["cursor"] = cursor
       async with vt_client(ctx) as client:
           resp = await client.get_json_async(
               f"/domains/{domain}/subdomains", params=params
           )
       return resp
   ```

2. Export the new tool function in `server/gti/gti_mcp/tools/__init__.py` so importing `gti_mcp.tools` registers it on the `FastMCP` instance.
3. Add hermetic unit tests under `server/gti/tests/`.
4. Document the tool signature, parameters, and return behavior in `docs/servers/gti_mcp.md` and `server/gti/README.md`.

## Coding conventions

- **Never write to `stdout` in MCP servers**: `stdio` transport reserves `stdout` exclusively for JSON-RPC 2.0 messages. Always log via Python's `logging` module (which writes to `stderr`), never `print()`.
- **Use lazy `%s` formatting in logger calls**: Write `logger.info("Fetching rule %s", rule_id)` and `logger.error("Request failed: %s", err, exc_info=True)` per the [Google Python Style Guide](https://google.github.io/styleguide/pyguide.html#3101-logging) rather than eager f-strings.
- **Keep `pyproject.toml` and `setup.py` synchronized**: When adding dependencies or bumping a server version, update `pyproject.toml`, `setup.py`, and any version constant in `server.py` together.
- **Type optional `None` defaults explicitly**: Write `param: Optional[str] = None` instead of `param: str = None` so Pydantic and MCP clients accept explicit `null` arguments.

## Run unit tests

Run the unit test suites with `uv` before opening a pull request:

```bash
# Google SecOps SIEM server
uv run --directory server/secops --with pytest --with pytest-asyncio --with pytest-mock pytest tests/

# Google Threat Intelligence server
uv run --directory server/gti --with pytest --with pytest-asyncio --with pytest-mock pytest tests/

# Security Command Center server
uv run --directory server/scc --with pytest --with pytest-asyncio --with pytest-mock pytest tests/

# Google ADK security agent
uv run --directory run-with-google-adk --extra test pytest tests/
```

## Build and verify documentation

The documentation site uses Sphinx, MyST Markdown, Furo, and `accessible-pygments`, backed by automated Markdown linting and WCAG 2.1 AA accessibility checks that run on every pull request in `.github/workflows/deploy-docs.yml`.

### 1. Install documentation dependencies

```bash
python3 -m venv .venv-docs
source .venv-docs/bin/activate
pip install -r docs/requirements.txt
playwright install chromium --only-shell
```

### 2. Lint Markdown source files

`make -C docs lint-docs` runs `markdownlint-cli2` against `docs/.markdownlint-cli2.jsonc` to enforce accessible authoring rules across all Markdown files:

- **Single `<h1>` and sequential heading hierarchy** (`MD025`, `MD001`): Start each page with one `#` title and step down one heading level at a time (`#` to `##` to `###`).
- **Image alt text** (`MD045`): Provide descriptive alt text on every image.
- **Descriptive link text** (`MD042`, `MD059`): Avoid empty links or generic labels such as `"click here"` or `"here"`.

```bash
make -C docs lint-docs
```

### 3. Build HTML and run WCAG 2.1 AA accessibility tests

Build the static HTML output and run the Playwright + `axe-core` test suite across both light and dark color themes:

```bash
make -C docs html
make -C docs test-a11y
```

By default, `test-a11y` audits structural semantics across every generated `.html` file (`<html lang>`, `<title>`, `<main>`, single `<h1>`, sequential headings, labeled controls, keyboard-focusable `<pre tabindex="0">` blocks, and SVG decorative attributes) and runs headless Chromium `axe-core` (`wcag2a`, `wcag2aa`, `wcag21a`, `wcag21aa`, `best-practice`) across representative page templates in both light and dark modes. To scan all 330+ generated HTML pages in Chromium, set `A11Y_FULL_SCAN="1"`:

```bash
A11Y_FULL_SCAN="1" make -C docs test-a11y
```

## Submit a pull request

1. Review the [contribution guidelines](https://github.com/google/mcp-security/blob/main/CONTRIBUTING) and sign the Google Contributor License Agreement (CLA).
2. Create a focused branch in your fork without trailing whitespace (`git diff --check`).
3. Update both code tests and the matching `docs/` pages for user-visible tool or configuration changes.
4. Confirm `make -C docs lint-docs` and `make -C docs test-a11y` pass locally before opening your pull request.
