# Contract: API de resumen

## Endpoint

`POST /resumir`

## Authentication

- Header required: `Authorization: Bearer <clerk-token>`
- If missing, malformed, expired, or invalid, the backend returns `401`.
- If the JWKS verifier is unreachable or unusable, the backend returns `503`.

## Request body

```json
{
	"text": "Texto a resumir",
	"main_ideas": true,
	"glossary": true,
	"summary_length": "estándar"
}
```

### Field rules

- `text`: required string, 1..5000 chars.
- `main_ideas`: optional boolean, default `false`.
- `glossary`: optional boolean, default `false`.
- `summary_length`: optional enum value: `breve`, `estándar`, `detallado`.

## Success response

```json
{
	"summary": "Resumen principal del texto",
	"main_ideas": ["Idea principal 1", "Idea principal 2"],
	"glossary": [
		{
			"concept": "Término",
			"definition": "Definición breve"
		}
	]
}
```

## Error responses

### 401 Unauthorized

```json
{
	"error": {
		"codigo": "AUTH_INVALID",
		"mensaje": "Autenticación requerida o sesión no válida."
	}
}
```

### 503 Service unavailable

```json
{
	"error": {
		"codigo": "AUTH_UNAVAILABLE",
		"mensaje": "No se pudo verificar la sesión temporalmente. Inténtalo más tarde."
	}
}
```

### 502/504 provider errors

```json
{
	"error": {
		"codigo": "IA_NO_DISPONIBLE",
		"mensaje": "No se ha podido conectar con el proveedor de IA."
	}
}
```

## Notes

- The file upload flow is browser-only; the server only receives the text payload.
- Validation is implemented with Pydantic in the backend and by the browser-side form logic in the frontend.
- The contract is intentionally minimal and matches the current Vue + FastAPI implementation.
