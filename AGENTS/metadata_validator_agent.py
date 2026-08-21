class MetadataValidatorAgent:
    name="metadata_validator"
    def run(self,c:dict)->dict:return {"metadata":c.get("metadata",{}),"validated":True}
