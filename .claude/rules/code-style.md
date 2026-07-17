# Estilo de Código

## Idioma
- **Todo código-fonte gerado deve ser em inglês**: nomes de variáveis, funções, classes, comentários, docstrings e mensagens de log.
- Exceções (permanecem em português): textos exibidos ao usuário (UI do frontend e conteúdo do relatório PDF), termos de domínio vindos do banco (ex.: colunas `Ameaça`, `Capacidade adaptativa`) e a documentação interna (`.specs/`, `.claude/`).

## Python (backend)
- Seguir a Clean Architecture existente: `domain/` não importa de `application/`, `infrastructure/` nem de FastAPI. Implementações concretas só entram via `application/dependencies.py`.
- Entidades são modelos Pydantic com campos `Optional` e default `None`; cada agregado tem um wrapper `*Report` com `formatted_data_dict`.
- Consultas SQL sempre parametrizadas (`$1`, `$2`…), somente `SELECT`, no schema `painel_municipal`.
- Nomes: snake_case para funções/variáveis, PascalCase para classes, enums para constantes (`ErrorKeys`, `PdfEngineType`).
- Novos erros: adicionar chave `ERR_*` em `core/constants.py`; nunca strings soltas de erro.
- Logs de fluxo com `print` seguem o padrão existente (`--- mensagem ---`); não introduzir framework de logging sem decisão registrada em `.specs/`.

## Frontend (Vanilla JS)
- Sem frameworks nem dependências de CDN.
- Toda chamada à API usa a `API_BASE_URL` resolvida em `app.js`; nunca URL hardcoded no ponto de uso.
- Textos de interface em português brasileiro.

## Templates de relatório (`backend/src/static/report/`)
- Dimensão fixa 842×595 px; nada pode transbordar o viewport.
- CSS extraído do Penpot sem `@font-face` local (fontes em `shared/css/fonts.css`).
- Dados dinâmicos chegam formatados via contexto Jinja2; o template não calcula nem formata valores.
- Comentários no topo de `styles.css`/`data.js` indicam o board Penpot de origem — manter atualizados.
