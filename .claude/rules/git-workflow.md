# Fluxo de Git

- Mensagens de commit **sempre em inglês**, com tag semântica: `feat:`, `fix:`, `style:`, `docs:`, `refactor:`, `chore:`, `test:`.
- Assunto no imperativo/descritivo curto; detalhes no corpo quando necessário.
- Um commit por mudança lógica — não misturar refactor com feature.
- Branch principal: `master`. Trabalho direto no master é aceito neste projeto (mantenedor único), mas features grandes devem usar branch dedicada.
- Nunca commitar: `.env`, dumps de banco, PDFs gerados, `local_data/` pesado.
- Release: bump de versão em `backend/pyproject.toml` (padrão `0.1.X`) em commit próprio (`feat:` ou `chore:`).
