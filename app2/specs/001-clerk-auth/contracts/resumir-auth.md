# HTTP Contract: Protected Summary Request

## Endpoint

`POST /resumir` (existing endpoint; no new route)

## Request

```http
POST /resumir
Content-Type: application/json
Authorization: Bearer <current Clerk session token>
```

```json
{
  "text": "Texto a resumir",
  "main_ideas": true
}
```

The JSON shape, route, and successful response schema remain unchanged. Obtain a fresh/current token from Clerk when submitting; do not put it in the JSON body, query string, logs, or persisted client state.

## Processing order

1. Inspect and verify the bearer credential before parsing or validating the JSON body.
2. If credentials are rejected, return 401 without processing the body.
3. If the verification service/JWKS is unavailable, return 503 without processing the body.
4. Only after successful verification, apply the existing request validation and call the existing summary service.
5. For one valid authenticated request, preserve exactly one OpenRouter call and the existing success payload.

## Responses

| Status | Meaning | Response body | OpenRouter call |
|---:|---|---|---|
| 200 | Authenticated, valid request processed | Existing summary JSON response | Exactly one |
| 401 | Missing/malformed bearer header or invalid/expired token, signature, issuer, algorithm, or signing-key match | Generic `{"error":{"codigo":"AUTH_INVALID","mensaje":"Autenticación requerida o sesión no válida."}}` | None |
| 422 | Authenticated request has invalid JSON or fails existing input validation | Existing FastAPI validation error contract | None |
| 502 | Existing provider or invalid-provider-response error | Existing controlled IA error contract | Only if authentication and input validation succeeded |
| 503 | JWKS/Clerk verification dependency unavailable or unusable | Generic `{"error":{"codigo":"AUTH_UNAVAILABLE","mensaje":"No se pudo verificar la sesión temporalmente. Inténtalo más tarde."}}` | None |
| 504 | Existing provider timeout | Existing controlled IA error contract | Only if authentication and input validation succeeded |

Messages must not include token contents, key material, raw JWKS responses, stack traces, or secrets. The exact error-code strings are contract proposals to be implemented consistently; response statuses and fail-closed behavior are mandatory.

## CORS

The browser request uses the `Authorization` header. Verify that the deployed API's CORS preflight permits this header for the configured SPA origin. The current FastAPI CORS configuration allows all headers; keep or narrow it according to the existing deployment policy, without adding credentials/cookies for bearer-token authentication unless independently required.

## Automated contract checks

- Missing header, wrong scheme, blank token, malformed/expired/bad-signature/wrong-issuer token: HTTP 401.
- Missing/invalid credential with malformed JSON: HTTP 401 takes precedence over body validation.
- JWKS connection failure, timeout, or unusable key source: HTTP 503.
- All rejected/unavailable cases: zero calls to the summary/OpenRouter service.
- Valid token and valid JSON: existing successful response and exactly one mocked summary/OpenRouter call.
- Token is not included in body, query, response, logs, or rendered UI.
