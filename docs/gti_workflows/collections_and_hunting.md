# Curate threat collections, hunting rules, and Digital Threat Monitoring

This guide walks through four threat intelligence workflows in `gti-mcp`: filtering threats with organization Threat Profiles, mapping collections to MITRE ATT&CK and detection rules, pivoting across IOC commonalities to build custom collections, and searching Digital Threat Monitoring (DTM) for external leaks.

## Prioritize threats with Threat Profiles

Before running a broad search across all threat collections, check whether your organization maintains Threat Profiles scoped to its target industries and regions.

1. List configured Threat Profiles:

   ```text
   list_threat_profiles(limit=10)
   ```

2. Inspect a profile's configured target industries, regions, malware roles, and actor motivations:

   ```text
   get_threat_profile(profile_id="0192a3b4-c5d6-7e8f-9a0b-1c2d3e4f5a6b")
   ```

3. Pull recommended and user-followed threat collections associated with that profile, along with its recent association timeline:

   ```text
   get_threat_profile_recommendations(
     profile_id="0192a3b4-c5d6-7e8f-9a0b-1c2d3e4f5a6b",
     limit=10
   )
   get_threat_profile_associations_timeline(
     profile_id="0192a3b4-c5d6-7e8f-9a0b-1c2d3e4f5a6b",
     limit=10
   )
   ```

4. Pass any returned collection `id` to `get_collection_report(id)` for full attribution and context.

## Map a campaign to MITRE ATT&CK and extract hunting rules

Once you identify a relevant threat actor, campaign, or malware family collection, pull its curated timeline, ATT&CK techniques, and associated detection rules.

1. Search for the campaign, actor, or malware family, then fetch its collection report and analyst timeline:

   ```text
   search_threats(query="UNC3944", collection_type="threat-actor", limit=5)
   get_collection_timeline_events(id="threat-actor--...")
   ```

2. Retrieve the collection's MITRE ATT&CK tree and full attack technique objects. Set `descriptors_only=False` whenever `relationship_name` is `"attack_techniques"`:

   ```text
   get_collection_mitre_tree(id="threat-actor--...")
   get_entities_related_to_a_collection(
     id="threat-actor--...",
     relationship_name="attack_techniques",
     limit=10,
     descriptors_only=False
   )
   ```

3. Fetch curated and community detection rules linked to the collection:

   ```text
   get_collection_rules(
     collection_id="malware-family--...",
     top_n=4,
     rule_types=["curated_yara_rule", "crowdsourced_yara", "crowdsourced_sigma", "crowdsourced_ids"]
   )
   ```

   `get_collection_rules` returns standard **YARA** rules (for file and payload pattern matching), Sigma rules, and network IDS signatures. It does not return Chronicle SIEM **YARA-L 2.0** event detection rules; translate Sigma or behavioral findings into YARA-L 2.0 separately when deploying detections in Google SecOps SIEM.

4. To inspect a specific GTI Livehunt ruleset and the files it matched, call `get_hunting_ruleset` and `get_entities_related_to_a_hunting_ruleset`:

   ```text
   get_hunting_ruleset(ruleset_id="0123456789abcdef")
   get_entities_related_to_a_hunting_ruleset(
     ruleset_id="0123456789abcdef",
     relationship_name="hunting_notification_files",
     limit=10
   )
   ```

## Pivot on IOC commonalities and curate a custom collection

When you have a collection of incident indicators, GTI can compute shared attributes across those indicators (such as shared PE import hashes, mutexes, SSL certificates, or favicon hashes) and pivot across the VirusTotal corpus to find related infrastructure.

1. Summarize shared features across the indicators in a collection:

   ```text
   get_collections_commonalities(collection_id="collection--...")
   ```

2. Pivot from a shared feature (such as an `imphash` or `favicon_dhash`) either within the collection (`search_space="collection"`) or across the full VirusTotal dataset (`search_space="corpus"`):

   ```text
   get_collection_feature_matches(
     collection_id="collection--...",
     feature_type="imphash",
     feature_id="f34d5f2d4577ed6d9ceec516c1f5a744",
     entity_type="file",
     search_space="corpus",
     entity_type_plural="files",
     descriptors_only=True
   )
   ```

3. Track confirmed indicators from your investigation in a private GTI collection:

   ```text
   create_collection(
     name="IR-2026-1103 Phishing Infrastructure",
     description="Confirmed staging domains and payload hashes from case 4812.",
     iocs=[
       "login-check-example.invalid",
       "203.0.113.42",
       "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855"
     ],
     private=True
   )
   ```

4. Add or remove indicators as the investigation evolves, and update tags or descriptions on the collection:

   ```text
   update_iocs_in_collection(
     id="collection--...",
     relationship="domains",
     iocs=["cdn-check-example.invalid"],
     operation="add"
   )
   update_collection_attributes(
     id="collection--...",
     attributes={
       "tags": ["case-4812", "phishing", "active-containment"]
     }
   )
   ```

## Search Digital Threat Monitoring for external leaks

Use `search_digital_threat_monitoring` to query surface, deep, and dark web forums, Telegram channels, paste sites, and ransomware victim listings using Lucene syntax.

1. Scope queries with uppercase boolean operators (`AND`, `OR`, `NOT`), document types (`__type`), threat labels (`label_threat`), and RFC3339 UTC bounds (`since` and `until`) so broad searches do not hit the 60-second query timeout:

   ```text
   search_digital_threat_monitoring(
     query='(__type:(forum_post OR message OR paste)) AND (label_threat:information-security/information-leak/credentials) AND (domain:"example.com")',
     size=10,
     since="2026-10-01T00:00:00Z",
     until="2026-11-03T00:00:00Z",
     truncate="500",
     sanitize=True
   )
   ```

2. If the response contains a non-empty `page` token, fetch the next page by passing the exact same `query`, `size`, `since`, `until`, `truncate`, and `sanitize` values together with `page`:

   ```text
   search_digital_threat_monitoring(
     query='(__type:(forum_post OR message OR paste)) AND (label_threat:information-security/information-leak/credentials) AND (domain:"example.com")',
     size=10,
     since="2026-10-01T00:00:00Z",
     until="2026-11-03T00:00:00Z",
     page="eyJafter...",
     truncate="500",
     sanitize=True
   )
   ```
