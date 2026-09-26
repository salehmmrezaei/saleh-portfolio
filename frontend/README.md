# Saleh Portfolio

The frontend for Saleh Rezaei's portfolio. It is a React and TypeScript application built with Vite.

## Development

From this directory:

```bash
npm ci
npm run dev
```

The Vite development server proxies `/api` requests to `http://127.0.0.1:8000` by default. Copy `.env.example` to `.env.local` to customize:

- `VITE_API_BASE_URL` sets the API base URL used by the browser.
- `VITE_API_PROXY_TARGET` sets the backend target for the local Vite proxy.

## Verification

```bash
npm run typecheck
npm run lint
npm test
npm run build
```

The portfolio data and contact form use the centralized API client in `src/api/client.ts`, which validates JSON responses at runtime.
