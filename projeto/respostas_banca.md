# Respostas para o banco de perguntas

Estas respostas usam a execução salva em `projeto_qualidade_vinhos_completo.ipynb`. Cada integrante deve saber localizar as tabelas e explicar as decisões, mesmo quando outra pessoa assinar a seção correspondente.

## 1 Modelo de referência e ganho

O modelo de referência é um `DummyRegressor` que prevê sempre a mediana do conjunto de desenvolvimento. No teste, seu MAE foi 0,643. A floresta teve MAE 0,529, redução de 0,114 ponto ou 17,7%. O ganho existe, mas o R² de 0,396 mostra que a maior parte da variação individual ainda não foi explicada.

**Onde mostrar:** tabela final de comparação no notebook.

## 2 Tipo de saída e relação com a pergunta

O modelo devolve um número, a nota estimada `quality`, por exemplo 6,3. Isso corresponde à pergunta “qual nota esta amostra deve receber?” e caracteriza regressão. A previsão contínua preserva a ordem e a distância aproximada entre as notas.

**Onde mostrar:** abertura do notebook e função `prever_amostra`.

## 3 Decisão alimentada pela saída

A previsão ordena amostras para uma segunda degustação humana. A regra envia primeiro as amostras com nota prevista de pelo menos 6,0. O sistema não aprova nem rejeita o vinho; o painel humano toma a decisão final.

**Onde mostrar:** curva de corte e métricas operacionais.

## 4 Motivo da métrica

O MAE é a métrica principal porque mede a distância média em pontos de nota. Ele é fácil de explicar e não transforma regressão em porcentagem de acertos. RMSE penaliza mais os erros grandes e R² mede quanta variação o modelo explica; ambos aparecem como complementos.

**Onde mostrar:** tabela de validação e tabela de teste.

## 5 Erro relevante e quem é prejudicado

Para a triagem, o erro mais preocupante é o falso negativo: um vinho realmente 7 ou maior que não segue para degustação prioritária. No teste, a regra recuperou 165 dos 202 vinhos de interesse e deixou 37 de fora. Falsos positivos consomem capacidade do painel, mas não encerram a avaliação de um vinho.

O erro numérico também cresce nos extremos. O MAE foi 2,369 para nota 3, 1,211 para nota 4, 1,521 para nota 8 e 3,371 para a única amostra de nota 9. Esses grupos pequenos exigem cautela.

**Onde mostrar:** tabela de triagem e gráfico de erros por nota.

## 6 Variáveis mais usadas

Na importância por permutação, embaralhar `alcohol` aumentou o MAE em 0,137, o maior efeito. Depois vieram `volatile acidity` com 0,057 e `free sulfur dioxide` com 0,038. Isso combina com a expectativa de que composição química se associe à avaliação, mas não demonstra que alterar uma variável causará mudança na nota.

**Onde mostrar:** tabela e gráfico de importância por permutação.

## 7 Evidência de generalização

A floresta teve MAE médio de 0,531 nas cinco dobras, variando de 0,521 a 0,547. O teste, mantido fora das escolhas, teve MAE 0,529 e ficou dentro dessa faixa. A curva da árvore também mostra que profundidades maiores reduzem o erro de treino enquanto aumentam o de validação depois de cerca de 5, sinal de sobreajuste.

**Onde mostrar:** tabela de validação, curva da árvore e tabela de teste.

## 8 Variáveis ou linhas descartadas

Nenhuma coluna preditora foi descartada. Removemos 1.177 duplicatas completas e mantivemos 5.320 linhas. A decisão reduz o risco de cópias idênticas em treino e teste. Como não há identificador de amostra, não podemos afirmar que toda repetição era erro; essa é uma limitação declarada.

**Onde mostrar:** auditoria e divisão dos dados.

## 9 Informação conhecida apenas depois do evento

A nota `quality` só existe depois da avaliação sensorial e fica exclusivamente em `y`. Ela não entra em `X`. As 11 medidas e o tipo do vinho estão disponíveis antes da triagem. Também evitamos vazamento de preparação: codificação e escala aprendem somente na parte de treino de cada dobra.

**Onde mostrar:** definição de `X`, `y` e do pipeline.

## 10 Perda ao trocar um modelo simples por um complexo

A floresta reduziu o MAE, mas perdeu legibilidade. A regressão linear pode ser descrita por coeficientes e a árvore rasa por caminhos. A floresta combina centenas de árvores, custa mais para treinar e exige técnicas posteriores, como importância por permutação, para resumir dependências. Essa importância continua sem provar causalidade.

**Onde mostrar:** dicionário de modelos e importância por permutação.

## 11 Efeito de outra divisão treino e teste

O resultado mudaria. Nas cinco dobras, o MAE da floresta variou de 0,521 a 0,547. Essa faixa mostra sensibilidade à composição da amostra. `random_state=42` permite reprodução, mas não torna a divisão única ou universal.

**Onde mostrar:** colunas “pior dobra” e “melhor dobra” da comparação.

## 12 Onde o modelo não deve ser usado

O modelo não deve substituir degustadores, aprovar ou rejeitar lotes automaticamente, certificar segurança sanitária, estimar preço ou orientar alterações químicas como se a importância fosse causal. Também não deve ser aplicado a outras regiões, variedades, safras, períodos ou laboratórios sem validação externa.

**Onde mostrar:** seção de limitações e restrições.

## 13 Modelos testados e escolha sem usar o teste

Testamos referência pela mediana, regressão linear, k-NN, árvore e floresta. Todos usaram as mesmas cinco dobras e o mesmo MAE. A floresta apresentou o menor MAE médio de validação e foi registrada como escolhida antes da célula de teste. O teste apareceu uma vez depois do congelamento do modelo e do corte.

**Onde mostrar:** comparação antes do teste, frase “Escolha congelada antes do teste” e tabela final.

## Divisão sugerida das seis seções

Substituam os identificadores pelos nomes reais do grupo antes da entrega.

| Responsável | Seções |
| --- | --- |
| Integrante 1 | 1 Objetivo da modelagem e 6 Restrições de uso |
| Integrante 2 | 2 Dados utilizados |
| Integrante 3 | 3 Desempenho e comparação e 5 Limitações |
| Integrante 4 | 4 Uso pretendido |

Todos devem entender o projeto completo, pois o banco permite perguntas de continuação como “por quê?”, “e se?” e “mostre no notebook”.
