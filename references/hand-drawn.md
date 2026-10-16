# Diagramas estilo boceto a mano alzada (hand-drawn)

Aspecto de pizarra/diseño temprano: trazos irregulares, sin pulir, ideales para workshops, validación de concepto y bocetos.

Índice: [1 Cuándo](#1-cuándo) · [2 Cómo lograrlo](#2-cómo-lograrlo) · [3 Reglas](#3-reglas)

## 1 Cuándo

- Boceto de flujo para discutir («no lo defiendas como diseño final»).
- Wireframe de concepto, mapa mental de lluvia de ideas.
- Cuando el entregable pida look de pizarra/servilleta.

No usar para documentación formal ni diagramas de arquitectura de producción (ahí cuenta el acabado).

## 2 Cómo lograrlo

**Vía A — Mermaid (si el destino es Markdown):** Mermaid no tiene tema hand-drawn nativo; el efecto se logra al renderizar con filtro SVG (Vía C) sobre el SVG de mmdc.

**Vía B — Excalidraw JSON (el camino directo):** los trazos ya salen a mano alzada. Esqueleto `.excalidraw`:

```json
{
  "type": "excalidraw",
  "version": 2,
  "source": "local",
  "elements": [
    {"type": "rectangle", "id": "n1", "x": 100, "y": 100, "width": 160, "height": 80,
     "angle": 0, "strokeColor": "#1e1e1e", "backgroundColor": "#ffec99",
     "fillStyle": "hachure", "strokeWidth": 2, "roughness": 1,
     "seed": 12345, "versionNonce": 1, "isDeleted": false, "groupIds": []},
    {"type": "text", "id": "t1", "x": 130, "y": 130, "text": "Pedido",
     "fontSize": 20, "strokeColor": "#1e1e1e", "seed": 54321,
     "versionNonce": 2, "isDeleted": false, "groupIds": []}
  ],
  "appState": {"viewBackgroundColor": "#ffffff"},
  "files": {}
}
```

Claves: `roughness: 1` (trazo irregular; 0 = recto), `fillStyle: "hachure"` (trama en vez de relleno plano), `seed` distinto por elemento (si dos comparten seed, el mismo temblor delata la plantilla). Abrir en excalidraw.com.

**Vía C — Filtro sobre cualquier SVG** (Mermaid, draw.io exportado, SVG propio):

```xml
<defs>
  <filter id="mano">
    <feTurbulence type="fractalNoise" baseFrequency="0.02" numOctaves="3" result="ruido"/>
    <feDisplacementMap in="SourceGraphic" in2="ruido" scale="4"
                       xChannelSelector="R" yChannelSelector="G"/>
  </filter>
</defs>
<g filter="url(#mano)"> ... todo el diagrama ... </g>
```

`scale="3..6"` da el temblor justo; >8 rompe legibilidad. Alternativa: línea con puntos de control ligeramente desviados (±2u) en vez de rectas perfectas.

## 3 Reglas

- Un solo estilo de boceto en todo el diagrama (todos temblorosos o ninguno).
- Relleno `hachure`/tinta, no degradados; paleta de rotuladores (máx. 5 colores).
- Flechas con punta simple dibujada, no ornamentos; texto con tipografía redondeada/handwriting si hay fuente disponible.
- El efecto jamás compromete la lectura: si con el filtro no se leen las etiquetas, baja `scale`.
- Anti-patrones: boceto a la vez que contenido definitivo (usa hand-drawn solo para borradores); sombras realistas (contradice el estilo); mezclar hand-drawn con iconos de librería pulida.
