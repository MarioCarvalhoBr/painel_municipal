---
name: formatacao-brasileira
description: Regras de formatação numérica brasileira do Folha Municipal. Use ao criar/alterar qualquer valor exibido no relatório (moeda, percentual, unidades, IDH, cenários climáticos) ou ao adicionar campos a entidades *Report.
---

# Formatação Numérica Brasileira

Referência completa: `.specs/business-rules/01-number-formatting.md`. Implementação: `CommonBusinessRules` em `backend/src/domain/entities.py`.

## Regras inegociáveis

1. Convenção pt-BR: `1.234,56` (ponto = milhar, vírgula = decimal).
2. **Truncar** a 2 casas, nunca arredondar (`to_decimal_truncated`).
3. `None` → sempre travessão `"—"` (exceto dimensões de risco ausentes na pagina2, que ficam `""`).
4. Formatação acontece **somente** no wrapper `*Report` do domínio — nunca em template Jinja2, JS ou frontend.

## Qual formatador usar

| Situação | Função |
|---|---|
| Valor genérico com 2 casas | `brazilian_formatted_value` |
| Omitir `,00` (populações, anos) | `brazilian_formatted_value_ignore_two_zeros` |
| Contagens inteiras | `brazilian_formatted_value_integer` |
| Moeda grande (danos, PIB agregado) | `brazilian_formatted_value_currency_short` → `R$ 2,00 Mi/Bi` |
| Cenários climáticos (`_tend`, `_otim`, `_pes`) | `brazilian_formatted_signed_value` → `+1,23` / `−1,23` (U+2212) |

## Sufixos consagrados

`km²`, `hab/km²`, `%`, `% do município`, `% das famílias pobres`, `anos`, `para cada 1.000 hab`, `para cada mil hab`, `por 100 mil hab`, `°C`, `mm`, `R$ X/hab`. IDH-M ganha classificação: ≥0,800 Muito Alto; 0,700–0,799 Alto; 0,550–0,699 Médio; <0,550 Baixo.

## Ao adicionar um campo novo

1. Adicione o campo `Optional` na entidade.
2. Adicione a regra de formatação no `formatted_data_dict` do wrapper, reutilizando os formatadores acima.
3. Registre a regra em `.specs/business-rules/01-number-formatting.md`.
4. Se possível, cubra com teste unitário (função pura — ver `.claude/rules/testing.md`).
