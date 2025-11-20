# Privacy Addendum: Payments Fraud Radar
Effective Date: 2025-11-17  
Version: 1.2

> Generated with OpenAI GPT-5.1, 2025-11-17.  
Manual edits applied to ensure alignment with the system architecture, risk register, monetization guardrails, and stakeholder protections.

## 1. Purpose of This Addendum
This Addendum explains how Payments Fraud Radar collects, uses, stores, and protects personal data for fraud detection. It supplements the Terms of Service and fulfills the SpecKit privacy requirements, including data minimization, retention rules, region isolation, and fairness across monetization tiers.

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

Hashed device or network fingerprints are used only for detecting anomaly patterns and are retained under the same 30-day raw log policy as other transaction telemetry.

### 2.2 Monetization Event Telemetry (Required)
For premium alert delivery, we capture limited telemetry needed to validate monetization promises:

• Alert send time and delivery latency  
• Retry count  
• Dashboard refresh intervals  
• Tier label (standard or premium)

No additional personal data is introduced for monetization features. Premium telemetry follows the same 30-day raw log and 1-year anonymized aggregate retention windows as the standard tier.

### 2.3 What We Do Not Collect
• PAN, CVV, magnetic stripe data, PINs  
• Social security or national ID numbers  
• Behavioral profiles outside the submitted transaction  

Ingestion validation blocks prohibited fields.

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
The service does not use telemetry for behavioral profiling beyond fraud detection and system reliability.

Cardholders may:

• Request access to logs  
• Request correction of incorrect metadata  
• Request deletion of identifiable logs (within 30-day window)  
• Object to processing (merchant assumes fraud risk)

Cardholders or merchants may also report concerns about suspected misuse of telemetry to privacy@fraudradar.example.com for investigation.  
Requests are completed within 5 business days.

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

## 6. Merchant Responsibilities
• Obtain cardholder consent  
• Tokenize card data before submission  
• Provide accurate metadata  
• Forward cardholder access or deletion requests within 14 days

## 7. Cardholder Rights
Cardholders may request:

• Access (15 business days)  
• Correction (10 business days)  
• Deletion (within 5 business days)  
• Objection to processing (merchant decision)

## 8. Privacy and Security Controls
• Encryption in transit and at rest  
• Tokenization required for all payment identifiers  
• Least privilege access policies  
• Monitoring for suspicious ingestion patterns  

## 9. Premium Tier Fairness Guarantee
Premium tier only affects delivery speed.  
The fraud model, telemetry fields, retention windows, and region boundaries remain identical to the standard tier.

This satisfies the monetization fairness promise.

## 10. Risk Register Alignment

### Risk 1 — Data Residency Drift  
Clause: Region locked processing  
Control: IAM boundaries, DNS rules  
Test: `test_canadian_logs_stay_in_ca_central_1`, `test_indian_logs_stay_in_approved_region`

### Risk 2 — False Positives Causing Revenue Loss  
Clause: Scores are advisory  
Control: Merchant dispute process  
Test: (no automated test present; validated through scoring metadata access process)

### Risk 3 — Premium Tier Distorting Fairness  
Clause: Shared model and telemetry  
Control: Feature flags  
Test: `test_premium_uses_same_fraud_model`, `test_premium_collects_same_telemetry_fields`

### Risk 4 — Surveillance Drift  
Clause: 30 day raw retention  
Control: S3 lifecycle rules  
Test: `test_raw_fraud_logs_deleted_within_30_days`

### Risk 5 — Cascading Regional Outages  
Clause: Region isolation  
Control: Region specific queues  
Test: `test_multi_az_deployment_active`, `test_graceful_degradation_order`

## 11. Clause → Control → Test Summary

| Promise | Clause | Control | Test |
|---------|--------|----------|------|
| No PAN/CVV | Ingestion rejects sensitive fields | Schema validation | `test_pan_never_logged`, `test_cvv_never_logged` |
| 30 day retention | Raw logs deleted in 30 days | Lifecycle policies | `test_raw_fraud_logs_deleted_within_30_days` |
| Region isolation | Data stays in region | DNS + IAM boundaries | `test_canadian_logs_stay_in_ca_central_1`, `test_indian_logs_stay_in_approved_region` |
| Premium fairness | Identical telemetry + model | Feature flags | `test_premium_uses_same_fraud_model`, `test_premium_collects_same_telemetry_fields`, `test_retention_windows_identical` |
| Premium overload guardrail | Premium cannot push standard behind baseline | Alert queue routing | `test_premium_overload_does_not_push_standard_behind_baseline` |

## 12. Human Review Notes

Pending review from:
• Privacy Steward  
• Engineering Leads (Data Platform + Ingestion)  
• Security Reviewer  
• Product Owner (Monetization)

Items to validate before sign-off:
• Confirm merchant consent UX flow  
• Confirm retention lifecycle policy paths in S3 and log sinks  
• Confirm telemetry fields used in premium latency measurement  
• Confirm anonymization transformations (hash dropping, amount bucketing, region aggregation)  
• Confirm region isolation is enforced at IAM + DNS layers  
• Confirm premium telemetry does not introduce new identifiers

## 13. Changelog

2025-11-20 — Version 1.2  
Aligned test references with actual repository test names.  
Removed references to non-existent tests and replaced them with correct equivalents.  
Clarified residency tests under Risk 1, premium fairness tests under Risk 3, and overload guardrail tests under Risk 5.  
Added explicit statements confirming 30-day raw log retention, identical premium/standard retention, and limited use of hashed device fingerprints.  
Strengthened explanation of premium telemetry limits and fairness guarantees.  
Added surveillance-recourse language in Section 4.3.

2025-11-17 — Version 1.1  
Initial publication aligned with Terms of Service version 1.3.  
Added telemetry definitions, retention windows, and anonymization thresholds.  
Added merchant responsibilities and cardholder rights.  
Included fairness guarantee for premium tier.

2025-11-17 — Version 1.0  
Initial internal draft prior to architectural alignment.