# Research: Autenticación con Clerk

**Feature**: [Autenticación con Clerk](./spec.md)  
**Date**: 2026-10-20

## Decisions

### Frontend session-token acquisition

- **Decision**: Use Clerk's Vue SDK/composable to read the current session token at the time a summary request is sent, then attach it as `Authorization: Bearer <token>`.
- **Rationale**: Clerk documents `useAuth()` for Vue and `getToken()` for retrieving the current session token. Its authenticated-request guide describes sending the token manually for API requests. This matches the existing same-SPA flow and avoids placing tokens in the request body or URL.
- **Alternatives considered**: Reading a token from browser storage or retaining it separately in app state was rejected because it can become stale and unnecessarily duplicates sensitive state. Redirecting to a separate login route conflicts with the specification.
- **Sources**:
  - [Clerk Vue `useAuth()`](https://clerk.com/docs/vue/reference/composables/use-auth)
  - [Clerk: Making authenticated requests](https://clerk.com/docs/guides/development/making-requests)

### Backend JWT verification and JWKS

- **Decision**: Plan PyJWT with `PyJWKClient` to retrieve Clerk's JWKS and choose the signing key by token `kid`; verify using a fixed allowed algorithm and explicitly validate signature, expected issuer, `exp`, and `nbf`.
- **Rationale**: JWKS verification uses the identity provider's published public keys and supports key rotation without placing a private key in the application. PyJWT combines JWT validation with JWKS retrieval/key selection, avoiding custom cryptographic and JWKS plumbing. The user's response explicitly authorized a Python JWKS verifier and backend tests.
- **Alternatives considered**:
  - A manually configured public key can avoid a live JWKS lookup but needs secure provisioning and key-rotation handling.
  - Authlib or python-jose can validate JWTs but would require additional JWKS retrieval/caching integration based on the documentation reviewed.
  - Decoding without signature verification is explicitly rejected.
- **Operational caveats**: PyJWT documents a default JWKS-set cache duration of 300 seconds and a 30-second refresh cooldown for unknown `kid`; these are library defaults, not project requirements. The JWKS network timeout must be finite and chosen for the actual deployment. The backend must classify fetch/connection and unusable-key-set failures as verifier unavailability (503), and invalid, expired, wrong-issuer, bad-signature or unmatched-key credentials as rejected (401). Confirm exact exception behavior against the pinned PyJWT version in tests.
- **Sources**:
  - [Clerk: Manual JWT verification](https://clerk.com/docs/guides/sessions/manual-jwt-verification)
  - [Clerk: Session token claims](https://clerk.com/docs/guides/sessions/session-tokens)
  - [PyJWT: Retrieve RSA signing keys from a JWKS endpoint](https://pyjwt.readthedocs.io/en/stable/usage.html#retrieve-rsa-signing-keys-from-a-jwks-endpoint)
  - [PyJWT API and `PyJWKClient`](https://pyjwt.readthedocs.io/en/stable/api.html#jwt.PyJWKClient)
  - [RFC 6750 §3.1: Bearer token errors](https://www.rfc-editor.org/rfc/rfc6750.html#section-3.1)
  - [RFC 9110 §15.5.2: 401 Unauthorized](https://www.rfc-editor.org/rfc/rfc9110.html#section-15.5.2)
  - [RFC 9110 §15.6.4: 503 Service Unavailable](https://www.rfc-editor.org/rfc/rfc9110.html#section-15.6.4)

### Request ordering and failure behavior

- **Decision**: Authenticate the `POST /resumir` request before parsing/validating its JSON body. Use a pre-body request gate and offload synchronous JWKS operations from the async event loop if the chosen ASGI middleware path is async.
- **Rationale**: The specification requires a missing/invalid token to return 401 even if the submitted body is invalid. An auth check that runs after automatic body validation could return 422 first and violate that observable rule.
- **Alternatives considered**: Checking only in the frontend is not an access control; relying on a typed route body without verifying request ordering cannot establish the required 401 precedence. The final plan uses an authentication gate scoped only to the existing processing endpoint.
- **Failure mapping**: Credential failures return 401. A network outage, timeout, or unusable JWKS source returns 503, fails closed, and never calls `resumir`/OpenRouter. Keep user-facing messages generic and do not expose the token, JWKS payload, or internal exception details.

## Repository findings relevant to the plan

- The SPA is mounted in `frontend/src/main.ts`; `App.vue` owns the existing summarization form and sends an Axios POST to the backend.
- The current `POST /resumir` route is in `backend/main.py`; it uses a Pydantic request body and calls `services.resumir`.
- `backend/requirements.txt` already includes pytest and FastAPI's HTTP test dependency; no backend test files were found.
- `frontend/package.json` already provides Vitest and Vue Test Utils; the existing component test mocks Axios.
- FastAPI CORS middleware currently allows all request headers; verify an `Authorization` preflight during validation rather than widening access without need.
- Existing successful request/response payloads and the OpenRouter implementation remain unchanged.
- The inspected App 2 environment example contains only OpenRouter settings. No Clerk publishable key, expected issuer or JWKS URL was present. Obtain these per environment; this document intentionally invents no values.

## Items to confirm during implementation setup

- The actual Clerk development and production Frontend API issuer and JWKS source.
- A finite JWKS-fetch timeout appropriate for the deployed request latency.
- Exact versions of `@clerk/vue` and PyJWT compatible with the actual Python/Node runtime; pin through the project's standard dependency workflow.
- Whether deployment configuration already supplies frontend public values and backend settings securely; do not commit secrets.
