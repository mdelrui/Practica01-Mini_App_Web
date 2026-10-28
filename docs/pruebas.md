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

### Observaciones de la app2

- La validación se centra en flujos reales de la aplicación: autenticación con Clerk, envío autenticado a `/resumir`, manejo de errores y presentación del resultado.
- Las pruebas están diseñadas para ejecutar localmente con Vitest y no requieren llamadas reales a servicios externos.
- El objetivo principal es comprobar la lógica visible del usuario en la SPA y la integración del token de sesión con la petición al backend.
