"""Entidad Reserva y su ciclo de vida."""

from __future__ import annotations

from enum import Enum
from typing import Any

from .exceptions import ReservationError
from .models import Client, Entity
from .services import Service


class ReservationStatus(str, Enum):
    """Estados permitidos para una reserva."""

    PENDING = "Pendiente"
    CONFIRMED = "Confirmada"
    CANCELLED = "Cancelada"


class Reservation(Entity):
    """Relaciona cliente, servicio, duración, datos específicos y estado."""

    def __init__(self, identifier: str, client: Client, service: Service, duration: float, **parameters: Any) -> None:
        super().__init__(identifier)
        self.client = client
        self.service = service
        self.duration = float(duration)
        self.parameters = parameters
        self.status = ReservationStatus.PENDING
        self.total = 0.0

    def process(self, tax_rate: float = 0.19, discount: float = 0.0) -> float:
        """Valida, calcula y confirma; conserva el objeto en estado consistente."""
        if self.status == ReservationStatus.CANCELLED:
            raise ReservationError("No se puede procesar una reserva cancelada.")
        self.service.ensure_available()
        self.service.validate_parameters(self.duration, **self.parameters)
        self.total = self.service.calculate_total(self.duration, tax_rate, discount, **self.parameters)
        self.status = ReservationStatus.CONFIRMED
        return self.total

    def cancel(self) -> None:
        """Cancela una reserva pendiente o confirmada una única vez."""
        if self.status == ReservationStatus.CANCELLED:
            raise ReservationError("La reserva ya se encuentra cancelada.")
        self.status = ReservationStatus.CANCELLED
