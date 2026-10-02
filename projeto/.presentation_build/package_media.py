from pathlib import Path
import shutil
import wave

root = Path(r'C:\Users\danie\OneDrive\Área de Trabalho\apredizado de maquinba\projeto')
build = root / '.presentation_build'
out = root / 'apresentacao_qualidade_vinhos'
media = out / 'midia'
media.mkdir(parents=True, exist_ok=True)

frames = []
params = None
durations = []
for i in range(1, 10):
    src_slide = build / f'slide-{i:02d}.png'
    src_audio = build / f'audio-slide-{i:02d}.wav'
    shutil.copy2(src_slide, media / src_slide.name)
    shutil.copy2(src_audio, media / src_audio.name)
    with wave.open(str(src_audio), 'rb') as wav:
        this = (wav.getnchannels(), wav.getsampwidth(), wav.getframerate(), wav.getcomptype())
        if params is None:
            params = this
        assert this == params, (this, params)
        part = wav.readframes(wav.getnframes())
        durations.append(wav.getnframes() / wav.getframerate())
        frames.append(part)

combined = out / 'narracao_completa_qualidade_de_vinhos.wav'
with wave.open(str(combined), 'wb') as wav:
    wav.setnchannels(params[0])
    wav.setsampwidth(params[1])
    wav.setframerate(params[2])
    for i, part in enumerate(frames):
        wav.writeframes(part)
        if i < len(frames) - 1:
            wav.writeframes(b'\0' * params[0] * params[1] * params[2])

html = '''<!doctype html>
<html lang="pt-BR">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Qualidade de vinhos: apresentação com voz</title>
<style>
  :root { color-scheme: dark; font-family: Arial, sans-serif; }
  * { box-sizing: border-box; }
  body { margin: 0; background: #1d1720; color: #fff; }
  main { min-height: 100vh; display: grid; place-items: center; padding: 16px; }
  .player { width: min(100%, 1280px); }
  img { display: block; width: 100%; aspect-ratio: 16/9; object-fit: contain; background: #f8f4ef; box-shadow: 0 8px 30px #0008; }
  .controls { display: flex; align-items: center; gap: 12px; padding-top: 16px; flex-wrap: wrap; }
  button { background: #8b4b64; color: #fff; border: 0; border-radius: 6px; padding: 12px 17px; font: inherit; cursor: pointer; }
  button:hover, button:focus-visible { background: #ae6983; }
  #counter { margin-left: auto; font-size: 18px; }
  audio { width: 100%; margin-top: 12px; }
  p { color: #d8cbd1; margin: 10px 0 0; font-size: 15px; }
</style>
</head>
<body>
<main><div class="player">
  <img id="slide" src="midia/slide-01.png" alt="Slide 1: Qualidade de vinhos">
  <div class="controls">
    <button id="start">▶ Iniciar apresentação</button>
    <button id="prev">◀ Anterior</button>
    <button id="next">Próximo ▶</button>
    <span id="counter" aria-live="polite">1 / 9</span>
  </div>
  <audio id="voice" controls preload="metadata" src="midia/audio-slide-01.wav"></audio>
  <p>Ao terminar a fala, o próximo slide começa automaticamente. Use os botões para navegar.</p>
</div></main>
<script>
const total = 9;
let index = 1;
const slide = document.getElementById('slide');
const voice = document.getElementById('voice');
const counter = document.getElementById('counter');
const pad = n => String(n).padStart(2, '0');
function show(n, play=true) {
  index = Math.max(1, Math.min(total, n));
  voice.pause();
  slide.src = `midia/slide-${pad(index)}.png`;
  slide.alt = `Slide ${index} de ${total}`;
  voice.src = `midia/audio-slide-${pad(index)}.wav`;
  counter.textContent = `${index} / ${total}`;
  if (play) voice.play().catch(() => {});
}
document.getElementById('start').onclick = () => show(1, true);
document.getElementById('prev').onclick = () => show(index - 1, true);
document.getElementById('next').onclick = () => show(index + 1, true);
voice.addEventListener('ended', () => { if (index < total) show(index + 1, true); });
document.addEventListener('keydown', e => {
  if (e.key === 'ArrowRight') show(index + 1, true);
  if (e.key === 'ArrowLeft') show(index - 1, true);
});
</script>
</body>
</html>'''
(out / 'apresentacao_com_voz.html').write_text(html, encoding='utf-8')
print(f'durations: {[round(x, 1) for x in durations]}')
print(f'total duration: {sum(durations) + 8:.1f}s')
print(f'combined bytes: {combined.stat().st_size}')
