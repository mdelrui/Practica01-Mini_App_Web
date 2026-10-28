# Feature Specification: Resumen y salida del documento

**Feature Branch**: `[002-summary-features]`

**Created**: 2026-10-28

**Status**: Draft

**Input**: User description: "Analiza el proyecto existente y documenta sus requisitos a partir de su implementación actual. La aplicación es un resumidor de textos desarrollado con Vue 3, TypeScript, Vite y FastAPI, que utiliza OpenRouter para generar los resultados. Antes de proponer cambios, inspecciona el código existente. Identifica el flujo completo desde el formulario hasta la respuesta de la API. Define únicamente las funcionalidades que estén realmente implementadas, incluyendo las opciones de longitud del resumen, extracción opcional de ideas principales, glosario, copia al portapapeles de texto generado y exportación, si están presentes en el código. Genera una especificación con requisitos funcionales verificables, criterios de aceptación y tratamiento de errores. No modifiques el código ni añadas funcionalidades durante esta fase. Si encuentras información que no puedas confirmar en el código, indícala como pendiente de verificar."

## User Scenarios & Testing _(mandatory)_

### User Story 1 - Enviar texto para resumir desde la interfaz actual (Priority: P1)

Una persona usuaria abre la SPA, escribe o pega un texto, o carga un archivo `.txt` o `.md` desde su equipo. Puede configurar la longitud del resumen, activar la extracción de ideas principales y activar la generación de glosario. Cuando confirma el formulario, el frontend obtiene el token actual de sesión de Clerk y envía la solicitud al backend para procesar el contenido.

**Why this priority**: Este es el flujo principal de valor de la aplicación: convertir un texto de entrada en una respuesta estructurada sin navegar a otra pantalla ni salir del formulario principal.

**Independent Test**: Probar una sesión autenticada con texto válido y comprobar que la petición incluye el texto, las opciones seleccionadas y la cabecera `Authorization: Bearer` antes de que el backend procese la solicitud.

**Acceptance Scenarios**:

1. **Given** que la persona usuaria tiene la pantalla principal visible y una sesión autenticada, **When** escribe un texto o arrastra un archivo `.txt` o `.md`, **Then** el contenido se carga en el formulario y no se envía al servidor hasta que se confirma el envío.
2. **Given** que la persona usuaria selecciona una longitud de resumen, **When** confirma el envío, **Then** el formulario incluye esa configuración en la petición a la API.
3. **Given** que la persona usuaria activa la extracción de ideas principales y/o el glosario, **When** se envía la solicitud, **Then** estos toggles se transmiten junto con el texto y se esperan en la respuesta del backend.
4. **Given** que el usuario está autenticado, **When** la petición llega al backend, **Then** el token vigente se envía en la cabecera `Authorization` y la app continúa con el procesamiento del resumen.

---

### User Story 2 - Ver resultados segmentados en la pantalla (Priority: P1)

Una vez recibido el resultado, la SPA muestra en la misma pantalla el resumen principal, la lista de ideas principales y el glosario si han sido solicitados. La longitud elegida se refleja en el texto de etiqueta del resultado y la interfaz permite copiar las secciones individuales al portapapeles.

**Why this priority**: La aplicación no solo genera un resumen, sino que ofrece una salida estructurada con distintos bloques de información para facilitar su uso.

**Independent Test**: Simular una respuesta de backend con `summary`, `mainIdeas` y `glossary`, renderizar la pantalla y comprobar que cada bloque aparece en su sección, con su botón de copia asociado.

**Acceptance Scenarios**:

1. **Given** que el backend responde con un resumen válido, **When** se procesa la respuesta, **Then** la sección de resumen se muestra en la pantalla con el contenido generado.
2. **Given** que `mainIdeas` está presente en la respuesta, **When** se renderiza el resultado, **Then** se visualiza la lista de ideas principales con numeración.
3. **Given** que `glossary` está presente en la respuesta, **When** se renderiza el resultado, **Then** se visualiza el glosario con cada concepto y su definición.
4. **Given** que la persona usuaria pulsa el botón de copia de una sección, **When** el navegador permite el acceso al portapapeles, **Then** se copia el contenido visible de esa sección y el botón muestra el estado de copiado.

---

### User Story 3 - Exportación local del resultado y tratamiento de errores (Priority: P2)

La persona usuaria puede exportar el contenido generado como archivo de texto o Markdown desde el navegador, sin que el backend realice esta acción. Si la sesión no es válida, la llamada falla por autenticación, o el proveedor de IA no está disponible, la interfaz presenta un mensaje de error comprensible y mantiene el flujo sin ejecutar más procesamiento.

**Why this priority**: La exportación local aporta utilidad práctica al resultado, y la gestión de errores evita que el usuario reciba un estado ambiguo o que la aplicación continúe con un flujo inválido.

**Independent Test**: Generar una respuesta con resumen válido, pulsar exportación en TXT y MD y comprobar la descarga del archivo; además, simular 401/503 y comprobar que la pantalla muestra el mensaje correcto.

**Acceptance Scenarios**:

1. **Given** que existe un resultado generado, **When** la persona usuaria elige exportar como `.txt`, **Then** la aplicación descarga un archivo local con el texto del resumen, ideas principales y glosario si existen.
2. **Given** que existe un resultado generado, **When** la persona usuaria elige exportar como `.md`, **Then** la aplicación descarga un archivo local con el contenido formateado en Markdown.
3. **Given** que la sesión no es válida o el token no puede verificarse, **When** se intenta enviar la solicitud, **Then** la aplicación muestra un error de autenticación y no intenta seguir procesando.
4. **Given** que el backend o el proveedor de IA no está disponible, **When** la petición falla, **Then** la aplicación muestra un mensaje de indisponibilidad y no expone detalles internos.

---

### Edge Cases

- Un archivo cargado con extensión distinta de `.txt` o `.md` se rechaza y se muestra un mensaje de error sin enviar contenido al backend.
- El texto de entrada supera el máximo permitido de 5000 caracteres por validación del backend; la solicitud no puede completarse si se excede el límite.
- Una sesión no autenticada o caducada bloquea el envío del resumen y exige volver a autenticarse desde la misma pantalla.
- Si la conexión al portapapeles del navegador está bloqueada por permisos o contexto inseguro, la copia no se ejecuta y la interfaz mantiene el estado previo.
- Si la respuesta de OpenRouter no incluye contenido válido o un esquema coherente, la aplicación reporta un error de respuesta inválida.
- El valor de `summary_length` puede variar entre `breve`, `estándar` y `detallado`; la interfaz refleja este valor en la etiqueta del resumen generado.

## Requirements _(mandatory)_

### Functional Requirements

- **FR-001**: El sistema MUST permitir a la persona usuaria introducir texto manualmente en un área de edición principal.
- **FR-002**: El sistema MUST permitir cargar un archivo local con extensión `.txt` o `.md`, leerlo en el navegador y utilizar su contenido como entrada del formulario, sin enviarlo como archivo al backend.
- **FR-003**: El sistema MUST limitar la carga de texto de entrada al máximo actual permitido por la aplicación y MUST mostrar un aviso si el archivo supera el tamaño o el tipo no es permitido.
- **FR-004**: El sistema MUST ofrecer al usuario opciones de longitud del resumen: `Breve`, `Estándar` y `Detallado`.
- **FR-005**: El sistema MUST permitir activar o desactivar la extracción de ideas principales como opción adicional del resumen.
- **FR-006**: El sistema MUST permitir activar o desactivar la generación del glosario de términos como opción adicional del resumen.
- **FR-007**: El sistema MUST enviar la solicitud de resumen con el contenido del texto y las opciones seleccionadas al backend autenticado.
- **FR-008**: El backend MUST validar la sesión de Clerk antes de continuar con el procesamiento de `/resumir` y MUST responder con 401 o 503 según el estado de autenticación y disponibilidad del verificador.
- **FR-009**: El backend MUST aceptar un cuerpo con `text`, `main_ideas`, `glossary` y `summary_length` y MUST invocar a OpenRouter con un prompt que incorpora la longitud y las opciones solicitadas.
- **FR-010**: La respuesta del backend MUST incluir el campo `summary` y MUST incluir `main_ideas` y `glossary` cuando estén presentes y son válidos.
- **FR-011**: La interfaz MUST renderizar el resumen principal, las ideas principales y el glosario en bloques separados, siempre que existan en la respuesta.
- **FR-012**: La interfaz MUST permitir copiar al portapapeles cada bloque generado (`summary`, `mainIdeas` y `glossary`) cuando el navegador lo permita.
- **FR-013**: La interfaz MUST permitir exportar el contenido generado como archivo `.txt` o `.md` desde el navegador, creando un archivo local con la salida formateada.
- **FR-014**: La interfaz MUST mostrar mensajes de error de autenticación y de indisponibilidad del servicio cuando la solicitud no puede completarse.
- **FR-015**: La aplicación MUST mantener el flujo sin reintento automático cuando la sesión no es válida o cuando el verificador del backend responde con 401/503.

### Key Entities _(include if feature involves data)_

- **Entrada de texto**: Contenido escrito o cargado desde un archivo local que se convierte en la base del resumen.
- **Opción de longitud**: Configuración del nivel de detalle del resumen: breve, estándar o detallado.
- **Resumen generado**: Texto principal devuelto por el backend y renderizado en la pantalla.
- **Ideas principales**: Lista opcional de puntos clave derivados del contenido.
- **Glosario**: Lista opcional de conceptos y definiciones asociados al texto.
- **Respuesta del backend**: Estructura JSON de salida que contiene el resumen y, opcionalmente, ideas principales y glosario.

## Success Criteria _(mandatory)_

### Measurable Outcomes

- **SC-001**: Un usuario autenticado puede completar un ciclo de resumen desde entrada de texto hasta visualización del resultado sin salir de la pantalla principal.
- **SC-002**: La presencia o ausencia de `main_ideas` y `glossary` se refleja claramente en el resultado visual y en la estructura del payload enviado.
- **SC-003**: La longitud elegida por el usuario se representa visualmente en la salida y se aplica al prompt enviado al proveedor de IA.
- **SC-004**: Las secciones resultantes pueden copiarse al portapapeles y exportarse en formatos locales `.txt` y `.md` desde la aplicación cliente.
- **SC-005**: Los errores de autenticación e indisponibilidad del proveedor o verificador se muestran al usuario en mensajes comprensibles y no se reenvía automáticamente la solicitud.
- **SC-006**: El sistema requiere que la entrada esté en un formato y tamaño aceptados; se rechaza el contenido inválido antes de continuar con el procesamiento.

## Assumptions

- La SPA está diseñada para una sola pantalla principal y el usuario permanece en ella durante el flujo completo de resumen.
- La aplicación asume que el navegador permite acceso al portapapeles y al almacenamiento local para la exportación de archivos; si esta capacidad no está disponible, la copia/exportación puede no ser posible y requiere validación en el entorno del usuario.
- El valor exacto de `summary_length` se usa en el prompt del proveedor de IA y se refleja también en la visualización del resumen; la semántica final de cada nivel de longitud se valida con el comportamiento real de la llamada a OpenRouter.
- La estructura JSON de salida de OpenRouter debe ser coherente con el esquema `ResumenResponse` del backend; si el contenido devuelto por la IA no cumple ese contrato, se reporta un error de respuesta inválida.
- El flujo de autenticación con Clerk y la validación del token están implementados y verificados en el backend, pero la revisión del código no permite afirmar la configuración de entorno ni la disponibilidad de una instancia real de Clerk sin validar las variables de entorno en el entorno de ejecución.
- La exportación del archivo se realiza en el navegador utilizando `Blob` y `URL.createObjectURL`; su funcionamiento depende del navegador y del contexto de ejecución actual.
