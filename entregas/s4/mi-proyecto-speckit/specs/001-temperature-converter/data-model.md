# Data Model: Convertidor de Temperatura

**Feature**: `001-temperature-converter`
**Date**: 2026-09-07

## Enums

### `Unit`
Representa las unidades de temperatura soportadas.
- `CELSIUS`: Grados Celsius (`"C"`, `"celsius"`)
- `FAHRENHEIT`: Grados Fahrenheit (`"F"`, `"fahrenheit"`)
- `KELVIN`: Kelvin (`"K"`, `"kelvin"`)

## Entities

### `TemperatureReading`
Representa la magnitud de temperatura de origen.

- **Campos**:
  - `value`: `float` — Valor numérico de la temperatura.
  - `unit`: `Unit` — Unidad en la que está expresada la lectura.
- **Validaciones**:
  - `value` debe ser numérico (`int` o `float`).
  - No puede ser inferior al cero absoluto correspondiente a su unidad:
    - `unit == Unit.KELVIN`: `value >= 0.0`
    - `unit == Unit.CELSIUS`: `value >= -273.15`
    - `unit == Unit.FAHRENHEIT`: `value >= -459.67`

### `ConversionResult`
Representa el resultado procesado de una conversión.

- **Campos**:
  - `original_value`: `float` — Valor original ingresado.
  - `from_unit`: `Unit` — Unidad original.
  - `to_unit`: `Unit` — Unidad resultante.
  - `converted_value`: `float` — Valor convertido redondeado a 3 decimales.
  - `formatted_result`: `str` — Representación en cadena con 3 decimales (ej. `"273.150"`).

## Reglas de Validación y Estados

1. **Rechazo por Cero Absoluto**:
   - Disparador: Lectura con temperatura inferior al mínimo físico de su escala.
   - Efecto: Genera un error descriptivo (ej. `ValueError("La temperatura en Kelvin no puede ser inferior a 0 (cero absoluto).")`).
2. **Identidad**:
   - Disparador: `from_unit == to_unit`.
   - Efecto: El valor resultante es numéricamente igual a `round(value, 3)`.
3. **Entrada no válida**:
   - Disparador: Cadenas vacías, caracteres alfabéticos o formatos no analizables numéricamente.
   - Efecto: Mensaje amigable capturado a nivel de CLI / API sin caída abrupta del programa.
