"""
Red-bar tests for Promise 2: Telemetry Privacy and Data Residency

Clause:
  Canadian fraud telemetry remains in ca-central-1. Indian fraud telemetry remains
  in ap-south-1. PAN and CVV values are never written to any log, and raw fraud
  logs are deleted within 30 days, with only anonymized aggregates retained up
  to one year.

Control:
  Region-locked log sinks, tokenization pipeline that strips PAN/CVV, and S3
  lifecycle rules enforcing 30-day deletion for raw logs.

Enforcement Point:
  S3 bucket configuration, ingestion/tokenization code, and lifecycle policies.

Stakeholders harmed by failure:
  - Canadian and Indian cardholders (privacy violations under PIPEDA/DPDP)
  - Merchants exposed to regulatory penalties and reputation damage
  - Small Indian merchants (empty chair) with least capacity to absorb fines


Replace each test with a failing case that names the harm, stakeholder, and enforcement point.
"""

import pytest


def test_canadian_logs_stay_in_ca_central_1():
    """
    This test enforces the DNS residency rule defined in policy/dns_policy.md.

    Red bar: Canadian fraud logs are not confined to ca-central-1.

    Harm:
      PIPEDA violation exposing Canadian cardholder data to foreign jurisdictions,
      creating liability for merchants and privacy harm for cardholders.

    Enforcement:
      S3 bucket region lock and IAM policies preventing cross-region writes
      for Canadian log sinks.
    """
    pytest.fail(
        "Canadian fraud logs not confined to ca-central-1. "
        "PIPEDA data residency requirement violated."
    )


def test_indian_logs_stay_in_approved_region():
    """
    Red bar: Indian transaction logs are not confined to ap-south-1 or other
    India-approved regions.

    Harm:
      DPDP violation exposing Indian cardholder data to foreign jurisdictions,
      particularly harmful to small Indian merchants (empty chair).

    Enforcement:
      Region-tagged log sinks and IAM policies restricting log writes to
      India-approved regions only.
    """
    pytest.fail(
        "Indian transaction logs not confined to approved regions. "
        "DPDP data residency violated."
    )


def test_raw_fraud_logs_deleted_within_30_days():
    """
    Red bar: S3 lifecycle policy does not automatically delete raw fraud logs
    after 30 days.

    Harm:
      Surveillance drift as detailed transaction data accumulates indefinitely,
      violating purpose limitation and increasing breach impact.

    Enforcement:
      S3 lifecycle rule expiring raw logs after 30 days, with configuration
      tracked in code and reviewed by privacy steward.
    """
    pytest.fail(
        "Raw fraud logs not deleted after 30 days. "
        "Surveillance drift violates retention promise."
    )


def test_pan_never_logged():
    """
    Red bar: Full PAN (Primary Account Number) values appear in processing or
    alert logs.

    Harm:
      PCI-DSS violation creating massive liability for merchants, with breach
      notification costs and fines that hit small merchants hardest.

    Enforcement:
      Tokenization at ingress with automated log scanning to detect PAN-like
      patterns before deployment.
    """
    pytest.fail(
        "PAN values may be logged. "
        "PCI-DSS violation creates existential risk for small merchants."
    )


def test_cvv_never_logged():
    """
    Red bar: CVV (Card Verification Value) codes appear in processing or alert
    logs.

    Harm:
      Severe fraud risk if logs are breached and direct PCI-DSS violation.

    Enforcement:
      Input validation that rejects any CVV fields and guarantees CVV is never
      written to logs or storage.
    """
    pytest.fail(
        "CVV values may be logged. "
        "PCI-DSS violation and severe fraud risk."
    )
