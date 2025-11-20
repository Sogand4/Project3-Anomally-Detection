# Terms of Service: Payments Fraud Radar
Effective Date: 2025-11-17  
Version: 1.3

> Generated with OpenAI GPT-5.1, 2025-11-17.  
Manual edits applied to align with monetization requirements, system architecture, and policy references.

---

## 1. Service Description
Payments Fraud Radar provides real time fraud scoring for e commerce transactions.  
The service operates in two regions:  
• Canada (ca central 1)  
• India (ap south 1)

All merchants use the same fraud detection model. Premium features only affect alert delivery speed and dashboard refresh rate. Detection logic, data fields, and retention rules remain identical across tiers.

By integrating with the service, merchants consent to the collection of operational telemetry (timestamps, request metadata, region identifiers) used solely for fraud scoring, debugging, and enforcing policy guarantees.

## 2. Service Tiers

### Standard Tier
Alert delivery within 25 seconds  
Dashboard refresh every 20 seconds  
Email support within 24 hours  

### Premium Tier
Alert delivery within 10 seconds  
Dashboard refresh every 5 seconds  
Priority support within 8 hours  
Price: 20 USD per month  

Premium improves delivery speed and dashboard responsiveness only.  
It does not modify scoring latency, detection logic, model behavior, telemetry fields, or data retention rules.

## 3. Availability

The service targets a 99.9% monthly uptime objective for the shared fraud scoring API.

The Premium alert queue targets a 99.95% uptime objective to support faster delivery.
These are operational targets only and do not include contractual credits or penalties.

## 4. Policy References for Data Handling
Core privacy and data retention policies are defined in **privacy_addendum.md**.  
This Terms of Service references those policies without repeating them.

Alert delivery SLAs are supported by:  
• region locked queues  
• DNS routing rules  
• log and data residency controls  

Data retention (30 days for raw logs, one year for anonymized aggregates) and residency requirements apply equally to all merchants and are specified in **privacy_addendum.md**, which defines the exact enforcement mechanisms.

## 5. Merchant Responsibilities
• Provide accurate transaction metadata  
• Tokenize card data before submission  
• Maintain secure webhook endpoints  
• Use HTTPS and validate webhook signatures  
• Follow integration requirements and rate limits  

(Privacy-specific responsibilities such as cardholder consent and deletion forwarding are defined in **privacy_addendum.md**.)

## 6. Graceful Degradation
During overload or partial failure, the system prioritizes:

1. Core fraud scoring  
2. Standard alert delivery  
3. Premium alert fanout and dashboard updates  

Premium delivery may pause temporarily to preserve fairness and scoring quality.

Service status is posted at: https://status.fraudradar.example.com

## 7. Prohibited Uses
Merchants may not:  
• redistribute scores  
• reverse engineer the model  
• use the service for unlawful payment processing  
• submit synthetic or test data to production without approval  

## 8. Rate Limits and Abuse Detection
The service may throttle traffic that exceeds safe operational thresholds.  
Automated safeguards detect harmful ingestion patterns and prevent misuse.

## 9. Monetization Guardrail
Premium alert delivery speed must not weaken:  
• fairness  
• privacy guarantees  
• region residency rules  
• retention rules  
• telemetry schema

The same fraud model and data schema apply to both tiers.  
This guardrail is enforced by a red bar acceptance test defined in `project3.yaml`.

---

Fraud scoring relies on operational telemetry such as timestamps, region identifiers, and retry metadata. This information is used only for scoring, debugging, and enforcing uptime and residency guarantees. The system does not profile individual cardholders or track merchant behavior beyond what is necessary for fraud detection.

Small Indian merchants, who rely heavily on low-latency checkout experiences, are identified as an at-risk stakeholder (“empty chair”). To protect this group, Premium delivery speed cannot degrade Standard-tier performance. Concerns or suspected misuses of telemetry may be reported to privacy@fraudradar.example.com for review.

---


## 10. Liability
The service is not responsible for losses resulting from false positives, false negatives, or webhook unavailability.  
Premium tier liability is limited to the last twelve months of subscription fees.

## 11. Changes to Terms
Material changes will be communicated at least 60 days in advance.  
Minor updates take effect after 14 days.  
Continued use after the effective date constitutes acceptance.

## 12. Contact
Support: support@fraudradar.example.com  
Premium support: +1 800 FRAUD 24  
Policy and privacy inquiries: privacy@fraudradar.example.com  

## 13. Human Review Notes
Pending review from:  
• Engineering (SLA feasibility)  
• Product (monetization configuration)  
• Privacy Steward (policy references)

## 14. Changelog
2025-11-18 — Version 1.4  
Added explicit telemetry consent sentence to the Service Description.  
Introduced Section 9A covering surveillance risk, empty-chair stakeholder protections, and recourse options.  
Clarified availability targets as operational SLOs without contractual credits or penalties.

2025-11-17 — Version 1.3  
Removed duplicate privacy material now covered in privacy_addendum.md.  
Added required LLM generation note and policy references.

2025-11-17 — Version 1.2  
Streamlined non-required legal text. Added monetization guardrail.

2025-11-17 — Version 1.1  
Aligned with risk register and simplified responsibilities.

2025-11-17 — Version 1.0  
Initial publication.