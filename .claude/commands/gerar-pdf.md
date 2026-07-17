---
description: Gera um PDF de teste (página individual ou relatório completo) e confere o resultado
argument-hint: [pagina0..pagina8|completo] [county_id]
allowed-tools: Bash(curl *), Bash(pdfinfo *), Bash(ls *), Read
---

Gere um PDF de teste da aplicação usando os argumentos: $ARGUMENTS

1. Confirme que o backend está de pé: `curl -s http://localhost:3000/api/v1/health` (verifique `database_status: connected`). Se não estiver, oriente a rodar `make run`.
2. Se o primeiro argumento for `completo` (ou vazio), baixe o relatório inteiro:
   `curl -s -o /tmp/report.pdf "http://localhost:3000/api/v1/reports/pdf/{county_id}"`
   Caso contrário, baixe a página individual:
   `curl -s -o /tmp/report.pdf "http://localhost:3000/api/v1/reports/pdf/{page_name}/{county_id}/"`
   (county_id padrão: 1)
3. Valide o resultado: arquivo começa com `%PDF`, tamanho > 0 e, se `pdfinfo` estiver disponível, reporte o número de páginas e dimensões.
4. Reporte o caminho do arquivo gerado e qualquer erro HTTP (chave `ERR_*` do corpo da resposta).
