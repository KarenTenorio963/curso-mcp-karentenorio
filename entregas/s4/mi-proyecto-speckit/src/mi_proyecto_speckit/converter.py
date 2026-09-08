from enum import Enum
from typing import Union


class Unit(str, Enum):
    CELSIUS = "C"
    FAHRENHEIT = "F"
    KELVIN = "K"

    @classmethod
    def from_string(cls, value: str) -> "Unit":
        cleaned = value.strip().upper()
        if cleaned in ("C", "CELSIUS", "CENTIGRADO", "CENTIGRADOS"):
            return cls.CELSIUS
        if cleaned in ("F", "FAHRENHEIT"):
            return cls.FAHRENHEIT
        if cleaned in ("K", "KELVIN"):
            return cls.KELVIN
        raise ValueError(f"Unidad no reconocida: '{value}'. Use C, F o K.")


class AbsoluteZeroError(ValueError):
    """Error lanzado cuando la temperatura es menor al cero absoluto."""
    pass


def round_result(val: float) -> float:
    """Redondea un número a 3 lugares decimales."""
    return round(val, 3)


def format_result(val: float) -> str:
    """Retorna el número formateado con exactamente 3 decimales."""
    return f"{round_result(val):.3f}"


def _validate_absolute_zero(value: float, unit: Unit) -> None:
    """Valida que el valor no se encuentre por debajo del cero absoluto."""
    if unit == Unit.KELVIN and value < 0.0:
        raise AbsoluteZeroError(
            f"Valor inválido: {value} K está por debajo del cero absoluto (mínimo 0 K)."
        )
    if unit == Unit.CELSIUS and value < -273.15:
        raise AbsoluteZeroError(
            f"Valor inválido: {value} °C está por debajo del cero absoluto (mínimo -273.15 °C)."
        )
    if unit == Unit.FAHRENHEIT and value < -459.67:
        raise AbsoluteZeroError(
            f"Valor inválido: {value} °F está por debajo del cero absoluto (mínimo -459.67 °F)."
        )


def convert_temperature(
    value: Union[float, int, str],
    from_unit: Union[str, Unit],
    to_unit: Union[str, Unit],
) -> float:
    """
    Convierte un valor de temperatura entre Celsius, Fahrenheit y Kelvin.
    """
    # Validación de entrada numérica
    try:
        numeric_value = float(value)
    except (ValueError, TypeError):
        raise ValueError(f"Entrada inválida: '{value}' no es un número válido.")

    src = from_unit if isinstance(from_unit, Unit) else Unit.from_string(str(from_unit))
    dst = to_unit if isinstance(to_unit, Unit) else Unit.from_string(str(to_unit))

    # Validación de cero absoluto sobre la unidad de origen
    _validate_absolute_zero(numeric_value, src)

    # Conversión a escala común intermedia (Celsius)
    if src == Unit.CELSIUS:
        celsius = numeric_value
    elif src == Unit.FAHRENHEIT:
        celsius = (numeric_value - 32.0) * 5.0 / 9.0
    elif src == Unit.KELVIN:
        celsius = numeric_value - 273.15
    else:
        raise ValueError(f"Unidad no soportada: {src}")

    # Conversión desde Celsius a la unidad destino
    if dst == Unit.CELSIUS:
        res = celsius
    elif dst == Unit.FAHRENHEIT:
        res = (celsius * 9.0 / 5.0) + 32.0
    elif dst == Unit.KELVIN:
        res = celsius + 273.15
    else:
        raise ValueError(f"Unidad no soportada: {dst}")

    return round_result(res)


