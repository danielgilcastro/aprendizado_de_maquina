"""Gera o guia de respostas em PDF a partir de respostas_banca.md."""

from __future__ import annotations

import re
from html import escape
from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.enums import TA_LEFT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import (
    HRFlowable,
    KeepTogether,
    PageBreak,
    Paragraph,
    SimpleDocTemplate,
    Spacer,
    Table,
    TableStyle,
)


PROJETO = Path(__file__).resolve().parent
FONTE = PROJETO / "respostas_banca.md"
DESTINO = PROJETO / "respostas_banca.pdf"
TEXTO = FONTE.read_text(encoding="utf-8")

pdfmetrics.registerFont(TTFont("ArialBanca", r"C:\Windows\Fonts\arial.ttf"))
pdfmetrics.registerFont(TTFont("ArialBancaBold", r"C:\Windows\Fonts\arialbd.ttf"))
pdfmetrics.registerFontFamily("ArialBanca", normal="ArialBanca", bold="ArialBancaBold")

NAVY = colors.HexColor("#17344A")
TEAL = colors.HexColor("#427C78")
INK = colors.HexColor("#24333E")
MUTED = colors.HexColor("#61717B")
LIGHT = colors.HexColor("#EEF3F2")
LINE = colors.HexColor("#D7E0E1")


def inline(text: str) -> str:
    text = escape(text)
    text = re.sub(r"\*\*(.+?)\*\*", r"<b>\1</b>", text)
    text = re.sub(r"`(.+?)`", r'<font color="#296561"><b>\1</b></font>', text)
    return text


estilos = {
    "titulo": ParagraphStyle(
        "titulo", fontName="ArialBancaBold", fontSize=20, leading=25,
        textColor=NAVY, spaceAfter=8,
    ),
    "subtitulo": ParagraphStyle(
        "subtitulo", fontName="ArialBanca", fontSize=9.3, leading=13.2,
        textColor=MUTED, spaceAfter=14,
    ),
    "faixa": ParagraphStyle(
        "faixa", fontName="ArialBancaBold", fontSize=10.4, leading=14,
        textColor=TEAL, spaceBefore=5, spaceAfter=12,
    ),
    "pergunta": ParagraphStyle(
        "pergunta", fontName="ArialBancaBold", fontSize=11, leading=15,
        textColor=NAVY, alignment=TA_LEFT,
    ),
    "resposta": ParagraphStyle(
        "resposta", fontName="ArialBanca", fontSize=10, leading=14.6,
        textColor=INK,
    ),
    "local": ParagraphStyle(
        "local", fontName="ArialBanca", fontSize=8.5, leading=11.3,
        textColor=MUTED,
    ),
    "resumo": ParagraphStyle(
        "resumo", fontName="ArialBanca", fontSize=9.4, leading=14,
        textColor=INK,
    ),
}


def cabecalho(canvas, doc):
    canvas.saveState()
    width, height = A4
    canvas.setFillColor(TEAL)
    canvas.setFont("ArialBancaBold", 8)
    canvas.drawString(45, height - 31, "IASEG  /  APRENDIZADO DE MÁQUINA")
    canvas.setStrokeColor(LINE)
    canvas.setLineWidth(0.6)
    canvas.line(45, height - 40, width - 45, height - 40)
    canvas.line(45, 43, width - 45, 43)
    canvas.setFillColor(MUTED)
    canvas.setFont("ArialBanca", 7.5)
    canvas.drawString(45, 29, "Qualidade de vinhos  |  Respostas para a banca")
    canvas.drawRightString(width - 45, 29, str(doc.page))
    canvas.restoreState()


padrao = re.compile(
    r"^## (\d+)\. (.+?)\n\n\*\*Resposta:\*\* (.+?)\n\n\*\*No notebook:\*\* (.+?)(?=\n\n## |\Z)",
    re.MULTILINE | re.DOTALL,
)
perguntas = [
    (int(n), titulo.strip(), resposta.strip(), local.strip())
    for n, titulo, resposta, local in padrao.findall(TEXTO)
]
assert [n for n, *_ in perguntas] == list(range(1, 14)), "Esperadas as 13 perguntas oficiais."
assert "R²" not in TEXTO

primeiros = TEXTO.split("\n\n## 1.", 1)[0].split("\n\n")
introducao = primeiros[1]
resumo = primeiros[2]
extra = TEXTO.split("## Se vier uma pergunta de continuação sobre o tipo de vinho\n\n", 1)[1]
extra_resposta, extra_local = extra.split("\n\n**No notebook:** ", 1)

story = [
    Paragraph("Respostas para a banca", estilos["titulo"]),
    Paragraph(inline(introducao), estilos["subtitulo"]),
    Table(
        [[Paragraph(inline(resumo), estilos["resumo"])]],
        colWidths=[A4[0] - 90],
        style=TableStyle([
            ("BACKGROUND", (0, 0), (-1, -1), LIGHT),
            ("BOX", (0, 0), (-1, -1), 0.45, LINE),
            ("LEFTPADDING", (0, 0), (-1, -1), 12),
            ("RIGHTPADDING", (0, 0), (-1, -1), 12),
            ("TOPPADDING", (0, 0), (-1, -1), 10),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 10),
        ]),
    ),
    Spacer(1, 19),
    Paragraph("Perguntas 1 a 3", estilos["faixa"]),
]

for n, titulo, resposta, local in perguntas:
    if n in {4, 8, 11}:
        story.extend([
            PageBreak(),
            Paragraph(
                {4: "Perguntas 4 a 7", 8: "Perguntas 8 a 10", 11: "Perguntas 11 a 13"}[n],
                estilos["faixa"],
            ),
        ])
    bloco = [
        Paragraph(f"{n:02d}  {inline(titulo)}", estilos["pergunta"]),
        Spacer(1, 6),
        Paragraph(inline(resposta), estilos["resposta"]),
        Spacer(1, 6),
        Paragraph("<b>No notebook:</b> " + inline(local), estilos["local"]),
        Spacer(1, 13),
        HRFlowable(width="100%", thickness=0.45, color=LINE),
        Spacer(1, 13),
    ]
    story.append(KeepTogether(bloco))

story.extend([
    Spacer(1, 8),
    Paragraph("Se perguntarem sobre o tipo de vinho", estilos["faixa"]),
    Paragraph(inline(extra_resposta.strip()), estilos["resposta"]),
    Spacer(1, 6),
    Paragraph("<b>No notebook:</b> " + inline(extra_local.strip()), estilos["local"]),
])

doc = SimpleDocTemplate(
    str(DESTINO), pagesize=A4,
    leftMargin=45, rightMargin=45,
    topMargin=57, bottomMargin=56,
    title="Respostas para a banca - Qualidade de vinhos",
    author="Projeto Qualidade de Vinhos",
)
doc.build(story, onFirstPage=cabecalho, onLaterPages=cabecalho)
print(f"PDF gerado: {DESTINO}")
