"""Punto de entrada de la aplicación.

Integrantes del equipo (reemplazar antes de entregar):
- David Santiago Acosta Garcia
"""

from app.gui import SoftwareFJApp
from app.manager import SoftwareFJManager


def main() -> None:
    """Crea la sesión en memoria, carga ejemplos y abre Tkinter."""
    manager = SoftwareFJManager()
    manager.load_initial_data()
    app = SoftwareFJApp(manager)
    app.mainloop()


if __name__ == "__main__":
    main()
    