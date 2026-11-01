# Registro de Pruebas de Integración Reales

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

## Pruebas documentadas para la app2

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

## Verificación manual de Vercel para App 2 (pendiente de completar)

> Esta comprobación no se marca como realizada. Los campos quedan vacíos para que se complete manualmente en el entorno real de Vercel por la persona responsable.

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
