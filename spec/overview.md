# Spec Overview (replace with SpecKit draft)

<!-- Describe the anomaly detection scenario, stakeholders, and jurisdictional constraints.
- Reference monetization events and expected telemetry flows.
- Link to Clause→Control→Test promises in `tests/redbar/`. -->

## 1. Scenario Summary
Payments Fraud Radar is a real time anomaly detection platform for e commerce transactions across **Canada** and **India**. The system ingests continuous payment telemetry, produces a fraud score within seconds, and fans out alerts to merchants and risk teams. A premium tier offers faster alert delivery and richer dashboards, but all merchants rely on the same baseline fraud model to avoid discriminatory outcomes.

The platform must operate under **PIPEDA** (Canada) and **DPDP** (India), which shape requirements for telemetry minimization, log retention controls, and regional data residency.

---

## 2. Stakeholders
### Primary Stakeholders
- **Cardholders** harmed by false positives blocking legitimate transactions.  
- **Merchants (Standard Tier)** depending on timely, accurate fraud scoring; harmed by outages or unfair detection.  
- **Merchants (Premium Tier)** paying for faster alerts; harmed if premium features weaken fairness or privacy.  
- **Risk and Compliance Teams** ensuring PIPEDA and DPDP alignment.  
- **SRE and On Call Engineers** responsible for uptime and failover behavior.

TODO: others?
### Empty Chair Stakeholder
- **Small Indian Merchants** at risk of revenue loss if outages, false positives, or data misrouting affect their ability to process legitimate payments. All monetization and DNS/log decisions must consider their harm first.

---

## 3. Telemetry Flows
Incoming transaction events contain:
- tokenized card identifier  
- merchant ID  
- transaction amount and currency  
- device fingerprint hash  
- region tag (`CA` or `IN`)  
- model feature vector and fraud score  
- optional premium alert routing metadata (webhook, retries)

Telemetry flows through:
1. **Ingress layer** (API gateway, stream processor)  
2. **Fraud scoring pipeline** (feature engine, model inference)  
3. **Alert layer** (standard vs premium fanout)  
4. **Log sinks** (raw logs 30 day retention, aggregated metrics 1 year)  
5. **DNS routing** which decides which region processes a given merchant’s traffic

Data residency constraints require:
- **Canadian logs** stored only in **ca central 1**  
- **Indian transactions** stored in India aligned buckets  
- prevention of debug or analytics data leaving approved regions

---

# TODO
## 4. Monetization Events
### Premium Merchant Alerts
Merchants can subscribe to receive accelerated fraud alerts and enhanced dashboards. All merchants still use the same fraud model to ensure equitable protection. Premium features must not extend retention windows or introduce extra data collection.

This monetization event is described in:  
`analysis/monetization/premium_merchant_alerts.md`  
and evaluated by its acceptance test in:  
`tests/redbar/test_dns_data_residency.py::test_monetization_guardrail_placeholder`

---

## 5. Clause → Control → Test Mapping

### Promise 1 — Uptime and Graceful Degradation
- **Clause:** Fraud scoring API maintains **99.9% uptime** and degrades by suspending non critical premium fanout before failing core scoring.  
- **Control:** DNS failover, multi AZ deployment, rate limiting, latency based routing.  
- **Test:** `tests/redbar/test_dns_data_residency.py::test_uptime_placeholder`

### Promise 2 — Telemetry Privacy and Data Residency
- **Clause:** Canadian fraud telemetry remains in **ca central 1**, PAN/CVV never logged, raw logs deleted after 30 days.  
- **Control:** Log retention policy, tokenization pipeline, region tagged log sinks, DNS firewall.  
- **Test:** `tests/redbar/test_dns_data_residency.py::test_canada_log_bucket`

### Promise 3 — Monetization Guardrail (Premium Alerts)
- **Clause:** Premium alerts increase revenue without weakening privacy or fairness for standard merchants.  
- **Control:** Monetization configuration, alert throttling rules, ToS and privacy alignment.  
- **Test:** `tests/redbar/test_dns_data_residency.py::test_monetization_guardrail_placeholder`

---

## 6. Jurisdictional Alignment
- **PIPEDA:** retention minimization, regional storage, limited export.  
- **DPDP:** purpose limitation, region labeling, consent aligned handling.  
- **DNS routing** ensures telemetry from CA/IN stays within approved jurisdictions.

---

# TODO
## 7. Architecture Overview

![architecture diagram](architecture_diagram.png)

Edge: Merchant checkout integrations (web and mobile) call a tokenised fraud scoring API over HTTPS. Mutual TLS between merchants and edge, tenant scoped API keys, signed client config. Premium merchants use a dedicated subdomain for alert webhooks but share the same scoring endpoint.

Ingest: Regional API gateway with WAF in front. Per tenant rate limiting, schema validation, and region tagging (CA vs IN) applied at the edge. Ingress logs captured under the log retention policy, without full PAN or CVV.

Streaming core: Managed event stream (for example Kafka or Kinesis) that decouples the gateway from model services. Idempotent producers, at least once delivery, and dead letter topics for malformed or suspicious events. Separate consumer groups for standard and premium alert fanout.

Anomaly service: Shared fraud model service for all merchants. Feature computation (amount patterns, device history, merchant risk profile) and model inference are done inside the P99 detection budget. A or B experiments and shadow traffic use the same privacy constraints and never leak raw identifiers to logs.

Serving and UI: Tenant scoped APIs return fraud scores and decisions to merchants. Standard merchants receive alerts on a shared queue and dashboards refreshing about every twenty seconds. Premium merchants receive priority queued alerts and dashboards refreshing about every five seconds. Role based access control applies to all dashboards with audited break glass access.

Data stores: Region tagged log sinks and decision stores. Canadian transactions write to ca central 1 stores and Indian transactions write to India aligned stores. Raw fraud logs retained for thirty days, then rolled into aggregated, anonymised metrics kept up to one year. All stores use tokenised identifiers and exclude full PAN and CVV.

DNS and control plane: DNS routing steers merchants to the correct regional stack (CA or IN) and enforces data residency promises. DNS firewall rules block exports or internal endpoints in unapproved regions such as us east 1 for Canadian merchants. Control plane configuration is mirrored across regions without raw transaction identifiers so that policy and deployment changes can be coordinated without moving sensitive data.

Monetization path: Premium merchants enable a feature flag that attaches them to the premium alert queue, stronger alert delivery SLO, and faster dashboard refresh. No extra telemetry is collected beyond what standard merchants send, and log retention windows remain identical across tiers. These differences are documented in the monetization worksheet and ToS or privacy addendum and enforced via SpecKit Clause → Control → Test promises.

---

## 8. Success Metrics

### Platform Reliability

### Default Tier (Standard Merchants)
- **99.9% monthly uptime** for the fraud scoring API.
- **P99 detection latency ≤ 3 seconds** from ingest → model → score.
- **Alert delivery ≤ 25 seconds** (standard webhook or dashboard update).
- **Retry window:** up to **2 retries** within 60 seconds if merchant endpoint fails.
- **Dashboard refresh rate:** every **20 seconds**.

### Premium Tier (Paid Merchants)
- **99.95% monthly uptime** for alert delivery path (premium-only queue + dedicated routing).
- **P99 detection latency ≤ 2 seconds** due to priority scheduling under load.
- **Alert delivery ≤ 10 seconds** end-to-end (fraud signal → webhook push).
- **Retry window:** up to **5 retries** within 60 seconds with exponential backoff.
- **Dashboard refresh rate:** every **5 seconds**.

### Accuracy & Fairness
- **False positive rate ≤ baseline threshold** across both Canada and India.
- **No model performance degradation** between standard and premium tiers.
- **Region balanced detection outcomes** verified in aggregate logs.

### Privacy & Residency
- **100% Canadian logs stored only in ca-central-1.**
- **Raw fraud logs deleted within 30 days** with automated lifecycle controls.
- **Zero identifiable PAN/CVV fields** in any processing or alert logs.

### Monetization & Ethics Alignment
- Premium alerts generate projected revenue **without extending retention windows**.
- **No extra telemetry collected** for premium features beyond what standard merchants already provide.
- Empty chair stakeholder (small Indian merchants) remains protected in all DNS/log/policy updates.

---

## 9. Key Risks and Mitigations

### Risk 1 — Data Residency Drift  
Telemetry from Canadian merchants may be routed to or stored in an unapproved region (e.g., us-east-1) due to misconfigured DNS or analyst exports.  
**Mitigation:**  
- Route53 DNS firewall + region-locked IAM boundaries.  
- Red-bar test: `test_canada_log_bucket`.  
- Weekly policy review by compliance team.

---

### Risk 2 — False Positives Causing Merchant Revenue Loss  
Model misclassifies legitimate transactions, blocking purchases during peak hours.  
**Mitigation:**  
- Real-time feedback loop for disputed transactions.  
- P99 latency budget tracking for overloaded scoring pipeline.  
- Prioritize core scoring over premium fanout under load.

---

### Risk 3 — Premium Tier Distorts Fairness  
Premium merchants receive materially different detection outcomes, or privacy guardrails weaken to support new paid features.  
**Mitigation:**  
- Fraud model identical across tiers.  
- Premium alerts only change **delivery speed**, not detection logic.  
- Red-bar test: `test_monetization_guardrail_placeholder`.  
- Ethics debt ledger entry documenting fairness constraints.

---

### Risk 4 — Extended Log Retention (Surveillance Drift)  
Pressure to support premium analytics could push retention beyond 30 days or reintroduce sensitive identifiers.  
**Mitigation:**  
- Mandatory lifecycle policies in log sinks.  
- Processing logs scrubbed for PII before storage.  
- Red-bar test for log retention enforcement.  
- Privacy steward approval required for retention changes.

---

### Risk 5 — Outage Cascading Across Regions  
Failure in India or Canada could cascade if DNS failover is misconfigured, harming both regions’ merchants.  
**Mitigation:**  
- Region-specific failover paths and independent alert queues.  
- Chaos experiments documented in reliability packet.  
- Prioritize regional isolation in DNS policy.

---

## 10. SpecKit Role in This Project
This overview guides:
- promises in `project3.yaml`  
- DNS, log retention, and data handling policies in `policy/`  
- failing red bar tests in `tests/redbar/`  
- monetization reasoning in `analysis/monetization/`  
- ethics debt entries in `docs/ethics_debt_ledger.md`