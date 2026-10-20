# Quickstart: Validar Autenticación Clerk

This guide validates the implementation after the plan is converted into tasks and the feature is implemented. Automated cases must use mocks; no Clerk or OpenRouter network calls are made by the test suites.

## Prerequisites

- Implemented feature and pinned dependencies for the supported Python and Node runtimes.
- No real credentials are required for automated tests.
- For an optional manual smoke test only, obtain the Clerk publishable key, expected issuer and JWKS source from the correct Clerk environment through approved local/deployment configuration. Do not put secrets or real tokens in source control, screenshots, or logs.
- Keep the existing OpenRouter key server-side; automated tests must replace its service call with a mock.

## Backend automated checks

From `app2/backend`:

```powershell
python -m pytest -q
```

Expected assertions:

- A mocked valid Clerk token reaches the existing summary service once and returns the existing successful response.
- Missing, malformed, invalid-signature, wrong-issuer, expired, and unrecognized-key tokens return 401.
- A request without valid credentials and with malformed JSON returns 401 before body validation.
- A mocked JWKS connection outage, timeout, or unusable JWKS source returns 503.
- Every 401/503 case makes zero calls to the mocked summary/OpenRouter service.
- The token is never returned, logged, included in JSON/query parameters, or persisted.

## Frontend automated checks

From `app2/frontend`:

```powershell
npm run test:unit -- --run
npm run type-check
```

Expected assertions:

- Loading, signed-out, signed-in and auth-error states are visible and the summary button cannot submit until authenticated.
- Selecting sign-in opens the Clerk modal without changing the current route; sign-out returns to the signed-out UI.
- A signed-in submission sends the current token in the `Authorization` Bearer header and leaves the existing JSON request body unchanged.
- A 401 shows a session/authentication message and preserves the entered text; a 503 shows a temporary verification-service message distinct from 401. Neither status triggers automatic resubmission.

## Manual configured-instance smoke test (optional)

1. Start the backend and SPA with Clerk values configured for the same development instance and an allowed CORS origin.
2. Open the existing SPA, verify the signed-out status, and open the access modal.
3. Complete authentication in the modal; verify the page route stays unchanged and the signed-in state is shown.
4. Submit a short non-sensitive test string and verify the backend receives a Bearer header and returns the existing summary response.
5. Sign out and verify the signed-out state; do not copy tokens into logs or debugging artifacts.
6. To check backend enforcement, send a request without authorization and another with an expired test token; both must return 401 and must not invoke OpenRouter. Use a controlled test environment.
7. Simulate a JWKS outage in automated tests rather than disabling production Clerk availability; expected response is 503 with no OpenRouter call.

## Existing behavior regression checks

- The summary route remains `POST /resumir`.
- Successful request and response JSON shapes remain unchanged.
- Input validation and existing IA error behavior remain unchanged for authenticated requests.
- The single-screen SPA, local file reading, and result display remain intact.
