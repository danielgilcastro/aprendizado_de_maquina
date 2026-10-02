$ErrorActionPreference = 'Stop'
Add-Type -AssemblyName System.Speech
$base = 'C:\Users\danie\OneDrive\Área de Trabalho\apredizado de maquinba\projeto'
$build = Join-Path $base '.presentation_build'
$items = Get-Content -LiteralPath (Join-Path $build 'narrations.json') -Raw -Encoding UTF8 | ConvertFrom-Json
$speaker = New-Object System.Speech.Synthesis.SpeechSynthesizer
$speaker.SelectVoice('Microsoft Maria Desktop')
$speaker.Rate = 0
$speaker.Volume = 100
try {
  for ($i=0; $i -lt $items.Count; $i++) {
    $wave = Join-Path $build ('audio-slide-{0:d2}.wav' -f ($i+1))
    $speaker.SetOutputToWaveFile($wave)
    $speaker.Speak(('Slide {0}. ' -f ($i+1)) + [string]$items[$i])
    $speaker.SetOutputToNull()
    $item = Get-Item -LiteralPath $wave
    Write-Output ('{0}: {1} bytes' -f $item.Name, $item.Length)
  }
} finally {
  $speaker.Dispose()
}
