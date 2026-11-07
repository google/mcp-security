# Security personas

These persona definitions outline typical responsibilities, focus areas, and MCP tool workflows across security operations, threat intelligence, engineering, and governance roles. Use them as role prompts or system instructions when configuring specialized sub-agents and runbooks.

## Roles by function

### Security Operations Center (SOC)

- **[SOC Analyst Tier 1](soc_analyst_tier_1.md)**: Initial alert triage, entity enrichment, and queue prioritization.
- **[SOC Analyst Tier 2](soc_analyst_tier_2.md)**: Escalated alert correlation, timeline reconstruction, and containment preparation.
- **[SOC Analyst Tier 3](soc_analyst_tier_3.md)**: Multi-stage intrusion analysis and forensic investigation.
- **[SOC Manager](soc_manager.md)**: Queue oversight, SLA tracking, and operational reporting.

### Proactive security

- **[Threat Hunter](threat_hunter.md)**: Hypothesis-driven UDM telemetry sweeps and campaign hunts.
- **[CTI Researcher](cti_researcher.md)**: Threat actor, malware family, and infrastructure profiling.

### Security engineering and response

- **[Detection Engineer](detection_engineer.md)**: YARA-L 2.0 rule authoring, validation, backtesting, and exclusion tuning.
- **[Security Engineer](security_engineer.md)**: Cloud posture review, control hardening, and remediation verification.
- **[Incident Responder](incident_responder.md)**: Host, account, and indicator containment and recovery execution.

### Leadership, governance, and evaluation

- **[CISO](ciso.md)**: Executive risk posture and incident impact summaries.
- **[Compliance Manager](compliance_manager.md)**: Benchmark mapping (CIS, PCI DSS, NIST 800-53, ISO 27001) and audit evidence review.
- **[Red Team](red_team.md)**: Adversary emulation and detection coverage validation.
- **[LLM Judge](llm_judge.md)**: Rubric-based evaluation of agent runbook executions and investigation reports.

```{toctree}
:maxdepth: 1
:hidden:
:caption: Security personas

personas
ciso
compliance_manager
cti_researcher
detection_engineer
incident_responder
llm_judge
red_team
security_engineer
soc_analyst_tier_1
soc_analyst_tier_2
soc_analyst_tier_3
soc_manager
threat_hunter
```
