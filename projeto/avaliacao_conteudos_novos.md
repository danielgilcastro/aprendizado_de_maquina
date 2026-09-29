# Avaliação dos conteúdos novos e adaptações do projeto

Revisão realizada em 29/09/2026 com base nas datas do sistema de arquivos, nos metadados internos dos PDFs e no conteúdo dos notebooks.

## Ordem dos materiais relevantes

| Arquivo ou conjunto | Criação no sistema | Última modificação | Metadado interno ou observação | Consequência para o projeto |
| --- | --- | --- | --- | --- |
| `Projeto_disciplina.pdf` | 22/09/2026 10:44 | 22/09/2026 10:44 | enunciado original | define notebook, relatório de até 5 páginas e seis seções |
| `Projeto_disciplina_gabarito_qualidade_vinhos.pdf` | 22/09/2026 14:27 | 22/09/2026 14:27 | criado em 22/09 | fornece uma resposta modelo e parâmetros de referência |
| `passo_1_qualidade_vinhos.ipynb` | 22/09/2026 15:02 | 23/09/2026 09:29 | anterior às Aulas 4 e 5 | respostas foram preenchidas e todas as células reexecutadas |
| `passo_2_qualidade_vinhos.ipynb` | 23/09/2026 09:27 | 24/09/2026 09:50 | anterior à Aula 5 | respostas foram preenchidas; a instalação dentro do notebook foi removida; todas as células foram reexecutadas |
| materiais da Aula 4 | 24–25/09/2026 | 24–25/09/2026 | árvores, sobreajuste e subajuste | acrescentamos curva de MAE de treino e validação para profundidades de 1 a 18 |
| `Banco_de_Perguntas.pdf` | 29/09/2026 12:38 | 29/09/2026 12:38 | PDF criado internamente em 28/09/2026 21:41 | acrescentamos respostas para 13 perguntas e confirmamos apresentação em 05/10, das 9h às 11h |
| `aula5/note.ipynb` | 29/09/2026 09:18 | 29/09/2026 12:29 | conteúdo da Aula 5 | acrescentamos validação cruzada, floresta, comparação sem teste e caça a vazamento |
| `aula5/1_aula5.pdf` | 29/09/2026 13:26 | 29/09/2026 13:26 | PDF criado internamente em 28/09/2026 21:41 | confirma o mesmo fluxo metodológico do notebook da aula |

As datas de criação do Windows podem mudar quando um arquivo é copiado ou sincronizado. Por isso, a avaliação usou também `LastWriteTime`, metadados dos PDFs e o conteúdo. A Aula 5 e o banco de perguntas são inequivocamente posteriores aos notebooks iniciais e exigiam a atualização.

## Avaliação do material anterior

Os passos 1 e 2 tinham uma base metodológica correta: alvo separado, duplicatas discutidas, teste reservado e transformações dentro de pipeline. Eles ainda não constituíam a entrega final pelos seguintes motivos:

- as respostas do grupo estavam em branco;
- o passo 1 tinha células sem contagem de execução;
- o passo 2 instalava `jinja2` durante a execução;
- não havia referência, validação cruzada, curva de árvore, floresta ou comparação final;
- não havia escolha de corte com previsões fora da dobra;
- não havia análise final por nota e tipo;
- o banco de perguntas ainda não estava incorporado;
- relatório e apresentação não estavam preparados.

## Adaptações concluídas

1. Os notebooks dos passos 1 e 2 foram preenchidos e executados sem erros.
2. `projeto_qualidade_vinhos_completo.ipynb` passou a reunir o fluxo de ponta a ponta.
3. A base original de 6.497 linhas foi reduzida a 5.320 após a remoção declarada de 1.177 duplicatas completas.
4. O teste final preserva 1.064 linhas. As 4.256 restantes formam o desenvolvimento.
5. Todos os modelos usam as mesmas cinco dobras de `KFold` com embaralhamento e `random_state=42`.
6. A profundidade 5 foi escolhida pela validação da árvore. A curva mostra sobreajuste após o mínimo de validação.
7. Foram comparados referência, regressão linear, k-NN, árvore e floresta.
8. A floresta de 350 árvores com `max_features=0.7` foi escolhida antes do teste.
9. No teste, a floresta obteve MAE 0,529, RMSE 0,684 e R² 0,396. O MAE da referência foi 0,643, uma redução relativa de 17,7%.
10. O corte 6,0 foi definido com previsões fora da dobra. No teste, a regra alcançou sensibilidade de 81,7% e precisão de 44,7%.
11. Foram registradas limitações, restrições, importância por permutação e erro por nota e por tipo.
12. O roteiro, o relatório, a apresentação e as respostas da banca foram alinhados aos números efetivamente executados.

## Verificações

- Os três notebooks foram executados do início ao fim e não contêm saídas de erro.
- Os resultados numéricos foram salvos em `resultados/` para uso no relatório e na apresentação.
- O teste final só aparece depois de o notebook registrar o modelo e o corte escolhidos.
- `quality` não aparece nas entradas; duplicatas saem antes da divisão; preparação e ajuste acontecem dentro de cada dobra.
- Diferenças pequenas em relação ao PDF gabarito resultam da execução atual e das versões atuais das bibliotecas. O projeto usa seus próprios números, como pede o gabarito.
