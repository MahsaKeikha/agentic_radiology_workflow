from AGENTS.worklist_coordinator_agent import WorklistCoordinatorAgent
from AGENTS.metadata_validator_agent import MetadataValidatorAgent
from AGENTS.prior_study_locator_agent import PriorStudyLocatorAgent
from AGENTS.reporting_completeness_agent import ReportingCompletenessAgent
from AGENTS.safety_escalation_agent import SafetyEscalationAgent
from AGENTS.human_reviewer_agent import HumanReviewerAgent

def run_workflow(c:dict)->dict:
    agents=[WorklistCoordinatorAgent(),MetadataValidatorAgent(),PriorStudyLocatorAgent(),ReportingCompletenessAgent(),SafetyEscalationAgent(),HumanReviewerAgent()]
    return {a.name:a.run(c) for a in agents}
