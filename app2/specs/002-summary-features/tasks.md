# Tasks: Resumen y salida del documento

**Input**: Design documents from `/specs/002-summary-features/`

**Status legend**:

- `[x]` = already implemented in the current app2 codebase
- `[ ]` = pending review or missing implementation

## Phase 1: Setup and architecture validation

**Purpose**: Confirm the project is already aligned with the intended Vue + FastAPI architecture and document the exact extension points.

- [x] T001 [P] Validate the existing app2 stack and confirm the frontend/backend split in `app2/frontend/src/App.vue` and `app2/backend/main.py`
- [x] T002 [P] Validate the current auth model and Clerk session enforcement in `app2/backend/auth.py`
- [x] T003 [P] Validate the summary payload schema in `app2/backend/models.py` and `app2/frontend/src/types/types.ts`
- [x] T004 [P] Validate the OpenRouter orchestration and prompt contract in `app2/backend/services.py`
- [x] T005 Confirm the feature remains within the single-screen scope defined by the constitution and spec in `app2/specs/002-summary-features/spec.md`

---

## Phase 2: Foundational backend and request flow

**Purpose**: Ensure the authenticated summary request is valid, safe, and consistent before UI work is expanded.

- [x] T006 [P] Implement and validate the `/resumir` route and CORS/auth middleware in `app2/backend/main.py`
- [x] T007 [P] Validate 401/503 handling for invalid or unavailable Clerk verification in `app2/backend/main.py`
- [x] T008 [P] Confirm `text`, `main_ideas`, `glossary` and `summary_length` are accepted by the backend schema in `app2/backend/models.py`
- [x] T009 [P] Confirm OpenRouter prompt generation includes summary length and optional flags in `app2/backend/services.py`
- [x] T010 Review whether the current CORS fallback and `Access-Control-Allow-Origin` handling fully cover all browser failure modes for non-credentialed or preflight requests in `app2/backend/main.py`
- [x] T011 Review whether the backend plus frontend error messages are sufficiently specific and consistent across 401, 503, 502 and 504 paths in `app2/backend/main.py` and `app2/frontend/src/App.vue`

---

## Phase 3: User Story 1 - Enviar texto para resumir desde la interfaz actual (Priority: P1) 🎯 MVP

**Goal**: Allow a signed-in user to enter or load text, choose summary options, and send the request authenticated to the backend.

**Independent Test**: Sign in, write text, choose length + toggles, send request, and confirm that the payload includes the text and auth header before the backend processes it.

### Tests for User Story 1

- [x] T012 [P] [US1] Validate auth/security tests for invalid/missing token and JWKS failures in `app2/backend/tests/test_auth.py`
- [x] T013 [P] [US1] Add a frontend test that covers the valid send flow from the form to the backend call in `app2/frontend/src/__tests__/App.spec.ts`

### Implementation for User Story 1

- [x] T014 [P] [US1] Implement the textarea, file loading and validation in `app2/frontend/src/App.vue`
- [x] T015 [P] [US1] Implement summary length selection and toggle handling in `app2/frontend/src/App.vue`
- [x] T016 [US1] Implement `getSummary()` with Clerk token retrieval, axios call and payload assembly in `app2/frontend/src/App.vue`
- [x] T017 [US1] Enforce input limits and block invalid file types or oversized files in `app2/frontend/src/App.vue`
- [x] T018 [US1] Review whether the `text` sanitization in `getSummary()` matches the intended UX for whitespace and newline normalization in `app2/frontend/src/App.vue`

**Checkpoint**: User Story 1 is already implemented and verified in the current codebase and in the frontend/backend test suites.

---

## Phase 4: User Story 2 - Ver resultados segmentados en la pantalla (Priority: P1)

**Goal**: Render the response as structured sections and allow copy actions for each one.

**Independent Test**: Provide a valid API response with summary, mainIdeas and glossary and verify each section is rendered and copied correctly.

### Tests for User Story 2

- [x] T019 [P] [US2] Add a frontend test for successful rendering of `summary`, `mainIdeas` and `glossary` in `app2/frontend/src/__tests__/App.spec.ts`
- [x] T020 [P] [US2] Add a frontend test for copy action behavior when `navigator.clipboard.writeText` succeeds/fails in `app2/frontend/src/__tests__/App.spec.ts`

### Implementation for User Story 2

- [x] T021 [P] [US2] Render the summary output and optional sections in `app2/frontend/src/App.vue`
- [x] T022 [P] [US2] Add copy handlers for the summary, main ideas and glossary in `app2/frontend/src/App.vue`
- [x] T023 [US2] Add the reusable copy button component in `app2/frontend/src/components/CopyButton.vue`
- [x] T024 [US2] Review browser permission and secure-context behavior for clipboard access in `app2/frontend/src/App.vue`
- [x] T025 [US2] Review whether the UI clearly distinguishes missing optional fields from empty values in the rendered result in `app2/frontend/src/App.vue`

**Checkpoint**: The rendering and copy path are implemented and verified by the current frontend test suite.

---

## Phase 5: User Story 3 - Exportación local del resultado y tratamiento de errores (Priority: P2)

**Goal**: Export the generated content locally and communicate backend/frontend errors without exposing internal details.

**Independent Test**: Generate a result, export `.txt` and `.md`, and verify that auth and availability failures show the right user-facing messages.

### Tests for User Story 3

- [x] T026 [P] [US3] Add a frontend test for `.txt` and `.md` export generation in `app2/frontend/src/__tests__/App.spec.ts`
- [x] T027 [P] [US3] Add a frontend test for 401 and 503 user messages in `app2/frontend/src/__tests__/App.spec.ts`

### Implementation for User Story 3

- [x] T028 [P] [US3] Implement the local `.txt` export path in `app2/frontend/src/App.vue`
- [x] T029 [P] [US3] Implement the local `.md` export path in `app2/frontend/src/App.vue`
- [x] T030 [US3] Show user-facing auth and availability messages in `app2/frontend/src/App.vue`
- [x] T031 [US3] Ensure the app does not auto-retry on invalid session or verifier-unavailable states in `app2/frontend/src/App.vue`
- [x] T032 [US3] Review whether export file naming and `URL.revokeObjectURL` timing are robust across browsers in `app2/frontend/src/App.vue`

**Checkpoint**: Export and error messaging are present and covered by the current regression tests.

---

## Phase 6: Polish and cross-cutting review

**Purpose**: Final review and hardening before sign-off.

- [x] T033 [P] Run backend validation against `app2/backend/tests/test_auth.py` and confirm the auth contract still matches the requirement in `app2/backend/tests/test_auth.py`
- [x] T034 [P] Run frontend validation through `app2/frontend/src/__tests__/App.spec.ts` and check the summary rendering, copy, and export flows
- [x] T035 Review the `quickstart.md` flow against the actual runtime behavior and update the validation checklist if needed in `app2/specs/002-summary-features/quickstart.md`
- [x] T036 Review the plan and contracts against the implemented code to ensure there are no drift issues between design and runtime in `app2/specs/002-summary-features/`

---

## Dependencies and execution order

- Phase 1 and Phase 2 must be considered as a shared validation gate before new feature work.
- User Story 1 is the MVP and is already implemented in the current codebase.
- User Story 2 and User Story 3 are also functionally present and verified by the current test suite.
- Polishing and testing are complete and validated with the existing backend/frontend checks.

### Parallel opportunities

- Setup and contract validation tasks can be executed in parallel.
- The backend auth and request contract checks can run independently from the frontend UI validation tasks.
- Rendering and copy/export tasks are independent once the summary contract is established.

## Implementation strategy

### MVP already present

1. Validate the auth and request flow.
2. Confirm the summary model contract.
3. Keep the current UI as the MVP baseline.
4. Add missing regression tests and review edge cases.

### Incremental follow-up

1. Review clipboard behavior and secure-context restrictions.
2. Review CORS/auth error consistency and add tests.
3. Strengthen frontend regression coverage for render/export/copy flows.
4. Finalize validation with backend and frontend test runs.
