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
        if(self.end < self.start): raise ValueError("Reservacion de Hora incorrecta")


class ReservePS5(Events):
    def validate(self):
        super().validate()
        if(self.start < 8 or self.end > 22): raise ValueError("Las Reservas deben ser entre 8 am y 10 pm")
        self.CoRequisite()

    def CoRequisite(self):
        hasPS5 = False
        for r in self.resources:
            if(r.type == "PS5"): 
                hasPS5 = r.quantity > 0
                resource.PS5.quantity -= 1

        hasPS5Controller = False
        for r in self.resources:
            if(r.type == "PS5Controller"):
                hasPS5Controller = r.quantity > 0 
                resource.PS5Controller.quantity -= 1
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
        hasPS4 = False
        hasPS4Controller = False
        for r in self.resources:
            if(r.type == "PS4"): 
                hasPS4 = r.quantity > 0
                resource.PS4.quantity -= 1
            if(r.type == "PS5"):
                hasPS4Controller = r.quantity > 0 
                resource.PS4Controller.quantity -= 1

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
        hasXbox360 = False
        hasXbox360Controller = False
        for r in self.resources:
            if(r.type == "Xbox360"):
                hasXbox360 = r.quantity > 0
                resource.Xbox360.quantity -= 1
            if(r.type == "Xbox360Controller"):
                hasXbox360Controller = r.quantity > 0
                resource.Xbox360Controller.quantity -= 1

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
        pc_count = False
        headphones_count = False
        
        for r in self.resources:
            if r.type == "PC":
                pc_count = r.quantity >= 16
                resource.PC.quantity -= 16
            if r.type == "HeadPhones" :
                headphones_count = r.quantity >= 16
                resource.HeadPhones.quantity -= 16
            
        
        
        if not pc_count :
            raise ValueError("El torneo de Dota requiere al menos 16 PCs")
        
        if not headphones_count:
            raise ValueError("El torneo de Dota requiere al menos 16 audifonos")
        
        

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
        ps_controllers_count = False
        pS_count = False
        Tvs_count = False

        for r in self.resources:
            if(r.type == "PS5Controller"):
                ps_controllers_count = r.quantity >= 2
                resource.PS5Controller.quantity -= 2
            if(r.type == "PS5"):
                pS_count = r.quantity >= 4
                resource.PS5.quantity -= 4            

            if(r.type == "TV"):
                Tvs_count = r.quantity >= 4
                resource.TV.quantity -= 4
        
        if not(ps_controllers_count and pS_count and Tvs_count):
            raise ValueError("Faltan recursos")
        
        
        
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