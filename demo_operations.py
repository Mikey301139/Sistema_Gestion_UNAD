"""Demostración secuencial del sistema sin abrir la interfaz gráfica.

Estudiante:
- David Santiago Acosta Garcia

Este archivo permite evidenciar en consola las operaciones solicitadas en el
anexo: creación de servicios, registro de clientes, reservas correctas y errores
controlados. La salida se presenta en formato tabular para facilitar depuración,
seguimiento y captura de evidencias.
"""

from __future__ import annotations

import logging
from collections.abc import Callable
from typing import Any

from app.exceptions import SoftwareFJError
from app.manager import SoftwareFJManager

logger = logging.getLogger("software_fj")


def format_result(result: Any) -> str:
    """Convierte el resultado de cada operación en texto claro para consola."""
    if result is None:
        return "Operación ejecutada correctamente"
    return str(result)


def execute_case(number: int, description: str, operation: Callable[[], Any]) -> None:
    """Ejecuta un caso de prueba manual sin detener la demostración.

    Si ocurre una excepción propia del sistema, el error se registra y se muestra
    como CONTROLADO. Esto evidencia que el programa continúa funcionando después
    de entradas inválidas.
    """
    try:
        result = operation()
    except SoftwareFJError as error:
        logger.error("Caso %s controlado: %s", number, error)
        status = "CONTROLADO"
        detail = str(error)
    except Exception as error:  # Protección final para detectar errores no previstos.
        logger.exception("Caso %s produjo un error inesperado", number)
        status = "ERROR"
        detail = f"Error inesperado: {error}"
    else:
        status = "OK"
        detail = format_result(result)

    print(f"{number:02} | {status:<10} | {description:<40} | {detail}")


def print_header() -> None:
    """Imprime encabezado informativo para que la consola sea fácil de leer."""
    print("=" * 118)
    print("DEMOSTRACIÓN SECUENCIAL - SISTEMA DE GESTIÓN SOFTWARE FJ")
    print("=" * 118)
    print(f"{'No':<2} | {'Estado':<10} | {'Operación':<40} | Resultado")
    print("-" * 118)


def print_summary(manager: SoftwareFJManager) -> None:
    """Muestra el resumen final de objetos gestionados en memoria."""
    summary = manager.summary()
    print("-" * 118)
    print("RESUMEN FINAL")
    print(f"Clientes registrados     : {summary['clientes']}")
    print(f"Servicios registrados    : {summary['servicios']}")
    print(f"Reservas almacenadas     : {summary['reservas']}")
    print(f"Reservas confirmadas     : {summary['confirmadas']}")
    print("Log de eventos y errores : logs/software_fj.log")


def main() -> None:
    """Ejecuta más de diez operaciones válidas e inválidas de forma secuencial."""
    manager = SoftwareFJManager()
    print_header()

    execute_case(1, "Crear sala válida", lambda: manager.register_room("SAL-01", "Sala Innovación", 85000, 20, "Video beam"))
    execute_case(2, "Crear equipo válido", lambda: manager.register_equipment("EQU-01", "Portátil empresarial", 120000, 8))
    execute_case(3, "Crear asesoría válida", lambda: manager.register_consulting("ASE-01", "Asesoría de software", 150000, "Arquitectura"))
    execute_case(4, "Crear servicio inválido", lambda: manager.register_room("SAL-ERR", "Sala sin cupo", 50000, 0, "Tablero"))
    execute_case(5, "Registrar cliente válido", lambda: manager.register_client("CC-100", "Ana Torres", "ana@example.com", "3001234567"))
    execute_case(6, "Registrar cliente inválido", lambda: manager.register_client("CC-101", "B", "correo-mal", "abc"))
    execute_case(7, "Crear reserva de sala válida", lambda: manager.create_reservation("RES-01", "CC-100", "SAL-01", 2, attendees=10))
    execute_case(8, "Crear reserva de equipo válida", lambda: manager.create_reservation("RES-02", "CC-100", "EQU-01", 3, discount=0.10, units=2))
    execute_case(9, "Reserva con inventario inválido", lambda: manager.create_reservation("RES-03", "CC-100", "EQU-01", 1, units=20))
    execute_case(10, "Deshabilitar servicio", lambda: manager.set_service_availability("ASE-01", False))
    execute_case(11, "Reservar servicio no disponible", lambda: manager.create_reservation("RES-04", "CC-100", "ASE-01", 1))
    execute_case(12, "Cancelar reserva", lambda: manager.cancel_reservation("RES-01"))
    execute_case(13, "Cancelar reserva nuevamente", lambda: manager.cancel_reservation("RES-01"))

    print_summary(manager)


if __name__ == "__main__":
    main()
