# F56 Agentic Radiology Workflow

**Maturity:** L3 reference candidate  
**Version:** 1.0.0

A six-agent reference architecture for governed radiology workflow support across worklist coordination, metadata validation, prior-study retrieval, report-completeness review, safety escalation, and qualified human review.

F56 focuses on the operational and information-quality layers surrounding radiology interpretation. It is deliberately non-diagnostic. The system can organize cases, validate metadata, identify potentially relevant prior studies, check whether expected report sections or workflow elements are present, surface operational safety concerns, and route cases for human attention. It does not interpret medical images, generate autonomous diagnoses, replace a radiologist, or authorize clinical action.

## Why radiology workflow needs explicit orchestration

Radiology depends on more than image interpretation. A study can be delayed or made unsafe by incorrect patient or study metadata, missing priors, incomplete worklists, mismatched accession information, unavailable comparison studies, reporting omissions, communication failures, or unrecognized urgent workflow conditions.

F56 models these concerns as separate responsibilities:

```text
incoming study / workflow case
            |
            v
   Worklist Coordinator
            |
            v
    Metadata Validator
            |
            v
   Prior Study Locator
            |
            v
 Reporting Completeness
            |
            v
    Safety Escalation
            |
            v
 Qualified Human Reviewer
```

The architecture keeps operational support distinct from diagnostic interpretation.

## Six-agent architecture

| Agent | Responsibility | Core question |
|---|---|---|
| Worklist Coordinator Agent | Organizes study queues and operational priority signals | Is the case represented in the correct workflow queue with the available operational context? |
| Metadata Validator Agent | Checks study and patient metadata consistency | Are required identifiers and study attributes present and internally consistent? |
| Prior Study Locator Agent | Locates candidate prior examinations and comparison records | Are relevant prior studies available for qualified reviewer consideration? |
| Reporting Completeness Agent | Checks expected reporting and workflow elements | Is the report/workflow package structurally complete without judging the diagnosis itself? |
| Safety Escalation Agent | Detects operational safety conditions requiring escalation | Does this case require immediate or higher-priority human attention? |
| Human Reviewer Agent | Represents the qualified human review boundary | Has an authorized radiology professional reviewed the case where required? |

## Repository structure

```text
AGENTS/
├── worklist_coordinator_agent.py
├── metadata_validator_agent.py
├── prior_study_locator_agent.py
├── reporting_completeness_agent.py
├── safety_escalation_agent.py
└── human_reviewer_agent.py

SKILLS/
├── worklist_coordination.py
├── metadata_validation.py
├── prior_study_review.py
├── report_completeness.py
└── safety_escalation.py

TOOLS/
├── worklist_tool.py
├── metadata_checker.py
├── prior_study_index.py
├── report_completeness_checker.py
└── escalation_router.py

benchmarks/
├── benchmark.py
└── RESULTS.md

evals/
├── evaluator.py
└── heldout_suite.py

orchestration/
memory/
observability/
schemas/
prompts/
config/
safety/
examples/
tests/
docs/
.github/workflows/ci.yml
run.py
pyproject.toml
README.md
```

## Worklist coordination

The Worklist Coordinator Agent supports operational organization of radiology studies. A worklist record can include information such as:

```text
study_id
accession_number
patient_reference
modality
exam_type
site
location
order_time
study_time
workflow_status
operational_priority
assigned_queue
```

Production implementations should derive priority and queue state from authorized hospital and radiology systems rather than inventing urgency from incomplete text.

Useful operational questions include:

- Is the study present in the expected queue?
- Is the modality correct?
- Is the study complete or still acquiring images?
- Is the exam associated with the correct site and service?
- Has the case already been assigned?
- Is a required preliminary or final workflow step outstanding?
- Is there an authorized operational priority flag?

`TOOLS/worklist_tool.py` provides the deterministic reference abstraction for worklist handling.

## Metadata validation

The Metadata Validator Agent checks information quality before downstream workflow support proceeds.

Relevant metadata can include:

- patient identifier
- accession number
- study instance identifier
- modality
- body region
- exam description
- acquisition date/time
- ordering service
- location
- laterality where applicable
- contrast status where applicable
- protocol identifier
- series information

`TOOLS/metadata_checker.py` provides deterministic checks for required fields and consistency.

### Identity safety

Patient and study identity errors can have serious consequences. F56 therefore treats missing or conflicting identifiers as blockers requiring human/system resolution.

The system must not guess a patient identity, merge records because names appear similar, or silently substitute one accession or study for another.

Potential states include:

```text
IDENTITY INCOMPLETE
ACCESSION MISMATCH
STUDY METADATA CONFLICT
MODALITY MISMATCH
REVIEW REQUIRED
```

## Prior-study retrieval

Comparison with prior imaging can be important to qualified interpretation, but prior-study retrieval is an information-retrieval problem, not a diagnostic conclusion.

The Prior Study Locator Agent can search an authorized index using factors such as:

- patient identity
- modality
- body region
- exam type
- date range
- institution
- study availability

`TOOLS/prior_study_index.py` provides the reference lookup layer.

The system should distinguish:

- no prior found
- prior exists but is unavailable
- candidate prior located
- multiple possible priors
- external prior pending import
- identity uncertainty

It must not claim that a prior is clinically relevant merely because metadata appears similar. Final comparison selection remains with the radiologist or authorized clinical workflow.

## Reporting completeness

The Reporting Completeness Agent checks structure and required workflow elements without determining whether the medical interpretation is correct.

Depending on local policy, a completeness check may look for expected sections or metadata such as:

- exam identification
- indication/history field
- technique
- comparison field
- findings section
- impression section
- critical communication documentation where applicable
- author/reviewer status
- report status

`TOOLS/report_completeness_checker.py` provides deterministic support for these checks.

A completeness pass means required structural elements are present. It does not mean the report is diagnostically accurate.

## Safety escalation

The Safety Escalation Agent identifies operational conditions that require prompt human attention.

Examples can include:

- unresolved patient/study identity conflict
- missing study in an expected urgent queue
- critical workflow flag from an authorized source
- report communication requirement not documented
- unexpected delay beyond a configured operational threshold
- failed prior retrieval where a required comparison workflow exists
- system outage affecting radiology operations
- incomplete case state that should not progress automatically

`TOOLS/escalation_router.py` provides the routing abstraction.

Escalation should use configured institutional channels. The system does not independently declare a medical emergency or determine a clinical diagnosis.

## Human review boundary

The Human Reviewer Agent represents a hard authority boundary.

F56 must not autonomously:

- interpret CT, MRI, X-ray, ultrasound, PET, mammography, or other medical images
- generate a final diagnosis
- determine that a finding is benign or malignant
- rule out disease
- prescribe treatment
- change imaging orders
- change contrast administration decisions
- approve radiation exposure
- determine patient disposition
- sign a radiology report
- communicate a diagnostic critical result as if it were a radiologist

Qualified professionals remain responsible for image interpretation, diagnostic conclusions, clinical communication, and patient-care decisions.

## Workflow state and provenance

The `memory/` and orchestration layers preserve state across agents.

Useful workflow state includes:

```text
case_id
study_id
metadata_validation_state
worklist_state
prior_search_state
candidate_priors
report_completeness_state
safety_flags
escalation_state
human_review_state
unresolved_questions
```

Production implementations should retain provenance for each field, including the source system, timestamp, version, and retrieval context where applicable.

A previous workflow result should not silently overwrite newer PACS/RIS/EHR information.

## DICOM, PACS, RIS, and EHR integration

F56 is intentionally platform-neutral, but production radiology workflows commonly interact with:

- DICOM systems
- PACS
- RIS
- EHR/EMR systems
- modality worklists
- vendor-neutral archives
- image exchange platforms
- reporting systems
- scheduling systems
- notification systems

Integration layers should preserve patient identity, accession identifiers, study/series identifiers, timestamps, provenance, access controls, and audit records.

A production adapter should validate source-system responses rather than assuming every returned record is current or complete.

## Privacy and access control

Radiology data can contain protected health information and sensitive images.

Production deployments should apply:

- authenticated user/service identity
- role-based or attribute-based access
- least privilege
- minimum-necessary access
- encryption in transit
- encryption at rest where required
- audit logging
- session controls
- retention policies
- secure export controls
- appropriate controls for external image exchange

The reference repository should be evaluated with synthetic or appropriately governed data.

## Downtime and degraded operation

Radiology workflows should define behavior when supporting systems are unavailable.

Examples include:

- PACS unavailable
- RIS unavailable
- EHR unavailable
- prior-study index unavailable
- reporting system unavailable
- network degradation
- image transfer delay

F56 should surface degraded-state uncertainty rather than presenting stale information as current.

Useful states include:

```text
SOURCE UNAVAILABLE
DATA STALE
PRIOR INDEX UNAVAILABLE
WORKLIST STATE UNKNOWN
MANUAL WORKFLOW REQUIRED
```

Institutional downtime procedures remain authoritative.

## Fail-closed workflow gates

A case should not be represented as operationally complete when required evidence is missing.

Potential blockers include:

- unresolved identity conflict
- missing required metadata
- accession mismatch
- study state unknown
- required prior-study search incomplete
- reporting structure incomplete
- unresolved safety escalation
- stale source data
- unavailable authoritative system
- unresolved workflow conflict
- required human review incomplete

Human review cannot erase an unresolved data-integrity blocker. The underlying issue should be resolved or explicitly handled according to institutional policy.

## End-to-end reference workflow

A typical F56 workflow follows this sequence:

1. Receive an authorized study/workflow case.
2. Confirm study and patient references.
3. Validate required metadata.
4. Determine worklist state using authoritative operational information.
5. Search for candidate prior studies when applicable.
6. Record prior availability and uncertainty.
7. Check report/workflow completeness without judging diagnostic correctness.
8. Detect operational safety or delay conditions.
9. Route escalation through configured channels when required.
10. Preserve evidence and provenance.
11. Require qualified human review for clinical interpretation and final authority.

## Observability

The `observability/` layer supports traceability of the workflow itself.

Useful operational telemetry includes:

- case processing time
- worklist queue age
- metadata validation failures
- accession mismatch count
- prior-search latency
- prior retrieval success/failure
- incomplete-report count
- escalation count
- escalation acknowledgement time
- source-system failures
- stale-data events
- human-review state

These metrics should support operational quality improvement and system reliability. They should not be used as a substitute for clinical quality assessment without appropriate methodology and governance.

## Benchmarks and evaluation

The repository includes:

```text
benchmarks/benchmark.py
benchmarks/RESULTS.md
evals/evaluator.py
evals/heldout_suite.py
```

Evaluation should test workflow safety and information integrity rather than diagnostic performance, because F56 is non-diagnostic.

Useful evaluation dimensions include:

- missing-metadata detection
- identity-conflict detection
- accession-mismatch detection
- worklist-state handling
- prior-study retrieval behavior
- no-prior handling
- unavailable-prior handling
- report-completeness detection
- stale-data handling
- source-outage handling
- escalation routing
- unresolved-state propagation
- human-review enforcement

Strong held-out cases should include incomplete metadata, conflicting identifiers, unavailable priors, stale source data, missing report elements, and operational escalation conditions.

## Reproduce the reference implementation

Install development dependencies:

```bash
python -m pip install -e '.[dev]'
```

Run checks and tests:

```bash
ruff check .
pytest -q
```

Run held-out evaluation:

```bash
python evals/heldout_suite.py
```

Run the example:

```bash
python examples/example_run.py
```

Run the main entry point:

```bash
python run.py
```

The repository includes CI under `.github/workflows/ci.yml`.

## CI and reproducibility

Production-oriented radiology workflow testing should additionally cover:

- DICOM metadata fixtures
- PACS/RIS/EHR adapter contracts
- identifier mismatch cases
- duplicate studies
- missing series
- late-arriving images
- external prior import
- stale-cache behavior
- system outage behavior
- escalation-channel failures
- access-control tests
- audit-log integrity

Version workflow policies, schemas, adapters, prompts, test fixtures, and benchmark cases so behavior can be reproduced after changes.

## L3 reference candidate

F56 follows the repository library's L3-oriented structure through specialist agents, deterministic tools, explicit safety boundaries, held-out evaluation, CI, observability, and human review.

This maturity designation describes the engineering structure of the reference repository. It is not FDA clearance or approval, clinical validation, diagnostic certification, hospital credentialing, or evidence that the software can independently interpret medical images.

## Failure states

Useful explicit states include:

```text
PATIENT IDENTITY UNRESOLVED
ACCESSION MISMATCH
METADATA INCOMPLETE
WORKLIST STATE UNKNOWN
PRIOR SEARCH INCOMPLETE
PRIOR UNAVAILABLE
REPORT INCOMPLETE
SOURCE DATA STALE
AUTHORITATIVE SYSTEM UNAVAILABLE
SAFETY ESCALATION REQUIRED
HUMAN REVIEW REQUIRED
```

The system should never fabricate patient identity, prior-study availability, report content, clinical findings, diagnostic conclusions, communication records, or human approval.

## Extending F56

Common extensions include:

- DICOM adapters
- PACS integration
- RIS integration
- EHR integration
- modality worklist integration
- VNA integration
- external image exchange
- structured reporting systems
- speech-recognition workflow integration
- operational dashboards
- queue analytics
- downtime-state detection
- critical-result communication workflow integration
- quality-assurance workflow integration

Extensions should preserve the non-diagnostic boundary unless they are separately developed, validated, regulated, and governed for an intended clinical function.

## Example use cases

F56 can serve as a reference for:

- radiology worklist coordination
- imaging metadata quality checks
- prior-study discovery
- reporting workflow completeness
- operational escalation
- PACS/RIS workflow research
- radiology operations dashboards
- teaching multi-agent healthcare architecture

## Design principles

1. Keep operational workflow support separate from diagnostic interpretation.
2. Never guess patient or study identity.
3. Treat metadata integrity as a safety requirement.
4. Retrieve priors with provenance and uncertainty.
5. Distinguish report completeness from report correctness.
6. Surface stale or unavailable source systems explicitly.
7. Escalate operational safety conditions through authorized channels.
8. Preserve privacy, least privilege, and auditability.
9. Fail closed when required workflow evidence is unresolved.
10. Keep image interpretation and clinical authority with qualified humans.

## Documentation

Additional architecture documentation is available under `docs/`, including `docs/ARCHITECTURE.md`.

## Citation and reuse

Use the repository metadata and citation files provided by the project when referencing this implementation. The code and documentation can be studied and adapted subject to the repository license.

## Responsible use

Use F56 as a radiology workflow and multi-agent systems reference. Validate integrations, identifiers, data freshness, privacy controls, operational policies, escalation procedures, and human-review boundaries against the actual institution before deployment. Final interpretation of medical images and all diagnostic or treatment decisions remain with appropriately qualified healthcare professionals.