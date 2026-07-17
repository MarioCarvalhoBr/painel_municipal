---
name: atualizar-design-penpot
description: Fluxo para integrar um export do Penpot como página do relatório. Use quando chegar um novo design (ou revisão) de página vindo do Penpot em local_data/.
---

# Integração de Design do Penpot

Fluxo estabelecido no projeto (ver `.specs/business-rules/02-report-pages.md`):

1. **Origem**: o export do Penpot chega em `local_data/src-atualizado/src/{pagina}/` (`index.html`, `styles.css`, `data.js`, `imgs/`). Nunca edite direto no `local_data/` — é área de staging.
2. **Adaptações obrigatórias ao copiar para `backend/src/static/report/{pagina}/`**:
   - Remover todo `@font-face` do CSS — fontes vêm de `../shared/css/fonts.css` (Roboto).
   - Manter o comentário de cabeçalho citando o board Penpot de origem (rastreabilidade).
   - Converter textos que são dados do município em variáveis Jinja2 (`{{ county_record.county }}`, etc.); textos fixos e tokens de cor ficam em `data.js` (`window.PAGE_DATA`).
   - Assets com caminho relativo `./imgs/...` (resolvidos via `base_url`).
   - Conferir dimensões: página 842×595 px, margens zero.
3. **Nomes de classe do Penpot** (ex.: `.rectangle-54ff94c2cd22`): preserve os sufixos hash — eles ligam o CSS ao board. Ao ajustar geometria manualmente, recalcule a centralização (`left + width/2 = 421` para centro horizontal).
4. **Validação**: gere a página real e compare visualmente com o board:
   `curl -o /tmp/p.pdf "http://localhost:3000/api/v1/reports/pdf/{pagina}/{county_id}/"`
5. **Documentação**: mudanças de regra visual (novos elementos dinâmicos, novos estados) devem refletir em `.specs/business-rules/02-report-pages.md`.
6. **Commit**: em inglês com tag semântica (ex.: `feat: Update pagina5 layout from Penpot board X` ou `style:` para ajuste puramente visual).
