# DNS Policy: Payments Fraud Radar

## 1. Purpose

This DNS Policy defines **resolver locations**, **firewall rules**, and **premium-tier routing behavior** for Payments Fraud Radar.  
It ensures:

- **Data residency protection** (Risk 1 – Residency Drift)  
- **Regional isolation** to prevent cascading outages (Risk 5)  
- **Fair and safe monetization** (premium tier cannot alter privacy or residency rules)  
- Enforcement through **automated DNS configurations** and **red-bar tests** defined in `project3.yaml`

DNS rules directly support the guarantees made in:

- `terms_of_service.md`  
- `privacy_addendum.md`  
- `log_retention_policy.md`

---

## 2. Resolver Architecture

### 2.1 Region-Specific Resolvers
Two resolvers are deployed:

- **ca-central-1-resolver** (Canada)  
- **ap-south-1-resolver** (India)

Each merchant request is routed to the resolver for its region.  
Resolvers **never forward queries across regions**, and recursive resolution is disabled for domains outside the regional allowlist.

### 2.2 Allowed Domains (Per Region)
Each resolver may only resolve:

- Internal fraud scoring endpoints (per-region ALBs)  
- Internal log sink domains (S3, CloudWatch regional endpoints)  
- Outbound webhook domains (merchant-provided, validated via allowlist)  
- Monitoring endpoints (region-specific)

### 2.3 Blocked Domains
Resolvers must reject:

- Any DNS query for non-regional AWS endpoints  
  - Example: CA merchants cannot resolve `*.us-east-1.amazonaws.com`  
- Any domain resolving outside the merchant's region  
- Any attempt to query global analytics services

Queries are blocked at the resolver and logged to DNS firewall logs.

---

## 3. DNS Firewall Rules

### 3.1 Residency Enforcement (Critical)
Rules enforce:

- **Canadian merchant traffic stays inside ca-central-1**  
- **Indian merchant traffic stays inside ap-south-1**  
- No failover across regions  
- No replication to non-approved regions

Blocked categories:

- Cross-region S3 endpoints  
- Cross-region Kinesis/CloudWatch endpoints  
- Global public analytics domains  
- Unapproved external destinations  

### 3.2 Premium-Tier Traffic Treatment
Premium merchants **do not bypass DNS restrictions**.

Premium tier changes **only**:

- Alert delivery queue priority (application layer)  
- Retry behavior and refresh speeds (application layer)

Premium tier **does not**:

- Alter DNS routing  
- Resolve additional domains  
- Gain access to cross-region failover  
- Use global CDNs, accelerators, or VPN-like endpoints

This satisfies the **monetization guardrail**.

---

## 4. Routing Rules

### 4.1 Fraud Scoring API
Requests are routed based on merchant region tag:

- CA merchants → `scoring.ca.central.internal`  
- IN merchants → `scoring.ap.south.internal`

Resolvers reject requests to the wrong scoring region.

### 4.2 Webhook Delivery
Outbound requests resolve through the regional resolver.  
If the webhook domain resolves outside the region:

- The request is blocked  
- Merchant receives a validation error  
- Event recorded in DNS firewall logs  

### 4.3 Regional Isolation (Risk 5 Mitigation)
Resolvers do not allow cross-region DNS fallback.  
During a region outage:

- Scoring remains local  
- No failover to the other region  
- Premium fanout is deprioritized but still region-locked  

---

## 5. Enforcement Automation

### 5.1 Resolver Configuration Checks
Automated CI step validates:

- Allowed domains match allowlist  
- No global endpoints present  
- Per-region resolvers resolve only to region-scoped IP ranges  
- Failover rules are disabled outside the region

### 5.2 Firewall Enforcement
Block/allow decisions are logged to:

- `dns_firewall_ca/` (30-day retention)  
- `dns_firewall_in/` (30-day retention)

TTL settings verified nightly by automated job.

### 5.3 Red-Bar Tests (Required)
- `test_dns_firewall_blocks_us_east_1`  
- `test_residency_enforced`  
- `test_premium_dns_no_privilege_escalation`  
- `test_cross_region_failover_disabled`  

Tests must pass before deployment.

---

## 6. Clause → Control → Test Mapping

| Promise | Clause (Policy) | Control | Test |
|---------|-----------------|---------|------|
| CA/IN residency guaranteed | Queries resolved only in-region | Region-specific resolvers + firewall | `test_residency_enforced` |
| No cross-region log routing | S3/Kinesis endpoints must be regional | Resolver deny rules | `test_dns_firewall_blocks_us_east_1` |
| Premium tier cannot weaken privacy | Premium uses same DNS rules as standard | No premium-only domains/routes | `test_premium_dns_no_privilege_escalation` |
| Outage cannot cascade across regions | No DNS failover to other region | Failover disabled at resolver | `test_cross_region_failover_disabled` |

---

## 7. Change Management

### 7.1 Who Approves DNS Changes
Any change to resolvers, firewall rules, or domain allowlists requires approval from:

- Network Engineering Lead  
- Privacy Steward  
- Compliance Lead  
- SRE Lead (for deployment)

### 7.2 Required Steps for Updates
1. Propose change via pull request in infrastructure repository  
2. Update DNS allowlist/blocklist configuration  
3. Update `dns_policy.md` if any rule or allowlist changes  
4. Add or update red-bar tests  
5. Obtain required approvals (see above)  
6. Deploy via automated pipeline with audit logging enabled  
7. Record change in audit log and ethics debt ledger (if related to fairness or privacy)

### 7.3 Auditing
- All DNS modifications logged to CloudTrail  
- Quarterly review by Compliance  
- Resolver configurations hashed and verified nightly  
- Any drift triggers a P1 incident  

---

## 8. Related Documents

- `privacy_addendum.md` – residency, retention, privacy guarantees  
- `log_retention_policy.md` – residency and TTL enforcement  
- `terms_of_service.md` – merchant promises and monetization guardrail  
- Risk Register (overview.md) – Risks 1 and 5  
- `project3.yaml` – DNS acceptance tests  

---