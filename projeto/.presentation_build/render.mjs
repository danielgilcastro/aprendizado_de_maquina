import fs from 'node:fs/promises';
import path from 'node:path';
import { FileBlob, PresentationFile } from '@oai/artifact-tool';
const base = process.env.PRES_WORKSPACE;
const pptx = path.join(base,'apresentacao_qualidade_vinhos','qualidade_de_vinhos_apresentacao.pptx');
const out = path.join(base,'.presentation_build');
const deck = await PresentationFile.importPptx(await FileBlob.load(pptx));
for (let i=0;i<9;i++) {
  const png=await deck.export({slide:deck.slides.getItem(i),format:'png',scale:1});
  await fs.writeFile(path.join(out,`slide-${String(i+1).padStart(2,'0')}.png`),new Uint8Array(await png.arrayBuffer()));
}
console.log('rendered 9');
