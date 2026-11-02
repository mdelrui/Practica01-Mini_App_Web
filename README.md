## Autores

- Francisco Luis Cara García
- Mario Delgado Ruiz

# Práctica 01 - Mini aplicación web

Este repositorio está organizado por aplicaciones y entregables, con la aplicación funcional principal en `app1` y el trabajo complementario/avanzado en `app2`, `docs`, `infra` y `presentation`.

## Estructura del repositorio

```text
.
├── app1/               # Aplicación principal (FastAPI + Vue 3 + Requests hacia OpenRouter)
├── app2/               # Segunda aplicación avanzada (SDK OpenAI + Spec-Kit + Clerk)
├── docs/               # Documentación y memorias de la práctica
├── infra/              # Docker y configuración de contenedores
├── presentation/       # Material de presentación y defensa
├── README.md           # Documentación general del repositorio
└── .gitignore          # Archivo gitignore unificado para todo el proyecto
```

---

## app1: Aplicación principal (Resumidor básico)

`app1` contiene el proyecto web funcional base de la práctica. Está diseñado de forma sencilla y modular: el backend sirve la API y los archivos estáticos compilados del frontend para ejecutar todo el proyecto en un único puerto.

### Estructura de app1

```text
app1/
├── main.py                 # Punto de entrada (arranca FastAPI y sirve el frontend compilado)
├── requirements.txt        # Dependencias directas de Python (FastAPI, uvicorn, requests, dotenv)
├── vercel.json             # Configuración de despliegue en Vercel
├── backend/
│   ├── config.py           # Lectura de variables de entorno desde app1/.env
│   ├── openrouter.py       # Petición HTTP simple con requests hacia la API de OpenRouter
│   └── routes.py           # Rutas de la API (endpoint POST /api/resumir con texto directo)
└── frontend/
    ├── package.json        # Dependencias y scripts de Vue
    └── src/                # Código fuente de la interfaz (App.vue, servicios, tests)
```

### Frontend de app1

- **Ubicación:** `app1/frontend`
- **Tecnologías:** Vue 3, TypeScript, Vite, Tailwind CSS, Vitest.

Para instalar dependencias y compilar el frontend:

```powershell
cd app1\frontend
npm install
npm run build-only
```

### Backend de app1

- **Ubicación:** `app1/backend`
- **Tecnologías:** Python 3.12+, FastAPI, Uvicorn, Requests.

El backend se conecta a OpenRouter mediante peticiones HTTP estándar con `requests`:

- `config.py`: Carga la clave secreta `OPENROUTER_API_KEY` desde el archivo `app1/.env`.
- `openrouter.py`: Envía el texto a la API de OpenRouter (`chat/completions`) usando el modelo gratuito `liquid/lfm-2.5-2.6b:free`.
- `routes.py`: Expone el endpoint `POST /api/resumir`, recibiendo directamente `texto: str = Body(embed=True)` sin estructuras complejas.

El archivo `.env` debe crearse en `app1/.env` con el contenido:

```env
OPENROUTER_API_KEY=tu_clave_de_openrouter
```

> **Nota:** El archivo `.env` nunca debe subirse al repositorio Git.

### Ejecutar app1 en local

1. Asegúrate de tener configurado `app1/.env` con tu clave de OpenRouter.
2. Compila el frontend (`npm run build-only` dentro de `app1/frontend`).
3. Inicia la aplicación desde la carpeta `app1`:

```powershell
cd app1
uv run python main.py
```

_(O con entorno virtual activo: `python main.py`)_

La aplicación estará disponible en:

- Interfaz web y API: `http://127.0.0.1:8000`
- Documentación interactiva Swagger: `http://127.0.0.1:8000/docs`

---

## app2: Segunda aplicación (versión avanzada con Clerk y resumen personalizado)

`app2` es la versión avanzada del resumidor, con autenticación de sesión gestionada por Clerk, validación JWT en el backend, opciones de resumen configurables y documentación técnica guiada por Spec-Kit.

### Estructura de app2

```text
app2/
├── backend/
│   ├── auth.py             # Verificación de tokens de Clerk y JWKS
│   ├── main.py             # FastAPI + middleware de autenticación + POST /resumir
│   ├── models.py           # Modelos Pydantic para entrada/salida (ideas, glosario, longitud)
│   ├── services.py         # Conexión a OpenRouter y manejo de errores IA
│   ├── pyproject.toml      # Dependencias del backend
│   └── tests/              # Pruebas de autenticación y validación del flujo seguro
├── frontend/
│   ├── package.json        # Dependencias de Vue + Clerk + Vitest
│   └── src/                # Interfaz con login, selector de opciones y exportación
├── specs/                  # Especificaciones y contratos (Spec-Kit)
├── vercel.json             # Configuración de despliegue multi-servicio en Vercel
└── README.md               # Documentación específica del proyecto app2 (si se añade en el futuro)
```

### Backend de app2

- **Ubicación:** `app2/backend`
- **Tecnologías:** Python 3.12+, FastAPI, Pydantic, SDK de OpenAI (`openai`) y validación de tokens JWT con Clerk.
- **Módulos principales:**
    - `auth.py`: valida el token de sesión de Clerk, comprueba el emisor y usa JWKS para verificar la firma del JWT.
    - `main.py`: define el middleware HTTP que protege `POST /resumir` y devuelve `401` para sesión inválida o `503` si el verificador de JWKS no está disponible.
    - `models.py`: define `UserInput` con `text`, `main_ideas`, `glossary` y `summary_length` y la estructura de respuesta.
    - `services.py`: envía la solicitud a OpenRouter a través del cliente `OpenAI` y maneja excepciones de IA y timeouts.

Para ejecutar el backend de `app2` por separado:

```powershell
cd app2\backend
uv sync
python -m uvicorn main:app --reload
```

Si no existe un entorno virtual de Python (`.venv`), se debe crear antes de ejecutar `uv sync`.

### Frontend de app2

- **Ubicación:** `app2/frontend`
- **Tecnologías:** Vue 3, TypeScript, Vite, Tailwind CSS, Vitest, `@clerk/vue`.
- **Funcionalidades actuales:**
    - Inicio y cierre de sesión con Clerk.
    - Entrada de texto o arrastre de archivos `.txt`/`.md`.
    - Selección de resumen breve/estándar/detallado.
    - Activación opcional de ideas principales y glosario.
    - Envío de la petición autenticada con `Authorization: Bearer <token>`.
    - Visualización del resultado y opciones de copia/exportación local.

Para arrancar el frontend en local:

```powershell
cd app2\frontend
npm install
npm run dev
```

La aplicación queda accesible normalmente en `http://localhost:5173`.

### Configuración de entorno de app2

El backend requiere varias variables de entorno para funcionar correctamente:

```env
CLERK_ISSUER=...
CLERK_JWKS_URL=...
CLERK_JWKS_TIMEOUT=10
OPENROUTER_API_KEY=...
CORS_ORIGINS=http://localhost:5173
```

Estas variables deben mantenerse en el backend y no exponerse al frontend.

### Pruebas de app2

La app2 incluye pruebas de frontend con Vitest que validan el flujo principal:

- pantalla de autenticación cuando no hay sesión
- envío del token Bearer al backend
- gestión de errores de autenticación 401 y 503
- renderizado del resumen y acciones de copia/exportación

Se ejecutan con:

```powershell
cd app2\frontend
npm exec vitest run
```

---

## Despliegue en Vercel

Ambas aplicaciones, `app1` y `app2` están configuradas para el despliegue en Vercel.

- Su archivo `app1/vercel.json` o `app2/vercel.json` define el servicio de backend (FastAPI en `main:app`) y el frontend estático compilado con Vite.
- Las peticiones a `/api/*` se dirigen al backend y el resto de rutas al frontend.
- En el panel de Vercel debe configurarse la variable de entorno `OPENROUTER_API_KEY` dentro del servicio backend.

---

## Documentación e Infraestructura

- **`docs/`**: Contiene la ERS de ambas aplicaciones (`ERS-app1.md`, `ERS-app2.md`), comparativas, evidencias, pruebas y tutoriales.
- **`app2/infra/`**: Dockerfiles y `compose.yaml` para despliegues contenerizados de la aplicación 2.
- **`presentation/`**: Diapositivas de defensa de la práctica.

---

## Ejecución local de App2 con Docker

### Requisitos previos

- Docker Desktop instalado y en ejecución
- Credenciales válidas de OpenRouter y configuración de Clerk

### Estructura de infraestructura

```text
app2/
├── backend/
├── frontend/
├── infra/
│   ├── Dockerfile.backend
│   ├── Dockerfile.frontend
│   ├── compose.yaml
│   ├── nginx.conf
│   ├── .env.example
│   └── .env
└── .dockerignore
```

El frontend se compila y se sirve mediante Nginx. Nginx reenvía las peticiones /api/ al backend FastAPI, que se ejecuta en otro contenedor. El backend no publica su puerto directamente en el host.

### 1. Preparar las variables de entorno

Desde la carpeta `app2/`, copia la plantilla:

```powershell
Copy-Item infra/.env.example infra/.env
```

Edita `infra/.env` y sustituye los valores de ejemplo por los de tu configuración.

- `VITE_CLERK_PUBLISHABLE_KEY`: clave publicable de Clerk utilizada durante la compilación del frontend.
- `OPENROUTER_API_KEY`: clave privada para las peticiones a OpenRouter.
- `OPENROUTER_MODEL` y `OPENROUTER_TIMEOUT`: configuración del proveedor de IA.
- `CLERK_ISSUER`, `CLERK_JWKS_URL` y `CLERK_JWKS_TIMEOUT`: configuración para validar los tokens de sesión.
- `CORS_ORIGINS`: orígenes autorizados por el backend.

No subas `infra/.env` al repositorio. La plantilla `.env.example` sí se comparte, siempre con valores ficticios. La clave de OpenRouter debe permanecer exclusivamente en el backend.

### 2. Construir y arrancar los contenedores

Navega a la carpeta `app2/` con:

```powershell
cd app2
```

Ejecuta los siguientes comandos desde la carpeta `app2/`.

Validar la configuración:

```powershell
docker compose --env-file infra/.env -f infra/compose.yaml config
```

Construir las imágenes y arrancar los contenedores:

```powershell
docker compose --env-file infra/.env -f infra/compose.yaml up --build -d
```

Comprobar el estado:

```powershell
docker compose --env-file infra/.env -f infra/compose.yaml ps
```

> Estos comandos crearán el contenedor Docker necesario para ejecutar la aplicación.
>
> Para verlo, pararlo, arrancarlo y visualizar logs, se puede usar `Docker Desktop`,
> ya que permite trabajar con el contenedor más fácilmente.

### 3. Acceder a la aplicación

Abre en el navegador:

`http://localhost:8080`

Comprueba que la web carga, que Clerk permite autenticarse y que puedes enviar un texto y recibir el resumen generado por la IA.

> **IMPORTANTE:**
>
> Es probable que dé errores. Al usar un modelo gratuito de `OpenRouter`
> tiene limitaciones y a veces saltan errores a la hora de consultar.
>
> Simplemente haz varias requests hasta que una de ellas consiga ejecutarse al completo.

### 4. Consultar los registros

Para diagnosticar problemas de arranque:

```powershell
docker compose --env-file infra/.env -f infra/compose.yaml logs
```

Para seguir los registros en tiempo real:

```powershell
docker compose --env-file infra/.env -f infra/compose.yaml logs -f
```

> También se puede usar `Docker Desktop` para visualizar los logs.

### 5. Detener la aplicación

Para detener y eliminar los contenedores y la red creada por Compose:

```powershell
docker compose --env-file infra/.env -f infra/compose.yaml down
```

> También se puede detener desde `Docker Desktop`.
