PROYECTO: RESUMIDOR DE TEXTOS

BACKEND CON PYTHON Y UV
1. Abre una terminal en la carpeta principal del proyecto.
2. Ejecuta: uv sync
3. Copia backend/.env.example y crea el archivo backend/.env.
4. Dentro de backend/.env, añade tu clave de OpenRouter:
   OPENROUTER_API_KEY=tu_clave_real
5. Inicia el backend: uv run uvicorn main:app --reload
6. Prueba la API en http://127.0.0.1:8000/docs.

FRONTEND
1. Abre otra terminal y entra en la carpeta frontend.
2. Ejecuta npm install.
3. Ejecuta npm run dev.
4. Si el backend está en otro dominio, crea frontend/.env y configura VITE_API_URL con la dirección del backend.

DESPLIEGUE
- Backend: despliega la carpeta principal del proyecto en Vercel.
- Frontend: despliega la carpeta frontend como otro proyecto de Vercel.
- Añade OPENROUTER_API_KEY en las variables de entorno del proyecto del backend.
- No subas backend/.env a GitHub, porque contiene una clave privada.
