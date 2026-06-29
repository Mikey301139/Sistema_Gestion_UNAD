"""Demostración secuencial de operaciones válidas e inválidas sin abrir Tkinter.

Integrantes del equipo (reemplazar antes de entregar):
- David Santiago Acosta Garcia
"""

from app.exceptions import SoftwareFJError
from app.manager import SoftwareFJManager


def execute(number: int, description: str, operation) -> None:
    """Ejecuta una operación, evidencia los errores esperados y continúa."""
    try:
        result = operation()
    except SoftwareFJError as error:
        # Se conserva evidencia del error, incluso en las operaciones de demostración.
        __import__("logging").getLogger("software_fj").error("Caso %s falló de forma controlada: %s", number, error)
        print(f"{number:02}. CONTROLADO | {description}: {error}")
    else:
        value = f" -> {result}" if result is not None else ""
        print(f"{number:02}. OK         | {description}{value}")


def main() -> None:
    """Ejecuta más de diez casos requeridos y mantiene la ejecución activa."""
    manager = SoftwareFJManager()
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
    print("\nResumen final:", manager.summary())
    print("Revise logs/software_fj.log para el registro de eventos y errores.")


if __name__ == "__main__":
    main()
