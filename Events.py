import Resource as resource
import Restrictions as restrictions



class Events:
    def __init__(self , descrpition ,  start , end , resources , clients = 0 , minAge = 0):
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
        hasPS5Controller = any(r.type == "PS5Controller" for r in self.resources)
        if not hasPS5:
            raise ValueError("La reserva de PS5 requiere una consola PS5")
        
        if not hasPS5Controller:
            raise ValueError("La reserva de PS5 requiere al menos un controlador PS5Controller")

    
class ReservePS4(Events):
    def validate(self):
        super().validate()
        if(self.start < 8 or self.end > 22): raise ValueError("Las Reservas deben ser entre 8 am y 10 pm")
        self.CoRequisite()


    def CoRequisite(self):
        hasPS4 = any(r.type == "PS4" for r in self.resources)
        hasPS4Controller = any(r.type == "PS4Controller" for r in self.resources)

        if not hasPS4:
            raise ValueError("La reserva de PS4 requiere una consola PS4")
        
        if not hasPS4Controller:
            raise ValueError("La reserva de PS4 requiere al menos un controlador PS4Controller")
    



class ReserveXbox360(Events):
    def validate(self):
        super().validate()
        if(self.start < 8 or self.end > 22): raise ValueError("Las Reservas deben ser entre 8 am y 10 pm")
        self.CoRequisite()
    def CoRequisite(self):
        hasXbox360 = any(r.type == "Xbox360" for r in self.resources)
        hasXbox360Controller = any(r.type == "Xbox360Controller" for r in self.resources)

        if not hasXbox360:
            raise ValueError("La reserva de Xbox360 requiere una consola Xbox360")
        
        if not hasXbox360Controller:
            raise ValueError("La reserva de Xbox360 requiere al menos un controlador Xbox360Controller")

class DotaTournament(Events):
    def validate(self):
        super().validate()
        if(self.clients != 16): raise ValueError("Solo puede realizarse si hay 16 personas") 
        self.CoRequisite()
    
    
    def CoRequisite(self):
        total_pc_capacity = 0
        pc_count = 0
        
        for r in self.resources:
            if r.type == "PC":
                pc_count += 1
                total_pc_capacity += getattr(r, 'capacity', 1)
        
        if pc_count == 0:
            raise ValueError("El torneo de Dota requiere al menos una PC")
        
        if total_pc_capacity < 16:
            raise ValueError(f"Se necesitan 16 capacidades de PC (tiene {total_pc_capacity})")
        
        headphone_count = sum(1 for r in self.resources if r.type == "HeadPhones")
        if headphone_count < 16:
            raise ValueError(f"Se necesitan 16 audífonos (tiene {headphone_count})")

class FifaTournament(Events):
    def __init__(self, descrpition, start, end, resources, clients=0, minAge=0):
        if(clients < 8):
            raise ValueError("Deben haber minimo 8 personas")
        super().__init__(descrpition , start , end , resources , clients)

    
    def validate(self):
        super().validate()
        if(self.clients < 8 ): 
            raise ValueError("Requiere al menos 8 clientes")
        self.CoRequisite()
    
    def CoRequisite(self):
        ps_controllers = sum(1 for r in self.resources if r.type in ["PS5Controller", "PS4Controller"])
        if(ps_controllers < 2):
            raise ValueError("Requiere 2 controllers")
        
        hasTv = any(r.type == "TV" for r in self.resources)
        if(not hasTv):
            raise ValueError("Se necesita de una TV")
        
        hasConsole = any(r.type in ["PS5" , "PS4"] for r in self.resources)
        if(not hasConsole):
            raise ValueError("Requiere de una consola")
        
class CallofDutyTournament(Events):
    def __init__(self, descrpition, start, end, resources, clients=16, minAge=16):
        self.clients = clients
        self.minAge = minAge
        super().__init__(descrpition , start , end , resources , clients , minAge)
    
    def validate(self):
        super().validate()
        
        if(self.clients < 16):
            raise ValueError("Se necesitan 16 clientes")
        
        if(self.minAge < 16):
            raise ValueError("Todos los participantes deben ser mayores de 16 años")
        
        self.CoRequisite()
    
    def CoRequisite(self):
        TVcont = 0
        for r in self.resources:
            if(r.type == "TV"): TVcont += 1
        if(TVcont < 4): raise ValueError("Se necesitan 4 TVs")

        XboxOnecont = 0
        for r in self.resources:
            if(r.type == "XboxOne"): XboxOnecont += 1
        if(XboxOnecont < 4): raise ValueError("Se necesitan 4 XboxOne")


        xboxOneController = 0 
        for r in self.resources:
            if(r.type == "XboxOneController"): xboxOneController += 1
        if(xboxOneController < 5): raise ValueError("Se necesitan minimo 16 XboxOneControllers")

class ReserveMovie(Events):
    def __init__(self, descrpition, start, end, resources, clients=0, minAge=0):
        super().__init__(descrpition, start, end, resources, clients, minAge)

    def validate(self):
        super().validate()
        self.CoRequisite()

    def CoRequisite(self):
        hasTV = any(r.type == "TV" for r in self.resources)
        if(not hasTV): raise ValueError("Se necesita de una TV")