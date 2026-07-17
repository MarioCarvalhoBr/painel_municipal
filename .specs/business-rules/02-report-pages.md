# Regras de Negócio — Páginas do Relatório

Cada página vive em `backend/src/static/report/paginaN/` e segue o padrão descrito em [`../architecture/03-pdf-generation.md`](../architecture/03-pdf-generation.md). Os designs vêm de boards do Penpot; o CSS exportado é adaptado (sem `@font-face` local — fontes vêm de `shared/css/fonts.css`, família principal **Roboto**).

## Regras comuns a todas as páginas

1. Dimensão fixa **842×595 px** (paisagem); nenhum conteúdo pode ultrapassar o viewport.
2. Textos dinâmicos vêm do contexto Jinja2 (`county_record`, `*_record`); textos fixos e tokens de design ficam em `data.js` (`window.PAGE_DATA`).
3. Identificação do município: `{{ county_record.county }} - {{ county_record.state }}` (exibida em caixa alta via CSS `text-transform: uppercase`).
4. Valores já chegam formatados do backend — o template não faz cálculo nem formatação.
5. Cores dos indicadores de risco vêm do banco (`color`, `current_value_color`, `future_color`, `{detail}_color`) e são aplicadas inline.

## pagina0 — Capa

- Título "Fichas Municipais" e figura de fundo (`figura-mapa-quadrados-coloridos.png`) cobrindo a página.
- Caixa do município (`.rectangle-*`): centralizada horizontalmente (o centro da caixa deve coincidir com `842/2 = 421px`), com o nome `município - UF` centrado dentro dela. Largura atual: 360px (`left: 241px`).
- Dados: apenas `county_record`.

## pagina1 — Institucional (PDF estático)

- `file.pdf` fornecido pela equipe de design; explica a metodologia AdaptaBrasil (flor de risco, lógica dos indicadores, logos INPE/AdaptaBrasil/GIZ/Plano Clima).
- Sem dados dinâmicos. Substituição = trocar o arquivo `file.pdf`.

## pagina2 — Fatores de Risco Climático

- Tabela transposta de riscos: uma linha por risco (`risk_id`), colunas Ameaça/Exposição/Vulnerabilidade/Sensibilidade/Capacidade adaptativa, valores atuais e futuros com suas cores.
- Ordem das linhas: `current_value` decrescente (riscos mais críticos primeiro), depois `sep_id`, `risk`, `detail`.
- Iconografia "flor de risco".

## pagina3 — Indicadores Municipais

- Blocos: caracterização territorial, características da população, condições socioeconômicas, infraestrutura e serviços, mobilidade.
- Renderizada com `scale: 1.50` (config específica em `pages_dir`).
- Ícones temáticos (água, esgoto, energia, resíduos).

## pagina4 — Perfil de Resiliência Municipal

- Planos municipais exibidos com selo visual: `POSSUI` / `NÃO POSSUI` / `AUSENTE` (imagens em `imgs/`).
- Histórico de desastres (contagens) e danos totais em escala curta de moeda.
- Mapa do município quando disponível; fallback: `imagem-sem-mapa-do-municipio.png`.

## pagina5 — Projeções Climáticas

- Injeta o registro completo no template: `{{ climate_projection_record | tojson | safe }}` (consumido via JS da página).
- Cada variável climática mostra: valor observado + três cenários (tendência, otimista, pessimista) **com sinal explícito** (`+`/`−`).
- Ícones por variável (temperatura média/máx/mín, dias secos, dias de chuva, chuvas extremas, intensidade, nível do mar).

## pagina6 — Saúde Municipal

- Perfil epidemiológico (incidências por 100 mil hab), recursos de saúde (por mil hab), despesas per capita e coberturas vacinais (geral, menores de 2 anos, influenza 60+).

## pagina7 / pagina8 — Institucionais (PDF estático)

- Mesmo tratamento da pagina1.

## Fluxo de atualização de design

1. Design é editado no Penpot e exportado.
2. Export é colocado em `local_data/src-atualizado/src/paginaN/` para conferência.
3. Após validação visual, os arquivos são adaptados e copiados para `backend/src/static/report/paginaN/` (remover `@font-face`, apontar fontes para `shared/`, converter textos fixos em variáveis Jinja2 quando forem dinâmicos).
4. Validar o resultado gerando a página isolada: `GET /api/v1/reports/pdf/paginaN/{county_id}/`.
