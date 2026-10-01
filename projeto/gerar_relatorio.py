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
teste = pd.read_csv(RESULTADOS / "comparacao_teste.csv")
arvore = pd.read_csv(RESULTADOS / "curva_arvore.csv")
cortes = pd.read_csv(RESULTADOS / "curva_corte.csv")
erros_nota = pd.read_csv(RESULTADOS / "erros_por_nota.csv")
erros_tipo = pd.read_csv(RESULTADOS / "erros_por_tipo.csv")
importancia = pd.read_csv(RESULTADOS / "importancia_permutacao.csv")
pares_correlacionados = pd.read_csv(RESULTADOS / "pares_correlacionados.csv")
desempenho_tipo = pd.read_csv(RESULTADOS / "desempenho_tipo.csv")

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
        "Siglas: MAE = erro absoluto médio; RMSE = raiz do erro quadrático médio; R² = coeficiente de determinação.",
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
        "Este projeto usa a qualidade de vinhos para entender as etapas do aprendizado de máquina supervisionado: preparar dados, treinar modelos, comparar resultados em casos inéditos e examinar limitações. A pergunta é qual nota sensorial (quality) pode ser estimada a partir das 11 medidas físico-químicas e do tipo de vinho. A saída é um número; portanto, a tarefa é regressão.",
    )
    cabecalho(fig, 0.622, "2", "Dados utilizados")
    paragrafo(
        fig, 0.08, 0.599,
        "Dois CSVs públicos (tinto e branco) trazem 11 medidas e a nota por amostra. Acrescentamos wine_type e usamos cópias locais dos links abaixo.",
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
        fig, [0.08, 0.414, 0.84, 0.105],
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
    ax = fig.add_axes([0.12, 0.125, 0.45, 0.245])
    sns.barplot(x=distribuicao.index.astype(str), y=distribuicao.values, color=TEAL, ax=ax)
    titulo_grafico(ax, "Distribuição das notas originais")
    ax.set(xlabel="Nota", ylabel="Amostras")
    ax2 = fig.add_axes([0.63, 0.13, 0.27, 0.22])
    ax2.axis("off")
    ax2.text(0, 1, "Auditoria", transform=ax2.transAxes, size=10, weight="bold", color=NAVY, va="top")
    ax2.text(
        0, 0.82,
        "Nulos e não finitos: zero;\n"
        "nenhuma linha saiu por isso.\n\n"
        "Duplicatas completas: 1.177;\n"
        "removidas antes da divisão\n"
        "para evitar cópias em treino\n"
        "e teste.\n\n"
        "Sem identificador, algumas\n"
        "podem ser amostras legítimas.",
        transform=ax2.transAxes, size=8.0, color=INK, va="top", linespacing=1.35,
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
        "Reservamos 20% (1.064 casos) para avaliar previsões em dados inéditos, mantendo 80% (4.256) para treinar e escolher o modelo. Assim, o teste tem tamanho útil sem reduzir demais o desenvolvimento. A estratificação preserva a proporção das notas. Todos os candidatos usaram as mesmas cinco dobras; codificação e escala são ajustadas dentro de cada dobra.",
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
                f"{t['R² teste']:.3f}",
            ]
        )
    tabela(
        fig, [0.08, 0.590, 0.84, 0.155],
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
    fig = pagina(3, "Uso pretendido", "Simulação para estudar o efeito de um ponto de corte")
    cabecalho(fig, 0.849, "4", "Decisão apoiada pela previsão")
    paragrafo(
        fig, 0.08, 0.823,
        "O uso pretendido é didático: simular a identificação de amostras com nota real de pelo menos 7 e observar a troca entre sensibilidade e precisão. Com previsões fora da dobra no desenvolvimento, escolhemos o maior corte em décimos que manteve sensibilidade mínima de 75%: 6,0. Uma previsão acima do corte recebe a classificação ilustrativa de 7+.",
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
             "34,7% recebem a classificação ilustrativa"],
        ],
        [0.24, 0.16, 0.60],
        7.6,
    )
    paragrafo(
        fig, 0.08, 0.188,
        "A simulação favorece recuperar os casos 7+. No teste, 37 ficaram abaixo do corte e 204 amostras acima dele não eram 7+. Esses erros mostram que o corte não é uma decisão automática de qualidade. Qualquer novo corte precisaria ser definido e validado em novos dados.",
        largura=107, tamanho=8.4,
    )
    pdf.savefig(fig)
    plt.close(fig)

    # Página 4 — limites e diferenças entre grupos.
    fig = pagina(4, "Limitações e auditoria", "O que o desempenho permite afirmar")
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
    fig.text(0.08, 0.318, "Colunas e grupos no teste", size=10.5, color=NAVY, weight="bold")
    paragrafo(
        fig, 0.08, 0.294,
        f"Wine_type teve importância isolada próxima de zero. Isso não prova que o tipo seja irrelevante: as medidas químicas podem carregar a mesma informação. Dióxido de enxofre livre e total têm correlação absoluta de {pares_correlacionados.iloc[0]['correlacao_absoluta']:.3f} no desenvolvimento, outro exemplo de informação compartilhada. O desempenho também varia entre tintos e brancos.",
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

    # Página 5 — teste de proxy, restrições e fontes.
    fig = pagina(5, "Proxies e restrições", "Aula 7 aplicada ao conjunto de vinhos")
    fig.text(0.08, 0.849, "O tipo continua nas outras medidas?", size=10.5, color=NAVY, weight="bold")
    paragrafo(
        fig, 0.08, 0.824,
        "Com apenas as 11 medidas químicas do desenvolvimento, um classificador tentou prever se o vinho era tinto ou branco. Também repetimos as cinco dobras da floresta para prever quality após retirar wine_type. Nenhum desses testes consultou o conjunto reservado para escolher um novo modelo.",
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
        "O tipo é altamente recuperável pelas medidas. Tirar wine_type, portanto, não apaga a informação de estilo. O MAE médio quase não mudou, mas essa pequena diferença não demonstra que a coluna deva ser descartada. Importância por permutação, correlação e este teste de proxy descrevem associações do modelo, não causas. Não há variáveis pessoais sensíveis para avaliar discriminação.",
        largura=108, tamanho=8.2,
    )
    cabecalho(fig, 0.434, "6", "Restrições de uso")
    paragrafo(
        fig, 0.08, 0.409,
        "O projeto é para compreender aprendizado de máquina. O modelo e o corte não devem decidir qualidade comercial, aprovação de lotes, preço, segurança sanitária ou mudanças químicas. A base não informa safra, produtor, variedade de uva ou armazenamento. Aplicações em outros contextos exigem validação externa e acompanhamento dos erros por grupo.",
        largura=108, tamanho=8.2,
    )
    fig.text(0.08, 0.292, "Reprodução e responsáveis", size=9.4, color=NAVY, weight="bold")
    paragrafo(
        fig, 0.08, 0.270,
        "Os CSVs locais, a semente 42 e as mesmas dobras permitem reproduzir a análise. O alvo fica fora das entradas; duplicatas saem antes da divisão; preparo, modelo e corte são fixados sem consultar o teste.",
        largura=110, tamanho=7.8,
    )
    fig.text(
        0.08, 0.203,
        "Seções: Daniel Gil (1 e 6); Bruno Pimentel (2); Bruno Groppo (3);",
        size=7.7, color=INK,
    )
    fig.text(0.08, 0.187, "Wallace Jardim (4); Reynato Junior (5).", size=7.7, color=INK)
    fig.text(0.08, 0.151, "Fontes", size=8.7, color=NAVY, weight="bold")
    fig.text(
        0.08, 0.132,
        "Cortez et al. (2009), Modeling wine preferences by data mining from physicochemical properties.\n"
        "IASEG, Projeto da Disciplina 2 e Aula 7 (2026). URLs dos CSVs na página 1.",
        size=7.3, color=MUTED, va="top", linespacing=1.35,
    )
    pdf.savefig(fig)
    plt.close(fig)

print(f"Relatório vetorial gerado: {DESTINO}")
