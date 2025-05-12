# Group Cases Workflow

From the last 5 cases, examine the underlying entities in the alerts and events and group the cases logically. Then, extract details from each case in each cluster to build a high fidelity understanding of each cases' disposition and involved entities. Make sure you have an in depth understanding of each case before moving on to the next step.

Then determine the priority of each case "grouping". Then for each grouping analyze and interpret the alerts to understand why each case might be relevant. Then assess the impact of each case grouping and prioritize the cases with the highest potentialy impact. Then for each case grouping examine the underlying entities and enrich any observables with GTI. Finally, search for any related security events that may be relevant to a case based on their entities (hostnames) and include those as part of your case analysis. Finally, create a comprehensive analysis report in markdown in which you present the prioritized case list, your justification, and your analysis of each case or case cluster.

Do not treat internal domains as indicators (such as those extracted from email addresses, or usernames)


# Graphviz Dotfile

```{graphviz}
digraph CaseAnalysisFlow {
    rankdir=TB;
    // Default node style (applied if not overridden)
    node [shape=box, style=rounded, fontname="Helvetica"];
    // --- Legend / Key ---
    subgraph cluster_legend {
        label = "Key / Legend";
        style = filled;
        fillcolor = whitesmoke; // Light background for the legend box
        fontsize = 10;
        fontcolor = darkslategray;
        node [shape=box, fontname="Helvetica", fontsize=9]; // Default style within legend
        key_step [label="Step / Action", shape=box, style=rounded];
        key_plan [label="Planning Step", shape=box, style="rounded,filled", fillcolor=lightyellow];
        key_tool [label="Tool Execution", shape=ellipse, style=filled, fillcolor=lightblue];
        key_result [label="Result / Summary", shape=note, align=left];
        key_report [label="Final Report", shape=note, style=filled, fillcolor=lightgrey];
        key_failed [label="Tool Not Found", shape=ellipse, style=filled, fillcolor=lightcoral]; // Added for completeness
        key_cluster [label="Phase / Grouping\n(Subgraph Border)", shape=box, style=dashed, color=gray];
        // Arrange legend items vertically using invisible edges
        key_step -> key_plan -> key_tool -> key_result -> key_report -> key_failed -> key_cluster [style=invis];
    }
    // --- End Legend ---
    // Start
    Start [label="Start Task:\nAnalyze Last 5 Cases"];
    // Planning Phase
    PlanMode1 [label="PLAN MODE:\nOutline 7-step analysis plan", shape=box, style="rounded,filled", fillcolor=lightyellow];
    PlanResponse1 [label="plan_mode_respond:\nPresent plan, request ACT MODE", shape=ellipse, style=filled, fillcolor=lightyellow]; // Style similar to plan
    PlanResult1 [label="User switches to ACT MODE", shape=note];
    Start -> PlanMode1;
    PlanMode1 -> PlanResponse1;
    PlanResponse1 -> PlanResult1;
    // Step 1: List Cases
    ListCases [label="Step 1: List Recent Cases"]; // Uses default style
    ListCasesTool [label="secops-soar.list_cases", shape=ellipse, style=filled, fillcolor=lightblue];
    ListCasesResult [label="Result:\nTop 5 Case IDs:\n553, 552, 551, 550, 549", shape=note];
    PlanResult1 -> ListCases;
    ListCases -> ListCasesTool;
    ListCasesTool -> ListCasesResult;
    // Step 2: Examine Cases (Parallel)
    Step2_Label [label="Step 2: Examine Cases (Parallel)", shape=box, style=rounded]; // Explicitly default style
    ListCasesResult -> Step2_Label;
    // Case 553 Examination
    subgraph cluster_case_553 {
        label = "Examine Case 553"; style=dashed; color=gray;
        Examine553_DetailsTool [label="Get Details (553)\nsecops-soar.get_case_full_details", shape=ellipse, style=filled, fillcolor=lightblue];
        Examine553_EntitiesTool [label="Get Entities (553)\nsecops-soar.get_entities_by_alert_group_identifiers", shape=ellipse, style=filled, fillcolor=lightblue];
        Examine553_EventsTool [label="List Events (553)\nsecops-soar.list_events_by_alert", shape=ellipse, style=filled, fillcolor=lightblue];
        Examine553_Summary [label="Summary (553):\nImpossible Travel", shape=note];
        Examine553_DetailsTool -> Examine553_EntitiesTool -> Examine553_EventsTool -> Examine553_Summary;
    }
    // Case 552 Examination
    subgraph cluster_case_552 {
        label = "Examine Case 552"; style=dashed; color=gray;
        Examine552_DetailsTool [label="Get Details (552)\nsecops-soar.get_case_full_details", shape=ellipse, style=filled, fillcolor=lightblue];
        Examine552_EntitiesTool [label="Get Entities (552)\nsecops-soar.get_entities_by_alert_group_identifiers", shape=ellipse, style=filled, fillcolor=lightblue];
        Examine552_Events1Tool [label="List Events (Alert 793)\nsecops-soar.list_events_by_alert", shape=ellipse, style=filled, fillcolor=lightblue];
        Examine552_Events2Tool [label="List Events (Alert 792)\nsecops-soar.list_events_by_alert", shape=ellipse, style=filled, fillcolor=lightblue];
        Examine552_Summary [label="Summary (552):\nChrome DLP", shape=note];
        Examine552_DetailsTool -> Examine552_EntitiesTool -> Examine552_Events1Tool -> Examine552_Events2Tool -> Examine552_Summary;
     }
     // Case 551 Examination
     subgraph cluster_case_551 {
        label = "Examine Case 551"; style=dashed; color=gray;
        Examine551_DetailsTool [label="Get Details (551)\nsecops-soar.get_case_full_details", shape=ellipse, style=filled, fillcolor=lightblue];
        Examine551_EntitiesTool [label="Get Entities (551)\nsecops-soar.get_entities_by_alert_group_identifiers", shape=ellipse, style=filled, fillcolor=lightblue];
        Examine551_Events1Tool [label="List Events (Alert 791)\nsecops-soar.list_events_by_alert", shape=ellipse, style=filled, fillcolor=lightblue];
        Examine551_Events2Tool [label="List Events (Alert 790)\nsecops-soar.list_events_by_alert", shape=ellipse, style=filled, fillcolor=lightblue];
        Examine551_Summary [label="Summary (551):\nSideload/Malware DL", shape=note];
        Examine551_DetailsTool -> Examine551_EntitiesTool -> Examine551_Events1Tool -> Examine551_Events2Tool -> Examine551_Summary;
     }
     // Case 550 Examination
     subgraph cluster_case_550 {
        label = "Examine Case 550"; style=dashed; color=gray;
        Examine550_DetailsTool [label="Get Details (550)\nsecops-soar.get_case_full_details", shape=ellipse, style=filled, fillcolor=lightblue];
        Examine550_EntitiesTool [label="Get Entities (550)\nsecops-soar.get_entities_by_alert_group_identifiers", shape=ellipse, style=filled, fillcolor=lightblue];
        Examine550_EventsTool [label="List Events (550)\nsecops-soar.list_events_by_alert", shape=ellipse, style=filled, fillcolor=lightblue];
        Examine550_Summary [label="Summary (550):\nJenkins CVE", shape=note];
        Examine550_DetailsTool -> Examine550_EntitiesTool -> Examine550_EventsTool -> Examine550_Summary;
     }
     // Case 549 Examination
     subgraph cluster_case_549 {
        label = "Examine Case 549"; style=dashed; color=gray;
        Examine549_DetailsTool [label="Get Details (549)\nsecops-soar.get_case_full_details", shape=ellipse, style=filled, fillcolor=lightblue];
        Examine549_EntitiesTool [label="Get Entities (549)\nsecops-soar.get_entities_by_alert_group_identifiers", shape=ellipse, style=filled, fillcolor=lightblue];
        Examine549_EventsTool [label="List Events (549)\nsecops-soar.list_events_by_alert", shape=ellipse, style=filled, fillcolor=lightblue];
        Examine549_Summary [label="Summary (549):\nPhishing Sim", shape=note];
        Examine549_DetailsTool -> Examine549_EntitiesTool -> Examine549_EventsTool -> Examine549_Summary;
     }
    // Edges for Parallel Step 2 - Fork
    Step2_Label -> Examine553_DetailsTool;
    Step2_Label -> Examine552_DetailsTool;
    Step2_Label -> Examine551_DetailsTool;
    Step2_Label -> Examine550_DetailsTool;
    Step2_Label -> Examine549_DetailsTool;
    // Step 3 & 4: Grouping and Prioritization
    GroupPrioritize [label="Steps 3 & 4:\nAnalyze Case Summaries,\nGroup Logically &\nPrioritize Groups"]; // Uses default style
    GroupPrioritizeResult [label="Prioritized Groups:\n1. CVE (550) - Critical\n2. Phishing (549) - High\n3. User Activity (551, 552) - Med\n4. Travel (553) - Low", shape=note, width=3];
    // Edges for Parallel Step 2 - Join
    Examine553_Summary -> GroupPrioritize;
    Examine552_Summary -> GroupPrioritize;
    Examine551_Summary -> GroupPrioritize;
    Examine550_Summary -> GroupPrioritize;
    Examine549_Summary -> GroupPrioritize;
    GroupPrioritize -> GroupPrioritizeResult;
    // Step 5: Enrichment (Iterative)
    Enrichment [label="Step 5: Enrich Indicators (Iterative)\n(Processing Groups 1 -> 2 -> 3 -> 4)"]; // Uses default style
    GroupPrioritizeResult -> Enrichment;
    // Group 1 Enrichment
    subgraph cluster_enrich_g1 {
        label = "Enrich Group 1 (CVE)"; style=dashed; color=gray;
        EnrichG1_IP_GTI [label="gti.get_ip_address_report\n(104.130.139.139)", shape=ellipse, style=filled, fillcolor=lightblue];
        EnrichG1_URL_GTI [label="gti.get_url_report\n(...:8080)", shape=ellipse, style=filled, fillcolor=lightblue];
        EnrichG1_CVE_GTI [label="gti.search_vulnerabilities\n(CVE-2024-23897)", shape=ellipse, style=filled, fillcolor=lightblue];
        EnrichG1_IP_Chron [label="secops.lookup_entity\n(104.130.139.139)", shape=ellipse, style=filled, fillcolor=lightblue];
        EnrichG1_Summary [label="Summary (G1):\nCVE Exploited, IP/URL Malicious", shape=note];
        EnrichG1_IP_GTI -> EnrichG1_URL_GTI -> EnrichG1_CVE_GTI -> EnrichG1_IP_Chron -> EnrichG1_Summary;
    }
     // Group 2 Enrichment
     subgraph cluster_enrich_g2 {
        label = "Enrich Group 2 (Phishing)"; style=dashed; color=gray;
        EnrichG2_Domain_GTI [label="gti.get_domain_report\n(bonesinoffensivebook.com)", shape=ellipse, style=filled, fillcolor=lightblue];
        EnrichG2_URL_GTI [label="gti.get_url_report\n(...invoke.js)", shape=ellipse, style=filled, fillcolor=lightblue];
        // Use specific color for failed/not found lookups
        EnrichG2_Hash1_GTI [label="gti.get_file_report\n(HTM hash) - Not Found", shape=ellipse, style=filled, fillcolor=lightcoral];
        EnrichG2_Hash2_GTI [label="gti.get_file_report\n(PNG hash) - Not Found", shape=ellipse, style=filled, fillcolor=lightcoral];
        EnrichG2_Domain_Chron [label="secops.lookup_entity\n(bonesinoffensivebook.com)", shape=ellipse, style=filled, fillcolor=lightblue];
        EnrichG2_Summary [label="Summary (G2):\nDomain/URL Malicious", shape=note];
        EnrichG2_Domain_GTI -> EnrichG2_URL_GTI -> EnrichG2_Hash1_GTI -> EnrichG2_Hash2_GTI -> EnrichG2_Domain_Chron -> EnrichG2_Summary;
     }
     // Group 3 Enrichment
     subgraph cluster_enrich_g3 {
        label = "Enrich Group 3 (User Activity)"; style=dashed; color=gray;
        EnrichG3_URL_GTI [label="gti.get_url_report\n(testsafebrowsing...)", shape=ellipse, style=filled, fillcolor=lightblue];
        EnrichG3_Hash_GTI [label="gti.get_file_report\n(test file hash)", shape=ellipse, style=filled, fillcolor=lightblue];
        EnrichG3_Summary [label="Summary (G3):\nSafe Browsing Test File/URL", shape=note];
        EnrichG3_URL_GTI -> EnrichG3_Hash_GTI -> EnrichG3_Summary;
     }
     // Group 4 Enrichment
     subgraph cluster_enrich_g4 {
        label = "Enrich Group 4 (Travel)"; style=dashed; color=gray;
        EnrichG4_IP1_GTI [label="gti.get_ip_address_report\n(SG IP)", shape=ellipse, style=filled, fillcolor=lightblue];
        EnrichG4_IP2_GTI [label="gti.get_ip_address_report\n(US IP)", shape=ellipse, style=filled, fillcolor=lightblue];
        EnrichG4_Summary [label="Summary (G4):\nIPs Benign", shape=note];
        EnrichG4_IP1_GTI -> EnrichG4_IP2_GTI -> EnrichG4_Summary;
     }
    // Edges for Enrichment Flow
    Enrichment -> EnrichG1_IP_GTI [label="Group 1"];
    EnrichG1_Summary -> EnrichG2_Domain_GTI [label="Group 2"];
    EnrichG2_Summary -> EnrichG3_URL_GTI [label="Group 3"];
    EnrichG3_Summary -> EnrichG4_IP1_GTI [label="Group 4"];
    // Step 6: Related Event Search
    RelatedEvents [label="Step 6: Search Related Events\n(Processing G3 - Host CYMBAL)"]; // Uses default style
    EnrichG4_Summary -> RelatedEvents;
    RelatedEvents_Tool [label="secops.search_security_events\n(hostname=CYMBAL, hours_back=72)", shape=ellipse, style=filled, fillcolor=lightblue];
    RelatedEvents_Result [label="Result: No events found", shape=note];
    RelatedEvents -> RelatedEvents_Tool;
    RelatedEvents_Tool -> RelatedEvents_Result;
    // Step 7: Generate Report
    GenerateReport [label="Step 7: Generate Final Report"]; // Uses default style
    RelatedEvents_Result -> GenerateReport;
    FinalReport [label="Final Markdown Report\n(attempt_completion)", shape=note, style=filled, fillcolor=lightgrey]; // Explicit style for report
    GenerateReport -> FinalReport;
}
```