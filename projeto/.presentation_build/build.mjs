import fs from 'node:fs/promises';
import path from 'node:path';
import { pathToFileURL } from 'node:url';
import { Presentation, PresentationFile } from '@oai/artifact-tool';

const workspaceDir = process.env.PRES_WORKSPACE;
const skillDir = process.env.SKILL_DIR;
const pythonExecutable = process.env.RUNTIME_PYTHON;
if (!workspaceDir || !skillDir || !pythonExecutable) throw new Error('Missing runtime paths');
const buildDir = path.join(workspaceDir, '.presentation_build');
const outputDir = path.join(workspaceDir, 'apresentacao_qualidade_vinhos');
await fs.mkdir(buildDir, { recursive: true });
await fs.mkdir(outputDir, { recursive: true });
const { resolvePresentationFont, applyPresentationChartFont, finalizePresentation } = await import(
  pathToFileURL(path.join(skillDir, 'container_tools/artifact_tool_utils.mjs')).href
);
const font = resolvePresentationFont({ fontFamily: 'Arial' });
const deck = Presentation.create({ slideSize: { width: 1280, height: 720 } });

const C = { plum: '#5B233B', plum2: '#7A3550', cream: '#F8F4EF', ink: '#272631', muted: '#645D63', rose: '#DDBAC7', grid: '#E4DBDA', white: '#FFFFFF', green: '#355C50' };
const narrations = [];
function box(slide, content, x, y, w, h, size=26, color=C.ink, bold=false, options={}) {
  const s = slide.shapes.add({
    geometry: 'textbox', position: { left:x, top:y, width:w, height:h },
    fill:'none', line:{ fill:'none', width:0 }
  });
  s.text = content;
  s.text.style = { typeface:font, fontSize:size, color, bold, autoFit:'none', ...options };
  return s;
}
function base(title, idx, dark=false) {
  const slide = deck.slides.add();
  slide.background.fill = dark ? C.plum : C.cream;
  if (idx > 1) {
    box(slide, title, 68, 40, 1144, 74, 43, dark ? C.white : C.plum, true);
    box(slide, String(idx).padStart(2,'0'), 1150, 657, 66, 29, 17, dark ? C.rose : C.muted);
  }
  return slide;
}
function notes(slide, narration, source) {
  narrations.push(narration);
  slide.speakerNotes.textFrame.setText(`${narration}\n\nFonte: ${source}`);
}
function metric(slide, number, label, x, y, w, color=C.plum) {
  box(slide, number, x, y, w, 88, 62, color, true);
  box(slide, label, x, y+86, w, 75, 25, C.ink);
}
function bar(slide, categories, values, position, opts={}) {
  const chart = slide.charts.add('bar', {
    position,
    categories,
    series:[{ name:opts.name ?? 'Valor', values, fill:opts.fill ?? C.plum2 }],
    barOptions:{ direction:'bar', grouping:'clustered', gapWidth:70 },
    hasLegend:false,
    xAxis:{ visible:true, min:0, max:opts.max, majorUnit:opts.major, numberFormatCode:opts.format ?? '0.000', textStyle:{ typeface:font, fontSize:17, fill:C.muted }, majorGridlines:{ fill:C.grid, width:1 } },
    yAxis:{ visible:true, textStyle:{ typeface:font, fontSize:19, fill:C.ink }, majorGridlines:null },
    dataLabels:{ showValue:true, position:'outEnd', textStyle:{ typeface:font, fontSize:18, fill:C.ink } },
    chartFill:'none', plotAreaFill:'none', chartLine:{fill:'none',width:0}, plotAreaLine:{fill:'none',width:0}
  });
  applyPresentationChartFont(chart, {fontFamily:font});
  return chart;
}

// 1. Capa
{
  const s=base('',1,true);
  box(s,'Qualidade de vinhos',70,176,1120,100,68,C.white,true);
  box(s,'Como o aprendizado de máquina estima uma nota sensorial',72,305,1050,125,35,C.rose);
  box(s,'Apresentação explicativa do projeto',72,562,950,42,23,C.white);
  notes(s,
    'Olá. Nesta apresentação, vou explicar o projeto de qualidade de vinhos. A ideia é usar medidas físico-químicas e o tipo do vinho para estimar a nota que uma amostra receberia numa avaliação sensorial. Vou mostrar como os dados foram preparados, por que escolhemos a floresta aleatória, o que seus resultados significam e onde estão os limites da análise. O foco é aprender o processo de modelagem, e não criar uma ferramenta pronta para decisões comerciais.',
    'relatorio_qualidade_vinhos.pdf, p. 1; README.md');
}
// 2. Pergunta
{
  const s=base('A pergunta do projeto',2);
  box(s,'Entradas',70,160,480,52,26,C.muted,true);
  box(s,'11 medidas físico-químicas\n+ tipo de vinho',70,221,540,160,34,C.ink,true);
  box(s,'Saída',708,160,460,52,26,C.muted,true);
  box(s,'Nota sensorial\nestimada',708,221,480,154,37,C.plum,true);
  box(s,'Exemplo: 6,3 pontos',708,426,460,70,30,C.plum2);
  box(s,'Como a saída é um número, esta é uma tarefa de regressão.',70,560,1120,80,27,C.ink);
  notes(s,
    'A pergunta central é simples: qual nota sensorial podemos estimar para um vinho a partir das informações que já temos sobre ele? Cada amostra traz onze medidas físico-químicas, como álcool e acidez volátil, além do tipo, tinto ou branco. A resposta do modelo é uma nota numérica prevista. Por exemplo, ele pode devolver seis vírgula três. Por isso, tratamos o problema como regressão. A nota real só é conhecida depois da avaliação sensorial e ficou fora das entradas do modelo.',
    'relatorio_qualidade_vinhos.pdf, p. 1; respostas_banca.md, itens 2 e 9');
}
// 3. Dados
{
  const s=base('Dados e preparação',3);
  metric(s,'6.497','amostras nos dois arquivos originais',69,170,340);
  metric(s,'1.177','duplicatas completas removidas',470,170,330);
  metric(s,'5.320','amostras após a limpeza',852,170,330);
  box(s,'4.256 para desenvolvimento',73,445,515,60,32,C.plum,true);
  box(s,'1.064 reservadas para teste',658,445,530,60,32,C.plum,true);
  box(s,'A remoção de duplicatas evita cópias idênticas em treino e teste. Sem identificador, não sabemos se toda repetição era um erro.',72,566,1130,94,23,C.muted);
  notes(s,
    'Os dados vieram de dois arquivos públicos, um de vinhos tintos e outro de brancos. Juntos, eles tinham seis mil quatrocentas e noventa e sete linhas. Não havia valores ausentes ou não finitos. Antes de dividir a base, removemos mil cento e setenta e sete duplicatas completas. Restaram cinco mil trezentas e vinte amostras. Desse total, quatro mil duzentas e cinquenta e seis ficaram para desenvolvimento, e mil e sessenta e quatro foram reservadas para o teste final. Essa limpeza reduz o risco de uma cópia idêntica aparecer nos dois conjuntos, embora a falta de um identificador não permita afirmar que toda repetição era um erro.',
    'relatorio_qualidade_vinhos.pdf, p. 1; resultados/resumo_metricas.json');
}
// 4. Avaliação
{
  const s=base('Como os modelos foram avaliados',4);
  box(s,'Métrica principal',70,161,460,47,26,C.muted,true);
  box(s,'MAE',70,220,420,103,73,C.plum,true);
  box(s,'Erro absoluto médio, em pontos de nota. Menor é melhor.',73,340,460,156,29,C.ink);
  box(s,'Escolha do modelo',656,161,500,47,26,C.muted,true);
  box(s,'5 dobras de validação',656,227,535,70,38,C.plum,true);
  box(s,'Todos os candidatos passaram pelas mesmas dobras. O teste reservado entrou apenas depois da escolha.',658,345,528,185,28,C.ink);
  box(s,'Referência simples: prever sempre a mediana do desenvolvimento.',70,578,1100,66,23,C.muted);
  notes(s,
    'Para comparar os modelos, usamos o erro absoluto médio, ou MAE. Ele informa quantos pontos de nota a previsão se afasta, em média, da nota real. Um MAE menor indica um resultado melhor. Começamos com uma referência simples: prever sempre a mediana do conjunto de desenvolvimento. Depois comparamos regressão linear, vizinhos mais próximos, árvore de decisão e floresta aleatória. Todos foram avaliados nas mesmas cinco dobras de validação cruzada. O preparo dos dados foi ajustado dentro de cada dobra, para evitar vazamento. O conjunto de teste permaneceu reservado até a escolha do modelo e do corte.',
    'relatorio_qualidade_vinhos.pdf, p. 2; respostas_banca.md, itens 4 e 13');
}
// 5. Comparação
{
  const s=base('A floresta teve o menor erro',5);
  box(s,'MAE médio nas cinco dobras de validação',72,137,1080,46,25,C.muted);
  bar(s,['Floresta aleatória','k-NN','Regressão linear','Árvore','Referência'],[0.531,0.550,0.565,0.582,0.643],{left:72,top:210,width:1115,height:370},{max:0.7,major:0.1});
  box(s,'No teste final: MAE 0,529 versus 0,643 da referência, uma redução de 17,7%.',72,610,1110,59,27,C.plum,true);
  notes(s,
    'Este gráfico mostra o MAE médio da validação cruzada. A floresta aleatória ficou em primeiro, com zero vírgula quinhentos e trinta e um ponto de nota. Em seguida vieram os quinze vizinhos mais próximos, a regressão linear, a árvore e a referência pela mediana. A floresta escolhida tinha trezentas e cinquenta árvores. Só depois dessa escolha usamos o teste reservado. Nele, o MAE da floresta foi zero vírgula quinhentos e vinte e nove, contra zero vírgula seiscentos e quarenta e três da referência. Isso representa uma redução de dezessete vírgula sete por cento no erro médio.',
    'relatorio_qualidade_vinhos.pdf, p. 2; resultados/comparacao_validacao.csv; resultados/comparacao_teste.csv');
}
// 6. Corte
{
  const s=base('Uma triagem apenas para estudo',6);
  box(s,'Corte da nota prevista: 6,0',70,144,1090,68,36,C.plum,true);
  metric(s,'81,7%','sensibilidade: 165 de 202 casos 7+ encontrados',70,240,530);
  metric(s,'44,7%','precisão: cerca de 45 em 100 selecionados são 7+',678,240,520);
  box(s,'37 casos 7+ ficaram abaixo do corte',73,514,530,62,25,C.ink,true);
  box(s,'204 selecionados não eram 7+',679,514,509,62,25,C.ink,true);
  box(s,'O corte foi definido no desenvolvimento. Não é uma regra de decisão comercial.',73,606,1120,55,23,C.muted);
  notes(s,
    'Além da previsão numérica, o projeto simulou uma triagem de vinhos com nota real sete ou maior. No desenvolvimento, escolhemos um corte de seis vírgula zero para a nota prevista. No teste, a regra recuperou cento e sessenta e cinco dos duzentos e dois vinhos com nota sete ou mais. Essa é uma sensibilidade de oitenta e um vírgula sete por cento. Mas a precisão foi de quarenta e quatro vírgula sete por cento: menos da metade dos selecionados realmente tinha nota sete ou mais. Trinta e sete bons vinhos ficaram abaixo do corte e duzentos e quatro selecionados não eram sete mais. Por isso, a regra serve para discutir compromissos entre erros, não para decidir qualidade comercial.',
    'relatorio_qualidade_vinhos.pdf, p. 3; resultados/resumo_metricas.json');
}
// 7. Erros
{
  const s=base('Os erros aumentam nas notas extremas',7);
  box(s,'MAE no teste por nota real',72,137,1080,43,24,C.muted);
  bar(s,['3 (n=6)','4 (n=41)','5 (n=350)','6 (n=465)','7 (n=171)','8 (n=30)','9 (n=1)'],[2.369,1.211,0.437,0.401,0.647,1.521,3.371],{left:70,top:195,width:780,height:420},{max:3.7,major:0.5,format:'0.0'});
  box(s,'Por tipo',900,214,290,47,27,C.muted,true);
  box(s,'Tinto: 0,453\nBranco: 0,554',900,276,280,130,30,C.plum,true);
  box(s,'Notas 3 e 9 têm apenas 6 e 1 casos no teste.',896,454,298,170,25,C.ink);
  notes(s,
    'O erro médio não é igual em todos os casos. As previsões tendem a se aproximar do centro da distribuição e ficam piores nas notas extremas. Para nota três, o MAE foi dois vírgula trinta e sete. Para nota nove, três vírgula trinta e sete. Esses números, porém, vêm de apenas seis e uma amostra no teste, respectivamente, então são pouco estáveis. Também observamos um MAE de zero vírgula quatrocentos e cinquenta e três em tintos e zero vírgula quinhentos e cinquenta e quatro em brancos. Essa diferença merece nova validação. Ela, sozinha, não permite concluir que exista discriminação.',
    'relatorio_qualidade_vinhos.pdf, p. 4; resultados/erros_por_nota.csv; resultados/desempenho_tipo.csv');
}
// 8. Variáveis
{
  const s=base('Quais medidas mais influenciam a previsão',8);
  box(s,'Aumento do MAE quando cada variável é embaralhada',72,138,1100,45,24,C.muted);
  bar(s,['Álcool','Acidez volátil','SO₂ livre','Sulfatos','SO₂ total'],[0.137,0.057,0.038,0.021,0.015],{left:72,top:210,width:910,height:325},{max:0.15,major:0.03});
  box(s,'Associação preditiva não prova causa.',73,563,1080,52,30,C.plum,true);
  box(s,'As medidas químicas também quase identificam o tipo do vinho: AUC 0,996.',73,622,1090,42,22,C.muted);
  notes(s,
    'Para entender de quais informações o modelo mais depende, embaralhamos cada variável e observamos quanto o erro aumentava. O maior aumento apareceu para o teor de álcool: zero vírgula cento e trinta e sete ponto de nota. Depois vieram a acidez volátil e o dióxido de enxofre livre. Isso mostra associação preditiva, mas não prova que alterar a composição química de um vinho causará mudança na avaliação. Também testamos se as onze medidas identificam o tipo do vinho. A AUC foi zero vírgula novecentos e noventa e seis. Portanto, mesmo retirando a coluna de tipo, muito dessa informação permanece nas outras medidas.',
    'relatorio_qualidade_vinhos.pdf, pp. 4–5; resultados/importancia_permutacao.csv; resultados/resumo_metricas.json');
}
// 9. Fechamento
{
  const s=base('O que podemos concluir',9,true);
  box(s,'O modelo melhora a referência',71,161,1070,55,31,C.rose,true);
  box(s,'MAE 0,529 no teste e R² 0,396',73,222,1100,72,41,C.white,true);
  box(s,'Ainda há muita variação individual sem explicação.',73,317,1070,60,29,C.white);
  box(s,'Uso adequado',73,427,450,49,26,C.rose,true);
  box(s,'Aprender e demonstrar o fluxo de modelagem.',73,489,1070,58,29,C.white);
  box(s,'Para aplicar em novos contextos, seriam necessários dados e validação externa.',73,582,1100,72,25,C.white);
  notes(s,
    'Para concluir, a floresta aleatória fez previsões melhores que a referência simples. O erro médio no teste ficou em cerca de meio ponto de nota. Ao mesmo tempo, o R quadrado de zero vírgula trezentos e noventa e seis mostra que boa parte da variação entre amostras ainda não foi explicada. O melhor uso deste trabalho é didático: compreender a preparação, a validação, a escolha do modelo e a análise dos erros. Ele não deve aprovar lotes, definir preços, certificar segurança sanitária nem orientar mudanças químicas. A base não informa safra, produtor ou armazenamento. Antes de usar o modelo em outras regiões, períodos ou laboratórios, precisaríamos de validação externa. Obrigado.',
    'relatorio_qualidade_vinhos.pdf, pp. 2 e 5; respostas_banca.md, itens 1 e 12');
}

const candidatePath = path.join(buildDir,'candidate.pptx');
await (await PresentationFile.exportPptx(deck)).save(candidatePath);
const finalPath = path.join(outputDir,'qualidade_de_vinhos_apresentacao.pptx');
const result = await finalizePresentation({
  workspaceDir,
  candidatePath,
  finalPath,
  pythonExecutable,
  integrityValidatorPath:path.join(skillDir,'container_tools/inspect_presentation_package_integrity.py'),
  layoutValidatorPath:path.join(skillDir,'container_tools/inspect_presentation_layout_geometry.py'),
  layoutArgs:['--expected-slide-size-emu','12192000,6858000','--validate-heading-fit'],
  requiredNativeTableOwnerSlides:[],
  requiredNativeChartOwnerSlides:[5,7,8],
  materializeLiteralChartWorkbooks:true,
  fontPolicy:{basis:'design',families:[font]},
  verifyArtifactToolImport:true,
  receiptPath:path.join(buildDir,'validation.json'),
});
await fs.writeFile(path.join(buildDir,'narrations.json'), JSON.stringify(narrations,null,2),'utf8');
await fs.writeFile(path.join(outputDir,'roteiro_da_narracao.txt'), narrations.map((x,i)=>`SLIDE ${i+1}\n${x}`).join('\n\n'),'utf8');
for (let i=0;i<deck.slides.length;i++) {
  const png = await deck.export({slide:deck.slides.getItemAt(i),format:'png',scale:1});
  await fs.writeFile(path.join(buildDir,`slide-${String(i+1).padStart(2,'0')}.png`),new Uint8Array(await png.arrayBuffer()));
}
console.log(JSON.stringify({finalPath,slideCount:deck.slides.length,validation:result}));
