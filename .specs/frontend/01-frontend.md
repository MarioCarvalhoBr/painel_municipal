# Especificação do Frontend

## Escopo

Aplicação estática mínima (sem framework): `frontend/index.html`, `frontend/css/style.css`, `frontend/js/app.js`, servida por **Nginx** (container `painel_frontend`).

## Funcionalidade

1. Ao carregar (`DOMContentLoaded`), busca `GET {API}/counties` e popula o `<select id="county-select">` com placeholder "Selecione um município...".
2. O botão `#download-btn` inicia desabilitado; habilita quando um município é selecionado.
3. Clique no botão abre `GET {API}/reports/pdf/{county_id}` em nova aba (`window.open`), o que dispara o download do PDF (por causa do `Content-Disposition: attachment`).

## Resolução da URL da API

Ordem de precedência em `resolveApiBaseUrl()`:

1. `window.APP_CONFIG.API_BASE_URL` (override explícito por configuração injetada).
2. Hostname local (`localhost`, `127.0.0.1`, `0.0.0.0`) → `http://localhost:3000/api/v1` (backend local).
3. Caso contrário → caminho relativo `/api/v1` (produção: o Nginx faz proxy para o backend — ver `frontend/nginx.conf`).

## Tratamento de erros

- Falha ao carregar municípios: o `<select>` exibe a opção desabilitada "Erro ao carregar os municípios" e o erro vai para o console.
- Clique sem seleção: guard clause silenciosa (não faz nada).

## Restrições

- Sem dependências externas (nenhuma lib JS/CSS de CDN).
- Textos da interface em **português brasileiro**.
- Qualquer nova chamada à API deve usar `API_BASE_URL` resolvida — nunca URL hardcoded no ponto de uso.
