# VarreSP | Registro de uso de IA e revisão técnica

**Equipe Observatório de Bairro · FIAP · Global Solution 2026.2**  
**Disciplina:** Data Science & Statistical Computing  
**Objeto da revisão:** notebook `VarreSP.ipynb`, painel semanal de reclamações de falta de varrição do SP156 e recomendação de vistorias para a cidade de São Paulo.

## 1. Os pedidos publicados sustentam as contagens do painel?

> Reconstrua o CSV a partir dos quatro arquivos trimestrais do SP156. Confira a assinatura de cada arquivo, o filtro do serviço e as datas das semanas completas. Reconcilie as exclusões com o total final. Considere a revisão aprovada se o CSV reconstruído for idêntico ao entregue e houver uma linha por distrito e semana. Explique o que significa uma contagem igual a zero.

**Conferência.** O script `fonte/reconstruir_csv.py` validou o SHA-256 das quatro cópias municipais e reproduziu o CSV byte a byte. O serviço aparece em 32.576 registros. A retirada de 23 registros sem distrito e de 532 registros nas semanas incompletas das extremidades deixa **32.021 pedidos**. Os 96 distritos e as 51 segundas-feiras formam **4.896 linhas**. Zero significa que o arquivo publicado não contém pedido desse serviço para aquele distrito naquela semana.

**Ajuste no código.** A primeira célula passou a comparar o índice observado com o calendário completo esperado. Assim, uma semana omitida e outra incluída por engano são detectadas mesmo quando o número total de linhas continua correto. A célula também verifica se as contagens são inteiras e não negativas.

## 2. O que seria conhecido na manhã da previsão?

> Assuma que a previsão é emitida na segunda-feira, antes de observar qualquer pedido daquela semana. Para cada distrito e data, recalcule as três variáveis usando exclusivamente as semanas encerradas. Verifique onde o código aprende a escala, o limite de alta demanda e o corte de probabilidade. Identifique qualquer escolha que dependa do teste antes da avaliação.

**Conferência.** Para cada uma das **4.512 linhas** com histórico suficiente, a auditoria recalculou a última contagem, a média das quatro semanas anteriores e a média de todo o histórico anterior. Os três valores coincidiram com os usados pelo notebook. As primeiras quatro semanas de cada distrito fornecem o histórico inicial. Os blocos seguintes somam **2.880 linhas de treino, 480 de validação e 1.152 de teste**, em ordem cronológica.

**Decisão.** Os dois padronizadores foram ajustados sobre as 2.880 linhas de treino. O percentil 75 do treino definiu alta demanda como **sete pedidos ou mais**. A escolha do corte de probabilidade, **0,25**, usou o F1 de validação. A operação semanal pressupõe acesso tempestivo a contagens que, na fonte pública consultada, estão reunidas em arquivos trimestrais.

## 3. A regressão linear ajuda a dimensionar as vistorias?

> Recalcule MAE, RMSE e R² a partir dos resíduos de teste. Compare a regressão com a média das quatro semanas anteriores nas mesmas observações. Localize o maior erro e explique se a escolha do modelo muda quando subestimar um pico é operacionalmente custoso.

**Conferência.** O cálculo direto pelos resíduos reproduziu as métricas da biblioteca. Os erros abaixo estão em pedidos por distrito e semana.

| Método | MAE | RMSE | R² |
|---|---:|---:|---:|
| Regressão linear | 3,015 | 6,206 | 0,761 |
| Média móvel de quatro semanas | 3,035 | 4,908 | 0,851 |

**Decisão.** A linear reduz o erro absoluto médio em cerca de 0,02 pedido. Em contrapartida, tem RMSE maior. Na Lapa, na semana de 17/11/2025, estimou 69,5 pedidos diante de 173 observados. Para dimensionar equipes em semanas atípicas, esse erro justifica consultar os registros locais antes de decidir o deslocamento.

## 4. O custo dos alertas é compatível com a ação proposta?

> Use exclusivamente as previsões do período de teste e mantenha o corte escolhido na validação. Reconstrua a matriz de confusão. A partir das quatro contagens, derive precisão, recall e F1. Diferencie o custo de um contato de triagem do custo de enviar uma equipe à rua.

**Conferência.** A classe positiva corresponde a sete pedidos ou mais. As linhas da matriz representam a demanda observada.

| Observado / previsto | Normal | Alta |
|---|---:|---:|
| Normal | 440 | 317 |
| Alta | 52 | 343 |

A precisão é **343/660 = 52,0%**. O recall é **343/395 = 86,8%**. O **F1 é 0,650**. As quatro contagens conciliam as 1.152 observações do teste.

**Decisão.** O corte recupera a maioria das semanas de alta demanda, mas gera 317 alertas falsos. Isso sustenta avaliar a logística em uma triagem remota de menor custo. Autorizar vistorias exige também considerar o limite semanal de equipes, tratado a seguir.

## 5. Qual regra merece as três vagas semanais?

> Aplique as duas regras aos mesmos distritos e conceda exatamente três vagas por semana a cada uma. Use o mesmo desempate. Conte vagas que coincidem com alta demanda, proporção das altas alcançadas e distritos distintos. Recomende a política inicial com base nesses resultados e indique qual evidência ainda falta para afirmar benefício ao morador.

**Conferência.** Nas 12 semanas de teste houve 395 casos de alta demanda. A ordenação usou desempate alfabético por distrito.

| Regra | Altas nas 36 vagas | Cobertura das 395 altas | Distritos visitáveis distintos |
|---|---:|---:|---:|
| Probabilidade da regressão logística | 29 | 7,3% | 4 |
| Média das quatro semanas anteriores | 36 | 9,1% | 6 |

**Decisão.** A média móvel é a primeira escolha para o piloto de vistorias. Seus 36 acertos coexistem com cobertura de apenas 9,1% das altas por causa do orçamento de três vagas. Em campo, a supervisão deve registrar falhas confirmadas e tempo até correção, além de acompanhar áreas onde poucos moradores usam o SP156. O teste retrospectivo mede a qualidade da priorização. O benefício ao morador dependerá da verificação em campo.

## 6. Quais dados são necessários para responder à pergunta?

> Liste as colunas do CSV e justifique cada uma com base na decisão de vistoria. Diga se uma linha permite identificar o solicitante ou confirmar que uma rua estava suja. Especifique qual evidência adicional seria necessária para confirmar a falha.

**Resultado.** O arquivo contém apenas `distrito`, `semana` e `pedidos`. As duas primeiras colunas identificam a unidade de análise e a terceira mede o volume registrado. O CSV não contém protocolo, endereço ou identificação pessoal. Vários relatos podem se referir à mesma ocorrência. Para confirmar uma falha, o piloto precisaria registrar o resultado de uma vistoria.

## 7. Os quatro trimestres permitem a mesma interpretação?

> Examine a tabela de origem na seção 1 do notebook. Confira a presença de registros em todos os dias de cada trimestre e procure indícios de limitação da extração. Separe a evidência de cobertura temporal da evidência de completude. Indique o que pode ser afirmado sobre o primeiro trimestre.

**Resultado.** Os arquivos contêm aberturas de serviços em 90, 91, 92 e 92 datas distintas. O primeiro contém exatamente 1.048.575 registros. Essa contagem merece conferência com a Prefeitura se os dados forem usados em produção. Por si só, ela não prova truncamento. As conclusões do estudo se referem aos pedidos publicados.

## 8. O que acontece se as semanas sem reclamação forem descartadas?

> Conte as linhas com zero pedidos e avalie a consequência de removê-las antes da média móvel. Use como exemplo um distrito que passa uma semana sem registro e recebe pedidos na seguinte. Especifique o intervalo de calendário que a variável “média de quatro semanas” deve representar.

**Resultado.** Há **267** combinações de distrito e semana com zero pedidos publicados. Removê-las faria a janela representar as quatro observações disponíveis mais recentes, que poderiam abranger mais de quatro semanas. O painel mantém os zeros nas semanas cobertas para conservar a janela de 28 dias.

## 9. As verificações do notebook detectam erros de entrada plausíveis?

> Em cópias temporárias do CSV, introduza um defeito por vez. Duplique uma chave distrito–semana, transforme uma contagem em −1 e troque uma segunda-feira válida por uma fora do período, mantendo o total de linhas. Execute as verificações de entrada em cada cópia e registre qual erro foi detectado.

**Resultado do teste.** A célula de entrada interrompeu as três execuções. As verificações acionadas foram, respectivamente, unicidade da chave, validade da contagem e correspondência com o calendário esperado. O terceiro caso demonstra por que contar 51 linhas por distrito seria insuficiente.

## 10. Como tratar um distrito que ainda não tem histórico suficiente?

> Determine a primeira semana elegível para previsão e reconcilie as linhas usadas para formar o histórico com o tamanho do painel. Examine a consequência de preencher a janela inicial com zeros. Defina como o protótipo deveria sinalizar esse caso ao operador.

**Resultado.** As quatro primeiras semanas de cada um dos 96 distritos fornecem **384 linhas de histórico inicial**. A primeira previsão avaliável começa em **03/02/2025**. Preencher as lacunas com zeros criaria uma história de baixa demanda que o arquivo não sustenta. Para um novo distrito, a aplicação deveria indicar “histórico insuficiente” até completar a janela.

## 11. É possível explicar uma previsão concreta ao responsável pela vistoria?

> Escolha a Lapa na semana de 17/11/2025. Reconstrua o que a supervisão teria em mãos na abertura da semana. Informe a última contagem, a média das quatro semanas anteriores e a média histórica. Apresente o valor observado ao final em uma coluna separada das entradas.

| Semana prevista | Última semana | Média de quatro semanas | Média histórica anterior | Observado ao final |
|---|---:|---:|---:|---:|
| 17/11/2025 · Lapa | 91 | 119,75 | 55,78 | 173 |

**Leitura.** O nível recente já superava a média histórica. O total de 173 só se tornou conhecido depois do encerramento. Essa distinção ajuda a explicar por que o pico era um risco que merecia atenção, mas seu tamanho exato continuava incerto.

## 12. Por que o percentil 75 produz mais de 25% de semanas de alta no treino?

> Refaça a definição do alvo binário com a distribuição discreta de pedidos. Conte separadamente os casos iguais ao limite e os maiores que ele. Quantifique quantas etiquetas mudariam se alguém trocasse `>=` por `>`. Especifique qual regra a equipe deve manter.

**Resultado.** No treino, **186** das 2.880 linhas têm exatamente sete pedidos e **687** têm mais de sete. A regra inclusiva classifica **873** linhas como alta, ou 30,3%. Uma alteração de um único operador mudaria 186 etiquetas e faria o modelo responder a outra pergunta. A definição adotada pelo projeto é “sete pedidos ou mais”.

## 13. O período de validação representa bem a frequência de alta demanda?

> Calcule a proporção de casos positivos no treino, na validação e no teste usando o mesmo limite. Explique que efeito uma diferença entre períodos pode ter sobre o número de alertas. Defina um indicador que a supervisão deveria acompanhar antes de reutilizar o corte em outro trimestre.

**Resultado.** A proporção de altas foi **30,3%** no treino, **54,2%** na validação e **34,3%** no teste. Setembro, usado para escolher o corte, concentrou mais altas. Em um piloto, a supervisão deveria acompanhar semanalmente a prevalência observada e a precisão dos alertas depois do fechamento dos registros.

## 14. O modelo superestima ou subestima o volume na maior parte das situações?

> Use o erro com sinal “previsto menos observado”. Calcule média e mediana no teste e compare com o percentil 90 do erro absoluto. Explique por que uma média próxima de zero não basta para dimensionar uma equipe.

**Resultado.** O erro médio com sinal foi **−0,17 pedido**, a mediana foi **+0,52** e o percentil 90 do erro absoluto foi **5,49 pedidos**. As superestimativas e subestimativas se compensam parcialmente na média. Para planejar uma semana individual, a distribuição do tamanho do erro é mais informativa.

## 15. Até que ponto o pico da Lapa explica o RMSE da regressão?

> Meça a participação da observação com maior erro na soma dos erros quadráticos. Como análise de sensibilidade, retire apenas essa linha e recalcule o RMSE da regressão e da média móvel nas mesmas linhas restantes. Preserve o resultado do teste completo como medida oficial.

**Resultado.** A observação de 17/11 na Lapa responde por **24,1%** da soma dos erros quadráticos da regressão. Ao retirá-la apenas para diagnóstico, o RMSE passa a **5,41** na linear e **4,65** na média móvel. A vantagem da média móvel em RMSE persiste além daquele pico.

## 16. As probabilidades aprendidas acrescentam informação à taxa histórica?

> Compare a probabilidade prevista para cada linha do teste com uma previsão constante igual à proporção de altas no treino. Use o escore de Brier, a média de `(probabilidade − evento observado)²`. Informe qual método tem menor erro e o que ainda falta verificar para interpretar “80%” em um distrito específico.

**Resultado.** O escore foi **0,1594** para a logística e **0,2269** para a taxa constante do treino. A logística melhora o erro probabilístico médio. Para interpretar uma faixa como 80%, seria necessário confrontar a frequência observada nessa faixa com as probabilidades emitidas e informar quantos casos sustentam a comparação.

## 17. Qual é a consequência operacional de elevar o corte de alerta?

> Mantendo o modelo fixo, compare o corte de 0,25 escolhido na validação com 0,50 como cenário de sensibilidade no teste. Informe alertas emitidos, falsos alertas e altas perdidas. Não use essa comparação retrospectiva para reescolher o corte oficial.

| Corte | Alertas emitidos | Falsos alertas | Altas perdidas |
|---|---:|---:|---:|
| 0,25 | 660 | 317 | 52 |
| 0,50 | 296 | 92 | 191 |

**Leitura.** Elevar o corte pouparia **364 contatos**, mas deixaria **139 altas adicionais** sem alerta. Antes de mudar a regra, o gestor precisaria estimar o custo de um contato e a consequência de perder uma ocorrência. A seleção de três distritos para vistoria usa a ordem das probabilidades e independe desse corte.

## 18. A recomendação muda com uma ou cinco vagas semanais?

> Repita a ordenação semanal com uma, três e cinco vagas, conservando o desempate e as mesmas 12 semanas de teste. Apresente os acertos sobre o total de vagas. Trate o resultado como cenário de capacidade e mantenha três vagas como hipótese principal do projeto.

| Vagas por semana | Média móvel | Probabilidade logística |
|---|---:|---:|
| 1 | 12/12 | 12/12 |
| 3 | 36/36 | 29/36 |
| 5 | 59/60 | 53/60 |

**Leitura.** Com uma vaga, as duas regras escolheram a Lapa nas 12 semanas. A diferença surge quando a equipe pode vistoriar outros distritos. Com cinco vagas, a média móvel continuou identificando mais casos de alta nessa janela de teste.

## 19. A boa taxa de acerto encobre concentração territorial?

> Para a regra recomendada de três vagas, conte quantas vezes cada distrito aparece. Verifique empates entre o terceiro e o quarto colocado. Explique como o desempate influencia a seleção e qual informação adicional seria necessária para avaliar a equidade territorial.

**Resultado.** A média móvel destinou **12 vagas à Lapa, 8 à Vila Mariana, 8 ao Jabaquara, 4 ao Belém, 3 à Vila Sônia e 1 à Saúde**. Em uma das 12 semanas houve empate entre a terceira e a quarta pontuação. A ordem alfabética torna a escolha reproduzível. Para avaliar equidade, a equipe precisaria também de medidas de cobertura do serviço e do acesso ao SP156 nos demais territórios.

## 20. Que evidência justificaria afirmar que o morador se beneficiou?

> Desenhe uma verificação de campo que diferencie “a fila antecipou reclamações” de “a falha foi corrigida mais cedo”. Defina unidade de acompanhamento, início e fim do indicador, período de comparação e tratamento de casos em aberto. Especifique o que o estudo atual já consegue medir.

**Proposta para o piloto.** A unidade é uma falha de varrição confirmada em vistoria. Registrar distrito, data de confirmação, data de correção e regra de seleção. Comparar a mediana de dias entre confirmação e correção com um período de referência de igual duração, informando também quantas falhas permanecem abertas após o mesmo prazo de acompanhamento. O notebook fornece o resultado retrospectivo da priorização. Esses registros de campo permitiriam avaliar se o serviço melhorou para o morador.

## Como conferir a entrega

Extraia o ZIP, mantenha o CSV ao lado de `VarreSP.ipynb` e execute o notebook do início ao fim. As seções 1 e 2 mostram o painel e a divisão temporal. As seções 3 e 4 apresentam os modelos, os gráficos e as métricas. A seção 5 compara as duas filas com o mesmo número de vagas. Para repetir a etapa opcional de reconstrução dos dados municipais, siga o README.
