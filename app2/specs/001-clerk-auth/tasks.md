# Tasks: Autenticación con Clerk

**Input**: Design documents from `/specs/001-clerk-auth/`

**Prerequisites**: [plan.md](./plan.md), [spec.md](./spec.md), [research.md](./research.md), [data-model.md](./data-model.md), [contracts/](./contracts/), [quickstart.md](./quickstart.md)

**Organization**: Tasks are grouped by user story for independently verifiable increments. Automated tests are required by FR-012 and MUST use mocks for Clerk/JWKS and OpenRouter.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel with other tasks in its phase; separate files and no unmet dependencies.
- **[Story]**: User story from `spec.md` (`US1`, `US2`, `US3`).
- Every task includes a concrete file path and starts with an unchecked checkbox and sequential ID.

## Phase 1: Setup

**Purpose**: Add only the approved integration dependencies and identify configuration inputs without inventing Clerk instance values.

- [X] T001 [P] Add a pinned `@clerk/vue` dependency compatible with the existing Vue and Node versions in `app2/frontend/package.json` and update `app2/frontend/package-lock.json`.
- [X] T002 [P] Add a pinned PyJWT cryptographic/JWKS dependency compatible with the deployed Python runtime in `app2/backend/requirements.txt`; record the selected version in the same file.
- [X] T003 Define `VITE_CLERK_PUBLISHABLE_KEY` and its TypeScript environment typing in `app2/frontend/.env.example` and `app2/frontend/env.d.ts`; define `CLERK_ISSUER`, `CLERK_JWKS_URL`, and finite `CLERK_JWKS_TIMEOUT` placeholders in `app2/backend/.env.example`. Obtain actual development/production values from the configured Clerk instance; do not commit credentials or invent issuer/URL values.

## Phase 2: Foundational

**Purpose**: Prepare deterministic backend test infrastructure required by the security stories.

- [X] T004 Create reusable FastAPI `TestClient` fixtures and controlled verifier/OpenRouter mock setup in `app2/backend/tests/conftest.py`; ensure test setup requires no real Clerk or OpenRouter credentials.

**Checkpoint**: Dependency manifests and test configuration are ready; stories can be implemented with the security gate completed before enabling authenticated processing.

## Phase 3: User Story 1 - Acceder desde la pantalla actual (Priority: P1)

**Goal**: Show Clerk loading, signed-out, signed-in and sign-out states on the existing screen, with sign-in presented in a same-screen modal and no route changes.

**Independent Test**: With Clerk mocked, verify each authentication state and sign-in/sign-out action; assert the route remains unchanged and Axios is not called while loading or signed out.

### Tests for User Story 1

- [X] T005 [P] [US1] Add component tests for loading/signed-out/signed-in states, modal opening, sign-out, unchanged route, and blocked summary submission while unauthenticated in `app2/frontend/src/__tests__/App.spec.ts`.

### Implementation for User Story 1

- [X] T006 [US1] Initialize the Clerk Vue provider with the configured public publishable key while preserving the current SPA mount in `app2/frontend/src/main.ts`.
- [X] T007 [US1] Add visible Clerk loading/signed-out/signed-in states, same-screen sign-in modal, and sign-out action without adding routes or replacing the existing summary screen in `app2/frontend/src/App.vue`.

**Checkpoint**: The authentication UI works independently with mocked Clerk state and does not send summary requests before sign-in.

## Phase 4: User Story 3 - Rechazar solicitudes sin sesión válida (Priority: P1)

**Goal**: Reject direct requests without valid credentials before parsing the body, distinguish invalid credentials (401) from verifier/JWKS outages (503), and visibly report these outcomes without invoking OpenRouter.

**Independent Test**: Use `TestClient` with mocked verifier/JWKS and summary service. Missing, malformed, invalid-signature, wrong-issuer and expired credentials return 401; an invalid credential with malformed JSON still returns 401; verifier/JWKS outage returns 503; every rejected/unavailable case produces zero summary/OpenRouter calls. Frontend tests distinguish 401 and 503, preserve entered text, and do not retry.

### Tests for User Story 3

- [X] T008 [P] [US3] Add backend contract tests for absent/wrong-scheme/blank, invalid-signature, wrong-issuer, expired and unmatched-key credentials; assert HTTP 401, 401 precedence over malformed JSON, and zero summary-service calls in `app2/backend/tests/test_auth.py`.
- [X] T009 [US3] Add backend tests for JWKS connection failure, timeout and unusable JWKS; assert HTTP 503 and zero summary-service calls in `app2/backend/tests/test_auth.py`.
- [X] T010 [P] [US3] Add frontend tests for distinct 401/session-invalid and 503/verifier-unavailable messages, retained input, no automatic retry, and no token exposure in `app2/frontend/src/__tests__/App.spec.ts`.

### Implementation for User Story 3

- [X] T011 [US3] Implement a backend verifier using the configured Clerk JWKS source, a fixed allowed algorithm, required valid `exp`, applicable `nbf`, signature and issuer checks, and a finite fetch timeout; avoid blocking the async request loop during JWKS I/O and classify rejected credentials separately from JWKS unavailability in `app2/backend/auth.py`.
- [X] T012 [US3] Protect the existing `POST /resumir` request before JSON parsing/validation and map invalid/missing credentials to HTTP 401 and verifier/JWKS outages to HTTP 503 without changing successful JSON behavior in `app2/backend/main.py`.
- [X] T013 [P] [US3] Display separate user-safe messages for HTTP 401 and HTTP 503, preserve the entered text, expose the same-screen Clerk modal for re-authentication, and do not auto-resubmit in `app2/frontend/src/App.vue`.

**Checkpoint**: Direct unauthenticated access fails closed before body validation; all 401/503 paths make zero OpenRouter calls and have distinct UI feedback.

## Phase 5: User Story 2 - Procesar una solicitud autenticada (Priority: P1)

**Goal**: A signed-in user sends the current Clerk token using the Bearer authorization header and receives the existing summary response after server verification.

**Independent Test**: Mock Clerk token acquisition to return a current token and the backend verifier to accept a valid signed-token fixture; assert the frontend sends `Authorization: Bearer ...`, preserves the existing JSON body, and the backend continues to the summary service exactly once for a valid request.

### Tests for User Story 2

- [X] T014 [P] [US2] Add a frontend test that an authenticated submission obtains the current Clerk token at submit time, sends it only in `Authorization: Bearer`, leaves the existing JSON body unchanged, and never renders the token in `app2/frontend/src/__tests__/App.spec.ts`.
- [X] T015 [P] [US2] Add a backend contract test that a valid token and valid existing request body return the existing success schema and invoke the mocked summary/OpenRouter service exactly once in `app2/backend/tests/test_auth.py`.

### Implementation for User Story 2

- [X] T016 [US2] Obtain the current Clerk session token for each submit, attach it as the `Authorization` Bearer header to the existing Axios `POST /resumir`, keep the JSON body unchanged, and handle token-acquisition failure without sending a request in `app2/frontend/src/App.vue`.

**Checkpoint**: An authenticated, valid request follows the original summary path once; token transport and successful payload match the contract.

## Phase 6: Polish & Cross-Cutting Concerns

**Purpose**: Verify privacy, CORS, documentation and regression criteria across the complete vertical slice.

- [X] T017 [P] Add assertions that tokens do not appear in response bodies or captured logs, and that the existing CORS policy accepts an `Authorization` preflight from the configured SPA origin in `app2/backend/tests/test_auth.py`.
- [X] T018 Update the setup/configuration and authentication testing instructions, including non-secret Clerk environment variables and the 401/503 distinction, in `app2/frontend/README.md` and `app2/backend/.env.example`.
- [X] T019 Run the backend test suite and frontend unit/type checks from the working directories described in `app2/specs/001-clerk-auth/quickstart.md`; resolve failures without contacting real Clerk or OpenRouter services.

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No story dependencies. T001 and T002 can run in parallel; T003 configures both environment examples and follows the integration settings agreed for the project.
- **Foundational (Phase 2)**: T004 depends on the backend test dependency from T002 and blocks backend story tests.
- **US1 (Phase 3)**: Depends on T001 and T003. Its frontend tests precede provider and interface implementation.
- **US3 (Phase 4)**: Backend contract tests depend on T002/T004; frontend error tests depend on US1's Clerk UI. Implement the verifier and route gate only after rejection/outage tests exist.
- **US2 (Phase 5)**: Depends on US1 session/token access and US3 backend enforcement. Tests are added before frontend submission integration; the backend success test validates the shared verified route.
- **Polish (Phase 6)**: Depends on all three user stories.

### User Story Dependencies

- **US1 (P1)**: Starts after setup; independent of backend processing.
- **US3 (P1)**: Direct backend rejection tests are independent of US1. The user-visible error/modal path depends on the Clerk UI from US1.
- **US2 (P1)**: Depends on US1 to obtain a session token and US3 to enforce backend verification before processing.
- Security ordering: complete the US3 backend gate before making the authenticated processing path available through US2.

### Parallel Opportunities

- **Setup**: T001 and T002 touch separate manifests and can run in parallel.
- **US1**: T005 is the test-first task; implementation tasks T006/T007 are sequential because the App uses the initialized Clerk provider.
- **US3**: T008 and T009 both modify `app2/backend/tests/test_auth.py` and therefore must be applied sequentially despite their independent cases. T010 modifies the frontend test file and can be done alongside one backend test task if work is coordinated without file overlap.
- **US2**: T014 and T015 target different test files and can run in parallel.
- **Polish**: T017 and documentation task T018 can run in parallel; T019 follows all changes.

## Parallel Example: User Story 1

US1 has no concurrent implementation tasks because the screen tests must be written first, then Clerk initialized before the App consumes its state:

```text
Task: T005 Add mocked authentication-state and modal tests in app2/frontend/src/__tests__/App.spec.ts
Then: T006 Initialize Clerk in app2/frontend/src/main.ts
Then: T007 Integrate the session UI in app2/frontend/src/App.vue
```

## Parallel Example: User Story 3

Run the independent frontend and backend tests in parallel after US1 is complete and backend test setup is ready. Keep backend test edits in the shared file sequential:

```text
Task: T008 Add invalid-credential and body-ordering tests in app2/backend/tests/test_auth.py
Task: T010 Add 401/503 UI tests in app2/frontend/src/__tests__/App.spec.ts
Then: T009 Add JWKS-outage tests in app2/backend/tests/test_auth.py
```

## Parallel Example: User Story 2

```text
Task: T014 Add frontend authenticated-submit test in app2/frontend/src/__tests__/App.spec.ts
Task: T015 Add valid-token backend contract test in app2/backend/tests/test_auth.py
```

## Implementation Strategy

### MVP

For a secure, useful vertical slice, deliver US1, US3 and US2 together: the user can authenticate in the existing screen, the backend rejects untrusted calls, and a verified request can reach the existing summarization function. US1 alone is independently testable but does not deliver protected summarization.

### Incremental Delivery

1. Complete setup and the backend mock test harness.
2. Deliver US1 and validate session UI and modal with Clerk mocked.
3. Deliver US3 and validate 401/503 rejection behavior before enabling processing.
4. Deliver US2 and validate the authorized end-to-end contract using mocks.
5. Complete privacy/CORS/documentation regression checks and run the quickstart suite.

## Notes

- All task lines use `- [ ] Tnnn`, include exact target paths, and carry `[USn]` only in user-story phases.
- `[P]` appears only where tasks target separate files and have no unfinished dependency; tests touching a shared file are explicitly sequenced.
- Do not implement beyond the approved Clerk/JWKS scope. Resolve deployment-specific issuer, JWKS URL, timeout, and dependency versions before running the corresponding setup tasks.
