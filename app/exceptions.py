"""Excepciones de dominio para comunicar errores controlados a la interfaz."""

# Todas las excepciones propias heredan de SoftwareFJError. Así, tanto la GUI
# como demo_operations.py pueden capturar un solo tipo base y mostrar el
# mensaje al usuario sin distinguir manualmente cada subclase.


class SoftwareFJError(Exception):
    """Clase base de los errores previsibles del sistema."""


class ValidationError(SoftwareFJError):
    """Indica que un dato no cumple una regla de negocio."""


class DuplicateError(SoftwareFJError):
    """Indica que se intentó registrar una entidad que ya existe."""


class NotFoundError(SoftwareFJError):
    """Indica que no se encontró la entidad solicitada."""


class ServiceUnavailableError(SoftwareFJError):
    """Indica que un servicio no puede aceptar una reserva."""


class ReservationError(SoftwareFJError):
    """Indica que no es posible completar una operación de reserva."""
