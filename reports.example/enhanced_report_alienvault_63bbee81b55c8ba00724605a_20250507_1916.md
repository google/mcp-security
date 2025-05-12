# Investigation Summary: GTI Collection alienvault_63bbee81b55c8ba00724605a

 * **Runbook Used:** `.clinerules/run_books/investigate_a_gti_collection_id.md`
 * **Timestamp:** 2025-05-07 19:16 (UTC-4)
 * **Collection ID:** `alienvault_63bbee81b55c8ba00724605a`
 * **Collection Name:** Unwrapping Ursnifs Gifts
 * **Collection Link:** https://otx.alienvault.com/pulse/63bbee81b55c8ba00724605a

## Summary

This report summarizes the investigation into GTI Collection `alienvault_63bbee81b55c8ba00724605a`, which details an incident involving Ursnif malware leading to Cobalt Strike deployment and lateral movement. The investigation involved enriching associated IOCs using GTI and correlating them with local SIEM data over the past 72 hours.

## Key Findings & Recommendations

*   **Finding:** GTI collection relates to Ursnif malware activity, potentially leading to Cobalt Strike.
*   **Finding:** Several associated domains (`superliner.top`, `superstarts.top`, `internetlined.com`, `superlinez.top`, `denterdrigx.com`, `internetlines.in`) and one file hash (`dfdfd0a339fe...`) are identified as malicious or high-risk by GTI.
*   **Finding:** **Local SIEM correlation found 27 suspicious DNS events involving `superstarts.top` from host `malwaretest-win` / `malwareTest-win10` via `rundll32.exe` (SHA256: `7d99c80a1249a1ec9af0f3047c855778b06ea57e11943a271071985afe09e6c2`) within the last 72 hours.** The parent process was `wscript.exe`.
*   **Finding:** No other associated IOCs from the GTI collection were found in the local SIEM within the last 72 hours.
*   **Recommendation:** **Investigate the activity on host `malwaretest-win` / `malwareTest-win10`** related to the DNS lookups for `superstarts.top`. Consider triggering the `case_event_timeline_and_process_analysis.md` runbook for the relevant events/host.
*   **Recommendation:** Consider blocking the identified malicious domains (`superliner.top`, `superstarts.top`, `internetlined.com`, `superlinez.top`, `denterdrigx.com`, `internetlines.in`) at the network perimeter if not already blocked.

## GTI Findings

### Related Files

*   `dfdfd0a339fe03549b2475811b106866d035954e9bc002f20b0f69e0f986838f`: **High Severity (GTI)**, associated with Ursnif.
*   `7d99c80a1249a1ec9af0f3047c855778b06ea57e11943a271071985afe09e6c2`: Identified as legitimate `rundll32.exe`.
*   `ce77f575cc4406b76c68475cb3693e14`: Partial GTI info, high Mandiant IC score.
*   Other related file hashes were not found in GTI.

### Related Domains

*   `superliner.top`: Malicious (7 detections), associated with Ursnif/ISFB.
*   `superstarts.top`: Malicious (10 detections), associated with Ursnif/Gozi.
*   `internetlined.com`: Malicious (9 detections), associated with Ursnif/ISFB.
*   `superlinez.top`: Malicious (10 detections), associated with Ursnif/ISFB.
*   `denterdrigx.com`: Malicious (11 detections), associated with Ursnif/ISFB.
*   `internetlines.in`: Malicious (9 detections), associated with Ursnif/ISFB.

### Related Attack Techniques (MITRE ATT&CK)

*   T1003 (OS Credential Dumping)
*   T1018 (Remote System Discovery)
*   T1021 (Remote Services)
*   T1027 (Obfuscated Files or Information)
*   T1033 (System Owner/User Discovery)
*   T1036 (Masquerading)
*   T1041 (Exfiltration Over C2 Channel)
*   T1047 (Windows Management Instrumentation)
*   T1049 (System Network Connections Discovery)
*   T1055 (Process Injection)

### Related Reports

*   `report--252e33f9227d94e22ed03f78164d44ffb9af07b8ca3288d7cd057b53e1859404`

### Other Relationships

*   No related IPs, URLs, Associations, Threat Actors, Malware Families, Software Toolkits, Campaigns, Vulnerabilities, or Suspected Threat Actors were found directly linked to this collection ID in GTI.

## Local Environment Correlation (Last 72 Hours)

*   **File Hash `dfdfd0a339fe...`:** No entity info found; No related events found.
*   **Domain `superliner.top`:** No entity info found; No related events found.
*   **Domain `superstarts.top`:** Entity seen recently (May 6th); **27 suspicious DNS events found** from host `malwaretest-win` / `malwareTest-win10` via `rundll32.exe` (SHA256: `7d99c80a1249a1ec9af0f3047c855778b06ea57e11943a271071985afe09e6c2`, Parent: `wscript.exe`).
*   **Domain `internetlined.com`:** No entity info found; No related events found.
*   **Domain `superlinez.top`:** No entity info found; No related events found.
*   **Domain `denterdrigx.com`:** No entity info found; No related events found.
*   **Domain `internetlines.in`:** No entity info found; No related events found.
