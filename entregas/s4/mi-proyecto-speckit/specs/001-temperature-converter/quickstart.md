# Quickstart: Convertidor de Temperatura

**Feature**: `001-temperature-converter`
**Date**: 2026-09-07

Guía de verificación rápida para validar la implementación end-to-end.

## Prerrequisitos

- Python >=3.14 instalado en el sistema.
- Gestor `uv` disponible en la terminal.

## Setup del Entorno

1. Sincronizar el entorno virtual y dependencias:
   ```bash
   uv sync
   ```

2. Ejecutar la suite de pruebas unitarias:
   ```bash
   uv run pytest
   ```

## Escenarios de Validación Rápida (CLI)

### 1. Conversión básica Celsius a Fahrenheit
```bash
uv run mi-proyecto-speckit 0 C F
```
- **Resultado esperado**: `32.000`

### 2. Conversión Fahrenheit a Celsius
```bash
uv run mi-proyecto-speckit 212 F C
```
- **Resultado esperado**: `100.000`

### 3. Conversión Celsius a Kelvin
```bash
uv run mi-proyecto-speckit 0 C K
```
- **Resultado esperado**: `273.150`

### 4. Rechazo de Cero Absoluto
```bash
uv run mi-proyecto-speckit -5 K C
```
- **Resultado esperado**: Mensaje descriptivo indicando que Kelvin no puede ser inferior a 0 y finalización con código de error.

### 5. Rechazo de Entrada No Numérica
```bash
uv run mi-proyecto-speckit abc C F
```
- **Resultado esperado**: Mensaje de error amigable indicando que 'abc' no es numérico sin caída no controlada.
