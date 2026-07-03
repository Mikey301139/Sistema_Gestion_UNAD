# Entrega preparada — Fase 4, Programación 213023

El proyecto funcional se encuentra en la carpeta principal del espacio de trabajo. Antes de entregarlo:

1. Reemplacen los cinco marcadores de integrantes en `main.py`, `demo_operations.py` y `README.md`.
2. Ejecuten `python main.py` para mostrar la interfaz Tkinter.
3. Ejecuten `python demo_operations.py` y tomen una captura de la evidencia de las 13 operaciones.
4. Ejecuten `python -m unittest discover -v` y tomen una captura de las pruebas.
5. Suban el proyecto a GitHub, agreguen a todos los integrantes como colaboradores y peguen el enlace en `docs/plantilla_informe.md`.
6. Completen la portada, conclusiones y participación real de cada integrante; luego exporten la plantilla como PDF.

La aplicación no usa base de datos. Los eventos y errores se guardan durante la ejecución en `logs/software_fj.log`.

## Nota de validación en este equipo

El comando `python` no está disponible en la variable PATH, pero se encontró un
intérprete instalado en:

```powershell
C:\Users\USUARIO\AppData\Local\Programs\Python\Python314\python.exe
```

Con esa ruta se validó correctamente:

```powershell
& "C:\Users\USUARIO\AppData\Local\Programs\Python\Python314\python.exe" demo_operations.py
& "C:\Users\USUARIO\AppData\Local\Programs\Python\Python314\python.exe" -m unittest discover -v
& "C:\Users\USUARIO\AppData\Local\Programs\Python\Python314\python.exe" -m compileall .
```

Resultado: las 5 pruebas unitarias pasaron y la compilación de sintaxis terminó
sin errores.
