# Spec Iteration Notes

<!-- Use this file to summarize the major spec revisions you make while iterating with SpecKit. -->

// TODO DUPLICATE THIS TO THE DOCS?


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

Next steps:
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

Next steps:
- Wire red bars into `project3.yaml` (uptime, data residency, monetization).
- Write missing policy files (DNS, log retention, data handling) and draft ToS + Privacy updates.
- Create the monetization worksheet for premium alerts and add the acceptance test path.
- Run validators (`validate_project3_manifest`, `speckit check`) and run `pytest tests/redbar` to confirm all tests fail.

## Iteration 2025-11-16

- Produced first full drafts of all required policy documents:
  - `terms_of_service.md` (simplified, monetization-aligned)
  - `privacy_addendum.md` (complete PIPEDA/DPDP alignment, retention + residency guarantees)
  - `log_retention_policy.md` (full per-source retention rules and enforcement tests)
  - `dns_policy.md` (resolver layout, firewall rules, monetization guardrail)
  - `data_handling.md` (data classification, allowed processing, storage regions, empty-chair protections)

- Ensured consistent residency, retention, and monetization promises across all files  
- Ensured empty-chair stakeholder (small Indian merchants) is supported in the relevant docs  
- Streamlined ToS to focus only on monetization, SLAs, and contractual obligations 
- Added LLM-generation notes and pending human review sections where needed

Next steps:
- Run manifest validation: `uv run python tools/validate_manifest.py --path project3.yaml --check-paths`
- Run red-bar tests to verify they fail appropriately: `uv run pytest tests/redbar --maxfail=1 -v`
- Document planned chaos experiments in experiments/chaos/placeholder.md
- Ethics debt ledger populated
- Update AI collaboration document

## Iteration 2025-11-17

### Red-Bar Test Suite Creation
- Wrote three full red-bar files:
  - `test_uptime_reliability.py` (Promise 1)
  - `test_data_residency_privacy.py` (Promise 2)
  - `test_monetization_guardrail.py` (Promise 3)
- Ensured all tests are **pure red-bar** (using `pytest.fail` only); added example red-bar failing screenshot
- Incorporated empty-chair harm reasoning and clear enforcement points for each clause.
- Added the monetization event acceptance test:  
  - `tests/redbar/test_monetization_guardrail.py::test_retention_windows_identical`
- Created **chaos_experiment_log.md** with four chaos experiments:
  - AZ failure  
  - Premium alert queue overload  
  - Retention misconfiguration  
  - Cross-region export attempt  
- Manifest structure passed: `uv run python tools/validate_manifest.py --path project3.yaml --check-paths`
- Red-bar tests failed as expected: `uv run pytest tests/redbar --maxfail=1 -v`

Next Steps
- Clean up and review all files for consistency

## Iteration 2025-11-18

- Created and integrated the **new red-bar test**:
  - `tests/redbar/test_dns_policy.py::test_premium_dns_no_privilege_escalation`
- Added corresponding ethics debt ledger entry for DNS privilege escalation risk.
- Cleaned and aligned DNS, Data Handling, ToS, and Retention policies so they reference each other consistently.
- Added specific section references (e.g., “see §3.4 of the ToS”, “see §5 of dns_policy.md”) across:
  - `premium_alerts.md`
  - `worksheet.md`
  - `dns_policy.md`
  - `data_handling_policy.md`
- Verified internal consistency: retention windows, regional boundaries, telemetry parity, and monetization guardrails now match across all documents.
- Updated the Reliability Packet with:
  - Clause→Control→Test mappings
  - Evidence placeholders  
  - Cross-links to the chaos experiment log and policy files  
- Cleaned the chaos experiment file.

### Next Steps
- Add screenshots/log excerpts for each enforcement point to the Reliability Packet:
  - DNS firewall hit  
  - Retention TTL deletion  
  - Export block  
  - Premium pause alert
- Prepare final README pointers (policy section, chaos logs, reliability packet)

## Iteration 2025-11-19

### Updates Completed
- Expanded **premium_alerts.md** with:
  - Policy & Guardrails section fully completed  
  - Cross-references to ToS, Privacy Addendum, DNS, Log Retention, and Data Handling  
  - Ethics debt ledger hooks and enforcement tests  
- Added detailed **Planned Fix** column to every row in `ethics_debt_ledger.md`
- Updated Reliability Packet:
  - Added missing “comms template” explanation  
  - Added more explicit monetization alert thresholds  
  - Added cross-links to policies and tests  
  - Added note that the Runbook is validated by red-bar test