# Scan and reanalyze files, URLs, domains, and IP addresses

This guide shows how to submit suspicious files and URLs for scanning, refresh stale verdicts on known indicators, and retrieve scan results without blocking your MCP client.

## Prerequisites

Set `VT_APIKEY` in your MCP client environment. See [Google Threat Intelligence (GTI) MCP Server](../servers/gti_mcp.md) for client configuration examples.

```{warning}
Standard VirusTotal file submissions are shared with the public VirusTotal corpus and accessible to Google Threat Intelligence subscribers. Always check the SHA-256 hash with `get_file_report` first, and confirm authorization before uploading local files that could contain proprietary code, credentials, or internal documents.
```

## Choose between `submit_file` and `analyse_file`

`gti-mcp` provides two file upload tools for different execution models:

- **Use `submit_file(file_path)` by default.** It uploads only the file basename (`os.path.basename`), avoids leaking your local directory path in the multipart `Content-Disposition` header, and returns the queued analysis descriptor (`id` and `type`) right away. You can run other SIEM or SOAR queries while VirusTotal scans the file, then check status with `get_analysis(analysis_id)`.
- **Use `analyse_file(file_path)` only when you want a single blocking call.** It uploads the file and holds the tool call open until VirusTotal finishes scanning, which can hit client tool-call timeouts on large binaries or busy sandbox queues.

## Triage a suspicious local file without blocking

Follow this sequence when an analyst or playbook isolates an unknown binary on disk.

1. Compute the local SHA-256 hash and check whether Google Threat Intelligence already has a report:

   ```text
   get_file_report(hash="24d004a104d4d54034dbcffc2a4b19a11f39008a575aa614ea04703480b1022c")
   ```

   If `get_file_report` returns a recent report, skip uploading the file and move to step 5.

2. If the hash is unknown and you have approval to share the sample, submit the file asynchronously:

   ```text
   submit_file(file_path="/quarantine/invoice_update.exe")
   ```

   Expected response:

   ```json
   {
     "id": "NjY0YjRlOTcxNTRhM2JjZGVmMDEyMzQ1Njc4OWFiY2Q6MTczMDU5MjAwMA==",
     "type": "analysis"
   }
   ```

3. Poll `get_analysis` with the returned `id`. Keep `include_engine_results=False` (the default) so 70+ individual scanner entries do not flood your model context window:

   ```text
   get_analysis(
     analysis_id="NjY0YjRlOTcxNTRhM2JjZGVmMDEyMzQ1Njc4OWFiY2Q6MTczMDU5MjAwMA=="
   )
   ```

   Expected response once `attributes.status` reaches `"completed"`:

   ```json
   {
     "id": "NjY0YjRlOTcxNTRhM2JjZGVmMDEyMzQ1Njc4OWFiY2Q6MTczMDU5MjAwMA==",
     "type": "analysis",
     "attributes": {
       "status": "completed",
       "date": 1730592045,
       "stats": {
         "malicious": 58,
         "suspicious": 2,
         "undetected": 12,
         "harmless": 0,
         "timeout": 0,
         "failure": 0,
         "type-unsupported": 4
       }
     },
     "meta": {
       "file_info": {
         "sha256": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
         "md5": "d41d8cd98f00b204e9800998ecf8427e",
         "size": 245760
       }
     }
   }
   ```

   If `attributes.status` is `"queued"` or `"in-progress"`, finish your surrounding enrichment steps and call `get_analysis` again after 15 to 30 seconds.

4. If you need vendor-specific signature names to diagnose a borderline detection (`malicious` between 1 and 3), re-fetch the completed analysis with `include_engine_results=True`:

   ```text
   get_analysis(
     analysis_id="NjY0YjRlOTcxNTRhM2JjZGVmMDEyMzQ1Njc4OWFiY2Q6MTczMDU5MjAwMA==",
     include_engine_results=True
   )
   ```

5. Pivot from the file's `sha256` into dynamic sandbox behavior and network infrastructure:

   ```text
   get_file_behavior_summary(
     hash="e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855"
   )
   get_entities_related_to_a_file(
     hash="e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
     relationship_name="contacted_domains",
     descriptors_only=True,
     limit=10
   )
   ```

## Scan a suspicious URL and trace redirects

Use `submit_url` during phishing triage when an email or chat message contains an unfamiliar link.

1. Submit the URL for live scanning:

   ```text
   submit_url(url="https://login-check-example.invalid/auth/verify")
   ```

2. Poll `get_analysis` with the returned `id` until `attributes.status` is `"completed"`:

   ```text
   get_analysis(analysis_id="u-9f86d081884c7d659a2feaa0c55ad015a3bf4f1b2b0b822cd15d6c15b0f00a08-1730592100")
   ```

3. Pull the consolidated URL report and inspect downstream redirect chains or dropped payloads. Pass `descriptors_only=True` when the target relationship returns URLs or files:

   ```text
   get_url_report(url="https://login-check-example.invalid/auth/verify")
   get_entities_related_to_an_url(
     url="https://login-check-example.invalid/auth/verify",
     relationship_name="redirects_to",
     descriptors_only=True,
     limit=10
   )
   get_entities_related_to_an_url(
     url="https://login-check-example.invalid/auth/verify",
     relationship_name="downloaded_files",
     descriptors_only=True,
     limit=10
   )
   ```

## Refresh stale verdicts on known indicators

Cached reports can lag behind newly deployed threat infrastructure or updated scanner signatures. Check `last_analysis_date` in the entity report first. If the timestamp predates the incident window, request a fresh scan without re-uploading any artifact:

- **Known file hash:**

  ```text
  reanalyze_file(hash="44d88612fea8a8f36de82e1278abb02f")
  ```

- **Known URL:**

  ```text
  reanalyze_url(url="https://login-check-example.invalid/auth/verify")
  ```

- **Domain reputation refresh:**

  ```text
  reanalyze_domain(domain="login-check-example.invalid")
  ```

- **IPv4 or IPv6 reputation refresh:**

  ```text
  reanalyze_ip(ip_address="203.0.113.42")
  ```

Each `reanalyze_*` call returns an analysis descriptor (`{"id": "...", "type": "analysis"}`). Pass `id` to `get_analysis(analysis_id)` to confirm completion, then re-read the updated entity report (`get_file_report`, `get_url_report`, `get_domain_report`, or `get_ip_address_report`).
