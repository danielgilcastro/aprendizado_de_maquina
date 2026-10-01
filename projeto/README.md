# Projeto: qualidade de vinhos

O notebook estima a nota sensorial de amostras de vinho e avalia uma regra de prioridade para degustação humana. Os dados públicos estão na pasta dados.

## Executar

A partir da raiz do repositório, com as dependências de requirements.txt instaladas:

1. Abra projeto_qualidade_vinhos_completo.ipynb no Jupyter e execute todas as células em ordem.
2. Confira as tabelas na pasta resultados e gere novamente o relatório:

   ~~~powershell
   python projeto/gerar_relatorio.py
   ~~~

Também é possível executar o notebook a partir da pasta projeto. O teste final permanece reservado até a escolha do modelo e do corte. Os gráficos do notebook são gerados por Seaborn e Matplotlib em SVG; o PDF usa gráficos vetoriais, sem arquivos de imagem.

## Entregáveis

- projeto_qualidade_vinhos_completo.ipynb: código, gráficos e resultados executados.
- relatorio_qualidade_vinhos.pdf: relatório em quatro páginas, com as seis seções do enunciado.
- respostas_banca.md: apoio para a apresentação e a divisão das seções.
- gerar_relatorio.py: reprodução do PDF a partir dos resultados do notebook.
