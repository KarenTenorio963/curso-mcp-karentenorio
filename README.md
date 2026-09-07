\## Clase 2 — APIs de IA Generativa y memoria conversacional

Karen Tenorio



\### Conversación de 8 turnos (Paso 7)



Ver evidencia en `entregas/s02/evidencia/memoria.png`.



\### Por qué elegí ventana deslizante



Se implementó la estrategia de ventana deslizante (`MAX\_TURNS = 10`) porque gestiona el consumo de memoria acotando el historial a las interacciones recientes necesarias para mantener el contexto, evitando un consumo excesivo e indeterminado de tokens en conversaciones extensas.



\### Límite de solicitudes provocado (Paso 9)



Ver evidencia en `entregas/s02/evidencia/rate\_limit.png`.



Se provocaron errores de tasa y servidor (429 y 503) utilizando el modelo `gemini-3.6-flash`. La aplicación ejecutó los reintentos con backoff exponencial mediante la captura explícita de `ClientError` y `ServerError` sin interrumpir la ejecución del script.

