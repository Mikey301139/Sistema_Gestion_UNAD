"""Punto de entrada de la aplicación.

Integrantes del equipo (reemplazar estos datos antes de entregar):
- [Nombre completo del integrante 1]
- [Nombre completo del integrante 2]
- [Nombre completo del integrante 3]
- [Nombre completo del integrante 4]
- [Nombre completo del integrante 5]
"""

from app.gui import SoftwareFJApp
from app.manager import SoftwareFJManager


def main() -> None:
    """Crea la sesión en memoria, carga ejemplos y abre Tkinter."""
    manager = SoftwareFJManager()
    manager.load_initial_data()
    app = SoftwareFJApp(manager)
    app.mainloop()


# Condición de entrada correcta en Python:
# solo ejecuta la interfaz cuando este archivo se abre directamente.
if __name__ == "__main__":
    main()
