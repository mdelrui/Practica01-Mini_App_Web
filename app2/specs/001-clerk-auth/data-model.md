# Data Model: Autenticación con Clerk

This feature introduces no persistent application data. The following are transient request/session concepts only.

## Session State

Represents the current Clerk authentication state exposed to the existing SPA.

| Attribute | Type / values | Rules |
|---|---|---|
| status | `loading`, `signed_out`, `signed_in`, `error` | Must be visible through an appropriate UI state; `loading` and `signed_out` cannot submit a summary request. |
| session token | opaque string or absent | Retrieved from Clerk for each request; held only as long as required to send the request. Never rendered, logged, persisted, or placed in a URL/body. |
| error category | auth initialization / token acquisition / none | User-facing message must not expose tokens, secrets, stack traces, or provider internals. |

### State transitions

```text
loading -> signed_out
loading -> signed_in
loading -> error
signed_out -> loading (access modal opened)
signed_in -> signed_out (user signs out)
signed_in -> signed_out or error (backend returns 401 / token acquisition fails)
signed_in -> error (backend returns 503 for verifier outage; session status may remain signed_in)
```

A 503 from the backend indicates verification dependency unavailability, not that the user's session is invalid. It must not be presented as a 401 or trigger automatic resubmission.

## Session JWT

An ephemeral bearer credential issued by Clerk and sent only in the `Authorization` header.

| Claim / property | Validation |
|---|---|
| Cryptographic signature | Must validate against a trusted Clerk JWKS signing key selected by `kid`. |
| Algorithm | Must be in a fixed verifier allowlist; never selected solely from untrusted token data. |
| `iss` | Must match the configured Clerk issuer for the current environment. |
| `exp` | Must be present/validated as required by the session-token contract and not expired. |
| `nbf` | Must be validated when present/required by the JWT contract. |
| `sub` | Identity claim; not used to create roles, profiles, or persistent user records. |

No claim value is persisted by this feature. Exact issuer and JWKS source are environment configuration inputs and must be confirmed from Clerk before implementation.

## Summary Request

Existing transient request to `POST /resumir`.

| Attribute | Type | Rules |
|---|---|---|
| text | string | Existing non-empty and maximum-length validation remains unchanged and is performed only after authentication. |
| main_ideas | boolean | Existing optional processing flag remains unchanged and is validated only after authentication. |
| bearer credential | HTTP header | `Authorization: Bearer <current Clerk session token>`; not part of JSON. |

## Authentication outcome

Represents the decision made before body processing.

| Outcome | Condition | HTTP status | OpenRouter |
|---|---|---:|---|
| accepted | Signature, allowed algorithm, issuer and time claims pass | Continue existing validation/summary flow | Exactly one call for a valid request |
| rejected | Header absent/malformed; token invalid, expired, bad signature, wrong issuer or no matching signing key | 401 | No call |
| verifier unavailable | JWKS cannot be fetched or is unusable, including network timeout | 503 | No call |

No identity or request state is stored after the request completes.
