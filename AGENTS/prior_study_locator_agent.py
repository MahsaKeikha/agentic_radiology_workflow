class PriorStudyLocatorAgent:
    name="prior_study_locator"
    def run(self,c:dict)->dict:return {"prior_studies":c.get("prior_studies",[]),"located":True}
