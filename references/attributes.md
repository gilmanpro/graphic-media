# Referencia de Atributos SVG

Catálogo de los atributos SVG más importantes basado en SVG 2 y MDN.

## Atributos de Geometría (también propiedades CSS en SVG 2)

| Atributo | Elementos | Descripción |
|---|---|---|
| `x`, `y` | rect, image, text, tspan, use | Posición |
| `width`, `height` | rect, image, svg | Tamaño |
| `cx`, `cy` | circle, ellipse | Centro |
| `r` | circle | Radio |
| `rx`, `ry` | rect, ellipse | Radio horizontal/vertical |
| `x1`, `y1`, `x2`, `y2` | line | Puntos de inicio/fin |

> **SVG 2:** Todos estos son ahora propiedades CSS oficiales. Puedes hacer `transition: r 400ms;` en un círculo.

## Atributos de Coordenadas y Viewport

| Atributo | Descripción |
|---|---|
| `viewBox="minX minY width height"` | Sistema de coordenadas interno |
| `preserveAspectRatio="align meetOrSlice"` | Cómo escalar |
| `width`, `height` | Tamaño del viewport SVG |

### Valores de preserveAspectRatio

**Align:**
- `xMinYMin` — esquina superior izquierda
- `xMidYMin` — centro superior
- `xMaxYMin` — esquina superior derecha
- `xMidYMid` — centro (default)
- `xMaxYMax` — esquina inferior derecha

**Opciones de escala:**
- `meet` — escala para que quepa (letterbox) — default
- `slice` — escala para cubrir todo (crop)
- `none` — estira sin preservar aspecto

## Atributos de Presentación (CSS Properties)

### Fill (Relleno)

| Atributo | Valores | Default |
|---|---|---|
| `fill` | color, `url(#id)`, `none`, `currentColor` | `black` |
| `fill-opacity` | 0-1 | `1` |
| `fill-rule` | `nonzero`, `evenodd` | `nonzero` |

- **nonzero**: determina si un punto está dentro/ fuera contando intersecciones con direcciones
- **evenodd**: cuenta intersecciones sin importar dirección; alterna dentro/fuera en cada cruce

### Stroke (Trazo)

| Atributo | Valores | Default |
|---|---|---|
| `stroke` | color, `none`, `url(#gradient)` | `none` |
| `stroke-width` | número | `1` |
| `stroke-opacity` | 0-1 | `1` |
| `stroke-linecap` | `butt`, `round`, `square` | `butt` |
| `stroke-linejoin` | `miter`, `round`, `bevel` | `miter` |
| `stroke-miterlimit` | número ≥ 1 | `4` |
| `stroke-dasharray` | serie de números | `none` |
| `stroke-dashoffset` | número | `0` |
| `paint-order` | `normal`, `fill`, `stroke` | `normal` |

**Nota sobre stroke:** Se dibuja **centrado** sobre el path. No se puede elegir interior/exterior. Esto significa que un path en el borde del viewBox puede tener el stroke recortado.

### stroke-linecap

```
butt:   ———  (corte recto exacto)
round:  ╭━━╮ (extremo redondeado)
square: ———  (se extiende medio stroke-width)
```

### stroke-linejoin

```
miter: vértice en punta (se convierte en bevel si excede miterlimit)
round: vértice redondeado
bevel: vértice cortado en bisel
```

## Atributos de Texto

| Atributo | Descripción |
|---|---|
| `font-family` | Fuente del texto |
| `font-size` | Tamaño (unidades o número sin unidad = usuario) |
| `font-weight` | Peso (100-900, bold, normal) |
| `font-style` | normal, italic, oblique |
| `text-anchor` | `start`, `middle`, `end` |
| `dominant-baseline` | `auto`, `middle`, `hanging`, `central`, `text-before-edge` |
| `letter-spacing` | Espaciado entre letras |
| `word-spacing` | Espaciado entre palabras |
| `textLength` | Forzar longitud del texto |
| `lengthAdjust` | `spacing`, `spacingAndGlyphs` |
| `direction` | `ltr`, `rtl` |

## Atributos de Transformación

| Atributo | Descripción |
|---|---|
| `transform` | `translate(x,y)`, `rotate(a)`, `scale(x,y)`, `skewX(a)`, `skewY(a)`, `matrix(a,b,c,d,e,f)` |
| `transform-origin` | Origen de la transformación (SVG 2) |
| `vector-effect` | `none`, `non-scaling-stroke` (el stroke no escala) |

## Atributos de Animación (SMIL)

| Atributo | Elemento animate | Descripción |
|---|---|---|
| `attributeName` | Todos | Atributo a animar |
| `from` | animate | Valor inicial |
| `to` | animate | Valor final |
| `values` | animate | Lista de valores intermedios |
| `dur` | animate | Duración |
| `repeatCount` | animate | Número de repeticiones (`indefinite`) |
| `fill` | animate | `freeze` (mantener estado final) |
| `calcMode` | animate | `linear`, `discrete`, `paced`, `spline` |

## Atributos de Filtro

| Atributo | Descripción |
|---|---|
| `filterUnits` | `objectBoundingBox` o `userSpaceOnUse` |
| `x`, `y`, `width`, `height` | Bounds del filtro (default -10% a 120%) |
| `stdDeviation` | feGaussianBlur |
| `in`, `in2` | `SourceGraphic`, `SourceAlpha`, `BackgroundImage`, resultado previo |
| `result` | Nombre del resultado para encadenar filtros |
| `type` | feColorMatrix: `matrix`, `saturate`, `hueRotate`, `luminanceToAlpha` |

## Atributos de Estructura

| Atributo | Descripción |
|---|---|
| `id` | Identificador único |
| `class` | Clase CSS |
| `style` | Estilo inline |
| `data-*` | Atributos personalizados |
| `lang` / `xml:lang` | Idioma |
| `tabindex` | Orden de tabulación |
| `role` | ARIA role (ej: `img`) |
| `aria-labelledby` | IDs de elementos que etiquetan este elemento |
| `aria-hidden` | Ocultar de lectores de pantalla |

## Atributos de Enlace

| Atributo | Elemento a | Descripción |
|---|---|---|
| `href` | a, use, image, textPath | URL de destino |
| `target` | a | `_self`, `_blank`, `_parent`, `_top` |
| `download` | a | Forzar descarga |

## Atributos de Imagen

| Atributo | Elemento image | Descripción |
|---|---|---|
| `href` | image | URL de la imagen |
| `crossorigin` | image | `anonymous`, `use-credentials` |
| `decoding` | image | `sync`, `async`, `auto` |
