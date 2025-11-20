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
| 2025-11-10 | ChatGPT-5.1  | “Give me a monetization plan for dynamic fraud pricing.” | Suggested a pricing model where fees scale with transaction volume and fraud rate. | Discard | Violated rubric: monetization must not alter detection quality or create surveillance incentives; switched back to Premium Alerts monetization. |
| 2025-11-11 | ChatGPT-5.1  | “Write Data Residency section using Canada + India constraints.” | Clear region-locked residency rules and mapping to red-bar enforcement. | Keep | Fully aligned with rubric residency clause and tests. |
| 2025-11-11 | ChatGPT-5.1  | “Draft risk register mitigation text for region drift, surveillance drift, and fairness drift.” | Identified 5 risks and tied each to mitigations + acceptance tests. | Modify | Human pass required to fit formatting of `overview.md`. |
| 2025-11-12 | ChatGPT-5.1  | “Draft privacy_addendum.md with anonymization thresholds and Clause → Control → Test mapping.” | Generated anonymization rules, consent flow, and retention enforcement. | Keep | Fully met rubric; no large changes required. |
| 2025-11-12 | ChatGPT-5.1  | “Draft DNS policy describing resolvers, firewalls, and premium routing rules.” | Produced resolver separation, deny-lists, and how firewall enforces region boundaries. | Modify | Trimmed unused sections to avoid overlap with ToS. |
| 2025-11-16 | ChatGPT-5.1  | “Refactor ToS to remove duplicated privacy commitments.” | Produced ToS v1.3 aligned with SLAs, monetization guardrails, and SLO credits. | Keep | Now matches rubric and avoids redundancy with privacy_addendum. |
| 2025-11-17 | ChatGPT-5.1  | “Help align all documents so Clause→Control→Test rows are consistent across ToS, Privacy Addendum, DNS Policy, and Log Retention Policy.” | Provided cross-document consistency and identified duplicate clauses. | Keep | Ensured rubric compliance and internal coherence. |
| 2025-11-17 | ChatGPT-5.1  | "Suggest an experiment where DNS outage tests graceful degradation." | Generated chaos experiment injecting resolver failure. | Keep | Matches uptime promise. |
| 2025-11-17 | ChatGPT-5.1  | "Draft retention policy language for raw fraud logs." | Provided 30-day limit + region-locked buckets. | Keep | Needed for Privacy Addendum and Log Policy. |
| 2025-11-17 | ChatGPT-5.1  | "Write test ensuring premium tier cannot modify data schema." | Produced red-bar test comparing ingress schemas. | Modify | Adjusted test name and path. |
| 2025-11-17 | ChatGPT-5.1  | "Add premium worker CPU boost for SLA compliance." | Proposed giving premium alerts CPU priority. | Discard | Violated monetization guardrail: premium can get speed but cannot take system resources away from standard-tier detection. |
| 2025-11-17 | ChatGPT-5.1  | "Propose a fraud-scoring overload scenario for chaos testing." | Suggested load test where premium alert fanout pauses first. | Keep | Fits graceful-degradation requirement. |
| 2025-11-19 | ChatGPT-5.1  | “Fix section numbering and integrate Related Policies into log_retention_policy.md.” | Cleaned section numbers, added Section 13, ensured markdown consistency. | Keep | Fixed structural consistency issues before final submission. |
| 2025-11-19 | ChatGPT-5.1  | “Cross-reference missing enforcement tests and update Clause→Control→Test blocks.” | Added missing references like `test_raw_fraud_logs_deleted_within_30_days`. | Keep | Ensured test coverage aligned across policies. |
| 2025-11-19 | ChatGPT-5.1  | “Add new premium DNS privilege escalation test.” | Generated `test_premium_dns_no_privilege_escalation`. | Keep | Required for DNS monetization guardrail enforcement. |
| 2025-11-19 | ChatGPT-5.1  | “Fix Data Handling Policy inconsistencies.” | Added storage-region alignment, clarified processing limits, ensured telemetry parity. | Modify | Minor edits needed to improve clarity. |
| 2025-11-19 | ChatGPT-5.1  | “Point specific sections in ToS/Privacy/DNS/Data to each other.” | Added explicit section references (“See §5.2 of dns_policy.md,” etc.). | Keep | Strengthened rubric alignment (“link to relevant clauses”). |
| 2025-11-20 | ChatGPT-5.1  | “Fix and extend Reliability Packet with Clause→Control→Test and enforcement evidence.” | Added Runbook validation test, updated metrics, added log excerpts section. | Keep | Needed to pass reliability and observability rubric. |

## Reflection

- AI was most helpful for fast drafting of policies, DNS rules, retention rules, and Clause→Control→Test structures.  
- It kept cross-document consistency and helped catch missing enforcement tests.  
- Some outputs were modified to remove duplicated content or fit the project format.  
- Several suggestions were discarded because they violated fairness or monetization constraints.
- Human judgment was needed for final decisions on residency limits, retention, monetization guardrails, and anything affecting the empty-chair stakeholder.  
- Overall, AI accelerated writing, but every policy still required a human pass to ensure correctness and rubric alignment.
