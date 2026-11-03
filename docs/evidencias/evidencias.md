# Evidencias del proyecto

Este documento sirve como punto para demostrar las evidencias respecto al funcionamiento del proyecto, App 1 y App 2.

## Evidencias automatizadas disponibles

| ID    | Evidencia                | Qué demuestra                                                           | Ubicación / resultado                                                                               |
| ----- | ------------------------ | ----------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------- |
| EV-01 | Pruebas de backend App 1 | Validación de entrada, petición válida, timeout y errores del proveedor | `app1/backend/tests/`; 18 pruebas superadas el 02/11/2026 en el entorno de trabajo de revisión      |
| EV-02 | Pruebas frontend App 1   | Casos automatizados para formulario, envío, carga y error               | `app1/frontend/src/__tests__/App.spec.ts`; 8 pruebas superadas y compilación correcta el 02/11/2026 |
| EV-03 | Pruebas backend App 2    | Comportamiento del servicio de resumen y autenticación                  | `app2/backend/tests/`; 32 pruebas superadas el 02/11/2026                                           |
| EV-04 | Pruebas frontend App 2   | Comportamiento de la interfaz y flujos de autenticación                 | `app2/frontend/src/__tests__/`; 6 pruebas superadas y compilación correcta el 02/11/2026            |
| EV-05 | Diagramas del proyecto   | Arquitectura y flujos documentados                                      | `docs/diagramas/`                                                                                   |

## Evidencias visuales pendientes

| ID    | Captura o registro que debe añadirse | Qué debe mostrar                                                       | Estado                                 |
| ----- | ------------------------------------ | ---------------------------------------------------------------------- | -------------------------------------- |
| EV-06 | App 1, entrada y resumen             | Texto de prueba y resumen generado en la aplicación desplegada o local | Pendiente                              |
| EV-07 | App 1, validación                    | Mensaje visible ante entrada no válida o error controlado              | Pendiente                              |
| EV-08 | App 2, autenticación                 | Inicio de sesión de Clerk sin mostrar datos personales                 | Pendiente                              |
| EV-09 | App 2, resumen                       | Generación del resumen con las opciones disponibles                    | Pendiente                              |
| EV-10 | App 2, rechazo sin token             | Respuesta HTTP 401 ante petición no autenticada                        | Pendiente                              |
| EV-11 | Docker Compose                       | Salida de `docker compose ps` con los servicios activos                | Pendiente de nueva captura verificable |
| EV-12 | Vercel                               | URL y flujo de las dos aplicaciones comprobados en navegador           | Pendiente                              |
| EV-13 | AWS EC2                              | Instancia, URL HTTPS y prueba externa de la aplicación App 2           | Pendiente de despliegue                |
