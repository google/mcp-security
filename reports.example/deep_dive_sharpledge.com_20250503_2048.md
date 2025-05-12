# Deep Dive IOC Analysis Report: sharpledge.com

**Runbook Used:** deep_dive_ioc_analysis.md (Adapted)
**Timestamp:** 2025-05-03 20:48:00 EDT
**IOC Value:** sharpledge.com
**IOC Type:** Domain

## Executive Summary

A deep dive analysis was performed on the domain `sharpledge.com`. Google Threat Intelligence (GTI) indicates this domain has a high Mandiant IC score (100), is detected as malicious/spyware by multiple vendors, and is associated with known malicious campaigns, malware families (`malware--58304da7-3d6a-5b8b-8924-b26673c4419e`), and threat actors (`threat-actor--7a39953e-0dae-569a-9d49-d52a4a8865b1`). SIEM analysis revealed DNS queries for `sharpledge.com` originating from the internal host `windows-prod-1` (IP `10.166.0.3`) within the last 7 days, resolving to IP `51.75.210.218`. No SIEM events were found for file hashes known to be associated (communicating/downloaded) with the domain in GTI. The DNS lookup from a production host to a known malicious domain strongly suggests potential compromise or malicious activity on `windows-prod-1`. Immediate investigation of the host and network blocking of the domain/associated IPs are recommended.

## GTI Report Details (sharpledge.com)

*   **Mandiant IC Score:** 100 (High Risk)
*   **Last Analysis Stats:** Malicious: 10, Suspicious: 2, Undetected: 29, Harmless: 53
*   **Categories:** spyware and malware (Sophos), Malware Sites (Webroot)
*   **WHOIS:** Registered via NAMECHEAP INC with privacy protection.
*   **Associations:** Linked to campaign (`campaign--8d6e7115-c792-5ded-b0a9-81d10027a943`), malware family (`malware--58304da7-3d6a-5b8b-8924-b26673c4419e`), threat actor (`threat-actor--7a39953e-0dae-569a-9d49-d52a4a8865b1`), and multiple other collections.

## GTI Pivoting Results

*   **Resolved IPs:** `76.223.54.146`, `13.248.169.48`, `72.52.178.23`, `199.59.243.227`, `199.59.243.226`, `51.75.210.218`, `162.0.230.75`, `66.42.116.212`, `162.254.32.222`, `34.133.73.143`.
*   **Communicating File Hashes (SHA256):**
    *   `b84d6a12bb1756b69791e725b0e3d7a962888b31a8188de225805717c299c086`
    *   `ece45b0ed87b6e956022a5e20582701b7f22c699d89c44144adde252515b0a66`
*   **Downloaded File Hashes (SHA256):**
    *   `6dc9c7fc93bb488bb0520a6c780a8d3c0fb5486a4711aca49b4c53fac7393023`
    *   `32f2fa940d4b4fe19aca1e53a24e5aac29c57b7c5ee78588325b87f1b649c864`

## SIEM Search Results (Last 168 hours)

*   **Domain (`sharpledge.com`):** Multiple DNS query events found originating from host `windows-prod-1` (IP `10.166.0.3`), resolving to `51.75.210.218`.
*   **Communicating Hash (`b84d...`):** No events found.
*   **Communicating Hash (`ece4...`):** No events found.
*   **Downloaded Hash (`6dc9...`):** No events found.
*   **Downloaded Hash (`32f2...`):** No events found.

## SIEM Context & Correlation

*   **Entity Lookup (`sharpledge.com`):** Shows domain presence but no specific events/alerts in summary.
*   **Entity Lookup (IP `76.223.54.146`):** No recent events/alerts found in summary. Belongs to Amazon AWS.
*   **IOC Match Check (IP `76.223.54.146`):** No recent matches found.

## Analysis & Conclusion

The domain `sharpledge.com` exhibits strong indicators of maliciousness based on GTI data, including a high Mandiant score, multiple vendor detections, and associations with known threats. The observation of DNS queries to this domain from the internal production host `windows-prod-1` is a critical finding. While the specific malicious files linked to the domain in GTI were not observed in recent SIEM logs, the DNS activity itself is highly suspicious and suggests potential compromise or unwanted software activity on `windows-prod-1`.

## Recommendations

1.  **Endpoint Investigation:** Initiate an immediate, high-priority investigation on the host `windows-prod-1` (IP `10.166.0.3`). Focus on identifying the process responsible for the DNS queries, searching for related malware artifacts, and analyzing system activity around the query times. Consider using the "Basic Endpoint Triage & Isolation" runbook.
2.  **Network Containment:** Block the domain `sharpledge.com` and associated IP addresses (especially `51.75.210.218`) at the network perimeter (firewall/proxy) using the `ioc_containment.md` runbook or equivalent procedures.
3.  **Further TI Research:** Investigate the associated malware family (`malware--58304da7-3d6a-5b8b-8924-b26673c4419e`) and threat actor (`threat-actor--7a39953e-0dae-569a-9d49-d52a4a8865b1`) using GTI tools (`get_collection_report`, etc.) to understand potential TTPs relevant to the host investigation.

## Workflow Diagram

```mermaid
sequenceDiagram
    participant Analyst
    participant Cline as Cline (MCP Client)
    participant GTI as gti-mcp
    participant SIEM as secops-mcp

    Analyst->>Cline: Start Deep Dive IOC Analysis (sharpledge.com)
    Cline->>GTI: get_domain_report(domain="sharpledge.com")
    GTI-->>Cline: GTI Domain Report (High Risk, Associations)
    Note over Cline: Get GTI Relationships (IPs, Files)
    Cline->>GTI: get_entities_related_to_a_domain(domain="sharpledge.com", relationship_name="resolutions")
    GTI-->>Cline: Resolved IPs (incl. 76.223.54.146, 51.75.210.218)
    Cline->>GTI: get_entities_related_to_a_domain(domain="sharpledge.com", relationship_name="communicating_files")
    GTI-->>Cline: Communicating Hashes (b84d..., ece4...)
    Cline->>GTI: get_entities_related_to_a_domain(domain="sharpledge.com", relationship_name="downloaded_files")
    GTI-->>Cline: Downloaded Hashes (6dc9..., 32f2...)
    Note over Cline: Search SIEM (168h)
    Cline->>SIEM: search_security_events(text="Events involving domain sharpledge.com")
    SIEM-->>Cline: DNS Events found (from 10.166.0.3 to 51.75.210.218)
    Cline->>SIEM: search_security_events(text="Events involving file hash b84d...")
    SIEM-->>Cline: No events found
    Cline->>SIEM: search_security_events(text="Events involving file hash ece4...")
    SIEM-->>Cline: No events found
    Cline->>SIEM: search_security_events(text="Events involving file hash 6dc9...")
    SIEM-->>Cline: No events found
    Cline->>SIEM: search_security_events(text="Events involving file hash 32f2...")
    SIEM-->>Cline: No events found
    Note over Cline: Enrich/Correlate in SIEM
    Cline->>GTI: get_ip_address_report(ip_address="76.223.54.146")
    GTI-->>Cline: GTI IP Report
    Cline->>SIEM: lookup_entity(entity_value="76.223.54.146")
    SIEM-->>Cline: SIEM IP Summary (No recent events)
    Cline->>SIEM: get_ioc_matches()
    SIEM-->>Cline: No recent matches for 76.223.54.146
    Cline->>SIEM: lookup_entity(entity_value="sharpledge.com")
    SIEM-->>Cline: SIEM Domain Summary (Seen, no specific events)
    Note over Cline: Synthesize findings and recommendations
    Cline->>Cline: write_to_file(path="./reports/deep_dive_sharpledge.com_...", content=ReportMarkdown)
    Note over Cline: Report file created
    Cline->>Analyst: attempt_completion(result="Deep dive analysis for sharpledge.com complete. Report generated.")
