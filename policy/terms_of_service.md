# Terms of Service: Payments Fraud Radar

**Effective Date:** 2025-11-17  
**Version:** 1.0

> **AI Generation Note:** Initial draft generated using GitHub Copilot on 2025-11-17. Human review and edits documented below.

---

## 1. Service Description

Payments Fraud Radar ("the Service") provides real-time fraud detection and risk scoring for e-commerce transactions. The Service operates in two jurisdictions:

- **Canada:** Processing in ca-central-1 (Ontario region)
- **India:** Processing in ap-south-1 (Mumbai region)

All merchants receive fraud scoring powered by a shared machine learning model. Premium tier merchants receive enhanced alert delivery speeds and dashboard refresh rates without changes to the underlying fraud detection logic.

---

## 2. Service Tiers

### 2.1 Standard Tier (Default)
- **Fraud Scoring API:** 99.9% monthly uptime commitment
- **P99 Detection Latency:** ≤ 3 seconds from request to score
- **Alert Delivery:** ≤ 25 seconds to merchant webhook or dashboard
- **Webhook Retries:** Up to 2 retries within 60 seconds
- **Dashboard Refresh:** Every 20 seconds
- **Support:** Email support with 24-hour response time

### 2.2 Premium Tier (Paid)
- **Fraud Scoring API:** 99.95% monthly uptime for alert delivery path
- **P99 Detection Latency:** ≤ 2 seconds from request to score
- **Alert Delivery:** ≤ 10 seconds to merchant webhook or dashboard
- **Webhook Retries:** Up to 5 retries within 60 seconds with exponential backoff
- **Dashboard Refresh:** Every 5 seconds
- **Support:** Priority email and phone support with 4-hour response time
- **Pricing:** $300 USD per merchant per month

**Important:** Premium tier does not change fraud detection logic, model features, or data collection practices. Only alert delivery speed and dashboard refresh rates differ.

---

## 3. Service Level Objectives (SLOs)

### 3.1 Uptime Measurement
- **Standard Tier:** 99.9% monthly uptime = max 43 minutes downtime per month
- **Premium Tier:** 99.95% monthly uptime = max 22 minutes downtime per month
- **Measurement:** Availability of the `/v1/fraud-score` API endpoint
- **Exclusions:** Scheduled maintenance (< 4 hours per quarter), merchant webhook unavailability

### 3.2 SLO Credits (Premium Tier Only)
| Monthly Uptime | Service Credit |
|----------------|----------------|
| < 99.95% but ≥ 99.9% | 10% of monthly fee |
| < 99.9% but ≥ 99.0% | 25% of monthly fee |
| < 99.0% | 50% of monthly fee |

**Credit Request:** Merchants must submit credit requests within 30 days of SLO violation via support portal.

---

## 4. Data Residency and Privacy

### 4.1 Regional Processing
- **Canadian merchants:** All transaction data processed and stored exclusively in Canada (ca-central-1)
- **Indian merchants:** All transaction data processed and stored exclusively in India (ap-south-1)
- **No cross-border transfers** of transaction-level data except as required by law

### 4.2 Data Retention
- **Raw fraud logs:** Deleted automatically after 30 days
- **Anonymized aggregates:** Retained up to 1 year for model evaluation and compliance reporting
- **Audit logs:** Retained for 7 years per PIPEDA and DPDP requirements

### 4.3 Sensitive Data Protection
- **PAN (Primary Account Number) and CVV** are never collected or stored by the Service
- Merchants must tokenize card identifiers before sending to the fraud scoring API
- The Service uses tokenized identifiers only; de-tokenization is not available

### 4.4 Privacy Policy
See **Privacy Addendum** (policy/privacy_addendum.md) for detailed data handling practices, cardholder rights, and compliance information.

---

## 5. Merchant Obligations

### 5.1 Data Quality
Merchants must:
- Tokenize all card identifiers before API submission
- Provide accurate transaction metadata (amount, currency, region tag)
- Not send PAN, CVV, or other prohibited data fields

### 5.2 Webhook Security
Merchants must:
- Validate webhook signatures using provided HMAC-SHA256 keys
- Use HTTPS endpoints for webhook delivery (HTTP prohibited)
- Maintain webhook endpoint availability for alert delivery

### 5.3 Compliance
Merchants must:
- Obtain cardholder consent for fraud detection processing
- Honor cardholder data access and deletion requests within required timeframes
- Notify the Service within 24 hours of any suspected data breach

---

## 6. Graceful Degradation

### 6.1 Prioritization Under Load
During partial failures or resource exhaustion, the Service prioritizes:
1. Core fraud scoring for all merchants (standard and premium)
2. Standard tier alert delivery
3. Premium tier alert fanout and dashboard updates

**Premium features may be temporarily suspended to preserve standard tier functionality.**

### 6.2 Merchant Notification
- Real-time status: Available at `https://status.fraudradar.example.com`
- Incident notifications: Email to registered merchant contacts
- SLO impact: Calculated and reported monthly

---

## 7. Prohibited Uses

Merchants may not:
- Resell or redistribute fraud scores to third parties
- Attempt to reverse-engineer the fraud detection model
- Use the Service for unlawful payment processing
- Submit synthetic or test data to production endpoints without prior approval

---

## 8. Termination

### 8.1 Merchant-Initiated
- Standard tier: Cancel anytime via support portal (no refund for partial months)
- Premium tier: Cancel with 30-day notice; prorated refund for unused days

### 8.2 Service-Initiated
The Service may suspend or terminate accounts for:
- Violation of prohibited uses
- Non-payment (premium tier only)
- Repeated submission of prohibited data fields (PAN/CVV)
- Fraudulent or abusive API usage

**Notice:** 15-day written notice except in cases of immediate security risk

---

## 9. Limitation of Liability

### 9.1 Service Liability Cap
The Service's total liability to any merchant is limited to:
- **Standard tier:** $0 (no monetary liability beyond service restoration)
- **Premium tier:** 12 months of fees paid by the merchant

### 9.2 Exclusions
The Service is not liable for:
- False positives or false negatives in fraud detection (scores are advisory only)
- Merchant revenue loss due to blocked transactions
- Downstream impacts of webhook delivery delays
- Force majeure events (natural disasters, ISP failures, AWS region outages)

---

## 10. Modifications to Terms

### 10.1 Notice Period
- Material changes: 60-day advance notice via email
- Non-material changes: Posted to website with 14-day effective date

### 10.2 Continued Use
Continued use of the Service after the effective date constitutes acceptance of modified terms.

---

## 11. Governing Law and Dispute Resolution

### 11.1 Canadian Merchants
- **Governing Law:** Laws of the Province of Ontario, Canada
- **Jurisdiction:** Courts of Ontario
- **Privacy Law:** PIPEDA (Personal Information Protection and Electronic Documents Act)

### 11.2 Indian Merchants
- **Governing Law:** Laws of India
- **Jurisdiction:** Courts of Mumbai, Maharashtra
- **Privacy Law:** DPDP (Digital Personal Data Protection Act)

### 11.3 Dispute Resolution
- Step 1: Good-faith negotiation (30 days)
- Step 2: Mediation (if negotiation fails)
- Step 3: Binding arbitration or litigation

---

## 12. Contact Information

**Support:**
- Email: support@fraudradar.example.com
- Premium Support Phone: +1-800-FRAUD-24 (premium tier only)

**Privacy and Compliance:**
- Privacy Steward: privacy@fraudradar.example.com
- Data Protection Officer: dpo@fraudradar.example.com

**Status Page:**
- https://status.fraudradar.example.com

---

## Human Review Notes

**Edits Made (2025-11-17):**
1. Added explicit SLO credit table for premium tier (generated version had only text description)
2. Clarified that premium features may be suspended under load to protect standard tier
3. Added specific contact information for privacy and compliance teams
4. Updated governing law section to distinguish Canadian vs Indian merchants
5. Emphasized that PAN/CVV prohibition applies to both standard and premium tiers

**Review Cadence:**
- Quarterly review by Legal and Compliance teams
- Triggered review after any SLO violation, data breach, or regulatory change

**Next Review Date:** 2026-02-17
