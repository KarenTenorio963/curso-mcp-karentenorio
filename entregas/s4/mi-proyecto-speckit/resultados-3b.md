\# Resultados - Bloque 3.B (Spec kit)


| Tipo de caso | Entrada probada | Resultado esperado | Resultado obtenido | Estado |
|---|---|---|---|---|
| **Caso normal** | `100 C F` | `212.000` | `212.000` | ✅ Exitoso |
| **Caso borde** | `-5 K C` | Error por estar debajo del cero absoluto | `Error: Valor inválido: -5.0 K está por debajo del cero absoluto (mínimo 0 K).` | ✅ Exitoso |
| **Caso no contemplado** | `abc C F` | Error por entrada no numérica | `Error: Entrada inválida: 'abc' no es un número válido.` | ✅ Manejado |

