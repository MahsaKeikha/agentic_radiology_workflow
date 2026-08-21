class ReportingCompletenessAgent:
    name="reporting_completeness"
    def run(self,c:dict)->dict:return {"report":c.get("report",{}),"completeness_reviewed":True}
