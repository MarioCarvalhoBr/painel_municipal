# Especificação da API REST

Base path: **`/api/v1`** — definido em `backend/src/application/router.py`.
Todos os endpoints são `GET`. CORS restrito às origens configuradas em `main.py`; verbos permitidos: `GET`, `OPTIONS`.

## GET /api/v1/health

Diagnóstico do serviço.

**Resposta 200** (exemplo):
```json
{
  "backend": {"status": "ok", "message": "Service is running"},
  "pdf_engine": "playwright",
  "pages_dir": ["..."],
  "project": {"name": "backend", "version": "0.1.7", "description": "Folha Municipal Backend API"},
  "database_status": "connected"
}
```

Regras:
- Falha ao ler `pyproject.toml` ou ao testar o banco **não** derruba o endpoint; o campo correspondente é omitido ou marcado como `disconnected`.

## GET /api/v1/counties

Lista todos os municípios disponíveis.

**Resposta 200**: `List[County]`
```json
[{"county_id": 1, "geocode": 3305158, "county": "São José do Vale do Rio Preto", "state": "RJ", "region": "Sudeste", "display": "São José do Vale do Rio Preto - RJ"}]
```

Regras:
- Ordenação por `display` (alfabética).
- Erros de consulta → HTTP 500 com `ERR_DATA_RETRIEVAL_FAILED`.

## GET /api/v1/reports/pdf/{county_id}

Gera o **relatório completo** (todas as páginas mescladas).

- **Rate limit**: 200 requisições/minuto por IP (HTTP 429 ao exceder).
- **Parâmetro**: `county_id` (int).
- **Resposta 200**: `application/pdf`, header `Content-Disposition: attachment; filename="{geocode}.pdf"` — o nome do arquivo é o **geocode IBGE** obtido da projeção climática (fallback: `county_{county_id}.pdf`).
- **Erros**:
  - 404 com chave específica quando qualquer conjunto de dados obrigatório não existe: `ERR_COUNTY_NOT_FOUND`, `ERR_RISK_FACTOR_NOT_FOUND`, `ERR_MUNICIPAL_REPORT_NOT_FOUND`, `ERR_MUNICIPAL_RESILIENCE_PROFILE_NOT_FOUND`, `ERR_CLIMATE_PROJECTION_NOT_FOUND`, `ERR_MUNICIPAL_HEALTH_NOT_FOUND`.
  - 500 quando a geração do PDF falha (`ERR_PDF_GENERATION_FAILED` no log; `detail` carrega a mensagem da exceção).

## GET /api/v1/reports/pdf/{page_name}/{county_id}/

Gera o PDF de **uma única página** do relatório.

- **Rate limit**: 200 requisições/minuto por IP.
- **Parâmetros**: `page_name` (str — `pagina0`…`pagina8`), `county_id` (int, `gt=0`).
- **Validação**: `page_name` deve existir em `settings.pages_dir` **e** em `settings.page_context_records`; caso contrário, 404 `ERR_PAGE_NOT_FOUND`.
- **Busca de dados condicional**: consulta apenas os repositórios listados em `page_context_records[page_name]`. A projeção climática é sempre consultada (nome do arquivo).
- **Resposta 200**: `application/pdf`, mesmo padrão de nome `{geocode}.pdf`.
- **Erros**: 404 por dado ausente (mesmas chaves do endpoint completo) ou página inexistente; 500 em falha de geração.

## Convenções de erro

- Chaves de erro são estáveis e definidas em `ErrorKeys` (`backend/src/core/constants.py`), formato `ERR_SNAKE_CASE`. Clientes devem tratar pela chave, não pela mensagem.
- Nunca expor stack trace ao cliente; logs detalhados ficam no stdout do backend.

## Compatibilidade

- Mudanças de contrato exigem novo prefixo de versão (`/api/v2`); o prefixo `/api/v1` não deve sofrer breaking changes.
