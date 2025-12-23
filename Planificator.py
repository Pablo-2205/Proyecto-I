class Planificator:

    def __init__(self ):
        self.events = []
        self.resources = []
    
    def AddResource(self , resource):
        self.resources.append(resource)
    
    def AddEvents(self , events):
        self.events.append(events)
    
    def ShowEvents(self):
        for event in self.events:
            print(event)

   