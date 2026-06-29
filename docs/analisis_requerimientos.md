# Análisis de requerimientos — Software FJ

## Requerimientos funcionales

| Código | Requerimiento | Implementación |
|---|---|---|
| RF-01 | Registrar clientes con datos válidos. | `Client` y `SoftwareFJManager.register_client` |
| RF-02 | Gestionar reservas de salas. | `RoomReservationService` |
| RF-03 | Gestionar alquiler de equipos. | `EquipmentRentalService` |
| RF-04 | Gestionar asesorías especializadas. | `SpecializedConsultingService` |
| RF-05 | Crear, confirmar y cancelar reservas. | `Reservation` |
| RF-06 | Calcular costos con impuesto y descuento. | `Service.calculate_total` |
| RF-07 | Mantener operación ante datos erróneos. | Excepciones, interfaz y `logs/software_fj.log` |

## Modelo de clases

| Clase | Atributos principales | Métodos principales |
|---|---|---|
| `Entity` (abstracta) | `identifier` | propiedad de lectura `identifier` |
| `Client` | `_name`, `_email`, `_phone` | validadores de propiedades |
| `Service` (abstracta) | `_name`, `_base_rate`, `_available` | `calculate_cost`, `validate_parameters`, `describe`, `calculate_total` |
| `RoomReservationService` | `capacity`, `equipment` | cálculo por hora y validación de asistentes |
| `EquipmentRentalService` | `stock` | cálculo por día/unidad y validación de inventario |
| `SpecializedConsultingService` | `specialty` | cálculo por hora y validación de duración |
| `Reservation` | `client`, `service`, `duration`, `parameters`, `status`, `total` | `process`, `cancel` |
| `SoftwareFJManager` | diccionarios de clientes, servicios y reservas | registros y operaciones de negocio |

## Principios POO y estabilidad

- **Abstracción:** `Entity` y `Service` definen contratos generales.
- **Herencia:** los tres servicios especializados derivan de `Service`.
- **Polimorfismo:** una reserva usa el mismo mensaje `calculate_cost`, `validate_parameters` y `describe`, pero cada servicio responde según su tipo.
- **Encapsulamiento:** los datos personales del cliente y los identificadores se controlan mediante propiedades y atributos internos.
- **Variantes de cálculo:** `calculate_total` usa parámetros opcionales para las versiones con impuesto y descuento; Python no tiene sobrecarga por firma nativa.
- **Excepciones:** se usan excepciones personalizadas, `try/except`, `try/except/else/finally`, y encadenamiento de errores. El log conserva los detalles técnicos.

## Casos de prueba secuenciales

`demo_operations.py` ejecuta 13 casos: tres servicios correctos, un servicio inválido, cliente válido e inválido, dos reservas exitosas, reserva con inventario inválido, servicio no disponible, cancelación y una cancelación no permitida. Cada falla se controla y la siguiente operación continúa.
