# Spec Iteration Notes

<!-- Use this file to summarize the major spec revisions you make while iterating with SpecKit. -->

## Iteration 2025-11-14

- Selected **Payments Fraud Radar** as the project scenario due to simpler jurisdictional boundaries (PIPEDA + DPDP) and clear tier-based monetization.
- Created the initial **spec/overview.md** describing the system scenario, stakeholders, telemetry flows, monetization event, and Clause → Control → Test alignment.
- Added detailed **success metrics** with numerical SLOs for both standard and premium tiers, enabling enforceable red-bar tests.
- Defined performance targets:
  - Standard tier: 99.9% uptime, P99 detection ≤ 3s, alert delivery ≤ 25s.
  - Premium tier: 99.95% uptime, P99 detection ≤ 2s, alert delivery ≤ 10s, faster dashboard refresh.
- Drafted the **Architecture Overview** describing edge, ingest, streaming, model service, alerting paths, dashboards, data stores, DNS routing, and control plane.
- Identified and documented primary stakeholders and the empty-chair stakeholder.
- Added a clear **risk and mitigation** section covering residency drift, false positives, fairness across tiers, surveillance drift via retention, and region-level outages.

Additional items still needed later:
- Update `project3.yaml` with the three promises, monetization event, acceptance test paths.
- Fill in DNS, log retention, and data handling policies under `policy/`.
- Add failing red-bar tests referencing the new latency and residency SLOs.
- Add first entries to AI collaboration log and ethics debt ledger.