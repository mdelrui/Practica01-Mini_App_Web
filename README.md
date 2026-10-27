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

* **Ubicación:** `app1/frontend`
* **Tecnologías:** Vue 3, TypeScript, Vite, Tailwind CSS, Vitest.

Para instalar dependencias y compilar el frontend:

```powershell
cd app1\frontend
npm install
npm run build-only
```

### Backend de app1

* **Ubicación:** `app1/backend`
* **Tecnologías:** Python 3.12+, FastAPI, Uvicorn, Requests.

El backend se conecta a OpenRouter mediante peticiones HTTP estándar con `requests`:
* `config.py`: Carga la clave secreta `OPENROUTER_API_KEY` desde el archivo `app1/.env`.
* `openrouter.py`: Envía el texto a la API de OpenRouter (`chat/completions`) usando el modelo gratuito `liquid/lfm-2.5-2.6b:free`.
* `routes.py`: Expone el endpoint `POST /api/resumir`, recibiendo directamente `texto: str = Body(embed=True)` sin estructuras complejas.

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
*(O con entorno virtual activo: `python main.py`)*

La aplicación estará disponible en:
* Interfaz web y API: `http://127.0.0.1:8000`
* Documentación interactiva Swagger: `http://127.0.0.1:8000/docs`

---

## app2: Segunda aplicación (Versión avanzada con Spec-Kit)

`app2` es la versión avanzada del resumidor, desarrollada con opciones adicionales de personalización (ideas principales), gestión de errores tipada y especificaciones guiadas mediante Spec-Kit.

### Estructura de app2

```text
app2/
├── backend/
│   ├── .env.example        # Plantilla de configuración específica de app2
│   ├── main.py             # Servidor FastAPI independiente (endpoint POST /resumir y CORS)
│   ├── requirements.txt    # Dependencias de app2 (FastAPI, SDK openai, pydantic)
│   └── services.py         # Conexión a OpenRouter usando el SDK oficial de OpenAI y excepciones
├── frontend/
│   ├── package.json        # Dependencias de Vue para app2
│   └── src/                # Interfaz de usuario con opciones de extracción
└── specs/                  # Especificaciones dirigidas (Spec-Kit, contratos y data model)
```

### Backend de app2

* **Ubicación:** `app2/backend`
* **Tecnologías:** Python 3.12+, FastAPI, SDK de OpenAI (`openai`), Pydantic.
* **Módulos:**
  - `main.py`: Configura CORS, define el modelo `UserInput` con `main_ideas: bool` y maneja excepciones personalizadas.
  - `services.py`: Gestiona la conexión con OpenRouter mediante el cliente `OpenAI(base_url="https://openrouter.ai/api/v1")`, con control de timeouts y clases de error (`IAError`, `IATimeoutError`, `ResumenResponse`).

Para ejecutar el backend de `app2` por separado:

```powershell
cd app2\backend
pip install -r requirements.txt
python -m uvicorn main:app --reload
```

---

## Despliegue en Vercel

La aplicación configurada para el despliegue en Vercel es **`app1`**.

* Su archivo `app1/vercel.json` define el servicio de backend (FastAPI en `main:app`) y el frontend estático compilado con Vite.
* Las peticiones a `/api/*` se dirigen al backend y el resto de rutas al frontend.
* En el panel de Vercel debe configurarse la variable de entorno `OPENROUTER_API_KEY` dentro del servicio backend.

---

## Documentación e Infraestructura

* **`docs/`**: Contiene la ERS de ambas aplicaciones (`ERS-app1.md`, `ERS-app2.md`), comparativas, evidencias, pruebas y tutoriales.
* **`infra/`**: Dockerfiles y `compose.yaml` para despliegues contenerizados.
* **`presentation/`**: Diapositivas de defensa de la práctica.
