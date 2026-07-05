# Instrucciones de entrega - Trabajo individual

Proyecto ubicado en:

`C:\Users\USUARIO\Desktop\Sistema_Gestion_UNAD`

## Estudiante

- David Santiago Acosta Garcia

## Antes de entregar

1. Abrir la carpeta `Sistema_Gestion_UNAD` en Visual Studio Code.
2. Ejecutar la interfaz gráfica:

```powershell
& "C:\Users\USUARIO\AppData\Local\Programs\Python\Python314\python.exe" main.py
```

3. Ejecutar la demostración por consola y tomar captura:

```powershell
& "C:\Users\USUARIO\AppData\Local\Programs\Python\Python314\python.exe" demo_operations.py
```

4. Ejecutar las pruebas unitarias y tomar captura:

```powershell
& "C:\Users\USUARIO\AppData\Local\Programs\Python\Python314\python.exe" -m unittest discover -v
```

5. Subir el proyecto a GitHub personal.
6. Copiar el enlace del repositorio en el informe final.
7. Exportar el informe como PDF.

## Validación realizada

Se validó directamente desde la carpeta del Escritorio:

- `demo_operations.py`: ejecución correcta con 13 operaciones.
- `python -m unittest discover -v`: 5 pruebas aprobadas.
- `python -m compileall .`: compilación sin errores de sintaxis.

## Correcciones importantes

- Entrada principal corregida en `main.py`.
- Eliminadas importaciones dinámicas innecesarias.
- Salida de consola mejorada en formato tabular.
- README actualizado para trabajo individual.
- Informe de correcciones agregado en `outputs/CORRECCIONES_TUTOR.md`.