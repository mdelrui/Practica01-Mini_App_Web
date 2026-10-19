# Tutorial de Spec Kit para vuestro proyecto Vue + FastAPI

Mi recomendación es que utilicéis Spec Kit para definir el proyecto, decidir cómo construirlo y dividir el trabajo en tareas pequeñas antes de pedirle a Copilot que programe. No necesitáis aprender todas las herramientas que aparecen en su documentación ni aplicar un proceso de desarrollo empresarial a una aplicación de una sola página.

Spec Kit está diseñado precisamente para estructurar el trabajo con un agente de IA mediante Spec-Driven Development (SDD): primero se define qué se quiere construir, después cómo se va a hacer y, por último, se implementa siguiendo las tareas generadas. Cada fase produce documentos Markdown que sirven de contexto para las siguientes.

En vuestro caso, ya tenéis tres decisiones importantes tomadas:

- Frontend: Vue 3, TypeScript y Vite.
- Backend: FastAPI, con una API que recibe datos del formulario y se comunica con OpenRouter.
- Interfaz: una única página con un formulario y una respuesta de IA que el frontend presenta de forma visual.

Todavía no habéis decidido la temática. Por tanto, lo ideal es empezar por definir las reglas de trabajo y concretar los requisitos funcionales, sin generar código innecesariamente pronto.

## 1. Entender qué aporta Spec Kit

> **Constitution**
>
> Las reglas que debe respetar todo el proyecto.<br/>
> Ejemplo: mantener una arquitectura sencilla, no introducir dependencias innecesarias y escribir pruebas para la lógica importante.
>
> **Specify**
>
> Qué debe hacer la aplicación y qué necesita el usuario.<br/>
> Ejemplo: introducir datos en un formulario, enviarlos y visualizar una respuesta estructurada.
>
> **Plan**
>
> Qué tecnologías, componentes y arquitectura se utilizarán.<br/>
> Ejemplo: Vue llama a FastAPI, FastAPI llama a OpenRouter y devuelve JSON.
>
> **Tasks**
>
> Cómo dividir el trabajo en pasos implementables.<br/>
> Ejemplo: definir el esquema de entrada, crear el endpoint, validar la respuesta y conectar el formulario.
>
> **Implement**
>
> El agente trabaja sobre el código y los documentos anteriores.<br/>
> Ejemplo: implementar una tarea, comprobar el resultado y continuar con la siguiente.

Hay una distinción fundamental: Spec Kit no es un framework que se ejecute dentro de vuestra aplicación. Es un conjunto de instrucciones, plantillas y procesos para dirigir al agente de programación. No sustituye a Vue, FastAPI, las pruebas ni vuestra revisión del código.

## 2. Antes de empezar: comprobar la instalación

Como ya habéis ejecutado:

```
uv tool install specify-cli
specify init --here --force --integration copilot
```

No volváis a ejecutar `specify init` por ahora. Ya habéis inicializado Spec Kit en el proyecto. Al hacerlo con `--here --force`, se permite integrar sus archivos en un directorio existente, pero también puede reemplazar archivos gestionados por Spec Kit. Conviene revisar los cambios, especialmente si ya tenéis trabajo hecho.

### Paso 2.1. Revisad qué ha añadido

Desde la raíz del repositorio, ejecutad:

```
specify version
specify check
git status --short
```

El último comando requiere que el proyecto esté bajo Git. Si ya lo está, revisad qué archivos se han añadido o modificado.

En particular, buscad estas ubicaciones:

> `.specify/`
>
> Contiene recursos compartidos del proyecto: plantillas, scripts, configuración y memoria, según la instalación.
>
> `.github/prompts/`
>
> Con la integración de Copilot, buscad los archivos de instrucciones que habilitan los comandos de Spec Kit. La ubicación exacta puede variar > según la versión y el modo de integración.
>
> `specs/`
>
> Aquí se guardarán las especificaciones y los artefactos de cada funcionalidad cuando iniciéis el flujo.

No pasa nada si alguna carpeta todavía no existe o si vuestra versión organiza los archivos de otra forma. Podéis consultar la [guía oficial para proyectos existentes](https://github.com/github/spec-kit/blob/main/docs/guides/existing-projects.md).

### Paso 2.2. Comprobad que Copilot reconoce los comandos

Abr id el proyecto en VS Code y probad en el chat de GitHub Copilot:

```
/speckit-constitution
```

No hace falta que lo ejecutéis todavía con instrucciones definitivas. Primero comprobad que Copilot reconoce el comando y puede acceder a los archivos del repositorio. Si no lo reconoce, comprobad los archivos de integración y recargad VS Code antes de seguir.

Si Spec Kit está instalado en una subcarpeta (por ejemplo, `app2/`) pero abrís en VS Code la carpeta padre del repositorio para tener también la documentación a mano, Copilot puede no detectar las skills porque están dentro de `app2/.github/skills/`. En este repositorio ya están añadidas en la raíz las skills puente de `.github/skills/`: exponen los mismos comandos y les indican que ejecuten el flujo original usando `app2` como raíz de Spec Kit. Así podéis seguir trabajando desde una sola ventana y consultar el resto del repositorio; los artefactos de Spec Kit continúan dentro de `app2`.

Los nombres de los comandos dependen de las skills instaladas. En esta instalación, el comando es `/speckit-constitution` (no `/specify-constitution`); podéis escribir `/` en el chat para ver los nombres disponibles.

Importante: los comandos `/speckit-*` se ejecutan en el chat del agente, no en PowerShell. La CLI `specify` se usa para inicializar y administrar la instalación; los comandos de desarrollo los ejecuta Copilot siguiendo las instrucciones instaladas.

## 3. Primer paso real: crear la Constitution

La constitution es el conjunto de principios que Spec Kit debe tener en cuenta durante el resto del trabajo. Se crea una vez para el proyecto y se actualiza cuando cambian las reglas fundamentales.

No debe convertirse en una lista enorme de requisitos técnicos ni en un documento de diseño. En vuestro caso, debería evitar que la IA os complique innecesariamente una aplicación pequeña.

En el chat de Copilot, ejecutad el comando con este texto:

```
/speckit-constitution Establece los principios de este proyecto con las siguientes reglas:

- Mantener una aplicación web de una sola página, con una arquitectura sencilla y sin funcionalidades innecesarias.
- Respetar el stack existente: Vue 3, TypeScript y Vite para el frontend; Python y FastAPI para el backend.
- Mantener el frontend y el backend separados, comunicándose mediante una API HTTP claramente definida.
- Utilizar OpenRouter desde el backend. La clave API debe almacenarse en una variable de entorno y nunca exponerse al frontend ni incluirse en el repositorio.
- Utilizar modelos y opciones gratuitas de OpenRouter para el desarrollo, sin introducir gastos deliberadamente.
- Validar los datos recibidos y las respuestas de la IA. Gestionar errores de validación, errores de comunicación y respuestas inválidas sin bloquear la interfaz.
- Definir un contrato JSON explícito entre backend y frontend, con una estructura estable y documentada.
- Priorizar soluciones que podamos entender y mantener dos estudiantes con experiencia limitada en algunas de las tecnologías utilizadas.
- Evitar nuevas dependencias, bases de datos, autenticación, despliegues, servicios externos y capas arquitectónicas que no sean necesarios para los requisitos acordados.
- Añadir pruebas proporcionadas al alcance del proyecto y ejecutar las comprobaciones pertinentes antes de dar una tarea por terminada.
- Explicar brevemente las decisiones técnicas relevantes y no realizar cambios ajenos a la tarea solicitada.

Crea o actualiza la constitution y las plantillas dependientes según corresponda. No implementes funcionalidades ni modifiques código de la aplicación en este paso.
```

He incluido una regla de seguridad importante: la clave de OpenRouter debe permanecer en el backend. También he especificado que la aplicación debe ser fácil de mantener, porque no os interesa que el agente introduzca una arquitectura demasiado avanzada para el alcance de la asignatura.

**Qué debéis revisar al terminar:**

- Que las reglas sean razonables para los dos.
- Que no haya aparecido una arquitectura más compleja de la necesaria.
- Que se haya creado o actualizado el archivo de la constitution, normalmente en `.specify/memory/constitution.md`.
- Que no se haya puesto a programar la aplicación todavía.

No hace falta que comprendáis cada detalle de las plantillas que Spec Kit actualice. Sí debéis entender las reglas que habéis decidido imponer al proyecto.

## 4. Antes de Specify: acordad qué aplicación vais a construir

Este es vuestro siguiente paso importante. Todavía no hace falta programar ni elegir todos los detalles técnicos.

Spec Kit puede ayudaros a definir los requisitos, pero no puede decidir por vosotros qué problema queréis resolver. Si la temática sigue abierta, os recomiendo dedicar un rato a acordar una idea mínima antes de generar la especificación.

No necesitáis redactar un documento formal. Basta con responder a estas cinco preguntas:

| Pregunta          | Qué debéis decidir                                      |
| ----------------- | ------------------------------------------------------- |
| ¿Para quién?      | Quién utilizará la aplicación.                          |
| ¿Para qué?        | Qué problema resuelve o qué necesidad cubre.            |
| ¿Qué introduce?   | Qué campos tendrá el formulario.                        |
| ¿Qué devuelve?    | Qué información debe producir la IA y cómo se mostrará. |
| ¿Qué queda fuera? | Funcionalidades que no vais a desarrollar.              |

Por ejemplo, una aplicación podría ayudar a interpretar un conjunto de datos, generar recomendaciones a partir de unas preferencias o analizar una situación descrita mediante opciones predefinidas. Son ejemplos del tipo de problema que podríais abordar, no propuestas que tengáis que adoptar.

Para vuestro proyecto, mantendría como alcance inicial una única página, sin cuentas de usuario, sin base de datos y sin funcionalidades adicionales que no os exija la asignatura.

## 5. Ejecutar Specify: crear la especificación funcional

Una vez tengáis una idea, utilizad:

```
/speckit-specify
```

Este comando genera la especificación funcional de la aplicación. En esta fase, lo importante es explicar qué debe hacer y qué experiencia debe ofrecer, sin entrar todavía en detalles como la organización de los archivos Python o los componentes Vue.

Podéis usar este ejemplo como base, sustituyendo los apartados entre corchetes:

**Plantilla para Specify**

```
/speckit-specify

Queremos desarrollar una aplicación web educativa para [tipo de usuario] que permita [objetivo principal].

La aplicación tendrá una única página con un formulario de campos definidos que el usuario completará para [objetivo concreto]. Al enviarlo, recibirá una respuesta generada por una IA que le ayude a [resultado esperado].

La respuesta debe presentarse de forma estructurada, clara y visualmente agradable, en lugar de mostrar únicamente un bloque de texto sin formato.

El usuario debe poder identificar cuándo se está procesando su solicitud, consultar el resultado y entender los errores si los datos introducidos no son válidos o si falla la generación de la respuesta.

El alcance inicial se limita al flujo principal del formulario y a la visualización de su resultado. No se incluyen autenticación, persistencia de datos, historial, perfiles ni otras funcionalidades que no sean imprescindibles.

Todavía no decidas la arquitectura ni añadas funcionalidades no solicitadas. Examina el repositorio existente para comprender el contexto, pero no implementes código en esta fase. Identifica los requisitos que falten o sean ambiguos en la especificación.
```

### ¿Qué archivo debéis revisar?

Normalmente, la especificación quedará en una ruta parecida a esta:

```
specs/
└── 001-nombre-de-la-funcionalidad/
    └── spec.md
```

El nombre y el número concretos dependerán de cómo se genere la especificación.

Revisad especialmente:

- Los requisitos funcionales: ¿ha entendido lo que queréis que haga la aplicación?
- Los criterios de aceptación: ¿se puede comprobar objetivamente que cada requisito se cumple?
- Los casos de error: ¿contempla entradas inválidas y fallos de la IA?
- El alcance: ¿ha añadido cuentas, historial, bases de datos u otras funciones que no necesitáis?

No paséis a la siguiente fase hasta que estéis conformes con el documento. Es mucho más barato corregir una especificación que corregir una implementación equivocada.

## 6. Clarify: resolver dudas antes de diseñar

El siguiente comando que os recomiendo es:

```
/speckit-clarify
```

Este paso sirve para detectar ambigüedades en la especificación y formular preguntas concretas antes de tomar decisiones de diseño. Es especialmente útil cuando estáis aprendiendo tecnologías o todavía no habéis definido todos los detalles.

En vuestro caso, prestaría atención a cuestiones como estas:

- ¿Qué campos son obligatorios y cuáles opcionales?
- ¿Qué debe devolver exactamente la IA?
- ¿La respuesta debe ser JSON con campos definidos o texto libre?
- ¿Qué se muestra cuando OpenRouter no devuelve una respuesta válida?
- ¿Qué ocurre si el usuario envía el formulario varias veces?

No tenéis que resolver todas las cuestiones técnicas en este paso. Por ejemplo, la elección concreta de los modelos de OpenRouter corresponde al diseño técnico posterior, aunque sí conviene establecer desde el principio que no queréis generar costes.

Contestad las preguntas que realmente afecten al comportamiento de la aplicación. Si el agente plantea algo que no sabéis decidir, podéis pedirle que explique las alternativas de forma sencilla y recomiende la opción menos compleja que cumpla los requisitos.

## 7. Plan: diseñar la solución técnica

Una vez validada la especificación, ejecutad:

```
/speckit-plan
```

Aquí sí debéis concretar el stack y la arquitectura. Para vuestro proyecto, usaría una instrucción de este estilo:

**Plantilla para Plan**

```
/speckit-plan

Diseña la solución técnica utilizando el proyecto existente como punto de partida.

- Frontend: Vue 3, TypeScript y Vite.
- Backend: Python y FastAPI.
- Comunicación: peticiones HTTP desde el frontend a una API REST del backend.
- IA: integración con OpenRouter exclusivamente desde el backend, utilizando una variable de entorno para la clave y modelos gratuitos para el desarrollo.
- Contrato de datos: definir esquemas de entrada y salida explícitos, con validación mediante Pydantic en el backend y tipos TypeScript coherentes en el frontend.
- Interfaz: formulario, estado de carga, presentación estructurada de resultados y mensajes de error.
- Pruebas: cubrir la validación, el endpoint y los casos principales de éxito y error, usando respuestas simuladas cuando sea posible para no depender de llamadas reales a la IA.
- Configuración: respetar las dependencias y herramientas que ya existan. No introducir nuevas librerías si no aportan una ventaja clara.

Antes de proponer cambios, inspecciona la estructura y la configuración actuales. Conserva la organización existente del frontend y del backend y no generes una segunda aplicación ni reorganices carpetas sin necesidad.

Prioriza una solución sencilla, explicable y mantenible por dos estudiantes. Documenta las decisiones relevantes y las comprobaciones necesarias para validar la solución.
```

### Qué debéis comprobar en el plan

El plan puede incluir varios documentos y decisiones, según las plantillas de vuestra instalación. Revisad, como mínimo, estos aspectos:

| Aspecto         | Qué debería quedar claro                                                    |
| --------------- | --------------------------------------------------------------------------- |
| Arquitectura    | Qué responsabilidades corresponden al frontend y cuáles al backend.         |
| Contrato API    | Qué recibe el endpoint y qué devuelve exactamente.                          |
| Respuesta de IA | Qué estructura debe producir OpenRouter y cómo se valida.                   |
| Seguridad       | Cómo se gestiona la clave API y los errores.                                |
| Pruebas         | Qué vais a probar y cómo evitar llamadas reales innecesarias a OpenRouter.  |
| Organización    | Qué archivos existentes se reutilizan y cuáles habrá que crear o modificar. |

Una recomendación concreta: pedidle que defina el contrato JSON antes de implementar la integración. Así no tendréis un backend que devuelve un formato improvisado y un frontend que espera otro diferente.

Por ejemplo, el resultado podría incluir un campo `resumen`, una lista de `recomendaciones` y un campo `advertencias`, pero los campos definitivos deben depender de la temática que elijáis.

## 8. Tasks: convertir el plan en trabajo manejable

Después, ejecutad:

```
/speckit-tasks
```

Spec Kit generará una lista de tareas ordenadas por dependencias, normalmente en `tasks.md`.

Aquí es donde podéis ahorraros buena parte del agobio de tener que aprender y construirlo todo a la vez.

Para una aplicación de vuestro tamaño, las tareas deberían dividir el trabajo aproximadamente así:

> **Fase 1. Preparación**
>
> Revisar la configuración actual, establecer el contrato de datos y comprobar que frontend y backend arrancan.
>
> **Fase 2. Backend**
>
> Definir los modelos Pydantic, crear el endpoint, validar las entradas y establecer el formato de respuesta.
>
> **Fase 3. Integración con la IA**
>
> Configurar OpenRouter, gestionar la clave, procesar la respuesta y controlar los errores.
>
> **Fase 4. Frontend**
>
> Construir el formulario, conectar la API y presentar los resultados con estados de carga y error.
>
> **Fase 5. Integración y pruebas**
>
> Verificar el flujo completo y corregir los problemas encontrados.

Estas fases son una orientación para revisar las tareas que genere Spec Kit, no una lista que tengáis que duplicar manualmente.

Si os genera tareas demasiado grandes, pedidle que las divida. Una tarea como «crear toda la aplicación» no os ayuda a entender qué se está haciendo ni a detectar dónde ha fallado.

## 9. Implement: no le pidáis que construya todo de golpe

Cuando hayáis revisado las tareas, ejecutad:

```
/speckit-implement
```

Aunque el comando puede ejecutar varias tareas consecutivas, para vuestro caso recomiendo trabajar por fases pequeñas. La propia documentación contempla implementar por partes cuando conviene controlar mejor el proceso.

Podéis darle instrucciones como estas:

```
/speckit-implement

Implementa únicamente las tareas de preparación y del contrato
de datos que sean necesarias para comenzar.

No continúes con las siguientes fases.

Al terminar:
- Resume los archivos creados o modificados.
- Explica las decisiones técnicas importantes.
- Ejecuta las comprobaciones pertinentes.
- Indica las tareas completadas y las que quedan pendientes.
- No marques una tarea como completada si no has verificado su resultado.
```

Después, revisad los cambios y ejecutad las pruebas. Si todo funciona, continuad con la siguiente parte.

La idea no es que aprendáis cada línea de código antes de avanzar, pero sí que podáis explicar qué hace cada componente y por qué está ahí. Eso es especialmente importante en un proyecto académico.

## 10. Qué comandos utilizar y cuáles dejar para más adelante

No necesitáis aprender todos los comandos de Spec Kit ahora mismo.

| Comando                 | ¿Lo usaría?            | Motivo                                                     |
| ----------------------- | ---------------------- | ---------------------------------------------------------- |
| `/speckit-constitution` | Sí                     | Fija las reglas comunes.                                   |
| `/speckit-specify`      | Sí                     | Define la aplicación.                                      |
| `/speckit-clarify`      | Sí, si hay dudas       | Resuelve ambigüedades.                                     |
| `/speckit-plan`         | Sí                     | Diseña la solución técnica.                                |
| `/speckit-tasks`        | Sí                     | Divide el trabajo.                                         |
| `/speckit-implement`    | Sí                     | Implementa las tareas.                                     |
| `/speckit-analyze`      | Opcional, recomendable | Detecta incoherencias entre especificación, plan y tareas. |
| `/speckit-checklist`    | Opcional               | Añade una revisión formal de la calidad de los requisitos. |
| `/speckit-converge`     | Recomendable al final  | Comprueba si la implementación satisface lo especificado.  |

La documentación oficial distingue entre un flujo corto, suficiente para proyectos pequeños, y otro más completo con controles adicionales. Para vosotros empezaría con el corto y añadiría `analyze` o `converge` cuando os aporten valor.

## 11. Cómo repartir el trabajo entre dos personas

Spec Kit no os obliga a dividir el proyecto de una manera concreta. Mi propuesta sería que los dos participéis en las decisiones iniciales y que luego os repartáis la implementación según las tareas y vuestras fortalezas.

- **Ambos:** acordar la temática, revisar la constitution, validar la especificación y aprobar el contrato JSON.
- **Persona A:** trabajar principalmente en el backend, la validación y la integración con OpenRouter.
- **Persona B:** trabajar principalmente en el formulario Vue, la presentación de resultados y los estados de la interfaz.
- **Ambos:** probar el flujo completo, revisar el código generado y verificar los criterios de aceptación.

No es necesario que cada persona trabaje exclusivamente en una capa. De hecho, si una tarea afecta a las dos, conviene acordar primero el contrato de datos y después trabajar sobre él.

## Mi recomendación final: vuestro siguiente movimiento

No empecéis con `/speckit-plan` ni con `/speckit-implement`.

Seguid este orden:

1. Comprobad que la instalación de Spec Kit y Copilot funciona.
2. Cread la constitution con las reglas anteriores y revisadla.
3. Acordad una temática y un objetivo mínimo para la aplicación.
4. Ejecutad `/speckit-specify` y corregid la especificación.
5. Utilizad `/speckit-clarify` si quedan decisiones importantes sin resolver.
6. Generad el plan y las tareas.
7. Implementad y probad una fase cada vez.

Como referencia principal, os recomiendo guardar la [guía oficial de inicio rápido de Spec Kit](https://github.com/github/spec-kit/blob/main/docs/quickstart.md) y la [guía para integrarlo en proyectos existentes](https://github.com/github/spec-kit/blob/main/docs/guides/existing-projects.md).

El objetivo es que Spec Kit reduzca el número de decisiones improvisadas y os ayude a entender el trabajo, no que os genere una cantidad mayor de documentos que después tengáis que mantener. Para una aplicación de una sola página, una buena especificación, un contrato JSON claro y unas tareas bien divididas os aportarán mucho más que adoptar todas las funcionalidades de la herramienta.
