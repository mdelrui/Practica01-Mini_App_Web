# Despliegue de App 1 y App 2

## 1. Despliegue de ambas aplicaciones en Vercel

Para este caso se ha conectado Vercel con el repositorio de GitHub, creando así las aplicaciones. Se ha hecho a través de Vercel CLI, seleccionando en cada caso la carpeta desde la que ejecutar la aplicación:

| App   | URL                                                   |
| ----- | ----------------------------------------------------- |
| App 1 | [Resumidor IA v1](https://resumidoria.vercel.app)     |
| App 2 | [Resumidor IA v2](https://resumidoria-v2.vercel.app/) |

## 2. Despliegue de App2 en AWS

### 2.1. Objetivo

Este documento recoge los procedimientos necesarios para ejecutar y desplegar la aplicación 2, desarrollada con Vue 3 y FastAPI, tanto en local mediante Docker como en los servicios de despliegue utilizados en el proyecto.

La aplicación utiliza Clerk para la autenticación de usuarios y OpenRouter para generar los resúmenes mediante un modelo de IA.

### 2.2. Entornos de despliegue

| Entorno                     | Tecnología              | Estado                                                                              |
| --------------------------- | ----------------------- | ----------------------------------------------------------------------------------- |
| Frontend y backend en local | Vue 3 y FastAPI         | Disponible                                                                          |
| Aplicación 2 en Vercel      | Vercel                  | [Ver la URL de la app 2 del punto 1](#1-despliegue-de-ambas-aplicaciones-en-vercel) |
| Aplicación 2 con Docker     | Docker Compose y Nginx  | Probado en local                                                                    |
| Aplicación 2 en AWS EC2     | Docker y Docker Compose | [Pendiente de completar]                                                            |

### 2.3. Despliegue con Docker en local

#### 2.3.1. Arquitectura

La aplicación 2 se ejecuta mediante dos contenedores coordinados con Docker Compose:

- **Frontend:** aplicación Vue 3 compilada y servida por Nginx.
- **Backend:** API desarrollada con FastAPI, encargada de procesar las peticiones y comunicarse con OpenRouter.
- **Nginx:** sirve el frontend y actúa como proxy inverso para redirigir las peticiones a la API.
- **Docker Compose:** configura y coordina los contenedores.

#### 2.3.2. Estructura de los archivos

Los archivos relacionados con Docker se encuentran en `app2/infra/`:

```text
app2/
├── backend/
├── frontend/
├── .dockerignore
└── infra/
    ├── Dockerfile.backend
    ├── Dockerfile.frontend
    ├── compose.yaml
    ├── nginx.conf
    ├── .env
    └── .env.example
```

- `Dockerfile.backend`: define la imagen del backend con Python y sus dependencias.
- `Dockerfile.frontend`: compila la aplicación Vue y utiliza Nginx para servir los archivos generados.
- `compose.yaml`: define los servicios, sus configuraciones y la comunicación entre ellos.
- `nginx.conf`: configura el servidor web y la redirección de peticiones hacia el backend.
- `.env`: contiene las variables de entorno utilizadas durante la ejecución y construcción de la aplicación.
- `.env.example`: documenta las variables necesarias sin incluir credenciales reales.
- `.dockerignore`: excluye del contexto de construcción archivos y directorios innecesarios.

#### 2.3.3. Requisitos previos

Es necesario disponer de:

- Docker instalado y en ejecución.
- Docker Compose disponible mediante el comando `docker compose`.
- El repositorio descargado en el equipo.
- Las variables de entorno configuradas en `app2/infra/.env`.

El archivo `.env` debe crearse a partir de `.env.example`, completando los valores necesarios para el entorno local.

Las variables utilizadas incluyen:

| Variable                     | Finalidad                                                                |
| ---------------------------- | ------------------------------------------------------------------------ |
| `VITE_CLERK_PUBLISHABLE_KEY` | Clave pública de Clerk utilizada por el frontend.                        |
| `OPENROUTER_API_KEY`         | Clave privada para acceder a OpenRouter.                                 |
| `OPENROUTER_MODEL`           | Modelo de IA utilizado para generar los resúmenes.                       |
| `OPENROUTER_TIMEOUT`         | Tiempo límite de espera para las peticiones a OpenRouter.                |
| `CLERK_ISSUER`               | Emisor esperado para los tokens de Clerk.                                |
| `CLERK_JWKS_URL`             | URL utilizada para obtener las claves públicas de verificación de Clerk. |
| `CLERK_JWKS_TIMEOUT`         | Tiempo límite de espera para obtener las claves de verificación.         |
| `CORS_ORIGINS`               | Orígenes autorizados para las peticiones al backend.                     |

Los valores concretos deben corresponder a la configuración del código y al entorno de despliegue. Las claves privadas y los tokens no deben incluirse en el repositorio ni en la documentación.

#### 2.3.4. Construcción y ejecución

Desde la raíz del repositorio, acceder al directorio de la aplicación:

```powershell
cd app2
```

Antes de construir los contenedores, se puede comprobar la configuración de Docker Compose:

```powershell
docker compose --env-file infra/.env -f infra/compose.yaml config
```

Para construir las imágenes y arrancar los servicios:

```powershell
docker compose --env-file infra/.env -f infra/compose.yaml up --build -d
```

El parámetro `--build` fuerza la construcción de las imágenes y `-d` permite ejecutar los contenedores en segundo plano.

Para comprobar el estado de los servicios:

```powershell
docker compose --env-file infra/.env -f infra/compose.yaml ps
```

Una vez iniciados, la aplicación está disponible en:

URL local: [http://localhost:8080](http://localhost:8080)

#### 2.3.5. Comprobación del funcionamiento

Con los contenedores en ejecución, se comprueba que:

1. La aplicación se carga correctamente en `http://localhost:8080`.
2. El usuario puede autenticarse mediante Clerk.
3. Se puede enviar un texto y obtener un resumen.
4. Las peticiones del frontend llegan correctamente al backend.
5. Los errores se gestionan de forma controlada.

Para consultar los registros de los servicios:

```powershell
docker compose --env-file infra/.env -f infra/compose.yaml logs
```

Para seguir los registros en tiempo real:

```powershell
docker compose --env-file infra/.env -f infra/compose.yaml logs -f
```

#### 2.3.6. Parada de los contenedores

Para detener y eliminar los contenedores creados por Docker Compose:

```powershell
docker compose --env-file infra/.env -f infra/compose.yaml down
```

Este comando no elimina las imágenes construidas.

#### 2.3.7. Resultado

La aplicación 2 se ha construido y ejecutado correctamente en local mediante Docker Compose. El frontend está disponible en el puerto 8080 y se comunica con el backend a través de Nginx.

Este entorno sirve como base para el despliegue posterior en AWS EC2.

### 2.4. Despliegue de la aplicación 2 en Vercel

#### 2.4.1. Configuración del proyecto

La aplicación 2, denominada _ResumidorIA_, se ha desplegado en Vercel mediante el proyecto `resumidoria-v2`.

El frontend está desarrollado con Vue 3, TypeScript y Vite. La aplicación utiliza Clerk para la autenticación de usuarios y se comunica con un backend desarrollado con FastAPI para procesar los textos y generar los resúmenes mediante OpenRouter.

**URL pública:** [Ver la URL de la app 2 del punto 1](#1-despliegue-de-ambas-aplicaciones-en-vercel)

#### 2.4.2. Instalación y vinculación mediante Vercel CLI

Para gestionar el despliegue desde la terminal, se utilizó Vercel CLI.

Los comandos se ejecutaron desde el directorio `app2` del repositorio.

Primero, se inició sesión en Vercel:

```powershell
vercel login
```

A continuación, se vinculó el directorio local con el proyecto de Vercel:

```powershell
vercel link
```

Durante este proceso se seleccionó el proyecto `resumidoria-v2`, asociado a la cuenta. La vinculación permite que los comandos ejecutados desde ese directorio actúen sobre el proyecto correspondiente.

Vercel generó también el archivo `.env.local` durante la configuración. Este archivo puede contener configuración local y valores sensibles, por lo que no debe subirse al repositorio.

#### 2.4.3. Despliegue de prueba y despliegue de producción

Una vez vinculado el proyecto, se utilizó el siguiente comando para iniciar un despliegue de prueba:

```powershell
vercel
```

Este comando permite generar un despliegue de vista previa (Preview Deployment), útil para comprobar el resultado antes de publicar los cambios en producción.

Para publicar la versión definitiva se utilizó:

```powershell
vercel --prod
```

Este comando genera un despliegue de producción y actualiza la versión publicada de la aplicación.

Durante el primer intento de despliegue se produjo un error en la fase de construcción, asociado a `npm run build`. Tras resolver los problemas de configuración y construcción, se continuó con el despliegue hasta publicar la aplicación.

#### 2.4.4. Gestión de la integración con GitHub

Inicialmente, el proyecto de Vercel se vinculó con el repositorio de GitHub. Posteriormente, se desconectó dicha integración desde la configuración del proyecto, en la sección Settings → Git, para evitar que los cambios enviados al repositorio desencadenaran despliegues automáticos.

A partir de ese momento, el procedimiento de publicación se realiza manualmente mediante Vercel CLI:

```powershell
vercel --prod
```

De esta forma, el envío de cambios a GitHub y la publicación de una nueva versión en Vercel son operaciones independientes.

#### 2.4.5. Variables de entorno

En la configuración del frontend se utiliza la variable:

| Variable                   | Finalidad                                 |
| -------------------------- | ----------------------------------------- |
| VITE_CLERK_PUBLISHABLE_KEY | Permite inicializar Clerk en el frontend. |

Esta variable contiene la clave pública de Clerk. No debe confundirse con las claves secretas de Clerk, que no deben exponerse en el navegador.

Las variables necesarias deben estar configuradas en el entorno de Vercel.

La clave privada `OPENROUTER_API_KEY` debe permanecer exclusivamente en el entorno del backend.

#### 2.4.6. Verificación del despliegue

Después de publicar la aplicación, se debe comprobar que:

1. La aplicación carga correctamente desde su URL pública.
2. Clerk se inicializa y permite autenticar a los usuarios.
3. El frontend se comunica correctamente con el backend.
4. Se pueden enviar textos y obtener resúmenes.
5. Los errores se gestionan de forma controlada.

### 2.5. Despliegue de la aplicación 2 en AWS EC2

> Estado: pendiente de completar tras realizar el despliegue.

#### 2.5.1. Información de la instancia

| Parámetro                   | Valor       |
| --------------------------- | ----------- |
| Proveedor                   | AWS Academy |
| Servicio                    | Amazon EC2  |
| Sistema operativo           | [Completar] |
| Región                      | [Completar] |
| Tipo de instancia           | [Completar] |
| Dirección pública o dominio | [Completar] |
| URL HTTPS de la aplicación  | [Completar] |

#### 2.5.2. Configuración de acceso y red

Documentar la configuración aplicada a la instancia:

- Grupo de seguridad utilizado.
- Acceso SSH limitado a las direcciones IP autorizadas.
- Puertos públicos necesarios para acceder a la aplicación.
- Configuración del dominio y HTTPS.

No se debe publicar el puerto interno del backend directamente en Internet. El acceso web debe realizarse a través del proxy inverso.

#### 2.5.3. Preparación del servidor

Describir los pasos realizados para:

1. Conectarse a la instancia mediante SSH.
2. Instalar Docker y Docker Compose.
3. Obtener el repositorio o la versión del código que se va a desplegar.
4. Crear el archivo de configuración de entorno en el servidor.
5. Verificar que las credenciales no están incluidas en el repositorio.

Añadir los comandos reales utilizados durante la configuración.

#### 2.5.4. Construcción y puesta en marcha

Documentar los comandos ejecutados en el servidor para construir las imágenes y arrancar los contenedores.

Por ejemplo, si se utiliza la misma estructura de directorios que en local, los comandos serán equivalentes a los siguientes, adaptados al sistema operativo y al método de acceso al repositorio:

```
cd app2

docker compose --env-file infra/.env -f infra/compose.yaml config

docker compose --env-file infra/.env -f infra/compose.yaml up --build -d

docker compose --env-file infra/.env -f infra/compose.yaml ps
```

Registrar cualquier cambio que haya sido necesario respecto a la configuración local.

#### 2.5.5. HTTPS, Clerk y configuración de producción

Documentar:

- Dominio o URL HTTPS de acceso.
- Método utilizado para habilitar HTTPS.
- Configuración del dominio en Clerk.
- Orígenes autorizados y configuración de CORS, si procede.
- Variables de entorno específicas del entorno de producción.

La aplicación debe funcionar con autenticación habilitada. No se deben desactivar las comprobaciones de los tokens para facilitar el despliegue.

#### 2.5.6. Verificación del despliegue

Desde otro dispositivo o una conexión distinta a la del servidor, comprobar:

1. Que la aplicación responde en su URL pública.
2. Que el inicio de sesión y la autenticación funcionan.
3. Que el backend acepta peticiones autenticadas.
4. Que las peticiones sin autenticación válida son rechazadas.
5. Que se puede generar un resumen correctamente.
6. Que los errores se gestionan de forma controlada.

Añadir capturas de pantalla o evidencias del funcionamiento real.

#### 2.5.7. Actualización y recuperación

Documentar el procedimiento seguido para actualizar la aplicación cuando se modifica el código:

1. Obtener la versión actualizada del repositorio.
2. Reconstruir las imágenes si es necesario.
3. Recrear los contenedores.
4. Comprobar que los servicios vuelven a funcionar.

Incluir también los comandos utilizados para consultar los servicios y recuperar la aplicación en caso de una interrupción.

#### 2.5.8. Costes y eliminación de recursos

Registrar los recursos de AWS utilizados y las precauciones necesarias para evitar costes innecesarios.

Al terminar las pruebas, seguir las indicaciones del profesorado para detener o eliminar los recursos. Comprobar también si quedan discos, direcciones IP reservadas u otros recursos que puedan seguir generando costes.

### 2.6. Seguridad y gestión de credenciales

- Las claves privadas de OpenRouter se mantienen exclusivamente en el backend.
- Los archivos `.env` no deben subirse al repositorio.
- Los archivos `.env.example` contienen únicamente nombres de variables y valores ficticios o de ejemplo.
- Las claves públicas de Clerk pueden ser utilizadas por el frontend, pero no deben confundirse con las claves secretas de Clerk.
- Las credenciales de AWS, las claves SSH y los tokens no deben incluirse en el código ni en las capturas de pantalla.
- Las peticiones al backend deben seguir validando los tokens de autenticación.
- No se deben registrar innecesariamente los textos introducidos por los usuarios ni los resultados generados.

### 2.7. Evidencias y documentación complementaria

Incluir o enlazar las siguientes evidencias:

- [Repositorio del proyecto](https://github.com/mdelrui/Practica01-Mini_App_Web) (**ACCESIBLE CON INVITACIÓN**)
- [README de la aplicación 2](../README.md)
- [Captura de Docker Compose en ejecución]
- [Ver la URL de la app 2 del punto 1](#1-despliegue-de-ambas-aplicaciones-en-vercel)
- [URL HTTPS de la aplicación 2 en EC2]
- [Capturas de las pruebas de autenticación y generación de resúmenes]
