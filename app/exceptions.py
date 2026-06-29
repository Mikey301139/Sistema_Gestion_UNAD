"""Excepciones de dominio para comunicar errores controlados a la interfaz."""


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
