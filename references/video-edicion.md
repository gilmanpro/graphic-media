# Edición y conversión de vídeo

Herramienta única: **FFmpeg** vía `scripts/video.py` (todo el conocimiento está en los comandos, no reescribas llamadas sueltas). Si falta FFmpeg → `references/instalacion.md`.

Índice: [1 Comandos](#1-comandos-del-script) · [2 Formatos](#2-formatos-y-codecs) · [3 Calidad](#3-calidad-crf-bitrate) · [4 Filtros](#4-filtros-y-denoise) · [5 GIF](#5-gif-de-calidad) · [6 Frames](#6-frames-onde-a-secuencia) · [7 Transparencia](#7-video-con-transparencia)

## 1 Comandos del script

```bash
python scripts/video.py info clip.mov                          # duración, resolución, fps, codecs
python scripts/video.py convertir clip.mov -o clip.mp4         # cambio de extensión
python scripts/video.py recortar clip.mp4 -o corte.mp4 --inicio 12 --duracion 5
python scripts/video.py redimensionar clip.mp4 -o 720p.mp4 --ancho 1280
python scripts/video.py filtro clip.mp4 -o limpio.mp4 --filtro denoise
python scripts/video.py comprimir pesado.mp4 -o ligero.mp4 --crf 28
python scripts/video.py frames clip.mp4 --carpeta frames --fps 2
python scripts/video.py gif clip.mp4 -o mini.gif --fps 12 --ancho 480
python scripts/video.py ensamblar --carpeta frames -o salida.mp4 --fps 24
python scripts/video.py silenciar clip.mp4 -o mudo.mp4
python scripts/video.py extraer-audio clip.mp4 -o pista.wav
```

Conversión de extensión de TODO tipo en un solo comando: `python scripts/convertir.py in.mov -o out.webp|mp4|mp3...`.

## 2 Formatos y codecs

| Destino | Cuándo elegirlo | Codec (el script lo pone) |
|---|---|---|
| **MP4 (H.264)** | por defecto: compatible con todo (web, redes, PowerPoint) | libx264 + yuv420p |
| **WebM (VP9)** | web ligera, HTML5 con transparencia | libvpx-vp9 |
| **MOV** | edición (Final Cut/iMovie), original Apple | libx264 |
| **MKV** | contenedor para múltiples pistas/subtítulos | libx264 |
| **AVI** | solo si lo pide un sistema antiguo | mpeg4 |
| **GIF** | previews cortas (<15s, sin audio) | paleta 256 |

`yuv420p` es obligatorio para compatibilidad; el script ya lo añade. Anchos impares rompen x264 (el script fuerza `-2` par).

## 3 Calidad (CRF / bitrate)

- **CRF** (x264/vp9): menor = mejor y más pesado. `18` casi lossless · `23` por defecto · `28` comprimido · `32` mínimo aceptable.
- Objetivos típicos: web 1080p ≈ CRF 20-23 y <5 MB/min; archive ≈ CRF 16-18.
- `comprimir` usa `-preset slow` (mejor relación tamaño/calidad a costa de CPU).
- No subas bitrate a mano si ya hay CRF: son estrategias distintas (CRF = calidad constante, bitrate = flujo constante).

## 4 Filtros y denoise

`--filtro` de `video.py`: `grayscale, sepia, blur, brillo, contraste, denoise, denoise-fuerte, nitidez`.

- **denoise** = `hqdn3d` (rápido, ruido de sensor/compresión). Primera elección en vídeo casero o poca luz.
- **denoise-fuerte** = `nlmeans` (lento, mejor); para archivo con grano muy sucio.
- Encadenar filtros: ejecuta `filtro` dos veces con salida intermedia (no uno tras otro en el mismo `-vf` salvo que lo controles tú).
- Denoise + nitidez después: el denoise ablanda; `nitidez` solo tras denoise, nunca solo en vídeo ya nítido (amplifica ruido).

## 5 GIF de calidad

`gif` hace **paleta doble pasada** (`palettegen` + `paletteuse` con dither bayer): sin bandas de color. Parámetros: `--fps 12` (legible), `--ancho 480` (peso). Reglas:

- GIF solo para previews cortas; para loops de calidad use MP4/WebM (mismo peso, mucho mejor).
- Sin audio (el formato no lo soporta).
- `convertir.py in.gif -o out.mp4` cuando el origen sea un GIF animado.

## 6 Frames: onda ↔ secuencia

- **Vídeo → frames**: `frames --fps 2` (analizar/corregir imágenes puntuales) o sin `--fps` (todos).
- **Frames → vídeo**: PNG con nombres `frame0001.png`, … y `ensamblar --fps 24`.
- Flujo de purga: vídeo → frames → `editar_imagen.py` sobre los frames que fallen → `ensamblar`.
- Antes de ensamblar: verificar que todos los PNG tienen el MISMO tamaño (si no, `redimensionar` los frames).

## 7 Vídeo con transparencia (overlay)

Para superponer un gráfico con alfa sobre otro clip sin re-codificar el fondo:

```bash
ffmpeg -i fondo.mp4 -i capa.webm -filter_complex "[1:v]format=rgba[c];[0:v][c]overlay" -c:v libx264 -crf 20 out.mp4
```

La capa debe ser WebM con canal alfa (VP9) o PNG secuencial; MP4 no tiene transparencia.

Anti-patrones: convertir MP4→MP4 (genera doble pérdida sin motivo — el origen ya está codificado; si recodificas, sube calidad de destino o no toques); denoise agresivo en animation/dibujo (borra el line-art); avisar de «alta calidad» con CRF 30.
