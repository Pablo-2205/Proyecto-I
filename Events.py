import Resource as resource
import Restrictions as restrictions
from datetime import datetime


class Events:
    def __init__(self , description ,  start_str , end_str ,  clients = 0 , minAge = 0):
        self.description = description
        try:
            self.start = datetime.strptime(start_str, "%Y-%m-%d %H:%M")
            self.end = datetime.strptime(end_str, "%Y-%m-%d %H:%M")
        except ValueError as e:
            raise ValueError(f"Formato de fecha/hora incorrecto. Use: YYYY-MM-DD HH:MM. Error: {e}")
        
        self.clients = clients
        self.minAge = minAge

        self.validate()
    
    def get_duration_inhours(self):
        return (self.end - self.start).total_seconds() / 3600
    
    def get_requiredResources(self):
        return {}

    def validate(self):
        if(self.end < self.start): 
            raise ValueError("Reservacion de Hora incorrecta")
    
    def to_dict(self):
        return {
            "class_name": self.__class__.__name__,  # Guardamos el tipo de evento
            "description": self.description,
            "start": self.start.strftime("%Y-%m-%d %H:%M"),
            "end": self.end.strftime("%Y-%m-%d %H:%M"),
            "clients": self.clients,
            "minAge": self.minAge
        }
    
    @classmethod
    def from_dict(cls, data):
        #Crear un evento desde un diccionario 
        return cls(
            description=data["description"],
            start_str=data["start"],
            end_str=data["end"],
            clients=data["clients"],
            minAge=data.get("minAge", 0)
        )

    def assign_resources(self):
        pass

    def release_resources(self):
        pass


class ReservePS5(Events):
    def get_requiredResources(self):
        return {"PS5" : 1 , "PS5Controller": 2}
    

    def validate(self):
        super().validate()
        start_hour = self.start.hour
        end_hour = self.end.hour
        if(start_hour < 8 or end_hour > 22): 
            raise ValueError("Las Reservas deben ser entre 8 am y 10 pm")
        self.CoRequisite()

    def CoRequisite(self):
        
        if not resource.PS5.is_available(self.start, self.end, amount_needed=1):
            raise ValueError(f"No hay PS5 disponibles de {self.start.strftime('%H:%M')} a {self.end.strftime('%H:%M')}")
        
        if not resource.PS5Controller.is_available(self.start, self.end, amount_needed=2):
            raise ValueError(f"No hay suficientes controles PS5 de {self.start.strftime('%H:%M')} a {self.end.strftime('%H:%M')}")

    def assign_resources(self):
        
        try:
            resource.PS5.book(self.description, self.start, self.end, amount=1)
            resource.PS5Controller.book(self.description, self.start, self.end, amount=2)
        except ValueError as e:
            
            self.release_resources()
            raise e
    
    def release_resources(self):
        
        resource.PS5.release(self.description)
        resource.PS5Controller.release(self.description)

    
class ReservePS4(Events):
    def get_requiredResources(self):
        return {"PS4" : 1 , "PS4Controller" : 2}
    
    def validate(self):
        super().validate()
        start_hour = self.start.hour
        end_hour = self.end.hour
        if(start_hour < 8 or end_hour > 22): 
            raise ValueError("Las Reservas deben ser entre 8 am y 10 pm")
        self.CoRequisite()

    def CoRequisite(self):
        
        if not resource.PS4.is_available(self.start, self.end, amount_needed=1):
            raise ValueError(f"No hay PS4 disponibles de {self.start.strftime('%H:%M')} a {self.end.strftime('%H:%M')}")
        
        if not resource.PS4Controller.is_available(self.start, self.end, amount_needed=1):
            raise ValueError(f"No hay suficientes controles PS4 de {self.start.strftime('%H:%M')} a {self.end.strftime('%H:%M')}")
    
    def assign_resources(self):
        
        try:
            resource.PS4.book(self.description, self.start, self.end, amount=1)
            resource.PS4Controller.book(self.description, self.start, self.end, amount=2)
        except ValueError as e:
            self.release_resources()
            raise e
    
    def release_resources(self):
        
        resource.PS4.release(self.description)
        resource.PS4Controller.release(self.description)



class ReserveXbox360(Events):
    def get_requiredResources(self):
        return {
            "Xbox360": 1,
            "Xbox360Controller": 1
        }

    def validate(self):
        super().validate()
        start_hour = self.start.hour
        end_hour = self.end.hour
        if(start_hour < 8 or end_hour > 22): 
            raise ValueError("Las Reservas deben ser entre 8 am y 10 pm")
        self.CoRequisite()

    def CoRequisite(self):
        
        if not resource.Xbox360.is_available(self.start, self.end, amount_needed=1):
            raise ValueError(f"No hay Xbox360 disponibles de {self.start.strftime('%H:%M')} a {self.end.strftime('%H:%M')}")
        
        if not resource.Xbox360Controller.is_available(self.start, self.end, amount_needed=1):
            raise ValueError(f"No hay suficientes controles Xbox360 de {self.start.strftime('%H:%M')} a {self.end.strftime('%H:%M')}")

    def assign_resources(self):
        
        try:
            resource.Xbox360.book(self.description, self.start, self.end, amount=1)
            resource.Xbox360Controller.book(self.description, self.start, self.end, amount=2)
        except ValueError as e:
            self.release_resources()
            raise e
    
    def release_resources(self):
       
        resource.Xbox360.release(self.description)
        resource.Xbox360Controller.release(self.description)


class DotaTournament(Events):
    def get_required_resources(self):
        return {
            "PC": 16,
            "HeadPhones": 16
        }

    def validate(self):
        super().validate()
        if self.clients != 16: 
            raise ValueError("Solo puede realizarse si hay 16 personas") 
        self.CoRequisite()
    
    def CoRequisite(self):      
        # Verificar disponibilidad para 16 unidades
        if not resource.PC.is_available(self.start, self.end, amount_needed=16):
            raise ValueError(f"No hay 16 PCs disponibles de {self.start.strftime('%H:%M')} a {self.end.strftime('%H:%M')}")
        
        if not resource.HeadPhones.is_available(self.start, self.end, amount_needed=16):
            raise ValueError(f"No hay 16 audífonos disponibles de {self.start.strftime('%H:%M')} a {self.end.strftime('%H:%M')}")
    
    def assign_resources(self):
        """Reserva los recursos para el horario específico"""
        try:
            resource.PC.book(self.description, self.start, self.end, amount=16)
            resource.HeadPhones.book(self.description, self.start, self.end, amount=16)
        except ValueError as e:
            self.release_resources()
            raise e
    
    def release_resources(self):
        """Libera las reservas cuando se elimina el evento"""
        resource.PC.release(self.description)
        resource.HeadPhones.release(self.description)


class FifaTournament(Events):
    def __init__(self, description, start_str, end_str, clients=0, minAge=0):
        if clients < 8:
            raise ValueError("Deben haber mínimo 8 personas")
        super().__init__(description, start_str, end_str, clients)
    
    def get_required_resources(self):
        return {
            "PS5Controller": 2,
            "PS5": 4,
            "TV": 4
        }

    def validate(self):
        super().validate()
        if self.clients < 8: 
            raise ValueError("Requiere al menos 8 clientes")
        self.CoRequisite()
    
    def CoRequisite(self):
       
        if not resource.PS5Controller.is_available(self.start, self.end, amount_needed=2):
            raise ValueError(f"No hay 2 controles PS5 disponibles de {self.start.strftime('%H:%M')} a {self.end.strftime('%H:%M')}")
        
        if not resource.PS5.is_available(self.start, self.end, amount_needed=4):
            raise ValueError(f"No hay 4 PS5 disponibles de {self.start.strftime('%H:%M')} a {self.end.strftime('%H:%M')}")
        
        if not resource.TV.is_available(self.start, self.end, amount_needed=4):
            raise ValueError(f"No hay 4 TVs disponibles de {self.start.strftime('%H:%M')} a {self.end.strftime('%H:%M')}")
    
    def assign_resources(self):
        
        try:
            resource.PS5Controller.book(self.description, self.start, self.end, amount=2)
            resource.PS5.book(self.description, self.start, self.end, amount=4)
            resource.TV.book(self.description, self.start, self.end, amount=4)
        except ValueError as e:
            self.release_resources()
            raise e
    
    def release_resources(self):
        
        resource.PS5Controller.release(self.description)
        resource.PS5.release(self.description)
        resource.TV.release(self.description)
        
        
class CallofDutyTournament(Events):
    def __init__(self, description, start_str, end_str, clients=16, minAge=16):
        self.clients = clients
        self.minAge = minAge
        super().__init__(description, start_str, end_str, clients, minAge)
    
    def get_required_resources(self):
        return {
            "TV": 4,
            "XboxOne": 4,
            "XboxOneController": 16
        }
    
    def validate(self):
        super().validate()
        
        if self.clients < 16:
            raise ValueError("Se necesitan 16 clientes")
        
        if self.minAge < 16:
            raise ValueError("Todos los participantes deben ser mayores de 16 años")
        
        self.CoRequisite()
    
    def CoRequisite(self):
        
        if not resource.TV.is_available(self.start, self.end, amount_needed=4):
            raise ValueError(f"No hay 4 TVs disponibles de {self.start.strftime('%H:%M')} a {self.end.strftime('%H:%M')}")
        
        if not resource.XboxOne.is_available(self.start, self.end, amount_needed=4):
            raise ValueError(f"No hay 4 XboxOne disponibles de {self.start.strftime('%H:%M')} a {self.end.strftime('%H:%M')}")
        
        if not resource.XboxOneController.is_available(self.start, self.end, amount_needed=16):
            raise ValueError(f"No hay 16 controles XboxOne disponibles de {self.start.strftime('%H:%M')} a {self.end.strftime('%H:%M')}")

    def assign_resources(self):
        try:
            resource.TV.book(self.description, self.start, self.end, amount=4)
            resource.XboxOne.book(self.description, self.start, self.end, amount=4)
            resource.XboxOneController.book(self.description, self.start, self.end, amount=16)
        except ValueError as e:
            self.release_resources()
            raise e
    
    def release_resources(self):
        
        resource.TV.release(self.description)
        resource.XboxOne.release(self.description)
        resource.XboxOneController.release(self.description)


class ReserveMovie(Events):
    def __init__(self, description, start_str, end_str, clients=0, minAge=0):
        super().__init__(description, start_str, end_str, clients, minAge)

    def validate(self):
        super().validate()
        self.CoRequisite()

    def get_required_resources(self):
        return {
            "TV": 1
        }
    
    def CoRequisite(self):
        # Verificar disponibilidad EN EL HORARIO ESPECÍFICO
        if not resource.TV.is_available(self.start, self.end, amount_needed=1):
            raise ValueError(f"No hay TVs disponibles de {self.start.strftime('%H:%M')} a {self.end.strftime('%H:%M')}")

    def assign_resources(self):
        """Reserva los recursos para el horario específico"""
        try:
            resource.TV.book(self.description, self.start, self.end, amount=1)
        except ValueError as e:
            self.release_resources()
            raise e
    
    def release_resources(self):
        """Libera las reservas cuando se elimina el evento"""
        resource.TV.release(self.description)


EVENT_CLASSES = {
    "Events": Events,
    "ReservePS5": ReservePS5,
    "ReservePS4": ReservePS4,
    "ReserveXbox360": ReserveXbox360,
    "DotaTournament": DotaTournament,
    "FifaTournament": FifaTournament,
    "CallofDutyTournament": CallofDutyTournament,
    "ReserveMovie": ReserveMovie
}


# metodo dado un diccionario que me devuelva su respectivo evento
def create_event_from_dict(data):
    """Crea una instancia de evento desde un diccionario"""
    class_name = data.get("class_name", "Events")
    
    if class_name not in EVENT_CLASSES:
        print(f"Advertencia: Clase '{class_name}' no encontrada. Usando Events.")
        class_name = "Events"
    
    event_class = EVENT_CLASSES[class_name]
    
    
    return event_class(
        description=data["description"],
        start_str=data["start"],
        end_str=data["end"],
        clients=data.get("clients", 0),
        minAge=data.get("minAge", 0)
    )