# Mini App Web Constitution

<!--
Sync Impact Report
- Version change: n/a -> 1.0.0
- Modified principles: new principles added: I. Simplicity & Scope, II. Stack Integrity, III. Frontend-Backend Separation, IV. Secure AI Integration & Operational Discipline, V. Validation, Error Handling & Contract Stability, VI. Maintainability & Minimal Dependency Governance
- Added sections: Technical Constraints, Development Workflow
- Removed sections: none
- Deferred items: TODO(RATIFICATION_DATE): date of original adoption not recorded in the repository
-->

## Core Principles

### I. Simplicity & Scope

This project MUST remain a single-page web application with a straightforward architecture and no unnecessary features. The team MUST prefer the smallest working solution that satisfies the agreed requirements, and any new capability MUST be justified by user value or explicit project needs. This keeps the app understandable and maintainable for two students with limited experience in some technologies.

### II. Stack Integrity

The frontend MUST remain built with Vue 3, TypeScript and Vite, while the backend MUST remain based on Python and FastAPI. Changes to the stack MUST be justified, documented, and approved as project-wide decisions rather than ad hoc changes. This preserves compatibility, reduces onboarding friction, and respects the agreed technical baseline.

### III. Frontend-Backend Separation

The frontend and backend MUST remain independent modules that communicate through a clearly defined HTTP API. The frontend MUST not access secrets, database details, or backend-only logic directly, and backend contracts MUST be explicit and stable. This reduces coupling and allows the two layers to evolve in a controlled way.

### IV. Secure AI Integration & Operational Discipline

The backend MUST use OpenRouter for model access, and the API key MUST be stored in an environment variable outside the repository and never exposed to the frontend. The project MUST use only free or low-cost model options during development and MUST avoid involuntary expenses. This protects credentials and keeps development aligned with the agreed budget constraints.

### V. Validation, Error Handling & Contract Stability

The system MUST validate all incoming data, AI responses, and outbound payloads before use. Backend and frontend MUST handle validation errors, communication failures, and invalid responses without blocking the interface or leaving the app in a broken state. The project MUST define and document a stable JSON contract between backend and frontend, including required fields and expected semantics. This makes failures predictable and prevents silent inconsistencies.

### VI. Maintainability & Minimal Dependency Governance

The team MUST favor understandable, reviewable solutions over architectural complexity. New dependencies, databases, authentication, deployments, external services, or extra layers MUST be added only when they are necessary for the agreed requirements and clearly justified. The project MUST prioritize easy maintenance, testing, and documentation for a small team with uneven expertise. This reduces technical debt and keeps the system manageable.

## Technical Constraints

The project MUST keep the frontend and backend separated, with a clear API boundary and explicit request/response schemas. The app MUST avoid unnecessary features, background complexity, and extra infrastructure not required by the assignment. OpenRouter usage MUST remain limited to free or low-cost configurations during development, and secrets MUST never be committed to version control or exposed in client code. The project MUST document any JSON structure used by the application in a way that remains stable and reviewable.

## Development Workflow

All work MUST stay within the scope of the requested task and avoid unrelated changes. Before a task is considered complete, the relevant checks for the affected area MUST be run and the results reviewed. The team MUST add or maintain tests when they are part of the project scope and MUST prefer solutions that are easy to explain, review, and maintain. Technical decisions that affect architecture, API design, or project constraints MUST be briefly explained in the task context or documentation.

## Governance

This constitution defines the non-negotiable baseline for the project. Any amendment MUST be documented, justified, and reviewed before it becomes binding. When a change affects architecture, contracts, testing expectations, or dependency policy, the project MUST assess the impact and ensure the new guidance remains consistent with the agreed requirements.

Versioning MUST follow semantic versioning: MAJOR for backward-incompatible governance or principle changes, MINOR for materially expanded guidance or added principles, and PATCH for clarifications or non-semantic wording improvements. Compliance review is expected whenever a change affects scope, dependencies, API contracts, or behavior. The project MUST prefer clear documentation and review over undocumented exceptions.

**Version**: 1.0.0 | **Ratified**: TODO(RATIFICATION_DATE): date of original adoption not recorded in the repository | **Last Amended**: 2026-10-10
