# Registro de pruebas de integración

> **Nota:** Las siguientes pruebas se ejecutan de forma aislada o manual utilizando datos ficticios. No forman parte de la ejecución rutinaria de `pytest` para evitar dependencias de red o consumo de créditos de la API externa.

## Pruebas añadidas para la app1

Estas pruebas están pensadas para ser sencillas, ejecutables localmente y alineadas con los requisitos funcionales del ERS de la app1.

### APP1-PR-01

| Campo                  | Descripción                                                                   |
| ---------------------- | ----------------------------------------------------------------------------- |
| **ID de Prueba**       | APP1-PR-01                                                                    |
| **Fecha**              | 18/10/2026                                                                    |
| **Entorno**            | Local (Vite + Vitest)                                                         |
| **Comando / Acción**   | `cd app1/frontend && npm exec vitest run src/__tests__/App.spec.ts`           |
| **Resultado Esperado** | La aplicación renderiza el título principal y el área de texto del formulario |
| **Resultado Obtenido** | Verificado al ejecutar la prueba en entorno local                             |

### APP1-PR-02

| Campo                  | Descripción                                                             |
| ---------------------- | ----------------------------------------------------------------------- |
| **ID de Prueba**       | APP1-PR-02                                                              |
| **Fecha**              | 18/10/2026                                                              |
| **Entorno**            | Local (Vite + Vitest)                                                   |
| **Comando / Acción**   | `cd app1/frontend && npm exec vitest run src/__tests__/App.spec.ts`     |
| **Resultado Esperado** | El botón de envío aparece deshabilitado cuando no hay texto introducido |
| **Resultado Obtenido** | Verificado al ejecutar la prueba en entorno local                       |

### APP1-PR-03

| Campo                  | Descripción                                                                                      |
| ---------------------- | ------------------------------------------------------------------------------------------------ |
| **ID de Prueba**       | APP1-PR-03                                                                                       |
| **Fecha**              | 18/10/2026                                                                                       |
| **Entorno**            | Local (Vite + Vitest)                                                                            |
| **Comando / Acción**   | `cd app1/frontend && npm exec vitest run src/__tests__/App.spec.ts`                              |
| **Resultado Esperado** | El texto introducido se envía al servicio de resumen y aparece el resultado generado en pantalla |
| **Resultado Obtenido** | Verificado al ejecutar la prueba en entorno local                                                |

### APP1-PR-04

| Campo                  | Descripción                                                                                           |
| ---------------------- | ----------------------------------------------------------------------------------------------------- |
| **ID de Prueba**       | APP1-PR-04                                                                                            |
| **Fecha**              | 18/10/2026                                                                                            |
| **Entorno**            | Local (Vite + Vitest)                                                                                 |
| **Comando / Acción**   | `cd app1/frontend && npm exec vitest run src/__tests__/App.spec.ts`                                   |
| **Resultado Esperado** | Si falla la generación del resumen, la interfaz muestra un mensaje de error claro sin romper la vista |
| **Resultado Obtenido** | Verificado al ejecutar la prueba en entorno local                                                     |

### Observaciones

- Las pruebas son de frontend y se ejecutan con Vitest.
- No dependen de una API externa real ni de créditos de OpenRouter.
- Están diseñadas para validar la lógica visible del usuario descrita en el ERS: entrada de texto, validación básica, envío y gestión de errores.

### APP1-PR-05

| Campo                  | Descripción                                                                                                               |
| ---------------------- | ------------------------------------------------------------------------------------------------------------------------- |
| **ID de Prueba**       | APP1-PR-05                                                                                                                |
| **Fecha**              | 02/11/2026                                                                                                                |
| **Entorno**            | Local (Python 3.13.5, pytest, FastAPI TestClient)                                                                         |
| **Comando / Acción**   | `cd app1 && python -m pytest -q`                                                                                          |
| **Resultado Esperado** | Las pruebas de rutas y del cliente OpenRouter verifican entrada válida, validación, límite, error del proveedor y timeout |
| **Resultado Obtenido** | 18 pruebas superadas                                                                                                      |

### APP1-PR-06

| Campo                  | Descripción                                                                          |
| ---------------------- | ------------------------------------------------------------------------------------ |
| **ID de Prueba**       | APP1-PR-06                                                                           |
| **Fecha**              | 02/11/2026                                                                           |
| **Entorno**            | Revisión de código y pruebas HTTP locales                                            |
| **Comando / Acción**   | Pruebas de integración añadidas en `app1/backend/tests/test_routes.py`               |
| **Resultado Esperado** | Las respuestas de error mantienen JSON con `detail` y distinguen HTTP 422, 502 y 504 |
| **Resultado Obtenido** | Verificado en las tres pruebas de contrato incluidas en las 18 pruebas superadas     |

### Estado de ejecución del frontend de App 1

Se ampliaron las pruebas de `app1/frontend/src/__tests__/App.spec.ts` para comprobar el mensaje de error y el estado de carga. El 02/11/2026 se ejecutaron 8 pruebas con Vitest y la compilación del frontend terminó correctamente. La instalación desde un entorno limpio se mantiene pendiente.

```bash
cd app1/frontend
npm ci
npm exec vitest run
npm run build
```

## Pruebas documentadas para la App 2

La suite de la app2 ya está implementada en el frontend y cubre el flujo principal de autenticación y resumen. A continuación se documentan de forma individual siguiendo el mismo formato del template.

### APP2-PR-01

| Campo                  | Descripción                                                                                                           |
| ---------------------- | --------------------------------------------------------------------------------------------------------------------- |
| **ID de Prueba**       | APP2-PR-01                                                                                                            |
| **Fecha**              | 28/10/2026                                                                                                            |
| **Entorno**            | Local (Vite + Vitest)                                                                                                 |
| **Comando / Acción**   | `cd app2/frontend && npm exec vitest run src/__tests__/App.spec.ts`                                                   |
| **Resultado Esperado** | Se muestran las opciones de iniciar sesión y crear cuenta, y no aparece el área de entrada hasta autenticar la sesión |
| **Resultado Obtenido** | Verificado en la suite existente para la app2                                                                         |

### APP2-PR-02

| Campo                  | Descripción                                                                                              |
| ---------------------- | -------------------------------------------------------------------------------------------------------- |
| **ID de Prueba**       | APP2-PR-02                                                                                               |
| **Fecha**              | 28/10/2026                                                                                               |
| **Entorno**            | Local (Vite + Vitest)                                                                                    |
| **Comando / Acción**   | `cd app2/frontend && npm exec vitest run src/__tests__/App.spec.ts`                                      |
| **Resultado Esperado** | La petición al backend incluye el token Bearer, el cuerpo del resumen y las opciones de resumen elegidas |
| **Resultado Obtenido** | Verificado en la suite existente para la app2                                                            |

### APP2-PR-03

| Campo                  | Descripción                                                                                                     |
| ---------------------- | --------------------------------------------------------------------------------------------------------------- |
| **ID de Prueba**       | APP2-PR-03                                                                                                      |
| **Fecha**              | 28/10/2026                                                                                                      |
| **Entorno**            | Local (Vite + Vitest)                                                                                           |
| **Comando / Acción**   | `cd app2/frontend && npm exec vitest run src/__tests__/App.spec.ts`                                             |
| **Resultado Esperado** | Se manejan correctamente los errores 401 y 503 de autenticación, manteniendo el contenido del texto introducido |
| **Resultado Obtenido** | Verificado en la suite existente para la app2                                                                   |

### APP2-PR-04

| Campo                  | Descripción                                                                                                                        |
| ---------------------- | ---------------------------------------------------------------------------------------------------------------------------------- |
| **ID de Prueba**       | APP2-PR-04                                                                                                                         |
| **Fecha**              | 28/10/2026                                                                                                                         |
| **Entorno**            | Local (Vite + Vitest)                                                                                                              |
| **Comando / Acción**   | `cd app2/frontend && npm exec vitest run src/__tests__/App.spec.ts`                                                                |
| **Resultado Esperado** | Se renderizan las secciones del resumen, ideas principales y glosario, y las acciones de copiar y exportar funcionan correctamente |
| **Resultado Obtenido** | Verificado en la suite existente para la app2                                                                                      |

### APP2-PR-05

| Campo                  | Descripción                                                                                                                          |
| ---------------------- | ------------------------------------------------------------------------------------------------------------------------------------ |
| **ID de Prueba**       | APP2-PR-05                                                                                                                           |
| **Fecha**              | 31/10/2026                                                                                                                           |
| **Entorno**            | Local (pytest + FastAPI TestClient)                                                                                                  |
| **Comando / Acción**   | `cd app2/backend && python -m pytest -q tests/test_services.py`                                                                      |
| **Resultado Esperado** | El servicio maneja respuesta válida, timeout, error de conexión, respuesta vacía, JSON inválido y contenido que no cumple el esquema |
| **Resultado Obtenido** | Verificado al ejecutar la suite de `test_services.py`                                                                                |

### APP2-PR-06

| Campo                  | Descripción                                                                                                                                                |
| ---------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **ID de Prueba**       | APP2-PR-06                                                                                                                                                 |
| **Fecha**              | 31/10/2026                                                                                                                                                 |
| **Entorno**            | Local (Vite + Vitest + JSDOM)                                                                                                                              |
| **Comando / Acción**   | `cd app2/frontend && npm exec vitest run src/__tests__/App.spec.ts`                                                                                        |
| **Resultado Esperado** | La UI maneja texto vacío, límite de 5000 caracteres, carga efectiva de `.txt` y `.md`, rechazo de extensiones no permitidas y errores de servicio visibles |
| **Resultado Obtenido** | Verificado al ejecutar la suite existente de la app2 y las pruebas añadidas para validación de entrada y archivo                                           |

### APP2-PR-07

| Campo                  | Descripción                                                                                               |
| ---------------------- | --------------------------------------------------------------------------------------------------------- |
| **ID de Prueba**       | APP2-PR-07                                                                                                |
| **Fecha**              | 03/11/2026                                                                                                |
| **Entorno**            | Local (Vite + Vitest + JSDOM)                                                                             |
| **Comando / Acción**   | `cd app2/frontend && npm exec vitest run src/__tests__/App.spec.ts`                                       |
| **Resultado Esperado** | No se envía la petición cuando el texto está vacío o contiene únicamente espacios, saltos de línea o tabs |
| **Resultado Obtenido** | Verificado al ejecutar la suite del frontend de app2 y comprobar que no se dispara la llamada al backend  |

### APP2-PR-08

| Campo                  | Descripción                                                                                                  |
| ---------------------- | ------------------------------------------------------------------------------------------------------------ |
| **ID de Prueba**       | APP2-PR-08                                                                                                   |
| **Fecha**              | 03/11/2026                                                                                                   |
| **Entorno**            | Local (Vite + Vitest + JSDOM)                                                                                |
| **Comando / Acción**   | `cd app2/frontend && npm exec vitest run src/__tests__/App.spec.ts`                                          |
| **Resultado Esperado** | La petición no se dispara si el usuario está autenticado pero no hay token de sesión disponible              |
| **Resultado Obtenido** | Verificado al ejecutar la suite del frontend de app2 y confirmar que la llamada a `axios.post` no se ejecuta |

### APP2-PR-09

| Campo                  | Descripción                                                                                                                       |
| ---------------------- | --------------------------------------------------------------------------------------------------------------------------------- |
| **ID de Prueba**       | APP2-PR-09                                                                                                                        |
| **Fecha**              | 03/11/2026                                                                                                                        |
| **Entorno**            | Local (Vite + Vitest + JSDOM)                                                                                                     |
| **Comando / Acción**   | `cd app2/frontend && npm exec vitest run src/__tests__/App.spec.ts`                                                               |
| **Resultado Esperado** | Cuando la API responde solo con el resumen y no incluye ideas principales ni glosario, la interfaz renderiza únicamente ese texto |
| **Resultado Obtenido** | Verificado al ejecutar la suite del frontend de app2 y comprobar que no aparecen las secciones opcionales                         |

## Verificación manual de App 2 en AWS EC2

> App 2 se publica mediante Docker Compose en AWS EC2. Esta comprobación debe realizarse desde el dominio o la IP pública de la instancia.

| Campo                        | Valor |
| ---------------------------- | ----- |
| **URL pública del frontend** |       |
| **Fecha de comprobación**    |       |
| **Resultado**                |       |
| **Observaciones**            |       |

### Checklist

- [ ] Acceso a la URL pública del frontend.
- [ ] Autenticación mediante Clerk.
- [ ] Generación de un resumen con una entrada válida.
- [ ] Rechazo de una petición al backend sin token.
- [ ] Rechazo de una petición con token inválido.
- [ ] Comprobación de errores y CORS desde el navegador.

---

## Resumen de ejecución de la revisión del 03/11/2026

| Suite               | Resultado observado en este entorno    | Detalle                                                                                 |
| ------------------- | -------------------------------------- | --------------------------------------------------------------------------------------- |
| App 1 backend       | 18/18 pruebas superadas                | `PYTHONPATH=app1 pytest -q app1/backend/tests`                                          |
| App 1 arranque HTTP | Correcto                               | `TestClient` obtuvo HTTP 200 en `/openapi.json` y detectó `/api/resumir`                |
| App 1 frontend      | 8 pruebas superadas y build correcto   | `npm.cmd exec vitest run` y `npm.cmd run build` desde `app1/frontend`                   |
| App 2 backend       | 32 pruebas superadas                   | `uv run pytest -q app2/backend/tests`                                                   |
| App 2 frontend      | 9/9 pruebas superadas y build correcto | `npm exec vitest run src/__tests__/App.spec.ts` y `npm run build` desde `app2/frontend` |
| Docker              | No ejecutado                           | No hay cliente Docker disponible en este entorno                                        |

Comprobaciones de bloqueo de dependencias:

```bash
uv lock --check --offline --directory app1
uv lock --check --offline --directory app2/backend
```

Ambos archivos de bloqueo se validaron correctamente. La validación del lock no equivale a instalar todas las dependencias ni a construir imágenes Docker.

Para completar la verificación en un equipo con conexión y Docker:

```bash
cd app1
uv sync --locked
uv run pytest -q
cd frontend
npm ci
npm exec vitest run
npm run build

cd ../../app2/backend
uv sync --locked
uv run pytest -q tests

cd ../frontend
npm ci
npm exec vitest run
npm run build

cd ../infra
docker compose --env-file .env -f compose.yaml config
docker compose --env-file .env -f compose.yaml up --build -d
docker compose --env-file .env -f compose.yaml ps
```
