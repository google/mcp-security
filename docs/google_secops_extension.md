# Google SecOps extension

The `extensions/google-secops/` directory packages security operations workflows and client onboarding guides as portable [Agent Skills](https://agentskills.io/specification). Each skill adapts at runtime to whichever MCP transport is connected:

- **[Remote MCP server for Google SecOps](remote_server.md)** (preferred when available)
- **[Local Python MCP servers](usage_guide.md)** (`server/secops` and `server/secops-soar` fallback)

A workspace `.agent` symlink exposes these skills as [Antigravity agent skills](https://antigravity.google/docs/skills) inside the repository, or you can symlink them into `~/.gemini/antigravity/skills/` to make them available across all workspaces.

## Prerequisites

1. **Install Gemini CLI** (when using the Gemini CLI extension workflow):
   ```bash
   npm install -g @google/gemini-cli@preview
   ```

2. **Enable skills in `~/.gemini/settings.json`**:
   ```json
   {
     "general": {
       "previewFeatures": true
     },
     "experimental": {
       "skills": true
     }
   }
   ```

3. **Verify skill discovery** from the Gemini CLI prompt:
   ```text
   /skills list
   ```

## Install the extension

From the root of a local `mcp-security` clone, install the extension into Gemini CLI:

```bash
gemini extensions install ./extensions/google-secops
```

When prompted, enter your Google Cloud `PROJECT_ID` and remote MCP `SERVER_URL` (for example, `https://us-chronicle.googleapis.com/mcp`).

## Included skills

| Skill name | Slash command | Path | Purpose |
| :--- | :--- | :--- | :--- |
| `secops-setup-gemini` | `/security:setup-gemini` | `skills/setup-gemini-cli/SKILL.md` | Verifies `uv` and Google Cloud ADC, collects `PROJECT_ID`, `CUSTOMER_ID`, and `REGION`, and adds `secops-hosted-mcp` to `~/.gemini/settings.json`. |
| `secops-setup-antigravity` | `/security:setup-antigravity` | `skills/setup-antigravity/SKILL.md` | Verifies Google Cloud ADC and merges the remote SecOps MCP configuration from `mcp_config.template.json` into `~/.gemini/antigravity/mcp_config.json`. |
| `secops-triage` | `/security:triage` | `skills/triage/SKILL.md` | Runs a structured Tier 1 alert and case triage protocol: gathers case and alert context, checks for duplicate cases, enriches entities, and recommends False Positive, Benign True Positive, or True Positive classification. |
| `secops-investigate` | `/security:investigate` | `skills/investigate/SKILL.md` | Guides Tier 2 and Tier 3 incident response investigations across malware triage, lateral movement, and suspicious authentication procedures. |
| `secops-hunt` | `/security:hunt` | `skills/hunt/SKILL.md` | Drives hypothesis-based and GTI campaign-based threat hunts using IOC matching and UDM event searches. |

## How adaptive tool selection works

Each operational skill (`secops-triage`, `secops-investigate`, and `secops-hunt`) embeds its step-by-step SOC procedure directly in `SKILL.md` and resolves tool names against [`extensions/google-secops/TOOL_MAPPING.md`](https://github.com/google/mcp-security/blob/main/extensions/google-secops/TOOL_MAPPING.md):

1. **Inspect registered MCP tools**: Check whether remote Google SecOps tools (such as `udm_search` and `summarize_entity`) or local Python tools (such as `search_udm`, `search_security_events`, and `lookup_entity`) are loaded in the active session.
2. **Prefer remote tools**: When the remote MCP server is connected, call the remote tool names.
3. **Adapt multi-step workflows**: Some operations differ in call shape between transports. For natural-language event search, the remote server pairs `translate_udm_query` followed by `udm_search`, whereas the local `google-secops-mcp` server executes `search_security_events` in one call.

### Key remote vs. local tool mappings

| Capability | Remote MCP tool | Local Python MCP tool |
| :--- | :--- | :--- |
| UDM query search | `udm_search` | `search_udm` |
| Natural-language event search | `translate_udm_query` then `udm_search` | `search_security_events` |
| Entity activity summary | `summarize_entity` | `lookup_entity` |
| IOC matches | `get_ioc_match` | `get_ioc_matches` |
| Get case details | `get_case` and `list_case_alerts` | `get_case_full_details` |
| Add case comment | `create_case_comment` | `post_case_comment` |
| Close case | `execute_bulk_close_case` | `close_case` |
| Update YARA-L 2.0 rule in place | Not exposed | `update_rule` |

## Cross-agent compatibility

The skills follow the open Agent Skills directory layout (`skills/<name>/SKILL.md` with YAML frontmatter) so they work across Gemini CLI, Antigravity, Claude Code, Goose, and other skill-aware coding agents:

- `slash_command` declares a shortcut pattern such as `/security:triage`.
- `personas` maps each workflow to its corresponding role in [Security personas](personas/index.md) (such as `tier1_soc_analyst`, `incident_responder`, or `threat_hunter`).

## References

- [Agent Skills specification](https://agentskills.io/specification)
- [Gemini CLI documentation](https://geminicli.com)
- [Gemini CLI preview features](https://geminicli.com/docs/settings/general#previewfeatures)
- [Antigravity agent skills](https://antigravity.google/docs/skills)
