# Registro de Pruebas de Integración Reales

> **Nota:** Las siguientes pruebas se ejecutan de forma aislada o manual utilizando datos ficticios. No forman parte de la ejecución rutinaria de `pytest` para evitar dependencias de red o consumo de créditos de la API externa.

## Ficha de Registro de Prueba - TEMPLATE PARA COPIA Y PEGA

| Campo                  | Descripción / Valor de ejemplo                                                                                         |
| ---------------------- | ---------------------------------------------------------------------------------------------------------------------- |
| **ID de Prueba**       | PR-01 (Ej: PR-01-Exito, PR-02-Error)                                                                                   |
| **Fecha**              | DD/MM/AAAA                                                                                                             |
| **Entorno**            | [Ej: Local (Uvicorn + Vite dev server) / Staging]                                                                      |
| **Comando / Acción**   | `pytest tests/integration/test_api_integration.py -m integration` o prueba manual vía interfaz                         |
| **Resultado Esperado** | Código HTTP esperado (ej. 200 o 422/502), presencia de claves JSON estructuradas (sin validar texto literal de la IA). |
| **Resultado Obtenido** | [Descripción de lo que realmente ocurrió al ejecutar la prueba]                                                        |

**PRUEBA 01 - PR-01**

| Campo                  | Descripción / Valor de ejemplo |
| ---------------------- | ------------------------------ |
| **ID de Prueba**       | PR-01                          |
| **Fecha**              | DD/MM/AAAA                     |
| **Entorno**            |                                |
| **Comando / Acción**   |                                |
| **Resultado Esperado** |                                |
| **Resultado Obtenido** |                                |

## Pruebas añadidas para la app1

Estas pruebas están pensadas para ser sencillas, ejecutables localmente y alineadas con los requisitos funcionales del ERS de la app1.

| ID de prueba | Objetivo                                                                                  | Comando de ejecución                                                | Resultado esperado                                                            |
| ------------ | ----------------------------------------------------------------------------------------- | ------------------------------------------------------------------- | ----------------------------------------------------------------------------- |
| APP1-PR-01   | Comprobar que la interfaz muestra el título y el área de texto principal                  | `cd app1/frontend && npm exec vitest run src/__tests__/App.spec.ts` | La aplicación renderiza correctamente el formulario y el texto del encabezado |
| APP1-PR-02   | Verificar que el botón de envío queda deshabilitado si el usuario no ha introducido texto | `cd app1/frontend && npm exec vitest run src/__tests__/App.spec.ts` | El botón aparece desactivado en el estado inicial                             |
| APP1-PR-03   | Confirmar que el texto se envía al backend y se visualiza el resumen devuelto             | `cd app1/frontend && npm exec vitest run src/__tests__/App.spec.ts` | Se llama al servicio de resumen y aparece el texto del resumen en pantalla    |
| APP1-PR-04   | Comprobar que la interfaz informa al usuario si ocurre un error al generar el resumen     | `cd app1/frontend && npm exec vitest run src/__tests__/App.spec.ts` | Se muestra el mensaje de error correspondiente sin romper la vista            |

### Observaciones

- Las pruebas son de frontend y se ejecutan con Vitest.
- No dependen de una API externa real ni de créditos de OpenRouter.
- Están diseñadas para validar la lógica visible del usuario descrita en el ERS: entrada de texto, validación básica, envío y gestión de errores.

## Pruebas documentadas para la app2

La suite de la app2 ya está implementada en el frontend y cubre el flujo principal de autenticación y resumen. A continuación se documentan de forma simple para ejecutar la validación localmente sin añadir más pruebas ni modificar el código existente.

| ID de prueba | Objetivo                                                                                                            | Comando de ejecución                                                | Resultado esperado                                                                                                |
| ------------ | ------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------- |
| APP2-PR-01   | Comprobar que la interfaz muestra las acciones de inicio de sesión y registro cuando el usuario no está autenticado | `cd app2/frontend && npm exec vitest run src/__tests__/App.spec.ts` | Se visualizan los botones de iniciar sesión y crear cuenta, y el área de entrada no aparece                       |
| APP2-PR-02   | Validar que el formulario envía el token Bearer junto con el JSON de resumen y las opciones elegidas                | `cd app2/frontend && npm exec vitest run src/__tests__/App.spec.ts` | La llamada HTTP se realiza con la ruta de resumen, el cuerpo correcto y el encabezado `Authorization: Bearer ...` |
| APP2-PR-03   | Comprobar los errores de autenticación del backend (401 y 503) y que el texto del usuario se conserva               | `cd app2/frontend && npm exec vitest run src/__tests__/App.spec.ts` | Se muestran mensajes de sesión inválida o temporalmente no verificada y el contenido introducido no se pierde     |
| APP2-PR-04   | Verificar que se renderizan las secciones de resultado y que funcionan las acciones de copiar y exportar            | `cd app2/frontend && npm exec vitest run src/__tests__/App.spec.ts` | Aparecen resumen, ideas principales y glosario; las acciones de copiar y exportar producen salida esperada        |

### Observaciones de la app2

- La validación se centra en flujos reales de la aplicación: autenticación con Clerk, envío autenticado a `/resumir`, manejo de errores y presentación del resultado.
- Las pruebas están diseñadas para ejecutar localmente con Vitest y no requieren llamadas reales a servicios externos.
- El objetivo principal es comprobar la lógica visible del usuario en la SPA y la integración del token de sesión con la petición al backend.
