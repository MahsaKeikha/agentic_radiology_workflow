# Agentic Radiology Workflow

F56 standalone multi-agent radiology workflow support system.

## Agents

- [`worklist_coordinator_agent.py`](AGENTS/worklist_coordinator_agent.py)
- [`metadata_validator_agent.py`](AGENTS/metadata_validator_agent.py)
- [`prior_study_locator_agent.py`](AGENTS/prior_study_locator_agent.py)
- [`reporting_completeness_agent.py`](AGENTS/reporting_completeness_agent.py)
- [`safety_escalation_agent.py`](AGENTS/safety_escalation_agent.py)
- [`human_reviewer_agent.py`](AGENTS/human_reviewer_agent.py)

## Tools

- [`worklist_tool.py`](TOOLS/worklist_tool.py)
- [`metadata_checker.py`](TOOLS/metadata_checker.py)
- [`prior_study_index.py`](TOOLS/prior_study_index.py)
- [`report_completeness_checker.py`](TOOLS/report_completeness_checker.py)
- [`escalation_router.py`](TOOLS/escalation_router.py)

## Skills

- [`worklist_coordination.py`](SKILLS/worklist_coordination.py)
- [`metadata_validation.py`](SKILLS/metadata_validation.py)
- [`prior_study_review.py`](SKILLS/prior_study_review.py)
- [`report_completeness.py`](SKILLS/report_completeness.py)
- [`safety_escalation.py`](SKILLS/safety_escalation.py)

Supporting layers include orchestration, memory, state, schemas, prompts, config, safety, observability, evals, benchmarks, examples, tests, docs, and CI.

This system is non-diagnostic and requires qualified human review.
