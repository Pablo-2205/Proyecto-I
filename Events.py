import Resource as resource
import Restrictions as restrictions



class Events:
    def __init__(self , descrpition ,  start , end , resources , clients = 0):
        self.description = descrpition
        self.start = start
        self.end = end
        self.resources = resources
        self.clientes = clients

        self.validate()

    def validate(self):
        if(self.end < self.start): raise ValueError
        print("Evento instanciado")

class ReservePS5(Events):
    def validate(self):
        super().validate()
        if(self.start < 8 or self.end > 22): raise ValueError("Las Reservas deben ser entre 8 am y 10 pm")


try:
    e = ReservePS5("Reserva Manana" , 15, 17  , [])
except ValueError as e:
    print("Error:" , e)