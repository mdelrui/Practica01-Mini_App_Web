# Quickstart: validación del resumen con la arquitectura actual

## Prerrequisitos

- Python 3.12+
- Node.js 22+
- Variables de entorno configuradas para la app2:
    - `CLERK_ISSUER`
    - `CLERK_JWKS_URL` o la configuración equivalente para la validación de tokens
    - `OPENROUTER_API_KEY`
    - opcionalmente `CORS_ORIGINS`, `OPENROUTER_MODEL`, `CLERK_JWKS_TIMEOUT`

## 1) Arrancar el backend

```bash
cd app2/backend
python -m uvicorn main:app --reload
```

**Resultado esperado**: el servicio FastAPI escuchando en `http://127.0.0.1:8000`.

## 2) Arrancar el frontend

```bash
cd app2/frontend
npm install
npm run dev
```

**Resultado esperado**: la SPA de Vue queda disponible en el puerto de Vite (por defecto `http://localhost:5173`).

## 3) Validar el flujo principal

1. Inicia sesión en la UI con Clerk.
2. Escribe o pega un texto en el formulario.
3. Selecciona la longitud del resumen.
4. Activa `Ideas principales` y/o `Glosario` si procede.
5. Pulsa el botón principal para enviar la solicitud.
6. Comprueba que el backend responde con un JSON estructurado y que la interfaz renderiza los bloques correspondientes.

## 4) Validar respuestas de error

### Autenticación inválida

- Eliminar o invalidar el token de sesión.
- Enviar la petición desde el frontend.
- Comprobar que aparece el mensaje de sesión no válida y que no se invoca OpenRouter.

### Verificador no disponible

- Forzar un error de JWKS con la configuración del backend.
- Esperar `HTTP 503` con el código de error de disponibilidad y sin procesamiento adicional.

### Proveedor IA no disponible

- Simular un fallo de OpenRouter o de conexión.
- Esperar un error controlado y la interfaz debe mostrar el mensaje correspondiente.

## 5) Validar exportación y copia

- En la pantalla con resultado, pulsar “copiar” sobre cada bloque y comprobar la acción con el navegador cuando el portapapeles esté disponible.
- Exportar el contenido como `.txt` y `.md` y comprobar que se genera un archivo local con el formato esperado.

## 6) Validar el caso de archivo local

- Cargar un archivo `.txt` o `.md` desde el navegador.
- Comprobar que su contenido entra en el área de texto y no se envía al backend como archivo.
- Probar un archivo no permitido o mayor de 1 MB y confirmar que se muestra el error del frontend.

## 7) Verificación de datos esperados

La llamada exitosa debe producir un payload equivalente a:

```json
{
	"summary": "Texto resumido",
	"main_ideas": ["Idea 1", "Idea 2"],
	"glossary": [{ "concept": "Término", "definition": "Definición breve" }]
}
```

Y la respuesta debe corresponder al contrato definido en el backend y en la especificación de la feature.
