<!--
Sync Impact Report
- Version change: plantilla sin versión ratificada → 1.0.0 (adopción inicial).
- Principios añadidos: I. Alcance funcional estricto; II. Tecnologías y arquitectura
  protegidas; III. Seguridad, identidad y privacidad; IV. Contratos, validación y
  resultados seguros; V. Desarrollo dirigido por especificaciones y calidad.
- Secciones añadidas: Restricciones permanentes; Flujo de desarrollo y calidad.
- Secciones eliminadas: ninguna.
- TODOs de plantilla: ninguno. Las decisiones de implementación se concretarán en la
  especificación y el plan.
-->

# Constitución de ResumidorIA (App 2)

## Principios fundamentales

### I. Alcance funcional estricto
La aplicación MUST consistir en una SPA con una sola pantalla y un único formulario para una
única función: resumir texto. El formulario MUST permitir seleccionar la longitud del resumen y
solicitar, opcionalmente, ideas principales y glosario. El backend MUST realizar exactamente una
llamada a OpenRouter por cada envío válido y autenticado. La carga de archivos `.txt` y `.md`
MUST limitarse a leerlos en el navegador y colocar su contenido en el formulario; MUST NOT
 enviar archivos al servidor. Copiar el resultado y exportarlo a `.txt` o `.md` MUST ocurrir en
el navegador y no constituir funciones de procesamiento adicionales. MUST NOT haber bases de
datos, persistencia funcional, historial, conversaciones con memoria, CRUD, pantallas o rutas de
navegación adicionales, perfiles, paneles, agentes encadenados, RAG, proveedores de IA
adicionales ni otras funciones no aprobadas. El texto y el resultado solo podrán mantenerse
transitoriamente en memoria durante el procesamiento y la visualización. Esta limitación
preserva la simplicidad exigida por la práctica.

### II. Tecnologías y arquitectura protegidas
El frontend MUST usar Vue 3, TypeScript y Tailwind CSS; el backend MUST usar Python y FastAPI;
OpenRouter MUST ser el único proveedor de IA y Clerk MUST ser el servicio de identidad de App 2.
La estructura actual de carpetas y archivos del frontend y el backend, sus configuraciones,
dependencias, puntos de entrada y contratos entre capas MUST tratarse como inmutables, salvo que
un requisito aprobado haga imprescindible modificarlos. Antes de proponer cualquier cambio de esa
clase, el agente MUST explicar su necesidad, impacto y alternativas, y solicitar autorización
explícita; MUST NOT ejecutarlo sin dicha autorización. Los archivos nuevos MUST añadirse únicamente
cuando estén justificados por un requisito aprobado o por Spec Kit, respetando la organización
existente. El proyecto MUST NOT recrearse ni inicializarse de nuevo. Esto protege el trabajo
existente y evita cambios estructurales innecesarios.

### III. Seguridad, identidad y privacidad
El backend MUST validar la firma y vigencia del token de sesión de Clerk antes de procesar
cualquier solicitud protegida o invocar a OpenRouter. Si el token falta o no es válido, MUST
responder HTTP 401 y MUST NOT llamar al proveedor de IA. La clave privada de OpenRouter MUST
permanecer exclusivamente en el backend y MUST NOT incluirse en el frontend, respuestas,
registros ni repositorio. La autenticación MUST delegarse en Clerk: MUST NOT implementarse
gestión propia de usuarios, contraseñas, perfiles o roles. Los registros MUST NOT incluir texto
de entrada, resultados, tokens ni secretos; MUST NOT almacenarse de forma funcional el
formulario o los resultados. Estas reglas reducen la exposición de datos y credenciales y hacen
efectivo el control de acceso en el servidor.

### IV. Contratos, validación y resultados seguros
El frontend y el backend MUST validar las entradas, y el backend MUST validar la respuesta del
proveedor antes de devolverla. La comunicación entre capas MUST utilizar un contrato JSON
coherente, explícito y trazable a requisitos; cualquier cambio del contrato MUST actualizar
ambos lados y sus pruebas en el mismo cambio aprobado. Los errores de validación, autenticación,
proveedor, respuesta inválida y timeout MUST producir respuestas controladas y estados visibles
para el usuario, sin trazas internas ni secretos. El frontend MUST presentar el contenido
generado como texto no ejecutable; MUST NOT interpretarlo como HTML ni ejecutarlo. La copia y
exportación MUST incluir únicamente los resultados visibles y MUST ocurrir localmente en el
navegador. Estas condiciones hacen verificable la integración y evitan que contenido externo se
ejecute como código.

### V. Desarrollo dirigido por especificaciones y calidad
Antes de implementar funcionalidades, el equipo MUST generar y revisar la especificación, el
plan y las tareas de Spec Kit, comprobar su coherencia y mantener trazabilidad desde los
requisitos de la ERS hasta los criterios de aceptación y las pruebas. La implementación MUST
avanzar incrementalmente, en tareas acotadas y revisables; cada cambio MUST validarse con las
comprobaciones pertinentes y MUST evitar alterar trabajo ajeno a la tarea. Las pruebas
automatizadas MUST cubrir validaciones, contrato, errores, autenticación y los casos funcionales
relevantes. Las pruebas del backend MUST simular Clerk y OpenRouter mediante mocks o sustitutos
controlados; MUST NOT realizar llamadas reales a OpenRouter. El equipo MUST NOT implementar
código mientras existan contradicciones de alcance o de estructura sin resolver.

## Restricciones permanentes

- La ERS y las reglas de la práctica definen los requisitos funcionales dentro de los límites de
  esta constitución. La carga local de `.txt`/`.md` y la copia/exportación a `.txt`/`.md` son
  acciones auxiliares de la misma función de resumen; se limitan al navegador y no habilitan
  procesamiento, persistencia o alcance adicional.
- Las especificaciones podrán precisar longitud y límites de entrada, campos y esquemas JSON,
  modelo y parámetros de OpenRouter, manejo de errores y timeouts, detalles de verificación de
  Clerk, presentación visual y estrategia de despliegue. Estas decisiones de implementación MUST
  concretarse en la especificación o el plan y MUST respetar los principios permanentes; no
  constituyen autorización para modificar arquitectura protegida ni ampliar el alcance.
- La ausencia de persistencia funcional no impide mantener temporalmente datos en memoria para
  procesar y mostrar una solicitud, ni conservar los documentos del proyecto, la configuración
  necesaria o evidencias académicas con datos ficticios.

## Flujo de desarrollo y calidad

1. Revisar los requisitos de la ERS, las reglas de la práctica y la estructura real antes de
   planificar cambios.
2. Crear o actualizar y revisar la especificación; resolver ambigüedades y contradicciones con
   el equipo antes de continuar.
3. Elaborar y revisar el plan técnico y las tareas; verificar trazabilidad, alcance y
   compatibilidad con la arquitectura protegida.
4. Implementar solo después de esa revisión, de forma incremental y con autorización previa
   cuando un cambio afecte elementos protegidos.
5. Ejecutar pruebas y comprobaciones relevantes, usando mocks para dependencias externas;
   revisar el diff para confirmar que no se sobrescribió trabajo previo ni se añadieron cambios
   ajenos.
6. No considerar una tarea terminada hasta que sus criterios de aceptación se hayan comprobado y
   los artefactos de Spec Kit relacionados estén coherentes.

## Gobernanza

Esta constitución establece las reglas permanentes para el desarrollo de ResumidorIA (App 2). Si
una propuesta, requisito, ERS, plan o instrucción entra en conflicto con ella o con la estructura
existente, el agente MUST detener el trabajo afectado, exponer la contradicción y solicitar una
decisión explícita; MUST NOT elegir una interpretación por su cuenta. Toda modificación de esta
constitución requiere aprobación explícita del equipo y MUST actualizarse junto con los artefactos
de Spec Kit afectados antes de implementar el cambio aprobado.

La versión seguirá SemVer: un cambio incompatible de alcance, tecnología o principio
incrementará MAJOR; un principio o restricción permanente añadido o ampliado incrementará MINOR;
una aclaración sin cambio normativo incrementará PATCH. Cada revisión y análisis de Spec Kit, y
cada cambio de código, MUST comprobar el cumplimiento de esta constitución. Las excepciones
requieren modificar y aprobar primero la constitución; no se permiten excepciones implícitas.

**Versión**: 1.0.0 | **Ratificada**: 2026-10-19 | **Última modificación**: 2026-10-19
