import pytest

def test_premium_dns_no_privilege_escalation():
    """
    Red bar: Premium-tier merchants resolve DNS differently than standard-tier merchants.

    Harm:
      Premium merchants may receive cross-region DNS routing or global accelerator paths,
      violating data residency (PIPEDA/DPDP) and unfairly disadvantaging standard-tier
      merchants (empty-chair: small Indian merchants). This creates privacy risk,
      jurisdiction leakage, and fairness drift.

    Enforcement:
      Region-locked resolvers (ca-central-1 for Canada, ap-south-1 for India),
      identical DNS allowlists, and no premium-only routing policies.

    Expected Fix:
      Premium and standard tiers must use identical DNS resolvers, identical allowlists,
      and identical failover behavior. Premium acceleration occurs only at the
      application layer, never at the DNS layer.
    """
    pytest.fail(
        "Premium DNS routing differs from standard tier. "
        "Residency and fairness risk: premium may escape region-locked resolvers."
    )
