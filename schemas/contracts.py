from dataclasses import dataclass,field
@dataclass
class RadiologyContext:
    worklist:list=field(default_factory=list)
    metadata:dict=field(default_factory=dict)
    prior_studies:list=field(default_factory=list)
