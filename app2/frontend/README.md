# frontend

ResumidorIA App 2 is a Vue single-page app. Authentication is provided by Clerk
in the existing screen; sign-in opens in a modal and does not add routes.

## Recommended IDE Setup

[VS Code](https://code.visualstudio.com/) + [Vue (Official)](https://marketplace.visualstudio.com/items?itemName=Vue.volar) (and disable Vetur).

## Recommended Browser Setup

- Chromium-based browsers (Chrome, Edge, Brave, etc.):
  - [Vue.js devtools](https://chromewebstore.google.com/detail/vuejs-devtools/nhdogjmejiglipccpnnnanhbledajbpd)
  - [Turn on Custom Object Formatter in Chrome DevTools](http://bit.ly/object-formatters)
- Firefox:
  - [Vue.js devtools](https://addons.mozilla.org/en-US/firefox/addon/vue-js-devtools/)
  - [Turn on Custom Object Formatter in Firefox DevTools](https://fxdx.dev/firefox-devtools-custom-object-formatters/)

## Type Support for `.vue` Imports in TS

TypeScript cannot handle type information for `.vue` imports by default, so we replace the `tsc` CLI with `vue-tsc` for type checking. In editors, we need [Volar](https://marketplace.visualstudio.com/items?itemName=Vue.volar) to make the TypeScript language service aware of `.vue` types.

## Customize configuration

See [Vite Configuration Reference](https://vite.dev/config/).

## Project Setup

```sh
npm install
```

### Clerk configuration

Create a local `.env` from `.env.example` and set `VITE_CLERK_PUBLISHABLE_KEY`
to the publishable key for the Clerk instance used by the backend. The key is
public configuration, not a secret. Do not commit `.env` or place session
tokens in frontend configuration.

The app intentionally shows an authentication-configuration error and blocks
summary requests when the publishable key is not configured. The backend must
use the issuer and JWKS URL from the same Clerk instance; see
`../backend/.env.example`. Do not guess or reuse values across Clerk
environments.

### Authentication responses

The frontend obtains the current session token at submit time and sends it only
in the `Authorization: Bearer` header. The backend returns `401` for missing or
invalid credentials and `503` when the verifier/JWKS is unavailable. A `503`
indicates a temporary verification outage, not an invalid user session. Neither
response triggers an automatic retry, and both preserve the entered text.

### Authentication tests

Automated tests use mocked Clerk/JWKS and the summary service; they do not need
real Clerk or OpenRouter credentials:

```sh
npm run test:unit -- --run
npm run type-check
```

Backend contract tests run from `../backend`:

```powershell
python -m pytest -q
```

### Compile and Hot-Reload for Development

```sh
npm run dev
```

### Type-Check, Compile and Minify for Production

```sh
npm run build
```

### Run Unit Tests with [Vitest](https://vitest.dev/)

```sh
npm run test:unit
```

### Lint with [ESLint](https://eslint.org/)

```sh
npm run lint
```
