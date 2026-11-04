# Comparativa App 1 y App 2

Este documento recoge una comparación práctica entre la App 1 y la App 2 del proyecto ResumidorIA, centrada en el tiempo invertido, la calidad del resultado, los errores detectados, la mantenibilidad y la utilidad real de la IA en cada una de las dos implementaciones.

## 1. Resumen ejecutivo

La App 1 sirvió como primera referencia de funcionalidad mínima: entrada de texto, validación básica y generación de un resumen. La App 2 mantiene esa función base pero añade autenticación con Clerk, control de longitud, ideas principales, glosario y exportación local. En términos de calidad técnica, App 2 tiene una estructura más robusta y mejor cubierta por pruebas, aunque también incorpora mayor complejidad de seguridad y manejo de errores.

### Tabla comparativa

| Dimensión      | App 1                           | App 2                                               | Observación                                              |
| -------------- | ------------------------------- | --------------------------------------------------- | -------------------------------------------------------- |
| Tiempo         | Menor complejidad y menos capas | Más tiempo por autenticación y validación           | App 2 requiere más revisión de integración               |
| Calidad        | Funcionalidad base suficiente   | Mejor estructura, validación y mensajes             | App 2 es más consistente con el contrato                 |
| Errores        | Menos dependencias externas     | Más puntos críticos: Clerk, CORS, OpenRouter        | Se resolvieron con pruebas y comprobación real           |
| Mantenibilidad | Estructura más simple           | Mejor separación frontend/backend                   | Más claramientos, pero también más superficie            |
| Utilidad de IA | Útil para síntesis básica       | Más útil por la personalización y JSON estructurado | La IA es más valiosa cuando se guía con un esquema claro |

---

## 2. Tiempo

### App 1

La App 1 fue más rápida de desarrollar en su fase inicial porque tenía un alcance más simple: un formulario, una sola llamada a la IA y una salida directa. Eso reducía el número de decisiones de diseño y de validación.

### App 2

La App 2 requirió más tiempo por varias razones:

- integración de autenticación con Clerk
- validación del token en el backend antes de llamar a la IA
- control de CORS y orígenes permitidos
- ajustes de contrato JSON
- revisión de errores

---

## 3. Calidad

La calidad se valora aquí por claridad del contrato, validaciones, mensajes de error y consistencia con la documentación. En este punto, App 2 está mejor alineada con la implementación:

- la entrada tiene validación reforzada por Pydantic
- la salida del backend está más estructurada
- la interfaz presenta errores y estados de carga de forma más clara
- la documentación técnica y las pruebas han sido revisadas con más detalle

En comparación, App 1 tenía una base funcional correcta pero menos cerrada técnicamente. App 2 presenta una mejor separación de responsabilidades y una experiencia más sólida para el usuario.

---

## 4. Errores y soluciones

### Ejemplo real 1: constructor de excepciones de OpenAI

Durante la revisión de las pruebas de backend, la implementación inicial de los mocks no coincidía con la firma real de las excepciones del SDK de OpenAI. Esta diferencia no era un problema funcional del proyecto, sino una discrepancia entre la API modelada y la API real instalada.

Solución aplicada:

- ajustar los mocks a las excepciones reales del SDK
- volver a ejecutar la suite
- verificar que la validación del backend era correcta con la respuesta real del entorno

### Ejemplo real 2: `DataTransfer` en JSDOM

La prueba de frontend para arrastrar un archivo fallaba en JSDOM porque el entorno no expone `DataTransfer` como un navegador real. Se evitó depender de una API específica del navegador y se validó el flujo con una simulación equivalente.

---

## 5. Mantenibilidad

App 1 es más fácil de mantener a corto plazo por su simplicidad. App 2, en cambio, gana en calidad de diseño:

- backend y frontend separados
- contratos más claros
- validación en varios niveles
- manejo de autenticación y errores explícito

La parte que resulta más difícil de mantener es la de seguridad y autenticación, porque cualquier cambio en Clerk, CORS o JWT exige revisión de integración. Sin embargo, este coste es razonable para una aplicación que debe proteger el acceso al proveedor de IA.

> La mantenibilidad de App 2 es, en conjunto, mejor que la de App 1, siempre que se respeten los contratos de entrada/salida y las pruebas se actualicen cuando cambie el entorno.

---

## 6. Utilidad de la IA

La IA resulta más útil en App 2 porque la aplicación guía la respuesta con un esquema más preciso:

- longitud del resumen configurable
- extracción de ideas principales y glosario opcionales
- validación del JSON para evitar salidas inconsistentes

La IA ayuda especialmente en tareas de síntesis, pero requiere revisiones humanas para confirmar que:

- el resumen conserva el sentido del texto original
- no se inventan hechos
- el formato JSON sigue siendo estable
- los mensajes de error no son ambiguos ni técnicos

---

## 7. Conclusión

La evolución de App 1 a App 2 es clara: se mantiene la utilidad principal de resumir texto, pero se mejora la robustez, la seguridad y la calidad del servicio. La App 2 es más compleja de implementar, pero también es más completa desde el punto de vista técnico y más preparada para validación real, despliegue y revisión académica.

La comparación no pretende decir que App 1 fuera _incorrecta_; más bien, App 2 refleja una segunda iteración mejor preparada para entorno real, autenticación y pruebas automatizadas.
