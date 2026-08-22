import json
from pathlib import Path

from orchestration.orchestrator import REQUIRED_GATES, evaluate_workflow


def base():
    context = {gate: True for gate in REQUIRED_GATES}
    context.update(
        critical_findings=[],
        high_uncertainty=False,
        unresolved_conflicts=[],
        unresolved_questions=[],
        human_signoff=True,
    )
    return context


SCENARIOS = [
    ("ready", {}, "READY_FOR_QUALIFIED_REVIEW"),
    ("identity_gap", {"patient_identity_verified": False}, "BLOCKED"),
    ("incomplete_acquisition", {"acquisition_complete": False}, "BLOCKED"),
    (
        "critical_unacknowledged",
        {"critical_findings": ["critical"], "critical_result_acknowledged": False},
        "BLOCKED",
    ),
    (
        "uncertain_no_second_read",
        {"high_uncertainty": True, "second_read_complete": False},
        "BLOCKED",
    ),
    ("privacy_gap", {"privacy_controls": False}, "BLOCKED"),
    ("conflict", {"unresolved_conflicts": ["laterality"]}, "BLOCKED"),
    ("missing_signoff", {"human_signoff": False}, "BLOCKED"),
]


def main():
    rows = []
    for name, changes, expected in SCENARIOS:
        context = base()
        context.update(changes)
        actual = evaluate_workflow(context)["status"]
        rows.append(
            {
                "scenario": name,
                "expected": expected,
                "actual": actual,
                "passed": actual == expected,
            }
        )
    passed = sum(row["passed"] for row in rows)
    result = {
        "passed": passed,
        "total": len(rows),
        "pass_rate": passed / len(rows),
        "results": rows,
    }
    Path("heldout-results.json").write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps(result, indent=2))
    raise SystemExit(0 if passed == len(rows) else 1)


if __name__ == "__main__":
    main()
