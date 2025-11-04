#!/usr/bin/env python3
"""
Validate Project 3 manifest files (project3.yaml) for structural integrity.

Usage:
  uv run python projects/analysis/validate_project3_manifest.py --path project3.yaml
  uv run python projects/analysis/validate_project3_manifest.py --path project3.yaml --check-paths

Install PyYAML if required:
  uv pip install pyyaml
"""
from __future__ import annotations

import argparse
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, Iterable, List, Optional

try:
    import yaml  # type: ignore
except ImportError as exc:  # pragma: no cover - handled at runtime
    raise SystemExit(
        "PyYAML is required. Install with `uv pip install pyyaml` and re-run."
    ) from exc


@dataclass
class Issue:
    severity: str  # "ERROR" or "WARN"
    message: str
    location: str

    def __str__(self) -> str:
        return f"[{self.severity}] {self.location}: {self.message}"


def expect_dict(data: Dict[str, Any], key: str, location: str, issues: List[Issue]) -> Dict[str, Any]:
    value = data.get(key)
    if not isinstance(value, dict):
        issues.append(Issue("ERROR", f"Expected `{key}` to be a mapping", location))
        return {}
    return value


def expect_list(data: Dict[str, Any], key: str, location: str, issues: List[Issue]) -> List[Any]:
    value = data.get(key)
    if not isinstance(value, list) or not value:
        issues.append(Issue("ERROR", f"Expected `{key}` to be a non-empty list", location))
        return []
    return value


def expect_str(data: Dict[str, Any], key: str, location: str, issues: List[Issue]) -> Optional[str]:
    value = data.get(key)
    if not isinstance(value, str) or not value.strip():
        issues.append(Issue("ERROR", f"Expected `{key}` to be a non-empty string", location))
        return None
    return value


def validate_paths(paths: Iterable[str], base_dir: Path, location: str, issues: List[Issue]) -> None:
    for path_str in paths:
        try:
            if not path_str:
                raise ValueError("empty path string")
            candidate = (base_dir / Path(path_str)).resolve()
        except Exception as exc:  # pragma: no cover - path parsing issue
            issues.append(Issue("WARN", f"Could not parse path `{path_str}` ({exc})", location))
            continue
        if not candidate.exists():
            issues.append(Issue("WARN", f"Referenced path not found: {path_str}", location))


def validate_manifest(manifest: Dict[str, Any], base_dir: Path, check_paths: bool) -> List[Issue]:
    issues: List[Issue] = []

    project = expect_dict(manifest, "project", "project", issues)
    if project:
        expect_str(project, "title", "project.title", issues)
        expect_str(project, "scenario", "project.scenario", issues)
        team_members = project.get("team_members")
        if not isinstance(team_members, list) or not team_members:
            issues.append(Issue("ERROR", "Expected `team_members` to list at least one member", "project.team_members"))
        else:
            for idx, member in enumerate(team_members):
                loc = f"project.team_members[{idx}]"
                if not isinstance(member, dict):
                    issues.append(Issue("ERROR", "Team member must be a mapping", loc))
                    continue
                expect_str(member, "name", f"{loc}.name", issues)
                expect_str(member, "role", f"{loc}.role", issues)
        if check_paths and "spec_iteration_notes" in project:
            if isinstance(project["spec_iteration_notes"], str):
                validate_paths([project["spec_iteration_notes"]], base_dir, "project.spec_iteration_notes", issues)

    speckit = expect_dict(manifest, "speckit", "speckit", issues)
    if speckit:
        expect_str(speckit, "spec_root", "speckit.spec_root", issues)
        expect_str(speckit, "manifest_version", "speckit.manifest_version", issues)
        expect_str(speckit, "validation_command", "speckit.validation_command", issues)
        expect_str(speckit, "last_validation", "speckit.last_validation", issues)

    cct = expect_dict(manifest, "clause_control_test", "clause_control_test", issues)
    if cct:
        promises = expect_list(cct, "promises", "clause_control_test.promises", issues)
        for idx, item in enumerate(promises):
            loc = f"clause_control_test.promises[{idx}]"
            if not isinstance(item, dict):
                issues.append(Issue("ERROR", "Each promise must be a mapping", loc))
                continue
            expect_str(item, "clause", f"{loc}.clause", issues)
            expect_str(item, "control", f"{loc}.control", issues)
            test_ref = expect_str(item, "test", f"{loc}.test", issues)
            expect_str(item, "enforcement_point", f"{loc}.enforcement_point", issues)
            if check_paths and test_ref:
                # Convert pytest-style references `path::test` into file paths.
                file_part = test_ref.split("::", 1)[0]
                validate_paths([file_part], base_dir, loc, issues)

    monetization = expect_dict(manifest, "monetization", "monetization", issues)
    if monetization:
        events = expect_list(monetization, "events", "monetization.events", issues)
        for idx, event in enumerate(events):
            loc = f"monetization.events[{idx}]"
            if not isinstance(event, dict):
                issues.append(Issue("ERROR", "Each monetization event must be a mapping", loc))
                continue
            expect_str(event, "name", f"{loc}.name", issues)
            expect_str(event, "description", f"{loc}.description", issues)
            revenue = event.get("projected_monthly_revenue")
            if not isinstance(revenue, (int, float)):
                issues.append(Issue("ERROR", "projected_monthly_revenue must be numeric", f"{loc}.projected_monthly_revenue"))
            expect_str(event, "acceptance_test", f"{loc}.acceptance_test", issues)
            if check_paths:
                evidence = event.get("evidence_path")
                if isinstance(evidence, str) and evidence:
                    validate_paths([evidence], base_dir, loc, issues)
        expect_str(monetization, "viability_statement", "monetization.viability_statement", issues)

    policies = expect_dict(manifest, "policies", "policies", issues)
    policy_paths: List[str] = []
    if policies:
        for key in ("tos_path", "privacy_path", "dns_policy_path", "log_policy_path", "data_policy_path"):
            path_value = expect_str(policies, key, f"policies.{key}", issues)
            if path_value:
                policy_paths.append(path_value)

    observability = expect_dict(manifest, "observability", "observability", issues)
    if observability:
        expect_str(observability, "uptime_slo", "observability.uptime_slo", issues)
        latency = observability.get("p95_latency_ms")
        if not isinstance(latency, (int, float)):
            issues.append(Issue("ERROR", "p95_latency_ms must be numeric", "observability.p95_latency_ms"))
        stack = observability.get("monitoring_stack")
        if not isinstance(stack, list) or not stack:
            issues.append(Issue("ERROR", "monitoring_stack must list tools/services", "observability.monitoring_stack"))
        if check_paths:
            chaos_path = observability.get("chaos_experiment_summary")
            if isinstance(chaos_path, str) and chaos_path:
                validate_paths([chaos_path], base_dir, "observability.chaos_experiment_summary", issues)

    ai_usage = expect_dict(manifest, "ai_usage", "ai_usage", issues)
    if ai_usage:
        tools = ai_usage.get("tools")
        if not isinstance(tools, list) or not tools:
            issues.append(Issue("ERROR", "tools must be a non-empty list", "ai_usage.tools"))
        doc_path = expect_str(ai_usage, "documentation_path", "ai_usage.documentation_path", issues)
        expect_str(ai_usage, "review_cadence", "ai_usage.review_cadence", issues)
        if check_paths and doc_path:
            validate_paths([doc_path], base_dir, "ai_usage.documentation_path", issues)

    risks = manifest.get("risks")
    if isinstance(risks, dict):
        ledger = risks.get("ledger_snapshot")
        if ledger and check_paths and isinstance(ledger, str):
            validate_paths([ledger], base_dir, "risks.ledger_snapshot", issues)
        high_risk = risks.get("high_risk_items")
        if isinstance(high_risk, list):
            for idx, item in enumerate(high_risk):
                loc = f"risks.high_risk_items[{idx}]"
                if not isinstance(item, dict):
                    issues.append(Issue("ERROR", "Risk entries must be mappings", loc))
                    continue
                expect_str(item, "description", f"{loc}.description", issues)
                expect_str(item, "mitigation", f"{loc}.mitigation", issues)
                expect_str(item, "associated_test", f"{loc}.associated_test", issues)

    if check_paths and policy_paths:
        validate_paths(policy_paths, base_dir, "policies", issues)

    return issues


def main() -> None:
    parser = argparse.ArgumentParser(description="Validate a Project 3 manifest (YAML).")
    parser.add_argument("--path", required=True, help="Path to project3.yaml")
    parser.add_argument("--check-paths", action="store_true", help="Verify referenced files exist on disk")
    args = parser.parse_args()

    manifest_path = Path(args.path)
    if not manifest_path.exists():
        raise SystemExit(f"{manifest_path} not found.")

    try:
        manifest_data = yaml.safe_load(manifest_path.read_text(encoding="utf-8"))
    except yaml.YAMLError as exc:
        raise SystemExit(f"Failed to parse YAML: {exc}") from exc

    if not isinstance(manifest_data, dict):
        raise SystemExit("Manifest root must be a mapping.")

    base_dir = manifest_path.resolve().parent
    issues = validate_manifest(manifest_data, base_dir, args.check_paths)

    if not issues:
        print("Manifest OK ✓")
        sys.exit(0)

    for issue in issues:
        print(issue)

    error_count = sum(1 for issue in issues if issue.severity == "ERROR")
    warn_count = len(issues) - error_count
    print(f"\nSummary: {error_count} error(s), {warn_count} warning(s).")

    if error_count > 0:
        sys.exit(1)


if __name__ == "__main__":
    main()
