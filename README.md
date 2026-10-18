## Autores

- Francisco Luis Cara García
- Mario Delgado Ruiz

# Práctica 01 - Mini aplicación web

Este repositorio está organizado por aplicaciones y entregables, con la parte funcional principal en `app1` y el trabajo complementario en `app2`, `docs`, `infra` y `presentation`.

## Estructura del repositorio

```text
.
├── app1/
│   ├── backend/        # FastAPI
│   └── frontend/       # Vue 3 + TypeScript + Vite
├── app2/               # trabajo pendiente o segunda aplicación
├── docs/               # documentación de la práctica
├── infra/              # Docker y configuración de despliegue
├── presentation/       # material de presentación
├── README.md           # documentación general del repositorio
└── .gitignore
```

## app1: aplicación principal

`app1` contiene el proyecto web funcional base de la práctica. El backend está separado por módulos y sirve el frontend compilado, por lo que la aplicación se puede iniciar con un solo comando.

### Estructura de app1

```text
app1/
├── main.py                 # Punto de entrada de la aplicación
├── pyproject.toml          # Dependencias de Python
├── requirements.txt        # Dependencias directas de Python
├── backend/
│   ├── config.py           # Configuración de OpenRouter
│   ├── models.py           # Modelo de los datos recibidos
│   ├── openrouter.py       # Conexión con OpenRouter
│   └── routes.py           # Rutas de la API
└── frontend/
    ├── package.json        # Dependencias y comandos de Vue
    └── src/                # Código de la interfaz
```

### Frontend

Ubicación: `app1/frontend`

Tecnologías:

- Vue 3
- TypeScript
- Vite
- Vitest

Primera instalación y compilación:

```bash
cd app1/frontend
npm install
npm run build-only
```

En Windows PowerShell, si `npm` está bloqueado, se puede usar `npm.cmd`:

```powershell
cd app1\frontend
npm install
npm run build-only
```

El frontend se sirve desde el backend después de compilarlo.

### Backend

Ubicación: `app1/backend`

Tecnologías:

- Python 3.12+
- FastAPI
- Uvicorn
- OpenRouter

El backend está organizado en módulos:

- `routes.py`: contiene el endpoint `/api/resumir`.
- `models.py`: define los datos que recibe la API.
- `openrouter.py`: realiza la petición a OpenRouter.
- `config.py`: carga la clave de la API desde `.env`.

El archivo `.env` debe estar en `app1/backend/.env` y contener:

```env
OPENROUTER_API_KEY=tu_clave_de_openrouter
```

No se debe subir el archivo `.env` al repositorio.

### Ejecutar toda la aplicación

Desde la carpeta `app1`:

```bash
cd app1
uv sync
uv run python main.py
```

En Windows PowerShell:

```powershell
cd app1
uv sync
uv run python main.py
```

La aplicación se ejecuta normalmente en:

```text
http://127.0.0.1:8000
```

La interfaz web se abre en:

```text
http://127.0.0.1:8000
```

El endpoint para generar resúmenes es:

```text
POST http://127.0.0.1:8000/api/resumir
```

## app2

La carpeta `app2/` aparece como trabajo o segunda app en curso, con documentación y estado pendiente del proyecto.

### Estructura de app1

```text
app2/
├── main.py                 # Punto de entrada de la aplicación
├── pyproject.toml          # Dependencias de Python
├── requirements.txt        # Dependencias directas de Python
├── backend/
│   ├── main.py           #
│   ├── services.py           #
└── frontend/
    ├── package.json        # Dependencias y comandos de Vue
    └── src/                # Código de la interfaz
```

### Frontend

Ubicación: `app2/frontend`

Tecnologías:

- Vue 3
- TypeScript
- Vite
- Vitest

Primera instalación y compilación:

```bash
cd app2/frontend
npm install
```

El frontend se sirve desde el backend después de compilarlo.

### Backend

Ubicación: `app2/backend`

Tecnologías:

- Python 3.12+
- FastAPI
- Uvicorn
- OpenRouter

El backend está organizado en módulos:

- `main.py`:
- `services.py`:

El archivo `.env` debe estar en `app2/backend/.env` y contener:

```env
OPENROUTER_API_KEY=tu_clave_de_openrouter
```

Para ejecutar únicamente el backend:

```bash
python -m uvicorn main:app --reload
```

No se debe subir el archivo `.env` al repositorio.

## Documentación

La carpeta `docs/` reúne los documentos de la práctica, comparaciones, proceso, despliegues, pruebas y referencias del trabajo realizado.

## Infraestructura

La carpeta `infra/` contiene la configuración de despliegue y contenedores:

- `compose.yaml`
- `Dockerfile.backend`
- `Dockerfile.frontend`

## Despliegue en Vercel

Configura el directorio `app1` como raíz del proyecto en Vercel. Su `vercel.json`
define dos servicios: `backend` (FastAPI, raíz `.`) y `frontend` (Vite, raíz
`frontend`). Las peticiones `/api/*` se enrutan al backend y el resto al
frontend. La aplicación web llama a la API con la ruta relativa `/api/resumir`,
por lo que ambas usan el mismo dominio.

Define `OPENROUTER_API_KEY` en las variables de entorno de Vercel para el
servicio backend. No es necesaria una binding entre frontend y backend: el
navegador accede al endpoint mediante la ruta pública `/api/*`.

## Uso recomendado

1. Configurar `app1/backend/.env` con la clave de OpenRouter.
2. Compilar el frontend desde `app1/frontend`.
3. Iniciar toda la aplicación desde `app1/main.py`.
4. Revisar la documentación en `docs/` para conocer el proyecto.
5. Usar `infra/` para despliegues o pruebas de entorno.

## Notas

- La aplicación se inicia desde `app1/main.py`.
- FastAPI sirve los archivos compilados de `frontend/dist`.
- El backend está dividido en módulos sencillos dentro de `app1/backend`.
- Para ejecutar la aplicación localmente no es necesario utilizar Vercel.
- La parte principal de desarrollo está en `app1`.
- `app2`, `docs`, `infra` y `presentation` complementan la práctica y su entrega.
