# Feature Specification: Autenticación con Clerk

**Feature Branch**: No creada (fase de especificación)

**Created**: 2026-10-20

**Status**: Draft

**Input**: User description: "Definir la especificación de la integración de autenticación con Clerk para ResumidorIA (App 2), basada en la ERS de App 2, la constitución del proyecto y el código existente. Mantener Clerk en la SPA actual, enviar el token como `Authorization: Bearer`, verificarlo en el backend antes de procesar o llamar a OpenRouter, rechazar con 401 los tokens ausentes o inválidos sin invocar a OpenRouter, mostrar los estados y errores de autenticación y cubrir con pruebas automatizadas mockeadas los casos autenticados y no autenticados. No añadir rutas/páginas de acceso, registro o perfil, ni implementar código en esta fase."

## Clarifications

### Session 2026-10-20

- Q: ¿Cómo debe presentarse el acceso de Clerk en la pantalla principal? (PEN-09) → A: Modal en la misma pantalla principal.
- Q: ¿Qué código HTTP debe devolver el backend si no puede verificar el token porque Clerk o el servicio de claves no está disponible? (FR-010) → A: HTTP 503 Service Unavailable.

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Acceder desde la pantalla actual (Priority: P1)

Una persona usuaria abre ResumidorIA y puede reconocer si su sesión está iniciándose, si debe autenticarse o si ya está autenticada. Puede iniciar o cerrar sesión con Clerk mediante un modal en la pantalla existente, sin navegar a una página o ruta de autenticación nueva.

**Why this priority**: La autenticación es necesaria para utilizar el procesamiento protegido y debe respetar la SPA de una sola pantalla.

**Independent Test**: Probar la pantalla con el estado de Clerk simulado como cargando, sin sesión y con sesión. Comprobar que el estado y la acción disponible son visibles y que la ruta actual no cambia.

**Acceptance Scenarios**:

1. **Given** que la aplicación está mostrando su pantalla principal y Clerk todavía está resolviendo la sesión, **When** se carga la interfaz, **Then** se indica visiblemente que el estado de autenticación está pendiente y no se permite enviar una solicitud de resumen.
2. **Given** que no hay una sesión autenticada, **When** la persona usuaria selecciona la acción de acceso, **Then** se abre el modal de Clerk sobre la pantalla actual y no se navega a una página o ruta nueva.
3. **Given** que Clerk confirma una sesión autenticada, **When** se muestra la pantalla, **Then** se identifica visiblemente el estado autenticado y se ofrece la acción de cerrar sesión en esa misma pantalla.
4. **Given** que la sesión está autenticada, **When** la persona usuaria cierra sesión, **Then** la interfaz vuelve a mostrar el estado no autenticado sin cambiar de ruta.

---

### User Story 2 - Procesar una solicitud autenticada (Priority: P1)

Una persona con una sesión de Clerk válida envía el texto desde el formulario existente. La solicitud incluye el token actual de la sesión y el backend solo continúa con el procesamiento después de validar dicho token.

**Why this priority**: Permite el uso legítimo de la función de resumen sin cambiar el flujo funcional ya existente.

**Independent Test**: Simular una sesión válida y un token aceptado por el verificador; comprobar que el envío incluye la cabecera `Authorization` con el esquema `Bearer` y el token vigente, que el backend acepta la petición y que el proveedor de IA se invoca exactamente una vez para una entrada válida.

**Acceptance Scenarios**:

1. **Given** que la sesión está autenticada y el texto cumple las validaciones actuales, **When** se envía el formulario, **Then** la petición al backend contiene el token vigente en la cabecera `Authorization` con el esquema `Bearer`.
2. **Given** que el backend recibe un token con firma, emisor y vigencia válidos, **When** termina la verificación, **Then** continúa el flujo de resumen existente y, para una entrada válida, realiza una única llamada a OpenRouter.
3. **Given** que la obtención del token falla o no devuelve un token, **When** la persona usuaria intenta enviar el formulario, **Then** la solicitud de procesamiento no se envía y se presenta un estado o error de autenticación comprensible.
4. **Given** que una solicitud autenticada se envía al backend, **When** se inspeccionan sus datos y la respuesta, **Then** el token solo aparece en la cabecera de autorización y no se incluye en el cuerpo, los parámetros, la respuesta ni los registros.

---

### User Story 3 - Rechazar solicitudes sin sesión válida (Priority: P1)

Una persona sin sesión válida —incluidas las solicitudes directas al backend— recibe una respuesta de autenticación no autorizada. La aplicación informa del problema y permite volver a autenticarse desde la misma pantalla, sin procesar el texto ni consumir el proveedor de IA.

**Why this priority**: La verificación del lado servidor es el límite efectivo de protección; la restricción visual del formulario por sí sola no protege el endpoint.

**Independent Test**: Enviar solicitudes con credenciales ausentes, mal formadas, inválidas, con firma incorrecta, emisor no aceptado o expiradas, usando un verificador y OpenRouter simulados. Comprobar el 401, cero llamadas al proveedor y un mensaje de autenticación visible en la interfaz cuando el 401 procede de un envío.

**Acceptance Scenarios**:

1. **Given** que una solicitud llega al endpoint de procesamiento sin cabecera de autorización o sin un esquema `Bearer` utilizable, **When** el backend la recibe, **Then** responde HTTP 401 antes de validar o procesar el contenido y no llama a OpenRouter.
2. **Given** que una solicitud contiene un token inválido, con firma o emisor no aceptado, o caducado, **When** el backend lo verifica, **Then** responde HTTP 401 y no llama a OpenRouter.
3. **Given** que la sesión expira después de que la interfaz haya mostrado el estado autenticado, **When** el backend responde HTTP 401 al envío, **Then** la interfaz muestra un aviso de sesión no válida o caducada, conserva el texto introducido y permite autenticarse de nuevo en la misma pantalla; no reenvía automáticamente la solicitud.
4. **Given** que el backend no puede verificar el token porque Clerk o el servicio de claves no está disponible, **When** se recibe una solicitud de resumen, **Then** responde HTTP 503, no llama a OpenRouter y la interfaz muestra un error comprensible que no expone detalles internos.

### Edge Cases

- Clerk tarda en resolver la sesión al abrir la SPA: no se debe tratar ese estado transitorio como una sesión autenticada ni enviar el formulario.
- El usuario pierde o cambia la sesión entre la habilitación del formulario y la obtención del token: el frontend no envía una petición sin token y muestra el estado de autenticación actualizado.
- El token tiene formato incorrecto, firma inválida, emisor inesperado o está caducado: se rechaza como no autorizado, sin procesar la entrada ni invocar al proveedor.
- Una petición sin credenciales contiene además un cuerpo JSON inválido: la respuesta de autenticación debe prevalecer y ser HTTP 401, sin iniciar el procesamiento de la entrada.
- Clerk o el mecanismo de verificación no está disponible: el backend responde HTTP 503, falla de forma cerrada y no invoca a OpenRouter; la interfaz muestra un error de indisponibilidad distinto al error de sesión no válida.
- El token no debe aparecer en mensajes visibles, registros ni en el cuerpo de la solicitud.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: La autenticación MUST integrarse en la SPA y la pantalla principal existentes, sin añadir páginas ni rutas de acceso, registro, perfil o navegación.
- **FR-002**: El sistema MUST permitir iniciar sesión mediante un modal de Clerk sobre la pantalla principal y cerrar sesión desde esa misma pantalla; no MUST implementar cuentas, contraseñas, perfiles ni roles propios ni añadir páginas o rutas para estas acciones.
- **FR-003**: La interfaz MUST mostrar de forma perceptible los estados de autenticación pendiente, no autenticado y autenticado, así como los errores de Clerk o del proceso de autenticación que afecten a la operación.
- **FR-004**: La interfaz MUST impedir el envío del formulario de resumen mientras la autenticación está pendiente o no hay una sesión disponible, e MUST indicar que se requiere autenticación.
- **FR-005**: Para cada solicitud de procesamiento autenticada, el frontend MUST obtener el token de sesión vigente de Clerk y enviarlo exclusivamente en la cabecera HTTP `Authorization`, usando el esquema `Bearer` y el token vigente como credencial.
- **FR-006**: El backend MUST verificar la firma del token y comprobar que corresponde al emisor de Clerk previsto y que está vigente, incluida su fecha de expiración, antes de validar o procesar el contenido de la petición y antes de llamar a OpenRouter.
- **FR-007**: Si una solicitud de procesamiento carece de token, presenta una cabecera o esquema de autorización no válido, o contiene un token inválido, con firma o emisor no aceptado o caducado, el backend MUST responder HTTP 401 y MUST NOT procesar el contenido ni invocar a OpenRouter.
- **FR-008**: Solo después de verificar correctamente el token, el backend MUST continuar el flujo actual de resumen sin alterar el contrato funcional existente; para cada solicitud autenticada y válida MUST realizar exactamente una llamada a OpenRouter.
- **FR-009**: Cuando el backend devuelve HTTP 401, la interfaz MUST mostrar un aviso que identifique el problema como autenticación o sesión no válida, ofrecer el acceso de Clerk en la misma pantalla y no clasificarlo como un error genérico del proveedor de IA. No MUST reenviar automáticamente la solicitud después de volver a autenticarse.
- **FR-010**: Si el backend no puede verificar el token porque Clerk o el servicio de claves no está disponible, MUST responder HTTP 503, fallar de forma cerrada y no invocar a OpenRouter; la interfaz MUST mostrar un mensaje comprensible de indisponibilidad sin exponer trazas, secretos ni detalles internos.
- **FR-011**: El token MUST NOT enviarse en el cuerpo o los parámetros de la solicitud de resumen ni incluirse en mensajes visibles, registros, respuestas del backend o almacenamiento funcional de la aplicación.
- **FR-012**: Las pruebas automatizadas MUST simular Clerk/la verificación de tokens y OpenRouter. MUST cubrir el flujo autenticado y, como mínimo, credenciales ausentes, formato no válido, token inválido y expirado; MUST comprobar HTTP 401 y cero invocaciones a OpenRouter para credenciales rechazadas, así como HTTP 503 y cero invocaciones cuando no se pueda verificar por indisponibilidad de Clerk o del servicio de claves. MUST comprobar que el token no se incluya en el cuerpo, la URL, la respuesta ni los registros. Las pruebas MUST NOT realizar llamadas reales a Clerk ni a OpenRouter.

### Key Entities *(include if feature involves data)*

- **Sesión de Clerk**: Estado temporal de autenticación que permite a la persona usuaria acceder al procesamiento desde la SPA existente.
- **Token de sesión**: Credencial de la sesión que se envía al backend en la cabecera `Authorization: Bearer` y cuya autenticidad y vigencia se verifican en cada solicitud protegida.
- **Estado de autenticación**: Estado visible para la persona usuaria (pendiente, no autenticado, autenticado o error) que determina si puede iniciar el procesamiento.
- **Solicitud de resumen**: Entrada funcional existente que solo puede procesarse después de verificar el token asociado; no se añade persistencia de la solicitud ni del token.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: En todas las pruebas de solicitudes válidas autenticadas, la petición incluye el token vigente en `Authorization: Bearer` y el procesamiento continúa solo tras una verificación satisfactoria.
- **SC-002**: El 100 % de los casos de prueba con credenciales ausentes, mal formadas, inválidas o caducadas recibe HTTP 401 y produce cero invocaciones al mock de OpenRouter, incluso si el cuerpo también es inválido; la indisponibilidad del verificador recibe HTTP 503 y también produce cero invocaciones.
- **SC-003**: En las pruebas de interfaz, los estados pendiente, no autenticado, autenticado y error relevante se distinguen mediante contenido visible, y el usuario puede iniciar sesión o recuperarse de un 401 sin abandonar la pantalla principal ni cambiar de ruta.
- **SC-004**: La suite automatizada cubre tanto la aceptación de una sesión válida como el rechazo de sesiones no válidas mediante mocks, sin conexiones reales a servicios externos.
- **SC-005**: La incorporación de autenticación mantiene una única pantalla y no añade rutas de acceso, registro o perfil.

## Assumptions

- La función de resumen, el endpoint existente y sus validaciones permanecen como están; esta especificación añade el requisito de autenticación y no redefine funciones ajenas a ella.
- La integración usará la identidad y los tokens de sesión emitidos por Clerk; no se presupone que Clerk ya esté integrado o configurado en el proyecto.
- La configuración concreta de Clerk para desarrollo y despliegue (identificador de aplicación, emisor esperado, claves públicas de verificación, orígenes y tolerancia temporal) no consta en el código inspeccionado y deberá acordarse antes de implementar. Esta especificación no asigna valores.
- El acceso de Clerk se presentará en un modal sobre la pantalla principal; no se crearán páginas ni rutas para iniciar o cerrar sesión.
- Si el backend no puede verificar una credencial por indisponibilidad de Clerk o del servicio de claves, devuelve HTTP 503 y no llama a OpenRouter; HTTP 401 queda reservado para credenciales ausentes o inválidas.
- El frontend existente es una SPA Vue con un formulario de resumen y pruebas de componente; el backend existente expone `POST /resumir` y su servicio realiza la llamada a OpenRouter. No se observa integración de Clerk ni una suite de pruebas del backend en la estructura inspeccionada. Estos hechos describen el punto de partida, no implican que la integración ya exista.
- Las referencias de origen son la ERS de App 2 (`RF-08`, `OBJ-07`, `CA-RF08-01`–`CA-RF08-03`, `INT-02`, `IU-01` y `PEN-09`) y la constitución del proyecto, especialmente los principios de alcance estricto, arquitectura protegida, seguridad y pruebas con mocks.
