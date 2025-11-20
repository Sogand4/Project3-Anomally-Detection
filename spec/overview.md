# Spec Overview

<!-- Describe the anomaly detection scenario, stakeholders, and jurisdictional constraints.
- Reference monetization events and expected telemetry flows.
- Link to Clause→Control→Test promises in `tests/redbar/`. -->

## 1. Anomaly Detection Scenario
Payments Fraud Radar is a real time anomaly detection platform for e commerce transactions across **Canada** and **India**. The system ingests continuous payment telemetry, produces a fraud score within seconds, and fans out alerts to merchants and risk teams. A premium tier serves as an add-on that offers faster alert delivery and richer dashboards, but all merchants rely on the same baseline fraud model to avoid discriminatory outcomes.

## 2. Stakeholders
### Primary Stakeholders
- **Cardholders** harmed by false positives blocking legitimate transactions.  
- **Merchants (Standard Tier)** depending on timely, accurate fraud scoring; harmed by outages or unfair detection.  
- **Merchants (Premium Tier)** paying for faster alerts; harmed if premium features weaken fairness or privacy.  
- **Risk and Compliance Teams** ensures PIPEDA and DPDP alignment.  
- **On Call Engineers** responsible for uptime and failover behavior.

### Empty Chair Stakeholder
**Small Indian Merchants at the Standard Tier**: When more merchants buy the premium tier, their alerts get sent faster. If the system is not designed carefully, this can push standard-tier alerts further down the line during busy periods. For small Indian merchants, even small delays can mean losing real customers at checkout or having more false positives that block legitimate payments. They often have tight margins, so losing just a few sales can seriously hurt their business. Smaller standard-tier merchants have fewer operational resources to absorb delays, outages, or routing mistakes, making them more exposed to harm.

In this project, we will treat small Indian standard-tier merchants as the empty chair because they are the least able to influence product decisions and the most exposed if premium traffic quietly gets priority over standard traffic. They depend on us to make sure that paid features never starve core fraud protection for everyone else.

To protect this empty chair, we promise that:

- Fraud scoring stays equal for everyone (same model, same accuracy).
- Premium only gets faster delivery, not better detection.
- During overload, premium features slow down first, so standard-tier alerts never get pushed aside or delayed.
- All data stays in the correct region, so merchants are not harmed by misrouting.

This makes sure that monetization does not come at the cost of small standard-tier merchants.

## 3. Jurisdictional Alignment

### Canada (PIPEDA)

- Canadian merchant telemetry stays in **ca-central-1**.  
- Cross-border export requires strong safeguards, so IAM and DNS prevent it by default.  
- Short-lived identifiable data (30-day TTL) supports access, correction, and deletion rights.

### India (DPDP)

- Indian merchant telemetry processed only in **approved Indian jurisdictions**.  
- Purpose limitation enforced by using only attributes required for fraud detection.  
- Identifiable data follows the same 30-day TTL, supporting data principal rights.

### Common Controls (Applied to Both Regions)

- Regional routing at ingestion ensures data stays in its jurisdiction.  
- Identifiable raw logs deleted after **30 days**; long-term analytics rely only on anonymized aggregates.  
- Cross-region writes blocked by IAM, DNS routing, and red-bar tests.  
- Encryption in transit and at rest for all telemetry.  
- Event-level audit logs for access, scoring, and export attempts.  
- Premium features change alert delivery time, not underlying data processing.  

### Residency

- **Canada:** ca-central-1  
- **India:** ap-south-1 
- Any cross-region analysis uses **only de-identified aggregates**.

## 4. Telemetry Flows and Monetization Events

This section outlines how transaction telemetry moves through the system and how monetization features interact with that pipeline. Concrete performance numbers are included to make expectations explicit and consistent with the rest of Project 3.

### Telemetry Flows

Incoming transaction telemetry includes:
- tokenized card identifier  
- merchant ID  
- transaction amount and currency  
- device fingerprint hash  
- region tag (`CA` or `IN`)  
- model feature vector and fraud score  
- optional premium routing metadata (webhook URL, retry count)

Telemetry follows a strict region-pinned pipeline:

**1. Ingestion**  
- Transaction POST request enters through `/api/v1/score`.  
- Events are routed to jurisdiction-specific topics:  
  - `fraud-events-ca` in **ca-central-1**  
  - `fraud-events-in` in **ap-south-1**  
- Ingestion SLO: **p95 < 120 ms** across regions.

**2. Feature and Scoring Pipeline**  
- Feature engine produces a vector in under **80 ms**.  
- ML model returns a fraud score and decision with **p99 < 200 ms**.  
- Threshold defaults:  
  - score ≥ 0.8 → block  
  - 0.5–0.8 → review  
  - < 0.5 → approve  
- Purpose limitation enforced: only attributes required for scoring are processed.

**3. Alert Layer**  
Two separate fanout queues prevent interference:

- **Standard merchants**  
  - dashboard notification only  
  - typical delivery: **1–3 minutes**

- **Premium merchants**  
  - dedicated queue with capped worker pool  
  - webhook delivery within **< 10 seconds** (p99 < 15 seconds)  
  - retries: exponential backoff, max **5 attempts**  
  - premium alerts never trigger extra data collection

**4. Retention**  
- Identifiable raw logs: **30-day TTL**  
- Aggregated and anonymized metrics: **1 year retention**  
- No debugging dumps or analytics exports may leave the region.

**5. Region Routing and Residency**  
- DNS ensures CA merchants resolve to **ca-central-1**, IN merchants to **ap-south-1**.  
- IAM denies cross-region writes (for both standard and premium flows).  
- Red-bar tests verify:  
  - no scoring happens outside the merchant’s region  
  - no raw telemetry leaves its jurisdiction

## 5. Monetization Events

Premium features build on the same fraud model and data pipeline, offering faster delivery without changing what data is collected or how long it is retained.

**Premium Merchant Alerts**  
- Accelerated alert delivery: **< 10 seconds p95**  
- Dedicated queue separate from scoring CPU to avoid interference  
- Same fraud model used for both tiers (mandated fairness rule)  
- Premium never extends retention or adds new fields  
- If system load spikes, premium alerts degrade **first**, never scoring

**Premium Dashboard Refresh**  
- Faster refresh cycle: **5–10 second** update intervals  
- Standard dashboards refresh every **30–60 seconds**  
- Both dashboards use the same anonymized aggregates

**Billing Telemetry**  
- Counts of premium alerts delivered (daily)  
- Stored regionally and retained for **30 days**  
- Never contains card tokens, device hashes, or scores

Documentation and enforcement:  
- Monetization design in `analysis/monetization/premium_merchant_alerts.md`  
- Residency guardrail tested by `tests/redbar/test_dns_data_residency.py::test_monetization_guardrail_placeholder`

TODO: should i be only using one test?
## 6. Clause → Control → Test Mapping
### Promise 1 — Uptime and Graceful Degradation

**Clause**  
The fraud scoring API maintains **99.9% monthly uptime**. Under load or partial failure, the platform suspends **premium alert fanout first**, keeping core fraud scoring available for all merchants (including small Indian merchants as the empty-chair stakeholder).

**Control**  
- Multi-AZ deployment for the scoring service  
- Health-checked scoring endpoints behind the load balancer  
- Uptime SLO dashboard and alerts  
- Load-based circuit breaker that pauses premium alert fanout before impacting scoring  
- Alert queue configuration that preserves baseline standard-tier latency even when premium volume spikes  

**Enforcement Point**  
- *(DNS firewall / routing)* DNS routing and load balancer rules removing unhealthy instances  
- *(Reliability control)* Circuit-breaker and queue priority configuration  
- *(Data policy for SLO transparency)* SLO metrics and dashboards for 99.9% uptime 

**Tests**  
- `tests/redbar/test_uptime_reliability.py::test_multi_az_deployment_active`  
- `tests/redbar/test_uptime_reliability.py::test_health_check_endpoints_monitored`  
- `tests/redbar/test_uptime_reliability.py::test_monthly_uptime_slo_tracking`  
- `tests/redbar/test_uptime_reliability.py::test_graceful_degradation_order`  
- `tests/redbar/test_monetization_guardrail.py::test_premium_overload_does_not_push_standard_behind_baseline`  

---

### Promise 2 — Telemetry Privacy and Data Residency

**Clause**  
Canadian fraud telemetry remains in **ca-central-1**, Indian telemetry remains in **ap-south-1** (or other India-approved regions). PAN (Primary Account Number) and CVV (Card Verification Value) are never written to logs. **Raw fraud logs are deleted within 30 days**, with only anonymized aggregates retained up to one year, and retention is identical for standard and premium tiers.

**Control**  
- Region-locked log sinks for CA and IN  
- **Log retention controls** via S3 lifecycle rules expiring raw logs at 30 days  
- Tokenization of card data at ingress  
- Input validation that rejects CVV and prevents PAN/CVV from entering logs  
- ToS, Privacy Addendum, and Log Retention Policy that fix the 30-day plus 1-year pattern  

**Enforcement Point**  
- *(DNS firewall)* DNS routing policy preventing cross-region writes  
- *(Log retention control)* S3 lifecycle expiration rules  
- *(Data policy)* `terms_of_service.md`, `privacy_addendum.md`, `log_retention_policy.md`  

**Tests**  
- `tests/redbar/test_data_residency_privacy.py::test_canadian_logs_stay_in_ca_central_1`  
- `tests/redbar/test_data_residency_privacy.py::test_indian_logs_stay_in_approved_region`  
- `tests/redbar/test_data_residency_privacy.py::test_raw_fraud_logs_deleted_within_30_days`  
- `tests/redbar/test_data_residency_privacy.py::test_pan_never_logged`  
- `tests/redbar/test_data_residency_privacy.py::test_cvv_never_logged`  
- `tests/redbar/test_monetization_guardrail.py::test_retention_windows_identical`  

---

### Promise 3 — Monetization Guardrail (Premium Alerts)

**Clause**  
**Premium alerts** may speed up delivery and improve dashboard freshness, but they **must not weaken privacy, data-retention, or fairness protections** compared to the standard tier. All merchants share:
- the **same fraud model**,  
- the **same request and event fields**,  
- the **same retention windows**,  
and premium fanout must never starve standard-tier detection.

**Control**  
- Shared model configuration for standard and premium scoring  
- Schema validation that enforces identical telemetry fields for both tiers  
- Identical S3 lifecycle rules applied to logs for both tiers  
- Alert queue routing that isolates premium fanout from core scoring and preserves the standard baseline  

**Enforcement Point**  
- *(Data policy)* API schemas, ToS, Privacy Addendum  
- *(Log retention control)* Lifecycle retention policies applied equally to both tiers  
- Queue and worker configuration ensuring no starvation of standard paths  

**Tests**  
- `tests/redbar/test_monetization_guardrail.py::test_premium_uses_same_fraud_model`  
- `tests/redbar/test_monetization_guardrail.py::test_premium_collects_same_telemetry_fields`  
- `tests/redbar/test_monetization_guardrail.py::test_alert_queue_routing_does_not_affect_detection`  
- `tests/redbar/test_monetization_guardrail.py::test_retention_windows_identical`  
- `tests/redbar/test_monetization_guardrail.py::test_premium_overload_does_not_push_standard_behind_baseline`  

## 7. Architecture Overview

![architecture diagram](architecture_diagram.png)

### Edge and Ingestion

- Merchants call the fraud scoring API over HTTPS with tenant scoped API keys.  
- Traffic enters through a **regional API gateway + WAF**:  
  - Canada: `ca-central-1`  
  - India: `ap-south-1`  
- Gateway responsibilities:  
  - schema validation  
  - per-tenant rate limiting  
  - attach region tag (`CA` or `IN`)  
- Ingress logs:  
  - follow the 30-day raw log retention rule  
  - contain no PAN or CVV  

---

### Streaming and Scoring Pipeline

- Events flow into a **region-specific event stream** (Kafka or Kinesis).  
- The stream decouples ingestion from compute and supports retries and DLQs.  
- Each region hosts a **fraud model service** that:  
  - computes features  
  - runs the **same model** for standard and premium merchants  
  - produces a fraud score and decision within the P99 budget  
- No raw cardholder identifiers appear in model or scoring logs.

---

### Alerting and Dashboards

- Scoring outputs are written to **two queues per region**:  
  - Standard alert queue  
  - Premium alert queue  
- Standard tier:  
  - dashboard refresh about every **20–60 seconds**  
  - no real-time webhook  
- Premium tier:  
  - dedicated queue  
  - webhook delivery **<10 seconds (p99 <15s)**  
  - dashboard refresh about **5–10 seconds**  
- Both tiers use:  
  - identical model  
  - identical telemetry fields  
  - identical retention windows  

---

### Logging and Storage

- Logs and decisions are written to **region-tagged sinks**:  
  - Canadian telemetry stored only in `ca-central-1`  
  - Indian telemetry stored only in `ap-south-1`  
- Retention rules:  
  - raw logs deleted after **30 days**  
  - aggregated, anonymized metrics kept up to **1 year**  
- All identifiers are tokenized.  
- PAN and CVV are never logged.

---

### DNS and Control Plane

- **DNS routing** directs CA traffic to CA stack and IN traffic to IN stack.  
- DNS firewall prevents cross-region access or exports.  
- Control plane defines:  
  - DNS and residency rules  
  - log retention policy  
  - model version configuration  
  - premium feature flags  
- Monitoring covers:  
  - uptime SLO tracking  
  - P99 scoring latency  
  - premium degradation order  
  - export attempts  
  - queue health  

---

### Monetization Path

- Premium tier enabled through a **feature flag**.  
- Premium queue provides:  
  - <10 second alert delivery  
  - faster dashboard refresh  
- Premium **does not**:  
  - collect new telemetry  
  - extend retention  
  - use a different model  
  - alter privacy guarantees  
- Guardrail enforced by red-bar tests ensuring:  
  - same fields  
  - same model  
  - same retention  
  - no starvation of standard-tier alerts or scoring  

## 8. Success Metrics

### Platform Reliability

#### Default Tier (Standard Merchants)

- **99.9% monthly uptime** for the fraud scoring API (shared across all tiers).  
- **P99 detection latency ≤ 400 ms** from ingest → model → score (same as premium).  
- **Standard alert delivery ≤ 180 seconds** (1–3 minute dashboard based alerting).  
- **Retry window:** up to **2 retries** within 60 seconds if internal delivery fails.  
- **Dashboard refresh rate:** every **20–60 seconds**.

#### Premium Tier (Paid Merchants)

- **99.9% monthly uptime** for the shared fraud scoring API (same as standard).  
- **P99 detection latency ≤ 400 ms** (no tier based priority in scoring).  
- **Premium alert path SLO:** **99.95% monthly uptime** for the premium alert queue and webhook workers.  
- **Alert delivery ≤ 10 seconds** end to end (fraud signal → webhook push, p95; p99 < 15 seconds).  
- **Retry window:** up to **5 retries** within 60 seconds with exponential backoff.  
- **Dashboard refresh rate:** every **5–10 seconds**.

> Note: Scoring SLOs are identical for standard and premium to preserve fairness. Premium improves **delivery speed and availability of alerts**, not detection quality.

---

### Accuracy and Fairness

- **False positive rate** kept at or below an agreed baseline threshold across Canada and India.  
- **No model performance degradation between tiers:**  
  - same model version  
  - same feature set  
  - same thresholds  
- **Region balanced detection outcomes** monitored in aggregate, so one region (for example India) does not systematically see worse fraud outcomes.  

---

### Privacy and Residency

- **Canadian telemetry and logs stored only in `ca-central-1`.**  
- **Indian telemetry and logs stored only in `ap-south-1`.**  
- **Raw fraud logs deleted within 30 days** via S3 lifecycle policies.  
- **Aggregated, anonymized metrics kept up to 1 year** only.  
- **Zero PAN or CVV** in any processing, application, or alert logs, enforced by:  
  - tokenization at ingress  
  - input validation that rejects CVV  

---

### Monetization and Ethics Alignment

- **Premium alerts generate revenue** through faster alert delivery and faster dashboards, **not** by:  
  - collecting extra telemetry  
  - extending retention windows  
  - using a different or “better” model  
- **Same telemetry fields** for standard and premium, enforced by schema validation and tests.  
- **Same retention windows** (30-day raw, 1-year aggregates) for both tiers.  
- **No starvation of standard merchants:**  
  - premium alert queue may be suspended or slowed first under overload  
  - standard-tier scoring and baseline alert window must not regress below their pre-premium baseline  
- **Empty chair stakeholder (small Indian merchants)** explicitly protected in:  
  - data residency tests  
  - monetization guardrail tests  
  - graceful degradation behavior


## 9. Key Risks and Mitigations

### Risk 1 — Data Residency Drift  
Canadian or Indian telemetry is accidentally sent to an unapproved region (e.g., `us-east-1`) due to DNS misrouting, IAM gaps, or analyst export attempts.

**Mitigation:**  
- DNS firewall and region-pinned routing (`ca-central-1` for CA, `ap-south-1` for IN).  
- IAM denies cross-region writes for all telemetry buckets.  
- Red-bar tests:  
  - `test_canadian_logs_stay_in_ca_central_1`  
  - `test_indian_logs_stay_in_approved_region`  
- Audit logs capture export attempts.  
- Weekly policy review by privacy steward.

---

### Risk 2 — False Positives Causing Merchant Revenue Loss  
A mis-scored legitimate transaction blocks checkout, disproportionately harming small Indian merchants (empty chair) with thin margins.

**Mitigation:**  
- Real-time dispute/feedback loop (merchant can send correction events).  
- P99 scoring latency tracked to avoid timeout-driven false negatives.  
- Graceful degradation: suspend **premium fanout first**, preserve scoring under load.  
- Red-bar tests:  
  - `test_health_check_endpoints_monitored`  
  - `test_graceful_degradation_order`  
  - `test_monthly_uptime_slo_tracking`

---

### Risk 3 — Premium Tier Distorts Fairness  
Premium merchants might—intentionally or accidentally—receive:  
- better detection  
- more features  
- different model versions  
- wider telemetry collection

All of these violate your monetization guardrail.

**Mitigation:**  
- Same model version and same feature set for standard and premium.  
- Premium improves **delivery speed only**, not detection quality.  
- No new fields allowed; schema validation enforces equality.  
- Red-bar tests:  
  - `test_premium_uses_same_fraud_model`  
  - `test_premium_collects_same_telemetry_fields`  
  - `test_retention_windows_identical`  
  - `test_alert_queue_routing_does_not_affect_detection`  
  - `test_premium_overload_does_not_push_standard_behind_baseline`

---

### Risk 4 — Extended Log Retention (Surveillance Drift)  
Pressure to support premium analytics or internal analysis might extend raw log retention past 30 days or accidentally reintroduce unsafe fields.

**Mitigation:**  
- Automatic S3 lifecycle policies deleting raw logs after **30 days**.  
- Aggregates only (anonymized, 1 year max).  
- No PAN/CVV in any logs: enforced by ingress tokenization + validation.  
- Red-bar tests:  
  - `test_raw_fraud_logs_deleted_within_30_days`  
  - `test_pan_never_logged`  
  - `test_cvv_never_logged`  
- Privacy steward sign-off required for any retention changes.

---

### Risk 5 — Region Outage Leads to Cascading Failure  
A failure in Canada or India could affect the other region if DNS or queues are misconfigured, causing a global outage.

**Mitigation:**  
- Regions operate independently (isolated streams, alert queues, model services).  
- DNS routing strictly keeps traffic within its region; no automatic cross-region failover.  
- Chaos experiments validate failure modes (AZ outage, queue overload).  
- Red-bar tests:  
  - `test_multi_az_deployment_active`  
  - `test_uptime_placeholder` (99.9% SLO enforcement)  
  - `test_health_check_endpoints_monitored`

---

### Risk 6 — Premium Overload Harms Standard Merchants  
High volume premium merchants could saturate workers and delay standard-tier alerts.

**Mitigation:**  
- Alert queues separated by tier.  
- Premium fanout gets suspended first during overload (circuit breaker).  
- Standard-tier baseline alert window preserved.  
- Red-bar tests:  
  - `test_alert_queue_routing_does_not_affect_detection`  
  - `test_premium_overload_does_not_push_standard_behind_baseline`  
  - `test_graceful_degradation_order`

## 10. SpecKit Role in This Project
This overview guides:
- promises in `project3.yaml`  
- DNS, log retention, and data handling policies in `policy/`  
- failing red bar tests in `tests/redbar/`  
- monetization reasoning in `analysis/monetization/`  
- ethics debt entries in `docs/ethics_debt_ledger.md`