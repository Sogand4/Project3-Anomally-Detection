# Monetization Worksheet Snapshot

<!--
- Link to Canvas page: https://canvas.ubc.ca/courses/168892/pages/project3-monetization-and-policy-worksheet
- Record projected revenue, policy touchpoints, and acceptance tests here.
- Update `project3.yaml` so each monetization event references this file.
-->

## 1. Selected Monetization Event

**Event name:** Premium Fraud Alerts (Premium SLA pattern)
**Description:** Paid tier that delivers fraud alerts faster and refreshes dashboards more frequently, while keeping the same fraud model, telemetry fields, and retention windows as the standard tier.

---

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

Even in the 30 percent drop scenario, premium revenue covers the marginal costs of providing faster delivery and more frequent dashboard refresh, though it does not cover the full baseline cost of operating the shared fraud scoring platform.

---

## 4. Policy Footprint

| Area              | Policy Touchpoint                                                                 |
|-------------------|-----------------------------------------------------------------------------------|
| Terms of Service  | Promise that premium alerts deliver within a defined window (for example ≤10 s).  |
| Privacy Addendum  | State that premium tier uses the same telemetry and retention windows as standard.|
| DNS Policy        | Region locked endpoints for premium webhooks and dashboard access.               |
| Log Policy        | Confirm 30 day raw log retention and 1 year aggregates for both tiers.           |
| Data Policy       | Confirm no PAN or CVV is stored or logged for any tier.                          |

---

## 5. Clause → Control → Test Linkage

- **Clause:** Premium alerts increase revenue but do not change model behavior, telemetry fields, or retention commitments relative to the standard tier.  
- **Control:** Feature flags for premium alert queues, shared fraud model service, identical log retention policy, and region locked DNS routing.  
- **Acceptance test path:**  
  `tests/redbar/test_monetization_guardrail.py::test_premium_overload_does_not_push_standard_behind_baseline`

The acceptance test asserts that enabling premium does not introduce new telemetry fields, longer retention, or different models, and does not route traffic to unapproved regions.

---

## 6. Ethics Debt Note

Empty chair stakeholder: **small Indian merchants** who remain on the standard tier.

- Risk: engineering attention or routing changes could favor premium merchants in ways that harm standard merchants during incidents.  
- Mitigation intent: keep the fraud model, telemetry, and retention identical across tiers; premium only affects alert delivery speed and dashboard refresh rate.  
- This item is be mirrored in `docs/ethics_debt_ledger.md`.
