import pytest

def test_uptime_placeholder():
    pytest.fail(
        "Red bar: 99.9% uptime and graceful degradation not yet enforced via DNS failover and rate limiting."
    )

def test_canada_log_bucket():
    pytest.fail(
        "Red bar: Canadian fraud logs not yet proven to stay in ca-central-1 with 30-day retention and no PAN/CVV."
    )

def test_monetization_guardrail_placeholder():
    pytest.fail(
        "Red bar: premium alerts not yet proven to keep the same telemetry, retention windows, and model as the standard tier."
    )
