# Projeto: Qualidade de vinhos

Este roteiro segue as seis seções do enunciado `Projeto_disciplina.pdf`. A proposta é avançar por etapas, registrando o que foi feito e o motivo de cada escolha.

**Escolha adotada:** regressão, para prever a nota `quality`. O modelo recebe medições físico-químicas e o tipo do vinho e devolve um número, como 6,3. Essa escolha é consistente com o gabarito preparado para o grupo.

## Atualização com os conteúdos novos

Esta versão foi revisada em **29/09/2026**. A ordem dos arquivos mostra que os notebooks iniciais foram produzidos antes das Aulas 4 e 5 e antes do banco de perguntas:

| Conteúdo | Data do arquivo | Adaptação aplicada |
| --- | --- | --- |
| notebooks intermediários dos passos 1 e 2 | criados entre 22 e 23/09 | revisados e depois consolidados no notebook final; as cópias intermediárias foram removidas da entrega |
| materiais da Aula 4 | 24–25/09 | curva de complexidade com treino e validação cruzada; diagnóstico de sobreajuste |
| `aula5/note.ipynb` e `aula5/1_aula5.pdf` | 29/09 | validação cruzada, floresta aleatória, comparação antes do teste e auditoria de vazamento |
| `Banco_de_Perguntas.pdf` | 29/09; metadados internos de 28/09 | respostas para as 13 perguntas e preparação para apresentação em 05/10, das 9h às 11h |

O arquivo principal agora é [projeto_qualidade_vinhos_completo.ipynb](projeto_qualidade_vinhos_completo.ipynb). Ele substitui os dois notebooks intermediários, contém todos os passos, salva resultados reproduzíveis em `resultados/` e deve ser a fonte dos números do relatório e da apresentação.

### Entregas preparadas

- `projeto_qualidade_vinhos_completo.ipynb`: notebook final, executado do início ao fim.
- `relatorio_qualidade_vinhos.docx` e `relatorio_qualidade_vinhos.pdf`: relatório final de até 5 páginas.
- `apresentacao_qualidade_vinhos.pptx`: apresentação de aproximadamente 5 minutos.
- `respostas_banca.md`: respostas curtas e evidências para as 13 perguntas.
- `avaliacao_conteudos_novos.md`: registro das datas, mudanças e verificações.

## Como começar

1. Abra a pasta do repositório no VS Code ou no Jupyter.
2. Selecione o ambiente Python `.venv` do projeto. Se estiver em outro computador, instale as dependências da raiz com `pip install -r requirements.txt`.
3. Abra [projeto_qualidade_vinhos_completo.ipynb](projeto_qualidade_vinhos_completo.ipynb), que reúne a construção, a revisão e a entrega final.
4. Execute as células de cima para baixo com `Shift + Enter`.
5. Leia as saídas e confira as respostas já preenchidas. Altere apenas se o grupo tomar uma decisão diferente e, nesse caso, reexecute o notebook completo e atualize relatório e apresentação.

Para reexecutar a entrega final sem abrir a interface:

```powershell
.\.venv\Scripts\jupyter-nbconvert.exe --to notebook --execute --inplace --ExecutePreprocessor.timeout=1200 projeto/projeto_qualidade_vinhos_completo.ipynb
```

Na primeira execução, o notebook baixa os dois CSVs públicos indicados no enunciado e guarda cópias em `projeto/dados/`. As execuções seguintes usam essas cópias e funcionam sem internet. O notebook pode ser executado com a pasta de trabalho na raiz do repositório ou em `projeto/`.

## Passo 1 — Definir o problema e conhecer os dados

**Arquivo desta etapa:** seção correspondente de [projeto_qualidade_vinhos_completo.ipynb](projeto_qualidade_vinhos_completo.ipynb).

**Ajuda a escrever:** seções 1 e 2 do relatório.

### O que fazer

1. Escrever a pergunta que o grupo quer responder.
2. Carregar `winequality-red.csv` e `winequality-white.csv` com `sep=";"`.
3. Acrescentar `wine_type` para identificar tinto e branco e juntar as tabelas.
4. Conferir linhas, colunas, tipos e exemplos.
5. Procurar ausências, valores não numéricos e linhas repetidas.
6. Consultar `describe()` e `value_counts()` para entender medidas e notas.
7. Separar conceitualmente as entradas (`X`) e a resposta desejada (`y`).
8. Registrar o que chamou atenção e preencher as respostas finais.

### O que vocês devem entender ao terminar

- Cada linha representa uma amostra de vinho.
- Cada arquivo original tem 12 colunas: 11 medidas e a nota.
- Juntos, os arquivos têm 6.497 linhas. Com `wine_type`, a tabela passa a ter 13 colunas.
- `quality` é o alvo. Ele não pode entrar em `X`.
- A escala documentada é 0–10; nestes arquivos, as notas observadas vão de 3 a 9.
- Não há células ausentes nos arquivos consultados, mas há 1.177 repetições além da primeira ocorrência de cada linha idêntica.
- A distribuição das notas é desigual, com concentração em 5 e 6.

Esses números são referências para conferir a leitura. As saídas do notebook mostram o que foi encontrado nos arquivos efetivamente carregados.

**Entrega do passo:** notebook executado e respostas escritas sobre objetivo, origem, alvo, entradas e problemas encontrados.

Neste primeiro passo, os dados originais são mantidos: a limpeza e o treinamento ficam para a próxima etapa.

## Passo 2 — Preparar os dados e ajustar a primeira regressão

**Arquivo desta etapa:** seção correspondente de [projeto_qualidade_vinhos_completo.ipynb](projeto_qualidade_vinhos_completo.ipynb).

**Ajuda a escrever:** seções 1 e 2; primeiro resultado para a seção 3.

**Corresponde à tarefa da Aula 2:** completar a auditoria e ajustar uma reta em uma coluna numérica. Aqui, essa coluna é o próprio alvo `quality`.

1. Criar uma cópia da base para tratamento.
2. Definir o tratamento das duplicatas. Para reproduzir a opção do gabarito, remover linhas integralmente idênticas com `drop_duplicates()`: devem restar 5.320 linhas.
3. Justificar a decisão: repetições podem inflar a avaliação se aparecerem nos dois lados da divisão. Sem identificador de amostra, não sabemos se todas são erros.
4. Investigar também linhas com entradas iguais e notas diferentes. Remover duplicatas completas não elimina esses casos. Se for necessário impedir que perfis idênticos se espalhem entre partições, usar uma divisão por grupos de entradas.
5. Definir `X = base.drop(columns="quality")` e `y = base["quality"]`.
6. Reservar aproximadamente 20% dos dados para teste final, com semente fixa (`random_state=42`). Se usar divisão aleatória por linha, preservar a distribuição das notas com `stratify=y`.
7. Dentro dos 80% de desenvolvimento, reservar 25% para validação interna, também com semente 42 e estratificação. Isso deixa 60% da base limpa para ajuste, 20% para validação e 20% para teste final.
8. Codificar `wine_type` e padronizar as medidas em um `Pipeline`. As transformações devem ser aprendidas somente nos dados de ajuste.
9. Ajustar uma `LinearRegression`, gerar previsões na validação e interpretar o MAE em pontos de nota.
10. Examinar os coeficientes e discutir três variáveis em que o modelo se apoia. Em variáveis padronizadas, o coeficiente numérico expressa a mudança prevista para um desvio-padrão da entrada, mantendo as demais fixas. Conferir uma previsão pela soma das contribuições e do intercepto.

**Entrega do passo:** limpeza justificada, divisão documentada e primeira regressão funcionando.

Guarde o teste final. Ele será utilizado no passo 5, após escolher o modelo no treino.

O notebook completo inclui tabelas, gráficos, respostas do grupo e checklist. Ele mantém os CSVs originais e apresenta os resultados em suas próprias saídas. Nas etapas seguintes, reproduz a mesma limpeza e divisão inicial para manter o teste reservado; a validação cruzada é aplicada somente aos dados de desenvolvimento.

## Passo 3 — Criar uma referência e escolher como medir o erro

**Ajuda a escrever:** seção 3 do relatório.

**Relaciona-se à Aula 3.**

1. Ajustar um `DummyRegressor(strategy="median")` usando somente o treino.
2. Entender a referência: ela prevê a mesma nota para todos os vinhos, a mediana do treino.
3. Adotar MAE como métrica principal: a média de `abs(nota real - nota prevista)`, em pontos de nota.
4. Comparar referência e regressão linear nas mesmas dobras de validação cruzada do treino.
5. Registrar RMSE e R² como informações complementares, explicando o que medem.

**Exemplo de leitura:** se as notas reais forem 5, 6 e 7 e as previsões forem 5,5; 5,5; 6,0, os erros absolutos são 0,5; 0,5; 1,0. O MAE é aproximadamente 0,67 ponto.

**Resultado executado:** a referência teve MAE de teste 0,643 e a regressão linear 0,566. A regressão reduz o erro, mas a comparação final ainda inclui k-NN, árvore e floresta.

**Entrega do passo:** tabela comparativa e um parágrafo explicando se a regressão melhora a referência.

O MAE não é porcentagem de acertos e não é o erro máximo de uma previsão individual.

## Passo 4 — Ajustar uma árvore e reconhecer sobreajuste

**Ajuda a escrever:** seções 3 e 5 do relatório.

**Relaciona-se à Aula 4.**

1. Ajustar árvores com diferentes profundidades usando o mesmo treino.
2. Medir MAE de treino e de validação cruzada para cada profundidade.
3. Construir o gráfico com profundidade no eixo horizontal e MAE no vertical.
4. Interpretar: erro alto nos dois conjuntos sugere subajuste; treino melhora enquanto validação piora sugere sobreajuste.
5. Escolher profundidade e demais parâmetros pela validação do treino.

Na execução de 29/09, a profundidade 5 apresentou o menor MAE médio entre as profundidades testadas com `KFold` embaralhado e `random_state=42`. A partir daí, o MAE de treino continuou caindo enquanto o MAE de validação subiu.

**Entrega do passo:** gráfico e justificativa da complexidade escolhida.

O enunciado fala em curva “treino × teste”. Para escolher a profundidade, use os conjuntos de validação das dobras como teste de cada ajuste e identifique a curva como “validação cruzada”. Assim, o teste final continua reservado.

## Passo 5 — Comparar modelos e avaliar no teste final

**Ajuda a escrever:** seções 3 e 5 do relatório.

**Relaciona-se à Aula 5.**

1. Comparar regressão linear, árvore, k-NN e floresta aleatória com as mesmas dobras de validação.
2. Ajustar hiperparâmetros exclusivamente no treino. Para k-NN, a padronização é especialmente importante.
3. Checar vazamento: alvo nas entradas, cópias da mesma amostra entre partições, transformações ajustadas na base inteira e escolhas feitas olhando o teste.
4. Escolher o modelo pelo resultado da validação, considerando a simplicidade e o desempenho.
5. Definir também a regra de decisão do passo 6 antes de consultar o teste.
6. Treinar o modelo escolhido com todo o conjunto de treino.
7. Avaliar uma vez no teste final e registrar MAE, RMSE, R² e desempenho da referência.
8. Analisar erros por nota e por tipo de vinho, sempre informando o número de casos de cada grupo.
9. Se investigar importância de variáveis, explicar que associação preditiva não demonstra causa.

**Resultado executado:** a floresta aleatória com 350 árvores e `max_features=0.7` foi escolhida antes do teste. No teste final, obteve MAE 0,529, RMSE 0,684 e R² 0,396. A referência teve MAE 0,643; a redução relativa do MAE foi 17,7%. O teste não foi usado para rever a escolha.

**Entrega do passo:** modelo escolhido, comparação com referência e análise das falhas.

Se o teste motivar novas escolhas de modelo ou corte, ele deixa de ser uma avaliação final independente. Será necessário outro conjunto reservado para confirmar essas mudanças.

## Passo 6 — Explicar o uso, o corte e as restrições

**Ajuda a escrever:** seções 4, 5 e 6 do relatório.

**O uso começa a ser discutido na Aula 3 e é concluído ao longo do projeto.**

1. Propor uma decisão concreta, por exemplo, priorizar amostras para degustação humana.
2. Se houver triagem de candidatos a nota 7 ou mais, distinguir:
   - condição real de interesse: `quality >= 7`;
   - regra aplicada pelo sistema: `nota_prevista >= corte`.
3. Escolher o corte usando apenas validação do treino e justificar os custos de deixar bons candidatos passar ou selecionar candidatos desnecessariamente.
4. Medir precisão e sensibilidade para essa regra de triagem. O modelo continua sendo um regressor; a decisão derivada é binária.
5. Explicar limitações: notas raras, região de origem, informações ausentes e subjetividade da avaliação.
6. Definir restrições: não substituir avaliação humana, não inferir segurança sanitária ou preço e não aplicar a outros contextos sem validação.

**Resultado executado:** o maior corte em décimos que preservou pelo menos 75% de sensibilidade nas previsões fora da dobra foi 6,0. No teste, ele selecionou 369 de 1.064 amostras, recuperou 165 de 202 vinhos com nota real 7 ou maior, teve sensibilidade de 81,7% e precisão de 44,7%.

**Entrega do passo:** decisão descrita, corte justificado e lista objetiva de limitações e restrições.

O corte usado no gabarito é um exemplo de política de triagem. Não o trate como obrigatório nem copie suas métricas se o experimento do grupo for diferente.

## Passo 7 — Montar o relatório e preparar a apresentação

**Relaciona-se à conclusão do projeto e à Aula 7.**

O relatório deve ter **no máximo 5 páginas** e estas seis seções:

| Seção | O que escrever |
| --- | --- |
| 1. Objetivo da modelagem | Pergunta, alvo, tipo de tarefa e saída do modelo. |
| 2. Dados utilizados | Origem, tamanho, variáveis, auditoria e descartes justificados. |
| 3. Desempenho e comparação | Divisão dos dados, métrica, referência, modelos e resultados. |
| 4. Uso pretendido | Decisão apoiada, corte e consequências dos erros. |
| 5. Limitações | Onde o modelo falha e em quais condições o resultado é frágil. |
| 6. Restrições de uso | Decisões e contextos em que o modelo não deve ser aplicado. |

Para o grupo de quatro pessoas:

1. Registrar os responsáveis por cada seção, conforme pedido no enunciado.
2. Reexecutar o notebook completo do início ao fim, sem depender de variáveis criadas fora da sequência.
3. Conferir se os números do relatório correspondem às saídas salvas.
4. Preparar cerca de 5 minutos de apresentação e 10 minutos para perguntas. O banco mais novo informa **05/10, das 9h às 11h**, com cerca de 15 minutos por grupo.
5. Ensaiar a explicação do alvo, do MAE, da referência, do vazamento, do sobreajuste e do corte.

**Entrega final:** notebook com importação, preparação, treinamento e previsões; relatório de até 5 páginas; apresentação curta; respostas para a banca; integrantes preparados para explicar as seções pelas quais respondem.

O enunciado indica entrega em 02/10 e apresentação em 05/10, ambas sujeitas a confirmação do professor.

## Fontes

- Enunciado: `Projeto_disciplina.pdf`, na raiz deste repositório.
- [Wine Quality — UCI Machine Learning Repository](https://doi.org/10.24432/C56S3T).
- [CSV de vinhos tintos indicado no enunciado](https://raw.githubusercontent.com/zygmuntz/wine-quality/master/winequality/winequality-red.csv).
- [CSV de vinhos brancos indicado no enunciado](https://raw.githubusercontent.com/zygmuntz/wine-quality/master/winequality/winequality-white.csv).
