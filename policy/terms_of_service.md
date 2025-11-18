# Terms of Service: Payments Fraud Radar
Effective Date: 2025-11-17  
Version: 1.2

AI Note: Initial draft created November 2025 using Copilot. Simplified and aligned with the risk register, system architecture, and monetization acceptance tests on 2025-11-17.

---

## 1. Service Description
Payments Fraud Radar provides real time fraud scoring for e commerce transactions in two regions:

Canada: ca central 1  
India: ap south 1

All merchants use the same fraud model. Premium tier only changes alert delivery speed and dashboard refresh frequency. Detection logic does not change across tiers.

---

## 2. Service Tiers

### Standard Tier
Alert delivery within 25 seconds  
P99 scoring latency around 3 seconds  
Dashboard refresh every 20 seconds  
Email support within 24 hours

### Premium Tier
Alert delivery within 10 seconds  
P99 scoring latency around 2 seconds  
Dashboard refresh every 5 seconds  
Priority support within 4 hours  
Price: 300 USD per month

Premium features only affect delivery speed, not scoring fairness or model behavior.

---

## 3. Availability and SLO Credits
Standard Tier: 99.9 percent monthly uptime  
Premium Tier: 99.95 percent monthly uptime

Credit schedule for Premium Tier:  
• 10 percent credit when uptime drops below 99.95  
• 25 percent credit when below 99.9  
• 50 percent credit when below 99.0

Requests must be submitted within 30 days.

---

## 4. Data Residency and Retention

### Residency
Canadian merchant data stays in Canada.  
Indian merchant data stays in India.  
No cross border transfers unless required by law.

### Retention
Raw fraud logs deleted after 30 days.  
Anonymized aggregates may be retained up to one year.  
Audit logs retained seven years.

### Sensitive Data
PAN and CVV are never collected.  
Merchants must use tokenized identifiers.

---

## 5. Merchant Responsibilities
Provide accurate transaction metadata.  
Avoid sending PAN, CVV, or other sensitive identifiers.  
Use HTTPS and validate webhook signatures.  
Obtain cardholder consent and forward deletion requests within 14 days.

---

## 6. Graceful Degradation
During overload or partial failure, the system follows this order:
1. Core scoring for all merchants  
2. Standard alert delivery  
3. Premium alert fanout and dashboards  

Premium delivery may pause temporarily to protect scoring quality.

Status updates appear at "https://status.fraudradar.example.com".

---

## 7. Prohibited Uses
No redistribution or resale of scores.  
No reverse engineering of the model.  
No use for unlawful payment processing.  
No synthetic test data in production without approval.

---

## 8. Rate Limits and Safety Guardrails
The service enforces rate limits to maintain stability.  
Abnormal or harmful traffic may be throttled.  
Automated safeguards detect suspicious usage patterns.

---

## 9. Alignment with Identified Risks

### Risk 1 — Data Residency Drift
This ToS commits to strict region locked processing.  
Lifecycle policies and red bar tests enforce this.

### Risk 2 — False Positives Causing Revenue Loss
Scores are advisory. Merchants make final decisions.  
Core scoring receives top priority under load.

### Risk 3 — Premium Tier Distorting Fairness
The fraud model is identical for all merchants.  
Premium tier changes only delivery speed.  
A monetization guardrail acceptance test enforces this.

### Risk 4 — Surveillance Drift
Retention is fixed at 30 days unless the privacy steward approves changes.  
Logs are scrubbed before storage.

### Risk 5 — Cascading Regional Outages
Regions operate independently.  
Alert queues and failover paths are isolated to prevent cross region impact.

---

## 10. Monetization Guardrail
Premium alert delivery must meet the latency rules defined here without adjusting detection logic or model calibration.  
This matches the monetization acceptance test in "project3.yaml".

---

## 11. Liability
The service is not responsible for losses caused by false positives, false negatives, or webhook unavailability.  
Premium tier liability is limited to the last twelve months of subscription fees.

---

## 12. Changes to Terms
Material changes will be communicated at least 60 days in advance.  
Minor updates take effect after 14 days.  
Continued use means acceptance of the updated terms.

---

## 13. Contact
Support: support@fraudradar.example.com  
Premium support: +1 800 FRAUD 24  
Privacy: privacy@fraudradar.example.com  
DPO: dpo@fraudradar.example.com  

---

## 14. Changelog
2025-11-17 — Version 1.2  
Simplified sections not required for rubric. Preserved risk alignment, monetization guardrail, and residency rules.

2025-11-17 — Version 1.1  
Added risk register alignment, rate limits, consent rules, and monetization guardrail.

2025-11-17 — Version 1.0  
Initial publication.

