# Manual de los scripts preestablecidos

Todos se ejecutan desde la raíz de la skill (`python scripts/<script> ...`). Errores de dependencia salen con el `pip install` exacto. No reescribas código que un script ya cubre.

## scripts/editar_imagen.py — Pillow (requisito: `pip install pillow`)

| Comando | Qué hace | Ejemplo |
|---|---|---|
| `info` | Dimensiones, modo, formato | `python scripts/editar_imagen.py info foto.jpg` |
| `recortar` | Corte exacto x,y,ancho,alto | `... recortar in.png out.png --box 50,50,800,600` |
| `redimensionar` | Escala (conserva proporción sin `--alto`) | `... redimensionar in.png out.png --ancho 1200` |
| `filtro` | `grayscale, sepia, blur, sharp, contour, bright, contrast, posterizar` | `... filtro in.png out.png --filtro sepia` |
| `transparencia` | Vuelve alfa un color de fondo | `... transparencia in.png out.png --color "#ffffff" --tolerancia 30` |
| `gif` | Combina frames en GIF (`disposal=2`, sin parpadeo) | `... gif out.gif f1.png f2.png f3.png --duracion 300` |
| `contacto` | Hoja de contacto en rejilla (QA de lotes) | `... contacto hoja.jpg a.png b.png c.png --columnas 3` |
| `superponer` | Compone una imagen sobre otra (marca de agua) | `... superponer base.png logo.png out.png --x 10 --y 10 --redimensionar 200` |

Notas: la orientación EXIF se respeta en todos los comandos; nunca escribe sobre el original si le pasas la misma ruta de salida distinta; para quitar fondos con ruido usa `--tolerancia` alto (hasta 120) y verifica con `info`.

## scripts/grafico.py — gráficos CSV→PNG/SVG (requisito: `pip install matplotlib`)

CSV con encabezados en la primera fila.

```bash
python scripts/grafico.py ventas.csv --tipo bar   --x mes --y ventas --titulo "Ventas 2026" -o ventas.png
python scripts/grafico.py kpi.csv   --tipo line   --x fecha --y visitas,conversion -o trafico.png
python scripts/grafico.py pob.csv   --tipo hist   --y edad -o hist.png
python scripts/grafico.py reg.csv   --tipo pie    --x region --y total -o pastel.png
python scripts/grafico.py disp.csv  --tipo scatter --x edad --y ingresos -o nube.png
```

Opciones: `--transparente` (PNG alfa), `--dpi 300` (def.), `--svg` (vectorial), `--xlabel/--ylabel`, `--ancho/--alto` (pulgadas, def. 8x4.5).

## scripts/histograma_animado.py — GIF de histograma (requisito: `pip install matplotlib`)

```bash
python scripts/histograma_animado.py --simular 500 -o hist.gif            # demo N(0,1) acumulada
python scripts/histograma_animado.py datos.csv --columna ventas --frames 40 -o hist.gif
python scripts/histograma_animado.py --simular 300 --evolutivo -o evo.gif # distribución que cambia
```

`--bins 40` (fijos en todos los frames: sin fijos el gif baila), `--fps 8`, `--mp4` (requiere ffmpeg). Sin ffmpeg el GIF usa PillowWriter (cero dependencias).

## scripts/svg_a_raster.py — SVG→PNG/PDF (backends en cadena)

```bash
python scripts/svg_a_raster.py logo.svg -o logo.png --escala 2
python scripts/svg_a_raster.py plano.svg -o plano.pdf
```

Cadena: `cairosvg` → `svglib+reportlab` → `inkscape`/`rsvg-convert`. Si todos fallan, indica el `pip install` concreto. `--ancho-px 1600` fija el ancho de salida. Usar cairosvg cuando el SVG lleve `mask`/`foreignObject` (svglib no los soporta).

## scripts/render_mermaid.py — Mermaid→SVG/PNG

```bash
python scripts/render_mermaid.py diagrama.mmd -o diagrama.svg
python scripts/render_mermaid.py informe.md   -o diagrama.png --ancho 1600 --tema dark
```

Extrae el primer bloque ` ```mermaid ` si el origen es `.md`. Requiere `npm install -g @mermaid-js/mermaid-cli`. Temas: `default|dark|forest|neutral|base`. Errores típicos que reporta: paréntesis sin comillas (`A[texto (x)]`), subgrafos sin `end`.

## scripts/circuito.py — circuitos IEC preestablecidos (requisito: `pip install schemdraw`)

```bash
python scripts/circuito.py --tipo rc -o rc.svg          # paso bajo RC
python scripts/circuito.py --tipo rlc -o rlc.svg        # serie RLC
python scripts/circuito.py --tipo led -o led.svg --etiquetas "R=220Ω,D=D1"
python scripts/circuito.py --tipo divisor -o div.svg    # divisor de tensión con toma
python scripts/circuito.py --tipo puente -o wheat.svg   # puente de Wheatstone
```

Para PNG: la salida intermedia SVG pasa por `svg_a_raster.py` automáticamente. Si necesitas un circuito que no está en los 5 tipos, copia el bloque más cercano de `scripts/circuito.py` y modifica (no empieces en blanco).

## scripts/plano_2d.py — plano a escala desde JSON (stdlib, sin dependencias)

Spec (cm, ver ejemplo completo en la cabecera del script):

```json
{"titulo":"Apartamento 8x6","escala":"1:50","ancho":800,"alto":600,
 "habitaciones":[{"nombre":"Sala","x":0,"y":0,"w":450,"h":350},
                 {"nombre":"Dorm","x":450,"y":0,"w":350,"h":350}]}
```

```bash
python scripts/plano_2d.py plano.json -o plano.svg --abrir
```

Genera rejilla cada 50cm, muros exteriores (6px), particiones (3px), rótulos con dimensiones, cotas inferior/lateral y cajetín con escala. Para añadir mobiliario o puertas: editar el SVG resultante o el script (bloques comentados por capas).

## Cadena típica de trabajo con scripts

1. Datos/estructura → spec (CSV/JSON/MMD) en el directorio de trabajo.
2. Script → artefacto intermedio (SVG/PNG).
3. `svg_a_raster.py` si hace falta cambiar de formato o escala.
4. `editar_imagen.py info` para verificar dimensiones antes de entregar.

## scripts/video.py — FFmpeg (requiere FFmpeg; si falta: `references/instalacion.md`)

| Comando | Qué hace | Ejemplo |
|---|---|---|
| `info` | duración, resolución, fps, codecs | `python scripts/video.py info clip.mov` |
| `convertir` | cambio de extensión (mp4, webm, mov, mkv, avi, gif) | `... convertir clip.mov -o clip.mp4 --crf 23` |
| `recortar` | corte por tiempo sin re-codificar | `... recortar a.mp4 -o c.mp4 --inicio 12 --duracion 5` |
| `redimensionar` | escala (ancho par obligatorio para x264) | `... redimensionar a.mp4 -o 720p.mp4 --ancho 1280` |
| `filtro` | `grayscale, sepia, blur, brillo, contraste, denoise, denoise-fuerte, nitidez` | `... filtro a.mp4 -o l.mp4 --filtro denoise` |
| `comprimir` | CRF + preset slow | `... comprimir pesado.mp4 -o ligero.mp4 --crf 28` |
| `frames` | vídeo → secuencia PNG | `... frames a.mp4 --carpeta frames --fps 2` |
| `gif` | GIF con paleta doble pasada (sin bandas) | `... gif a.mp4 -o m.gif --fps 12 --ancho 480` |
| `ensamblar` | PNG (`frame0001.png`...) → MP4 | `... ensamblar --carpeta frames -o v.mp4 --fps 24` |
| `silenciar` / `extraer-audio` | quita/saca la pista de audio | `... extraer-audio a.mp4 -o pista.wav` |

Detalle y tablas de codecs/CRF: `references/video-edicion.md`.

## scripts/audio.py — FFmpeg

| Comando | Qué hace | Ejemplo |
|---|---|---|
| `info` | codecs, canales, bitrate | `python scripts/audio.py info tema.wav` |
| `convertir` | mp3, wav, flac, ogg, m4a, aac, opus | `... convertir t.wav -o t.mp3 --bitrate 192k` |
| `recortar` | corte por tiempo | `... recortar t.mp3 -o i.mp3 --inicio 30 --duracion 15` |
| `normalizar` | loudnorm EBU R128 **dos pasadas** (mide y aplica) | `... normalizar voz.mp3 -o v.wav --lufs -16` |
| `volumen` | ganancia en dB | `... volumen t.mp3 -o s.mp3 --db 3` |
| `silencios` | recorta bordes (y pausas con `--internos`) | `... silencios v.wav -o l.wav` |
| `extraer` / `unir` | pista de vídeo → audio / concatenar | `... unir a.mp3 b.mp3 -o c.mp3` |
| `forma` | PNG de la onda (1200x300) | `... forma t.mp3 -o onda.png` |
| `fundir` | voz sobre fondo con **ducking** automático | `... fundir voz.mp3 fondo.mp3 -o mezcla.mp3` |

LUFS objetivo y limpieza paso a paso: `references/audio-tools.md`.

## scripts/convertir.py — cambio de extensión universal

```bash
python scripts/convertir.py foto.png  -o foto.webp --calidad 90
python scripts/convertir.py logo.svg  -o logo.png --escala 2
python scripts/convertir.py clip.mov  -o clip.mp4 --crf 20
python scripts/convertir.py gif anim.gif -o anim.mp4
python scripts/convertir.py cancion.wav -o cancion.mp3 --bitrate 192k
```

Enruta por la extensión de ORIGEN: imagen→Pillow, svg→`svg_a_raster.py`, vídeo→`video.py`, audio→`audio.py`. Misma extensión = error (no re-codifiques sin motivo).

## scripts/plot3d.py — figuras 3D (matplotlib+numpy)

```bash
python scripts/plot3d.py superficie -o s.png --titulo "Onda" --gif s.gif   # + órbita 360°
python scripts/plot3d.py superficie -o f.png --func "np.sin(x)*np.cos(y)"  # función propia
python scripts/plot3d.py malla -o m.png --func "x*y"                       # wireframe
python scripts/plot3d.py nube puntos.csv --x px --y py --z pz -o n.png --ejes "X,Y,Z"
python scripts/plot3d.py barras datos.csv --x cat --y val -o b.png --transparente
```

Cámara (`--elev/--azim`), GIF (`--frames/--fps`) y calidad de render: `references/planos-3d.md`.
