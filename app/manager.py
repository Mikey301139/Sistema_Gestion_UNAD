"""Fachada de negocio: almacena objetos en memoria y centraliza operaciones."""

from __future__ import annotations

import logging
from pathlib import Path
from typing import Any

from .exceptions import DuplicateError, NotFoundError, ReservationError, SoftwareFJError
from .models import Client
from .reservation import Reservation
from .services import EquipmentRentalService, RoomReservationService, Service, SpecializedConsultingService


def configure_logger() -> logging.Logger:
    """Configura el archivo de eventos sin añadir manejadores repetidos."""
    logger = logging.getLogger("software_fj")
    if logger.handlers:
        return logger
    log_path = Path(__file__).resolve().parent.parent / "logs" / "software_fj.log"
    log_path.parent.mkdir(exist_ok=True)
    handler = logging.FileHandler(log_path, encoding="utf-8")
    handler.setFormatter(logging.Formatter("%(asctime)s | %(levelname)s | %(message)s"))
    logger.addHandler(handler)
    logger.setLevel(logging.INFO)
    return logger


class SoftwareFJManager:
    """Servicio de aplicación; sus listas viven solo mientras se ejecuta el programa."""

    def __init__(self) -> None:
        self.clients: dict[str, Client] = {}
        self.services: dict[str, Service] = {}
        self.reservations: dict[str, Reservation] = {}
        self.logger = configure_logger()
        self.logger.info("Aplicación iniciada.")

    def _add_unique(self, collection: dict[str, Any], identifier: str, entity: Any, label: str) -> None:
        if identifier in collection:
            raise DuplicateError(f"Ya existe {label} con identificador '{identifier}'.")
        collection[identifier] = entity
        self.logger.info("%s registrado: %s", label.capitalize(), identifier)

    def register_client(self, identifier: str, name: str, email: str, phone: str) -> Client:
        client = Client(identifier, name, email, phone)
        self._add_unique(self.clients, identifier, client, "un cliente")
        return client

    def register_room(self, identifier: str, name: str, rate: float, capacity: int, equipment: str) -> Service:
        service = RoomReservationService(identifier, name, rate, capacity, equipment)
        self._add_unique(self.services, identifier, service, "un servicio")
        return service

    def register_equipment(self, identifier: str, name: str, rate: float, stock: int) -> Service:
        service = EquipmentRentalService(identifier, name, rate, stock)
        self._add_unique(self.services, identifier, service, "un servicio")
        return service

    def register_consulting(self, identifier: str, name: str, rate: float, specialty: str) -> Service:
        service = SpecializedConsultingService(identifier, name, rate, specialty)
        self._add_unique(self.services, identifier, service, "un servicio")
        return service

    def create_reservation(self, identifier: str, client_id: str, service_id: str, duration: float, discount: float = 0.0, **parameters: Any) -> Reservation:
        if identifier in self.reservations:
            raise DuplicateError(f"Ya existe una reserva con identificador '{identifier}'.")
        try:
            client = self.clients[client_id]
            service = self.services[service_id]
        except KeyError as error:
            self.logger.exception("Entidad requerida no encontrada al crear la reserva.")
            raise NotFoundError(f"No existe el identificador '{error.args[0]}'.") from error
        reservation = Reservation(identifier, client, service, duration, **parameters)
        try:
            reservation.process(discount=float(discount))
        except (SoftwareFJError, ValueError, TypeError) as error:
            self.logger.exception("No fue posible procesar la reserva %s.", identifier)
            raise ReservationError(f"No se creó la reserva: {error}") from error
        else:
            self.reservations[identifier] = reservation
            self.logger.info("Reserva confirmada: %s. Total: %.2f", identifier, reservation.total)
            return reservation
        finally:
            self.logger.info("Finalizó el intento de creación de la reserva %s.", identifier)

    def cancel_reservation(self, identifier: str) -> None:
        if identifier not in self.reservations:
            raise NotFoundError(f"No existe la reserva '{identifier}'.")
        try:
            self.reservations[identifier].cancel()
            self.logger.info("Reserva cancelada: %s", identifier)
        except ReservationError:
            self.logger.exception("No fue posible cancelar la reserva %s.", identifier)
            raise

    def set_service_availability(self, service_id: str, available: bool) -> None:
        if service_id not in self.services:
            raise NotFoundError(f"No existe el servicio '{service_id}'.")
        self.services[service_id].set_availability(available)
        self.logger.info("Disponibilidad de %s: %s", service_id, available)

    def load_initial_data(self) -> None:
        """Carga tres servicios de ejemplo al iniciar una sesión nueva."""
        if self.services:
            return
        self.register_room("SAL-01", "Sala Innovación", 85000, 20, "Video beam y tablero")
        self.register_equipment("EQU-01", "Portátil empresarial", 120000, 8)
        self.register_consulting("ASE-01", "Asesoría de software", 150000, "Arquitectura y desarrollo")

    def summary(self) -> dict[str, int]:
        return {
            "clientes": len(self.clients),
            "servicios": len(self.services),
            "reservas": len(self.reservations),
            "confirmadas": sum(r.status.value == "Confirmada" for r in self.reservations.values()),
        }
