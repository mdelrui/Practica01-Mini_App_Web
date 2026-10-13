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
