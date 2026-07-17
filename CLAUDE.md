# Folha Municipal — AdaptaBrasil (INPE)

Gera fichas municipais em PDF com indicadores socioclimáticos. Especificações completas em `.specs/`.

## Stack
- Backend: Python 3.12+, FastAPI, asyncpg (PostgreSQL, schema `painel_municipal`), Jinja2, Playwright, pypdf, Poetry.
- Frontend: HTML/CSS/Vanilla JS servido por Nginx. Orquestração: Docker Compose (`make run`, `make logs-backend`).

## Arquitetura (Clean Architecture — `backend/src/`)
- `domain/` (entidades + interfaces, sem framework) ← `application/` (router + DI) ← `infrastructure/` (DB, PDF).
- Config centralizada em `core/config.py` (`.env` na raiz); erros padronizados em `core/constants.py` (`ERR_*`).
- Templates do relatório em `static/report/paginaN/` (842×595 px; ordem das páginas em `settings.pages_dir`).

## Convenções
- Todo código-fonte em **inglês** (identificadores, comentários, docstrings, logs); textos de UI/relatório em pt-BR.
- Commits: inglês, com tags semânticas (`feat:`, `fix:`, `style:`, `docs:`, `chore:`).
- Formatação numérica pt-BR só no domínio (`CommonBusinessRules`); valor ausente = `"—"`. Nunca formatar em JS/Jinja2.
- API versionada em `/api/v1` — sem breaking changes; textos de UI em português brasileiro.
- Regras detalhadas em `.claude/rules/`; versão do backend em `backend/pyproject.toml` (bump a cada release).
