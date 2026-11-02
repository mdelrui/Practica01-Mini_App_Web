# Frontend del resumidor de textos

Interfaz creada con Vue 3 y Vite.

## Requisitos

Instala Node.js y npm antes de continuar.

## Instalar dependencias

Desde esta carpeta, ejecuta:

```sh
npm ci
```

## Iniciar el frontend

```sh
npm run dev
```

## Comprobar y preparar para producción

```sh
npm run build
```

## Ejecutar las pruebas

```sh
npm run test:unit
```

## Revisar el código

```sh
npm run lint
```

## Conectar con el backend

Si el backend está desplegado en otro dominio, crea un archivo `.env` en esta carpeta y añade la dirección de tu API:

```env
VITE_API_URL=https://tu-backend.vercel.app
```

Cambia el ejemplo por la dirección real del backend. No pongas claves secretas en variables que empiecen por `VITE_`, porque se muestran en el navegador.
