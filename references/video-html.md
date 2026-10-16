# Video desde HTML — composiciones motion a MP4

Convertir dibujos/gráficos en video: se escribe un HTML de composición con atributos de tiempo y se renderiza a MP4 de forma **determinista** (mismo entrada = mismos frames = mismo vídeo). El motor (si está disponible en el entorno) es la CLI `hyperframes` (Node 22+ y FFmpeg); si no, el fallback es GIF con matplotlib (§1.2 del SKILL.md).

Índice: [1 Contrato](#1-contrato-de-composición) · [2 Animación seekable](#2-animación-seekable) · [3 Bucle de producción](#3-bucle-de-producción) · [4 Tipos](#4-tipos-de-motion-graphic) · [5 frame.md](#5-frame-md--traducir-el-diseño-a-cámara) · [6 Fallbacks](#6-sin-motor-de-video)

## 1 Contrato de composición

Un `index.html` sin build se reproduce tal cual. Estructura base copiable:

```html
<div id="stage" data-composition-id="demo"
     data-start="0" data-width="1920" data-height="1080">

  <video class="clip" data-start="0" data-duration="6"
         data-track-index="0" src="fondo.mp4" muted playsinline></video>

  <h1 class="clip" data-start="1" data-duration="4" data-track-index="1">Lanzamiento</h1>

  <audio data-start="0" data-duration="6" data-track-index="2"
         data-volume="0.5" src="musica.wav"></audio>

  <script src="ruta-a-gsap.min.js"></script>
  <script>
    const tl = gsap.timeline({ paused: true });
    tl.from("#stage h1", { opacity: 0, y: 40, duration: 0.8 }, 1);
    window.__timelines = window.__timelines || {};
    window.__timelines.demo = tl;
  </script>
</div>
```

Reglas del contrato:

| Atributo | Significado |
|---|---|
| `class="clip"` | Elemento con línea de tiempo propia |
| `data-start` / `data-duration` | Entrada y duración en segundos (compuestos en el tiempo global) |
| `data-track-index` | Pista (0 = base, superiores encima) |
| `data-volume` | Volumen de audio 0–1 |
| `data-composition-id` | Debe coincidir con la clave de `window.__timelines` |
| `data-width` / `data-height` | Resolución de salida (1920x1080, 1080x1920 vertical, 1080x1080 cuadrado) |

## 2 Animación seekable

El motor recorre frame a frame saltando a cualquier instante: **la animación debe poder posicionarse en el tiempo**, no avanzar sola.

- **Sí**: GSAP `gsap.timeline({ paused: true })` publicado en `window.__timelines[id]`; CSS `@keyframes`/`animation` (seekables); WAAPI con `timeline.playbackRate = 0` + `currentTime`; Lottie/Three.js/Anime.js con su adaptador de frame.
- **No** (rompe la búsqueda): `setTimeout`/`setInterval`, `requestAnimationFrame` con reloj propio, `Date.now()` en la lógica de la animación, autoplay que depende de la reproducción en vivo.
- Toda animación nace en un instante `t` del timeline (`tl.from(..., t)`), nunca «al cargar la página».
- Duración del clip = duración de su timeline; el audio se corta con `data-duration` (no con fade improvisado).

## 3 Bucle de producción

Secuencia (igual que el flujo base, aplicado a video):

1. **Plan de escenas**: lista de planos con tiempos (`P1 0-3s título · P2 3-7s gráfico · P3 7-10s logo`) y resolución/aspecto.
2. **HTML válido**: stage + clips con `data-*` + tracks ordenados.
3. **Animaciones seekables**: timelines pausados publicados; easing suave (`power2.out`), nada de tiempos de pared.
4. **Media congelada**: vídeo/fuentes/audio locales y fijos (un asset que cambie rompe la reproducción idéntica).
5. **Lint + preview**: `npx hyperframes lint` / `npx hyperframes preview` (recarga en navegador).
6. **Render**: `npx hyperframes render` → MP4 (motor determinista: Chrome busca cada frame, FFmpeg codifica).

```bash
npx hyperframes init mi-video      # scaffolding (Node 22+ y FFmpeg en el PATH)
cd mi-video                        # editar index.html
npx hyperframes preview            # vista previa en navegador
npx hyperframes render             # MP4 final
```

Si solo falta FFmpeg: instalar (`winget install Gyan.FFmpeg` en Windows) y reintentar; si no hay Node 22+ → §6.

## 4 Tipos de motion graphic

| Tipo | Qué es | Duración típica |
|---|---|---|
| Kinetic type | Tipografía que entra/mueve por el beat | 5-10s |
| Stat/chart hit | Dato o gráfico que aparece con impacto | 3-8s |
| Logo sting | Entrada de marca al final | 2-5s |
| Lower-third | Bajada de nombre/rol sobre entrevista | 3-6s |
| Tweet/headline animado | Cabecera que se revela | 5-10s |
| Título con fondo de vídeo | Portada sobre clip de fondo | 6-15s |

Reglas comunes: un mensaje por escena; el dato manda (el número en grande, la explicación pequeña); corte o crossfade entre escenas; texto 100% legible a 1080p (mín. ~40px para títulos); sin superposiciones en el último frame.

## 5 frame.md — traducir el diseño a cámara

Un sistema de diseño web no está escrito para la cámara: antes de componer, invierte las reglas al formato de frame:

- **Misma paleta y tipografía**, pero escaladas a tamaño de pantalla (lo que en web es 16px, en 1920x1080 es ~40-64px).
- **Los números salen del guion**: los tiempos de cada elemento salen de lo que hay que decir, no de ajustes ojo.
- **Sin cromo web**: barras de scroll, botones, badges de UI no existen en cámara.
- Guardar el resultado como `frame.md` y reutilizarlo en todas las piezas de la misma marca.

## 6 Sin motor de video

Si no hay Node/FFmpeg/red para instalar:

1. **GIF/PNG**: `scripts/histograma_animado.py` (datos), o un timeline propio de `FuncAnimation` para cualquier secuencia de frames.
2. **Frames sueltos → vídeo**: generar N frames PNG con matplotlib/Pillow y ensamblar si aparece ffmpeg después (`ffmpeg -framerate 8 -i frame%03d.png out.mp4`).
3. **SVG+CSS animado**: entregar el HTML/SVG animado (se reproduce en navegador) y avisar de que el MP4 requiere el motor de video.
