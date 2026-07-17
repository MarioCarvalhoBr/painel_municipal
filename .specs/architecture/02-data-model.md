# Modelo de Dados

## Fonte de dados

Banco PostgreSQL, schema **`painel_municipal`**. A aplicação é **somente leitura**: todas as consultas são `SELECT` parametrizados (asyncpg, placeholders `$1`). A chave de junção universal é **`county_id`** (inteiro, > 0).

## Tabelas consumidas

| Tabela | Repositório | Entidade | Alimenta |
|---|---|---|---|
| `adapta_data` | `CountyRepository` | `County` | Lista de municípios, capa (pagina0), cabeçalhos |
| `quatro_pg_2` | `RiskFactorRepository` | `RiskFactor` (lista) | pagina2 — fatores de risco |
| `pg_3` | `MunicipalIndicatorsRepository` | `MunicipalIndicators` | pagina3 — indicadores municipais |
| `pq_4` | `MunicipalResilienceProfileRepository` | `MunicipalResilienceProfile` | pagina4 — perfil de resiliência |
| `pag5_climaticos_observados_cenarios` | `ClimateProjectionRepository` | `ClimateProjection` | pagina5 — projeções climáticas (e `geocode` para nome de arquivo de toda página) |
| `pg_6` | `MunicipalHealthRepository` | `MunicipalHealth` | pagina6 — saúde municipal |

## Entidades (resumo dos campos)

### County
`county_id`, `geocode` (código IBGE), `county`, `state`, `region`, `display` (derivado: `CONCAT(county, ' - ', state)`).

### RiskFactor
Linhas granulares por risco × detalhe. Campos-chave: `risk_id`, `detail_id`, `sep_id`, `county_id`, `sep`, `risk`, `detail` (dimensão: Ameaça, Exposição, Vulnerabilidade, Sensibilidade, Capacidade adaptativa), `level`, `year`, `value`, `color`, `current_value`/`current_value_color`, `future_value`/`future_color`, `imageurl`, `risk_url`.
Ordenação da consulta: `current_value desc, sep_id, risk, detail`.

### MunicipalIndicators
Grupos: território (`area`, `regic_influencia`, `pop_urb_*`, `pop_rural_*`, `densidade_urb`, `pib`); características populacionais (`mulheres`, `pretos_pardos`, `pop_inf`, `pop_idosa`, `indigenas`, `quilombolas`); socioeconomia (`idh_m`, `renda_media`, `escolaridade`, `expec_vida`, `firjan`, `bolsa_familia`, `alfabet`); infraestrutura/serviços (`leito_hab`, `prof_hab`, `cob_vacinal`, `pop_fav`, `dom_semi_inadeq`, `acesso_agua2`, `acesso_esgoto`, `acesso_energia`, `acesso_lixo`); mobilidade (`imig_regist`, `solic_refugio`, `imigrantes`, `tx_turismo`).

### MunicipalResilienceProfile
Uso do solo (`bioma`, `veg_natural`, `agropec`, `ucs`, `ti`); gestão municipal (planos `plano_saneam`, `plano_residuos`, `plano_drenagem`, `plano_transporte`, `plano_hab`, `plano_diretor`, `plano_rrd`, `plano_conting`, `cid_resilientes` — valores textuais tipo "possui"/"não possui"); desastres (`estiagem_incend`, `geohidro`, `tornad_vendav`, `obitos`, `desabrig`, `desaloj`, `danos_prej_tot`); monitoramento CEMADEN (`escola_risco`, `eventos_geohidro`, `pessoas_area_risco_cemaden`).

### ClimateProjection
Para cada variável climática — `temp_med`, `temp_max`, `temp_min`, `dias_secos`, `dias_chuva`, `chuva_ext`, `precip` — existem 4 colunas: valor observado, `*_tend` (tendência observada), `*_otim` (cenário otimista) e `*_pes` (cenário pessimista). Nível do mar: `nivel_mar`, `nivel_mar_tend`, `nivel_mar_30`, `nivel_mar_50`. Também carrega `geocode` e `nm_munic`.

### MunicipalHealth
Perfil epidemiológico (`incid_arbo_2025`, `incid_lepto_2025`, `incid_hepatitea_2023`, `intern_dda_2025`, `inter_doenc_circ_2025`, `intern_doenc_resp_2025`); recursos (`leitos_1000_hab`, `prof_saude_hab_2025`, `medicos_hab_2025`, `despesas_saude`); cobertura vacinal (`cob_vac_geral` — pode vir como string com formato brasileiro —, `cob_vac_menor_2`, `cob_vac_influenza`).

## Invariantes e convenções

1. **Todos os campos de indicadores são opcionais** (`Optional`); valor ausente é sempre renderizado como travessão `"—"` (nunca `null`, `None`, `0` ou vazio).
2. Cada entidade possui um wrapper `*Report` que expõe:
   - `formatted_data_dict` — dados prontos para o template (formatação brasileira aplicada);
   - `formatted_data_df` — mesmo conteúdo como `pandas.DataFrame`;
   - `ClimateProjectionReport` expõe adicionalmente `pure_data_dict` (sem formatação — usado para extrair `geocode`).
3. Os templates recebem **somente dados já formatados**; nenhuma formatação numérica é feita em JS ou Jinja2.
4. `RiskFactorReport.formatted_data_dict` **transpõe** as linhas: agrupa por `risk_id` e transforma cada `detail` em coluna (`Ameaça`, `Exposição`, `Vulnerabilidade`, `Sensibilidade`, `Capacidade adaptativa`), com a cor correspondente em `{detail}_color`.
