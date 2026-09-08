# Comparación Final: Spec a Mano vs. Spec Kit

## Tabla 1: Comparativa de Aspectos Metodológicos

| Aspecto | Spec a mano | Spec Kit |
|---|---|---|
| **¿Cubrió los mismos casos borde?** | Sí, cubrió los casos contemplados explícitamente en el documento manual (entradas no numéricas, cero absoluto en Kelvin y misma escala). | Cubrió los mismos y además identificó casos borde físicos extra, como rechazar temperaturas en Celsius/Fahrenheit equivalentes a menos de 0 Kelvin (ej. -300°C). |
| **¿Qué generó Spec Kit que tú no habías escrito?** | Documentación básica orientada a lógica directa en un solo archivo de script. | Generó un spec formal en formato BDD (Given-When-Then), arquitectura modular, lista de tareas priorizadas (`tasks.md`), validaciones estrictas y una suite de pruebas unitarias automáticas. |
| **¿Qué se sintió más rápido de arrancar?** | Spec a mano. Es ideal para comenzar de inmediato sin necesidad de instalar CLI ni ejecutar comandos de inicialización. | Spec Kit requiere un par de minutos iniciales para la configuración del entorno (`specify init`) y la ejecución del flujo interactivo. |
| **¿Cuál te generó más confianza en el resultado?** | Genera confianza rápida para prototipos simples, pero depende completamente de la rigurosidad y atención del desarrollador. | Spec Kit. La estructura formal BDD, la separación de responsabilidades y la generación de tests automáticos garantizan un código más robusto y listo para producción. |

---

## Tabla 2: Comparativa de Casos de Prueba Lado a Lado

| Caso | Resultado Spec a mano | Resultado Spec Kit |
|---|---|---|
| **Caso normal (100 C a F)** | `32.0` / `212.0` (redondeado a 2 decimales). | `212.000` (con formato BDD y precisión a 3 decimales). |
| **Caso borde (-5 K a C)** | `Error: La temperatura en Kelvin no puede ser menor a 0.` | `Error: Valor inválido: -5.0 K está por debajo del cero absoluto (mínimo 0 K).` |
| **Caso no contemplado (`abc C F`)** | `Error: El valor ingresado debe ser un número válido.` | `Error: Entrada inválida: 'abc' no es un número válido.` |

---

## Cierre

> "La próxima vez que tenga un proyecto de tamaño **mediano o grande**, elegiría **Spec Kit** porque automatiza la arquitectura, cubre casos borde críticos con el formato BDD y genera la suite de pruebas unitarias que le dan solidez y confianza al código desde el primer momento."
