# Project 3 SpecKit Starter

This folder mirrors the repository skeleton we will seed in GitHub Classroom.

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

Replace the placeholder files before submitting. Each directory is pre-created so CI and local tooling should work out of the box.
