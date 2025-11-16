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
- Add first entries to AI collaboration log and ethics debt ledger.

## Iteration 2025-11-15

- Created comprehensive red-bar test suite organized into three files aligned with the three promises.
- Added **test_uptime_reliability.py** with 8 tests for Promise 1 (DNS failover, multi-AZ, health checks, graceful degradation, rate limiting, latency routing, SLO tracking, resource prioritization).
- Added **test_data_residency_privacy.py** with 13 tests for Promise 2 (Canadian/Indian residency, DNS firewall, log retention, PAN/CVV protection, tokenization, region tagging, IAM boundaries, analyst controls).
- Added **test_monetization_fairness.py** with 12 tests for Promise 3 (model parity, telemetry equality, retention matching, delivery speed scope, policy alignment, queue isolation, dashboard parity, webhook fairness, data access limits).
- Each test documents specific harm to stakeholders (including empty chair), enforcement points, and control requirements.
- All tests designed to fail until controls are implemented, following red-bar testing principle.
- Added full monetization plan for Premium Alerts, including revenue projections, policy touchpoints, and Clause→Control→Test linkage; integrated worksheet and created acceptance test reference.

Additional items still needed later:
- Wire red bars into `project3.yaml` (uptime, data residency, monetization).
- Write missing policy files (DNS, log retention, data handling) and draft ToS + Privacy updates.
- Create the monetization worksheet for premium alerts and add the acceptance test path.
- Run validators (`validate_project3_manifest`, `speckit check`) and run `pytest tests/redbar` to confirm all tests fail.