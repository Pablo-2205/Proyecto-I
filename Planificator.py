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
newPlanification.AddEvents(events.ReservePS5("Pablo Rodriguez Reserva" , 8 , 10 , [resource.PS5Controller("PS5Controller" , 1) , resource.PS5("PS5" , 1)]))
newPlanification.AddEvents(events.ReservePS4("Jonathan Pavia Reserva" , 10 , 12 , [resource.PS4("PS4" , 2) , resource.PS4Controller("PS4Controller" , 2)]))
newPlanification.AddEvents(events.CallofDutyTournament("Torneo 1" , 11, 14 , [resource.TV("TV" , 1) , resource.TV("TV" , 2) , resource.TV("TV" , 3) , resource.TV("TV" , 4) , resource.XboxOne("XboxOne" , 1) , resource.XboxOne("XboxOne" , 2) , resource.XboxOne("XboxOne" , 3) , resource.XboxOne("XboxOne" , 4) , resource.XboxOneController("XboxOneController" , 1) , resource.XboxOneController("XboxOneController" , 1) , resource.XboxOneController("XboxOneController" , 1) , resource.XboxOneController("XboxOneController" , 1) , resource.XboxOneController("XboxOneController" , 1)] , 16 , 16))