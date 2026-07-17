# UC-004 — Verificar Saúde do Serviço

## Descrição
Expor um endpoint de diagnóstico para monitoramento e troubleshooting: status do backend, engine de PDF ativa, páginas configuradas, versão do projeto e conectividade do banco.

## Atores
- **Primário**: Operador/DevOps, monitoramento externo, desenvolvedor.

## Gatilho
`GET /api/v1/health`

## Fluxo principal
1. Sistema monta a resposta base: `{"backend": {"status": "ok", ...}}`.
2. Adiciona `pdf_engine` (valor de `settings.pdf_engine`) e `pages_dir` (páginas configuradas).
3. Tenta ler os metadados do projeto (`ProjectInfoService` → `pyproject.toml`: nome, versão, descrição) e agrega em `project`.
4. Tenta abrir/fechar uma conexão com o banco (`test_connection`) e agrega `database_status: "connected" | "disconnected"`.
5. Responde `200` sempre que o processo estiver de pé.

## Regras de negócio
- **Resiliência**: falha em qualquer verificação parcial (metadados, banco) **não** derruba o endpoint — o erro é logado e o campo omitido/degradado. HTTP 200 indica apenas "processo vivo"; a saúde real do banco deve ser lida em `database_status`.

## Requisitos de monitoramento
- Sistemas de monitoramento devem alertar quando `database_status != "connected"`, mesmo com HTTP 200.

## Referências
- `backend/src/application/router.py` (`health_check`)
- `backend/src/infrastructure/project_info_service.py`
