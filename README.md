## Autores
* Francisco Luis Cara García
* Mario Delgado Ruiz

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

`app1` contiene el proyecto web funcional base de la práctica, separando frontend y backend.

### Frontend

Ubicación: `app1/frontend`

Tecnologías:

- Vue 3
- TypeScript
- Vite
- Vitest

Comandos habituales:

```bash
cd app1/frontend
npm install
npm run dev
```

La app se ejecuta normalmente en:

```text
http://localhost:5173
```

### Backend

Ubicación: `app1/backend`

Tecnologías:

- Python 3.12+
- FastAPI
- uvicorn

Comandos habituales:

```bash
cd app1/backend
uv sync
uv run uvicorn main:app --reload
```

La API queda disponible en:

```text
http://127.0.0.1:8000
```

Endpoint actual:

```bash
curl http://127.0.0.1:8000/
```

Respuesta esperada:

```json
{ "message": "La API funciona correctamente" }
```

## app2

La carpeta `app2/` aparece como trabajo o segunda app en curso, con documentación y estado pendiente del proyecto.

## Documentación

La carpeta `docs/` reúne los documentos de la práctica, comparaciones, proceso, despliegues, pruebas y referencias del trabajo realizado.

## Infraestructura

La carpeta `infra/` contiene la configuración de despliegue y contenedores:

- `compose.yaml`
- `Dockerfile.backend`
- `Dockerfile.frontend`

## Uso recomendado

1. Entrar en `app1/frontend` y arrancar la interfaz.
2. Entrar en `app1/backend` y arrancar la API.
3. Revisar la documentación en `docs/` para contexto de la práctica.
4. Usar `infra/` para despliegues o pruebas de entorno.

## Notas

- El repositorio se organiza por módulos en lugar de mantener todo el proyecto a nivel raíz.
- La parte principal de desarrollo está en `app1`.
- `app2`, `docs`, `infra` y `presentation` complementan la práctica y su entrega.
