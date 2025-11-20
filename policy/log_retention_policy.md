# Log Retention Policy: Payments Fraud Radar

**Version:** 1.0  
**Effective Date:** 2025-11-17  
**Owner:** Data Governance Team  
**Approvers:** Privacy Steward, Compliance Team, SRE Lead

## 1. Purpose

This policy defines log sources, retention periods, access controls, and deletion procedures for the Payments Fraud Radar platform. It ensures compliance with PIPEDA (Canada) and DPDP (India) by minimizing unnecessary data retention while supporting operational needs and fraud investigation.

All retention configurations are enforced via S3 lifecycle policies and validated by red-bar tests.

## 2. Log Classification

### 2.1 Raw Fraud Logs (High Sensitivity)
**Content:**
- Tokenized transaction identifiers (PAN and CVV never logged)
- Merchant ID, transaction amount, currency
- Device fingerprint hash
- Fraud score and model feature vector
- Region tag (CA or IN)
- Timestamp and request ID

**Retention:** **30 days maximum**  
**Storage:**
- Canadian logs: S3 bucket in `ca-central-1` with server-side encryption (SSE-KMS)
- Indian logs: S3 bucket in `ap-south-1` with server-side encryption (SSE-KMS)

**Deletion:**
- S3 lifecycle rule automatically deletes objects > 30 days old
- Deletion logged to CloudTrail for audit trail

### 2.2 Anonymized Aggregate Metrics (Medium Sensitivity)
**Content:**
- Daily/hourly aggregates: transaction count, false positive rate, P95/P99 latency
- Fraud score distributions by region (no merchant-level breakdown)
- Model performance metrics (precision, recall, F1 score)
- No tokenized identifiers or individual transaction details

**Retention:** **1 year maximum**  
**Storage:**
- Time-series database (e.g., CloudWatch Metrics or Prometheus) in respective regions

**Deletion:**
- Automatic TTL-based deletion after 365 days

### 2.3 Application Logs (Low Sensitivity)
**Content:**
- Service health events (startup, shutdown, restarts)
- Error traces without transaction identifiers
- Performance metrics (CPU, memory, network)

**Retention:** **90 days**  
**Storage:**
- CloudWatch Logs in respective regions

**Deletion:**
- CloudWatch log group retention policy set to 90 days

### 2.4 DNS Query Logs (Medium Sensitivity)
**Content:**
- DNS query domain, timestamp, source IP (masked to /24 subnet)
- Firewall block events
- No transaction content

**Retention:** **30 days**  
**Storage:**
- CloudWatch Logs in Route53 Resolver query logging

**Deletion:**
- CloudWatch retention policy set to 30 days

### 2.5 Audit Logs (Regulatory)
**Content:**
- IAM access events (who accessed what data, when)
- Configuration changes (DNS, IAM policies, S3 buckets)
- Break-glass access to sensitive data

**Retention:** **7 years** (PIPEDA and DPDP compliance requirement)  
**Storage:**
- AWS CloudTrail in respective regions with S3 bucket versioning
- Glacier Deep Archive transition after 1 year

**Deletion:**
- Manual deletion after 7 years with compliance team approval

## 3. Access Controls

### 3.1 Raw Fraud Logs
- **Read access:** SRE on-call (break-glass only), fraud investigation team
- **Write access:** Fraud scoring service only (via IAM service role)
- **Export:** Prohibited except for regulatory investigation with Privacy Steward approval

### 3.2 Anonymized Aggregates
- **Read access:** Analytics team, product managers, compliance team
- **Write access:** Automated aggregation pipeline only

### 3.3 Application and DNS Logs
- **Read access:** SRE team, on-call engineers
- **Write access:** Application services via IAM roles

### 3.4 Audit Logs
- **Read access:** Compliance team, security team, Privacy Steward
- **Write access:** Immutable (CloudTrail managed)

## 4. Regional Boundaries

### 4.1 Canadian Logs
- **All log types** for Canadian merchants stored exclusively in `ca-central-1`
- **No replication** to other regions (including cross-region backup)
- **No exports** to analysis tools hosted in non-Canadian regions

### 4.2 Indian Logs
- **All log types** for Indian merchants stored exclusively in `ap-south-1`
- **No replication** to other regions
- **No exports** to analysis tools hosted in non-Indian regions

### 4.3 Control Plane Logs
- Configuration and deployment logs (no transaction data) may be stored in a central region
- Must not contain tokenized identifiers or fraud scores

## 5. Monetization and Premium Tier

### 5.1 Retention Parity
- **Premium merchants** have identical retention windows as standard merchants
- Premium tier does **not** unlock longer retention or special analytics buckets

### 5.2 Dashboard Data Sources
- Standard tier dashboards: read from anonymized aggregates (max 1 year)
- Premium tier dashboards: same data sources, refreshed more frequently
- Neither tier accesses raw fraud logs directly

### 5.3 Enforcement
- Configuration flags enforce retention parity
- Red-bar test: `tests/redbar/test_monetization_guardrail.py::test_retention_windows_identical`

## 6. Automated Enforcement

### 6.1 S3 Lifecycle Policies
Raw fraud log buckets:
```yaml
Rules:
  - ID: delete-after-30-days
    Status: Enabled
    ExpirationInDays: 30
    NoncurrentVersionExpirationInDays: 1
```

### 6.2 CloudWatch Retention
Application and DNS log groups:
```bash
aws logs put-retention-policy \
  --log-group-name /fraud-radar/ca/application \
  --retention-in-days 90
```

### 6.3 Red-Bar Tests
- `tests/redbar/test_data_residency_privacy.py::test_raw_fraud_logs_deleted_within_30_days`
- `tests/redbar/test_monetization_guardrail.py::test_retention_windows_identical`

If any lifecycle policy permits retention beyond the defined limits, the corresponding red-bar test will fail and block deployment until corrected.

## 7. Data Breach Response

### 7.1 Incident Detection
- Unauthorized access to raw fraud logs triggers P1 incident
- CloudTrail monitors S3 GetObject calls from non-approved IAM principals

### 7.2 Immediate Actions
1. Revoke compromised credentials via IAM
2. Enable S3 MFA Delete if not already active
3. Notify Privacy Steward and affected stakeholders
4. Document incident in ethics debt ledger

### 7.3 Post-Incident Review
- Determine scope of exposure (date range, merchant count)
- Required notifications per PIPEDA/DPDP within 72 hours
- Update access controls and re-run red-bar tests

## 8. Cardholder and Merchant Rights

### 8.1 Right to Access
- Cardholders may request copies of their fraud logs within 30-day window
- After 30 days, only anonymized aggregates available
- Response time: 15 business days per PIPEDA

### 8.2 Right to Deletion
- Cardholders may request deletion of their fraud logs
- Deletion executed within 5 business days
- Documented in audit logs

### 8.3 Merchant Data Requests
- Merchants may request their own fraud logs within 30-day window
- Export provided in encrypted format via secure portal
- Does not extend retention beyond 30 days

## 9. Surveillance Risk Mitigation

### 9.1 No Extended Retention
- **Prohibited:** Creating "premium analytics" buckets with longer retention
- **Prohibited:** Retaining raw logs for model retraining beyond 30 days
- Model training uses anonymized feature vectors only

### 9.2 Ethics Debt Entry
- Risk documented: "Pressure to extend retention for monetization or ML improvements"
- Owner: Data Governance Team
- Review cadence: Quarterly

## 10. Clause → Control → Test Mapping

### Promise 2: Data Residency and Privacy
- **Clause:** Raw fraud logs deleted within 30 days, aggregates retained max 1 year
- **Control:** S3 lifecycle policies, CloudWatch retention settings
- **Test:** `tests/redbar/test_data_residency_privacy.py::test_raw_fraud_logs_deleted_within_30_days`
- **Enforcement Point:** S3 bucket lifecycle configuration and CloudWatch log group settings

### Promise 3: Monetization Guardrail
- **Clause:** Premium tier does not extend retention windows
- **Control:** Identical S3 lifecycle rules for standard and premium merchants
- **Test:** `tests/redbar/test_monetization_guardrail.py::test_retention_windows_identical`
- **Enforcement Point:** Feature flag configuration and policy documents

## 11. Change Management

### 11.1 Retention Extension Requests
- Must be approved by Privacy Steward and Compliance Team
- Requires update to PIPEDA/DPDP compliance documentation
- Must pass updated red-bar tests before deployment

### 11.2 Audit Trail
- All retention policy changes committed to Git
- CloudTrail logs all S3 lifecycle policy modifications
- Quarterly review of changes by compliance team

## 12. Related Policies

- `data_handling_policy.md` Defines tokenization and PAN/CVV exclusion
- `dns_policy.md` Ensures logs remain in approved regions
- `privacy_addendum.md` Customer-facing retention commitments
- `terms_of_service.md` Merchant data access and deletion procedures