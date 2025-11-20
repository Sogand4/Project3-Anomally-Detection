# Premium Alert Monetization Plan

<!--Use this file to spell out the details for the "premium alerts" monetization event referenced in `project3.yaml`. Replace the sections below with your own data when you define your real monetization strategy.

## Summary
- Offering: Premium anomaly alerts with a 5-minute response backed by on-call rotation.
- Customer segment: e.g., enterprise merchants with high fraud risk.

## Pricing & Viability
- Proposed pricing: e.g., $50/user/month with a minimum of 25 seats.
- Expected monthly units/revenue.
- Sensitivity analysis (what happens if usage drops 30%?).

## Policy & Guardrails
- Link to relevant ToS/Privacy clauses.
- DNS/log/data policies touched by this revenue stream.
- Ethics debt items triggered by this event.

## Acceptance Test
- Reference the failing red-bar test that enforces this monetization promise (the same path used in `project3.yaml`).

## Evidence / Research Notes
- Any supporting research, customer interviews, or cost breakdowns that justify the numbers above.

-->

## Summary

- **Offering:** Premium fraud alerts that deliver within a tighter window (for example within 10 seconds end to end in normal conditions) and drive faster dashboard refreshes for manual review teams.  
- **What changes:** Alert delivery speed and dashboard freshness for premium merchants.  
- **What does not change:** Fraud model, detection logic, telemetry fields collected, data residency rules, and log retention windows.  
- **Customer segment:** Medium to large merchants in Canada and India with higher transaction volume and fraud exposure who want fresher signals for their risk analysts.

## Pricing and Viability

**Pricing model**

- Flat price of **\$20 per merchant per month** for the starter premium tier.  
- No per seat complexity for this assignment; each merchant counts as a unit.

**Expected units and revenue**

- Expected premium merchants in month one: **80–120**  

Revenue cases:

- Low: 80 × \$20 = **\$1,600 per month**  
- Mid: 100 × \$20 = **\$2,000 per month**  
- High: 120 × \$20 = **\$2,400 per month**

**Sensitivity analysis (usage drops 30 percent)**

- Applied to the low end of the expected merchant range: 56 premium merchants × \$20 = **\$1,120 per month**  

Even with a 30 percent adoption drop, premium revenue still covers the marginal overhead for faster alert queues, priority routing, and the small increase in monitoring needed to support the add-on.

## Policy and Guardrails

TODO

### ToS and Privacy Clauses

- ToS excerpt should promise:
  - that premium alerts target a clear delivery window (for example within 10 seconds end to end under normal conditions)  
  - that service may degrade gracefully by pausing premium extras before impacting core fraud scoring  

- Privacy addendum should state:
  - that premium merchants send the **same fraud telemetry** as standard merchants  
  - that raw logs are retained for **30 days** and anonymized aggregates for about **one year**, regardless of tier  
  - that the fraud model and feature set are shared across tiers to support fairness

### DNS, Logging, and Data Policies

- **DNS policy**
  - premium webhook endpoints and dashboards are region locked  
  - Canadian merchants route to ca central 1 only  
  - Indian merchants route to an India aligned region only  
  - failover never sends CA traffic to IN or vice versa  

- **Log retention policy**
  - no extension of the 30 day raw log window for premium merchants  
  - no special “premium analytics” bucket that keeps identifiable data longer  

- **Data handling policy**
  - PAN and CVV never stored or logged  
  - tokenised identifiers used for all merchants  
  - premium tier does not unlock extra feature fields beyond what standard merchants send

### Ethics Debt Items

- **Risk:** premium tier could pressure the team to store more history or collect more identifiers for “better analytics.”  
- **Guardrail:** retention limits and no extra fields are codified in log and data policies and enforced by tests.  
- **Ledger:** record this as a monetization driven risk in `docs/ethics_debt_ledger.md` with an owner and a planned review cadence.

## Acceptance Test

- **Red bar test that enforces this monetization promise:**  
  `tests/redbar/test_monetization_guardrail.py::test_premium_overload_does_not_push_standard_behind_baseline`

Test intent:

Verify that when Premium alert volume increases, Standard-tier alerts are not delayed beyond their baseline delivery window. Premium may receive faster delivery, but it cannot starve or degrade service for non-paying merchants. This enforces the fairness requirement tied to the Premium monetization event.

## Evidence and Research Notes

- Comparable SaaS products often offer lightweight “speed” or “priority update” add-ons in the **$10–$30 per month** range. These add-ons typically improve delivery speed or refresh frequency without providing dedicated compute or contractual SLA guarantees, which aligns with this Premium tier’s design.

- The adoption estimate of **80–120 merchants** reflects a reasonable early-stage uptake for an opt-in feature in a multi-region e-commerce fraud platform serving Canada and India. The **30 percent sensitivity drop** models common early-market variability in optional add-on engagement.

- Baseline cloud cost reference typical AWS pricing for HTTP API Gateway, stream processing, shared model hosting, and monitoring. Because Premium only adjusts **alert delivery speed** and **dashboard refresh rate**, the marginal cost impact is low and concentrated in:
  - slightly higher queue throughput during bursts  
  - more frequent dashboard updates  
  - small increases in monitoring load  

- The **baseline cost of approximately $1,180 per month** is driven by shared fraud scoring infrastructure used by all merchants. The modest **$20 per month Premium add-on** is therefore viable because it offsets the incremental cost of faster delivery rather than funding the entire platform.
