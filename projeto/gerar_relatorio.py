"""Gera o relatório vetorial (até cinco páginas) a partir do notebook executado.

Execute após o notebook, a partir da raiz do repositório ou da pasta projeto:
    python projeto/gerar_relatorio.py
"""

from __future__ import annotations

import json
from pathlib import Path
from textwrap import fill

import matplotlib

matplotlib.use("pdf")
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
import numpy as np
import pandas as pd
import seaborn as sns


PROJETO = Path(__file__).resolve().parent
RESULTADOS = PROJETO / "resultados"
DESTINO = PROJETO / "relatorio_qualidade_vinhos.pdf"

resumo = json.loads((RESULTADOS / "resumo_metricas.json").read_text(encoding="utf-8"))
comparacao = pd.read_csv(RESULTADOS / "comparacao_validacao.csv")
teste = pd.read_csv(RESULTADOS / "comparacao_teste.csv")
arvore = pd.read_csv(RESULTADOS / "curva_arvore.csv")
cortes = pd.read_csv(RESULTADOS / "curva_corte.csv")
erros_nota = pd.read_csv(RESULTADOS / "erros_por_nota.csv")
erros_tipo = pd.read_csv(RESULTADOS / "erros_por_tipo.csv")
importancia = pd.read_csv(RESULTADOS / "importancia_permutacao.csv")

dados = pd.concat(
    [
        pd.read_csv(PROJETO / "dados" / "winequality-red.csv", sep=";").assign(wine_type="red"),
        pd.read_csv(PROJETO / "dados" / "winequality-white.csv", sep=";").assign(wine_type="white"),
    ],
    ignore_index=True,
)

NAVY = "#17344A"
TEAL = "#427C78"
RUST = "#AE6854"
INK = "#24333E"
MUTED = "#61717B"
LIGHT = "#EEF3F2"
LINE = "#D7E0E1"

sns.set_theme(style="whitegrid", context="paper", palette="colorblind")
plt.rcParams.update(
    {
        "font.family": "DejaVu Sans",
        "font.size": 9,
        "axes.titlesize": 10,
        "axes.labelsize": 8,
        "axes.edgecolor": LINE,
        "grid.color": LINE,
        "grid.alpha": 0.55,
        "pdf.fonttype": 42,
        "savefig.facecolor": "white",
    }
)


def pagina(numero: int, titulo: str, subtitulo: str = ""):
    fig = plt.figure(figsize=(8.27, 11.69), facecolor="white")
    fig.text(0.08, 0.963, "IASEG  /  APRENDIZADO DE MÁQUINA", size=7.5, color=TEAL, weight="bold")
    fig.text(0.08, 0.925, titulo, size=19, color=NAVY, weight="bold")
    if subtitulo:
        fig.text(0.08, 0.900, subtitulo, size=8.6, color=MUTED)
    fig.add_artist(plt.Line2D([0.08, 0.92], [0.883, 0.883], transform=fig.transFigure, color=LINE, lw=0.8))
    fig.add_artist(plt.Line2D([0.08, 0.92], [0.060, 0.060], transform=fig.transFigure, color=LINE, lw=0.7))
    fig.text(0.08, 0.038, "Qualidade de vinhos  •  Projeto da Disciplina 2", size=7, color=MUTED)
    fig.text(0.92, 0.038, f"{numero} / 4", size=7, color=MUTED, ha="right")
    return fig


def cabecalho(fig, y, numero, titulo):
    fig.text(0.08, y, numero, size=10.5, color=TEAL, weight="bold")
    fig.text(0.116, y, titulo, size=11, color=NAVY, weight="bold")


def paragrafo(fig, x, y, texto, largura=104, tamanho=8.6, altura=1.48, cor=INK):
    texto = fill(texto, width=largura, break_long_words=False, break_on_hyphens=False)
    fig.text(x, y, texto, size=tamanho, color=cor, va="top", linespacing=altura)


def tabela(fig, bbox, colunas, linhas, larguras=None, tamanho=8):
    ax = fig.add_axes(bbox)
    ax.axis("off")
    tb = ax.table(
        cellText=linhas,
        colLabels=colunas,
        colWidths=larguras,
        loc="center",
        cellLoc="left",
        colLoc="left",
        bbox=[0, 0, 1, 1],
    )
    tb.auto_set_font_size(False)
    tb.set_fontsize(tamanho)
    for (r, c), cell in tb.get_celld().items():
        cell.set_edgecolor(LINE)
        cell.set_linewidth(0.55)
        cell.PAD = 0.09
        if r == 0:
            cell.set_facecolor(NAVY)
            cell.set_text_props(color="white", weight="bold")
        elif r % 2 == 0:
            cell.set_facecolor("#F4F7F7")
        else:
            cell.set_facecolor("white")
    return ax


def titulo_grafico(ax, titulo):
    ax.set_title(titulo, loc="left", weight="bold", color=NAVY, pad=8)
    ax.tick_params(labelsize=7.5)
    ax.spines[["top", "right"]].set_visible(False)


with PdfPages(DESTINO, metadata={"Title": "Qualidade de vinhos | Relatório do projeto"}) as pdf:
    # Página 1 — tarefa e dados.
    fig = pagina(1, "Qualidade de vinhos", "Relatório do projeto • Regressão para apoio à degustação")
    metricas = [
        ("6.497", "amostras originais"),
        ("5.320", "após duplicatas"),
        (f"{resumo['mae_teste_modelo']:.3f}", "MAE no teste"),
        (f"{100 * resumo['reducao_mae_referencia']:.1f}%", "redução do MAE"),
    ]
    for i, (valor, rotulo) in enumerate(metricas):
        x = 0.08 + i * 0.215
        fig.add_artist(
            plt.Rectangle((x, 0.805), 0.195, 0.062, transform=fig.transFigure, color=LIGHT, ec="none")
        )
        fig.text(x + 0.014, 0.835, valor, size=16, color=NAVY, weight="bold", va="center")
        fig.text(x + 0.014, 0.811, rotulo, size=7, color=MUTED)
    cabecalho(fig, 0.765, "1", "Objetivo da modelagem")
    paragrafo(
        fig, 0.08, 0.741,
        "Pergunta: qual nota sensorial (quality) uma amostra receberia a partir de 11 medidas físico-químicas e do tipo tinto ou branco? O modelo devolve uma nota numérica, como 6,3. A tarefa é regressão. A saída ajuda a ordenar amostras para uma segunda degustação; a avaliação final continua humana.",
    )
    cabecalho(fig, 0.660, "2", "Dados utilizados")
    paragrafo(
        fig, 0.08, 0.635,
        "Fonte: UCI Wine Quality, arquivos winequality-red.csv e winequality-white.csv. Cada linha representa uma amostra. Acrescentamos wine_type antes da união. A auditoria verificou ausências, valores não finitos, duplicatas completas e perfis idênticos com notas conflitantes.",
    )
    tabela(
        fig, [0.08, 0.451, 0.84, 0.105],
        ["Etapa", "Linhas", "Decisão"],
        [
            ["Arquivos originais", "6.497", "11 medidas, tipo e nota"],
            ["Após limpeza", "5.320", "1.177 duplicatas completas removidas"],
            ["Desenvolvimento", "4.256", "seleção, ajuste e corte"],
            ["Teste final", "1.064", "avaliação depois das escolhas"],
        ],
        [0.30, 0.14, 0.56],
        7.8,
    )
    distribuicao = dados["quality"].value_counts().sort_index()
    ax = fig.add_axes([0.12, 0.145, 0.45, 0.245])
    sns.barplot(x=distribuicao.index.astype(str), y=distribuicao.values, color=TEAL, ax=ax)
    titulo_grafico(ax, "Distribuição das notas originais")
    ax.set(xlabel="Nota", ylabel="Amostras")
    ax2 = fig.add_axes([0.63, 0.16, 0.27, 0.20])
    ax2.axis("off")
    ax2.text(0, 1, "Auditoria", transform=ax2.transAxes, size=10, weight="bold", color=NAVY, va="top")
    ax2.text(
        0, 0.82,
        "Sem ausências ou valores\nnão finitos.\n\n"
        "Notas observadas: 3 a 9.\n"
        "76,6% são notas 5 ou 6.\n\n"
        "Sem identificador, uma\n"
        "repetição pode ser legítima.",
        transform=ax2.transAxes, size=8.5, color=INK, va="top", linespacing=1.5,
    )
    pdf.savefig(fig)
    plt.close(fig)

    # Página 2 — método, comparação e curva de sobreajuste.
    fig = pagina(
        2, "Desempenho e comparação",
        f"Escolha antes do teste: {resumo['modelo_escolhido'].lower()} com {resumo['n_arvores_escolhido']} árvores",
    )
    cabecalho(fig, 0.849, "3", "Métrica e desenho da avaliação")
    paragrafo(
        fig, 0.08, 0.826,
        "Reservamos 20% com estratificação por nota e semente 42. Nos 80% de desenvolvimento, todos os modelos usaram as mesmas cinco dobras embaralhadas. MAE, em pontos de nota, foi a métrica principal; RMSE e R² complementam. Codificação e escala são ajustadas dentro de cada dobra.",
    )
    ordem = ["Referência (mediana)", "Regressão linear", "k-NN", "Árvore", "Floresta aleatória"]
    cv = comparacao.set_index("modelo")
    te = teste.set_index("modelo")
    linhas = []
    for nome in ordem:
        r, t = cv.loc[nome], te.loc[nome]
        linhas.append(
            [
                nome,
                f"{r['MAE VC']:.3f}",
                f"{r['melhor dobra']:.3f}–{r['pior dobra']:.3f}",
                f"{t['MAE teste']:.3f}",
                f"{t['R² teste']:.3f}",
            ]
        )
    tabela(
        fig, [0.08, 0.604, 0.84, 0.155],
        ["Modelo", "MAE VC", "Faixa VC", "MAE teste", "R² teste"],
        linhas,
        [0.34, 0.13, 0.19, 0.18, 0.16],
        7.4,
    )
    ax = fig.add_axes([0.26, 0.380, 0.61, 0.178])
    grafico = comparacao.sort_values("MAE VC", ascending=False)
    sns.barplot(data=grafico, y="modelo", x="MAE VC", color=TEAL, ax=ax)
    titulo_grafico(ax, "MAE médio na validação cruzada")
    ax.set(xlabel="Pontos de nota (menor é melhor)", ylabel="")
    ax.set_xlim(0, max(grafico["MAE VC"]) * 1.12)
    for p in ax.patches:
        ax.text(p.get_width() + 0.006, p.get_y() + p.get_height() / 2, f"{p.get_width():.3f}",
                va="center", size=7, color=INK)
    ax2 = fig.add_axes([0.16, 0.111, 0.72, 0.170])
    sns.lineplot(data=arvore, x="profundidade", y="MAE treino", marker="o", label="Treino", color=RUST, ax=ax2)
    sns.lineplot(data=arvore, x="profundidade", y="MAE VC", marker="o", label="Validação", color=TEAL, ax=ax2)
    ax2.axvline(resumo["profundidade_arvore"], color=NAVY, ls="--", lw=0.9)
    titulo_grafico(ax2, f"Árvore: profundidade {resumo['profundidade_arvore']} minimiza o MAE de validação")
    ax2.set(xlabel="Profundidade máxima", ylabel="MAE")
    ax2.legend(loc="lower left", fontsize=7, frameon=False)
    pdf.savefig(fig)
    plt.close(fig)

    # Página 3 — uso operacional e escolha do corte.
    fig = pagina(3, "Uso pretendido", "Uma fila de degustação, não uma decisão automática")
    cabecalho(fig, 0.849, "4", "Decisão apoiada pela previsão")
    paragrafo(
        fig, 0.08, 0.823,
        "Definimos como caso de interesse uma nota real de pelo menos 7. Com previsões fora da dobra no desenvolvimento, escolhemos o maior corte em décimos que manteve sensibilidade mínima de 75%: 6,0. Amostras com previsão nesse valor ou acima seguem primeiro para degustação humana.",
    )
    ax = fig.add_axes([0.16, 0.435, 0.70, 0.295])
    sns.lineplot(data=cortes, x="corte", y="sensibilidade", color=TEAL, label="Sensibilidade", ax=ax)
    sns.lineplot(data=cortes, x="corte", y="precisão", color=RUST, label="Precisão", ax=ax)
    ax.axvline(resumo["corte"], color=NAVY, lw=1, ls="--", label=f"Corte {resumo['corte']:.1f}")
    ax.axhline(0.75, color=MUTED, lw=0.8, ls=":")
    titulo_grafico(ax, "Escolha do corte no desenvolvimento")
    ax.set(xlabel="Nota prevista", ylabel="Proporção", ylim=(0, 1.03))
    ax.legend(loc="center left", fontsize=7.5, frameon=False)
    tabela(
        fig, [0.08, 0.229, 0.84, 0.151],
        ["Métrica no teste", "Resultado", "Interpretação"],
        [
            ["Sensibilidade", f"{100 * resumo['triagem_sensibilidade']:.1f}%",
             f"{resumo['triagem_bons_recuperados']} de {resumo['triagem_bons_total']} vinhos 7+ recuperados"],
            ["Precisão", f"{100 * resumo['triagem_precisão']:.1f}%",
             "aproximadamente 45 em 100 selecionados são 7+"],
            ["F1", f"{resumo['triagem_F1']:.3f}", "equilíbrio das duas medidas"],
            ["Volume", f"{resumo['triagem_selecionados']} de {resumo['triagem_total']}",
             "34,7% das amostras seguem primeiro"],
        ],
        [0.24, 0.16, 0.60],
        7.6,
    )
    paragrafo(
        fig, 0.08, 0.188,
        "A política favorece não perder bons candidatos. No teste, 37 vinhos 7+ ficaram fora da prioridade e 204 selecionados não eram 7+. Se a capacidade do painel mudar, um novo corte precisa de validação em novos dados; o teste atual não serve para recalibrar esta avaliação.",
        largura=107, tamanho=8.4,
    )
    pdf.savefig(fig)
    plt.close(fig)

    # Página 4 — limites, interpretação, restrições e fontes.
    fig = pagina(4, "Limitações e restrições", "O que o desempenho permite afirmar")
    cabecalho(fig, 0.849, "5", "Onde o modelo erra")
    paragrafo(
        fig, 0.08, 0.825,
        "A previsão tende ao centro da distribuição e erra mais nas notas extremas. Os grupos de nota 3 e 9 têm apenas 6 e 1 casos no teste; suas médias não são estáveis. Também há diferença entre vinhos tintos e brancos, que exige acompanhamento em novos dados.",
    )
    ax = fig.add_axes([0.13, 0.585, 0.39, 0.162])
    sns.barplot(data=erros_nota, x="nota_real", y="MAE", color=TEAL, ax=ax)
    titulo_grafico(ax, "MAE por nota no teste")
    ax.set(xlabel="Nota real", ylabel="MAE")
    ax2 = fig.add_axes([0.66, 0.585, 0.25, 0.162])
    sns.barplot(data=erros_tipo, x="wine_type", y="MAE", color=RUST, ax=ax2)
    titulo_grafico(ax2, "MAE por tipo")
    ax2.set(xlabel="", ylabel="")
    ax2.set_xticks([0, 1], ["Tinto", "Branco"])
    for a, df in [(ax, erros_nota), (ax2, erros_tipo)]:
        for patch, n in zip(a.patches, df["n"]):
            a.annotate(f"n={int(n)}", (patch.get_x() + patch.get_width() / 2, patch.get_height()),
                       ha="center", va="bottom", xytext=(0, 2), textcoords="offset points", size=6.2)
    ax3 = fig.add_axes([0.28, 0.385, 0.62, 0.138])
    top = importancia.head(5).sort_values("aumento_MAE")
    ax3.barh(top["variavel"], top["aumento_MAE"], color=TEAL)
    titulo_grafico(ax3, "Importância por permutação: aumento do MAE")
    ax3.set(xlabel="", ylabel="")
    fig.text(
        0.08, 0.352,
        "Associação preditiva não demonstra que alterar a química causará uma nota diferente.",
        size=8.1, color=MUTED,
    )
    cabecalho(fig, 0.318, "6", "Restrições de uso")
    paragrafo(
        fig, 0.08, 0.294,
        "Não usar para aprovar ou rejeitar lotes automaticamente, substituir degustadores, certificar segurança, estimar preço ou orientar intervenções químicas. A base não informa safra, produtor, uva, armazenamento ou identificador. Aplicações em outras regiões, variedades, períodos ou laboratórios exigem validação externa e monitoramento.",
        largura=106, tamanho=8.3,
    )
    fig.text(0.08, 0.213, "Reprodução e responsabilidades", size=9.4, color=NAVY, weight="bold")
    paragrafo(
        fig, 0.08, 0.197,
        "Os CSVs locais, a semente 42 e as mesmas cinco dobras permitem repetir a análise. O alvo fica fora das entradas; duplicatas saem antes da divisão; modelo e corte são fixados antes do teste.",
        largura=110, tamanho=7.5,
    )
    fig.text(
        0.08, 0.148,
        "Seções: Daniel Gil (1 e 6); Bruno Pimentel (2); Bruno Groppo (3);",
        size=7.4, color=INK,
    )
    fig.text(
        0.08, 0.135,
        "Wallace Jardim (4); Reynato Junior (5).",
        size=7.4, color=INK,
    )
    fig.text(0.08, 0.112, "Fontes", size=8.5, color=NAVY, weight="bold")
    fig.text(
        0.08, 0.095,
        "Cortez et al. (2009), Modeling wine preferences by data mining from physicochemical properties.\n"
        "UCI Machine Learning Repository, Wine Quality, DOI 10.24432/C56S3T.\n"
        "IASEG, Projeto da Disciplina 2 e Banco de Perguntas (2026).",
        size=7.0, color=MUTED, va="top", linespacing=1.3,
    )
    pdf.savefig(fig)
    plt.close(fig)

print(f"Relatório vetorial gerado: {DESTINO}")
