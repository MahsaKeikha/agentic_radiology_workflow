def check(metadata:dict,required:list[str])->dict:return {"missing":[x for x in required if not metadata.get(x)]}
