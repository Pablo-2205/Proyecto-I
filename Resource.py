# Resource.py (versión mejorada)
from datetime import datetime, timedelta
import copy

class Resource:
    def __init__(self, type, id):
        self.id = id
        self.type = type
    
    quantity = 0
    bookings = []
    
    @classmethod
    def _time_overlap(cls, start1, end1, start2, end2):
        return not (end1 <= start2 or end2 <= start1)
    
    @classmethod
    def get_available_in_interval(cls, start, end):
        if not hasattr(cls, 'bookings'):
            cls.bookings = []
        
        occupied = 0
        for booking in cls.bookings:
            if cls._time_overlap(booking['start'], booking['end'], start, end):
                occupied += booking['amount']
        
        return cls.quantity - occupied
    
    @classmethod
    def is_available(cls, start, end, amount_needed=1):
        available = cls.get_available_in_interval(start, end)
        return available >= amount_needed
    
    @classmethod
    def book(cls, event_description, start, end, amount=1):
        if not cls.is_available(start, end, amount):
            raise ValueError(f"No hay suficientes {cls.__name__} disponibles de {start} a {end}")
        
        if not hasattr(cls, 'bookings'):
            cls.bookings = []
        
        cls.bookings.append({
            'event': event_description,
            'start': start,
            'end': end,
            'amount': amount
        })
    
    @classmethod
    def release(cls, event_description):
        if not hasattr(cls, 'bookings'):
            cls.bookings = []
        
        cls.bookings = [b for b in cls.bookings 
                       if b['event'] != event_description]
    
    @classmethod
    def get_bookings(cls):
        if not hasattr(cls, 'bookings'):
            cls.bookings = []
        return cls.bookings
    
    @classmethod
    def get_free_intervals(cls, date, start_hour=8, end_hour=22, min_duration_hours=1, max_days=7):
        
        if not hasattr(cls, 'bookings'):
            cls.bookings = []
        
        free_intervals = []
        
        for day_offset in range(max_days):
            current_date = date + timedelta(days=day_offset)
            
            # Crear día completo
            day_start = datetime(current_date.year, current_date.month, current_date.day, start_hour, 0)
            day_end = datetime(current_date.year, current_date.month, current_date.day, end_hour, 0)
            
            # Si el día ya pasó, saltar
            if day_start < datetime.now():
                continue
            
            # Obtengo todas las reservas de este dia 
            day_bookings = []
            for booking in cls.bookings:
                if booking['start'].date() == current_date:
                    day_bookings.append(booking)
            
            # Ordenar reservas por hora de incio 
            day_bookings.sort(key=lambda x: x['start'])
            
            # Encontrar huecos entre reservas
            current_time = day_start
            
            for booking in day_bookings:
                # Si hay espacio antes de esta reserva
                if current_time < booking['start']:
                    gap_duration = (booking['start'] - current_time).total_seconds() / 3600
                    if gap_duration >= min_duration_hours:
                        free_intervals.append((current_time, booking['start']))
                
                # Actualizar current_time al final de esta reserva
                if booking['end'] > current_time:
                    current_time = booking['end']
            
            # Verificar hueco al final del día
            if current_time < day_end:
                gap_duration = (day_end - current_time).total_seconds() / 3600
                if gap_duration >= min_duration_hours:
                    free_intervals.append((current_time, day_end))
        
        return free_intervals
    
    @classmethod
    def get_next_available_slot(cls, duration_hours, date=None, start_hour=8, end_hour=22):
        """
        Encuentra el próximo slot disponible para una duración específica.
        """
        if date is None:
            date = datetime.now().date()
        
        # Buscar en los próximos 7 días
        free_intervals = cls.get_free_intervals(date, start_hour, end_hour, 
                                               min_duration_hours=duration_hours, max_days=7)
        
        for interval_start, interval_end in free_intervals:
            # Verificar si este intervalo puede contener la duración requerida
            available_duration = (interval_end - interval_start).total_seconds() / 3600
            if available_duration >= duration_hours:
                # Retornar el inicio del hueco y el fin (inicio + duración)
                slot_end = interval_start + timedelta(hours=duration_hours)
                return interval_start, slot_end
        
        return None, None

class PS5(Resource):
    quantity = 10
    bookings = []
    
    def __init__(self, type, id):
        super().__init__("PS5", id)

class PS4(Resource):
    quantity = 5
    bookings = []
    
    def __init__(self, type, id):
        super().__init__("PS4", id)

class PS5Controller(Resource):
    quantity = 10
    bookings = []
    
    def __init__(self, type, id):
        super().__init__("PS5Controller", id)

class PS4Controller(Resource):
    quantity = 10
    bookings = []
    
    def __init__(self, type, id):
        super().__init__("PS4Controller", id)

class PC(Resource):
    quantity = 32
    bookings = []
    
    def __init__(self, type, id):
        super().__init__("PC", id)

class Xbox360Controller(Resource):
    quantity = 10
    bookings = []
    
    def __init__(self, type, id):
        super().__init__("Xbox360Controller", id)

class Xbox360(Resource):
    quantity = 5
    bookings = []
    
    def __init__(self, type, id):
        super().__init__("Xbox360", id)

class XboxOne(Resource):
    quantity = 5
    bookings = []
    
    def __init__(self, type, id):
        super().__init__("XboxOne", id)

class XboxOneController(Resource):
    quantity = 10
    bookings = []
    
    def __init__(self, type, id):
        super().__init__("XboxOneController", id)

class TV(Resource):
    quantity = 12
    bookings = []
    
    def __init__(self, type, id):
        super().__init__("TV", id)

class HeadPhones(Resource):
    quantity = 32
    bookings = []
    
    def __init__(self, type, id):
        super().__init__("HeadPhones", id)

class VRGlasses(Resource):
    quantity = 6
    bookings = []
    
    def __init__(self, type, id):
        super().__init__("VRGlasses", id)

