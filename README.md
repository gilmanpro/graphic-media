# graphic-media

> **Super skill open source de dibujo y visualización para agentes de IA**: diagramas, planos 2D/3D, gráficos de datos, circuitos eléctricos, arte SVG, posters, y edición de imagen, vídeo y audio — todo autocontenido, con **11 scripts Python probados** y **21 referencias** sin depender de documentación externa.

[![Python](https://img.shields.io/badge/Python-3.10%2B-3776AB?style=flat-square&logo=python&logoColor=white)](https://www.python.org/)
[![Agent Skills](https://img.shields.io/badge/formato-Agent%20Skills-06B6D4?style=flat-square)](https://agentskills.io/)
[![FFmpeg](https://img.shields.io/badge/v%C3%ADdeo%20y%20audio-FFmpeg-7E1E7E?style=flat-square)](https://ffmpeg.org/)
[![MIT](https://img.shields.io/badge/License-MIT-10B981?style=flat-square)](LICENSE.txt)

## El problema que resuelve

Cuando un agente tiene que «dibujar» algo, el resultado depende de que el modelo **improvise**: se inventa un snippet de matplotlib, mezcla Mermaid con SVG a mitad de diagrama, entrega un PNG sin verificar o reinventa el mismo helper de Pillow cada sesión. graphic-media elimina esa improvisación con un **enrutador claro** (`petición → sección → referencia → script → verificación`) y scripts que resuelven en vez de delegar excepciones al modelo.

## Qué incluye

| Dominio | Qué hay |
|---|---|
| Diagramas | Mermaid, PlantUML, Graphviz DOT, BPMN, C4, draw.io/Excalidraw, estilo boceto |
| Gráficos de datos | `grafico.py` (CSV → PNG/SVG), `histograma_animado.py` (GIF/MP4) |
| Planos e ingeniería | `plano_2d.py` (escala, cotas, cajetín), cotas ISO, DXF con `ezdxf` |
| Circuitos eléctricos | `circuito.py` (RC, RLC, LED, divisor, Wheatstone, símbolos IEC) |
| 3D | `plot3d.py` (superficie, malla, nube, barras + GIF orbitando) |
| Arte vectorial SVG | paths, filtros, animación, optimización, `svg_a_raster.py` |
| Posters y arte | flujo filosofía → lienzo + 46 fuentes OFL en `canvas-fonts/` |
| Imagen | `editar_imagen.py` (recorte, filtros, transparencia, GIF, contacto) |
| Vídeo | `video.py` (convertir, recortar, denoise, comprimir, frames ↔ GIF) |
| Audio | `audio.py` (convertir, loudnorm EBU R128, silencios, ducking, waveform) |
| Conversión | `convertir.py` (imagen/vídeo/audio/svg en un solo comando) |
| Instalación de herramientas | `references/instalacion.md`: una vez por equipo, en el PATH |

## Instalación

```bash
npx skills add gilmanpro/graphic-media
```

O a mano:

```bash
git clone https://github.com/gilmanpro/graphic-media.git ~/.agents/skills/graphic-media
```

Núcleo: `pip install pillow matplotlib`. FFmpeg, Graphviz, mermaid-cli y demás se instalan **una sola vez por equipo** siguiendo `references/instalacion.md`; los scripts avisan con el comando exacto cuando falta algo.

## Estructura

```
graphic-media/
├── SKILL.md              # enrutador + conocimiento embebido (<500 líneas)
├── references/           # 21 guías autocontenidas (diagramas, planos, vídeo, audio, 3D...)
├── scripts/              # 11 CLIs probados funcionalmente
├── evals/                # activación (17 queries) y rendimiento (10 evals)
├── canvas-fonts/         # 46 fuentes OFL
└── LICENSE.txt           # MIT
```

Diseño: **autocontenida** (nunca carga otras skills para hacer su tarea), **sin URLs de documentación externa** (todo embebido) y **verificada** (`quick_validate` + auditoría de seguridad anti-skill-maliciosa).

## Mejora esta skill

**Esta skill crece con peticiones concretas.** Si algo falta o se puede hacer mejor, tu Issue es el camino:

- **¿Falta una capacidad?** → [Solicitud de mejora](https://github.com/gilmanpro/graphic-media/issues/new?template=solicitud-mejora.yml): describe el tipo de dibujo/edición que necesitas, el formato de salida esperado y un ejemplo de uso real.
- **¿Un script falla?** → [Bug de script](https://github.com/gilmanpro/graphic-media/issues/new?template=bug-script.yml): comando ejecutado, salida esperada y error obtenido.
- **¿Prefieres código?** → Pull requests bienvenidos: scripts nuevos **probados**, referencias embebidas y tipos de diagrama. Sigue las reglas de la skill: autocontenida, sin URLs externas, sin delegar a otras skills.

## Licencia

[MIT](LICENSE.txt) — © [Gilberto Castillo](https://github.com/gilmanpro). Sin cláusulas de uso comercial; las 46 fuentes de `canvas-fonts/` son Open Font License (los `.OFL.txt` van junto a cada `.ttf`).
