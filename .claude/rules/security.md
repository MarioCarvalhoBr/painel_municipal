# Requisitos de Segurança

- **Segredos**: credenciais só em `.env` (nunca commitado; `.env.example` é o contrato). Não ler nem imprimir o conteúdo de `.env` em logs ou respostas.
- **SQL**: somente consultas parametrizadas via asyncpg (`$1`…); proibido interpolar entrada do usuário em SQL.
- **Banco**: porta do PostgreSQL vinculada a `127.0.0.1` no host (docker-compose) — não expor externamente.
- **API**: manter rate limiting (SlowAPI, 200/min por IP) nos endpoints de PDF; CORS restrito à lista `ALLOWED_ORIGINS` em `main.py` (adicionar origens explicitamente, nunca `*`); apenas verbos `GET`/`OPTIONS`.
- **Erros**: nunca expor stack trace ou detalhes de infraestrutura ao cliente; usar chaves `ERR_*` estáveis.
- **Playwright**: as flags `--disable-web-security --allow-file-access-from-files` existem apenas para renderizar assets locais dos templates; jamais carregar URLs externas não confiáveis nesse contexto.
- **Entrada**: validar parâmetros de rota (ex.: `county_id` int `gt=0`; `page_name` contra a lista de páginas configuradas).
