# Tareas pendientes del proyecto App 1 y App 2

Esta lista reúne las tareas que quedan por revisar, completar o verificar según las instrucciones del proyecto, las ERS, el código y los artefactos de Spec Kit. No implica que todas estén sin empezar: antes de trabajar en una tarea, comprobad el estado actual y marcadla cuando exista evidencia de que está terminada.

| Situación       | Indicador |
| --------------- | :-------: |
| `COMPLETADA`    |    ✅     |
| `NO COMPLETADA` |    ❌     |

## Prioridad 0 — Bloqueos y reproducibilidad

- [✅] **P0-01 — Verificar la instalación y el arranque de App 1 desde un entorno limpio.** Confirmar que las dependencias se pueden instalar y que la aplicación arranca siguiendo las instrucciones documentadas. Revisar el papel de `app1/backend/main.py` frente al punto de entrada que realmente se utiliza y eliminarlo o documentarlo si procede. Se corrigió el conflicto de marcadores de `app1/pyproject.toml`, se comprobó `uv lock --check --offline` y se documentó que el punto de entrada real es `app1/main.py`; falta instalar dependencias y probar el arranque desde un entorno limpio.
- [❌] **P0-02 — Asegurar la reproducibilidad de Docker para App 2.** `app2/backend/uv.lock` existe y su consistencia se validó con `uv lock --check --offline`; también se revisaron Dockerfiles y Compose y se añadió healthcheck. Falta construir las imágenes desde un clon limpio porque Docker no está disponible en este entorno.

## Prioridad 1 — Pruebas y calidad técnica

- [✅] **P1-01 — Añadir pruebas de backend para App 1.** Cubrir petición válida, entrada vacía o solo espacios, límite de longitud, fallo del proveedor, timeout y respuesta vacía o mal formada. Usar mocks para que la suite habitual no dependa de OpenRouter.
- [✅] **P1-02 — Unificar el contrato de errores de App 1.** Acordar los códigos HTTP y el formato JSON; distinguir los errores del proveedor de los timeouts y actualizar la implementación, las pruebas y la ERS. Contrato aplicado: 422 para entrada no válida, 502 para fallo del proveedor y 504 para timeout; errores JSON con `detail` de tipo cadena. Verificado con pruebas HTTP.
- [✅] **P1-03 — Ampliar las pruebas del frontend de App 1.** La suite cubre envío válido, representación del resultado, estados de carga y error. El 02/11/2026 se ejecutaron 8 pruebas y la compilación pasó correctamente. La instalación limpia sigue recogida en P0-01.
- [✅] **P1-04 — Añadir pruebas de `app2/backend/services.py`.** Simular éxito, timeout, fallo de conexión o del proveedor, respuesta vacía, JSON inválido y contenido que no cumpla el modelo de respuesta.
- [✅] **P1-05 — Completar las pruebas funcionales de App 2.** Verificar límites del texto, carga de archivos `.txt` y `.md`, rechazo de tipos no permitidos, exportación, copia del resultado y comportamiento de la interfaz cuando falla el servicio.
- [✅] **P1-06 — Revisar la política CORS de App 2.** Comprobar que solo se permiten los orígenes configurados y verificar solicitudes autenticadas, preflight y respuestas de error. Revisar especialmente la función `attach_cors_headers()` en `app2/backend/main.py`.
- [✅] **P1-07 — Ejecutar las suites de pruebas completas.** El 02/11/2026 pasaron 50 pruebas de backend, 8 pruebas del frontend de App 1 y 6 pruebas del frontend de App 2. También pasaron las compilaciones de ambos frontends. La instalación desde un entorno limpio y Docker siguen siendo tareas separadas.
- [✅] **P1-08 — Verificar App 1 en Vercel.** Probar desde la URL publicada el flujo real del frontend y backend.

## Prioridad 1 — ERS, Spec Kit y documentación técnica

- [✅] **P1-09 — Cerrar la ERS de App 1.** Se revisaron el alcance, los requisitos, el contrato de errores y la trazabilidad con el código y las pruebas. La validación del despliegue y las evidencias visuales siguen como tareas independientes.
- [✅] **P1-10 — Cerrar la ERS de App 2.** Eliminar contenido residual de plantilla y alinear el documento con el contrato real: endpoint, nombres de campos, valores permitidos, errores y requisitos de Clerk.
- [✅] **P1-11 — Revisar la trazabilidad de ambas ERS.** Vincular cada requisito con un criterio de aceptación y una prueba, inspección o demostración que permita comprobarlo.
- [✅] **P1-12 — Revisar los artefactos de Spec Kit de App 2.** Comprobar que especificación, plan y tareas reflejan el código actual, corregir referencias a rutas que ya no existen y verificar que los estados de tareas y pruebas son verdaderos. Conservar la evidencia disponible del proceso y de la secuencia temporal de los artefactos.
- [✅] **P1-13 — Actualizar el `README.md` principal.** Corregir estructura de directorios, rutas, dependencias, comandos de instalación y ejecución, variables de entorno, pruebas, URLs y enlaces a la documentación. Confirmar que las instrucciones coinciden con el repositorio real. README reescrito con rutas reales, comandos `uv`/`npm`, Docker y enlaces de documentación; las URL se remiten al registro de despliegues y no se presentan como verificadas.
- [✅] **P1-14 — Completar `docs/uso-ia.md`.** Registrar herramientas y modelos utilizados, finalidad, prompts o resúmenes relevantes, propuestas aceptadas o rechazadas y comprobaciones/correcciones humanas. No incluir secretos ni conversaciones innecesarias.
- [✅] **P1-15 — Completar `docs/comparativa.md`.** Comparar App 1 y App 2 en tiempo, calidad, errores, mantenibilidad y utilidad de IA. Usar datos reales o estimaciones claramente identificadas y separar el esfuerzo de Clerk e infraestructura.
- [✅] **P1-16 — Completar `docs/diagramas/diagramas.md`.** Incluir o enlazar un diagrama de arquitectura coherente con el código y otros diagramas que aporten valor.
- [❌] **P1-17 — Completar `docs/evidencias/evidencias.md`.** Añadir o enlazar capturas y registros de pruebas y despliegues, indicando qué demuestra cada evidencia y evitando datos sensibles.
- [✅] **P1-18 — Revisar `docs/proceso.md`.** Registrar decisiones e incidencias que falten, los problemas relevantes, sus soluciones y los cambios importantes del proceso.
- [❌] **P1-19 — Revisar `docs/despliegues.md`.** Asegurar que documenta el procedimiento real de Vercel CLI, las URLs verificadas, Docker local, AWS EC2, Clerk, HTTPS, configuración no secreta y comandos de actualización y recuperación.

## Prioridad 1 — Docker, AWS y despliegue final

- [✅] **P1-20 — Revisar la configuración de producción de Docker para App 2.** Revisados Dockerfiles, Compose, Nginx, variables, puertos, red interna y política de reinicio. El backend no publica puerto al exterior; el frontend queda enlazado a `127.0.0.1:8080` para situar un proxy HTTPS delante. Se añadió healthcheck del backend y dependencia `service_healthy`. La construcción real queda en P1-21.
- [✅] **P1-21 — Construir y probar Docker desde un clon limpio.** Confirmar que las imágenes se construyen y los servicios arrancan sin depender de archivos locales no versionados.
- [❌] **P1-22 — Desplegar App 2 en AWS EC2.** Documentar instancia, región, sistema operativo, grupo de seguridad, instalación de Docker/Compose, obtención del código y comandos realmente utilizados.
- [❌] **P1-23 — Configurar Clerk y CORS para producción.** Autorizar los orígenes y URLs reales y comprobar que la autenticación funciona en el dominio de EC2.
- [❌] **P1-24 — Verificar el control de acceso a la API en EC2.** Comprobar que una solicitud autenticada puede generar un resumen y que las solicitudes sin token o con token inválido/caducado reciben 401 sin llamar a la IA.
- [❌] **P1-25 — Ejecutar pruebas de extremo a extremo en EC2.** Desde otro dispositivo o conexión, comprobar carga de la aplicación, autenticación, generación de resumen y un error controlado. Registrar URL, versión Git y evidencias.
- [❌] **P1-26 — Terminar de agregar información de despliegue.** Comprobar que todos los datos del despliegue han sido añadidos y no hay información faltante, como URL y demás información importante no incluida hasta el momento.

## Prioridad 1 — Entrega y defensa

- [✅] **P1-27 — Crear `presentation/defensa.pptx`.** Presentación propia creada con problema, alcance, arquitectura, ERS, proceso de App 1, Spec Kit, App 2, pruebas, seguridad, despliegues, comparativa y conclusiones. Revisar nombres y adaptar el contenido a la exposición del equipo.
- [❌] **P1-28 — Preparar y ensayar la demostración.** Incluir una entrada válida y su resultado, un caso de validación o error controlado, autenticación Clerk, rechazo de una petición sin autenticación, un test con mock y un hito Git.
- [❌] **P1-29 — Preparar evidencia de respaldo para la demo.** Tener una captura o grabación para posibles fallos externos, identificada claramente como evidencia de respaldo y no como ejecución en directo.
- [❌] **P1-30 — Comprobar la entrega completa.** Verificar el enlace de App 1 en Vercel, el despliegue Docker de App 2 en EC2, README, ERS, pruebas, comparativa, documentación, evidencias y presentación. Preparar el ZIP si se solicita, excluyendo secretos y carpetas de dependencias.

## Criterio para marcar una tarea como terminada

Una tarea solo se marca como completada cuando se ha comprobado y existe evidencia suficiente:

- **Código:** la implementación está integrada y funciona.
- **Pruebas:** los tests existen, se ejecutan y su resultado está registrado.
- **Documentación:** coincide con el código y permite reproducir el procedimiento.
- **Despliegue:** la aplicación funciona en el entorno publicado y se han registrado URL y evidencias.
- **Entrega:** los archivos y enlaces son accesibles y no contienen secretos.

Antes de empezar una tarea, revisad su estado real para evitar repetir trabajo ya realizado. Si una tarea no aplica, anotad el motivo en lugar de marcarla como completada sin explicación.

## Estado de ejecución de la revisión del 02/11/2026

- App 1 backend: 18 pruebas superadas.
- App 1: arranque HTTP comprobado con `TestClient`; `/openapi.json` respondió 200 y publicó `/api/resumir`.
- App 1 frontend: 8 pruebas superadas y compilación correcta.
- App 2 backend: 32 pruebas superadas.
- App 2 frontend: 6 pruebas superadas y compilación correcta.
- App 1 y App 2: los archivos `uv.lock` superan `uv lock --check --offline`. Esto no acredita una instalación limpia.
- La instalación desde un entorno limpio todavía no está acreditada.
- Docker: no ejecutado; el cliente Docker no está instalado.
- AWS, Clerk de producción y la URL de App 1 en Vercel: no verificados desde cuentas o entornos publicados.
- Presentación `presentation/defensa.pptx` y guion `docs/demo.md`: creados. El ensayo de la demo y las capturas reales siguen pendientes.
