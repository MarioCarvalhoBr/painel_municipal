# Visão Geral — Folha Municipal (AdaptaBrasil)

## Propósito

O **Folha Municipal** é uma aplicação web que gera **fichas municipais em PDF** com indicadores socioclimáticos dos municípios brasileiros, no contexto do projeto AdaptaBrasil (INPE). O objetivo é apoiar a tomada de decisão em políticas públicas de adaptação climática e resiliência municipal.

## Escopo funcional

1. **Listagem de municípios** — o usuário seleciona um município em uma lista carregada da base de dados.
2. **Geração de relatório completo em PDF** — relatório multipágina (páginas 0 a 8), em formato paisagem A4-like (842×595 px), mesclado em um único arquivo.
3. **Geração de página individual em PDF** — qualquer página do relatório pode ser gerada isoladamente (usado para depuração, downloads parciais e scripts de lote).
4. **Health check** — endpoint de diagnóstico com status do serviço, engine de PDF, páginas configuradas e conectividade do banco.

## Fora de escopo (versão 0.1.x)

- Autenticação/autorização de usuários (a API é pública, protegida apenas por rate limiting e CORS).
- Edição de dados pelo usuário (a base é somente leitura para a aplicação).
- Engines de PDF alternativos (WeasyPrint, WkHtmlToPdf, Puppeteer estão previstos no enum `PdfEngineType`, mas apenas Playwright está habilitado).

## Componentes

| Componente | Tecnologia | Responsabilidade |
|---|---|---|
| Backend | Python 3.12+, FastAPI, asyncpg, Jinja2, Playwright, pypdf | API REST, acesso a dados, renderização e mesclagem de PDFs |
| Frontend | HTML/CSS/Vanilla JS + Nginx | Seleção de município e disparo do download do PDF |
| Banco de dados | PostgreSQL 15 (schema `painel_municipal`) | Armazena os indicadores municipais consolidados |
| Scripts | Bash/Python (`scripts/`) | Download em lote de relatórios, verificação de completude, merge de páginas |

## Estrutura do relatório (páginas)

| Página | Origem | Conteúdo | Dados dinâmicos |
|---|---|---|---|
| pagina0 | Template HTML | Capa (Fichas Municipais) | `county_record` |
| pagina1 | PDF estático | Página institucional (logos, metodologia) | — |
| pagina2 | Template HTML | Fatores de risco climático (flor de risco) | `county_record`, `risks_record` |
| pagina3 | Template HTML | Indicadores municipais (território, população, socioeconomia) | `county_record`, `municipal_report_record` |
| pagina4 | Template HTML | Perfil de resiliência municipal (planos, desastres) | `county_record`, `municipal_resilience_profile_record` |
| pagina5 | Template HTML | Projeções climáticas (cenários observado/otimista/pessimista) | `county_record`, `climate_projection_record` |
| pagina6 | Template HTML | Saúde municipal (perfil epidemiológico, cobertura vacinal) | `county_record`, `municipal_health_record` |
| pagina7 | PDF estático | Página institucional | — |
| pagina8 | PDF estático | Página institucional | — |

## Documentos relacionados

- Arquitetura: [`architecture/01-architecture.md`](architecture/01-architecture.md)
- API: [`api/01-rest-api.md`](api/01-rest-api.md)
- Regras de negócio: [`business-rules/`](business-rules/)
- Casos de uso: [`use-cases/`](use-cases/)
