# Data Handling Policy: Payments Fraud Radar

## 1. Purpose

This policy defines how data is **classified, processed, and stored** within Payments Fraud Radar.  
It supports:

- Data residency requirements (Canada + India)  
- Minimizing privacy risk (especially Surveillance Drift)  
- Fair monetization (premium tier must not alter data handling)  
- Protection for the designated empty-chair stakeholder: **small Indian merchants on the standard tier**  

It aligns with controls defined in:

- `privacy_addendum.md`  
- `terms_of_service.md`  
- `log_retention_policy.md`  
- `dns_policy.md`  

---

## 2. Data Classification

### 2.1 High Sensitivity  
(Strict access, short retention)

- Tokenized transaction identifiers  
- Transaction metadata (amount, currency)  
- Device fingerprint hash  
- Fraud score + model feature vector  
- Webhook delivery logs containing status codes and retry counts  

**Storage:**  
- CA merchants → `ca-central-1`  
- IN merchants → `ap-south-1`  
- Never copied to other regions  

**Retention:**  
- 30 days (defined in `log_retention_policy.md`)  

---

### 2.2 Medium Sensitivity  
(Operational value, moderate retention)

- Aggregated fraud metrics (daily/hourly)  
- DNS firewall logs  
- Health and routing metrics (no identifiers)  

**Storage:** regional only  
**Retention:** 30–365 days depending on log type

---

### 2.3 Low Sensitivity  
(Operational metadata only)

- Application health logs  
- CPU/memory metrics  
- Deployment logs  

**Storage:** regional  
**Retention:** 90 days  

---

### 2.4 Regulatory (Immutable)

- IAM and S3 access audit logs  
- Lifecycle policy change history  
- Break-glass access history  

**Retention:** 7 years  
**Reason:** PIPEDA + DPDP compliance  

---

## 3. Allowed Processing

### 3.1 Permitted  
Processing is allowed only when it meets:

- Fraud detection  
- Alert delivery  
- Webhook retries  
- Short-term fraud investigation  
- Aggregate reporting (non-identifiable)  
- Operational monitoring  

This covers only what is necessary for the platform to function.

### 3.2 Prohibited  
The following are explicitly forbidden:

- **Cross-merchant profiling**  
- **Credit scoring or creditworthiness inference**  
- **Model training using raw identifiable logs older than 30 days**  
- **Premium-only data enrichment**  
- **Any cross-region compute or data transfer**  

### 3.3 Model Training Rules  
Model training may use:

- Raw logs ≤ 30 days old  
- Permanently anonymized feature vectors  
- Aggregates (non-identifiable)  

Training must never use:

- PAN, CVV, identity numbers  
- Merchant-specific behavioural patterns  

---

## 4. Storage Regions

### 4.1 Canadian Merchants  
- All identifiable data must remain in `ca-central-1`  
- No replication to other regions  
- DNS and IAM boundaries enforce this (`dns_policy.md`)  

### 4.2 Indian Merchants  
- All identifiable data must remain in `ap-south-1`  
- Region isolation prevents cascading impact (Risk 5)  

### 4.3 Control Plane Exceptions  
Deployment metadata (no identifiers) may exist in a central region.  
It must **never** contain:

- Tokenized identifiers  
- Fraud scores  
- Merchant-level patterns  

---

## 5. Data Handling Rules That Enable Monetization

Premium features include faster alert delivery and dashboard refresh speeds.  
**Premium merchants do not receive additional data**, longer retention, or privileged access.

### 5.1 Promise → Clause Mapping

| Monetization Promise | Data Handling Clause | Enforcement |
|----------------------|----------------------|-------------|
| Premium tier uses same fraud model | “All merchants share identical detection logic.” | Feature flags + acceptance test |
| Premium tier cannot weaken privacy | “No premium-only processing paths, retention, or logs.” | Identical storage regions + retention |
| Premium alerts use same data | “No additional fields collected for premium merchants.” | Ingestion schema validator |
| Faster reporting only | “Premium dashboards read from same aggregates.” | Dashboard configuration |

These rules protect the empty-chair stakeholder by ensuring premium features **never introduce fairness or privacy regressions**.

---

## 6. Empty-Chair Stakeholder Protection

The platform designates **small Indian merchants** as the empty-chair stakeholder.  
Data handling policies safeguard them by ensuring:

### 6.1 Equal Privacy Guarantees  
- Same 30-day raw retention  
- Same region-locked storage rules  
- Same access controls  
- Same fraud model  

### 6.2 Equal Policy Recourse  
Small Indian merchants may:

- Request deletion of their raw logs (within 30 days)  
- Request export of their data (secure portal)  
- Challenge incorrect fraud scores  
- Escalate issues to the Privacy Steward  

### 6.3 No Monetization Drift  
Premium tier must not:

- Increase retention  
- Add new telemetry fields  
- Re-route them through global accelerators  
- Change data residency  

These guardrails ensure that monetization cannot disadvantage the empty-chair stakeholder.

---