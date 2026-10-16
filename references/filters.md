# Filtros SVG

Guía de efectos de filtro SVG basada en SVG 2 y MDN.

## Sintaxis Básica

```xml
<defs>
  <filter id="mi-filtro" x="-20%" y="-20%" width="140%" height="140%">
    <!-- primitivas de filtro aquí -->
  </filter>
</defs>
<rect filter="url(#mi-filtro)" ... />
```

> ⚠️ **Bounds del filtro**: Por defecto `x="-10%" y="-10%" width="120%" height="120%"`. Si el efecto se recorta (común con sombras y desenfoques), aumenta estos valores.

## Primitivas de Filtro

### feGaussianBlur — Desenfoque

```xml
<filter id="blur">
  <feGaussianBlur stdDeviation="3" />
</filter>
```

`stdDeviation` puede ser 1 valor (x=y) o 2 valores (horizontal, vertical).

### feDropShadow — Sombra

```xml
<filter id="sombra" x="-20%" y="-20%" width="140%" height="140%">
  <feDropShadow dx="2" dy="4" stdDeviation="4"
                flood-color="#000000" flood-opacity="0.3" />
</filter>
```

Es un atajo que combina feOffset + feGaussianBlur + feMerge.

### feOffset — Desplazamiento

```xml
<filter id="offset">
  <feOffset dx="5" dy="5" />
</filter>
```

### feColorMatrix — Transformación de color

```xml
<!-- Escala de grises -->
<filter id="grises">
  <feColorMatrix type="saturate" values="0" />
</filter>

<!-- Sepia -->
<filter id="sepia">
  <feColorMatrix type="matrix" values="
    0.39 0.69 0.27 0 0
    0.35 0.59 0.23 0 0
    0.27 0.47 0.19 0 0
    0    0    0    1 0" />
</filter>

<!-- Brillo/contraste (con feComponentTransfer) -->
<filter id="brillo">
  <feComponentTransfer>
    <feFuncR type="linear" slope="1.2" />
    <feFuncG type="linear" slope="1.2" />
    <feFuncB type="linear" slope="1.2" />
  </feComponentTransfer>
</filter>
```

### feBlend — Mezcla

```xml
<filter id="mezcla">
  <feImage href="textura.png" result="textura" />
  <feBlend in="SourceGraphic" in2="textura" mode="multiply" />
</filter>
```

Modos: `normal`, `multiply`, `screen`, `darken`, `lighten`, `overlay`

### feMerge — Combinar capas

```xml
<filter id="sombra-manual">
  <feOffset dx="2" dy="2" in="SourceAlpha" result="offset" />
  <feGaussianBlur stdDeviation="3" in="offset" result="blur" />
  <feFlood flood-color="#000" flood-opacity="0.3" result="color" />
  <feComposite in="color" in2="blur" operator="in" result="sombra" />
  <feMerge>
    <feMergeNode in="sombra" />
    <feMergeNode in="SourceGraphic" />
  </feMerge>
</filter>
```

### feMorphology — Engrosar/adelgazar

```xml
<filter id="engrosar">
  <feMorphology operator="dilate" radius="2" />
</filter>
<filter id="adelgazar">
  <feMorphology operator="erode" radius="1" />
</filter>
```

### feTurbulence — Textura procedural

```xml
<filter id="niebla">
  <feTurbulence type="fractalNoise" baseFrequency="0.015"
                numOctaves="3" result="ruido" />
  <feColorMatrix type="saturate" values="0" in="ruido" result="gris" />
  <feBlend in="SourceGraphic" in2="gris" mode="screen" />
</filter>
```

## Encadenamiento de Primitivas

Las primitivas se encadenan usando `in` y `result`:

```
SourceGraphic → feOffset → feGaussianBlur → feMerge → resultado final
                     ↓                          ↓
               SourceAlpha (para sombras)   SourceGraphic
```

Valores especiales de `in`:
- `SourceGraphic` — el gráfico original
- `SourceAlpha` — el canal alpha del gráfico
- `BackgroundImage` — el fondo detrás del elemento
- `FillPaint`, `StrokePaint` — el fill/stroke como imagen

## Ejemplos Prácticos

### Glow (resplandor)

```xml
<filter id="glow" x="-50%" y="-50%" width="200%" height="200%">
  <feGaussianBlur stdDeviation="4" result="blur" />
  <feMerge>
    <feMergeNode in="blur" />
    <feMergeNode in="blur" /> <!-- doble para intensificar -->
    <feMergeNode in="SourceGraphic" />
  </feMerge>
</filter>
```

### Duotono

```xml
<filter id="duotono" color-interpolation-filters="sRGB">
  <feColorMatrix type="matrix" values="
    0.5 0.5 0.5 0 0
    0.3 0.3 0.3 0 0
    0.1 0.1 0.1 0 0
    0   0   0   1 0" />
</filter>
```

### Borde interior (bevel)

```xml
<filter id="bevel">
  <feGaussianBlur stdDeviation="2" in="SourceAlpha" result="blur" />
  <feSpecularLighting in="blur" surfaceScale="3"
                      specularConstant="0.8" specularExponent="20"
                      lighting-color="#ffffff" result="spec">
    <fePointLight x="50%" y="30%" z="20" />
  </feSpecularLighting>
  <feComposite in="spec" in2="SourceAlpha" operator="in" result="spec-in" />
  <feMerge>
    <feMergeNode in="SourceGraphic" />
    <feMergeNode in="spec-in" />
  </feMerge>
</filter>
```
