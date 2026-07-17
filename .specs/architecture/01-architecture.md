# Arquitetura do Sistema

## Princípio

O backend segue **Clean Architecture**: dependências apontam sempre para dentro (Infrastructure → Application → Domain). O domínio não conhece FastAPI, SQL nem Playwright.

```
backend/src/
├── domain/           # Camada de Domínio (sem dependências externas de framework)
│   ├── entities.py       # Entidades Pydantic + regras de formatação (CommonBusinessRules)
│   └── interfaces.py     # Contratos abstratos (ABC) de repositórios e serviços
├── application/      # Camada de Aplicação
│   ├── router.py         # Endpoints FastAPI (casos de uso orquestrados)
│   └── dependencies.py   # Injeção de dependências (Depends)
├── infrastructure/   # Camada de Infraestrutura (implementações concretas)
│   ├── database.py           # PostgresDatabase (asyncpg)
│   ├── repository.py         # Repositórios SQL por agregado
│   ├── pdf_service.py        # PlaywrightPdfService (render + merge)
│   ├── image_service.py      # Download de imagens como data URI
│   └── project_info_service.py  # Metadados do projeto (pyproject.toml)
├── core/             # Configuração global
│   ├── config.py         # Settings (pydantic-settings, .env) + mapa de páginas
│   └── constants.py      # Enums: PdfEngineType, ErrorKeys
├── helpers/          # Utilitários puros
│   └── common/formatting/number_formatting_processing.py
├── static/report/    # Templates das páginas do relatório (paginaN/)
└── main.py           # Bootstrap FastAPI: CORS, rate limiting, rotas
```

## Regras de dependência

1. `domain/` **não importa** de `application/`, `infrastructure/` ou FastAPI. Pode usar Pydantic, pandas e `helpers/`.
2. `application/` depende apenas de `domain/` (interfaces + entidades) e `core/`. A escolha das implementações concretas acontece **exclusivamente** em `application/dependencies.py`.
3. `infrastructure/` implementa as interfaces de `domain/interfaces.py`. Toda nova integração externa (banco, browser, HTTP) entra aqui.
4. `core/config.py` é a **única fonte de verdade** para configuração: variáveis `.env`, engine de PDF, diretórios de template, dimensões das páginas (`pages_dir`) e mapa página→registros (`page_context_records`).

## Interfaces do domínio (contratos)

| Interface | Método(s) | Implementação |
|---|---|---|
| `DatabaseInterface` | `fetch_all(query, *args)`, `test_connection()` | `PostgresDatabase` |
| `CountyRepositoryInterface` | `get_counties()`, `get_county(id)` | `CountyRepository` |
| `RiskFactorRepositoryInterface` | `get_risk_factors_by_county_id(id)` | `RiskFactorRepository` |
| `MunicipalIndicatorsRepositoryInterface` | `get_municipal_report(id)` | `MunicipalIndicatorsRepository` |
| `MunicipalResilienceProfileRepositoryInterface` | `get_municipal_resilience_profile(id)` | `MunicipalResilienceProfileRepository` |
| `ClimateProjectionRepositoryInterface` | `get_climate_projection(id)` | `ClimateProjectionRepository` |
| `MunicipalHealthRepositoryInterface` | `get_municipal_health(id)` | `MunicipalHealthRepository` |
| `PdfServiceInterface` | `generate_single_page_pdf`, `generate_pdf_merged`, `generate_pdf_page` | `PlaywrightPdfService` |
| `ProjectInfoServiceInterface` | `get_project_info()` | `ProjectInfoService` |
| `ImageServiceInterface` | `fetch_as_data_uri(url)` | `ImageService` |

## Padrões transversais

- **Rate limiting**: SlowAPI, chave por IP remoto (`get_remote_address`), limite de `200/minute` nos endpoints de PDF. Excesso retorna HTTP 429.
- **CORS**: apenas origens listadas em `main.py` (`ALLOWED_ORIGINS`), métodos `GET` e `OPTIONS`.
- **Erros**: chaves padronizadas no enum `ErrorKeys` (`core/constants.py`), no formato `ERR_*`. Endpoints traduzem ausência de dados em HTTP 404 com a chave correspondente e falhas internas em HTTP 500.
- **Formatação numérica**: centralizada em `CommonBusinessRules` (`domain/entities.py`) — ver [`../business-rules/01-number-formatting.md`](../business-rules/01-number-formatting.md).

## Requisitos para novas funcionalidades

Ao adicionar um novo dado ao relatório:

1. Criar/estender a **entidade** e o **Report wrapper** (com `formatted_data_dict`) em `domain/entities.py`.
2. Declarar a **interface** do repositório em `domain/interfaces.py` e implementá-la em `infrastructure/repository.py` (consulta ao schema `painel_municipal`).
3. Registrar o provider em `application/dependencies.py` e injetar no endpoint em `application/router.py`.
4. Atualizar `page_context_records` em `core/config.py` caso o dado alimente uma página específica.
5. Consumir o registro no template Jinja2 da página (`static/report/paginaN/`).
