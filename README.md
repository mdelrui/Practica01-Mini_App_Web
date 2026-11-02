# Practica 01 - Mini aplicación web con IA

Repositorio de la práctica con dos versiones de una aplicación web para resumir textos. App 1 implementa el flujo básico. App 2 amplía la aplicación con autenticación mediante Clerk, opciones de resumen y exportación.

## Estructura del repositorio

```text
.
├── app1/
│   ├── backend/             # Rutas, configuración y cliente de OpenRouter
│   ├── frontend/            # Vue 3 + TypeScript + Vite
│   ├── main.py              # Punto de entrada FastAPI de App 1
│   ├── pyproject.toml
│   ├── uv.lock
│   └── vercel.json
├── app2/
│   ├── backend/              # FastAPI, autenticación Clerk y servicio IA
│   ├── frontend/             # Vue 3 + TypeScript + Vite
│   ├── infra/                # Docker Compose, Dockerfiles y Nginx
│   ├── specs/                # Especificaciones y artefactos Spec Kit
│   └── vercel.json
├── docs/                     # ERS, pruebas, despliegues y evidencias
├── presentation/             # Presentación de la práctica
└── README.md
```

## Requisitos generales

- Git.
- Python 3.12 o superior.
- [uv](https://docs.astral.sh/uv/) para gestionar los entornos Python.
- Node.js 22.18 o superior y npm.
- Una clave de OpenRouter para probar la generación real de resúmenes.
- Para App 2: configuración de Clerk.
- Para Docker: Docker Engine o Docker Desktop con Docker Compose.

No es necesario configurar credenciales reales para ejecutar las pruebas automatizadas, ya que los tests del proveedor de IA utilizan mocks.

## Continuar el proyecto desde otro PC

Después de clonar el repositorio, sitúate en la carpeta principal del proyecto:

```bash
git clone https://github.com/mdelrui/Practica01-Mini_App_Web.git
cd Practica01-Mini_App_Web
```

Instala las dependencias de Python de todas las aplicaciones desde la raíz. El
proyecto está configurado como un workspace de `uv`, por eso se usa
`--all-packages`:

```bash
uv sync --all-packages
```

Instala también las dependencias de los dos frontends:

```bash
cd app1/frontend
npm ci
cd ../../app2/frontend
npm ci
cd ../..
```

Los archivos `.env` no se guardan en Git. Hay que crearlos copiando los
archivos `.env.example` de la aplicación que se vaya a usar y rellenarlos con
las credenciales propias. Los comandos de instalación y despliegue están
explicados en este README y en [`docs/despliegues.md`](docs/despliegues.md).

## App 1: versión básica

App 1 permite introducir texto, cargar archivos `.txt` o `.md` mediante arrastrar y soltar y mostrar el resumen generado. El backend valida entradas de hasta 5000 caracteres y llama a OpenRouter.

### Configuración y ejecución del backend

En una terminal:

```bash
uv sync --all-packages
```

Crea `app1/.env` a partir de `.env.example` y configura:

```env
OPENROUTER_API_KEY=tu_clave_de_openrouter
```

Compila el frontend:

```bash
cd frontend
npm ci
npm run build
cd ..
```

Arranca la aplicación desde `app1/`:

```bash
uv run python main.py
```

La aplicación estará disponible en `http://127.0.0.1:8000` y la documentación de la API en `http://127.0.0.1:8000/docs`.

El punto de entrada real es `app1/main.py`. Este crea la aplicación FastAPI, registra las rutas del backend y sirve `frontend/dist` cuando existe. No existe un `app1/backend/main.py`.

### Pruebas de App 1

Backend:

```bash
cd app1
uv run pytest -q
```

Frontend:

```bash
cd app1/frontend
npm ci
npm exec vitest run
```

## App 2: versión con autenticación

App 2 añade autenticación de Clerk, configuración de longitud del resumen, extracción opcional de ideas principales y glosario, y acciones para copiar o exportar el resultado.

### Backend

```bash
cd app2/backend
cd ../..
uv sync --all-packages
```

Configura las variables del backend tomando como referencia `app2/backend/.env.example`. Como mínimo, se necesitan `OPENROUTER_API_KEY`, `CLERK_ISSUER`, `CLERK_JWKS_URL` y `CORS_ORIGINS`.

Arranque local:

```bash
uv run uvicorn main:app --reload
```

### Frontend

```bash
cd app2/frontend
npm ci
npm run dev
```

Vite muestra en la terminal la dirección local del frontend (habitualmente `http://localhost:5173`).

### Pruebas

Backend:

```bash
cd app2/backend
uv run pytest -q
```

Frontend:

```bash
cd app2/frontend
npm ci
npm exec vitest run
```

## App 2 con Docker Compose

Crea `app2/infra/.env` a partir de `app2/infra/.env.example` y completa las variables necesarias. Desde la carpeta `app2/`:

```bash
docker compose --env-file infra/.env -f infra/compose.yaml config
docker compose --env-file infra/.env -f infra/compose.yaml up --build -d
docker compose --env-file infra/.env -f infra/compose.yaml ps
```

La interfaz se sirve en `http://localhost:8080` (el puerto del host se enlaza a `127.0.0.1`). El backend se mantiene en la red interna de Docker, incorpora `/health` para el healthcheck y Nginx actúa como proxy inverso. En producción, coloca un proxy HTTPS en el host delante de `127.0.0.1:8080`; no abras los puertos 8000 ni 8080 en el grupo de seguridad.

Para consultar los registros y detener los servicios:

```bash
docker compose --env-file infra/.env -f infra/compose.yaml logs -f
docker compose --env-file infra/.env -f infra/compose.yaml down
```

## Variables de entorno y seguridad

- No subas archivos `.env`, `.env.local`, claves API, tokens ni credenciales de AWS.
- Los archivos `.env.example` deben contener solo nombres de variables y valores ficticios.
- `OPENROUTER_API_KEY` debe permanecer en el backend.
- La clave publicable de Clerk puede utilizarse en el frontend. La clave secreta nunca debe exponerse al navegador.
- App 2 debe mantener la verificación de tokens y limitar CORS a los orígenes configurados.
- No publiques directamente el puerto interno del backend en producción.

## Despliegues y documentación

Las URL documentadas para Vercel y el estado del despliegue en AWS EC2 se recogen en [`docs/despliegues.md`](docs/despliegues.md). Las URL publicadas deben comprobarse manualmente antes de considerarlas operativas.

Documentación adicional:

- [ERS de App 1](docs/ERS-app1.md)
- [ERS de App 2](docs/ERS-app2.md)
- [Registro de pruebas](docs/pruebas.md)
- [Evidencias](docs/evidencias/evidencias.md)
- [Comparativa App 1 y App 2](docs/comparativa.md)
- [Proceso de desarrollo](docs/proceso.md)
- [Uso de herramientas de IA](docs/uso-ia.md)
- [Procedimientos de despliegue](docs/despliegues.md)
- [Guion de demostración y defensa](docs/demo.md)
- [Lista de tareas pendientes](docs/tareas_pendientes_app1_app2.md)
