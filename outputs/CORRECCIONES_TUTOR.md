# Correcciones aplicadas según observaciones del tutor

Fecha de revisión: 2026-07-02

## 1. Condición de entrada principal

Se revisó y dejó explícita la condición correcta de ejecución:

```python
if __name__ == "__main__":
    main()
```

Esta condición está en `main.py` y permite que la aplicación Tkinter se ejecute
solamente cuando el archivo principal se abre de forma directa.

## 2. Importaciones dinámicas innecesarias

Se eliminó el uso de:

```python
__import__("logging")
```

Ahora `demo_operations.py` usa una importación normal:

```python
import logging
```

Esto mejora legibilidad, mantenimiento y claridad del código.

## 3. Salida por consola más informativa

La demostración secuencial ahora imprime una tabla con:

- número de caso;
- estado de ejecución;
- operación realizada;
- resultado o error controlado.

Esto facilita tomar evidencia y depurar el funcionamiento.

## 4. Documentación con comentarios

Se reforzaron docstrings y comentarios en:

- `main.py`;
- `demo_operations.py`;
- `app/models.py`;
- `app/services.py`;
- `app/reservation.py`;
- `app/manager.py`;
- `app/gui.py`.

Los comentarios explican abstracción, encapsulamiento, polimorfismo, validaciones,
flujo de reservas y manejo de errores.

## 5. Abstracción más clara

La clase `Entity` ahora incluye el método abstracto `display_name`, implementado
por las entidades concretas. Esto hace más evidente el uso de abstracción en el
modelo del sistema.

## 6. Validaciones más robustas

Se corrigieron conversiones numéricas para que errores como asistentes o unidades
con letras se transformen en `ValidationError`, en lugar de errores genéricos de
Python.

## 7. Interfaz más consistente

El botón para cambiar la disponibilidad de servicios quedó ubicado en la pestaña
de Servicios, donde el usuario selecciona el servicio correspondiente.

## 8. Pendiente antes de entregar

Reemplazar los marcadores de integrantes en:

- `main.py`;
- `demo_operations.py`;
- `README.md`.

No se escribieron nombres reales porque deben corresponder a los integrantes del
grupo.
