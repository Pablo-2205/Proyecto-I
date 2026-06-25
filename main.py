import sys
from datetime import datetime, timedelta
import Events as events
import Planificator as plan
import Resource as resource  
from Events import create_event_from_dict

def mostrar_menu():
    """Muestra el menú principal"""
    print("\n" + "="*50)
    print("  PLANIFICADOR INTELIGENTE DE EVENTOS")
    print("  Salón de Videojuegos y Cine")
    print("="*50)
    print("\nMENÚ PRINCIPAL:")
    print("1. Listar todos los eventos")
    print("2. Agregar nuevo evento")
    print("3. Eliminar evento")
    print("4. Buscar hueco disponible")
    print("5. Guardar datos")
    print("6. Cargar datos")
    print("7. Ver recursos disponibles")
    print("8. Ver agenda de recursos")
    print("0. Salir")
    print("-"*50)

def listar_eventos(planificador):
    """Lista todos los eventos programados"""
    print("\n" + "="*60)
    print("EVENTOS PROGRAMADOS")
    print("="*60)
    
    if not planificador.events:
        print("No hay eventos programados")
        return
    
    for i, event in enumerate(planificador.events, 1):
        print(f"\n{i}. {event.description}")
        print(f"   Tipo: {event.__class__.__name__}")
        print(f"   Hora: {event.start.strftime('%Y-%m-%d %H:%M')} a {event.end.strftime('%H:%M')}")
        print(f"   Duración: {(event.end - event.start).seconds // 3600} horas")
        print(f"   Personas: {event.clients}")
        if event.minAge > 0:
            print(f"   Edad mínima: {event.minAge} años")
        print(f"   Estado: {'✓ Recursos reservados' if event.description in planificador.tags else '✗ Sin recursos'}")

def agregar_evento_manual(planificador):
    """Interfaz para agregar un evento manualmente"""
    print("\n" + "="*50)
    print("AGREGAR NUEVO EVENTO")
    print("="*50)
    
    print("\nTipos de eventos disponibles:")
    print("1. Reserva de PS5 (requiere 1 PS5 + 2 controles)")
    print("2. Reserva de PS4 (requiere 1 PS4 + 2 control)")
    print("3. Reserva de Xbox 360 (requiere 1 Xbox360 + 2 control)")
    print("4. Torneo de Dota (requiere 16 PCs + 16 audífonos, 16 personas)")
    print("5. Torneo de FIFA (requiere 4 PS5 + 2 controles + 4 TVs, mínimo 8 personas)")
    print("6. Torneo de Call of Duty (requiere 4 XboxOne + 16 controles + 4 TVs, mínimo 16 personas, edad 16+)")
    print("7. Reserva para ver películas (requiere 1 TV)")
    
    try:
        opcion = input("\nSeleccione el tipo de evento (1-7): ").strip()
        
        # Datos comunes
        descripcion = input("Descripción del evento: ").strip()
        fecha = input("Fecha (YYYY-MM-DD): ").strip()
        hora_inicio = input("Hora de inicio (HH:MM): ").strip()
        hora_fin = input("Hora de fin (HH:MM): ").strip()
        
        start_str = f"{fecha} {hora_inicio}"
        end_str = f"{fecha} {hora_fin}"
        
        # Validar formato de fecha
        try:
            datetime.strptime(start_str, "%Y-%m-%d %H:%M")
            datetime.strptime(end_str, "%Y-%m-%d %H:%M")
        except ValueError:
            print("✗ Error: Formato de fecha/hora incorrecto. Use YYYY-MM-DD HH:MM")
            return
        
        evento = None
        
        if opcion == "1":  # ReservePS5
            clients = int(input("Número de personas: ") or "1")
            evento = events.ReservePS5(descripcion, start_str, end_str, clients)
            
        elif opcion == "2":  # ReservePS4
            clients = int(input("Número de personas: ") or "1")
            evento = events.ReservePS4(descripcion, start_str, end_str, clients)
            
        elif opcion == "3":  # ReserveXbox360
            clients = int(input("Número de personas: ") or "1")
            evento = events.ReserveXbox360(descripcion, start_str, end_str, clients)
            
        elif opcion == "4":  # DotaTournament
            print("Torneo de Dota: se requieren exactamente 16 personas")
            clients = 16  # Fijo para Dota
            evento = events.DotaTournament(descripcion, start_str, end_str, clients)
            
        elif opcion == "5":  # FifaTournament
            clients = int(input("Número de personas (mínimo 8): ") or "8")
            evento = events.FifaTournament(descripcion, start_str, end_str, clients)
            
        elif opcion == "6":  # CallofDutyTournament
            clients = int(input("Número de personas (mínimo 16): ") or "16")
            min_age = int(input("Edad mínima (mínimo 16): ") or "16")
            evento = events.CallofDutyTournament(descripcion, start_str, end_str, clients, min_age)
            
        elif opcion == "7":  # ReserveMovie
            clients = int(input("Número de personas: ") or "1")
            evento = events.ReserveMovie(descripcion, start_str, end_str, clients)
            
        else:
            print("✗ Opción no válida")
            return
        
        # Validar fecha futura
        if evento.start < datetime.now():
            print("✗ Error: No se pueden crear eventos en el pasado")
            return
        
        # Intentar agregar el evento
        planificador.AddEvents(evento)
        print(f"✓ Evento '{descripcion}' agregado exitosamente")
        
    except ValueError as e:
        print(f"✗ Error: {e}")
    except Exception as e:
        print(f"✗ Error inesperado: {e}")
        import traceback
        traceback.print_exc()

def eliminar_evento(planificador):
    """Elimina un evento por descripción"""
    print("\n" + "="*50)
    print("ELIMINAR EVENTO")
    print("="*50)
    
    if not planificador.tags:
        print("No hay eventos para eliminar")
        return
    
    print("\nEventos disponibles:")
    for i, tag in enumerate(planificador.tags, 1):
        # Encontrar el evento para mostrar más detalles
        evento = None
        for e in planificador.events:
            if e.description == tag:
                evento = e
                break
        
        hora_info = ""
        if evento:
            hora_info = f" ({evento.start.strftime('%H:%M')}-{evento.end.strftime('%H:%M')})"
        
        print(f"{i}. {tag}{hora_info}")
    
    try:
        opcion = input("\nSeleccione el número del evento a eliminar: ").strip()
        indice = int(opcion) - 1
        
        if 0 <= indice < len(planificador.tags):
            tag_a_eliminar = planificador.tags[indice]
            planificador.RemoveEvents(tag_a_eliminar)
            print(f"✓ Evento '{tag_a_eliminar}' eliminado")
        else:
            print("✗ Número no válido")
            
    except (ValueError, IndexError):
        print("✗ Entrada no válida")
    except Exception as e:
        print(f"✗ Error: {e}")

def buscar_hueco_disponible(planificador):
    """Busca el próximo hueco disponible para un tipo de evento"""
    print("\n" + "="*50)
    print("BUSCAR HUECO DISPONIBLE")
    print("="*50)
    
    print("\nTipos de eventos disponibles:")
    print("1. Reserva de PS5 (1 PS5 + 2 controles)")
    print("2. Reserva de PS4 (1 PS4 + 2 control)")
    print("3. Reserva de Xbox 360 (1 Xbox360 + 2 control)")
    print("4. Torneo de Dota (16 PCs + 16 audífonos, 16 personas)")
    print("5. Torneo de FIFA (4 PS5 + 2 controles + 4 TVs, mínimo 8 personas)")
    print("6. Torneo de Call of Duty (4 XboxOne + 16 controles + 4 TVs, 16 personas, edad 16+)")
    print("7. Reserva para ver películas (1 TV)")
    
    try:
        opcion = input("\nSeleccione el tipo de evento (1-7): ").strip()
        
        # Mapear opción a clase de evento
        event_classes = {
            "1": events.ReservePS5,
            "2": events.ReservePS4,
            "3": events.ReserveXbox360,
            "4": events.DotaTournament,
            "5": events.FifaTournament,
            "6": events.CallofDutyTournament,
            "7": events.ReserveMovie
        }
        
        if opcion not in event_classes:
            print("✗ Opción no válida")
            return
        
        event_class = event_classes[opcion]
        
        # Obtener duración
        try:
            duration = float(input("Duración deseada (horas): ").strip())
            if duration <= 0:
                print("✗ La duración debe ser mayor a 0")
                return
        except ValueError:
            print("✗ Duración no válida")
            return
        
        # Parámetros específicos según el evento
        clients = 0
        min_age = 0
        
        if opcion == "4":  # Dota
            clients = 16
            print(f"Torneo de Dota: se requieren exactamente {clients} personas")
        elif opcion == "5":  # FIFA
            clients = int(input("Número de personas (mínimo 8): ") or "8")
            if clients < 8:
                print("✗ Se requieren al menos 8 personas para un torneo de FIFA")
                return
        elif opcion == "6":  # Call of Duty
            clients = int(input("Número de personas (mínimo 16): ") or "16")
            if clients < 16:
                print("✗ Se requieren al menos 16 personas para un torneo de Call of Duty")
                return
            min_age = int(input("Edad mínima (mínimo 16): ") or "16")
            if min_age < 16:
                print("✗ La edad mínima debe ser al menos 16 años")
                return
        else:
            clients = int(input("Número de personas: ") or "1")
        
        # Opción para especificar fecha de inicio
        print("\n¿Buscar desde una fecha específica?")
        fecha_input = input("Fecha (YYYY-MM-DD) [hoy]: ").strip()
        
        start_date = None
        if fecha_input:
            try:
                start_date = datetime.strptime(fecha_input, "%Y-%m-%d").date()
            except ValueError:
                print("⚠ Formato de fecha inválido. Usando fecha de hoy.")
        
        # Opción para número de días a buscar
        try:
            max_days = int(input("Número de días a buscar (1-30) [7]: ") or "7")
            if max_days < 1 or max_days > 30:
                print("⚠ Número de días debe estar entre 1 y 30. Usando 7 días.")
                max_days = 7
        except ValueError:
            print("⚠ Entrada inválida. Usando 7 días.")
            max_days = 7
        
        # Buscar hueco
        print(f"\n🔍 Buscando hueco disponible para {event_class.__name__}...")
        print(f"   Duración: {duration} horas")
        print(f"   Personas: {clients}")
        if min_age > 0:
            print(f"   Edad mínima: {min_age}")
        if start_date:
            print(f"   Fecha de inicio: {start_date}")
        print(f"   Días a buscar: {max_days}")
        
        slot_start, slot_end = planificador.find_available_slot(
            event_class, duration, clients, min_age, start_date, max_days
        )
        
        if slot_start and slot_end:
            print("\n✅ ¡HUECO ENCONTRADO!")
            print(f"   Fecha: {slot_start.strftime('%Y-%m-%d')}")
            print(f"   Horario: {slot_start.strftime('%H:%M')} - {slot_end.strftime('%H:%M')}")
            print(f"   Duración: {duration} horas")
            
            # Preguntar si quiere crear el evento en ese hueco
            crear = input("\n¿Crear evento en este horario? (s/n): ").strip().lower()
            if crear == "s":
                descripcion = input("Descripción del evento: ").strip()
                
                # Crear el evento
                try:
                    evento = event_class(
                        description=descripcion,
                        start_str=slot_start.strftime("%Y-%m-%d %H:%M"),
                        end_str=slot_end.strftime("%Y-%m-%d %H:%M"),
                        clients=clients,
                        minAge=min_age
                    )
                    
                    planificador.AddEvents(evento)
                    print(f"✅ Evento '{descripcion}' creado exitosamente")
                    
                except ValueError as e:
                    print(f"✗ Error al crear evento: {e}")
                except Exception as e:
                    print(f"✗ Error inesperado: {e}")
        else:
            print("\n❌ No se encontró ningún hueco disponible en el período especificado.")
            print("   Sugerencias:")
            print("   - Intente con una duración más corta")
            print("   - Busque en más días")
            print("   - Pruebe en otra fecha")
        
    except Exception as e:
        print(f"✗ Error: {e}")
        import traceback
        traceback.print_exc()

def ver_recursos_disponibles():
    """Muestra los recursos disponibles REALES (cantidades totales)"""
    print("\n" + "="*50)
    print("INVENTARIO DE RECURSOS")
    print("="*50)
    
    recursos = [
        ("PS5", resource.PS5.quantity),
        ("PS4", resource.PS4.quantity),
        ("Control PS5", resource.PS5Controller.quantity),
        ("Control PS4", resource.PS4Controller.quantity),
        ("Xbox 360", resource.Xbox360.quantity),
        ("Control Xbox 360", resource.Xbox360Controller.quantity),
        ("Xbox One", resource.XboxOne.quantity),
        ("Control Xbox One", resource.XboxOneController.quantity),
        ("PC", resource.PC.quantity),
        ("TV", resource.TV.quantity),
        ("Audífonos", resource.HeadPhones.quantity),
        ("Gafas VR", resource.VRGlasses.quantity)
    ]
    
    print("\nRecurso\t\t\tCantidad total")
    print("-"*40)
    for nombre, cantidad in recursos:
        print(f"{nombre:20} {cantidad:3d} unidades")

def ver_agenda_recursos():
    """Muestra las reservas activas por recurso"""
    print("\n" + "="*60)
    print("AGENDA DE RECURSOS (RESERVAS ACTIVAS)")
    print("="*60)
    
    # Lista de todos los recursos a verificar
    recursos_info = [
        ("PS5", resource.PS5),
        ("PS4", resource.PS4),
        ("Control PS5", resource.PS5Controller),
        ("Control PS4", resource.PS4Controller),
        ("Xbox 360", resource.Xbox360),
        ("Control Xbox 360", resource.Xbox360Controller),
        ("Xbox One", resource.XboxOne),
        ("Control Xbox One", resource.XboxOneController),
        ("PC", resource.PC),
        ("TV", resource.TV),
        ("Audífonos", resource.HeadPhones),
        ("Gafas VR", resource.VRGlasses)
    ]
    
    total_reservas = 0
    recursos_con_reservas = 0
    
    for nombre, clase_recurso in recursos_info:
        # Verificar si la clase tiene el atributo bookings
        if hasattr(clase_recurso, 'bookings') and clase_recurso.bookings:
            recursos_con_reservas += 1
            print(f"\n{nombre.upper()}:")
            print("-" * 40)
            
            for i, booking in enumerate(clase_recurso.bookings, 1):
                # Formatear las horas
                hora_inicio = booking['start'].strftime('%H:%M')
                hora_fin = booking['end'].strftime('%H:%M')
                fecha = booking['start'].strftime('%Y-%m-%d')
                
                print(f"  {i}. Evento: {booking['event']}")
                print(f"     Cantidad: {booking['amount']} unidad(es)")
                print(f"     Fecha: {fecha}")
                print(f"     Horario: {hora_inicio} - {hora_fin}")
                print(f"     Duración: {(booking['end'] - booking['start']).seconds // 3600} hora(s)")
                total_reservas += booking['amount']
    
    if recursos_con_reservas == 0:
        print("\nNo hay reservas activas en ningún recurso")
    else:
        print(f"\n{'='*60}")
        print(f"RESUMEN: {total_reservas} recurso(s) reservado(s) en total")
        print(f"         {recursos_con_reservas} tipo(s) de recurso con reservas activas")

def ver_recursos_por_horario():
    """Muestra disponibilidad de recursos en un horario específico"""
    print("\n" + "="*50)
    print("DISPONIBILIDAD POR HORARIO")
    print("="*50)
    
    try:
        fecha = input("Fecha (YYYY-MM-DD) [hoy]: ").strip()
        if not fecha:
            fecha = datetime.now().strftime("%Y-%m-%d")
        
        hora_inicio = input("Hora de inicio (HH:MM): ").strip()
        hora_fin = input("Hora de fin (HH:MM): ").strip()
        
        start_str = f"{fecha} {hora_inicio}"
        end_str = f"{fecha} {hora_fin}"
        
        # Convertir a datetime
        start_time = datetime.strptime(start_str, "%Y-%m-%d %H:%M")
        end_time = datetime.strptime(end_str, "%Y-%m-%d %H:%M")
        
        if end_time <= start_time:
            print("✗ Error: La hora de fin debe ser después de la hora de inicio")
            return
        
        print(f"\nDisponibilidad de {hora_inicio} a {hora_fin} el {fecha}:")
        print("-" * 50)
        
        recursos_info = [
            ("PS5", resource.PS5),
            ("PS4", resource.PS4),
            ("Control PS5", resource.PS5Controller),
            ("Control PS4", resource.PS4Controller),
            ("Xbox 360", resource.Xbox360),
            ("Control Xbox 360", resource.Xbox360Controller),
            ("Xbox One", resource.XboxOne),
            ("Control Xbox One", resource.XboxOneController),
            ("PC", resource.PC),
            ("TV", resource.TV),
            ("Audífonos", resource.HeadPhones),
            ("Gafas VR", resource.VRGlasses)
        ]
        
        print("\nRecurso\t\t\tDisponible\tOcupado\t\tTotal")
        print("-" * 60)
        
        for nombre, clase_recurso in recursos_info:
            if hasattr(clase_recurso, 'get_available_in_interval'):
                disponible = clase_recurso.get_available_in_interval(start_time, end_time)
                ocupado = clase_recurso.quantity - disponible
                print(f"{nombre:20} {disponible:3d}\t\t{ocupado:3d}\t\t{clase_recurso.quantity:3d}")
        
    except ValueError as e:
        print(f"✗ Error en el formato: {e}")
    except Exception as e:
        print(f"✗ Error: {e}")

def main():
    """Función principal del programa"""
    print("\n" + "="*50)
    print("  BIENVENIDO AL PLANIFICADOR DE EVENTOS")
    print("  Salón de Videojuegos y Cine")
    print("="*50)
    print("\nSistema de gestión de reservas por horario")
    print("✓ Los recursos se bloquean durante la duración del evento")
    print("✓ No se permiten dobles reservas en el mismo horario")
    print("✓ Recursos se liberan automáticamente al eliminar eventos")
    print("✓ Búsqueda inteligente de huecos disponibles")
    
    # Crear planificador
    planificador = plan.Planificator()
    
    # Cargar datos automáticamente al inicio
    print("\nCargando datos previos...")
    try:
        planificador.load_from_file("datos.json")
        print("✓ Datos cargados exitosamente")
    except Exception as e:
        print(f"⚠ No se pudieron cargar datos previos: {e}")
        print("Comenzando con lista vacía de eventos")
    
    while True:
        mostrar_menu()
        
        opcion = input("\nSeleccione una opción (0-8): ").strip()
        
        if opcion == "0":
            print("\n¿Desea guardar antes de salir? (s/n): ", end="")
            if input().strip().lower() == "s":
                try:
                    planificador.save_to_file("datos.json")
                    print("✓ Datos guardados exitosamente")
                except Exception as e:
                    print(f"✗ Error al guardar: {e}")
            print("\n¡Gracias por usar el Planificador de Eventos!")
            print("¡Hasta pronto!")
            break
            
        elif opcion == "1":
            listar_eventos(planificador)
            
        elif opcion == "2":
            agregar_evento_manual(planificador)
            
        elif opcion == "3":
            eliminar_evento(planificador)
            
        elif opcion == "4":
            buscar_hueco_disponible(planificador)
            
        elif opcion == "5":
            try:
                planificador.save_to_file("datos.json")
                print("✓ Datos guardados exitosamente")
            except Exception as e:
                print(f"✗ Error al guardar: {e}")
            
        elif opcion == "6":
            print("\n⚠ Cargando nuevos datos (se perderán los cambios no guardados)...")
            confirmar = input("¿Continuar? (s/n): ").strip().lower()
            if confirmar == "s":
                try:
                    planificador.load_from_file("datos.json")
                    print("✓ Datos cargados exitosamente")
                except Exception as e:
                    print(f"✗ Error al cargar: {e}")
            
        elif opcion == "7":
            print("\nOpciones de recursos:")
            print("1. Ver inventario total")
            print("2. Ver agenda de reservas")
            print("3. Ver disponibilidad por horario")
            
            sub_opcion = input("\nSeleccione (1-3): ").strip()
            
            if sub_opcion == "1":
                ver_recursos_disponibles()
            elif sub_opcion == "2":
                ver_agenda_recursos()
            elif sub_opcion == "3":
                ver_recursos_por_horario()
            else:
                print("✗ Opción no válida")
            
        elif opcion == "8":
            ver_agenda_recursos()
            
        else:
            print("✗ Opción no válida. Intente nuevamente.")
        
        # Pausa antes de mostrar el menú nuevamente
        if opcion != "0":
            input("\nPresione Enter para continuar...")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nPrograma interrumpido por el usuario.")
        # Preguntar si quiere guardar antes de salir
        guardar = input("\n¿Desea guardar antes de salir? (s/n): ").strip().lower()
        if guardar == "s":
            try:
                planificador = plan.Planificator()
                planificador.load_from_file("datos.json")
                planificador.save_to_file("datos.json")
                print("✓ Datos guardados")
            except:
                print("✗ No se pudieron guardar los datos")
        print("\n¡Hasta pronto!")
    except Exception as e:
        print(f"\n✗ Error crítico: {e}")
        import traceback
        traceback.print_exc()
        input("\nPresione Enter para salir...")
