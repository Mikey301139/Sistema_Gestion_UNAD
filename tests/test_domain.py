"""Validación secuencial de las reglas más importantes del problema."""

import unittest

from app.exceptions import DuplicateError, ReservationError, ValidationError
from app.manager import SoftwareFJManager


class SoftwareFJDomainTests(unittest.TestCase):
    """Comprueba que las fallas controladas no destruyen el estado de la sesión."""

    def setUp(self) -> None:
        self.manager = SoftwareFJManager()
        self.manager.load_initial_data()
        self.manager.register_client("CLI-01", "María López", "maria@example.com", "3001234567")

    def test_confirmed_room_reservation_includes_tax(self) -> None:
        reservation = self.manager.create_reservation("RES-01", "CLI-01", "SAL-01", 2, attendees=5)
        self.assertEqual(reservation.status.value, "Confirmada")
        self.assertEqual(reservation.total, 202300.0)

    def test_invalid_equipment_does_not_store_reservation(self) -> None:
        with self.assertRaises(ReservationError):
            self.manager.create_reservation("RES-02", "CLI-01", "EQU-01", 1, units=99)
        self.assertNotIn("RES-02", self.manager.reservations)

    def test_invalid_client_is_rejected(self) -> None:
        with self.assertRaises(ValidationError):
            self.manager.register_client("CLI-02", "X", "incorrecto", "12")

    def test_duplicate_client_is_rejected(self) -> None:
        with self.assertRaises(DuplicateError):
            self.manager.register_client("CLI-01", "Otra Persona", "otra@example.com", "3000000000")

    def test_reservation_can_only_be_cancelled_once(self) -> None:
        self.manager.create_reservation("RES-03", "CLI-01", "ASE-01", 2)
        self.manager.cancel_reservation("RES-03")
        with self.assertRaises(ReservationError):
            self.manager.cancel_reservation("RES-03")


if __name__ == "__main__":
    unittest.main(verbosity=2)
