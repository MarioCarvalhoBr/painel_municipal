# Pipeline de Geração de PDF

## Visão geral

O relatório é composto por páginas independentes definidas em `settings.pages_dir` (`backend/src/core/config.py`). Cada página é:

- **Template HTML** (`paginaN/index.html`) — renderizada com Jinja2 e convertida em PDF pelo Playwright (Chromium headless); ou
- **PDF estático** (`paginaN/file.pdf`) — anexada diretamente, com escala ajustada ao tamanho padrão.

A ordem das entradas em `pages_dir` **é a ordem das páginas no PDF final**.

## Especificação de página

Cada entrada de `pages_dir` mapeia `Path do template → config de impressão`:

```python
{template_dir / "pagina0" / "index.html": {
    "width": "842px", "height": "595px",
    "print_background": True, "landscape": False,
    "margin": {"top": "0px", "right": "0px", "bottom": "0px", "left": "0px"},
    # opcional: "scale": 1.50 (usado na pagina3)
}}
```

Requisitos:

1. Dimensão padrão de página: **842×595 px** (A4 paisagem em 96 dpi). Conversão para pontos PDF: `px × 72 / 96` (`_page_size_in_points`).
2. `device_scale_factor=3` no Chromium para alta resolução de render.
3. `prefer_css_page_size=True` é aplicado por padrão.
4. Chromium é lançado com `--disable-web-security --allow-file-access-from-files` para permitir assets locais (`file://`).

## Fluxo de renderização (página HTML)

1. O contexto recebe `base_url` = URI absoluta do diretório da página (para resolver `imgs/`, `styles.css`, `data.js`).
2. O template é renderizado com Jinja2 (`FileSystemLoader` no diretório da página).
3. O HTML resultante é escrito em arquivo temporário e aberto via `file://` com `wait_until="networkidle"` (garante carregamento de fontes e imagens antes do print).
4. `page.pdf(**config)` gera os bytes; o arquivo temporário é removido em `finally`.

## Fluxo de mesclagem (`generate_pdf_merged`)

1. Itera `pages_dir` na ordem declarada.
2. Página `.pdf`: valida existência, aplica `scale_to` para o tamanho padrão e anexa via pypdf.
3. Página `.html`: gera o PDF individual e anexa todas as suas páginas.
4. Escreve o resultado consolidado em memória (`io.BytesIO`) e retorna os bytes.

## Página individual (`generate_pdf_page`)

Localiza a entrada de `pages_dir` cujo diretório-pai é `page_name`; aplica o mesmo tratamento (estático × renderizado). `page_name` inexistente lança `KeyError` → HTTP 404 (`ERR_PAGE_NOT_FOUND`).

## Otimização de contexto por página

`settings.page_context_records` declara quais registros cada template realmente usa. O endpoint de página individual consulta **apenas** os repositórios necessários. Exceção: **a projeção climática é sempre consultada**, pois o `geocode` dela nomeia o arquivo baixado (`{geocode}.pdf`).

| Página | Registros exigidos |
|---|---|
| pagina0 | `county_record` |
| pagina1 | — (PDF estático) |
| pagina2 | `county_record`, `risks_record` |
| pagina3 | `county_record`, `municipal_report_record` |
| pagina4 | `county_record`, `municipal_resilience_profile_record` |
| pagina5 | `county_record`, `climate_projection_record` |
| pagina6 | `county_record`, `municipal_health_record` |
| pagina7 / pagina8 | — (PDF estático) |

## Estrutura de um diretório de página

```
static/report/paginaN/
├── index.html   # Template Jinja2 (ou file.pdf para página estática)
├── styles.css   # CSS extraído do design (Penpot), sem @font-face próprio
├── data.js      # window.PAGE_DATA: tokens de design e textos default
└── imgs/        # Assets locais da página
```

Recursos compartilhados ficam em `static/report/shared/` (fontes em `shared/css/fonts.css`, imagens comuns, JS utilitário). Os designs de referência são exportados do Penpot; a cópia de trabalho fica em `local_data/src-atualizado/` antes de ser integrada ao backend.

## Requisitos para adicionar uma nova página

1. Criar `static/report/paginaX/` com `index.html` (+ `styles.css`, `data.js`, `imgs/`) **ou** `file.pdf`.
2. Registrar a página no enum `Settings.PageName` e em `pages_dir` na posição desejada.
3. Declarar os registros usados em `page_context_records`.
4. Se precisar de dado novo, seguir o fluxo descrito em [`01-architecture.md`](01-architecture.md#requisitos-para-novas-funcionalidades).
