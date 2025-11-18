# Privacy Addendum: Payments Fraud Radar
Effective Date: 2025-11-17  
Version: 1.1

> Generated with OpenAI GPT-5.1, 2025-11-17.  
Manual edits applied to ensure alignment with the system architecture, risk register, monetization guardrails, and stakeholder protections.

---

## 1. Purpose of This Addendum
This Addendum explains how Payments Fraud Radar collects, uses, stores, and protects personal data for fraud detection. It supplements the Terms of Service and fulfills the SpecKit privacy requirements, including data minimization, retention rules, region isolation, and fairness across monetization tiers.

---

## 2. Data Collected

### 2.1 Transaction and Telemetry Data
The service collects:

• Tokenized card identifier (no PAN or CVV)  
• Transaction amount and currency  
• Timestamp and region tag (Canada or India)  
• Merchant identifier  
• Device or network fingerprint (hashed)  
• Computed fraud score  
• Latency, webhook status, and other operational telemetry  

### 2.2 Monetization Event Telemetry (Required)
For premium alert delivery, we capture limited telemetry needed to validate monetization promises:

• Alert send time and delivery latency  
• Retry count  
• Dashboard refresh intervals  
• Tier label (standard or premium)

No additional personal data is introduced for monetization features.

### 2.3 What We Do Not Collect
• PAN, CVV, magnetic stripe data, PINs  
• Social security or national ID numbers  
• Behavioral profiles outside the submitted transaction  

Ingestion validation blocks prohibited fields.

---

## 3. Purpose of Use

### 3.1 Primary Use
• Fraud scoring  
• Anomaly detection  
• Alert delivery

### 3.2 Secondary Use (Anonymized Aggregates Only)
• Model evaluation  
• System reliability reporting  
• Compliance reporting

### 3.3 Prohibited Uses
• Marketing  
• Selling data  
• Cross merchant profiling  
• Training models outside approved regions  

---

## 4. Data Retention and Anonymization

### 4.1 Retention Windows
• Raw logs: deleted automatically after **30 days**  
• Aggregated data: retained up to **1 year**, fully anonymized  
• Audit logs: retained **7 years** (regulatory requirement)

### 4.2 Anonymization Thresholds
Aggregates are stored only when identifying attributes are removed or bucketed:

• Device hashes dropped  
• Merchant IDs replaced by region counts  
• Amounts bucketed into ranges  
• Fraud scores aggregated into percentiles  

### 4.3 Opt-Out Recourse
Cardholders may:

• Request access to logs  
• Request correction of incorrect metadata  
• Request deletion of identifiable logs (within 30-day window)  
• Object to processing (merchant assumes fraud risk)

Requests submitted to privacy@fraudradar.example.com and completed within 5 business days.

---

## 5. Data Residency and Isolation

### 5.1 Regional Boundaries
• Canada → ca central 1  
• India → ap south 1  
• No cross border transfers except when legally required

### 5.2 Enforcement
• DNS routing rules  
• IAM region boundaries  
• Region locked storage buckets  
• CI tests verifying isolation

---

## 6. Merchant Responsibilities
• Obtain cardholder consent  
• Tokenize card data before submission  
• Provide accurate metadata  
• Forward cardholder access or deletion requests within 14 days  

---

## 7. Cardholder Rights
Cardholders may request:

• Access (15 business days)  
• Correction (10 business days)  
• Deletion (within 5 business days)  
• Objection to processing (merchant decision)

---

## 8. Privacy and Security Controls
• Encryption in transit and at rest  
• Tokenization required for all payment identifiers  
• Least privilege access policies  
• Monitoring for suspicious ingestion patterns  

---

## 9. Premium Tier Fairness Guarantee
Premium tier only affects delivery speed.  
The fraud model, telemetry fields, retention windows, and region boundaries remain identical to the standard tier.

This satisfies the monetization fairness promise.

---

## 10. Risk Register Alignment

### Risk 1 — Data Residency Drift  
Clause: Region locked processing  
Control: IAM boundaries, DNS rules  
Test: `test_residency_enforced`

### Risk 2 — False Positives Causing Revenue Loss  
Clause: Scores are advisory  
Control: Merchant dispute process  
Test: `test_scoring_metadata_accessible`

### Risk 3 — Premium Tier Distorting Fairness  
Clause: Shared model and telemetry  
Control: Feature flags  
Test: `test_telemetry_fields_identical`

### Risk 4 — Surveillance Drift  
Clause: 30 day raw retention  
Control: S3 lifecycle rules  
Test: `test_log_retention_30_days`

### Risk 5 — Cascading Regional Outages  
Clause: Region isolation  
Control: Region specific queues  
Test: `test_cross_region_isolation`

---

## 11. Clause → Control → Test Summary

| Promise | Clause | Control | Test |
|---------|--------|----------|------|
| No PAN/CVV | Ingestion rejects sensitive fields | Schema validation | `test_no_pan_in_ingestion` |
| 30 day retention | Raw logs deleted in 30 days | Lifecycle policies | `test_log_retention_30_days` |
| Region isolation | Data stays in region | DNS + IAM boundaries | `test_residency_enforced` |
| Premium fairness | Identical telemetry + model | Feature flags | `test_telemetry_fields_identical` |
| No extended retention for monetization | Premium cannot alter retention | Shared pipelines | `test_reuse_retention_policies` |

---

## 12. Human Review Notes
Pending review from Privacy Steward and Engineering leads.

Items to validate:  
• Confirm merchant consent UX flow  
• Confirm retention lifecycle policy paths  
• Confirm telemetry fields included in premium latency test  
• Confirm anonymization transformations documented above

Next scheduled review: 2026-02-17

