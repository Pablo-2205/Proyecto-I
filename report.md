Descripcion del Proyecto: Este proyecto implementa un planificador inteligente para un salón de videojuegos y cine. Permite gestionar la reserva de recursos (consolas, controles, TVs, PCs, audífonos, etc.) para diferentes tipos de eventos, garantizando que no haya conflictos de horario ni violaciones de las reglas de negocio definidas.

La aplicación ofrece una interfaz por consola (CLI) con la que el usuario puede: -Listar todos los eventos programados. -Agregar nuevos eventos (con validación automática). -Eliminar eventos (liberando los recursos asociados). -Buscar automáticamente el próximo hueco disponible para un tipo de evento. -Ver el inventario de recursos y su agenda de reservas. -Guardar y cargar el estado desde un archivo JSON.

Dominio Elegido: El dominio elegido es de un salón de videojuegos y cine, un espacio de entretenimiento donde los clientes pueden reservar consolas, participar en torneos o ver películas en salas equipadas con TVs.

Eventos Soportados: -Reserva de PS5 – requiere 1 PS5 y 2 controles PS5. -Reserva de PS4 – requiere 1 PS4 y 2 controles PS4. -Reserva de Xbox 360 – requiere 1 Xbox 360 y 2 controles Xbox 360. -Torneo de Dota – requiere exactamente 16 participantes, 16 PCs y 16 audífonos. -Torneo de FIFA – requiere al menos 8 participantes, 4 PS5, 2 controles PS5 y 4 TVs. -Torneo de Call of Duty – requiere al menos 16 participantes (todos mayores de 16 años), 4 Xbox One, 16 controles Xbox One y 4 TVs. -Reserva de película – requiere 1 TV.

Ejecucion del Programa: Requsitos: -Python 3.6 o superior -No se requieren librerias externas (solo módulos estándar: datetime, json, sys).

Instrucciones: Asegurate de tener: main.py Planificator.py Events.py Resource.py datos.json

Ejecuta el programa con main.py

Estructura del Codigo: -main.py – Punto de entrada, interfaz de usuario y orquestación general. -Planificator.py – Clase Planificator que gestiona la lista de eventos, la validación de solapamientos, la asignación/liberación de recursos y la persistencia. -Events.py – Define la clase base Events y todas las subclases de eventos concretos. Cada una implementa su propia validación y la lógica de reserva/liberación de recursos. -Resource.py – Clase base Resource y sus subclases (PS5, PS4, etc.) que mantienen la cantidad disponible, las reservas activas y los métodos para consultar disponibilidad, reservar y liberar.
