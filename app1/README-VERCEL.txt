RESUMIDOR DE TEXTOS: GUÍA DEL BACKEND

ESTRUCTURA
- main.py: crea la aplicación FastAPI.
- backend/routes.py: define la ruta /api/resumir.
- backend/openrouter.py: envía el texto a OpenRouter y recoge el resumen.
- backend/config.py: lee la clave de la API.
- api/index.py: permite a Vercel iniciar la API.

PROBAR EN TU ORDENADOR
1. Instala uv si todavía no lo tienes.
2. Abre una terminal en la carpeta principal del proyecto.
3. Ejecuta: uv sync
4. Copia backend/.env.example y crea backend/.env.
5. En backend/.env, añade tu clave real:
   OPENROUTER_API_KEY=tu_clave_real
6. Inicia el servidor: uv run uvicorn main:app --reload
7. Abre http://127.0.0.1:8000/docs para probar la API.

DESPLEGAR EL BACKEND EN VERCEL
1. Sube el proyecto a GitHub sin incluir backend/.env.
2. Importa el repositorio en Vercel usando la carpeta principal como directorio raíz.
3. En la configuración del proyecto, abre las variables de entorno y añade OPENROUTER_API_KEY con tu clave.
4. Vuelve a desplegar el proyecto.
5. La ruta para resumir textos será /api/resumir y la comprobación básica estará en /.

FRONTEND
El frontend de Vue está en la carpeta frontend y puede desplegarse como otro proyecto de Vercel seleccionando esa carpeta como directorio raíz. Como los proyectos están separados, configura VITE_API_URL en el frontend con la dirección completa del backend. Si el navegador bloquea las peticiones, configura CORS en FastAPI para permitir el dominio del frontend.

SEGURIDAD
No guardes ni subas claves privadas a GitHub. Usa las variables de entorno de Vercel para configurar la clave.
