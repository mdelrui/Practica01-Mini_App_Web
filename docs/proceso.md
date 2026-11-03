# Registro de Proceso y Decisiones

Este documento sirve como registro oficial de bitácora para el equipo de desarrollo. Su propósito es documentar de forma trazable las decisiones técnicas clave tomadas durante el diseño y la implementación, así como los problemas imprevistos y su correspondiente resolución conforme vayan ocurriendo.

## Historial de Decisiones y Problemas

## 18/10/2026 - Base arquitectónica y alcance de la App 2

- **Tipo:** Decisión de Diseño
- **Contexto / Problema:** La App 2 debía resolver la misma necesidad que la App 1 (resumir texto) pero añadiendo autenticación y funcionalidades complementarias sin aumentar la complejidad del proyecto. La documentación base de la práctica y la ERS de la App 1 indicaban un enfoque simple, con frontend y backend separados, sin persistencia ni múltiples pantallas.
- **Decisión / Solución adoptada:** Se reutilizó la idea central de la App 1 como punto de partida y se diseñó una SPA de una sola pantalla con un formulario, validación del backend, integración con OpenRouter desde el backend y una capa adicional de autenticación con Clerk. Se mantuvo la restricción de no guardar entradas ni resultados en base de datos ni en servidor.
- **Evidencia visual (Opcional):** El esquema de arquitectura de la ERS de App 2 y la comparación entre App 1 y App 2 muestran este patrón: frontend con Vue, backend con FastAPI, acceso a la IA únicamente desde servidor y salida sin persistencia.

## 21/10/2026 - Integración de Clerk como control de acceso

- **Tipo:** Decisión de Diseño
- **Contexto / Problema:** La práctica exigía que la App 2 protegiese el procesamiento del texto con autenticación externa sin implementar gestión propia de usuarios. El riesgo era permitir llamadas no autorizadas a la API de IA o usar el servicio sin validar el token.
- **Decisión / Solución adoptada:** Se integró Clerk para que el usuario inicie sesión desde la misma pantalla de la aplicación. El frontend obtiene el token de sesión y lo envía en la cabecera `Authorization: Bearer` a cada petición relevante. En el backend, la validación comprueba firma, emisor y caducidad antes de permitir el acceso a la lógica de resumen. Si el token es ausente, inválido o caducado, la respuesta es 401 y no se llama a OpenRouter.
- **Evidencia visual (Opcional):** La ERS de la App 2 recoge el flujo de autenticación, los requisitos RF-08 y los criterios de aceptación de seguridad del token, además de la arquitectura que muestra la interacción entre Frontend, Clerk y Backend.

## 28/10/2026 - Nuevas features de resumen y salida del resultado

- **Tipo:** Decisión de Diseño
- **Contexto / Problema:** La App 2 debía ampliar la funcionalidad base de la App 1 con opciones de personalización y utilidad real para el usuario: longitud, ideas principales, glosario, copia y exportación del resultado. El diseño debía seguir siendo una sola pantalla y evitar complejidad innecesaria.
- **Decisión / Solución adoptada:** Se incorporó un flujo único de envío en el que la petición incluye texto, longitud del resumen y flags de ideas/principales y glosario. La respuesta del backend se presenta en secciones diferenciadas en la interfaz y se habilitaron dos acciones sobre el resultado: copiar al portapapeles y exportar en `.txt` o `.md` desde el navegador. Todo ello se mantiene sin persistencia ni almacenamiento del contenido fuera del usuario.
- **Evidencia visual (Opcional):** La ERS de App 2 documenta RF-05, RF-06, RF-07, RF-09 y RF-10, así como la vista única principal y la interfaz de usuario en la misma pantalla.

## 28/10/2026 - Validación del estado real y revisión documental

- **Tipo:** Incidencia o Problema
- **Contexto / Problema:** Durante la revisión del proyecto hubo riesgo de confundir “código presente” con “funcionalidad realmente verificada”. La documentación debía reflejar el estado real de la implementación y no dejar marcas de plantillas o supuestos no confirmados.
- **Decisión / Solución adoptada:** Se revisó la implementación existente, la cobertura de pruebas del backend y del frontend, y la propia ERS para distinguir claramente lo validado de lo hipotético. Se actualizó el historial del documento y se eliminaron elementos de plantilla residuales, dejando la especificación alineada con la app actual y con la validación real de requisitos.
- **Evidencia visual (Opcional):** La ERS de la App 2 incorpora el catálogo de requisitos con estado “Validado”, y la documentación de pruebas y comparativa confirma que la base funcional y la autenticación fueron revisadas como parte del trabajo final.

## 28/10/2026 - Estado final de la documentación y del proceso

- **Tipo:** Decisión de Diseño
- **Contexto / Problema:** El proyecto necesitaba dejar un registro ordenado del trabajo realizado, su alcance y las decisiones esenciales para futuras revisiones o entregas. No se buscaba documentar cada línea de código, sino los puntos clave que afectaban al diseño, la seguridad y la funcionalidad.
- **Decisión / Solución adoptada:** Se consolidó un registro de proceso centrado en cuatro decisiones principales: base del producto, autenticación con Clerk, nuevas features de resumen y validación final. Esta bitácora deja constancia de qué se tomó como criterio de diseño y qué se confirmó con evidencia, sin incluir detalles no esenciales.
- **Evidencia visual (Opcional):** La documentación del repositorio (ERS App 1, ERS App 2, comparativa, despliegues y pruebas) sirve como soporte de estas decisiones y consolida la trazabilidad del proyecto.

## 03/11/2026 - Validación del estado real y revisión documental

- **Tipo:** Incidencia o Problema
- **Contexto / Problema:** Durante la revisión del proyecto hubo un problema de comprobación del input del usuario. La documentación establecía la comprobación de un input vacío antes de llamar al backend, pero la aplicación no comprobaba si el texto insertado estaba formado únicamente por espacios en blanco y/o saltos de línea.
- **Decisión / Solución adoptada:** Se revisó la implementación existente y la cobertura de pruebas del frontend. Se actualizó la función de llamada al backend desde el frontend para incluir esta situación y mostrar el mensaje correspondiente de error. Además se creó y documentó su correspondiente test en la documentación de la aplicación.
- **Evidencia visual (Opcional):** La documentación de pruebas incorpora la nueva prueba correspondiente a esta situación.
