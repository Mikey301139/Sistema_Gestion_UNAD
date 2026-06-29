"""Entidades generales y cliente; no dependen de la interfaz gráfica."""

from __future__ import annotations

from abc import ABC
from re import fullmatch

from .exceptions import ValidationError


class Entity(ABC):
    """Abstracción común para las entidades identificables del sistema."""

    def __init__(self, identifier: str) -> None:
        if not identifier or not identifier.strip():
            raise ValidationError("El identificador es obligatorio.")
        self._identifier = identifier.strip()

    @property
    def identifier(self) -> str:
        """Entrega el identificador sin permitir modificarlo desde fuera."""
        return self._identifier


class Client(Entity):
    """Cliente con datos privados y validados mediante propiedades."""

    def __init__(self, identifier: str, name: str, email: str, phone: str) -> None:
        super().__init__(identifier)
        self.name = name
        self.email = email
        self.phone = phone

    @property
    def name(self) -> str:
        return self._name

    @name.setter
    def name(self, value: str) -> None:
        if not value or len(value.strip()) < 3:
            raise ValidationError("El nombre debe tener al menos 3 caracteres.")
        self._name = value.strip().title()

    @property
    def email(self) -> str:
        return self._email

    @email.setter
    def email(self, value: str) -> None:
        pattern = r"[^@\s]+@[^@\s]+\.[^@\s]+"
        if not value or not fullmatch(pattern, value.strip()):
            raise ValidationError("El correo electrónico no tiene un formato válido.")
        self._email = value.strip().lower()

    @property
    def phone(self) -> str:
        return self._phone

    @phone.setter
    def phone(self, value: str) -> None:
        normalized = value.strip().replace(" ", "").replace("-", "")
        if not normalized.isdigit() or not 7 <= len(normalized) <= 15:
            raise ValidationError("El teléfono debe contener entre 7 y 15 dígitos.")
        self._phone = normalized

    def __str__(self) -> str:
        return f"{self.identifier} - {self.name}"
