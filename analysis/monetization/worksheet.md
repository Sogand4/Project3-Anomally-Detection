# Monetization Worksheet Snapshot

<!--
- Link to Canvas page: https://canvas.ubc.ca/courses/168892/pages/project3-monetization-and-policy-worksheet
- Record projected revenue, policy touchpoints, and acceptance tests here.
- Update `project3.yaml` so each monetization event references this file.
-->

## 1. Selected Monetization Event

**Event name:** Premium Fraud Alerts (Premium SLA pattern)  
**Description:** Paid tier that delivers fraud alerts faster and refreshes dashboards more frequently, while keeping the same fraud model, telemetry fields, and retention windows as the standard tier.  
(References: `terms_of_service.md §4.3`, `privacy_addendum.md §3.1`, `data_handling_policy.md §3.2`)

## 2. Baseline Cloud Spend

| Cost Area              | Est. Monthly Cost | Notes                                               |
|------------------------|------------------:|-----------------------------------------------------|
| API Gateway + WAF      |            \$250  | Ingest for CA and IN regions                        |
| Stream Processing      |            \$400  | Kafka or Kinesis, moderate throughput               |
| Model Hosting          |            \$300  | Shared fraud model inference                        |
| Storage (logs + data)  |            \$150  | 30 day raw logs, 1 year anonymized aggregates       |
| Monitoring / Tracing   |             \$80  | Metrics, logs, traces                               |
| **Total baseline**     |     **≈ \$1,180** | Sensitivity about ±25 percent                       |

If overall usage drops by about 30 percent, baseline spend is roughly in the \$820–900 range.

---

## 3. Revenue Mix for Premium Alerts

- Price for premium: **\$20 per merchant per month**  
- Expected number premium merchants in month one: **80–120**

**Projected monthly revenue**

- Low: 80 × \$20 = **\$1,600**  
- Mid: 100 × \$20 = **\$2,000**  
- High: 120 × \$20 = **\$2,400**

**Sensitivity (30 percent drop in adoption)**

- Applied to the low end of the expected merchant range: 56 merchants × \$20 ≈ **\$1,120 per month**

Even in the 30 percent drop scenario, premium revenue covers the marginal costs of faster delivery and dashboard refresh, though not the entire baseline platform cost.

## 4. Policy Footprint

| Area              | Policy Touchpoint                                                                 |
|-------------------|-----------------------------------------------------------------------------------|
| **Terms of Service**  | Premium 10–15s alert window; graceful degradation (see `terms_of_service.md §4.3–§5.2`).  |
| **Privacy Addendum**  | Same telemetry fields and 30-day raw log retention for both tiers (`privacy_addendum.md §3.1, §4.2`). |
| **DNS Policy**        | Region-locked endpoints for premium webhooks and dashboards (`dns_policy.md §3.1, §4.3`). |
| **Log Retention Policy** | 30-day raw log retention, 1-year aggregates shared across tiers (`log_retention_policy.md §2.1, §5.1`). |
| **Data Handling Policy** | No PAN, CVV; same data fields and feature vectors for all merchants (`data_handling_policy.md §2.1, §3.2`). |

These references satisfy the rubric requirement to link monetization to explicit policy clauses.

## 5. Clause → Control → Test Linkage

- **Clause:** Premium alerts generate revenue but cannot modify the fraud model, telemetry fields, data residency, or retention windows (see `terms_of_service.md §6.1`, `privacy_addendum.md §3.1`, `data_handling_policy.md §3.2`, `dns_policy.md §3.1`).  
- **Control:** Shared fraud model; shared telemetry schema; feature flags controlling premium routing; region-locked DNS; same S3 lifecycle rules (`log_retention_policy.md §5.1`).  
- **Acceptance test path:**  
  `tests/redbar/test_monetization_guardrail.py::test_premium_overload_does_not_push_standard_behind_baseline`

The acceptance test ensures no monetization shortcut introduces new telemetry, longer retention, or cross-region routing.

## 6. Ethics Debt Note

Empty chair stakeholder: **small Indian merchants** on the standard tier.

- Risk: engineering or routing shortcuts might benefit premium merchants in ways that harm standard merchants during incidents.  
- Mitigation: identical model, telemetry, retention, and residency rules across tiers (see `privacy_addendum.md §3.1`, `data_handling_policy.md §2.1`, `dns_policy.md §3.1`).  
- This issue is mirrored in the ethics ledger (`docs/ethics_debt_ledger.md` entry dated 2025-11-17 and 2025-11-20).