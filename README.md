# Sistema Integral de Gestión - Software FJ

Trabajo individual desarrollado para la Fase 4 del curso de Programación.

## Estudiante

- David Santiago Acosta Garcia

## Descripción del proyecto

Esta aplicación permite gestionar clientes, servicios y reservas para la empresa Software FJ. El sistema fue desarrollado en Python aplicando programación orientada a objetos y utilizando Tkinter para la interfaz gráfica.

La información se maneja en memoria durante la ejecución del programa, es decir, no se usa base de datos. Los eventos y errores controlados se registran en el archivo de log generado por la aplicación.

## Funcionalidades principales

- Registro de clientes con validación de nombre, correo e identificación.
- Creación de servicios de tres tipos:
  - reserva de salas;
  - alquiler de equipos;
  - asesoría especializada.
- Creación y confirmación de reservas.
- Cancelación de reservas.
- Cambio de disponibilidad de servicios.
- Cálculo de costos con impuesto y descuento opcional.
- Manejo de errores mediante excepciones personalizadas.
- Registro de eventos y errores en archivo log.
- Interfaz gráfica desarrollada con Tkinter.
- Demostración secuencial por consola con operaciones válidas e inválidas.

## Conceptos de programación aplicados

El proyecto implementa los principios solicitados en la actividad:

- Abstracción: uso de clases base abstractas para entidades y servicios.
- Herencia: servicios especializados derivados de una clase general `Service`.
- Polimorfismo: cada tipo de servicio calcula y valida su costo de forma diferente.
- Encapsulamiento: atributos protegidos y acceso mediante propiedades.
- Manejo avanzado de excepciones: excepciones propias, bloques `try/except/else/finally` y registro de errores.
- Modularidad: separación entre lógica de negocio, modelos, interfaz y pruebas.

## Estructura del proyecto

```text
.
├── app/
│   ├── exceptions.py
│   ├── gui.py
│   ├── manager.py
│   ├── models.py
│   ├── reservation.py
│   └── services.py
├── docs/
│   ├── analisis_requerimientos.md
│   └── plantilla_informe.md
├── outputs/
│   ├── CORRECCIONES_TUTOR.md
│   └── INSTRUCCIONES_DE_ENTREGA.md
├── tests/
│   └── test_domain.py
├── demo_operations.py
├── main.py
├── README.md
└── .gitignore
```

## Requisitos

- Python 3.10 o superior.
- Tkinter incluido en la instalación estándar de Python para Windows.

No se requieren librerías externas.

## Cómo ejecutar la aplicación gráfica

Abrir PowerShell en la carpeta del proyecto y ejecutar:

```powershell
python main.py
```

Si el comando `python` no funciona, en este equipo se puede usar la ruta directa encontrada:

```powershell
& "C:\Users\USUARIO\AppData\Local\Programs\Python\Python314\python.exe" main.py
```

## Cómo ejecutar la demostración por consola

La demostración ejecuta más de diez operaciones, incluyendo casos correctos y errores controlados:

```powershell
python demo_operations.py
```

O con la ruta directa:

```powershell
& "C:\Users\USUARIO\AppData\Local\Programs\Python\Python314\python.exe" demo_operations.py
```

## Cómo ejecutar las pruebas

```powershell
python -m unittest discover -v
```

O con la ruta directa:

```powershell
& "C:\Users\USUARIO\AppData\Local\Programs\Python\Python314\python.exe" -m unittest discover -v
```

## Evidencia de validación

Durante la revisión se validó:

- ejecución de la demostración por consola;
- ejecución de pruebas unitarias;
- compilación de sintaxis de los archivos Python.

Resultado de pruebas:

```text
Ran 5 tests
OK
```