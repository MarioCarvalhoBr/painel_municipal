# UC-001 — Baixar Relatório Completo em PDF

## Descrição
Usuário obtém a ficha municipal completa (páginas 0–8 mescladas) de um município em um único arquivo PDF.

## Atores
- **Primário**: Usuário final (via frontend) ou script de lote (`scripts/download_reports_*.sh`).
- **Sistema**: Backend FastAPI, PostgreSQL, Playwright/Chromium.

## Pré-condições
- Município existe na tabela `painel_municipal.adapta_data`.
- Todas as tabelas de dados possuem registro para o `county_id` solicitado.
- Backend com Chromium instalado (imagem Docker já provisiona).

## Gatilho
`GET /api/v1/reports/pdf/{county_id}` (no frontend: clique em "Download" após selecionar o município).

## Fluxo principal
1. Sistema valida rate limit (200/min por IP).
2. Sistema busca, em sequência: county, fatores de risco, indicadores municipais, perfil de resiliência, projeção climática e saúde municipal.
3. Sistema aplica as regras de formatação brasileira a cada conjunto (wrappers `*Report`).
4. Sistema monta o contexto único e chama `generate_pdf_merged`:
   - páginas HTML são renderizadas via Jinja2 + Playwright;
   - páginas estáticas (`file.pdf`) são anexadas com escala normalizada;
   - tudo é mesclado na ordem de `settings.pages_dir`.
5. Sistema responde `200` com `application/pdf` e `Content-Disposition: attachment; filename="{geocode}.pdf"`.

## Fluxos alternativos / exceções
- **A1 — Dados ausentes**: qualquer conjunto vazio → `404` com a chave `ERR_*_NOT_FOUND` correspondente; nenhum PDF é gerado.
- **A2 — Falha de renderização** (template inexistente, erro do Chromium, PDF estático ausente): `500` com detalhe da exceção.
- **A3 — Rate limit excedido**: `429` (handler padrão do SlowAPI).
- **A4 — Geocode indisponível**: nome do arquivo cai para `county_{county_id}.pdf`.

## Pós-condições
- Nenhum estado persistido; geração é stateless (arquivos temporários são removidos).

## Requisitos não funcionais
- Página renderizada em alta resolução (`device_scale_factor=3`).
- O endpoint deve permanecer stateless para permitir paralelização por scripts de lote.

## Referências
- `backend/src/application/router.py` (`download_report_pdf`)
- [`../architecture/03-pdf-generation.md`](../architecture/03-pdf-generation.md)
