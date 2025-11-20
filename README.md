# Project 3 SpecKit Starter

SpecKit is the source of truth.  
All changes follow one path: **Spec → Manifest → Policy → Test**.

## Pre-Requisites

This assumes you are using the uv package manager.  If you prefer some other tooling, you should use the techniques there to ensure the required packages are installed (see [pyproject.toml](./pyproject.toml))

The instructions for installing are on the astral website: [Installing uv](https://docs.astral.sh/uv/getting-started/installation/)

## Tools

Key commands (run from repo root):

To validate the repo:

```bash
uv run python tools/validate_manifest.py --path project3.yaml --check-paths
```

To validate the redbar testing:

```bash
uv run pytest tests/redbar --maxfail=1
```

## Repository Map
- **spec/** system overview and iteration notes  
- **project3.yaml** clause, control, test, enforcement mapping  
- **tests/redbar/** failing red-bar tests  
- **policy/, docs/, analysis/** TOS, privacy, DNS, log retention, monetization, ethics ledger  
- **reports/** manifest validation and observability snapshots  
- **experiments/** chaos logs  

## Daily Loop
1. Update spec in spec/.  
2. Add or adjust a red-bar test.  
3. Run tests (uv run pytest tests/redbar --maxfail=1)
4. Update project3.yaml and validate (uv run python tools/validate_manifest.py --path project3.yaml --check-paths > reports/manifest_validation.txt)
5. Commit updated reports and any screenshots.  
6. Keep only artefacts that strengthen spec, manifest, policies, or tests.


## Release Readiness
- Manifest validated and report committed  
- Monetization worksheet completed  
- TOS, Privacy Addendum, DNS and log policies written and referenced  
- Red-bar tests failing as expected  
- Ethics ledger and AI log up to date

## Observability
- See **docs/reliability_observability_snapshot.md** for metrics and logs demonstrating enforcement.  
- See **experiments/chaos/2025-11-17.md** for outlined chaos experiments.

## Tests
- **docs/all_redbar_tests_fail_log.txt** contains log of full failing test output  
- **docs/failing_redbar_test_output.png** provides a screenshot of one failing test  
