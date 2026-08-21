from dataclasses import dataclass,field
@dataclass
class RunState:
    phase:str="worklist"
    artifacts:dict=field(default_factory=dict)
