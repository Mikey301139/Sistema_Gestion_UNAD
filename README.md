# Sistema de Gestión Software FJ - UNAD

Trabajo individual desarrollado para la Fase 4 del curso de Programación.

## Estudiante

- David Santiago Acosta Garcia

## Descripción

Aplicación de escritorio desarrollada en Python con Tkinter para gestionar clientes, servicios y reservas de la empresa Software FJ. El sistema trabaja en memoria, sin base de datos, y registra eventos y errores en archivos de log.

## Correcciones realizadas según observación del tutor

Se aplicaron correcciones concretas de calidad y ejecución:

- Se corrigió y verificó la condición de entrada principal:

```python
if __name__ == "__main__":
    main()
```

- Se eliminaron importaciones dinámicas innecesarias como `__import__(...)`.
- Se mejoró la salida por consola de `demo_operations.py` con formato tabular.
- Se agregaron estados claros para cada operación: `OK`, `CONTROLADO` y `ERROR`.
- Se agregó resumen final de clientes, servicios y reservas.
- Se reforzó la documentación interna mediante comentarios y docstrings.
- Se mantuvo separación modular entre interfaz, lógica de negocio, modelos, reservas, servicios, excepciones y pruebas.

## Funcionalidades

- Registro validado de clientes.
- Creación de servicios de reserva de salas.
- Creación de servicios de alquiler de equipos.
- Creación de servicios de asesoría especializada.
- Confirmación de reservas.
- Cancelación de reservas.
- Cambio de disponibilidad de servicios.
- Cálculo de costos con impuesto y descuento opcional.
- Manejo de excepciones personalizadas.
- Registro de eventos y errores en `logs/software_fj.log`.
- Interfaz gráfica con Tkinter.
- Simulación secuencial por consola.

## Principios de programación orientada a objetos

- Abstracción: clases base para entidades y servicios.
- Herencia: servicios especializados derivados de `Service`.
- Polimorfismo: cada servicio valida y calcula costos de forma diferente.
- Encapsulamiento: atributos protegidos y acceso mediante propiedades.
- Excepciones: errores personalizados y controlados.
- Modularidad: archivos separados por responsabilidad.

## Estructura

```text
Sistema_Gestion_UNAD/
├── app/
│   ├── exceptions.py
│   ├── gui.py
│   ├── manager.py
│   ├── models.py
│   ├── reservation.py
│   └── services.py
├── docs/
├── logs/
├── outputs/
├── tests/
├── demo_operations.py
├── main.py
├── README.md
└── .gitignore
```

## Requisitos

- Python 3.10 o superior.
- Tkinter incluido con Python.

No se requieren librerías externas.

## Ejecutar la interfaz gráfica

Desde PowerShell, dentro de la carpeta del proyecto:

```powershell
python main.py
```

Si el comando `python` no funciona, usar la ruta directa encontrada en este equipo:

```powershell
& "C:\Users\USUARIO\AppData\Local\Programs\Python\Python314\python.exe" main.py
```

## Ejecutar demostración por consola

```powershell
python demo_operations.py
```

O con ruta directa:

```powershell
& "C:\Users\USUARIO\AppData\Local\Programs\Python\Python314\python.exe" demo_operations.py
```

## Ejecutar pruebas

```powershell
python -m unittest discover -v
```

O con ruta directa:

```powershell
& "C:\Users\USUARIO\AppData\Local\Programs\Python\Python314\python.exe" -m unittest discover -v
```

## GitHub individual

Para subir el proyecto a un repositorio personal:

```powershell
git init
git add .
git commit -m "Entrega fase 4 sistema gestion Software FJ"
git branch -M main
git remote add origin https://github.com/USUARIO/NOMBRE_REPOSITORIO.git
git push -u origin main
```

## Nota

Antes de entregar, verificar que `main.py`, `demo_operations.py` y las pruebas funcionen correctamente. También incluir el enlace del repositorio GitHub en el informe final.
