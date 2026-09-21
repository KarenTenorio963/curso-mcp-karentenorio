### Práctica 8, Sesión 9
### 1. ¿Qué artículo de la constitución tuviste que "defender" activamente durante `/speckit-implement`?
El **Artículo IV.4 (Autorización e Invariant de Usuario)** y el **Artículo VI.4 (Manejo de Identidad en MCP)**. Durante la implementación, es habitual que los agentes o el código generado tiendan a aceptar el `usuario_id` como un parámetro explicito en los endpoints REST o a asumir un usuario demo de manera global por simplicidad. Se tuvo que corregir esto activamente para asegurar que el `usuario_id` provenga de forma estricta e incondicional del token JWT autenticado mediante `get_current_user`, garantizando el aislamiento completo de los datos.

### 2. Comparación de tiempo: Spec-Driven Development vs. Código a mano (Sesiones 6-8)
El tiempo total utilizado hoy se invirtió predominantemente en la fase de **pensamiento, definición de contratos y aclaración de reglas** (`constitution.md`, `spec.md` y `plan.md`), a diferencia de las Sesiones 6-8 donde la mayor parte del tiempo se fue escribiendo y depurando código manualmente. 
Al definir de forma inequívoca el comportamiento y los contratos en la especificación, la generación e implementación del código fue prácticamente inmediata y libre de errores de arquitectura. El esfuerzo se desplazó del "cómo codificar" al "qué especificar".

### 3. Impacto del umbral explícito de cobertura (Artículo VII.3)
Sí, completamente. Sin una regla constitucional escrita que fije un umbral del 90% para `services/` y un 80% global con verificación estricta via `pytest-cov`, el agente se habría detenido tras generar los flujos básicos (alrededor de un 50%-60% de cobertura) dando la tarea por "completada" sin validar los escenarios de borde, los errores de autenticación (401) ni el aislamiento de identificadores ajenos.

---

> "Hoy la especificación reemplazó al código como fuente de verdad. Lo comprobé cuando **los tests de compatibilidad de las sesiones anteriores y las reglas de negocio pasaron en verde al primer intento tras seguir las firmas fijadas en el spec**, y el artículo de la constitución que más me costó defender fue **el Artículo IV.4 sobre la extracción estricta del usuario desde el JWT sin aceptar IDs externos**."