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

## Executar
Extraia todo o ZIP para uma pasta. Abra VarreSP.ipynb no Jupyter e execute todas as células na ordem. O CSV incluído é a entrada completa para a análise. O notebook não precisa consultar a internet. Os nomes dos distritos mantêm a grafia da base municipal.

## Reconstituir o CSV municipal
A etapa opcional em fonte/reconstruir_csv.py baixa os quatro arquivos oficiais, confere o SHA-256 e reconstrói o painel ao lado do notebook. Requer Python e pandas, internet para essa etapa e espaço para os arquivos trimestrais. Os arquivos originais ficam em uma pasta temporária e são descartados ao final. O CSV usa UTF-8, separador vírgula e datas ISO.

| Coluna | Definição |
|---|---|
| distrito | Distrito registrado no SP156, normalizado em maiúsculas |
| semana | Segunda-feira que inicia o intervalo de sete dias |
| pedidos | Número de registros publicados do serviço no distrito e intervalo |

A unidade observada é o pedido publicado. A análise é documental. As decisões propostas e as três vagas de vistoria são hipóteses de piloto. O estudo não inclui visita, entrevista ou avaliação operacional de impacto.

## Fontes primárias

- [Dados do SP156 - 1º TRI 2025](https://dados.prefeitura.sp.gov.br/dataset/0aecfa2b-aa3a-40d4-8183-0d4351b7fd0a/resource/7c5aeb58-2cad-40ba-9e9e-af1c17cc5070/download/arquivo-final-1-trim-25.csv) — SHA-256 `f9d02a8bf358f019a5851e0d3d05daa236f803f5b22f254b66fd7b69f63e5170`.
- [Dados do SP156 - 2º TRI 2025](https://dados.prefeitura.sp.gov.br/dataset/0aecfa2b-aa3a-40d4-8183-0d4351b7fd0a/resource/f5df7f4a-d614-4f85-b4a0-263ec9370cd9/download/arquivo-final-2-trim-25.csv) — SHA-256 `66fc96cf4c4bed437b9f560f23aeb8d93c33d2ff7212fd0bc240742681bedc1e`.
- [Dados do SP156 - 3º TRI 2025](https://dados.prefeitura.sp.gov.br/dataset/0aecfa2b-aa3a-40d4-8183-0d4351b7fd0a/resource/3b1d2648-d586-40c8-819c-24fbb8005343/download/arquivo-final-3-trim-25.csv) — SHA-256 `6b5c382dbc409074db3a3dbdb577c4c2abc76c8009757a457a2a418956e22c2d`.
- [Dados do SP156 - 4º TRI 2025](https://dados.prefeitura.sp.gov.br/dataset/0aecfa2b-aa3a-40d4-8183-0d4351b7fd0a/resource/d3a98097-8128-45d4-b8fe-21874b81c971/download/arquivo-final-4-trim-25.csv) — SHA-256 `0a19e3451e30f33f1a8c2581608e1cc92d036915d0594737f0a2ceb0e05929cc`.

[Catálogo municipal Dados do SP156](https://dados.prefeitura.sp.gov.br/dataset/dados-do-sp156)
