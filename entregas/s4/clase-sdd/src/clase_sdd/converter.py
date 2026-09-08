"""Módulo de conversión de temperatura según spec_manual.md."""

from typing import Any, Union

VALID_UNITS = {
    "C": "Celsius",
    "CELSIUS": "Celsius",
    "F": "Fahrenheit",
    "FAHRENHEIT": "Fahrenheit",
    "K": "Kelvin",
    "KELVIN": "Kelvin",
}


def _normalize_unit(unit: str) -> str:
    """Normaliza la unidad de temperatura ingresada."""
    if not isinstance(unit, str):
        raise ValueError(f"Unidad inválida: {unit}. Debe ser una cadena de texto.")
    cleaned = unit.strip().upper()
    if cleaned not in VALID_UNITS:
        raise ValueError(
            f"Escala no válida: '{unit}'. Use Celsius (C), Fahrenheit (F) o Kelvin (K)."
        )
    return VALID_UNITS[cleaned]


def convert_temperature(
    value: Any,
    from_unit: str,
    to_unit: str,
    raise_errors: bool = False,
) -> Union[float, str]:
    """
    Convierte una temperatura entre las escalas Celsius, Fahrenheit y Kelvin.

    Criterios de aceptación y casos borde:
    - Convierte correctamente entre Celsius, Fahrenheit y Kelvin (y viceversa).
    - Redondea el resultado obtenido a exactamente 3 decimales.
    - Rechaza cualquier valor numérico en la escala Kelvin que sea menor a 0 (cero absoluto).
    - Entradas no numéricas (ejemplo: "abc" o vacíos) -> Retorna un mensaje de error claro sin romper la aplicación.
    - Mismo valor de entrada y salida -> Retorna el mismo valor ingresado (redondeado a 3 decimales).
    - Valores negativos válidos en Celsius y Fahrenheit -> Los procesa y convierte correctamente.

    :param value: Valor numérico o texto convertible a número.
    :param from_unit: Unidad de origen ('C', 'F', 'K' o nombre completo).
    :param to_unit: Unidad de destino ('C', 'F', 'K' o nombre completo).
    :param raise_errors: Si es True, lanza ValueError en lugar de retornar el mensaje de error.
    :return: Valor numérico redondeado a 3 decimales o mensaje de error en caso de fallo.
    """
    try:
        # Validación de entradas vacías o None
        if value is None or (isinstance(value, str) and value.strip() == ""):
            raise ValueError("Error: La entrada no puede estar vacía y debe ser un valor numérico.")

        # Validación de entradas no numéricas
        try:
            numeric_val = float(value)
        except (ValueError, TypeError):
            raise ValueError(
                f"Error: Entrada no numérica '{value}'. Debe ingresar un número válido."
            )

        # Normalización de escalas
        source = _normalize_unit(from_unit)
        target = _normalize_unit(to_unit)

        # Rechazo de valores en escala Kelvin menores a 0 (cero absoluto)
        if source == "Kelvin" and numeric_val < 0:
            raise ValueError(
                "Error: Rechazado. La temperatura en escala Kelvin no puede ser menor a 0 (cero absoluto)."
            )

        # Validación física de temperaturas por debajo del cero absoluto
        if source == "Celsius" and numeric_val < -273.15:
            raise ValueError(
                "Error: Rechazado. El valor en Celsius no puede ser menor a -273.15 °C (cero absoluto)."
            )
        if source == "Fahrenheit" and numeric_val < -459.67:
            raise ValueError(
                "Error: Rechazado. El valor en Fahrenheit no puede ser menor a -459.67 °F (cero absoluto)."
            )

        # Caso borde: Misma unidad de entrada y salida
        if source == target:
            return round(numeric_val, 3)

        # Conversión a escala intermedia: Celsius
        if source == "Celsius":
            temp_c = numeric_val
        elif source == "Fahrenheit":
            temp_c = (numeric_val - 32.0) * 5.0 / 9.0
        elif source == "Kelvin":
            temp_c = numeric_val - 273.15

        # Conversión desde Celsius a la unidad destino
        if target == "Celsius":
            result = temp_c
        elif target == "Fahrenheit":
            result = (temp_c * 9.0 / 5.0) + 32.0
        elif target == "Kelvin":
            result = temp_c + 273.15
            if result < 0:
                raise ValueError(
                    "Error: Rechazado. El resultado en escala Kelvin no puede ser menor a 0 (cero absoluto)."
                )

        return round(result, 3)

    except ValueError as e:
        if raise_errors:
            raise
        return str(e)
