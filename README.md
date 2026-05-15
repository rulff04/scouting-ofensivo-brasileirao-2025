\# Scouting Ofensivo do Brasileirão 2025



Projeto de análise de dados esportivos desenvolvido em \*\*Power BI\*\*, com foco em \*\*scouting ofensivo\*\* de jogadores do Brasileirão 2025.



O dashboard foi construído para avaliar jogadores ofensivos a partir de métricas de \*\*produção\*\*, \*\*criação\*\* e \*\*drible\*\*, combinadas em um \*\*Scouting Score autoral\*\*.



\## Objetivo do projeto



O objetivo deste projeto foi construir um modelo de avaliação ofensiva que permitisse responder perguntas como:



\- Quais jogadores ofensivos entregaram mais valor no Brasileirão 2025?

\- Quem se destaca mais em finalização, criação e drible?

\- Como comparar dois jogadores de forma visual e objetiva?

\- Como transformar métricas brutas em um score interpretável de scouting?



\## Ferramentas utilizadas



\- \*\*Power BI\*\*

\- \*\*Power Query\*\*

\- \*\*DAX\*\*

\- \*\*Python\*\*

\- \*\*Excel\*\*



\## Fontes de dados



Os dados utilizados no projeto foram consolidados a partir de duas fontes principais:



\- \*\*FBref\*\*

&#x20; - Standard Stats

&#x20; - Shooting

\- \*\*SofaScore\*\*

&#x20; - métricas complementares de criação e drible



O processo incluiu extração, limpeza, padronização e união das bases para formar uma tabela analítica final.



\## Metodologia



O projeto foi estruturado em etapas:



1\. Extração e organização dos dados

2\. Consolidação das bases do FBref e SofaScore

3\. Filtragem dos jogadores ofensivos

4\. Criação de métricas comparáveis por 90 minutos

5\. Construção de subscores por bloco

6\. Criação do \*\*Scouting Score\*\*



\### Blocos do modelo



O modelo foi organizado em quatro dimensões:



\- \*\*Finalização\*\*

\- \*\*Criação\*\*

\- \*\*Drible\*\*

\- \*\*Impacto ofensivo\*\*



\### Lógica dos subscores



Os subscores foram criados a partir de percentis das métricas ofensivas da base.



\#### Finalização

Baseado em métricas como:

\- gols sem pênalti por 90

\- finalizações no alvo por 90

\- gols por finalização

\- gols por finalização no alvo



\#### Criação

Baseado em:

\- assistências por 90

\- passes decisivos por 90

\- grandes chances criadas por 90



\#### Drible

Baseado em:

\- dribles certos por 90

\- acerto no drible %



\#### Impacto ofensivo

Baseado em:

\- participações sem pênalti por 90



\### Scouting Score



O score final foi construído com os seguintes pesos:



\- \*\*Finalização\*\* = 40%

\- \*\*Criação\*\* = 30%

\- \*\*Drible\*\* = 15%

\- \*\*Impacto ofensivo\*\* = 15%



\## Páginas do dashboard



\### 1. Visão Geral do Scouting

Página executiva com:

\- KPIs da base analisada

\- filtros por perfil, clube e jogador

\- Top 10 do Scouting Score

\- gráfico de dispersão com finalização, criação e drible



!\[Página 1 - Visão Geral](images/pagina1.png)



\### 2. Tabela de Scouting

Página de consulta detalhada com:

\- tabela completa dos jogadores analisados

\- métricas principais por jogador

\- formatação condicional para facilitar leitura comparativa



!\[Página 2 - Tabela de Scouting](images/pagina2.png)



\### 3. Comparação entre Jogadores

Página para comparação direta entre dois jogadores, com:

\- seleção independente de dois atletas

\- score e ranking de cada um

\- comparação visual por subscores



!\[Página 3 - Comparação entre Jogadores](images/pagina3.png)



\## Estrutura do repositório



```text

scouting-ofensivo-brasileirao-2025/

│

├── README.md

├── dashboard/

│   └── Scouting\_Ofensivo\_Brasileirao\_2025.pbix

├── data/

│   ├── scouting\_score\_2025.xlsx

│   ├── base\_scouting\_2025.xlsx

│   ├── base\_ofensivos\_2025.xlsx

│   ├── fbref\_standard\_2025.xlsx

│   ├── fbref\_shooting\_2025.xlsx

│   └── sofascore\_complemento\_2025.xlsx

├── scripts/

│   ├── fbref\_local\_standard.py

│   ├── fbref\_local\_shooting.py

│   ├── parse\_sofascore.py

│   ├── montar\_base\_final.py

│   └── criar\_scouting\_score.py

└── images/

&#x20;   ├── pagina1-visao-geral.png

&#x20;   ├── pagina2-tabela-scouting.png

&#x20;   └── pagina3-comparacao-jogadores.png





