# Interface Contracts: Convertidor de Temperatura

**Feature**: `001-temperature-converter`
**Date**: 2026-09-07

## 1. Python Library Contract (`converter.py`)

### Enumeración `Unit`
```python
from enum import Enum

class Unit(str, Enum):
    CELSIUS = "C"
    FAHRENHEIT = "F"
    KELVIN = "K"
```

### Función Principal `convert_temperature`
```python
def convert_temperature(value: float, from_unit: str | Unit, to_unit: str | Unit) -> float:
    """
    Convierte un valor de temperatura entre Celsius, Fahrenheit y Kelvin.
    
    Args:
        value: Magnitud numérica a convertir.
        from_unit: Unidad de origen ('C', 'F', 'K' o nombres completos sin distinción de mayúsculas).
        to_unit: Unidad de destino ('C', 'F', 'K' o nombres completos sin distinción de mayúsculas).
        
    Returns:
        float: Valor convertido redondeado a exactamente 3 lugares decimales.
        
    Raises:
        ValueError: Si la unidad no es reconocida, si el valor es menor al cero absoluto,
                    o si la entrada no es un valor numérico convertible.
    """
```

### Función Auxiliar `format_conversion`
```python
def format_conversion(value: float, from_unit: str | Unit, to_unit: str | Unit) -> str:
    """Retorna el resultado formateado a 3 decimales como cadena (ej. '273.150')."""
```

---

## 2. CLI Contract (`cli.py` / `main`)

### Invocación mediante comando
```bash
uv run mi-proyecto-speckit <valor> <origen> <destino>
```
O de forma interactiva si se ejecuta sin argumentos:
```bash
uv run mi-proyecto-speckit
```

### Ejemplos de Salida Exitosa:
- Comando: `uv run mi-proyecto-speckit 0 C F`
  - Salida stdout: `32.000`
- Comando: `uv run mi-proyecto-speckit 100 C K`
  - Salida stdout: `373.150`
- Salida de error (cero absoluto): `uv run mi-proyecto-speckit -5 K C`
  - Salida stderr: `Error: La temperatura en Kelvin no puede ser inferior a 0 (cero absoluto).`
  - Código de salida: `1`
- Salida de error (no numérico): `uv run mi-proyecto-speckit abc C F`
  - Salida stderr: `Error: El valor 'abc' no es un número válido.`
  - Código de salida: `1`
