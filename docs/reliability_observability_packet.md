# Project 3 Reliability and Observability Packet

This packet summarizes how the system meets the 99.9 percent uptime requirement, how chaos experiments validate graceful degradation and fairness guarantees, and how controls and tests enforce data residency, privacy, and monetization guardrails. It links directly to the Project 3 design which includes core fraud scoring, premium alert fanout, streaming ingestion, and region scoped data handling for Canada and India.

---

## 1. Uptime Budget and Dependency Tree

Target SLO: 99.9 percent monthly availability.  
This allows about 43 minutes of downtime per month.

### Dependency Table

| Component | Provider | Individual SLO | Contribution | Mitigation | Cost to Harden |
|----------|----------|----------------|--------------|-----------|----------------|
| API Gateway | AWS API Gateway | 99.95 percent | Entry point for scoring and alerts | Multi AZ, retry policy | Medium |
| Fraud Scoring Service | ECS Fargate or EC2 Auto Scaling | 99.9 percent | Core scoring path | Multi AZ, health checks, circuit breaker | High |
| Alert Fanout Workers | SQS plus worker fleet | 99.9 percent | Premium alerts only | Separate worker pool and caps | Medium |
| Stream Processor | Kinesis or Kafka | 99.9 percent | Processes incoming events | Multi shard, DLQ | High |
| Storage for models | S3 | 99.99 percent | Model files | Versioning, regional bucket | Low |
| Storage for logs | S3 | 99.99 percent | Raw logs (30 days) | TTL deletion, region locked | Low |
| IAM and Auth | AWS IAM | 99.99 percent | Access control | Least privilege policy | Low |
| Observability stack | CloudWatch | 99.9 percent | Metrics, logs, alerts | Cross region backup dashboards | Medium |
| DNS | Route 53 | 100 percent | Global resolution | Health checks | Low |

### Combined Uptime Math

If the core path is:

API Gateway → Fraud Scoring → Storage → Observability

Approximate combined availability:

0.9995 × 0.999 × 0.9999 × 0.999 ≈ 0.9973  
This is lower than the target, so mitigation is necessary.

### Hardening Strategy

The scoring tier must run across multiple Availability Zones.  
Failover and health checks remove unhealthy hosts within seconds.  
Alert fanout workers are not part of the core path, so they are allowed to degrade.  
This design raises the scoring path to sustained 99.9 percent availability.

---

## 2. Chaos Experiment Summary

All chaos experiments are logged under `experiments/chaos/2025-11-17.md` and referenced from `project3.yaml` under `observability.chaos_experiment_summary`.

| Date | Fault Injected | Hypothesis | Observed | Follow-up |
|------|----------------|-----------|----------|-----------|
| 2025-11-17 | One AZ outage in ca-central-1 during peak load | Scoring remains up, premium alerts degrade first | Latency spike. Premium queue backed up | Add circuit breaker, health check removal |
| 2025-11-17 | Premium alert queue overload | Scoring stays within SLO. Premium stops first | Premium workers consumed too much CPU. Standard alerts delayed | Split worker pools, cap premium workers |
| 2025-11-17 | Log retention misconfiguration attempt | Retention extension should be blocked | No guardrail present | Add red bar test, retention policy as code |
| 2025-11-17 | Cross region export attempt | Analyst cannot export Canadian data to USA | Over-permission risk | Tighten IAM, add export red bar tests |

---

## 3. Premium Incident Runbook Snippet

### Trigger

Premium alert P99 latency exceeds threshold or error budget burn indicates overload.

### Roles

On call engineer for scoring.  
On call engineer for alert fanout.  
Privacy steward for any data movement review.

### Steps

1. Verify that scoring latency remains inside SLO.  
2. Check worker saturation for the premium queue.  
3. If scoring is near its limit, immediately pause premium fanout.  
4. Drain backlog or shift to a safe minimum.  
5. Communicate to premium customers that alerts are delayed but scoring is healthy.  
6. Provide estimated recovery time.

### Customer Communication Template

Hello,  
We are observing high load on the premium alert channel. Core fraud scoring remains fully available. Premium alert delivery may be slower while we rebalance the system. We will notify you once normal operation resumes.

### Red Bar Test

`tests/redbar/test_monetization_guardrail.py::test_graceful_premium_pause_exists`

---

## 4. Metrics and Alert Plan

| Metric | Threshold | Collection | Alert Destination | Monetization Tie |
|--------|-----------|-----------|-------------------|------------------|
| P95 scoring latency | 250 ms | CloudWatch | PagerDuty | Ensures fair scoring for standard tier |
| P99 scoring latency | 400 ms | CloudWatch | PagerDuty | Empty chair protection |
| Premium alert latency | 2 minutes | CloudWatch | Slack and PagerDuty | Detects overload early |
| Error budget burn rate | 10 percent per hour | CloudWatch | PagerDuty | Protects core uptime |
| DNS region violations | Any | Route 53 logs | Slack | Residency guardrail |
| Raw log retention TTL | 30 days | S3 lifecycle logs | GitHub Actions report | Privacy guardrail |
| Attempted export across regions | Any | CloudTrail | Slack | Residency enforcement |
| Queue depth premium | Exceeds cap | CloudWatch | Slack | Premium is allowed to pause |

---

## 5. Enforcement Evidence

Each enforcement point is supported by a test, policy, or log excerpt stored in the repo.

### DNS Firewall Hits

Route 53 logs show blocked attempts to reach buckets outside the allowed region.  
Mapped to Clause to Control to Test under data residency.

### Retention TTL

S3 lifecycle transition logs prove that raw logs are deleted after 30 days.  
Mapped to privacy commitments in the Privacy Addendum.

### Cross Region Export Block

CloudTrail event shows access denied for a write attempt to us-east-1.  
Mapped to residency clause in the ToS.

### Monetization Guardrails

Alert worker cap log plus the metric alert shows premium fanout paused before any scoring degradation.  
Mapped to monetization guardrail stating that premium can never impact detection quality for standard merchants.

---