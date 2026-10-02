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
import pandas as pd
import seaborn as sns


PROJETO = Path(__file__).resolve().parent
RESULTADOS = PROJETO / "resultados"
DESTINO = PROJETO / "relatorio_qualidade_vinhos.pdf"

resumo = json.loads((RESULTADOS / "resumo_metricas.json").read_text(encoding="utf-8"))
comparacao = pd.read_csv(RESULTADOS / "comparacao_validacao.csv")
ajustes = pd.read_csv(RESULTADOS / "ajustes_modelos.csv")
teste = pd.read_csv(RESULTADOS / "comparacao_teste.csv")
arvore = pd.read_csv(RESULTADOS / "curva_arvore.csv")
cortes = pd.read_csv(RESULTADOS / "curva_corte.csv")
erros_nota = pd.read_csv(RESULTADOS / "erros_por_nota.csv")
erros_tipo = pd.read_csv(RESULTADOS / "erros_por_tipo.csv")
importancia = pd.read_csv(RESULTADOS / "importancia_permutacao.csv")
pares_correlacionados = pd.read_csv(RESULTADOS / "pares_correlacionados.csv")
desempenho_tipo = pd.read_csv(RESULTADOS / "desempenho_tipo.csv")
mae_100_arvores = float(ajustes.loc[ajustes["parametro"].eq(100), "MAE VC"].iloc[0])

dados = pd.concat(
    [
        pd.read_csv(PROJETO / "dados" / "winequality-red.csv", sep=";").assign(wine_type="red"),
        pd.read_csv(PROJETO / "dados" / "winequality-white.csv", sep=";").assign(wine_type="white"),
    ],
    ignore_index=True,
)
base_limpa = dados.drop_duplicates(keep="first")
exemplo = pd.concat(
    [
        base_limpa.loc[base_limpa["wine_type"].eq("red")].head(4),
        base_limpa.loc[base_limpa["wine_type"].eq("white")].head(4),
    ]
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
    fig.text(0.92, 0.038, f"{numero} / 5", size=7, color=MUTED, ha="right")
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
    fig = pagina(1, "Qualidade de vinhos", "Relatório do projeto • Estudo didático de aprendizado de máquina")
    fig.text(
        0.08, 0.866,
        "Siglas: MAE = erro absoluto médio; RMSE = raiz do erro quadrático médio.",
        size=7.1, color=MUTED,
    )
    fig.text(
        0.08, 0.851,
        "VC = validação cruzada; F1 = média harmônica da precisão e da sensibilidade.",
        size=7.1, color=MUTED,
    )
    metricas = [
        ("6.497", "amostras originais"),
        ("5.320", "após duplicatas"),
        (f"{resumo['mae_teste_modelo']:.3f}", "MAE no teste"),
        (f"{100 * resumo['reducao_mae_referencia']:.1f}%", "redução do MAE"),
    ]
    for i, (valor, rotulo) in enumerate(metricas):
        x = 0.08 + i * 0.215
        fig.add_artist(
            plt.Rectangle((x, 0.774), 0.195, 0.061, transform=fig.transFigure, color=LIGHT, ec="none")
        )
        fig.text(x + 0.014, 0.804, valor, size=16, color=NAVY, weight="bold", va="center")
        fig.text(x + 0.014, 0.780, rotulo, size=7, color=MUTED)
    cabecalho(fig, 0.735, "1", "Objetivo da modelagem")
    paragrafo(
        fig, 0.08, 0.711,
        "Queremos estimar a nota sensorial (quality) com 11 medidas químicas e o tipo do vinho. A saída é um número; por isso, usamos regressão. O estudo mostra a limpeza dos dados, o treino, a comparação dos modelos e seus limites.",
    )
    cabecalho(fig, 0.622, "2", "Dados utilizados")
    paragrafo(
        fig, 0.08, 0.599,
        "Usamos dois CSVs públicos, um de vinhos tintos e outro de brancos. Cada linha tem 11 medidas e uma nota. Acrescentamos wine_type para indicar o tipo.",
        largura=108,
    )
    fig.text(
        0.08, 0.551,
        "Tinto: https://raw.githubusercontent.com/zygmuntz/wine-quality/master/winequality/winequality-red.csv",
        size=6.5, color=TEAL,
    )
    fig.text(
        0.08, 0.537,
        "Branco: https://raw.githubusercontent.com/zygmuntz/wine-quality/master/winequality/winequality-white.csv",
        size=6.5, color=TEAL,
    )
    tabela(
        fig, [0.08, 0.445, 0.84, 0.084],
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
    fig.text(0.08, 0.420, "Exemplo da base limpa: 8 linhas", size=10.5, color=NAVY, weight="bold")
    fig.text(
        0.08, 0.402,
        "Quatro tintos e quatro brancos, após retirar duplicatas. As 13 colunas aparecem em dois blocos.",
        size=7.5, color=MUTED,
    )
    colunas_a = ["wine_type", "quality", "fixed acidity", "volatile acidity", "citric acid", "residual sugar"]
    colunas_b = ["chlorides", "free sulfur dioxide", "total sulfur dioxide", "density", "pH", "sulphates", "alcohol"]
    linhas_a = [
        [str(idx), row["wine_type"], str(int(row["quality"]))]
        + [f"{row[col]:.2f}" for col in colunas_a[2:]]
        for idx, row in exemplo.iterrows()
    ]
    linhas_b = [
        [str(idx), f"{row['chlorides']:.3f}", f"{row['free sulfur dioxide']:.0f}",
         f"{row['total sulfur dioxide']:.0f}", f"{row['density']:.4f}",
         f"{row['pH']:.2f}", f"{row['sulphates']:.2f}", f"{row['alcohol']:.1f}"]
        for idx, row in exemplo.iterrows()
    ]
    tabela(
        fig, [0.08, 0.247, 0.84, 0.140],
        ["linha", *colunas_a], linhas_a,
        [0.08, 0.12, 0.08, 0.16, 0.19, 0.15, 0.22], 6.2,
    )
    tabela(
        fig, [0.08, 0.084, 0.84, 0.140],
        ["linha", "chlorides", "free SO2", "total SO2", "density", "pH", "sulphates", "alcohol"],
        linhas_b, [0.08, 0.15, 0.14, 0.14, 0.14, 0.07, 0.14, 0.14], 6.2,
    )
    fig.text(0.08, 0.070, "SO2 = dióxido de enxofre. Não havia valores ausentes ou não finitos.",
             size=7, color=MUTED)
    pdf.savefig(fig)
    plt.close(fig)

    # Página 2 — método, comparação e curva de sobreajuste.
    fig = pagina(
        2, "Desempenho e comparação",
        "Comparação pela média do erro absoluto (MAE): menor é melhor",
    )
    fig.add_artist(plt.Rectangle((0.08, 0.789), 0.84, 0.078,
                                 transform=fig.transFigure, color=LIGHT, ec="none"))
    fig.text(0.095, 0.846,
             f"Modelo escolhido: {resumo['modelo_escolhido']} ({resumo['n_arvores_escolhido']} árvores)",
             size=11, color=NAVY, weight="bold")
    fig.text(0.095, 0.823,
             f"Por quê? Foi o menor MAE entre os modelos nas cinco dobras: {resumo['MAE_floresta_com_tipo']:.3f}.",
             size=8.2, color=INK)
    fig.text(0.095, 0.801,
             f"Por que 350 árvores? O MAE caiu de {mae_100_arvores:.3f} (100 árvores) para "
             f"{resumo['MAE_floresta_com_tipo']:.3f}; escolhemos o menor erro.",
             size=8.2, color=INK)
    cabecalho(fig, 0.776, "3", "Métrica e desenho da avaliação")
    paragrafo(
        fig, 0.08, 0.752,
        "O MAE mostra, em média, quantos pontos de nota a previsão errou. Usamos 4.256 casos para treinar e comparar nas mesmas cinco dobras. Reservamos 1.064 casos para o teste final. A proporção das notas foi mantida na divisão.",
        largura=108, tamanho=8.2,
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
            ]
        )
    tabela(
        fig, [0.08, 0.574, 0.84, 0.129],
        ["Modelo", "MAE VC", "Faixa VC", "MAE teste"],
        linhas,
        [0.38, 0.17, 0.23, 0.22],
        7.6,
    )
    fig.text(0.08, 0.544, "Por que não os outros?", size=9.5, color=NAVY, weight="bold")
    paragrafo(
        fig, 0.08, 0.525,
        "k-NN (0,550), regressão linear (0,565) e árvore (0,582) erraram mais na validação. A mediana (0,643) foi a referência mais fraca. A escolha foi feita antes de olhar o teste.",
        largura=108, tamanho=8.0,
    )
    ax = fig.add_axes([0.28, 0.311, 0.57, 0.151])
    grafico = comparacao.sort_values("MAE VC", ascending=False)
    sns.barplot(data=grafico, y="modelo", x="MAE VC", color=TEAL, ax=ax)
    titulo_grafico(ax, "MAE médio na validação cruzada")
    ax.set(xlabel="Pontos de nota (menor é melhor)", ylabel="")
    ax.set_xlim(0, max(grafico["MAE VC"]) * 1.12)
    for p in ax.patches:
        ax.text(p.get_width() + 0.006, p.get_y() + p.get_height() / 2, f"{p.get_width():.3f}",
                va="center", size=7, color=INK)
    ax2 = fig.add_axes([0.19, 0.109, 0.67, 0.138])
    sns.lineplot(data=arvore, x="profundidade", y="MAE treino", marker="o", label="Treino", color=RUST, ax=ax2)
    sns.lineplot(data=arvore, x="profundidade", y="MAE VC", marker="o", label="Validação", color=TEAL, ax=ax2)
    ax2.axvline(resumo["profundidade_arvore"], color=NAVY, ls="--", lw=0.9)
    titulo_grafico(ax2, f"Árvore: profundidade {resumo['profundidade_arvore']} minimiza o MAE de validação")
    ax2.set(xlabel="Profundidade máxima", ylabel="MAE")
    ax2.legend(loc="lower left", fontsize=7, frameon=False)
    pdf.savefig(fig)
    plt.close(fig)

    # Página 3 — uso operacional e escolha do corte.
    fig = pagina(3, "Uso pretendido", "Simulação para estudar o efeito de um ponto de corte")
    cabecalho(fig, 0.849, "4", "Decisão apoiada pela previsão")
    paragrafo(
        fig, 0.08, 0.823,
        "Usamos o corte apenas para simular uma triagem de vinhos com nota real 7+. No desenvolvimento, escolhemos 6,0: foi o maior corte que manteve pelo menos 75% de sensibilidade. Previsões de 6,0 ou mais entram na triagem.",
    )
    ax = fig.add_axes([0.19, 0.455, 0.65, 0.255])
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
             "34,7% recebem a classificação ilustrativa"],
        ],
        [0.24, 0.16, 0.60],
        7.6,
    )
    paragrafo(
        fig, 0.08, 0.188,
        "No teste, 37 vinhos 7+ ficaram fora da triagem e 204 escolhidos não eram 7+. Por isso, a regra não pode decidir qualidade sozinha. Um novo corte exigiria validação em novos dados.",
        largura=107, tamanho=8.4,
    )
    pdf.savefig(fig)
    plt.close(fig)

    # Página 4 — limites e diferenças entre grupos.
    fig = pagina(4, "Limitações e auditoria", "O que o desempenho permite afirmar")
    cabecalho(fig, 0.849, "5", "Onde o modelo erra")
    paragrafo(
        fig, 0.08, 0.825,
        "O modelo erra mais nas notas extremas. No teste, só 6 vinhos tiveram nota 3 e só 1 teve nota 9; os erros médios desses grupos são instáveis. O erro também varia entre tintos e brancos.",
    )
    ax = fig.add_axes([0.14, 0.592, 0.36, 0.145])
    sns.barplot(data=erros_nota, x="nota_real", y="MAE", color=TEAL, ax=ax)
    titulo_grafico(ax, "MAE por nota no teste")
    ax.set(xlabel="Nota real", ylabel="MAE")
    ax2 = fig.add_axes([0.67, 0.592, 0.23, 0.145])
    sns.barplot(data=erros_tipo, x="wine_type", y="MAE", color=RUST, ax=ax2)
    titulo_grafico(ax2, "MAE por tipo")
    ax2.set(xlabel="", ylabel="")
    ax2.set_xticks([0, 1], ["Tinto", "Branco"])
    for a, df in [(ax, erros_nota), (ax2, erros_tipo)]:
        for patch, n in zip(a.patches, df["n"]):
            a.annotate(f"n={int(n)}", (patch.get_x() + patch.get_width() / 2, patch.get_height()),
                       ha="center", va="bottom", xytext=(0, 2), textcoords="offset points", size=6.2)
    ax3 = fig.add_axes([0.30, 0.393, 0.57, 0.124])
    top = importancia.head(5).sort_values("aumento_MAE")
    ax3.barh(top["variavel"], top["aumento_MAE"], color=TEAL)
    titulo_grafico(ax3, "Importância por permutação: aumento do MAE")
    ax3.set(xlabel="", ylabel="")
    fig.text(
        0.08, 0.352,
        "Associação preditiva não demonstra que alterar a química causará uma nota diferente.",
        size=8.1, color=MUTED,
    )
    fig.text(0.08, 0.318, "Colunas e grupos no teste", size=10.5, color=NAVY, weight="bold")
    paragrafo(
        fig, 0.08, 0.294,
        f"wine_type quase não mudou o erro quando embaralhado. As medidas químicas já podem indicar o tipo; por isso, não concluímos que a coluna é inútil. Dióxido de enxofre livre e total têm correlação de {pares_correlacionados.iloc[0]['correlacao_absoluta']:.3f} no desenvolvimento: também repetem parte da informação.",
        largura=108, tamanho=8.1,
    )
    linhas_grupo = []
    for _, r in desempenho_tipo.iterrows():
        linhas_grupo.append([
            "Tinto" if r["tipo"] == "red" else "Branco",
            f"{int(r['amostras_teste'])}",
            f"{int(r['casos_7_mais'])}",
            f"{r['MAE']:.3f}",
            f"{100 * r['sensibilidade_regra']:.1f}%",
        ])
    tabela(
        fig, [0.08, 0.130, 0.84, 0.092],
        ["Tipo", "Casos no teste", "Nota 7+", "MAE", "Sensibilidade da simulação"],
        linhas_grupo,
        [0.19, 0.19, 0.16, 0.14, 0.32],
        7.4,
    )
    fig.text(
        0.08, 0.105,
        "As diferenças são descritivas; a base não contém atributos pessoais protegidos.",
        size=7.6, color=MUTED,
    )
    pdf.savefig(fig)
    plt.close(fig)

    # Página 5 — teste de proxy, restrições e resumo.
    fig = pagina(5, "Proxies e restrições", "Aula 7 aplicada ao conjunto de vinhos")
    fig.text(0.08, 0.849, "O tipo continua nas outras medidas?", size=10.5, color=NAVY, weight="bold")
    paragrafo(
        fig, 0.08, 0.824,
        "Testamos se as 11 medidas químicas revelam o tipo do vinho. Depois, comparamos o MAE da floresta com e sem wine_type nas mesmas cinco dobras. Usamos só os dados de desenvolvimento para essas verificações.",
        largura=108, tamanho=8.4,
    )
    tabela(
        fig, [0.08, 0.590, 0.84, 0.155],
        ["Verificação", "Resultado", "Leitura"],
        [
            ["AUC para prever o tipo", f"{resumo['AUC_tipo_pelas_medidas']:.3f}",
             "medidas químicas quase identificam o tipo"],
            ["Acurácia equilibrada", f"{resumo['acuracia_equilibrada_tipo']:.3f}",
             "confere as duas classes apesar do desbalanceamento"],
            ["MAE VC com tipo", f"{resumo['MAE_floresta_com_tipo']:.3f}",
             "floresta original"],
            ["MAE VC sem tipo", f"{resumo['MAE_floresta_sem_tipo']:.3f}",
             "diferença inferior a 0,001 ponto de nota"],
        ],
        [0.31, 0.13, 0.56],
        7.5,
    )
    paragrafo(
        fig, 0.08, 0.550,
        "As medidas quase identificam o tipo do vinho. Retirar wine_type não apaga essa informação. O MAE mudou menos de 0,001, então não há motivo para descartar a coluna por esse teste. Esses resultados mostram associações, não causas. A base não traz dados pessoais sensíveis.",
        largura=108, tamanho=8.2,
    )
    cabecalho(fig, 0.434, "6", "Restrições de uso")
    paragrafo(
        fig, 0.08, 0.409,
        "O modelo serve para estudo. Não deve aprovar lotes, definir preço ou indicar segurança e mudanças químicas. Faltam safra, produtor, variedade e armazenamento. Antes de usar em outro contexto, seria preciso testar novos dados e acompanhar os erros por grupo.",
        largura=108, tamanho=8.2,
    )
    fig.text(0.08, 0.292, "Resumo do projeto: o que fizemos e por quê", size=10, color=NAVY, weight="bold")
    resumo_direto = [
        (0.263, "Pergunta", "Estimamos a nota quality. Usamos regressão porque a resposta é um número."),
        (0.227, "Dados", "Tiramos 1.177 duplicatas para evitar cópias em treino e teste; ficaram 5.320 linhas."),
        (0.191, "Modelo", f"Floresta com 350 árvores: menor MAE na validação ({resumo['MAE_floresta_com_tipo']:.3f}). Com 100, foi {mae_100_arvores:.3f}."),
        (0.155, "Resultado", f"MAE {resumo['mae_teste_modelo']:.3f} no teste, contra {resumo['mae_teste_referencia']:.3f} da mediana: {100 * resumo['reducao_mae_referencia']:.1f}% menos erro."),
        (0.119, "Limite", "O corte 6,0 só simula uma triagem. Faltam dados e o modelo erra mais nas notas extremas."),
    ]
    for y, rotulo, texto in resumo_direto:
        fig.text(0.08, y, rotulo, size=8.2, color=TEAL, weight="bold", va="top")
        paragrafo(fig, 0.20, y, texto, largura=88, tamanho=8.0, altura=1.3)
    pdf.savefig(fig)
    plt.close(fig)

print(f"Relatório vetorial gerado: {DESTINO}")
