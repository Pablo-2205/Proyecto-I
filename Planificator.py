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
newPlanification.AddEvents(events.ReservePS5("Pablo" , 8 , 9 , [resource.PS5("PS5" , 1) , resource.PS5Controller("PS5Controller" , 1)]))
newPlanification.AddEvents(events.ReserveXbox360("Reserva Xbox 360 Pedro", 13 , 14 , [resource.Xbox360("Xbox360",1) , resource.Xbox360Controller("Xbox360Controller" , 1)]))
newPlanification.AddEvents(events.FifaTournament("Fifa Torneo Jorge" , 19 , 20 , [resource.PS5Controller("PS5Controller" , 1) , resource.TV("TV" , 1 ) , resource.PS5("PS5" , 1)] , 8))