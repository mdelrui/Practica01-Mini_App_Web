# Implementation Plan: Autenticación con Clerk

**Branch**: `001-clerk-auth` | **Date**: 2026-10-20 | **Spec**: [spec.md](./spec.md)

**Input**: Feature specification from `/specs/001-clerk-auth/spec.md`

## Summary

Integrar la autenticación gestionada por Clerk en la SPA Vue existente mediante su SDK para Vue y un modal en la pantalla principal. El frontend obtendrá el token vigente en el momento del envío y lo enviará en `Authorization: Bearer`. En FastAPI, una barrera de autenticación para el `POST /resumir` verificará el token mediante JWKS de Clerk —firma, algoritmo permitido, emisor y vigencia— antes de leer y validar el cuerpo. Las credenciales ausentes o rechazadas producirán HTTP 401; los fallos de disponibilidad al obtener o utilizar JWKS producirán HTTP 503. En ambos casos el servicio de OpenRouter no será invocado. El contrato JSON existente para solicitudes/respuestas exitosas se conserva.

## Technical Context

**Language/Version**: Frontend Vue 3.5 con TypeScript 6; backend Python con FastAPI 0.144. App 2 no declara versión de Python en un manifiesto inspeccionado; confirmar compatibilidad con el runtime de despliegue al fijar la dependencia.

**Primary Dependencies**: Existentes: Vue, Axios, FastAPI, Pydantic y OpenAI SDK utilizado contra OpenRouter. Propuestas por este plan: SDK oficial `@clerk/vue` para la SPA y PyJWT con soporte criptográfico y `PyJWKClient` para verificación JWKS. Las versiones concretas deben fijarse en sus manifiestos/lockfiles durante la implementación, no se presupone una versión instalada.

**Storage**: Ninguno. Sesión, token, cuerpo y resultado permanecen transitorios; no se añade persistencia.

**Testing**: Frontend: Vitest y Vue Test Utils existentes, simulando los composables/estado de Clerk y Axios. Backend: pytest ya presente en `backend/requirements.txt`, FastAPI `TestClient` y mocks para el verificador/JWKS y `resumir`/OpenRouter. No se usarán servicios externos reales en las pruebas automatizadas.

**Target Platform**: SPA servida en navegador y API FastAPI. La ERS contempla despliegue web y EC2; el runtime Python y los dominios/identificadores por entorno aún deben obtenerse de la configuración de despliegue.

**Project Type**: Aplicación web de dos capas con frontend y backend existentes.

**Performance Goals**: No se define un objetivo de latencia en la especificación. La consulta remota de JWKS debe tener un timeout finito y no debe bloquear indefinidamente el endpoint; el valor se fijará conforme al entorno antes de la implementación.

**Constraints**:
- Mantener una SPA de una pantalla, el formulario único y el endpoint/cuerpo JSON actuales.
- Verificar identidad en el backend antes de parsear/validar el cuerpo de solicitudes a `/resumir` para que credenciales ausentes o inválidas prevalezcan sobre errores del cuerpo y reciban 401.
- Usar lista fija de algoritmos permitidos y validar explícitamente firma, emisor, expiración y not-before; no confiar en el algoritmo indicado por el JWT sin validación.
- Fallar de forma cerrada. Separar una credencial rechazada (401) de una imposibilidad de obtener/usar las claves JWKS (503).
- No exponer tokens en cuerpos, URLs, mensajes, respuestas o registros; no registrar texto ni resultados.
- No añadir páginas, rutas, bases de datos, cuentas, perfiles ni roles propios.
- El CORS de FastAPI ya permite cabeceras arbitrarias; comprobar preflight con `Authorization` y ajustar solo si el despliegue real lo requiere.
- El usuario autorizó planificar verificación Python basada en JWKS y nuevas pruebas de backend. Los cambios descritos en este plan no implementan ni modifican archivos de aplicación en esta fase.

**Scale/Scope**: Una ruta de procesamiento protegida (`POST /resumir`), una pantalla existente, sesión individual en Clerk y ninguna persistencia funcional.

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

| Principle / gate | Status | Evidence and planned control |
|---|---|---|
| I. Alcance funcional estricto | PASS | Solo se protege el flujo de resumen existente; no se agregan pantallas, rutas de navegación, perfiles, roles, almacenamiento ni funciones de IA. |
| II. Tecnologías y arquitectura protegidas | PASS WITH AUTHORIZATION | Se conservan Vue/TypeScript, FastAPI, endpoint y estructura principal. La integración requiere dependencias de identidad/verificación y pruebas; el usuario autorizó explícitamente planificar verificador Python JWKS y pruebas backend. Las versiones y cambios concretos se revisarán antes de implementarse. |
| III. Seguridad, identidad y privacidad | PASS | Clerk emite identidad; FastAPI verifica criptográficamente cada token antes de procesar. Fallo cerrado, 401 frente a 503, cero llamadas a IA para rechazos, sin logs de token/texto/resultado. |
| IV. Contratos, validación y resultados seguros | PASS | Se conserva el contrato JSON exitoso; se documentan los estados y respuestas de error controladas, y se añade `Authorization` como cabecera HTTP. |
| V. Desarrollo dirigido por especificaciones y calidad | PASS | Esta planificación precede a tareas/implementación; las pruebas de backend simulan Clerk/JWKS y OpenRouter y cubren entradas, autenticación y errores. |
| Gobernanza y autorización | PASS FOR PLANNED SCOPE | No se edita código aquí. La especificación aprobada habilita la integración Clerk; la respuesta del usuario autoriza el enfoque JWKS y pruebas backend. No quedan autorizados cambios de alcance, nuevas rutas o gestión propia de usuarios. |

## Project Structure

### Documentation (this feature)

```text
specs/001-clerk-auth/
├── plan.md
├── research.md
├── data-model.md
├── quickstart.md
└── contracts/
    └── resumir-auth.md
```

### Source Code (repository root)

```text
app2/
├── backend/
│   ├── main.py                 # Protege /resumir antes de analizar el cuerpo
│   ├── auth.py                 # Nuevo: verificación JWT/JWKS y clasificación de errores
│   ├── requirements.txt        # Añade la dependencia de verificación autorizada
│   └── tests/                  # Nuevo: pruebas de contrato/autenticación con mocks
│       └── test_auth.py
└── frontend/
    ├── package.json            # Añade el SDK Vue de Clerk
    └── src/
        ├── main.ts             # Inicializa Clerk en la SPA existente
        ├── App.vue             # Estados, modal, obtención y envío del token, UX de 401/503
        └── __tests__/
            └── App.spec.ts     # Amplía pruebas de sesión, cabecera y estados de error
```

**Structure Decision**: Conservar las dos capas y los puntos de entrada existentes. Se justifica un módulo pequeño `backend/auth.py` para aislar la verificación y su clasificación de errores, y un directorio de pruebas backend porque actualmente no hay tests Python y RF-012 exige probar el límite de seguridad. No se añade ninguna ruta HTTP nueva. Cualquier desviación de estos archivos propuestos requiere revisión antes de implementación.

## Complexity Tracking

| Violation | Why Needed | Simpler Alternative Rejected Because |
|-----------|------------|-------------------------------------|
| Dependencia frontend `@clerk/vue` y verificador JWT/JWKS Python | Clerk debe proporcionar la sesión en Vue y el backend debe verificar firma/claims con claves de confianza; la implementación actual no tiene ninguna de esas capacidades. | Decodificar JWT sin firma no autentica; implementar criptografía/JWKS propia aumenta riesgo; una integración remota ad hoc acoplaría la ruta a llamadas manuales a Clerk. |
| Módulo de autenticación y pruebas backend | Aísla el control previo al parseo y permite verificar 401/503 y cero llamadas a IA con pruebas deterministas. | Proteger solo el botón del frontend no protege llamadas directas al endpoint; no hay suite backend actual en que alojar estas pruebas. |

## Phase 0: Research

Completed in [research.md](./research.md). The chosen plan is a Vue session-token client and JWKS-backed Python verification. The Clerk environment's issuer and JWKS endpoint remain deployment inputs; no real values or credentials are assumed.

## Phase 1: Design & Contracts

- [Data model](./data-model.md): session state, transient bearer token and processing request lifecycle.
- [HTTP contract](./contracts/resumir-auth.md): existing `POST /resumir`, bearer header and 200/401/422/502/503/504 outcomes.
- [Quickstart](./quickstart.md): mock-only test procedures, targeted UI checks and optional configured-instance smoke test.

### Constitution Check (post-design)

| Gate | Status | Design evidence |
|---|---|---|
| One-screen scope/no new login pages or routes | PASS | Clerk access is a modal and processing remains on the current SPA route. |
| Protected structure and approved dependencies | PASS WITH AUTHORIZATION | Backend verifier and backend tests were authorized; SDK/dependency versions must be reviewed and pinned during implementation. |
| Backend security and no IA call on auth failure | PASS | Auth check precedes body parsing; 401 for invalid/missing credentials and 503 for verifier/JWKS unavailability; both stop the request before `resumir`. |
| No persistence/logging of sensitive data | PASS | Token is in header only, never logged; input/results remain transient and tests assert no leakage. |
| Test quality and external-service isolation | PASS | Unit/contract tests replace Clerk/JWKS and OpenRouter with controlled mocks. |

## Readiness and implementation gates

- Before coding, configure the per-environment Clerk publishable key, expected issuer and JWKS source through the deployment's approved configuration. Do not add real credentials to source control.
- Confirm the production/development issuer values against Clerk's actual instance settings; do not derive trust from an unverified JWT claim.
- Select and pin dependency versions compatible with the declared runtime; test JWKS connection-failure classification and the configured finite timeout.
- Review any proposed app structure/dependency changes against the authorization recorded above. Do not implement beyond this approved scope.
