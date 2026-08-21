def check(report:dict,required:list[str])->dict:return {"missing":[x for x in required if not report.get(x)]}
