"""Punto de entrada principal del Sistema de Gestión Software FJ.

Estudiante:
- David Santiago Acosta Garcia

Este archivo corrige la condición de entrada principal del programa. La aplicación
solo se abre cuando se ejecuta directamente este módulo, evitando errores al
importarlo desde pruebas u otros archivos.
"""

from app.gui import SoftwareFJApp
from app.manager import SoftwareFJManager


def main() -> None:
    """Inicializa los datos en memoria y abre la interfaz gráfica Tkinter."""
    manager = SoftwareFJManager()
    manager.load_initial_data()
    app = SoftwareFJApp(manager)
    app.mainloop()


if __name__ == "__main__":
    main()
