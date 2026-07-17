---
description: Revisão de código das mudanças pendentes seguindo as regras do projeto
allowed-tools: Bash(git status), Bash(git diff *), Bash(git log *), Read, Grep, Glob
---

Revise as mudanças pendentes (working tree + staged) deste repositório:

1. Rode `git status` e `git diff` para levantar o que mudou.
2. Verifique conformidade com as regras do projeto:
   - `.claude/rules/code-style.md` (Clean Architecture, formatação só no domínio, SQL parametrizado)
   - `.claude/rules/security.md` (segredos, CORS, validação de entrada)
   - `.specs/` quando a mudança tocar comportamento especificado
3. Para templates de relatório: confira dimensões 842×595 px, centralização e ausência de formatação numérica no template.
4. Reporte os achados em ordem de severidade (bug > violação de regra > melhoria), citando `arquivo:linha`. Se estiver tudo certo, diga explicitamente.
