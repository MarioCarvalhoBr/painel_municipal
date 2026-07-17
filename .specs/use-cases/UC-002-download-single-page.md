# UC-002 — Baixar Página Individual do Relatório

## Descrição
Obter o PDF de uma única página da ficha municipal (ex.: só a capa ou só as projeções climáticas), sem gerar o relatório inteiro. Usado para depuração de layout, downloads parciais e composição por scripts (`scripts/download_reports_by_page*.sh`, `scripts/merge_pages_range.sh`).

## Atores
- **Primário**: Desenvolvedor/designer validando uma página; scripts de lote.

## Pré-condições
- `page_name` ∈ {`pagina0` … `pagina8`}, registrado em `settings.pages_dir` **e** `settings.page_context_records`.
- Dados exigidos pela página existem para o `county_id`.

## Gatilho
`GET /api/v1/reports/pdf/{page_name}/{county_id}/` (nota: barra final obrigatória; `county_id > 0`).

## Fluxo principal
1. Sistema valida rate limit (200/min por IP).
2. Sistema valida `page_name` contra as páginas configuradas; inválido → `404 ERR_PAGE_NOT_FOUND`.
3. Sistema consulta **apenas** os repositórios listados em `page_context_records[page_name]` (otimização: páginas estáticas não consultam quase nada).
4. A projeção climática é consultada **sempre**, para obter o `geocode` que nomeia o arquivo.
5. Sistema chama `generate_pdf_page(context, page_name)`:
   - página estática → retorna o `file.pdf` reescalado;
   - página HTML → renderiza somente aquele template.
6. Resposta `200` com `application/pdf`, `filename="{geocode}.pdf"`.

## Fluxos alternativos / exceções
- **A1 — Página desconhecida** (na validação ou `KeyError` do serviço): `404 ERR_PAGE_NOT_FOUND`.
- **A2 — Dado obrigatório ausente**: `404` com a chave `ERR_*_NOT_FOUND` do conjunto faltante.
- **A3 — Falha de renderização**: `500`.

## Regras de negócio envolvidas
- Mapa página→registros: ver [`../architecture/03-pdf-generation.md`](../architecture/03-pdf-generation.md#otimização-de-contexto-por-página).

## Referências
- `backend/src/application/router.py` (`download_report_page_pdf`)
- `backend/src/core/config.py` (`page_context_records`)
