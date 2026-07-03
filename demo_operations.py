"""Demostración secuencial de operaciones válidas e inválidas sin abrir Tkinter.

Nombre del estudinate:
- David Santiago Acosta Garcia

"""

import logging
from collections.abc import Callable
from typing import Any

from app.exceptions import SoftwareFJError
from app.manager import SoftwareFJManager

logger = logging.getLogger("software_fj")


def execute(number: int, description: str, operation: Callable[[], Any]) -> None:
    """Ejecuta una operación y muestra un resultado legible para la revisión.

    La demostración no se detiene cuando aparece un error controlado. Esto permite
    evidenciar que el sistema valida datos inválidos, registra el evento y continúa
    procesando los demás casos, tal como solicita la actividad.
    """
    try:
        result = operation()
    except SoftwareFJError as error:
        # Se conserva evidencia del error, incluso en las operaciones de demostración.
        logger.error("Caso %s falló de forma controlada: %s", number, error)
        print(f"{number:02} | CONTROLADO | {description:<38} | {error}")
    else:
        detail = str(result) if result is not None else "Operación ejecutada correctamente"
        print(f"{number:02} | OK         | {description:<38} | {detail}")


def print_header() -> None:
    """Imprime una cabecera para que la salida de consola sea fácil de leer."""
    print("=" * 110)
    print("DEMOSTRACIÓN SECUENCIAL - SISTEMA INTEGRAL SOFTWARE FJ")
    print("=" * 110)
    print("No | Estado     | Operación                              | Resultado")
    print("-" * 110)


def main() -> None:
    """Ejecuta más de diez casos requeridos y mantiene la ejecución activa."""
    manager = SoftwareFJManager()
    print_header()
    execute(1, "Crear sala válida", lambda: manager.register_room("SAL-01", "Sala Innovación", 85000, 20, "Video beam"))
    execute(2, "Crear equipo válido", lambda: manager.register_equipment("EQU-01", "Portátil empresarial", 120000, 8))
    execute(3, "Crear asesoría válida", lambda: manager.register_consulting("ASE-01", "Asesoría de software", 150000, "Arquitectura"))
    execute(4, "Crear servicio inválido", lambda: manager.register_room("SAL-ERR", "Sala sin cupo", 50000, 0, "Tablero"))
    execute(5, "Registrar cliente válido", lambda: manager.register_client("CC-100", "Ana Torres", "ana@example.com", "3001234567"))
    execute(6, "Registrar cliente inválido", lambda: manager.register_client("CC-101", "B", "correo-mal", "abc"))
    execute(7, "Crear reserva de sala válida", lambda: manager.create_reservation("RES-01", "CC-100", "SAL-01", 2, attendees=10))
    execute(8, "Crear reserva de equipo válida", lambda: manager.create_reservation("RES-02", "CC-100", "EQU-01", 3, discount=0.10, units=2))
    execute(9, "Crear reserva con inventario inválido", lambda: manager.create_reservation("RES-03", "CC-100", "EQU-01", 1, units=20))
    execute(10, "Deshabilitar un servicio", lambda: manager.set_service_availability("ASE-01", False))
    execute(11, "Reservar un servicio no disponible", lambda: manager.create_reservation("RES-04", "CC-100", "ASE-01", 1))
    execute(12, "Cancelar reserva", lambda: manager.cancel_reservation("RES-01"))
    execute(13, "Cancelar de nuevo", lambda: manager.cancel_reservation("RES-01"))
    print("-" * 110)
    print(f"Resumen final: {manager.summary()}")
    print("Registro de eventos y errores: logs/software_fj.log")


if __name__ == "__main__":
    main()
