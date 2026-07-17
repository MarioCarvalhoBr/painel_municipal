---
name: debug-pdf
description: Diagnóstico de problemas na geração de PDF (página em branco, layout quebrado, erro 500, imagem faltando, fonte errada). Use quando um PDF gerado sair diferente do esperado.
---

# Depuração da Geração de PDF

Pipeline: Jinja2 → HTML temporário → Chromium (Playwright, `file://`, `networkidle`) → `page.pdf()` → merge pypdf. Detalhes: `.specs/architecture/03-pdf-generation.md`.

## Roteiro de diagnóstico

1. **Reproduza isolado**: gere só a página problemática —
   `curl -s -o /tmp/p.pdf "http://localhost:3000/api/v1/reports/pdf/{pagina}/{county_id}/"` e confira o corpo em caso de erro (chave `ERR_*`).
2. **Erro 404 com `ERR_*_NOT_FOUND`**: dado ausente no banco para o `county_id` — confirme na tabela correspondente (mapa em `.specs/architecture/02-data-model.md`).
3. **Erro 500**: veja `make logs-backend`. Causas comuns: template com variável inexistente no contexto (confira `page_context_records` em `core/config.py`), `file.pdf` estático ausente, Chromium não instalado no container.
4. **Página renderiza mas layout quebrado**:
   - Imagem faltando → caminho relativo errado (assets resolvem via `base_url` = diretório da página; use `./imgs/...`).
   - Fonte errada → `shared/css/fonts.css` não referenciado ou `@font-face` local indevido.
   - Elemento fora de lugar → conferir geometria (viewport 842×595; centro horizontal em 421px).
   - Conteúdo cortado → transbordou o viewport; reduza dimensões, nunca aumente a página.
5. **Depuração visual rápida**: abra o template no navegador com um contexto fake — renderize o Jinja2 manualmente ou substitua as variáveis por valores de exemplo — antes de regenerar o PDF.
6. **Merge com página errada/faltando**: ordem e presença vêm de `settings.pages_dir`; confira a entrada e o sufixo (`.html` × `.pdf`).

## O que não fazer

- Não alterar as dimensões padrão (842×595) para "consertar" uma página.
- Não adicionar formatação de valores no template como paliativo — a correção é no domínio.
