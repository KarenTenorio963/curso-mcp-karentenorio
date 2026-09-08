# Feature Specification: Convertidor de Temperatura

**Feature Branch**: `001-temperature-converter`

**Created**: 2026-09-07

**Status**: Draft

**Input**: User description: "Implementa convertidor de unidades de temperatura siguiendo esta spec: @spec_manual.md . Ayudame configurando el tema de python con uv"

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Conversión entre Celsius y Fahrenheit (Priority: P1)

Como usuario, quiero convertir valores de temperatura entre grados Celsius y Fahrenheit (en ambos sentidos), redondeados con precisión a 3 decimales, para realizar equivalencias comunes de temperatura de forma confiable.

**Why this priority**: Es la conversión más habitual en aplicaciones cotidianas y científicas, constituyendo el MVP funcional básico del convertidor.

**Independent Test**: Puede probarse de forma independiente ingresando valores en Celsius y verificando la salida esperada en Fahrenheit (y viceversa), corroborando que el resultado numérico incluya 3 decimales.

**Acceptance Scenarios**:

1. **Given** un valor en Celsius de `0.0`, **When** se solicita la conversión a Fahrenheit, **Then** el resultado es `32.000`.
2. **Given** un valor en Fahrenheit de `212.0`, **When** se solicita la conversión a Celsius, **Then** el resultado es `100.000`.
3. **Given** un valor en Celsius de `37.0`, **When** se solicita la conversión a Fahrenheit, **Then** el resultado es `98.600`.

---

### User Story 2 - Conversión con Kelvin y Validación de Cero Absoluto (Priority: P2)

Como usuario técnico o científico, quiero convertir temperaturas entre Kelvin, Celsius y Fahrenheit, garantizando que no se permitan temperaturas por debajo del cero absoluto (0 Kelvin), para mantener la validez física de los cálculos.

**Why this priority**: Complementa el rango de escalas estándar y previene datos físicamente imposibles en cálculos científicos.

**Independent Test**: Puede probarse de forma independiente ejecutando conversiones directas e inversas de Kelvin con Celsius y Fahrenheit, comprobando tanto los valores numéricos como el rechazo explícito cuando Kelvin es menor a 0.

**Acceptance Scenarios**:

1. **Given** un valor en Celsius de `0.0`, **When** se convierte a Kelvin, **Then** el resultado es `273.150`.
2. **Given** un valor en Kelvin de `373.15`, **When** se convierte a Celsius, **Then** el resultado es `100.000`.
3. **Given** un valor en Fahrenheit de `32.0`, **When** se convierte a Kelvin, **Then** el resultado es `273.150`.
4. **Given** un valor numérico en Kelvin menor a `0` (ejemplo: `-1.0`), **When** se intenta procesar la conversión, **Then** el sistema rechaza la operación informando que los valores en Kelvin no pueden ser inferiores al cero absoluto.
5. **Given** un valor en Celsius o Fahrenheit equivalente a menos de `0 Kelvin` (ejemplo: `-300 °C`), **When** se intenta convertir, **Then** el sistema rechaza la operación indicando que está por debajo del cero absoluto.

---

### User Story 3 - Manejo de Identidad y Entradas No Numéricas (Priority: P3)

Como usuario, quiero que la aplicación maneje conversiones sobre la misma escala retornando el mismo valor, y que ante entradas inválidas o no numéricas reporte un mensaje claro y comprensible sin fallos inesperados.

**Why this priority**: Asegura la robustez operativa de la herramienta y una experiencia de usuario clara frente a errores típicos de entrada.

**Independent Test**: Probar con la misma escala origen y destino (ej. Celsius a Celsius) y con entradas como texto o cadenas vacías, verificando mensajes de error comprensibles.

**Acceptance Scenarios**:

1. **Given** un valor numérico de `25.5` con escala origen Celsius y destino Celsius, **When** se procesa la conversión, **Then** el resultado es `25.500`.
2. **Given** una entrada no numérica como `"abc"` o una cadena vacía, **When** se solicita la conversión, **Then** el sistema responde con un mensaje de error descriptivo sin terminar abruptamente el proceso.
3. **Given** valores negativos válidos en Celsius o Fahrenheit (por encima del cero absoluto, ej. `-40`), **When** se solicita la conversión mutua, **Then** el resultado es `-40.000`.

---

### Edge Cases

- **Cero Absoluto exacto**: Entrada de `0 K` debe ser procesada correctamente (retornando `-273.150 °C` y `-459.670 °F`).
- **Punto de corte común**: `-40 °C` debe equivaler exactamente a `-40.000 °F`.
- **Entradas con espacios en blanco o formatos con coma/punto**: El sistema debe manejar o reportar limpiamente entradas con formato numérico incorrecto.
- **Redondeo exacto a 3 decimales**: Valores con decimales continuos deben truncarse/redondearse consistentemente a 3 cifras decimales.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: El sistema DEBE convertir valores de temperatura entre las escalas Celsius, Fahrenheit y Kelvin en todas las combinaciones posibles (Celsius ↔ Fahrenheit, Celsius ↔ Kelvin, Fahrenheit ↔ Kelvin).
- **FR-002**: El sistema DEBE redondear los resultados numéricos obtenidos a exactamente 3 lugares decimales.
- **FR-003**: El sistema DEBE rechazar cualquier valor de temperatura que se encuentre por debajo del cero absoluto (`0 K`, `-273.15 °C`, `-459.67 °F`), emitiendo un mensaje claro de error de validación.
- **FR-004**: El sistema DEBE validar las entradas del usuario y rechazar entradas no numéricas o vacías mediante un mensaje de error claro y amigable, sin interrumpir abruptamente la ejecución.
- **FR-005**: El sistema DEBE permitir conversiones donde la escala de origen y destino sean idénticas, retornando el valor proporcionado formateado a 3 decimales.
- **FR-006**: El sistema DEBE soportar valores de temperatura negativos siempre y cuando sean mayores o iguales al cero absoluto.

### Key Entities

- **TemperatureReading**: Representa una magnitud de temperatura, compuesta por un valor numérico escalar y su unidad/escala asociada (`Celsius`, `Fahrenheit`, `Kelvin`).
- **ConversionResult**: Representa el resultado exitoso de una conversión, conteniendo el valor convertido formateado a 3 decimales y la unidad de destino.
- **ValidationError**: Información descriptiva cuando una entrada no cumple con el formato numérico o infringe los límites físicos del cero absoluto.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: El 100% de las conversiones entre escalas válidas se calculan con una exactitud consistente con el redondeo a 3 decimales.
- **SC-002**: El 100% de los intentos de ingresar temperaturas por debajo de 0 Kelvin son rechazados con un mensaje explicativo claro.
- **SC-003**: El 100% de las entradas no numéricas o vacías son interceptadas y reportadas sin causar excepciones no controladas.
- **SC-004**: Cualquier usuario puede completar una conversión y obtener su respuesta en menos de 1 segundo.

## Assumptions

- Las tres escalas soportadas son exclusivamente Celsius (`C`), Fahrenheit (`F`) y Kelvin (`K`).
- La constante estándar adoptada para el cero absoluto en Celsius es `-273.15 °C` y en Fahrenheit es `-459.67 °F`.
- La regla de redondeo es estándar (aritmética a 3 lugares decimales).
- El entorno de ejecución del proyecto es Python administrado a través del gestor `uv`.
