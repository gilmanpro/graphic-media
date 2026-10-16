# Herramientas de audio

Herramienta única: **FFmpeg** vía `scripts/audio.py`. Si falta FFmpeg → `references/instalacion.md`. Frontera: TTS (texto→voz) y transcripción (voz→texto) NO son de esta skill (hay skills dedicadas); aquí: conversión, recorte, normalización, limpieza, mezcla y visualización.

Índice: [1 Comandos](#1-comandos-del-script) · [2 Formatos](#2-formatos) · [3 Normalización](#3-normalización-loudnorm-ebu-r128) · [4 Silencios y limpieza](#4-silencios-y-limpieza) · [5 Mezcla](#5-mezcla-y-ducking) · [6 Waveform](#6-waveform)

## 1 Comandos del script

```bash
python scripts/audio.py info tema.wav                          # codecs, canales, duración
python scripts/audio.py convertir tema.wav -o tema.mp3 --bitrate 192k
python scripts/audio.py recortar tema.mp3 -o intro.mp3 --inicio 30 --duracion 15
python scripts/audio.py normalizar voz.mp3 -o voz_n.wav --lufs -16
python scripts/audio.py volumen tema.mp3 -o subido.mp3 --db 3
python scripts/audio.py silencios voz.wav -o voz_limpia.wav        # bordes
python scripts/audio.py silencios voz.wav -o v.wav --internos      # también pausas largas
python scripts/audio.py extraer video.mp4 -o audio.wav
python scripts/audio.py unir a.mp3 b.mp3 c.mp3 -o completo.mp3
python scripts/audio.py forma tema.mp3 -o onda.png                 # imagen de la onda
python scripts/audio.py fundir voz.mp3 fondo.mp3 -o mezcla.mp3     # ducking automático
```

## 2 Formatos

| Formato | Cuándo | Notas |
|---|---|---|
| **WAV** | trabajo/edición intermedia | sin pérdida, pesado (≈10 MB/min estéreo 44.1k) |
| **FLAC** | archivo sin pérdida comprimido | ~50% del WAV |
| **MP3** | distribución general | 192k suficiente para voz/música |
| **M4A/AAC** | vídeo y Apple | el que embeben los MP4 |
| **OGG Vorbis** | juegos/web cuando no se quiere MP3 | licencia libre |
| **OPUS** | web en tiempo real (WebRTC), lo más eficiente | mejor que MP3 a cualquier bitrate |

Regla: ** WAV/FLAC para editar** (sin pérdida acumulada en varias pasadas), **MP3/M4A/OPUS para entregar**. Cada conversión a lossy pierde calidad: cadena mínima de pasadas.

## 3 Normalización (loudnorm EBU R128)

`normalizar` hace **dos pasadas** (medir → aplicar), como exige el estándar:

1. Mide el archivo (`input_i`, `input_lra`, `input_thresh`...).
2. Aplica `loudnorm` con esas medidas en modo `linear` (sin compresión de rango).

Objetivos: `--lufs -16` (podcast, Spotify/YouTube, por defecto) · `--lufs -23` (radiodifusión EBU R128) · pico `--tp -1.5` dBTP (margen antipico).

- Normalizar ≠ limitar: si el original tiene picos a 0 dB, la normalización a -16 sube el nivel y luego limita; NO arregla un audio que ya está cortado (distorsión previa).
- Un solo archivo de la cadena: si normalizas dos veces, la segunda corrección es residual (mejor normaliza al FINAL de la edición).

## 4 Silencios y limpieza

- `silencios` recorta bordes por debajo de -50 dB; `--internos` también pausas internas (cuidado: en entrevistas rompe el ritmo — usar solo en locución continua).
- Para ruido de fondo constante (soplo, aire): encadenar tras normalizar `highpass=f=80` (quita retumbe) y `afftdn` (denoise espectral) — se aplica con `filtro` manual de ffmpeg si el caso lo requiere.
- Orden recomendado de limpieza: recorte → highpass/denoise → normalizar → entregar.

## 5 Mezcla y ducking

- `fundir voz fondo` aplica **sidechaincompress**: el fondo baja automáticamente mientras suena la voz (ducking). Voz encima, fondo debajo.
- Niveles de referencia al mezclar: voz ≈ -16 LUFS, música de fondo -18 a -23 dB bajo la voz (con ducking, automático).
- `unir` concatena pistas del mismo formato (si mezclas formatos, convierte todos a WAV antes).

## 6 Waveform

`forma` genera PNG de la onda (1200x300, color de la skill) con `showwavespic`: útil como imagen de pista en páginas, portadas de podcast o para verificar visualmente picos/silencios antes de entregar.

Anti-patrones: subir volumen con `volume=+10dB` en vez de normalizar (recorta); cadenas de conversión MP3→MP3 (pérdida acumulada); normalizar a la vez varios archivos sin medir cada uno (el script ya mide uno a uno); aplicar reverb/EQ sin escuchar — esta skill no diseña sonido, solo opera y limpia.
