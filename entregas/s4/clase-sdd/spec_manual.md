# Spec Manual — Conversor de Temperatura - Karen Tenorio

## Objetivo

Convertir una temperatura entre las escalas Celsius, Fahrenheit y Kelvin.

## Criterios de aceptación

- [x] Convierte correctamente de Celsius a Fahrenheit y viceversa.

- [x] Convierte correctamente de Celsius a Kelvin y viceversa.

- [x] Convierte correctamente de Fahrenheit a Kelvin y viceversa.

- [x] Redondea el resultado obtenido a exactamente 3 decimales.

- [x] Rechaza cualquier valor numérico en la escala Kelvin que sea menor a 0 (cero absoluto).

## Casos borde

- Entradas no numéricas (ejemplo: "abc" o vacíos) → Debe retornar un mensaje de error claro sin romper la aplicación.

- Mismo valor de entrada y salida (ejemplo: Celsius a Celsius) → Debe retornar el mismo valor ingresado.

- Valores negativos válidos en Celsius y Fahrenheit → Debe procesarlos y convertirlos correctamente.
