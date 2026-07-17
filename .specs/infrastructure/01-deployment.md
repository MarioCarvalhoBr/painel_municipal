# Infraestrutura e Deploy

## Topologia (Docker Compose)

| Serviço | Container | Imagem/Build | Porta (host → container) |
|---|---|---|---|
| `db` | `painel_db` | `postgres:15-alpine` | `127.0.0.1:${DATABASE_SECRET_PORT}` → 5432 |
| `backend` | `painel_backend` | `backend/Dockerfile` (arg `PDF_ENGINE`) | `${BACKEND_SECRET_PORT}` → 8000 |
| `frontend` | `painel_frontend` | `frontend/Dockerfile` (Nginx) | `${FRONTEND_SECRET_PORT}` → 80 |

Regras:

1. A porta do PostgreSQL é **obrigatoriamente** vinculada a `127.0.0.1` no host — o banco nunca fica exposto à internet.
2. O backend roda `uvicorn src.main:app --reload` com o código montado como volume (hot reload em desenvolvimento).
3. Dados do banco persistem no volume nomeado `postgres_data`.
4. Portas são parametrizadas por variáveis `*_SECRET_PORT` no `.env` (defaults do `.env.example`: frontend 8000, backend 3000, db 5533).

## Variáveis de ambiente (`.env`, ver `.env.example`)

| Variável | Uso |
|---|---|
| `DB_HOST`, `DB_PORT`, `DB_NAME`, `DB_USER`, `DB_PASSWORD`, `DB_USE_SSL` | Conexão asyncpg (lidas por `Settings` via pydantic-settings) |
| `PDF_ENGINE` | Engine de PDF (`playwright` — único valor habilitado) |
| `FRONTEND_SECRET_PORT`, `BACKEND_SECRET_PORT`, `DATABASE_SECRET_PORT` | Mapeamento de portas no host |

O arquivo `.env` fica na **raiz do repositório** (o backend o lê via `BACKEND_DIR.parent / ".env"`). Nunca commitá-lo; `.env.example` é o contrato.

## Comandos operacionais (Makefile)

- `make run` — sobe tudo com rebuild (`docker compose up --build -d`)
- `make start` / `make stop` / `make restart`
- `make logs`, `make logs-backend`, `make logs-frontend`
- `make shell-backend` / `make shell-frontend` / `make shell-db`

## Deploy

- Produção atual: AWS (IP em `ALLOWED_ORIGINS` de `main.py`, porta 5530 do frontend).
- `deploy.sh` executa o fluxo de deploy; `erase_docker.sh` limpa o ambiente Docker local.
- CI/CD: `.github/workflows/deploy.yml`.
- **CORS**: novas origens de produção devem ser adicionadas explicitamente em `ALLOWED_ORIGINS` (`backend/src/main.py`).

## Scripts de lote (`scripts/`)

| Script | Função |
|---|---|
| `download_report.sh` | Baixa o relatório completo de um município |
| `download_reports_range.sh` / `download_reports_parallel.sh` | Download em faixa de `county_id`s / paralelo |
| `download_reports_by_page*.sh` | Baixa páginas individuais (com variante de correção de faltantes) |
| `merge_pages_range.sh` | Mescla páginas baixadas isoladamente |
| `verificar_nao_baixados.py` / `verifica_porcentagem.py` | Auditoria de completude dos downloads (usa `tabela_completa.csv`) |

Requisito: os scripts dependem apenas da API pública (`/api/v1/...`) — não acessam o banco diretamente.

## Versionamento

- Versão do backend em `backend/pyproject.toml` (`version`), exposta no `/health`. Incrementar a cada release (padrão atual: bump de patch em `0.1.X`).
- Commits: mensagens **em inglês** com tags semânticas (`feat:`, `fix:`, `style:`, `chore:` …).
