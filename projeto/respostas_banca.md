# Respostas para a banca - Qualidade de vinhos

Este guia segue as 13 perguntas oficiais do `Banco_de_Perguntas.pdf`. Os números vêm da execução de 02/10/2026 do `projeto_qualidade_vinhos_completo.ipynb`. A resposta deve ser explicada com palavras próprias; a indicação ao fim de cada item ajuda a mostrar a evidência no notebook.

**Números para lembrar:** 6.497 linhas originais; 5.320 após retirar duplicatas; 4.256 no desenvolvimento; 1.064 no teste. Modelo escolhido: floresta aleatória com 350 árvores. MAE médio na validação: 0,531; MAE no teste: 0,529; referência no teste: 0,643. O corte 6,0 é apenas uma simulação de triagem.

## 1. Qual é o modelo de referência e quanto o nosso modelo melhora?

**Resposta:** A referência prevê sempre a mediana das notas do treino. No teste, seu MAE foi 0,643. A floresta teve MAE 0,529: errou 0,114 ponto de nota a menos, uma redução de 17,7%.

**No notebook:** seções 3 (referência e métrica) e 5 (avaliação final no teste).

## 2. O que o modelo devolve e como isso responde à pergunta?

**Resposta:** Ele devolve um número, a nota estimada do vinho, como 6,3. Nossa pergunta é qual nota sensorial podemos estimar a partir das medidas químicas e do tipo. Como a resposta é numérica, a tarefa é regressão.

**No notebook:** abertura, definição de `quality` como alvo e função `prever_amostra`.

## 3. Que decisão a saída alimenta? Como passamos do número à ação?

**Resposta:** No exercício, simulamos uma fila de revisão de vinhos com nota real 7 ou mais. Escolhemos o corte 6,0 nas previsões: notas previstas de 6,0 ou mais entram na fila. Esse foi o maior corte que manteve sensibilidade de pelo menos 75% nos dados de desenvolvimento. Não é uma regra comercial.

**No notebook:** seção 5, curva de corte e métricas da triagem no teste.

## 4. Por que usamos essa métrica?

**Resposta:** Usamos MAE porque ele mostra, em média, quantos pontos de nota a previsão erra. É fácil comparar com a referência: menor MAE significa menor erro. Acurácia não mede a distância entre notas; RMSE aparece só como complemento para destacar erros grandes.

**No notebook:** seção 3 e tabelas de validação e teste.

## 5. Qual erro seria o pior e para quem?

**Resposta:** Na triagem simulada, priorizamos não deixar um vinho realmente 7+ de fora. Isso aconteceu com 37 dos 202 vinhos 7+ do teste; quem faria a revisão perderia essas amostras. Também houve 204 falsos positivos, que aumentariam o trabalho. Como o uso é didático, não há uma decisão comercial real sendo tomada.

**No notebook:** curva de corte, métricas da triagem e erros por nota.

## 6. Quais variáveis o modelo mais usou? Era esperado?

**Resposta:** Pelo teste de importância por permutação, as três primeiras foram `alcohol` (aumento de 0,137 no MAE ao embaralhar), `volatile acidity` (0,057) e `free sulfur dioxide` (0,038). Esperávamos que medidas químicas ajudassem a estimar a nota. Essa análise mostra associação com a previsão; não prova que mudar uma medida mudará a nota.

**No notebook:** seção 6, tabela e gráfico de importância por permutação.

## 7. Como sabemos que o modelo aprendeu e não apenas decorou o treino?

**Resposta:** O MAE da floresta no treino foi 0,195, menor que na validação (0,531); isso mostra algum sobreajuste. Mesmo assim, o MAE no teste separado foi 0,529, próximo da validação e melhor que a referência (0,643). É evidência de que a floresta aprendeu padrões úteis, sem prometer o mesmo resultado em qualquer base nova.

**No notebook:** seção 5, comparação entre treino, cinco dobras e teste; seção 4, curva da árvore.

## 8. Descartamos alguma variável na auditoria? Por quê?

**Resposta:** Não descartamos colunas de entrada. Removemos 1.177 linhas totalmente repetidas antes da divisão, para evitar cópias em treino e teste. Ficaram 5.320 linhas. Mantivemos `wine_type`: sua importância isolada foi pequena, mas outras medidas podem carregar a mesma informação sobre o tipo. Sem identificador, algumas linhas repetidas podem ser vinhos diferentes; essa é uma limitação.

**No notebook:** seções 1 e 2 (auditoria e limpeza) e 7 (teste de `wine_type`).

## 9. Há informação conhecida só depois da avaliação? E se ela entrasse?

**Resposta:** Sim: `quality` é a nota dada depois da avaliação sensorial. Ela é o alvo (`y`) e não entra nas entradas (`X`). Se entrasse, o modelo veria a resposta durante o treino e os resultados pareceriam bons por vazamento. Escala e codificação também são ajustadas só com o treino de cada dobra.

**No notebook:** seção 2, criação de `X` e `y`; seção 3, pipeline de preparação.

## 10. O que perdemos ao escolher um modelo mais complexo?

**Resposta:** A floresta foi mais precisa na validação que a regressão linear (MAE 0,531 contra 0,565), mas é mais difícil de explicar e custa mais para treinar. Uma regressão linear tem coeficientes; uma árvore rasa tem caminhos. A floresta combina 350 árvores, então usamos a importância por permutação para resumir quais entradas ajudam na previsão.

**No notebook:** seções 4 e 5 (modelos e comparação) e 6 (importância).

## 11. Outra divisão treino/teste mudaria muito o resultado?

**Resposta:** Pode mudar; uma única divisão não diz exatamente quanto. Nas cinco dobras do desenvolvimento, o MAE da floresta variou de 0,521 a 0,547. O teste deu 0,529, dentro dessa faixa. Para medir melhor a variação, repetiríamos a avaliação com outras divisões e novos dados.

**No notebook:** seção 5, colunas de melhor e pior dobra e MAE do teste.

## 12. Para que este modelo não deve ser usado? Por quê?

**Resposta:** Não deve aprovar lotes, definir preço, certificar segurança ou orientar mudanças químicas. A base não tem safra, produtor, variedade nem condições de armazenamento, e os erros aumentam em notas extremas. Mesmo com bom resultado neste teste, outro contexto exigiria nova validação.

**No notebook:** seção 8, uso, limitações e restrições; seção 6, erros por nota.

## 13. Quais modelos testamos e como escolhemos sem usar o teste?

**Resposta:** Testamos mediana (MAE 0,643), regressão linear (0,565), k-NN (0,550), árvore (0,582) e floresta (0,531) nas mesmas cinco dobras do desenvolvimento. Escolhemos a floresta porque teve o menor MAE médio. Entre 100 e 350 árvores, o MAE caiu de 0,533 para 0,531; a melhora foi pequena, mas 350 foi a melhor configuração testada. Só depois avaliamos o modelo no teste reservado.

**No notebook:** seção 4 (ajuste de parâmetros), seção 5 (comparação e escolha) e avaliação final.

## Se vier uma pergunta de continuação sobre o tipo de vinho

As medidas químicas quase identificam se o vinho é tinto ou branco (AUC 0,996 no desenvolvimento). Tirar `wine_type` quase não mudou o MAE médio da floresta: 0,531 com a coluna e 0,531 sem ela, diferença inferior a 0,001. Isso não prova que a coluna seja inútil, pois a informação pode estar repetida nas outras medidas. No teste, o MAE foi 0,453 para tintos (267 casos) e 0,554 para brancos (797 casos); é uma diferença descritiva que precisa de nova validação.

**No notebook:** seção 7, auditoria de variáveis, proxies e diferenças entre tipos.
