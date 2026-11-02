# Research: Resumen y salida del documento

## Decision 1: Mantener la arquitectura actual de dos capas

**Decision**: La feature se implementa sobre la arquitectura actual: Vue 3 + TypeScript en `frontend/` y FastAPI en `backend/`, sin sustituir ni recrear ninguno de los dos elementos.

**Rationale**: La especificación actual y la constitución de la app protegen el stack usado en app2. El frontend ya gestiona la autenticación con Clerk, la extracción de archivos, la configuración de resumen y la exportación local; el backend ya valida el token y construye el prompt a OpenRouter. Cambiar de framework introduciría un riesgo de reescritura no justificado.

**Alternatives considered**:

- Reescribir el frontend en otra tecnología: rechazado porque rompe la constitución y la estructura actual.
- Mover la lógica de IA al frontend: rechazado porque la clave de OpenRouter y el control de sesión deben estar en el backend.

## Decision 2: Usar una única petición autenticada a `/resumir`

**Decision**: El frontend debe obtener el token actual de Clerk y enviarlo como `Authorization: Bearer <token>` a `POST /resumir` con el JSON de entrada (`text`, `main_ideas`, `glossary`, `summary_length`).

**Rationale**: El backend ya valida la sesión antes de procesar el contenido y el flujo de la interfaz depende de obtener el token justo antes del envío. Esto mantiene el punto de acceso autenticado y evita depender de sesiones en el frontend.

**Alternatives considered**:

- Enviar el texto sin token: rechazado por la seguridad y por la validación del backend.
- Guardar el resumen en almacenamiento local: rechazado por la limitación funcional de la práctica.

## Decision 3: Mantener el contrato de salida estructurado y opcional

**Decision**: El backend devuelve un JSON con `summary` y, opcionalmente, `main_ideas` y `glossary` según la solicitud. La GUI renderiza esos bloques de forma separada y los botones de copia/exportación actúan sobre cada sección visible.

**Rationale**: El modelo de datos definido en `backend/models.py` y el tipo `Summary` en `frontend/src/types/types.ts` ya reflejan este diseño, y la especificación limita el alcance a ese resultado estructurado.

**Alternatives considered**:

- Un único string con todo el contenido: rechazado porque la interfaz actual ya necesita secciones diferenciadas.
- Añadir persistencia del resultado: rechazado por la constitución.

## Decision 4: Validación de entrada en el navegador y en el backend

**Decision**: El frontend valida tipo y tamaño del archivo local (`.txt` o `.md`, máximo 1 MB en la interfaz) y el backend valida longitud máxima de texto (`max_length=5000`) y el esquema del payload con Pydantic.

**Rationale**: La carga local solo se usa para llenar el área de texto del formulario; el archivo nunca se envía al servidor. El backend conserva la validación de límites y tipos de campos.

**Alternatives considered**:

- Cargar el archivo como blob o base64 hacia el backend: rechazado porque la práctica y la constitución exigen que el archivo se lea localmente y no se envíe como archivo.
- Eliminar validación de tamaño: rechazado porque la especificación y el backend ya la imponen.

## Decision 5: Tratamiento de errores y seguridad del flujo

**Decision**: La app mantiene mensajes de error específicos para autenticación inválida (401), indisponibilidad del verificador de sesión (503), problema con OpenRouter (502/504) y respuesta inválida del proveedor. Ninguno de estos estados debe reintentar el envío automáticamente.

**Rationale**: La feature requiere mensajes comprensibles y flujo controlado. El backend y la UI ya implementan estos caminos; es más seguro mantener el patrón actual que introducir reintentos heurísticos.

**Alternatives considered**:

- Reintentos automáticos con backoff: rechazado porque la constitución pide no reintentar por defecto cuando hay sesión inválida o proveedor no disponible.
- Exponer mensajes técnicos internos: rechazado por privacidad y buenas prácticas.

## Outstanding questions

No quedan necesidades de aclaración bloqueantes para el diseño. La información restante necesaria para la implementación pasa a través de los contratos y el quickstart de esta feature.
