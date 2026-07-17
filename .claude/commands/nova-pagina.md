---
description: Guia a criação de uma nova página do relatório PDF seguindo o padrão do projeto
argument-hint: <nome-da-pagina> [descrição do conteúdo]
allowed-tools: Read, Write, Edit, Glob, Grep, Bash(ls *)
---

Crie a estrutura de uma nova página do relatório: $ARGUMENTS

Siga o checklist de `.specs/architecture/03-pdf-generation.md`:

1. Crie `backend/src/static/report/{nome}/` com `index.html`, `styles.css`, `data.js` e `imgs/`, usando uma página existente (ex.: `pagina0`) como referência de estrutura (842×595 px, fontes de `../shared/css/fonts.css`, `window.PAGE_DATA` em `data.js`).
2. Registre a página em `backend/src/core/config.py`:
   - novo membro no enum `Settings.PageName`;
   - entrada em `pages_dir` na posição desejada do PDF final;
   - registros usados em `page_context_records` (consulte `.specs/architecture/03-pdf-generation.md` para os nomes válidos).
3. Se a página precisar de dado novo do banco, siga o fluxo de `.specs/architecture/01-architecture.md` (entidade → interface → repositório → dependencies → router).
4. Ao final, indique como validar: `GET /api/v1/reports/pdf/{nome}/{county_id}/` e atualize `.specs/business-rules/02-report-pages.md` com as regras da nova página.
