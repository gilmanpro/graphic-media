# Cómo hacer cada trabajo — secuencia paso a paso

Regla general de 4 pasos para TODA tarea: **(1) spec** (JSON/CSV/MMD o boceto de estructura) → **(2) ejecuta el script** → **(3) convierte/escala** si hace falta → **(4) verifica** con `editar_imagen.py info`. Aquí está la secuencia concreta por tipo de encargo.

Índice: [1 Gráfico de datos](#1-gráfico-de-datos) · [2 Diagrama de texto](#2-diagrama-de-texto-mermaid) · [3 Arquitectura cloud](#3-arquitectura-cloud) · [4 Editable](#4-diagrama-editable-drawio--excalidraw) · [5 Infografía](#5-infografía-htmlsvg) · [6 Circuito](#6-circuito-eléctrico) · [7 Plano](#7-plano-2d) · [8 Logo/icono SVG](#8-logo--icono-svg) · [9 Poster](#9-poster-o-arte) · [10 Edición](#10-edición-de-imágenes-en-lote) · [11 Animación](#11-animación) · [12 Conversión](#12-conversión-de-formatos) · [13 Vídeo/audio](#13-vídeo-y-audio)

## 1 Gráfico de datos

1. Lleva los datos a CSV con encabezados (`mes,ventas` / una columna por serie).
2. `python scripts/grafico.py datos.csv --tipo line --x fecha --y visitas,conv --titulo "..." -o grafico.png`
3. Si piden fondo transparente: `--transparente`; si piden vectorial: `--svg`.
4. Verifica: `python scripts/editar_imagen.py info grafico.png`.

Errores típicos: columna no numérica (usa `.` como decimal), barras con >12 categorías (el script ya rota etiquetas), series sin unidades en el eje (añade `--ylabel`).

## 2 Diagrama de texto (Mermaid)

1. Escribe `d.mmd` con UN solo diagrama (`flowchart`, `sequenceDiagram`, `erDiagram`, `stateDiagram-v2`, `gantt`, `mindmap`).
2. `python scripts/render_mermaid.py d.mmd -o d.svg` (o `-o d.png --ancho 1600`).
3. Si vive en un `.md`, pasa el Markdown directamente: el script extrae el primer bloque.
4. Sintaxis segura: etiquetas con paréntesis entre comillas `A["texto (x)"]`; subgrafos cerrados con `end`; flechas `-->` con texto `-- etiqueta -->`.

## 3 Arquitectura cloud

1. Escribe el script (esqueleto en SKILL.md §1.3): nodos = servicios, `>>` = dependencia.
2. Comprueba Graphviz (`dot -V`); si falta: `winget install Graphviz.Graphviz` (Windows).
3. `python arquitectura.py` → PNG junto al script.
4. Para vectorial: `show=False, outformat="png"` cambia a generar y luego `dot -Tsvg web.dot -o web.svg` si exportas DOT.

Convención de etiquetas: componente + rol (`"api REST"`), versión solo si importa al lector.

## 4 Diagrama editable (draw.io / Excalidraw)

Elige cuando vayan a REABRIRLO. No hay script: plantilla mínima copiable.

**draw.io** — guardar como `d.drawio` y abrir en app.diagrams.net:

```xml
<mxfile>
  <diagram name="Página 1" id="p1">
    <mxGraphModel dx="800" dy="600" grid="1" gridSize="10">
      <root>
        <mxCell id="0"/>
        <mxCell id="1" parent="0"/>
        <mxCell id="n1" value="Pedido" style="rounded=1;whiteSpace=wrap;html=1;"
                 vertex="1" parent="1"><mxGeometry x="40" y="40" width="120" height="60"/></mxCell>
        <mxCell id="n2" value="Enviar" style="rounded=1;whiteSpace=wrap;html=1;"
                 vertex="1" parent="1"><mxGeometry x="240" y="40" width="120" height="60"/></mxCell>
        <mxCell id="e1" style="edgeStyle=orthogonalEdgeStyle;" edge="1" parent="1" source="n1" target="n2"/>
      </root>
    </mxGraphModel>
  </diagram>
</mxfile>
```

Reglas: nodos en rejilla de 10; una arista por `mxCell` con `source`/`target`; estilos separados por `;`.

**Excalidraw** — guardar como `d.excalidraw` y abrir en excalidraw.com: JSON con `type:"excalidraw"`, `elements: []` (rectángulos `type:"rectangle"`, texto `type:"text"`, flechas `type:"arrow"` con `startBinding/endBinding`), `appState: {"viewBackgroundColor":"#ffffff"}`. Mantén ids cortos y únicos.

## 5 Infografía (HTML+SVG)

Un único `.html` autocontenido (sin CDNs) que se abre en navegador y se captura a PNG:

```html
<meta charset="utf-8">
<style>body{font-family:system-ui;margin:0;background:#fff}
.card{width:800px;padding:32px;box-sizing:border-box}
.kpi{font:700 40px system-ui;color:#4F46E5}
.lbl{font:14px system-ui;color:#6B7280}</style>
<div class="card">
  <svg viewBox="0 0 736 220" width="100%">
    <!-- barras: x = i*92, alto = valor*4 -->
    <rect x="0"   y="140" width="80" height="80"  fill="#4F46E5"/>
    <text x="40"  y="130" text-anchor="middle" font-size="14">Ene</text>
  </svg>
  <div class="kpi">+32%</div><div class="lbl">crecimiento Q1</div>
</div>
```

Reglas: 2 acentos + 2 neutros; una tipografía (system-ui); KPIs en cifras grandes; captura con cualquier screenshot a 800px de ancho (o convierte con `svg_a_raster.py` si exportas solo el SVG).

## 6 Circuito eléctrico

1. `python scripts/circuito.py --tipo rc|rlc|led|divisor|puente -o c.svg --etiquetas "R=10kΩ,C=100nF"`.
2. Si el circuito no está en los 5 tipos: copia el bloque más cercante de `scripts/circuito.py` y añade/quita elementos (referencia de elementos: `Resistor, Capacitor, Inductor, Diode, LED, Battery, Switch, Ground, Lamp, Relay, Motor`).
3. A mano solo si necesitas control de página: símbolos IEC (resistencia = rectángulo), rejilla 10u, cables a 90°, nodos con `circle r="3"`.

## 7 Plano 2D

1. Mide en cm y escribe `plano.json` (formato en `scripts/plano_2d.py` y en `references/scripts.md`).
2. `python scripts/plano_2d.py plano.json -o plano.svg --abrir` → revisa en el navegador.
3. Añade lo que falte editando el SVG: mobiliario (`<rect>` finos), puertas (arco: `<path d="M... a...">`), ventanas (líneas dobles en el muro).
4. Para PNG: `svg_a_raster.py plano.svg -o plano.png --escala 2`.
5. Si piden AutoCAD: `ezdxf` con capas `MUROS/COTAS/TEXTO/MOBILIARIO` en mm.

Errores típicos: cambiar la escala entre vistas (prohibido); cotas pegadas al muro (mínimo 8u de separación); olvidar el cajetín con `E:`.

## 8 Logo / icono SVG

1. Escribe el SVG con `viewBox` + `xmlns` + `role/title/desc`; formas en `<defs>` si se repiten.
2. Iconos 24x24: `stroke-width="2"`, `stroke-linecap="round"`, `fill="none"`, un solo color (`#666` o currentColor).
3. Optimiza: `npx svgo logo.svg`.
4. Raster: `python scripts/svg_a_raster.py logo.svg -o logo.png --escala 4` (logos: PNG @2x–@4x para pantallas densas).
5. Anti-patrones: stroke que toca el borde del viewBox (recorta 50% del grosor); `viewBox` ausente; colores sin contraste en fondo oscuro.

## 9 Poster o arte

1. Filosofía `.md`: nombre del movimiento + 4-6 párrafos (espacio, color, escala, composición, jerarquía).
2. Traduce cada párrafo a decisión de lienzo (color, tipografía de `canvas-fonts/`, ritmo).
3. Lienzo: HTML+SVG de página única (mismo patrón que §5) o script Pillow/Matplotlib si el arte es generativo; texto mínimo, nada fuera del margen.
4. Exporta: captura del navegador (PNG) o `svg_a_raster.py` (PDF vectorial).
5. Refina SIN añadir: segunda pasada sobre el mismo código (espaciado, color, tipografía).

## 10 Edición de imágenes en lote

```bash
# 1) diagnóstico
python scripts/editar_imagen.py info *.jpg
# 2) tareas típicas (siempre salida nueva, jamás sobre el original)
python scripts/editar_imagen.py redimensionar in.jpg out.jpg --ancho 1600
python scripts/editar_imagen.py filtro in.jpg out.jpg --filtro contrast
python scripts/editar_imagen.py transparencia logo.png limpio.png --color "#ffffff" --tolerancia 40
# 3) revisión visual en bloque
python scripts/editar_imagen.py contacto qa.jpg out/*.jpg --columnas 4
# 4) verificación final
python scripts/editar_imagen.py info out/*.jpg
```

Fondos con degradado → no funciona `transparencia` por color: segmenta (umbral por canal) o reencuadra.

## 11 Animación

- **Histograma/dato animado**: `python scripts/histograma_animado.py datos.csv --columna valor -o a.gif`.
- **Dibujo a video** (boceto): sigue `references/animacion-ia.md` — prepara el dibujo (pose legible, fondo simple), describe la acción en orden con cámara y estilo, vistas de referencia para coherencia, storyboard de 2-3 bocetos.
- **GIF desde frames** (p.ej. renders): `python scripts/editar_imagen.py gif out.gif frames/*.png --duracion 200`.

## 12 Conversión de formatos

Punto único: **`python scripts/convertir.py in.ext -o out.ext`** (detecta imagen/vídeo/audio/svg y enruta).

| Origen → Destino | Comando |
|---|---|
| Cualquier imagen → otra extensión | `python scripts/convertir.py a.png -o a.webp --calidad 90` |
| SVG → PNG/PDF | `python scripts/convertir.py a.svg -o a.png --escala 2` |
| Vídeo → mp4/webm/mov/mkv/avi/gif | `python scripts/convertir.py a.mov -o a.mp4 --crf 23` |
| Audio → mp3/wav/flac/ogg/m4a/opus | `python scripts/convertir.py a.wav -o a.mp3 --bitrate 192k` |
| GIF animado → vídeo | `python scripts/convertir.py a.gif -o a.mp4` |
| Mermaid → SVG/PNG | `python scripts/render_mermaid.py in.mmd -o out.svg` |
| DXF → PNG | `inkscape in.dxf -o out.png` |
| SVG → DXF | no fiable con curvas: regenera desde el modelo con `ezdxf` |

Regla: nunca recodificar «por probar» (MP4→MP4 = doble pérdida); si el destino coincide con el origen, no toques el fichero.

## 13 Vídeo y audio

1. **Diagnóstico**: `python scripts/video.py info a.mov` · `python scripts/audio.py info a.wav`.
2. **Vídeo típico**: `convertir a.mov -o a.mp4` → si hay grano: `filtro --filtro denoise` → si pesa: `comprimir --crf 28` → si hace falta cortar: `recortar --inicio --duracion` (corte clave a clave, sin pérdida).
3. **Audio típico**: `convertir` al formato destino → `silencios` si arranca/termina en blanco → `normalizar --lufs -16` **al final** (la última pasada manda) → `forma` para verificar la onda visualmente.
4. **Voz sobre música**: `fundir voz.mp3 fondo.mp3 -o mezcla.mp3` (ducking automático).
5. **Frames ↔ vídeo**: `video.py frames` para inspección/corrección puntual con `editar_imagen.py`, `ensamblar` para volver a vídeo (mismo tamaño de PNG, mismo fps).
6. Verificar siempre con `info` (duración/codec esperados) antes de entregar.

Detalle: `references/video-edicion.md` y `references/audio-tools.md`. Si falta FFmpeg: `references/instalacion.md`.
