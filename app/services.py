"""Jerarquía polimórfica de servicios ofrecidos por Software FJ."""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any

from .exceptions import ServiceUnavailableError, ValidationError
from .models import Entity


class Service(Entity, ABC):
    """Contrato abstracto que deben cumplir todos los servicios.

    Las clases hijas cambian la forma de validar y calcular costos. Esa variación
    es el uso principal de polimorfismo en la solución.
    """

    def __init__(self, identifier: str, name: str, base_rate: float, available: bool = True) -> None:
        super().__init__(identifier)
        if not name or not name.strip():
            raise ValidationError("El nombre del servicio es obligatorio.")
        if base_rate <= 0:
            raise ValidationError("La tarifa base debe ser mayor que cero.")
        self._name = name.strip()
        self._base_rate = float(base_rate)
        self._available = bool(available)

    @property
    def name(self) -> str:
        return self._name

    @property
    def available(self) -> bool:
        return self._available

    def set_availability(self, available: bool) -> None:
        """Cambia la disponibilidad desde una operación controlada."""
        self._available = bool(available)

    def ensure_available(self) -> None:
        """Impide reservar servicios deshabilitados."""
        if not self.available:
            raise ServiceUnavailableError(f"El servicio '{self.name}' no está disponible.")

    def display_name(self) -> str:
        """Nombre común usado por la interfaz, consola y reportes."""
        return self.name

    @abstractmethod
    def calculate_cost(self, duration: float, **parameters: Any) -> float:
        """Calcula el costo particular del servicio."""

    @abstractmethod
    def validate_parameters(self, duration: float, **parameters: Any) -> None:
        """Valida duración y parámetros exclusivos de cada servicio."""

    @abstractmethod
    def describe(self) -> str:
        """Devuelve una descripción legible para la interfaz."""

    def calculate_total(self, duration: float, tax_rate: float = 0.0, discount: float = 0.0, **parameters: Any) -> float:
        """Variante ampliada del cálculo: costo base, impuesto y descuento opcionales.

        Python no admite sobrecarga por firma como Java; los parámetros opcionales
        ofrecen las variantes solicitadas sin duplicar la lógica.
        """
        if not 0 <= tax_rate <= 1 or not 0 <= discount <= 1:
            raise ValidationError("Impuesto y descuento deben estar entre 0 y 1.")
        base = self.calculate_cost(duration, **parameters)
        return round(base * (1 + tax_rate) * (1 - discount), 2)


class RoomReservationService(Service):
    """Servicio de reserva de salas por horas."""

    def __init__(self, identifier: str, name: str, base_rate: float, capacity: int, equipment: str) -> None:
        super().__init__(identifier, name, base_rate)
        if capacity <= 0:
            raise ValidationError("La capacidad de la sala debe ser positiva.")
        self.capacity = capacity
        self.equipment = equipment.strip() or "Equipamiento básico"

    def validate_parameters(self, duration: float, **parameters: Any) -> None:
        try:
            attendees = int(parameters.get("attendees", 1))
        except (TypeError, ValueError) as error:
            raise ValidationError("La cantidad de asistentes debe ser numérica.") from error
        if duration <= 0:
            raise ValidationError("La duración debe ser mayor que cero.")
        if attendees < 1 or attendees > self.capacity:
            raise ValidationError(f"La sala admite entre 1 y {self.capacity} asistentes.")

    def calculate_cost(self, duration: float, **parameters: Any) -> float:
        self.validate_parameters(duration, **parameters)
        return round(self._base_rate * duration, 2)

    def describe(self) -> str:
        return f"Sala: {self.name} | capacidad: {self.capacity} | {self.equipment}"

    def __str__(self) -> str:
        return f"{self.identifier} - {self.describe()} - tarifa base ${self._base_rate:,.0f}"


class EquipmentRentalService(Service):
    """Servicio de alquiler de equipos por días y unidades."""

    def __init__(self, identifier: str, name: str, base_rate: float, stock: int) -> None:
        super().__init__(identifier, name, base_rate)
        if stock <= 0:
            raise ValidationError("El inventario de equipos debe ser positivo.")
        self.stock = stock

    def validate_parameters(self, duration: float, **parameters: Any) -> None:
        try:
            units = int(parameters.get("units", 1))
        except (TypeError, ValueError) as error:
            raise ValidationError("La cantidad de unidades debe ser numérica.") from error
        if duration <= 0:
            raise ValidationError("Los días de alquiler deben ser mayores que cero.")
        if units < 1 or units > self.stock:
            raise ValidationError(f"Solo hay {self.stock} unidades disponibles.")

    def calculate_cost(self, duration: float, **parameters: Any) -> float:
        self.validate_parameters(duration, **parameters)
        units = int(parameters.get("units", 1))
        return round(self._base_rate * duration * units, 2)

    def describe(self) -> str:
        return f"Equipo: {self.name} | unidades disponibles: {self.stock}"

    def __str__(self) -> str:
        return f"{self.identifier} - {self.describe()} - tarifa base ${self._base_rate:,.0f}"


class SpecializedConsultingService(Service):
    """Servicio de asesoría especializada por horas."""

    def __init__(self, identifier: str, name: str, base_rate: float, specialty: str) -> None:
        super().__init__(identifier, name, base_rate)
        if not specialty or not specialty.strip():
            raise ValidationError("La especialidad es obligatoria.")
        self.specialty = specialty.strip()

    def validate_parameters(self, duration: float, **parameters: Any) -> None:
        if duration <= 0 or duration > 40:
            raise ValidationError("La asesoría debe durar entre 0 y 40 horas.")

    def calculate_cost(self, duration: float, **parameters: Any) -> float:
        self.validate_parameters(duration, **parameters)
        return round(self._base_rate * duration, 2)

    def describe(self) -> str:
        return f"Asesoría: {self.name} | especialidad: {self.specialty}"

    def __str__(self) -> str:
        return f"{self.identifier} - {self.describe()} - tarifa base ${self._base_rate:,.0f}"
