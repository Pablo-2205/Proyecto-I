import Resource as resource
import Events as events
from Events import create_event_from_dict
import Restrictions as restrictions
import json
from datetime import datetime, timedelta

class Planificator:

    def __init__(self):
        self.events = []
        self.resources = []
        self.tags = []
    
    def AddResource(self, resource):
        self.resources.append(resource)
    
    def AddEvents(self, newevent):
        if newevent.description in self.tags:
            raise ValueError("Ya existe un evento con esa descripcion")
        for existing_event in self.events:
            if self._events_overlap(newevent, existing_event):
                raise ValueError(f"El evento se solapa con '{existing_event.description}' ({existing_event.start.strftime('%H:%M')}-{existing_event.end.strftime('%H:%M')})")

        newevent.validate()
        try:
            newevent.assign_resources()
        except ValueError as e:
            raise ValueError(f"No se pueden reservar recursos: {e}")
        
        self.events.append(newevent)
        self.tags.append(newevent.description)
        print(f"✓ Evento '{newevent.description}' agregado exitosamente")

    def _events_overlap(self, event1, event2):
        return not (event1.end <= event2.start or event2.end <= event1.start)

    def RemoveEvents(self, tag):
        if tag not in self.tags: 
            raise ValueError("No existe una reserva a ese nombre")
        for event in self.events:
            if tag == event.description:
                try:
                    event.release_resources()
                except AttributeError:
                    print(f"⚠ El evento no tiene método release_resources")
                except Exception as e:
                    print(f"⚠ Error al liberar recursos: {e}")
                
                self.events.remove(event)
                self.tags.remove(tag)
                print(f" Evento '{tag}' eliminado y recursos liberados")
                return
        
        print(f" Error: Evento '{tag}' no encontrado")
    
    def save_to_file(self, filename="data.json"):
        
        try:
            # Convertir todos los eventos a diccionarios
            events_data = [event.to_dict() for event in self.events]
            
            # Crear datos completos
            data = {
                "events": events_data,
                "saved_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }
            
            # Guardar en archivo
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            
            print(f"✓ Datos guardados en '{filename}'")
            print(f"  Eventos guardados: {len(events_data)}")
            
        except Exception as e:
            print(f"✗ Error al guardar: {e}")
    
    def load_from_file(self, filename="data.json"):
        try:
            # Leer archivo
            with open(filename, 'r', encoding='utf-8') as f:
                data = json.load(f)
        
            # Limpiar eventos actuales
            self.events = []
            self.tags = []
        
            # Cargar cada evento
            events_loaded = 0
            for event_data in data.get("events", []):
                try:
                    # Usar la nueva función para crear el evento correcto
                    event = create_event_from_dict(event_data)
                    try:
                        event.assign_resources()
                    except ValueError as e:
                        print(f"No se pudieron reservar recursos para '{event.description}' : {e}")
                        continue
                    # Agregar el evento
                    self.events.append(event)
                    self.tags.append(event.description)
                    events_loaded += 1
                
                except Exception as e:
                    print(f"  ⚠ Error cargando evento '{event_data.get('description', 'Desconocido')}': {e}")
                    continue
        
            print(f"✓ Datos cargados desde '{filename}'")
            print(f"  Eventos cargados: {events_loaded}")
            print(f"  Guardado originalmente: {data.get('saved_at', 'Desconocido')}")
        
        except FileNotFoundError:
            print(f"⚠ Archivo '{filename}' no encontrado. Comenzando con lista vacía.")
        except json.JSONDecodeError:
            print(f"✗ Error: Archivo '{filename}' no tiene formato JSON válido.")
        except Exception as e:
            print(f"✗ Error al cargar: {e}")
    
    def find_available_slot(self, event_type, duration_hours, clients=0, min_age=0, 
                           start_date=None, max_days=7):
        """
        Encuentra el próximo hueco disponible para un tipo de evento.
        """
        if start_date is None:
            start_date = datetime.now().date()
        
        # Obtener recursos requeridos para este tipo de evento
        required_resources = self._get_required_resources_for_event_type(
            event_type, clients, min_age
        )
        
        if not required_resources:
            print("⚠ Este tipo de evento no requiere recursos específicos")
            return None, None
        
        # Mapear nombres de recursos a clases
        resource_classes = {
            "PS5": resource.PS5,
            "PS4": resource.PS4,
            "PS5Controller": resource.PS5Controller,
            "PS4Controller": resource.PS4Controller,
            "Xbox360": resource.Xbox360,
            "Xbox360Controller": resource.Xbox360Controller,
            "XboxOne": resource.XboxOne,
            "XboxOneController": resource.XboxOneController,
            "PC": resource.PC,
            "TV": resource.TV,
            "HeadPhones": resource.HeadPhones,
            "VRGlasses": resource.VRGlasses
        }
        
        # Buscar hueco común para todos los recursos requeridos
        current_date = start_date
        
        for day_offset in range(max_days):
            check_date = current_date + timedelta(days=day_offset)
            
            # Saltar si el día ya pasó
            if check_date < datetime.now().date():
                continue
            
            # Para este día, buscar todos los huecos de cada recurso
            all_free_intervals = {}
            
            for res_name, res_class in resource_classes.items():
                if res_name in required_resources:
                    free_intervals = res_class.get_free_intervals(
                        check_date, 
                        min_duration_hours=duration_hours,
                        max_days=1
                    )
                    all_free_intervals[res_name] = free_intervals
            
            # Buscar intersección de huecos entre todos los recursos
            common_slots = self._find_common_slots(all_free_intervals, duration_hours)
            
            if common_slots:
                # Filtrar huecos que cumplan con horario 8am-10pm
                valid_slots = []
                for slot_start, slot_end in common_slots:
                    if self._is_valid_time_slot(slot_start, slot_end):
                        valid_slots.append((slot_start, slot_end))
                
                if valid_slots:
                    # Retornar el primer hueco válido encontrado
                    slot_start, slot_end = valid_slots[0]
                    return slot_start, slot_end
        
        return None, None
    

    # funcion para por cada tipo de evento devuelva los recursos que necesita
    def _get_required_resources_for_event_type(self, event_type, clients=0, min_age=0):
        
        event_resources = {
            "ReservePS5": {"PS5": 1, "PS5Controller": 2},
            "ReservePS4": {"PS4": 1, "PS4Controller": 1},
            "ReserveXbox360": {"Xbox360": 1, "Xbox360Controller": 1},
            "DotaTournament": {"PC": 16, "HeadPhones": 16},
            "FifaTournament": {"PS5Controller": 2, "PS5": 4, "TV": 4},
            "CallofDutyTournament": {"TV": 4, "XboxOne": 4, "XboxOneController": 16},
            "ReserveMovie": {"TV": 1}
        }
        
        event_name = event_type.__name__
        return event_resources.get(event_name, {}).copy()  # Retornar copia para no modificar el original
    
    def _find_common_slots(self, all_free_intervals, duration_hours):
        """
        Encuentra huecos comunes entre múltiples recursos.
        """
        if not all_free_intervals:
            return []
        
        # Tomar los intervalos del primer recurso como base
        first_resource = list(all_free_intervals.keys())[0]
        base_intervals = all_free_intervals[first_resource]
        
        common_slots = []
        
        for interval_start, interval_end in base_intervals:
            interval_duration = (interval_end - interval_start).total_seconds() / 3600
            
            if interval_duration < duration_hours:
                continue
            
            # Verificar que todos los demás recursos tengan este intervalo libre
            is_common = True
            
            for res_name, intervals in all_free_intervals.items():
                if res_name == first_resource:
                    continue
                
                # Verificar si este recurso tiene el intervalo libre
                resource_has_interval = False
                for res_start, res_end in intervals:
                    # Si el intervalo base está completamente contenido en un intervalo libre del recurso
                    if res_start <= interval_start and res_end >= interval_end:
                        resource_has_interval = True
                        break
                
                if not resource_has_interval:
                    is_common = False
                    break
            
            if is_common:
                # Ajustar el fin al exacto de la duración requerida
                slot_end = interval_start + timedelta(hours=duration_hours)
                common_slots.append((interval_start, slot_end))
        
        return common_slots
    
    # verifica horario dentro de 8 am y 10 pm
    def _is_valid_time_slot(self, start_time, end_time):
        
        hour_start = start_time.hour
        hour_end = end_time.hour

        if hour_end == 22 and end_time.minute == 0:
            hour_end = 22
        
       
        elif hour_end > 22 or (hour_end == 22 and end_time.minute > 0):
            return False
        
        
        return 8 <= hour_start and hour_end <= 22
    
    def find_slot_for_event(self, event_instance):
        """
        Encuentra hueco para un evento ya creado (pero sin horario asignado).
        """
        duration_hours = event_instance.get_duration_hours()
        event_type = type(event_instance)
        
        return self.find_available_slot(
            event_type, 
            duration_hours,
            event_instance.clients,
            event_instance.minAge
        )


newPlanification = Planificator()
