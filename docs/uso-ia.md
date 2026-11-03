# Uso de inteligencia artificial durante el desarrollo

## 1. Objetivo del documento

Este documento recoge cómo se han utilizado herramientas de inteligencia artificial como apoyo durante el desarrollo de App 1 y App 2.

La IA se ha empleado como herramienta de asistencia para comprender tecnologías, resolver dudas de programación, analizar errores, proponer soluciones, elaborar pruebas y mejorar la documentación. Las decisiones finales sobre la implementación y las modificaciones del código han correspondido al equipo.

## 2. Herramientas de inteligencia artificial utilizadas

### 2.1. ChatGPT

Se ha utilizado ChatGPT como herramienta de consulta y apoyo técnico durante las distintas fases del proyecto.

Sus principales usos han sido:

- Comprender conceptos y tecnologías utilizadas en el proyecto.
- Resolver dudas sobre Python, FastAPI, Vue, TypeScript y otras herramientas.
- Analizar fragmentos de código y comprender por qué funcionan o por qué producen determinados errores.
- Proponer soluciones a problemas de integración entre frontend y backend.
- Revisar decisiones de arquitectura y configuración.
- Revisar documentación y mejorar la claridad de las explicaciones.

### 2.2. GitHub Copilot

Se ha utilizado GitHub Copilot como asistente de programación dentro del entorno de desarrollo.

Su utilización se ha orientado principalmente a:

- Generar o modificar código a partir de instrucciones concretas.
- Ayudar con tareas de implementación.
- Revisar y corregir código existente.
- Preparar y ampliar pruebas automatizadas.
- Aplicar cambios relacionados con la autenticación y la configuración de la aplicación.

Para tareas que afectaban a varias partes del proyecto se han preparado instrucciones específicas, indicando el contexto, el resultado esperado y las restricciones que debía respetar.

Las modificaciones propuestas por Copilot debían revisarse y probarse antes de considerarse válidas.

## 3. Utilización de IA durante el desarrollo de App 1

### 3.1. Definición de la aplicación y planificación

Durante las primeras fases se utilizó ChatGPT para explorar posibles ideas y concretar el alcance de la aplicación.

Se trabajó sobre una aplicación de resumen de textos que permitiera introducir contenido y obtener un resultado generado mediante IA.

Estas consultas ayudaron a concretar las opciones que podía ofrecer la aplicación, manteniendo el alcance reducido exigido por la práctica.

También se consultó cómo estructurar el proyecto y cómo documentar los requisitos, la arquitectura y el funcionamiento esperado.

### 3.2. Desarrollo del backend

Se utilizó ChatGPT para resolver dudas relacionadas con Python y FastAPI, especialmente en la comunicación con el proveedor de IA.

Entre los temas trabajados se encuentran:

- Organización de la lógica del backend.
- Recepción y validación de peticiones.
- Comunicación con la API externa de IA.
- Construcción de las instrucciones enviadas al modelo.
- Definición de una respuesta JSON que pudiera consumir el frontend.
- Gestión de errores y respuestas inesperadas del proveedor.

También se consultó cómo separar la lógica de comunicación con el proveedor para facilitar su comprobación mediante pruebas automatizadas.

### 3.3. Desarrollo del frontend e integración

Durante el desarrollo del frontend, basado en Vue y TypeScript, se utilizó ChatGPT para resolver dudas sobre el tratamiento de las respuestas del backend.

También se consultaron cuestiones relativas a:

- Envío de peticiones HTTP desde Vue.
- Tratamiento de respuestas JSON.
- Integración entre el contrato del backend y los tipos de TypeScript.
- Representación de resultados y estados de la interfaz.
- Gestión de errores de comunicación.

### 3.4. Configuración y despliegue

Se utilizó ChatGPT para comprender las opciones de despliegue de una aplicación con frontend Vue y backend FastAPI.

Se analizaron las diferencias entre utilizar GitHub Pages y Vercel, teniendo en cuenta que el backend necesita ejecutar código Python.

También se consultaron aspectos como:

- Configuración de variables de entorno.
- Separación de las direcciones del frontend y backend.
- Configuración de CORS.
- Protección de las claves de acceso al proveedor de IA.
- Organización del repositorio y documentación de instalación.

## 4. Utilización de IA durante el desarrollo de App 2

### 4.1. Preparación del proyecto mediante GitHub Spec Kit

App 2 se planteó como una nueva implementación de la aplicación, utilizando GitHub Spec Kit para introducir un proceso de desarrollo dirigido por especificaciones.

Se consultó cómo instalar e inicializar Spec Kit, cómo utilizarlo desde GitHub Copilot y qué función tenía cada uno de sus artefactos.

También se consultó cómo organizar los archivos generados por Spec Kit.

**Importante:** Spec Kit no se utilizó de la misma manera en todas las fases de App 2. Su utilización estuvo especialmente vinculada a la integración de Clerk y las nuevas funcionalidades. El resto del desarrollo contó con asistencia de IA, pero no siguió necesariamente un proceso completo de especificación, planificación y ejecución mediante Spec Kit, ya que se comenzó a trabajar desde lo que ya había hecho de la App 1.

### 4.2. Diseño de la aplicación y funcionalidades

Se utilizó ChatGPT para revisar la idea inicial y estudiar cómo mejorar la utilidad del resumidor sin aumentar innecesariamente su complejidad.

Se analizaron opciones de personalización del resumen, como:

- Seleccionar la longitud del resumen.
- Activar o desactivar la extracción de ideas principales.
- Obtener un glosario de términos relevantes.

También se valoraron otras posibilidades, como seleccionar documentos para introducirlos en la aplicación.

Las propuestas se contrastaron con las restricciones de la práctica. Se priorizó mantener una única pantalla y un flujo sencillo, evitando incorporar funcionalidades que implicasen nuevas pantallas, persistencia o servicios adicionales.

### 4.3. Desarrollo del backend y comunicación con OpenRouter

Se utilizó ChatGPT para resolver dudas sobre la organización de los servicios del backend y el tratamiento de las respuestas del proveedor de IA.

Entre los aspectos trabajados se encuentran:

- Separación de la lógica de generación del resumen.
- Construcción del prompt enviado al modelo.
- Validación de los datos de entrada.
- Definición de la estructura JSON de salida.
- Tratamiento de respuestas vacías o mal formadas.
- Gestión de errores de conexión y tiempos de espera.
- Validación de la respuesta antes de devolverla al frontend.

### 4.4. Integración de Clerk y autenticación

Una de las tareas en las que se utilizó GitHub Copilot junto con Spec Kit fue la integración de Clerk.

Se consultó cómo implementar un sistema de autenticación externo sin desarrollar una gestión propia de usuarios.

También se trabajaron aspectos como:

- Integración de Clerk en el frontend Vue.
- Obtención del token de sesión.
- Envío del token mediante la cabecera `Authorization`.
- Verificación del token en el backend.
- Rechazo de peticiones sin autenticación o con un token inválido.
- Separación entre autenticación y autorización de acceso al servicio de resumen.

Durante esta fase se revisó la propuesta de implementación y se simplificaron algunas soluciones para ajustarlas al alcance de la práctica.

### 4.5. Resolución de errores y depuración

ChatGPT se utilizó para analizar fragmentos de código y comprender errores encontrados durante el desarrollo.

Entre los temas consultados se incluyen:

- Tratamiento de las respuestas JSON en TypeScript.
- Compatibilidad entre los nombres de propiedades del backend y los esperados por el frontend.
- Validación de los datos recibidos.
- Comunicación entre Vue y FastAPI.
- Configuración de CORS.
- Gestión de errores de autenticación.
- Organización de dependencias y configuración del entorno.

### 4.6. Pruebas y control de calidad

Se utilizó ChatGPT para planificar las pruebas necesarias y preparar instrucciones específicas para GitHub Copilot.

Se trabajaron los siguientes aspectos:

- Pruebas unitarias de los servicios que realizan llamadas al proveedor de IA.
- Simulación de respuestas mediante mocks.
- Comprobación de entradas válidas e inválidas.
- Tratamiento de respuestas vacías o JSON incorrecto.
- Simulación de errores de conexión y timeout.
- Pruebas de autenticación con tokens válidos e inválidos.
- Comprobación de la configuración CORS.
- Pruebas funcionales del frontend y del backend.

### 4.7. Documentación del proyecto

ChatGPT y GitHub Copilot se han utilizado para revisar y mejorar la documentación técnica.

Entre las tareas consultadas se encuentran:

- Estructuración del README.
- Documentación de instalación y ejecución.
- Explicación de las variables de entorno.
- Documentación del funcionamiento de la API.
- Revisión de la ERS.
- Documentación de las pruebas.
- Organización de los documentos relacionados con Spec Kit.

También se han utilizado como apoyo para redactar explicaciones técnicas comprensibles y comprobar que la documentación no atribuya al proyecto funcionalidades que no están implementadas.

## 5. Supervisión y validación humana

La utilización de herramientas de IA no ha sustituido la revisión del equipo.

Las propuestas generadas se han considerado soluciones que debían analizarse y comprobarse antes de incorporarse al proyecto.

El proceso de revisión ha incluido:

1. Analizar la propuesta y comprobar que se ajusta a los requisitos.
2. Revisar el código generado o modificado.
3. Comprender las tecnologías y los mecanismos utilizados.
4. Ejecutar la aplicación para comprobar su comportamiento.
5. Realizar pruebas para detectar errores.
6. Modificar o simplificar las soluciones cuando resultaban innecesariamente complejas.

## 6. Limitaciones y dificultades encontradas

Durante el desarrollo se han tenido en cuenta algunas limitaciones del uso de asistentes de IA.

**Las respuestas pueden proponer soluciones más complejas de lo necesario para el alcance de la práctica**

Al realizar la implementación de Clerk, Copilot, junto con Spec-Kit, generó en el frontend código innecesario, donde incluía configuraciones del servicio de Clerk que eran demasiado complejas e innecesarias para lo que realmente es el proyecto, por lo que se decidió eliminar y simplificar estas partes, haciendo que tuviera la misma funcionalidad.

**El código generado puede no coincidir exactamente con la estructura o las dependencias existentes en el proyecto**

Había veces que se generaba código usando código vanilla de JavaScript, creando bloques de código que se hacían incomprensibles. Por lo que se decidió intentar simplificar algunas cosas y usar librerías populares que simplifican las tareas, como utilizar `axios` en vez de `requests` para las llamadas a API, ya que simplifica mucho el proceso de llamadas.

**Las respuestas del backend y los tipos esperados por el frontend deben coincidir; no basta con que el código generado sea sintácticamente correcto**

Algunas respuestas del backend no estaban muy bien adaptadas a lo que pedía el frontend o viceversa y a veces daba error. La IA creó los tipos de datos directamente en el propio endpoint, pero esto hacía que fuera complejo entender los contratos entre frontend y backend, por lo que decidimos crear tipos de datos (objetos/clases) que fueran comunes en ambas partes para que la comunicación fuera más fluida y fácil de entender.

**Las pruebas generadas deben comprobarse y ejecutarse. Su existencia no garantiza que sean correctas.**

Algunas pruebas generadas del backend tenían errores de tipado (TypeScript) y al ejecutarse daban error. La IA no llegaba a corregir estos fallos e intentaba buscar por otro lado, por lo que era necesario corregirlo manualmente y especificar ciertos tipos o condiciones.

**La IA puede proponer funcionalidades que contradigan las restricciones del enunciado**

Al crear la conexión con Clerk, la IA también creó un pequeño login especificado por los desarrolladores. Sin embargo, creó un código excesivamente complejo para mostrar dos botones con una acción cada uno, por lo que tuvo que simplificarse y adaptar el código a lo que ofrecía Clerk sin necesidad de crearlo todo desde cero.
