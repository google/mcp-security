# Alert Investigation Summary Report: Case 607

**Report Timestamp:** 2025-05-02 13:18 ET

## Case Summary

*   **Case ID:** 607
*   **Name:** ursnif_malware_dns
*   **Priority:** PriorityHigh
*   **Status:** Opened
*   **Assignee:** @Tier1
*   **Environment:** LogStory

## Alert(s) Summary

*   **Alert ID:** 866
*   **Name:** URSNIF_MALWARE_DNS
*   **Timestamp (Start):** 2025-05-01T16:44:54Z (approx)
*   **Timestamp (End):** 2025-05-01T16:49:30Z (approx)
*   **Severity:** Medium (from alert details, case priority is High)

## Key Entities Involved

*   **File Hash:** `7d99c80a1249a1ec9af0f3047c855778b06ea57e11943a271071985afe09e6c2` (Filename: `\\Device\\CdRom1\\me\\123.com`)
*   **Source IP:** `192.168.30.20` (Internal)
*   **Destination IP:** `193.106.191.163` (External)
*   **Destination Domain 1:** `superlist.top`
*   **Destination Domain 2:** `superstarts.top`

## Enrichment Summary

*   **File Hash (`7d99...`)**:
    *   **GTI:** Identified as `rundll32.exe`, a legitimate Microsoft executable often used as a LOLBIN. No malicious detections on the hash itself. Tagged as `lolbin`, `known-distributor`, `legit`.
*   **Source IP (`192.168.30.20`)**:
    *   **SIEM Lookup:** Failed due to permission error (`chronicle.entities.summarizeFromQuery` denied). No SIEM context available.
*   **Destination IP (`193.106.191.163`)**:
    *   **GTI:** Negative reputation (-2), 3 malicious detections. Associated with Ursnif/Gozi malware collections. Registered in Russia (RU).
*   **Domain (`superlist.top`)**:
    *   **GTI:** Negative reputation (-1), 11 malicious detections. Associated with Ursnif/Gozi malware collections.
*   **Domain (`superstarts.top`)**:
    *   **GTI:** Negative reputation (-57), 10 malicious detections. Associated with Ursnif/Gozi malware collections. Registrar: ERANET INTERNATIONAL LIMITED.

## Event Summary

The alert was triggered by events associated with the process `\\Device\\CdRom1\\me\\123.com` (hash `7d99...`, identified as `rundll32.exe`) running on the internal host `192.168.30.20`.
*   **NETWORK_DNS Events:** The process made DNS requests for `superlist.top` (around 2025-05-01T16:46:15Z) and `superstarts.top` (around 2025-05-01T16:44:54Z). Both domains are flagged as malicious by GTI and associated with Ursnif/Gozi.
*   **NETWORK_CONNECTION Event:** The process established a network connection from `192.168.30.20` to the malicious IP `193.106.191.163` on port 80 (around 2025-05-01T16:48:53Z). This IP is also associated with Ursnif/Gozi by GTI.

## Initial Assessment/Conclusion

The alert indicates likely malicious activity associated with the Ursnif/Gozi malware family. A legitimate Windows process (`rundll32.exe`) executed from an unusual path (`\\Device\\CdRom1\\me\\123.com`) on host `192.168.30.20` made DNS requests to known malicious domains (`superlist.top`, `superstarts.top`) and connected to a known malicious IP address (`193.106.191.163`). This strongly suggests C2 communication or further malware download attempts. Further investigation of the host `192.168.30.20` is required.

## Recommendations

*   Trigger **Basic Endpoint Triage & Isolation Runbook** for host `192.168.30.20`.
*   Trigger **IOC Containment Runbook** for IP `193.106.191.163`, domain `superlist.top`, and domain `superstarts.top`.
*   Escalate to Tier 2/Incident Response for deeper analysis of the host and potential malware infection.
