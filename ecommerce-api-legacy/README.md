# ecommerce-api-legacy

LMS API (com fluxo de checkout) em Node.js/Express usada como entrada do desafio `refactor-arch`.

## Como rodar

```bash
cp .env.example .env
npm start
```

A aplicação sobe em `http://localhost:3000`. O banco SQLite é em memória e já carrega seeds automaticamente no boot.

Os endpoints administrativos exigem `x-admin-token` ou `Authorization: Bearer <token>` com o valor definido em `ADMIN_TOKEN`.

Exemplos de requisições estão em `api.http`.
