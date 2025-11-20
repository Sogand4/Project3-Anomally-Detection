# Ethics Debt Ledger

<!--
| Date | Harm / Stakeholder | Description | Owner | Planned Fix | Associated Test |
| ---- | ------------------ | ----------- | ----- | ----------- | ---------------- |
| YYYY-MM-DD | Empty chair: gig drivers | Premium alerts rely on tracking driver location | Student A | Add opt-out + anonymize location before export | tests/redbar/test_policy_alignment.py::test_driver_privacy |

Update whenever monetization introduces new risk. -->

TODO: verify this with monetization. end of worksheet.md references this page for some reason lol.

This ledger tracks ethical trade-offs and emerging risks introduced through monetization, data handling, and technical design choices. Each entry records the impacted stakeholder, the potential harm, the owner responsible for mitigation, and the red-bar test ensuring future enforcement.

| Date       | Harm / Stakeholder                    | Description                                                             | Owner              | Planned Fix                                                     | Associated Test                                                            |
|------------|----------------------------------------|-------------------------------------------------------------------------|---------------------|------------------------------------------------------------------|----------------------------------------------------------------------------|
| 2025-11-17 | Empty chair: small Indian merchants    | Premium alert speed could pressure engineering to weaken residency or retention rules to improve latency. | Data Governance     | Hard-code tier-agnostic retention + DNS boundaries; enforce guardrail | tests/redbar/test_monetization_guardrail.py::test_retention_windows_identical |
| 2025-11-17 | All merchants                          | Pressure to extend raw fraud log retention beyond 30 days for analytics or premium reporting.              | Privacy Steward     | Reject retention extensions; ensure anonymized aggregates only  | tests/redbar/test_data_residency_privacy.py::test_log_retention_30_days      |
| 2025-11-17 | Empty chair: small Indian merchants    | Faster premium routing could tempt addition of cross-region failover paths, causing residency violations. | SRE Lead            | Lock resolvers per region; deny cross-region DNS resolution      | tests/redbar/test_dns_firewall.py::test_residency_enforced                   |
| 2025-11-17 | Standard-tier merchants                | Premium latency optimizations could cause degraded standard-tier alert delivery under load.               | Platform Engineering | Enforce graceful-degradation ordering (core scoring → standard → premium) | tests/redbar/test_outage_behavior.py::test_graceful_degradation_order |
| 2025-11-17 | Cardholders (CA + IN)                  | Feature requests may introduce new telemetry fields incompatible with minimal data principle.             | Product Owner       | Schema validator blocks new fields; require privacy approval    | tests/redbar/test_schema_validation.py::test_telemetry_fields_identical |
| 2025-11-17 | All merchants                          | Engineering pressure to tune fraud model differently for premium tier could introduce fairness drift.     | ML Lead             | Single shared model; prohibit premium-specific features          | tests/redbar/test_model_parity.py::test_single_model_enforced            |

---

### Notes
- The empty-chair stakeholder for this project is **small Indian merchants on the standard tier**, representing those least equipped to absorb harm from privacy drift, outage behavior, or monetization bias.
- This ledger must be updated **whenever a new monetization idea, feature request, or architectural shortcut introduces additional ethical risk**.
- Tests listed here must remain red-bar tests—if they fail, deployment should be blocked.

