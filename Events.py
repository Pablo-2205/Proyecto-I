import Resource as resource
import Restrictions as restrictions



class Events:
    def __init__(self , descrpition ,  start , end , resources , clients = 0):
        self.description = descrpition
        self.start = start
        self.end = end
        self.resources = resources
        self.clients = clients

        self.validate()

    def validate(self):
        if(self.end < self.start): raise ValueError


class ReservePS5(Events):
    def validate(self):
        super().validate()
        if(self.start < 8 or self.end > 22): raise ValueError("Las Reservas deben ser entre 8 am y 10 pm")
        self.CoRequisite()

    def CoRequisite(self):
        hasPS5 = any(r.type == "PS5" for r in self.resources)
        hasPS5Controller = any(r.type == "PS5 Controller" for r in self.resources)
        if not hasPS5:
            raise ValueError("La reserva de PS5 requiere una consola PS5")
        
        if not hasPS5Controller:
            raise ValueError("La reserva de PS5 requiere al menos un controlador PS5Controller")

    
class ReservePS4(Events):
    def validate(self):
        super().validate()
        if(self.start < 8 or self.end > 22): raise ValueError("Las Reservas deben ser entre 8 am y 10 pm")

        hasPS4 = any(r.type == "PS4" for r in self.resources)
        hasPS4Controller = any(r.type == "PS4 Controller" for r in self.resources)

        if not hasPS4:
            raise ValueError("La reserva de PS5 requiere una consola PS4")
        
        if not hasPS4Controller:
            raise ValueError("La reserva de PS4 requiere al menos un controlador PS4Controller")
    



class ReserveXbox360(Events):
    def validate(self):
        super().validate()
        if(self.start < 8 or self.end > 22): raise ValueError("Las Reservas deben ser entre 8 am y 10 pm")

class DotaTournament(Events):
    def validate(self):
        super().validate()
        if(self.clients != 16): raise ValueError("Solo puede realizarse si hay 16 personas") 