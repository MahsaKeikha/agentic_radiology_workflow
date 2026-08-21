class SafetyEscalationAgent:
    name="safety_escalation"
    def run(self,c:dict)->dict:return {"flags":c.get("safety_flags",[]),"escalate":bool(c.get("safety_flags"))}
