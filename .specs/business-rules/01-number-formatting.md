# Regras de Negócio — Formatação Numérica Brasileira

Fonte: `CommonBusinessRules` em `backend/src/domain/entities.py` e `NumberFormattingProcessing` em `backend/src/helpers/common/formatting/number_formatting_processing.py`.

## Princípios gerais

1. **Convenção brasileira**: vírgula como separador decimal, ponto como separador de milhar (ex.: `1.234,56`).
2. **Truncamento, não arredondamento**: valores são truncados a 2 casas decimais antes de formatar (`to_decimal_truncated`, precision=2).
3. **Valor ausente** (`None`): renderizar **sempre** o travessão `"—"`.
4. Toda formatação acontece **no domínio** (wrappers `*Report`), nunca no template ou no frontend.

## Formatadores

| Função | Regra | Exemplo |
|---|---|---|
| `brazilian_formatted_value` | Trunca a 2 casas e formata pt-BR | `1234.567` → `1.234,56` |
| `brazilian_formatted_value_ignore_two_zeros` | Idem, mas omite decimais quando são `,00` | `1234.00` → `1.234` |
| `brazilian_formatted_value_integer` | Converte para inteiro truncado e formata | `1234.9` → `1.234` |
| `brazilian_formatted_value_currency_short` | ≥ 1 bi → `R$ X,XX Bi`; ≥ 1 mi → `R$ X,XX Mi`; abaixo → `R$` + formato pleno | `2_000_000_000` → `R$ 2,00 Bi` |
| `brazilian_formatted_signed_value` | Sinal explícito: `+` positivo, `−` (minus sign U+2212) negativo, `+0,00` para zero | `-1.23` → `−1,23` |

## Sufixos e unidades por indicador

### Indicadores municipais (pagina3)
- `area` → `{valor} km²`
- `renda_media`, `pib` → `R$ {valor}`
- `densidade_urb` → `{inteiro} hab/km²`
- Percentuais (`pop_urb_pct`, `pop_rural_pct`, `mulheres`, `pretos_pardos`, `pop_inf`, `pop_idosa`, `imigrantes`, `indigenas`, `quilombolas`, `alfabet`, `cob_vacinal`, `acesso_agua2`, `acesso_esgoto`, `acesso_energia`, `acesso_lixo`, `solic_refugio`, `tx_turismo`) → `{valor}%`
- `bolsa_familia` → `{valor}% das famílias pobres`
- `pop_urb_pessoas`, `pop_rural_pessoas`, `pop_fav`, `dom_semi_inadeq` → formato sem zeros decimais
- `leito_hab`, `prof_hab` → `{valor} para cada 1.000 hab`
- `escolaridade`, `expec_vida` → `{valor} anos`
- `firjan`, `imig_regist` → valor puro formatado

### Classificação do IDH-M
| Faixa | Rótulo |
|---|---|
| ≥ 0,800 | `(Muito Alto)` |
| 0,700 – 0,799 | `(Alto)` |
| 0,550 – 0,699 | `(Médio)` |
| < 0,550 | `(Baixo)` |

Formato final: `0,754 (Alto)`.

### Projeções climáticas (pagina5)
- Colunas de cenário (sufixos `_tend`, `_otim`, `_pes`) usam **sinal explícito** (`brazilian_formatted_signed_value`).
- Temperaturas (`temp_med*`, `temp_max*`, `temp_min*`) → `{valor} °C`
- Chuva extrema e precipitação (`chuva_ext*`, `precip*`) → `{valor} mm`
- Nível do mar (`nivel_mar`, `nivel_mar_tend`, `nivel_mar_30`, `nivel_mar_50`) → `{valor} mm`
- Dias secos/chuva → valor sem unidade

### Perfil de resiliência (pagina4)
- `veg_natural`, `agropec` → `{valor}% do município`
- Contagens de desastres (`estiagem_incend`, `geohidro`, `tornad_vendav`, `obitos`, `desabrig`, `desaloj`, `escola_risco`, `eventos_geohidro`, `pessoas_area_risco_cemaden`) → inteiro formatado
- `danos_prej_tot` → moeda em escala curta (`R$ X,XX Mi`/`Bi`)

### Saúde municipal (pagina6)
- Incidências e internações (`incid_*`, `intern_*`, `inter_*`) → `{inteiro} por 100 mil hab`
- `leitos_1000_hab`, `prof_saude_hab_2025`, `medicos_hab_2025` → `{inteiro} para cada mil hab`
- `despesas_saude` → `R${valor}/hab`
- Coberturas vacinais (`cob_vac_menor_2`, `cob_vac_influenza`) → `{valor}%`
- `cob_vac_geral`: pode chegar como **string em formato brasileiro** (`"1.234,5"`); deve ser normalizada (remover `.` de milhar, trocar `,` por `.`) antes de formatar; se a conversão falhar, exibir o valor original.

## Fatores de risco (pagina2)

- Linhas são agrupadas por `risk_id`; cada `detail` vira coluna transposta: `Ameaça`, `Exposição`, `Vulnerabilidade`, `Sensibilidade`, `Capacidade adaptativa`, com cor associada em `{detail}_color`.
- `current_value` e `future_value` também recebem versões formatadas (`formatted_current_value`, `formatted_future_value`).
- Dimensões ausentes permanecem como string vazia `""` (célula em branco, não travessão).
