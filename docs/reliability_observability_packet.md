# Project 3 Reliability and Observability Packet

This packet explains how Payments Fraud Radar meets the **99.9 percent uptime target**, enforces **data residency and privacy guarantees**, and protects the **empty-chair stakeholder (small Indian merchants)** from monetization side effects.

# 1. Uptime Budget and Dependency Tree

Target monthly SLO: **99.9 percent**, which allows **≈43 minutes of downtime per month**.

## 1.1 Dependency Table

| Component           | Provider               | Individual SLO | Contribution to Path         | Mitigation                             | Cost to Harden |
|--------------------|------------------------|----------------|-------------------------------|-----------------------------------------|----------------|
| API Gateway        | AWS API Gateway        | 99.95 percent  | Ingress for scoring/alerts   | Multi-AZ, retries                       | Medium         |
| Fraud Scoring      | ECS Fargate / EC2 ASG  | 99.9 percent   | Core scoring path            | Multi-AZ, health checks, circuit break  | High           |
| Alert Fanout       | SQS + worker fleet     | 99.9 percent   | Premium only                 | Separate pools, worker caps             | Medium         |
| Stream Processor   | Kafka / Kinesis        | 99.9 percent   | Ingestion                    | Multi shard, DLQ                        | High           |
| Model Storage      | S3                     | 99.99 percent  | Model loading                | Versioning, regional bucket             | Low            |
| Log Storage        | S3                     | 99.99 percent  | 30-day raw + 1-yr aggregates | TTL enforced, region-locked             | Low            |
| Auth / IAM         | AWS IAM                | 99.99 percent  | Access control               | Least privilege                         | Low            |
| Observability      | CloudWatch             | 99.9 percent   | Metrics + Alerts             | Dashboard backups                       | Medium         |
| DNS                | Route 53               | 100 percent    | Region-locked resolution     | DNS firewall rules                      | Low            |

## 1.2 Combined Uptime Math

Core scoring path:

API Gateway → Fraud Scoring → S3 → CloudWatch

Combined availability:

0.9995 × 0.999 × 0.9999 × 0.999 ≈ 0.9973  
This is lower than the target, so mitigation is necessary.

### Hardening Strategy

The scoring tier must run across multiple Availability Zones.  
Failover and health checks remove unhealthy hosts within seconds.  
Alert fanout workers are not part of the core path, so they are allowed to degrade.  
This design raises the scoring path to sustained 99.9 percent availability.

## 1.3 Clause → Control → Test Mapping

| Clause (Policy) | Control (System) | Test (Red-Bar) |
|-----------------|------------------|----------------|
| Scoring must meet 99.9 percent uptime | Multi-AZ, health checks | `tests/redbar/test_uptime_reliability.py::test_multi_az_deployment_active` |
| Premium must not degrade standard tier | Worker caps, separate pools | `tests/redbar/test_monetization_guardrail.py::test_premium_overload_does_not_push_standard_behind_baseline` |
| Residency guaranteed (CA/IN) | Region-locked resolvers | `tests/redbar/test_data_residency_privacy.py::test_indian_logs_stay_in_approved_region` |
| Raw logs must delete after 30 days | S3 TTL lifecycle rules | `tests/redbar/test_data_residency_privacy.py::test_raw_fraud_logs_deleted_within_30_days` |
| Premium DNS cannot bypass residency | Same resolver rules for all tiers | `tests/redbar/test_dns_policy.py::test_premium_dns_no_privilege_escalation` |


## 2. Chaos Experiment Summary

All chaos experiments are logged under `experiments/chaos/2025-11-17.md` and referenced from `project3.yaml` under `observability.chaos_experiment_summary`.

| Date | Fault Injected | Hypothesis | Observed | Follow-up |
|------|----------------|-----------|----------|-----------|
| 2025-11-17 | One AZ outage in ca-central-1 during peak load | Scoring remains up, premium alerts degrade first | Latency spike. Premium queue backed up | Add circuit breaker, health check removal |
| 2025-11-17 | Premium alert queue overload | Scoring stays within SLO. Premium stops first | Premium workers consumed too much CPU. Standard alerts delayed | Split worker pools, cap premium workers |
| 2025-11-17 | Log retention misconfiguration attempt | Retention extension should be blocked | No guardrail present | Add red bar test, retention policy as code |
| 2025-11-17 | Cross region export attempt | Analyst cannot export Canadian data to USA | Over-permission risk | Tighten IAM, add export red bar tests |


## 3. Premium Incident Runbook Snippet

### Trigger  
- Premium alert **P99 > 10 seconds (SLA)**  
- Or **P99 > 120 seconds** operational alert  
- But **scoring still healthy**

### Roles  
- On-call Scoring Engineer  
- On-call Alerts Engineer  
- Privacy Steward  

### Steps  
1. Verify scoring P95/P99 still within SLO.  
2. Inspect premium queue depth.  
3. If depth > cap, **pause premium fanout immediately**.  
4. Drain backlog.  
5. Re-enable at safe concurrency.  
6. Notify customers.

### Customer Communication Template  
> Premium alert delivery is temporarily delayed.  
> Core fraud scoring remains fully available and healthy.  
> We are rebalancing the premium fanout service and will update once resolved.

### Red-Bar Test  
`tests/redbar/test_monetization_guardrail.py::test_graceful_premium_pause_exists`


## 4. Metrics and Alert Plan

| Metric | Threshold | Collection | Destination | Monetization Tie |
|--------|-----------|------------|-------------|------------------|
| P95 scoring latency | 250 ms | CloudWatch | PagerDuty | Protects standard tier |
| P99 scoring latency | 400 ms | CloudWatch | PagerDuty | Empty-chair protection |
| Premium alert latency | SLA: 10 s; Alert if P99 > 120 s | CloudWatch | Slack + PagerDuty | Premium SLA |
| Error budget burn | >10% per hour | CloudWatch | PagerDuty | Protects uptime budget |
| DNS region violations | Any | Route 53 | Slack | Residency guardrail |
| Raw log TTL | Any object >30 days | S3 TTL logs | GitHub Actions | Privacy guardrail |
| Cross-region export attempts | Any | CloudTrail | Slack | Residency enforcement |
| Premium queue depth | cap exceeded | CloudWatch | Slack | Premium pause workflow |

# 5. Enforcement Evidence (Logs)

## 5.1 DNS Firewall Logs  
Evidence for residency enforcement.

```text
2025-11-17T09:15:23Z dns_firewall_ca INFO action=BLOCK
  query_name=s3.us-east-1.amazonaws.com
  src_ip=203.0.113.10
  reason="cross-region endpoint not allowed for CA merchant"
```

Match:
- Clause: “Canadian telemetry must remain in CA.”
- Control: DNS firewall + region-locked resolvers
- Test: test_indian_logs_stay_in_approved_region

## 5.2 S3 TTL (Raw Logs Deleted After 30 Days)
```text
2025-11-17T00:05:01Z s3_lifecycle_ca INFO
  bucket=fraud-rawlogs-ca
  rule_id=delete-after-30-days
  action=EXPIRE
  key=logs/2025/10/17/txn-12345.json
  age_days=31
```

Match:
- Clause: 30-day raw log deletion
- Control: S3 lifecycle rules
- Test: test_raw_fraud_logs_deleted_within_30_days

## 5.3 CloudTrail – Cross-Region Export Blocked
```text
2025-11-17T11:42:10Z cloudtrail WARN
  eventName=PutObject
  userIdentity=arn:aws:iam::123456789012:user/analyst-ca
  requestParameters.bucketName=fraud-exports-us
  errorCode=AccessDenied
  errorMessage="Export to non-Canadian bucket blocked by policy"
```

Match:
- Clause: “No telemetry leaves region except anonymized aggregate.”
- Control: IAM deny + DNS deny
- Test: test_indian_logs_stay_in_approved_region

## 5.4 Monetization Guardrail – Premium Paused Before Harm
```text
2025-11-17T09:43:00Z app INFO
  component=premium_fanout_manager
  event="premium_pause_activated"
  reason="queue_depth_exceeded"
  premium_queue_depth=18500
  standard_queue_depth=230
  scoring_p95_ms=210
  scoring_p99_ms=340

2025-11-17T09:43:02Z alert INFO
  destination=pagerduty
  incident="premium_alert_latency_breach"
  message="Premium alerts paused to protect core scoring SLO"
```

Match:
- Clause: Premium cannot degrade standard tier
- Control: Worker caps, pause workflow
- Tests: test_premium_overload_does_not_push_standard_behind_baseline, test_graceful_premium_pause_exists