# Ethics Debt Ledger

<!--
| Date | Harm / Stakeholder | Description | Owner | Planned Fix | Associated Test |
| ---- | ------------------ | ----------- | ----- | ----------- | ---------------- |
| YYYY-MM-DD | Empty chair: gig drivers | Premium alerts rely on tracking driver location | Student A | Add opt-out + anonymize location before export | tests/redbar/test_policy_alignment.py::test_driver_privacy |

Update whenever monetization introduces new risk. -->

This ledger tracks ethical trade-offs and emerging risks introduced through
monetization, data handling, and technical design choices. Each entry records
the impacted stakeholder, the potential harm, the owner responsible for
mitigation, and the red-bar test that should block deployment if the promise
is violated.


| Date       | Stakeholder                     | Description                                                                                                                                                                                         | Owner              | Test Path |
|------------|---------------------------------|-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|--------------------|-----------|
| 2025-11-17 | Empty chair: small Indian merchants | Premium alert speed could pressure engineering to weaken data residency or shorten-region paths. This would harm small Indian merchants who rely on predictable checkout latency and strict DPDP compliance. | Data Gov           | `tests/redbar/test_monetization_guardrail.py::test_retention_windows_identical` |
| 2025-11-17 | All merchants                   | Pressure to extend raw fraud-log retention beyond 30 days increases surveillance drift and breach exposure. Only anonymized aggregates may persist.                                                 | Privacy Steward    | `tests/redbar/test_data_residency_privacy.py::test_raw_fraud_logs_deleted_within_30_days` |
| 2025-11-17 | Empty chair: small Indian merchants | Premium routing optimizations might tempt cross-region DNS failover, violating regional isolation. Residency must remain strict for India merchants under DPDP.                                     | SRE Lead           | `tests/redbar/test_data_residency_privacy.py::test_indian_logs_stay_in_approved_region` |
| 2025-11-17 | Standard-tier merchants         | Under load, premium queues could crowd out baseline alerts, causing degraded latency for standard merchants. Graceful-degradation ordering must protect baseline first.                            | Platform Eng       | `tests/redbar/test_outage_behavior.py::test_graceful_degradation_order` |
| 2025-11-17 | Cardholders (CA + IN)           | Monetization may drive requests for new telemetry fields that violate minimal-data principles. Schema validator must block new fields without privacy review.                                       | Product Owner      | `tests/redbar/test_schema_validation.py::test_telemetry_fields_identical` |
| 2025-11-17 | All merchants                   | Premium-specific ML tuning could introduce fairness drift if models diverge. All merchants must share a single fraud model.                                                                         | ML Lead            | `tests/redbar/test_model_parity.py::test_single_model_enforced` |

## Notes

- The empty-chair stakeholder for this project is **small Indian merchants on the
  standard tier**, representing those least equipped to absorb harm from privacy
  drift, outage behavior, or monetization bias.
- This ledger must be updated whenever a new monetization idea, feature request,
  or architectural shortcut introduces additional ethical risk.
- Tests listed here are intended to remain red-bar tests; if any of them fail,
  deployment should be blocked until the underlying risk is addressed or
  consciously re-evaluated.
