# Changelog

All notable changes to the Google MCP Security packages (`google-secops-mcp`, `gti-mcp`, `secops-soar-mcp`, and `scc-mcp`) are documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/), and each server package adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

---

## [2026-11-01]

### `google-secops-mcp` v0.8.0 (`secops-v0.8.0`)

#### Added
- Add `update_rule` tool to update existing Chronicle YARA-L 2.0 detection rules in place, with rule ID normalization and revision handling ([#253](https://github.com/google/mcp-security/pull/253) by [@Pavornoc](https://github.com/Pavornoc) and [@dandye](https://github.com/dandye)).
- Add optional `start_time`, `end_time`, and `list_basis` filtering parameters to `get_rule_detections` ([#283](https://github.com/google/mcp-security/pull/283) by [@abdeltaehass](https://github.com/abdeltaehass)).

#### Fixed
- Replace `print()` calls in `investigation_management.py` (`list_investigations`, `get_investigation`, `trigger_investigation`, `fetch_associated_investigations`) with lazy `%s`-formatted `logger.info` and `logger.error(..., exc_info=True)` calls so diagnostic output does not corrupt the MCP stdio JSON-RPC stream ([#315](https://github.com/google/mcp-security/pull/315), fixes [#267](https://github.com/google/mcp-security/issues/267) by [@abdeltaehass](https://github.com/abdeltaehass)).
- Fall back from empty `feedbackSummary` dictionaries and surface alert IDs, severity, status, verdict, and rule metadata in `get_security_alerts` ([#287](https://github.com/google/mcp-security/pull/287) by [@rioyu123](https://github.com/rioyu123), [#283](https://github.com/google/mcp-security/pull/283) by [@abdeltaehass](https://github.com/abdeltaehass)).
- Forward `alert_state` and time-range parameters (`start_time`, `end_time`, `list_basis`) properly in `get_rule_detections` ([#283](https://github.com/google/mcp-security/pull/283) by [@abdeltaehass](https://github.com/abdeltaehass)).
- Round `test_rule` `end_time` down to the start of the current hour to satisfy Chronicle SIEM historical indexing constraints ([#143](https://github.com/google/mcp-security/pull/143) by [@sidxparab](https://github.com/sidxparab) and [@dandye](https://github.com/dandye)).

---

### `gti-mcp` v0.1.4 (`gti-v0.1.4`)

#### Added
- Enable `trust_env=True` in `vt.Client` initialization so `gti-mcp` honors standard corporate proxy environment variables (`HTTP_PROXY`, `HTTPS_PROXY`, `NO_PROXY`) and `SSL_CERT_FILE` ([#273](https://github.com/google/mcp-security/pull/273) by [@Dom206](https://github.com/Dom206)).

#### Fixed
- Annotate `None`-defaulted parameters (`search_threats.collection_type`, `get_collection_rules.rule_types`, `search_digital_threat_monitoring.{since,until,page,truncate}`) with `Optional[...]` so FastMCP schemas accept explicit `null` values ([#323](https://github.com/google/mcp-security/pull/323) by [@vishalhabib99](https://github.com/vishalhabib99)).
- Make `attributes` a required parameter in `update_collection_attributes` and filter out empty-string query parameters (`""`) alongside `None` in `search_digital_threat_monitoring` ([#323](https://github.com/google/mcp-security/pull/323) by [@vishalhabib99](https://github.com/vishalhabib99)).

---

### `secops-soar-mcp` v0.2.0 (`secops-soar-v0.2.0`)

#### Breaking / Behavioral Changes
- `get_case_full_details` now returns the top-level dictionary key `"case_details"` instead of `"case_details:"` (removing the trailing colon typo to match `"case_alerts"` and `"case_comments"`) ([#257](https://github.com/google/mcp-security/pull/257) by [@Haihan-Jiang](https://github.com/Haihan-Jiang)).
- `HttpClient.get()`, `post()`, and `patch()` now re-raise `ssl.SSLError` and `aiohttp.ClientSSLError` instead of swallowing certificate verification failures as `None`, surfacing actionable certificate error messages rather than masking them as invalid credentials ([#308](https://github.com/google/mcp-security/pull/308), fixes [#191](https://github.com/google/mcp-security/issues/191) by [@Som0111](https://github.com/Som0111)).

#### Added
- Add 7 SOAR case lifecycle management tools (`create_case`, `update_case_description`, `close_case`, `assign_case`, `change_case_stage`, `add_case_tag`, `remove_case_tag`) and update the `secops-triage` skill to reference local case closure ([#281](https://github.com/google/mcp-security/pull/281) by [@jshlbrd](https://github.com/jshlbrd) and [@dandye](https://github.com/dandye)).
- Enable `trust_env=True` in `HttpClient` (`aiohttp.ClientSession`) so `secops-soar-mcp` honors `HTTP_PROXY`, `HTTPS_PROXY`, `NO_PROXY`, and `SSL_CERT_FILE` in corporate proxy environments ([#311](https://github.com/google/mcp-security/pull/311), fixes [#198](https://github.com/google/mcp-security/issues/198) by [@dandye](https://github.com/dandye)).

#### Fixed
- Catch `aiohttp.ClientSSLError` in `bindings.py` and provide actionable `SSL_CERT_FILE` / `certifi` troubleshooting guidance ([#308](https://github.com/google/mcp-security/pull/308), fixes [#191](https://github.com/google/mcp-security/issues/191) by [@Som0111](https://github.com/Som0111)).
- Correct `get_case_full_details` response key from `"case_details:"` to `"case_details"` ([#257](https://github.com/google/mcp-security/pull/257) by [@Haihan-Jiang](https://github.com/Haihan-Jiang)).
- Guard SOAR cleanup when the HTTP client is uninitialized and avoid creating a new `aiohttp` session during `cleanup` ([#258](https://github.com/google/mcp-security/pull/258), [#260](https://github.com/google/mcp-security/pull/260) by [@Haihan-Jiang](https://github.com/Haihan-Jiang)).
- Declare `python-dotenv>=1.0.0` dependency in `pyproject.toml` and `setup.py`, and align the `setup.py` console script entry point (`secops_soar_mcp.server:run_main`) ([#259](https://github.com/google/mcp-security/pull/259), [#261](https://github.com/google/mcp-security/pull/261) by [@Haihan-Jiang](https://github.com/Haihan-Jiang)).

#### Documentation
- Document how to locate `SOAR_URL` in troubleshooting documentation ([#256](https://github.com/google/mcp-security/pull/256) by [@P-r-e-m-i-u-m](https://github.com/P-r-e-m-i-u-m)).

---

### `scc-mcp` v0.2.0 (`scc-v0.2.0`)

#### Breaking / Behavioral Changes
- **SCC v2 API Migration:** Migrated backend client from `google.cloud.securitycenter` (SCC v1) to `google.cloud.securitycenter_v2` (SCC v2). Finding `name` resource paths returned by `top_vulnerability_findings` and `get_finding_remediation` now use regionalized v2 paths (`projects/{project}/sources/{source}/locations/{location}/findings/{finding_id}` or `organizations/{org}/...`, defaulting to `location="global"`). Deployments with regional SCC v2 findings should pass the `location` parameter ([#274](https://github.com/google/mcp-security/pull/274), fixes [#167](https://github.com/google/mcp-security/issues/167)).
- **Direct Python Positional Parameter Order:** Added `organization_id: str = None` as the second parameter in `top_vulnerability_findings` and `get_finding_remediation`. Named MCP tool calls (`tools/call`) are unaffected, but direct Python callers passing positional arguments after `project_id` should use keyword arguments ([#249](https://github.com/google/mcp-security/pull/249), [#274](https://github.com/google/mcp-security/pull/274)).

#### Added
- Migrate from `google.cloud.securitycenter` (v1) to `google.cloud.securitycenter_v2` with location-aware resource routing (`location: str = "global"`) ([#274](https://github.com/google/mcp-security/pull/274), fixes [#167](https://github.com/google/mcp-security/issues/167) by [@notluken](https://github.com/notluken) and [@dandye](https://github.com/dandye)).
- Add organization-level findings support (`organization_id`) across all SCC tools and Cloud Asset Inventory (CAI) enrichment ([#249](https://github.com/google/mcp-security/pull/249), fixes [#248](https://github.com/google/mcp-security/issues/248) by [@regevWe](https://github.com/regevWe); [#274](https://github.com/google/mcp-security/pull/274) by [@notluken](https://github.com/notluken)).
- Add 4 new FastMCP tools: `search_findings`, `get_finding_details`, `search_findings_by_compliance`, and `set_finding_mute` ([#274](https://github.com/google/mcp-security/pull/274) by [@notluken](https://github.com/notluken)).
- Add unit test suite (`server/scc/tests/test_scc_unit.py`) covering all 6 SCC v2 tools and filter helpers ([#300](https://github.com/google/mcp-security/pull/300) by [@dandye](https://github.com/dandye)).

#### Fixed
- Over-fetch candidate findings in `top_vulnerability_findings` for accurate descending attack exposure score sorting and include inline `nextSteps` ([#274](https://github.com/google/mcp-security/pull/274) by [@notluken](https://github.com/notluken)).
- Support case-insensitive `OR` and comma-separated filter splitting in `_build_or_filter`, and dynamic `project` / `organization` target labels on `NotFound` errors ([#274](https://github.com/google/mcp-security/pull/274)).
- Use `securitycenter_v2.SetMuteRequest` in `set_finding_mute` and align `setup.py` `py_modules` and dependency floors with `pyproject.toml` ([#300](https://github.com/google/mcp-security/pull/300) by [@dandye](https://github.com/dandye)).

---

### Repository & Agent Tooling (Non-PyPI)
- Modernize `run-with-google-adk` into the `mcp-security-agent` package powered by Google ADK v2, featuring an interactive CLI REPL (`mcp-security-agent chat`), a FastAPI Cloud Run server (`mcp-security-agent serve`), a zero-build SecOps web console, and credential-aware MCP toolset auto-discovery ([#303](https://github.com/google/mcp-security/pull/303), [#309](https://github.com/google/mcp-security/pull/309) by [@dandye](https://github.com/dandye)).

---

## [2026-08-27]

### `google-secops-mcp` v0.7.1 (`secops-v0.7.1`), `gti-mcp` v0.1.3 (`gti-v0.1.3`), `secops-soar-mcp` v0.1.2 (`secops-soar-v0.1.2`), `scc-mcp` v0.1.1 (`scc-v0.1.1`)

#### Added
- Add `list_parsers` tool to `google-secops-mcp` ([#252](https://github.com/google/mcp-security/pull/252) by [@arod-ops](https://github.com/arod-ops)).
- Add security persona documentation under `docs/personas/` and move `gemini-extension.json` to top-level ([#241](https://github.com/google/mcp-security/pull/241), [#245](https://github.com/google/mcp-security/pull/245) by [@dandye](https://github.com/dandye)).

#### Fixed
- Pin `mcp<2.0` (`mcp[cli]<2.0`) across all four MCP servers to prevent breaking changes from `mcp` 2.x ([#278](https://github.com/google/mcp-security/pull/278), [#288](https://github.com/google/mcp-security/pull/288) by [@dandye](https://github.com/dandye)).

---

## [2026-03-11]

### `google-secops-mcp` v0.7.0 (`secops-v0.7.0`)
- Add rule exclusions management tools (`get_rule_exclusion`, `list_rule_exclusions`, `create_rule_exclusion`, `patch_rule_exclusion`, `compute_rule_exclusion_activity`, `update_rule_exclusion_deployment`) ([#242](https://github.com/google/mcp-security/pull/242), [#243](https://github.com/google/mcp-security/pull/243) by [@mihirvala08](https://github.com/mihirvala08)).

---

## [2026-02-27]

### `google-secops-mcp` v0.6.0 (`secops-v0.6.0`) and v0.5.3 (`secops-v0.5.3`)
- Add curated rules management tools (`list_curated_rules`, `get_curated_rule`, `get_curated_rule_by_name`, `search_curated_rules`, `list_curated_rule_Sets`, `list_curated_rule_set_categories`, `list_curated_rule_set_deployments`, `update_curated_rule_set_deployment`, `list_curated_rule_detections`) ([#227](https://github.com/google/mcp-security/pull/227) by [@mihirvala08](https://github.com/mihirvala08)).
- Add retrohunt and alert search tools (`create_retrohunt`, `get_retrohunt`, `search_rule_alerts`) ([#229](https://github.com/google/mcp-security/pull/229) by [@mihirvala08](https://github.com/mihirvala08)).
- Add investigation management tools (`list_investigations`, `get_investigation`, `trigger_investigation`, `fetch_associated_investigations`) ([#220](https://github.com/google/mcp-security/pull/220) by [@mihirvala08](https://github.com/mihirvala08)).
- Add watchlist management tools (`list_watchlists`, `get_watchlist`, `create_watchlist`, `update_watchlist`, `delete_watchlist`) ([#222](https://github.com/google/mcp-security/pull/222) by [@mihirvala08](https://github.com/mihirvala08)).
- Add Remote MCP Server documentation and refine Gemini CLI extension skills ([#215](https://github.com/google/mcp-security/pull/215), [#218](https://github.com/google/mcp-security/pull/218), [#219](https://github.com/google/mcp-security/pull/219), [#228](https://github.com/google/mcp-security/pull/228)).

---

## [2026-01-13]

### `google-secops-mcp` v0.5.2 (`secops-v0.5.2`) and v0.5.1 (`secops-v0.5.1`)
- Add custom `start_time` and `end_time` support for UDM search and event search tools ([#210](https://github.com/google/mcp-security/pull/210) by [@eranc-google](https://github.com/eranc-google)).
- Restore `Optional[...]` type annotations for `None`-defaulted parameters and tighten `.dockerignore` ([#194](https://github.com/google/mcp-security/pull/194), [#195](https://github.com/google/mcp-security/pull/195), [#200](https://github.com/google/mcp-security/pull/200)).
- Add service account option for SecOps and update dependencies ([#179](https://github.com/google/mcp-security/pull/179), [#206](https://github.com/google/mcp-security/pull/206), [#214](https://github.com/google/mcp-security/pull/214)).

---

## [2025-10-28]

### `google-secops-mcp` v0.5.0 (`secops-v0.5.0`)
- Add `search_udm` and `export_udm_search_csv` tools ([#153](https://github.com/google/mcp-security/pull/153)).

---

## [2025-10-06 — 2025-10-07]

### `google-secops-mcp` v0.4.1 (`secops-v0.4.1`) and v0.4.0 (`secops-v0.4.0`)
- Add `get_detection_rule` tool ([#184](https://github.com/google/mcp-security/pull/184) by [@sidxparab](https://github.com/sidxparab)).
- Handle mixed entry types in `get_reference_list` ([#175](https://github.com/google/mcp-security/pull/175) by [@MRADULTRIPATHI](https://github.com/MRADULTRIPATHI)).
- Configure `setuptools` package discovery and align package name in `setup.py` ([#188](https://github.com/google/mcp-security/pull/188), [#190](https://github.com/google/mcp-security/pull/190)).

---

## [2025-09-17 — 2025-09-19]

### `google-secops-mcp` v0.3.0 (`secops-v0.3.0`) and `secops-soar-mcp` v0.1.1 (`secops-soar-v0.1.1`)
- Add SecOps feed management tools (`list_feeds`, `get_feed`, `create_feed`, `update_feed`, `enable_feed`, `disable_feed`, `delete_feed`, `generate_secret`) ([#183](https://github.com/google/mcp-security/pull/183)).
- Fix async console script entry point for `secops-soar-mcp` ([#181](https://github.com/google/mcp-security/pull/181)).

---

## [2025-09-04 — 2025-09-05]

### Initial PyPI Releases (`secops-v0.2.0`, `gti-v0.1.2`, `secops-soar-v0.1.0`, `scc-v0.1.0`)
- Initial PyPI package releases for `google-secops-mcp` (`0.2.0`), `gti-mcp` (`0.1.2`), `secops-soar-mcp` (`0.1.0`), and `scc-mcp` (`0.1.0`) ([#176](https://github.com/google/mcp-security/pull/176)).
