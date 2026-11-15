# VarreSP
## Ficha da CitizenTech
| Campo | Projeto |
|---|---|
| Equipe | Observatório de Bairro |
| Cidade e território | São Paulo (SP), com a Lapa como caso de leitura e os 96 distritos como universo de comparação |
| Cidadão beneficiado | Morador ou pedestre exposto à falta de varrição |
| Problema | Como direcionar vistorias semanais dispondo de três vagas e apenas do histórico de pedidos? |
| Funcionamento | A solução agrega as reclamações, estima o volume e a probabilidade de alta e compara as filas de prioridade em dados históricos. |
| Tecnologias e partes | Python prepara o histórico e avalia as previsões. Oracle representa distritos, observações e previsões semanais. |
| Ecossistema | Moradores registram pedidos no SP156. A Prefeitura publica os registros. No piloto proposto, a supervisão de zeladoria confirma as prioridades em campo. |
| Indicador | Acertos nas vagas de vistoria e cobertura territorial. No piloto, medir tempo entre falha confirmada e correção. |
| ODS | ODS 11, cidades e comunidades sustentáveis, com foco na gestão dos serviços urbanos; ODS 16, instituições eficazes, pela possibilidade de auditar critérios de priorização. |
| Repositório | [MarcelloLM/gs-2026.2](https://github.com/MarcelloLM/gs-2026.2) |

## Entregas da Global Solution 2026.2

**Data Science & Statistical Computing.** [Notebook executado](DataScience/VarreSP.ipynb) · [ZIP para entrega](DataScience/Data_Science_VarreSP.zip) · [Fonte dos dados e instruções de reprodução](DataScience/README.md).

**Database Design.** [Documentação e diagrama](DataBase/Database_Design_VarreSP.pdf) · [DDL](DataBase/01_DDL.SQL) · [DML](DataBase/02_DML.SQL) · [DQL](DataBase/03_DQL.SQL). Execute os scripts nessa ordem em um esquema vazio.
