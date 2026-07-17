# Estratégia de Testes

## Estado atual
- `backend/tests/` existe mas está vazio (apenas `__init__.py`). Novos testes devem usar **pytest** via Poetry (`poetry run pytest`), com `httpx` para testar endpoints FastAPI.

## Diretrizes para novos testes
- **Domínio primeiro**: regras de formatação (`CommonBusinessRules`, wrappers `*Report`) são funções puras — cobri-las com testes unitários é barato e de alto valor (truncamento, travessão `—`, faixas do IDH, sinal explícito, escala Mi/Bi).
- **Repositórios**: testar com `DatabaseInterface` fake (lista de dicts), sem banco real.
- **Endpoints**: usar `TestClient`/`httpx.AsyncClient` com dependências sobrescritas (`app.dependency_overrides`) — nunca depender de PostgreSQL vivo em teste unitário.
- **PDF**: teste de fumaça apenas (bytes começam com `%PDF`, contagem de páginas via pypdf); não comparar bytes exatos.

## Validação manual obrigatória
Mudanças visuais em páginas do relatório exigem geração real para conferência:
```bash
curl -o /tmp/pagina.pdf "http://localhost:3000/api/v1/reports/pdf/{page_name}/{county_id}/"
```
