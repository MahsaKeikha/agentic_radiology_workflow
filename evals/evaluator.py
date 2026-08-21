def evaluate(r:dict)->dict:
    required=["worklist_coordinator","metadata_validator","prior_study_locator","reporting_completeness","safety_escalation","human_reviewer"]
    m=[x for x in required if x not in r]
    return {"passed":not m,"missing":m}
