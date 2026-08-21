class WorklistCoordinatorAgent:
    name="worklist_coordinator"
    def run(self,c:dict)->dict:return {"worklist":c.get("worklist",[]),"coordinated":True}
