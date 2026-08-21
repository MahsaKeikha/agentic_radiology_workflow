class TraceLog:
    def __init__(self):self.events=[]
    def record(self,s,d):self.events.append({"stage":s,"detail":d})
