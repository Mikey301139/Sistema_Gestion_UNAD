"""Interfaz gráfica Tkinter para el Sistema Integral Software FJ."""

from __future__ import annotations

import logging
import tkinter as tk
from tkinter import messagebox, ttk

from .exceptions import SoftwareFJError, ValidationError
from .manager import SoftwareFJManager
from .services import EquipmentRentalService, RoomReservationService


class SoftwareFJApp(tk.Tk):
    """Ventana principal que delega las reglas de negocio al administrador."""

    def __init__(self, manager: SoftwareFJManager) -> None:
        super().__init__()
        self.manager = manager
        self.title("Software FJ | Clientes, Servicios y Reservas")
        self.geometry("1010x690")
        self.minsize(900, 620)
        self.configure(padx=12, pady=12)
        self._build_interface()
        self.refresh_all()

    def _build_interface(self) -> None:
        ttk.Label(self, text="Sistema Integral de Gestión - Software FJ", font=("Segoe UI", 18, "bold")).pack(anchor="w")
        ttk.Label(self, text="Gestión en memoria con validaciones, herencia, polimorfismo y registro de eventos.").pack(anchor="w", pady=(0, 10))
        self.tabs = ttk.Notebook(self)
        self.tabs.pack(expand=True, fill="both")
        self.dashboard_tab = ttk.Frame(self.tabs, padding=12)
        self.clients_tab = ttk.Frame(self.tabs, padding=12)
        self.services_tab = ttk.Frame(self.tabs, padding=12)
        self.reservations_tab = ttk.Frame(self.tabs, padding=12)
        self.tabs.add(self.dashboard_tab, text="Resumen")
        self.tabs.add(self.clients_tab, text="Clientes")
        self.tabs.add(self.services_tab, text="Servicios")
        self.tabs.add(self.reservations_tab, text="Reservas")
        self._build_dashboard()
        self._build_clients()
        self._build_services()
        self._build_reservations()

    def _build_dashboard(self) -> None:
        self.summary_label = ttk.Label(self.dashboard_tab, font=("Segoe UI", 14), justify="left")
        self.summary_label.pack(anchor="w", pady=10)
        ttk.Label(self.dashboard_tab, text="Flujo sugerido", font=("Segoe UI", 12, "bold")).pack(anchor="w", pady=(15, 5))
        ttk.Label(self.dashboard_tab, text="1. Registre clientes.   2. Cree o use servicios iniciales.   3. Confirme o cancele reservas.\nLos errores se muestran sin cerrar la aplicación y quedan registrados en logs/software_fj.log.", justify="left").pack(anchor="w")

    def _build_clients(self) -> None:
        form = ttk.LabelFrame(self.clients_tab, text="Registrar cliente", padding=10)
        form.pack(fill="x")
        self.client_vars = {key: tk.StringVar() for key in ("id", "name", "email", "phone")}
        for column, (key, label) in enumerate((("id", "Identificación"), ("name", "Nombre"), ("email", "Correo"), ("phone", "Teléfono"))):
            ttk.Label(form, text=label).grid(row=0, column=column, sticky="w", padx=4)
            ttk.Entry(form, textvariable=self.client_vars[key], width=24).grid(row=1, column=column, sticky="ew", padx=4)
        ttk.Button(form, text="Registrar cliente", command=self.add_client).grid(row=1, column=4, padx=10)
        self.clients_tree = self._tree(self.clients_tab, ("ID", "Nombre", "Correo", "Teléfono"), (120, 230, 260, 140))

    def _build_services(self) -> None:
        form = ttk.LabelFrame(self.services_tab, text="Crear servicio", padding=10)
        form.pack(fill="x")
        self.service_type = tk.StringVar(value="Sala")
        self.service_vars = {key: tk.StringVar() for key in ("id", "name", "rate", "detail")}
        ttk.Label(form, text="Tipo").grid(row=0, column=0, sticky="w", padx=4)
        type_box = ttk.Combobox(form, textvariable=self.service_type, values=("Sala", "Equipo", "Asesoría"), state="readonly", width=18)
        type_box.grid(row=1, column=0, padx=4)
        type_box.bind("<<ComboboxSelected>>", lambda _event: self._update_service_detail_label())
        for column, (key, label) in enumerate((("id", "Código"), ("name", "Nombre"), ("rate", "Tarifa")), start=1):
            ttk.Label(form, text=label).grid(row=0, column=column, sticky="w", padx=4)
            ttk.Entry(form, textvariable=self.service_vars[key], width=20).grid(row=1, column=column, padx=4)
        self.detail_label = ttk.Label(form)
        self.detail_label.grid(row=0, column=4, sticky="w", padx=4)
        ttk.Entry(form, textvariable=self.service_vars["detail"], width=26).grid(row=1, column=4, padx=4)
        ttk.Button(form, text="Crear servicio", command=self.add_service).grid(row=1, column=5, padx=8)
        self._update_service_detail_label()
        self.services_tree = self._tree(self.services_tab, ("Código", "Tipo", "Descripción", "Estado"), (110, 110, 520, 110))

    def _build_reservations(self) -> None:
        form = ttk.LabelFrame(self.reservations_tab, text="Crear reserva", padding=10)
        form.pack(fill="x")
        self.reservation_vars = {key: tk.StringVar() for key in ("id", "client", "service", "duration", "parameter", "discount")}
        fields = (("id", "Código", 0), ("client", "Cliente", 1), ("service", "Servicio", 2), ("duration", "Duración", 3), ("discount", "Descuento 0-1", 5))
        for key, label, column in fields:
            ttk.Label(form, text=label).grid(row=0, column=column, sticky="w", padx=4)
            if key in ("client", "service"):
                widget = ttk.Combobox(form, textvariable=self.reservation_vars[key], state="readonly", width=19)
                setattr(self, f"{key}_box", widget)
                if key == "service":
                    widget.bind("<<ComboboxSelected>>", lambda _event: self._update_reservation_parameter_label())
            else:
                widget = ttk.Entry(form, textvariable=self.reservation_vars[key], width=16)
            widget.grid(row=1, column=column, padx=4)
        self.reservation_parameter_label = ttk.Label(form)
        self.reservation_parameter_label.grid(row=0, column=4, sticky="w", padx=4)
        ttk.Entry(form, textvariable=self.reservation_vars["parameter"], width=16).grid(row=1, column=4, padx=4)
        ttk.Button(form, text="Confirmar reserva", command=self.add_reservation).grid(row=1, column=6, padx=8)
        self.reservations_tree = self._tree(self.reservations_tab, ("Código", "Cliente", "Servicio", "Estado", "Total"), (110, 180, 260, 120, 120))
        actions = ttk.Frame(self.reservations_tab)
        actions.pack(fill="x", pady=8)
        ttk.Button(actions, text="Cancelar reserva seleccionada", command=self.cancel_selected_reservation).pack(side="left")
        ttk.Button(actions, text="Cambiar disponibilidad del servicio", command=self.toggle_selected_service).pack(side="left", padx=8)

    def _tree(self, parent: ttk.Frame, columns: tuple[str, ...], widths: tuple[int, ...]) -> ttk.Treeview:
        container = ttk.Frame(parent)
        container.pack(expand=True, fill="both", pady=12)
        tree = ttk.Treeview(container, columns=columns, show="headings", height=13)
        for name, width in zip(columns, widths):
            tree.heading(name, text=name)
            tree.column(name, width=width, anchor="w")
        scrollbar = ttk.Scrollbar(container, orient="vertical", command=tree.yview)
        tree.configure(yscrollcommand=scrollbar.set)
        tree.pack(side="left", expand=True, fill="both")
        scrollbar.pack(side="right", fill="y")
        return tree

    def _update_service_detail_label(self) -> None:
        labels = {"Sala": "Capacidad y equipos", "Equipo": "Unidades disponibles", "Asesoría": "Especialidad"}
        self.detail_label.config(text=labels[self.service_type.get()])

    def _update_reservation_parameter_label(self) -> None:
        service = self.manager.services.get(self.reservation_vars["service"].get())
        text = "Parámetro"
        if isinstance(service, RoomReservationService):
            text = "Cantidad asistentes"
        elif isinstance(service, EquipmentRentalService):
            text = "Unidades a alquilar"
        self.reservation_parameter_label.config(text=text)

    def _number(self, value: str, field: str, integer: bool = False) -> float | int:
        try:
            number = int(value) if integer else float(value)
        except ValueError as error:
            raise ValidationError(f"{field} debe ser numérico.") from error
        return number

    def _run_operation(self, action, success: str) -> None:
        try:
            action()
        except SoftwareFJError as error:
            self.manager.logger.exception("Error controlado desde la interfaz.")
            messagebox.showerror("Operación no realizada", str(error))
        except Exception as error:  # Defensa final para que la interfaz permanezca activa.
            self.manager.logger.exception("Error inesperado desde la interfaz.")
            messagebox.showerror("Error inesperado", f"Se registró el incidente: {error}")
        else:
            self.refresh_all()
            messagebox.showinfo("Operación exitosa", success)

    def add_client(self) -> None:
        values = self.client_vars
        self._run_operation(lambda: self.manager.register_client(values["id"].get(), values["name"].get(), values["email"].get(), values["phone"].get()), "Cliente registrado correctamente.")

    def add_service(self) -> None:
        values = self.service_vars

        def operation() -> None:
            # La conversión también queda dentro del bloque protegido de la interfaz.
            rate = self._number(values["rate"].get(), "La tarifa")
            detail = values["detail"].get()
            if self.service_type.get() == "Sala":
                parts = detail.split(";", 1)
                capacity = self._number(parts[0], "La capacidad", True)
                equipment = parts[1].strip() if len(parts) > 1 else "Equipamiento básico"
                self.manager.register_room(values["id"].get(), values["name"].get(), rate, capacity, equipment)
            elif self.service_type.get() == "Equipo":
                stock = self._number(detail, "Las unidades", True)
                self.manager.register_equipment(values["id"].get(), values["name"].get(), rate, stock)
            else:
                self.manager.register_consulting(values["id"].get(), values["name"].get(), rate, detail)

        self._run_operation(operation, "Servicio registrado correctamente.")

    def add_reservation(self) -> None:
        values = self.reservation_vars

        def operation() -> None:
            duration = self._number(values["duration"].get(), "La duración")
            discount = self._number(values["discount"].get() or "0", "El descuento")
            service = self.manager.services.get(values["service"].get())
            parameter: dict[str, int] = {}
            if isinstance(service, RoomReservationService):
                parameter["attendees"] = self._number(values["parameter"].get(), "Los asistentes", True)
            elif isinstance(service, EquipmentRentalService):
                parameter["units"] = self._number(values["parameter"].get(), "Las unidades", True)
            self.manager.create_reservation(values["id"].get(), values["client"].get(), values["service"].get(), duration, discount, **parameter)

        self._run_operation(operation, "Reserva confirmada correctamente.")

    def cancel_selected_reservation(self) -> None:
        selected = self.reservations_tree.selection()
        if not selected:
            messagebox.showwarning("Seleccione una reserva", "Elija una reserva de la tabla.")
            return
        code = self.reservations_tree.item(selected[0], "values")[0]
        self._run_operation(lambda: self.manager.cancel_reservation(code), "Reserva cancelada correctamente.")

    def toggle_selected_service(self) -> None:
        selected = self.services_tree.selection()
        if not selected:
            messagebox.showwarning("Seleccione un servicio", "Elija un servicio de la tabla.")
            return
        code = self.services_tree.item(selected[0], "values")[0]
        service = self.manager.services[code]
        new_value = not service.available
        self._run_operation(lambda: self.manager.set_service_availability(code, new_value), "Disponibilidad actualizada.")

    def refresh_all(self) -> None:
        summary = self.manager.summary()
        self.summary_label.config(text=f"Clientes: {summary['clientes']}\nServicios: {summary['servicios']}\nReservas: {summary['reservas']}\nReservas confirmadas: {summary['confirmadas']}")
        self._fill_tree(self.clients_tree, [(c.identifier, c.name, c.email, c.phone) for c in self.manager.clients.values()])
        self._fill_tree(self.services_tree, [(s.identifier, type(s).__name__.replace("Service", ""), s.describe(), "Disponible" if s.available else "No disponible") for s in self.manager.services.values()])
        self._fill_tree(self.reservations_tree, [(r.identifier, r.client.name, r.service.name, r.status.value, f"${r.total:,.0f}") for r in self.manager.reservations.values()])
        self.client_box["values"] = list(self.manager.clients)
        self.service_box["values"] = list(self.manager.services)
        self._update_reservation_parameter_label()

    @staticmethod
    def _fill_tree(tree: ttk.Treeview, rows: list[tuple[object, ...]]) -> None:
        for item in tree.get_children():
            tree.delete(item)
        for row in rows:
            tree.insert("", "end", values=row)
