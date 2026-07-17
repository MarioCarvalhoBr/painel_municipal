# .specs — Especificações Técnicas do Folha Municipal

Centralização de especificações técnicas e requisitos do projeto **Folha Municipal — AdaptaBrasil (INPE)**.
Esta pasta documenta casos de uso, regras de negócio e definições técnicas detalhadas para guiar o desenvolvimento de novas funcionalidades.

## Estrutura

| Pasta / Arquivo | Conteúdo |
|---|---|
| [`00-overview.md`](00-overview.md) | Visão geral do projeto, objetivos e escopo |
| [`architecture/`](architecture/) | Arquitetura do sistema (Clean Architecture, modelo de dados, pipeline de PDF) |
| [`api/`](api/) | Especificação dos endpoints REST |
| [`business-rules/`](business-rules/) | Regras de negócio (formatação numérica brasileira, conteúdo das páginas do relatório) |
| [`use-cases/`](use-cases/) | Casos de uso detalhados (UC-XXX) |
| [`frontend/`](frontend/) | Especificação do frontend estático |
| [`infrastructure/`](infrastructure/) | Deploy, Docker, variáveis de ambiente e scripts operacionais |
| [`templates/`](templates/) | Modelos para criação de novas especificações |

## Convenções

- **Casos de uso** seguem a numeração `UC-NNN-nome-curto.md` e o modelo em [`templates/use-case-template.md`](templates/use-case-template.md).
- **Novas especificações** devem partir de [`templates/spec-template.md`](templates/spec-template.md).
- As especificações descrevem o **comportamento pretendido**; quando o código divergir da especificação, a divergência deve ser tratada como bug ou a especificação deve ser atualizada de forma explícita (via commit dedicado).
- Referências a código usam caminhos relativos à raiz do repositório (ex.: `backend/src/application/router.py`).

## Estado do projeto (referência)

- Versão atual do backend: **0.1.7** (`backend/pyproject.toml`)
- Stack: FastAPI + PostgreSQL (asyncpg) + Jinja2 + Playwright + pypdf; frontend Vanilla JS servido por Nginx; orquestração via Docker Compose.
