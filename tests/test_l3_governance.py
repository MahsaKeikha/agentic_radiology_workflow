from orchestration.orchestrator import REQUIRED_GATES, evaluate_workflow


def ready_context():
    context = {gate: True for gate in REQUIRED_GATES}
    context.update(
        critical_findings=[],
        high_uncertainty=False,
        unresolved_conflicts=[],
        unresolved_questions=[],
        human_signoff=True,
    )
    return context


def test_ready_workflow_requires_qualified_signoff():
    result = evaluate_workflow(ready_context())
    assert result["status"] == "READY_FOR_QUALIFIED_REVIEW"
    assert result["autonomous_diagnosis"] is False


def test_each_required_gate_fails_closed():
    for gate in REQUIRED_GATES:
        context = ready_context()
        context[gate] = False
        result = evaluate_workflow(context)
        assert result["status"] == "BLOCKED", gate


def test_critical_findings_require_acknowledged_escalation():
    context = ready_context()
    context["critical_findings"] = ["critical"]
    context["critical_result_acknowledged"] = False
    result = evaluate_workflow(context)
    assert result["status"] == "BLOCKED"


def test_high_uncertainty_requires_second_read():
    context = ready_context()
    context["high_uncertainty"] = True
    context["second_read_complete"] = False
    assert evaluate_workflow(context)["status"] == "BLOCKED"


def test_signoff_cannot_be_inferred():
    context = ready_context()
    context["human_signoff"] = False
    result = evaluate_workflow(context)
    assert result["status"] == "BLOCKED"
