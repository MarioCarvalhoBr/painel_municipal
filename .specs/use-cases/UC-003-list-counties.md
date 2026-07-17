# UC-003 — Listar Municípios Disponíveis

## Descrição
Fornecer a lista de municípios com dados disponíveis para popular o seletor do frontend.

## Atores
- **Primário**: Frontend (carregamento da página inicial).

## Pré-condições
- Banco acessível; tabela `painel_municipal.adapta_data` populada.

## Gatilho
`GET /api/v1/counties` (disparado no `DOMContentLoaded` do frontend).

## Fluxo principal
1. Sistema executa `SELECT DISTINCT county_id, geocode, county, region, state, CONCAT(county, ' - ', state) AS display ... ORDER BY display`.
2. Cada registro é validado como entidade `County`.
3. Resposta `200` com a lista ordenada alfabeticamente por `display`.
4. Frontend popula o `<select>` usando `county_id` como valor e `display` como rótulo, e habilita o botão de download quando um item é selecionado.

## Fluxos alternativos / exceções
- **A1 — Lista vazia ou erro de consulta**: repositório lança `ERR_DATA_RETRIEVAL_FAILED` → `500`; frontend exibe "Erro ao carregar os municípios" no seletor.

## Regras de negócio
- `display` é sempre derivado no SQL como `{county} - {state}`; o frontend não concatena nada.
- A lista deve conter apenas municípios com registro em `adapta_data` (fonte de verdade da disponibilidade).

## Referências
- `backend/src/infrastructure/repository.py` (`CountyRepository.get_counties`)
- `frontend/js/app.js`
