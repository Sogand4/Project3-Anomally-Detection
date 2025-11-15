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

## 7. SpecKit Role in This Project
This overview guides:
- promises in `project3.yaml`  
- DNS, log retention, and data handling policies in `policy/`  
- failing red bar tests in `tests/redbar/`  
- monetization reasoning in `analysis/monetization/`  
- ethics debt entries in `docs/ethics_debt_ledger.md`