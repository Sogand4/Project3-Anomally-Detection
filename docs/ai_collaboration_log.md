# AI Collaboration Log

<!--
| Date | Tool | Prompt / Context | Output Summary | Keep / Modify / Discard | Rationale |
| ---- | ---- | ---------------- | -------------- | ----------------------- | --------- |
| YYYY-MM-DD | ChatGPT-4o | "Summarize premium SLA requirements..." | ... | Modify | Added jurisdiction notes manually. |

Update weekly and reference this file in `project3.yaml`. -->

| Date       | Tool         | Prompt / Context | Output Summary | Keep / Modify / Discard | Rationale |
|------------|--------------|------------------|----------------|--------------------------|-----------|
| 2025-11-10 | ChatGPT-5.1  | “Explain how premium alert fanout can be added without violating fairness.” | Produced a blueprint separating model logic from delivery-speed paths. | Keep | Matched rubric requirement that monetization cannot alter detection logic. |
| 2025-11-10 | ChatGPT-5.1  | “Draft initial Terms of Service for fraud detection system.” | Generated tier definitions, latency SLAs, and region/retention clauses. | Modify | Needed simplification and removal of privacy content better suited for `privacy_addendum.md`. |
| 2025-11-11 | ChatGPT-5.1  | “Write Data Residency section using Canada + India constraints.” | Clear region-locked residency rules and mapping to red-bar enforcement. | Keep | Fully aligned with rubric residency clause and tests. |
| 2025-11-11 | ChatGPT-5.1  | “Draft risk register mitigation text for region drift, surveillance drift, and fairness drift.” | Identified 5 risks and tied each to mitigations + acceptance tests. | Modify | Human pass required to fit formatting of `overview.md`. |
| 2025-11-12 | ChatGPT-5.1  | “Draft privacy_addendum.md with anonymization thresholds and Clause → Control → Test mapping.” | Generated anonymization rules, consent flow, and retention enforcement. | Keep | Fully met rubric; no large changes required. |
| 2025-11-12 | ChatGPT-5.1  | “Draft DNS policy describing resolvers, firewalls, and premium routing rules.” | Produced resolver separation, deny-lists, and how firewall enforces region boundaries. | Modify | Trimmed unused sections to avoid overlap with ToS. |
| 2025-11-13 | ChatGPT-5.1  | “Generate log_retention_policy.md from rubric requirements.” | Produced classification (raw logs, aggregates, DNS logs, audit logs) with retention windows + red-bar tests. | Keep | Strong alignment with privacy drift risk + monetization guardrail. |
| 2025-11-13 | ChatGPT-5.1  | “Write data_handling.md including empty-chair recourse and processing limits.” | Added classification rules, region boundaries, and stakeholder protections. | Keep | Added missing rubric items not covered elsewhere.
| 2025-11-16 | ChatGPT-5.1  | “Refactor ToS to remove duplicated privacy commitments.” | Produced ToS v1.3 aligned with SLAs, monetization guardrails, and SLO credits. | Keep | Now matches rubric and avoids redundancy with privacy_addendum. |
| 2025-11-16 | ChatGPT-5.1  | “Draft ethics.debt_ledger.md entries for fairness drift, residency drift, and monetization risk.” | Created ledger entries with tests and owners. | Keep | Filled required deliverable precisely. |
| 2025-11-17 | ChatGPT-5.1  | “Help align all documents so Clause→Control→Test rows are consistent across ToS, Privacy Addendum, DNS Policy, and Log Retention Policy.” | Provided cross-document consistency and identified duplicate clauses. | Keep | Ensured rubric compliance and internal coherence. |
| 2025-11-17 | ChatGPT-5.1 | "Suggest an experiment where DNS outage tests graceful degradation." | Generated chaos experiment injecting resolver failure.      | Keep                     | Matches uptime promise. |
| 2025-11-17 | ChatGPT-5.1 | "Draft retention policy language for raw fraud logs."        | Provided 30-day limit + region-locked buckets.              | Keep                     | Needed for Privacy Addendum and Log Policy. |
| 2025-11-17 | ChatGPT-5.1 | "Write test ensuring premium tier cannot modify data schema." | Produced red-bar test comparing ingress schemas.            | Modify                   | Adjusted test name and path. |
| 2025-11-17 | ChatGPT-5.1 | "Propose a fraud-scoring overload scenario for chaos testing." | Suggested load test where premium alert fanout pauses first. | Keep                     | Fits graceful-degradation requirement. |

---

## Reflection

- AI accelerated drafting of all compliance documents but required human pruning to avoid over-specification.  
- AI output was most useful for structuring Clause→Control→Test mappings and tying monetization to fairness guardrails.  
- Human judgment was necessary to remove duplicate content between ToS and privacy sections, and to ensure region-locked constraints matched the architectural design.  
- No AI-generated text was used without manual verification of residency, retention, or latency claims.

