---
description: Prepara uma release - bump de versão no pyproject.toml e commit padronizado
argument-hint: [patch|minor|major]
allowed-tools: Read, Edit, Bash(git *)
---

Prepare uma release do backend (tipo de bump: $ARGUMENTS — padrão: patch):

1. Leia a versão atual em `backend/pyproject.toml`.
2. Calcule a nova versão (padrão do projeto: série `0.1.X`, bump de patch).
3. Atualize o campo `version` no `pyproject.toml`.
4. Confirme com `git diff` que só a versão mudou e commite:
   `chore: Bump version to {nova_versao} in pyproject.toml`
   (mensagem em inglês, tag semântica — ver `.claude/rules/git-workflow.md`).
5. Reporte a versão anterior, a nova e o hash do commit. Não faça push sem pedido explícito.
