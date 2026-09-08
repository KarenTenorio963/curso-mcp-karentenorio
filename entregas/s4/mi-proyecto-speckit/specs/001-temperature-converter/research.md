# Research: Convertidor de Temperatura

**Feature**: `001-temperature-converter`
**Date**: 2026-09-07

## Findings and Technical Decisions

### Decision 1: Entorno de ejecución y empaquetado con uv
- **Decision**: Utilizar Python >=3.14 estándar administrado mediante `uv`, definiendo la estructura con paquete `src/mi_proyecto_speckit`.
- **Rationale**: `uv` proporciona una resolución de dependencias rápida, gestión limpia de `.venv` y empaquetado nativo mediante `pyproject.toml` y `uv.lock`.
- **Alternatives considered**: Entornos virtuales manuales con `python -m venv` o `poetry`. Se descartaron porque el requerimiento del usuario pide explícitamente configurar y usar `uv`.

### Decision 2: Arquitectura modular y biblioteca central
- **Decision**: Implementar la lógica matemática en `converter.py` mediante funciones directas y tipos enumerados para las unidades (`Unit.CELSIUS`, `Unit.FAHRENHEIT`, `Unit.KELVIN`).
- **Rationale**: Cumple con el principio Library-First de la constitución: la lógica central es 100% independiente de cualquier framework o interfaz de usuario.
- **Alternatives considered**: Patrón Strategy con jerarquía de clases polimórficas. Se descartó por añadir complejidad innecesaria para 3 escalas bien definidas.

### Decision 3: Formato numérico y redondeo a 3 decimales
- **Decision**: Realizar cálculos intermedios en precisión estándar `float` y redondear el resultado final a 3 cifras decimales mediante `round(resultado, 3)`.
- **Rationale**: Cumple exactamente con el criterio de aceptación de redondeo a 3 decimales prescrito en `spec.md` y `spec_manual.md`.
- **Alternatives considered**: Uso de `decimal.Decimal`. Aunque previene imprecisiones binarias mínimas, para conversiones físicas de temperatura con redondeo a 3 decimales la aritmética con `float` es óptima, estándar y más sencilla.

### Decision 4: Validación de Cero Absoluto
- **Decision**: Validar la temperatura de entrada antes o durante la conversión según los límites físicos conocidos:
  - Kelvin: `< 0` no permitido.
  - Celsius: `< -273.15` no permitido.
  - Fahrenheit: `< -459.67` no permitido.
  Lanzar un `ValueError` descriptivo que indique claramente la violación del límite físico.
- **Rationale**: Protege la integridad física de los cálculos y atiende tanto el criterio de Kelvin < 0 como casos borde de temperaturas físicamente imposibles.
- **Alternatives considered**: Retornar `None` o mensajes silenciosos; se descartó porque las excepciones permiten reportar mensajes de error claros al usuario y a la CLI sin romper la aplicación.

### Decision 5: Framework de pruebas
- **Decision**: Emplear `pytest` configurado bajo el grupo dev de `pyproject.toml` y ejecutado mediante `uv run pytest`.
- **Rationale**: Facilita parametrizar casos de prueba (Given-When-Then de la spec) y verificar casos borde, entradas no numéricas y excepciones de cero absoluto.
- **Alternatives considered**: `unittest` estándar. Se prefirió `pytest` por su claridad en assertions y reportes.
