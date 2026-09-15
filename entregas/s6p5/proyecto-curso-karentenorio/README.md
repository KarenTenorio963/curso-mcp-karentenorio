# Proyecto Curso — Control de Gastos con IA Generativa

Backend de control de gastos personales, construido durante el curso.
Arquitectura: monolito modular + capas + Repository.

Reflexión

Si mañana quisieras agregar un segundo tipo de repository (por ejemplo, uno que guarde los gastos en un archivo JSON en vez de en memoria), ¿qué tendrías que cambiar en services/gastos.py?

Nada. No se tendría que modificar una sola línea de services/gastos.py. Gracias al principio de Inversión de Dependencias (DIP), el servicio solo exige que le pase un objeto que cumpla con el contrato esperado (es decir, que tenga los métodos guardar, listar y total_por_categoria). Para soportar JSON, solo crearía un nuevo archivo como app/repositories/gastos_json.py con esos mismos métodos e inyectaría ese nuevo repositorio al llamar al servicio.

Un compañero te dice: "para ir más rápido, voy a poner la validación del monto directo en el router". Basado en lo que construiste hoy, ¿qué le responderías?

Le respondería que poner la validación en el router viola el Principio de Responsabilidad Única (SRP) y acopla la regla de negocio a la capa de entrada (HTTP). Si mañana el proyecto necesita registrar gastos desde otro medio —como un bot de Telegram, una tarea programada, un script de CLI o un servidor MCP—, habría que duplicar la lógica de validación en cada un lugar. Mantener la validación dentro de la capa de servicios asegura que las reglas de negocio se apliquen siempre, independientemente de quién o desde dónde se llame la función.

Cierre
"Hoy pude probar mi lógica de negocio sin depender de una base de datos real ni usar unittest.mock, gracias a la Inversión de Dependencias (DIP) y al uso de un RepositorioFalso para hacer las pruebas."


Prática 6

Reflexión
Si mañana quisieras cambiar de SQLite a Postgres, ¿qué archivo específico tendrías que tocar? ¿Y qué archivos NO tendrías que tocar?

Únicamente .env (o app/config.py), cambiando la variable de entorno DATABASE_URL para que apunte a la cadena de conexión de PostgreSQL (junto con instalar el driver psycopg2 o asyncpg).
Archivos que NO se tocan: Ningún archivo de la lógica de negocio ni de la API. Gracias al patrón Repository y al ORM (SQLAlchemy), app/repositories/gastos.py, app/services/gastos.py, app/routers/gastos.py y los modelos de datos permanecen exactamente iguales sin cambiar una sola línea de código.

¿Qué pasaría si alguien intentara hacer GET /gastos/ pasando el usuario_id de otra persona en la URL en vez de en el token? ¿Podría ver los gastos de otro usuario, con el código que escribiste hoy?

No podría ver los gastos de otro usuario. El endpoint GET /gastos/ no recibe ningún usuario_id por parámetro o en la URL. La identidad del usuario se extrae obligatoriamente del Bearer Token JWT en el encabezado Authorization a través de la dependencia get_current_user. Como la consulta a la base de datos se filtra internamente usando el id extraído y verificado del token token autenticado, es imposible forzar o suplantar la consulta para ver la información de otra persona.

Cierre 
"Si mañana un atacante consigue mi archivo .env, podría firmar tokens JWT falsos o acceder a la base de datos en el entorno de desarrollo, pero NO podría obtener las contraseñas reales de los usuarios en texto plano, porque las contraseñas no se almacenan directamente, sino procesadas mediante algoritmos de hashing seguro (bcrypt/argon2)."


Práctica 7

Reflexión 
Si conectan el servidor por stdio a un cliente real con varios usuarios distintos: Todos los usuarios compartirían exactamente la misma cuenta demo. Se rompería la privacidad e integridad de los datos, ya que las acciones de cualquier usuario sobreescribirían o listarían los gastos del usuario demo único, al no existir un mecanismo en stdio para transmitir la identidad/token de cada usuario individual.

Lo que tendría que haber estado mal en la arquitectura: Habría existido un acoplamiento directo entre la lógica de negocio y la capa de transporte/interfaz (por ejemplo, recibir objetos Request de FastAPI o depender de contexto de sesión HTTP dentro del servicio). Como services/gastos.py es agnóstico a la interfaz y trabaja solo con tipos de datos nativos e inyecciones de base de datos, la lógica permaneció intacta.

Por qué esa solución no le sirve a stdio y qué tendría que cambiar: stdio es un canal local de entrada/salida estándar sin cabeceras HTTP de solicitud/respuesta para adjuntar un Authorization: Bearer <token>. Para que sirviera, el cliente tendría que enviar el token JWT explícitamente en los parámetros de cada llamada a las herramientas (tools) o el protocolo MCP tendría que soportar un apretón de manos (handshake) de autenticación inicial al abrir el proceso stdio.

Control para evitar duplicados por reintento y su capa: Se implementarían claves de idempotencia (idempotency keys) enviadas desde el cliente/agente por cada transacción. Este control debe ir en la capa de services/, ya que es la encargada de la lógica de negocio y la persistencia; el tool solo se limitaría a recibir dicha clave y delegarla al servicio para verificar si la transacción con ese ID único ya fue procesada.

Cierre 
"Hoy construí una tercera puerta de entrada al mismo backend. Lo que NO tuve que duplicar fue la lógica de negocio y los servicios (services/gastos.py), y eso fue posible gracias a la separación de capas y el diseño desacoplado de la arquitectura (decisión que tomamos en la Sesión 6)."