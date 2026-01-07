import Resource as resource
import Events as events
import Restrictions as restrictions

class Planificator:

    def __init__(self ):
        self.events = []
        self.resources = []
        self.tags = []
    
    def AddResource(self , resource):
        self.resources.append(resource)
    

    def AddEvents(self , newevent):
        IsIncompatible = restrictions.IsIncompatible( newevent , self.events)
        if not (IsIncompatible): 
            self.events.append(newevent)
            self.tags.append(newevent.description)
        print(self.tags)
    
    





newPlanification = Planificator()
newPlanification.AddEvents(events.ReservePS5("Pablo Rodriguez Reserva" , 8 , 10 , [resource.PS5Controller("PS5 Controller" , 1) , resource.PS5("PS5" , 1)]))