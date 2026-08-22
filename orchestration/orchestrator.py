from __future__ import annotations

from typing import Any

REQUIRED_GATES = {
    "patient_identity_verified": "patient identity is not verified",
    "study_metadata_complete": "study metadata is incomplete",
    "acquisition_complete": "required imaging acquisition is incomplete",
    "protocol_review_complete": "imaging protocol review is incomplete",
    "critical_result_path_ready": "critical-result escalation path is not ready",
    "privacy_controls": "privacy controls are incomplete",
    "downtime_plan_ready": "downtime and recovery plan is incomplete",
    "audit_trace_complete": "audit traceability is incomplete",
    "reporting_workflow_ready": "reporting workflow is incomplete",
    "qualified_reviewer_available": "qualified radiology reviewer is unavailable",
}


def evaluate_workflow(context: dict[str, Any]) -> dict[str, Any]:
    blockers = [
        message for gate, message in REQUIRED_GATES.items() if not context.get(gate, False)
    ]
    if context.get("critical_findings") and not context.get("critical_result_acknowledged", False):
        blockers.append("critical result requires documented escalation and acknowledgment")
    if context.get("high_uncertainty") and not context.get("second_read_complete", False):
        blockers.append("high uncertainty requires second-read or overread workflow")
    if context.get("unresolved_conflicts"):
        blockers.append("unresolved imaging or report conflicts remain")
    if context.get("unresolved_questions"):
        blockers.append("unresolved radiology workflow questions remain")
    if context.get("human_signoff") is not True:
        blockers.append("qualified human report sign-off is required")
    return {
        "status": "READY_FOR_QUALIFIED_REVIEW" if not blockers else "BLOCKED",
        "blockers": blockers,
        "human_signoff_required": True,
        "autonomous_diagnosis": False,
        "notes": (
            "Workflow governance only. Diagnostic interpretation and final reporting remain "
            "the responsibility of qualified radiology professionals."
        ),
    }


def run_workflow(context: dict[str, Any]) -> dict[str, Any]:
    return {
        "system_id": "F56",
        "version": "1.0.0",
        "governance": evaluate_workflow(context),
    }
