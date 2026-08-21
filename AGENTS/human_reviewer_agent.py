class HumanReviewerAgent:
    name="human_reviewer"
    def run(self,c:dict)->dict:return {"approved":bool(c.get("human_approved",False)),"diagnostic_authority":False}
