\# Resultados - Bloque 3.A (Spec a mano)



| Tipo de caso | Entrada probada | Resultado esperado | Resultado obtenido | Estado |

|---|---|---|---|---|

| \*\*Caso normal\*\* | `0°C` a `Fahrenheit` | `32.0` | `32.0` | ✅ Exitoso |

| \*\*Caso borde\*\* | `-5 Kelvin` a `Celsius` | Mensaje de error (Kelvin < 0) | `Error: La temperatura en Kelvin no puede ser menor a 0.` | ✅ Exitoso |

| \*\*Caso no contemplado\*\* | `100 Rankine` a `Celsius` | Mensaje de error de escala no soportada | `Error: Escala origen 'Rankine' no soportada.` | ✅ Manejado de forma segura |

