# Mejores Prácticas SVG

Guía de optimización, accesibilidad, herramientas y anti-patrones.

## Optimización

### 1. Limpieza manual

```xml
<!-- ❌ ANTES: lleno de metadatos de Illustrator -->
<svg xmlns:dc="http://purl.org/dc/elements/1.1/"
     xmlns:cc="http://creativecommons.org/ns#"
     xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#"
     xmlns:svg="http://www.w3.org/2000/svg"
     xmlns="http://www.w3.org/2000/svg"
     viewBox="0 0 200 200">
  <metadata>...</metadata>
  <g id="capa_x0020_1">
    <rect id="rect1" x="10" y="10" width="180" height="180"
          fill="#4F46E5" />
  </g>
</svg>

<!-- ✅ DESPUÉS: limpio y semántico -->
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 200 200">
  <rect x="10" y="10" width="180" height="180" fill="#4F46E5" />
</svg>
```

### 2. SVGO (herramienta CLI estándar)

```bash
# Instalación global
npm install -g svgo

# Optimizar un archivo
svgo input.svg -o output.svg

# Optimizar in-place
svgo input.svg

# Configuración personalizada (svgo.config.js)
module.exports = {
  plugins: [
    'preset-default',
    { name: 'removeViewBox', active: false },  // mantener viewBox
    { name: 'sortAttrs', active: true },
  ],
};
```

### 3. Redondear coordenadas

Coordenadas con muchos decimales (de exportadores) aumentan el tamaño sin beneficio visible:

```xml
<!-- ❌ Demasiados decimales -->
<path d="M 10.1234,20.5678 L 50.9101,60.2345" />

<!-- ✅ Redondeado a 2 decimales (suficiente) -->
<path d="M 10.12,20.57 L 50.91,60.23" />

<!-- ✅ Enteros cuando sea posible -->
<path d="M 10,20 L 50,60" />
```

### 4. Usar `<use>` para repeticiones

```xml
<!-- ❌ Repetir el mismo icono muchas veces -->
<svg viewBox="0 0 300 100">
  <g id="icono">
    <circle cx="15" cy="15" r="10" fill="blue" />
    <path d="M 10,15 L 15,20 L 20,10" stroke="white" />
  </g>
  <use href="#icono" x="0" y="0" />
  <use href="#icono" x="50" y="0" />
  <use href="#icono" x="100" y="0" />
  <use href="#icono" x="150" y="0" />
</svg>
```

### 5. Eliminar elementos invisibles

- `<defs>` no se renderizan directamente (bueno)
- Elementos con `display="none"` o `opacity="0"` — eliminar
- Paths vacíos — eliminar
- `<g>` sin atributos y con un solo hijo — aplanar

## Accesibilidad

### Estructura básica accesible

```xml
<svg role="img" aria-labelledby="titulo descripcion"
     viewBox="0 0 200 200" xmlns="http://www.w3.org/2000/svg">
  <title id="titulo">Gráfico de ventas 2025</title>
  <desc id="descripcion">
    Barrra apilada que muestra $50K en Q1, $75K en Q2,
    $60K en Q3 y $90K en Q4.
  </desc>
  <!-- contenido visual -->
</svg>
```

### Iconos decorativos

Los iconos puramente decorativos deben ocultarse de screen readers (aria-hidden):

```xml
<svg aria-hidden="true" focusable="false" viewBox="0 0 24 24">
  <path d="..." />
</svg>
```

### Contraste de color

- Texto sobre fondo: ratio mínimo 4.5:1 (WCAG AA)
- Para iconos informativos: ratio mínimo 3:1
- Evitar solo color para transmitir información

### Texto en SVG

```xml
<!-- Los textos en SVG son naturalmente accesibles -->
<text font-size="14" fill="#333">Total: $50,000</text>

<!-- Los títulos anidados también ayudan -->
<g role="group" aria-label="Barra del mes de enero">
  <rect x="10" y="20" width="20" height="100" fill="blue" />
  <text x="20" y="130" text-anchor="middle" font-size="10">Enero</text>
</g>
```

## Herramientas

| Herramienta | Uso |
|---|---|
| **SVGO** | Optimización CLI |
| **Inkscape** | Editor SVG gratuito de escritorio |
| **cairosvg** | Python: SVG → PDF/PNG |
| **librsvg** | CLI: rsvg-convert SVG → PNG |
| **svg-sprite** | Crear sprites SVG |
| **svgr** | SVG → React components |
| **Yqnn SVG Path Editor** | Editor visual de paths online |
| **Boxy SVG** | Editor SVG online (buen balance código/visual) |
| **Figma → SVG** | Exportar con "Incluir ID de capa" y SVG 2 stylesheet |

## Estructura de Archivo SVG

```xml
<!-- Estándar mínimo para SVG válido -->
<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg"
     xmlns:xlink="http://www.w3.org/1999/xlink"
     viewBox="0 0 100 100"
     width="100%" height="100%"
     role="img" aria-labelledby="title-el desc-el">
  <title id="title-el">Título</title>
  <desc id="desc-el">Descripción</desc>

  <defs>
    <!-- Gradientes, filtros, patrones, elementos reutilizables -->
  </defs>

  <!-- Contenido agrupado semánticamente -->
  <g id="capa-principal">
  </g>
</svg>
```

## Frameworks y Librerías

| Librería | Propósito |
|---|---|
| **D3.js** | Visualización de datos con SVG |
| **Snap.svg** | Manipulación SVG con JavaScript |
| **GSAP** | Animaciones SVG de alto rendimiento |
| **Lucide Icons** | Iconos SVG open-source (React, Vue, Svelte, HTML) |
| **Feather Icons** | Iconos SVG minimalistas |
| **Heroicons** | Iconos SVG de Tailwind CSS |
| **Humane Tech Icons** | Iconos SVG con diseño amigable |

## Anti-patrones (Errores Comunes)

| Error | Problema | Solución |
|---|---|---|
| **Degenerate shapes** | rect con width=0 o height=0 no se renderiza | Asegurar dimensiones > 0 |
| **Stroke recortado** | stroke-width grande en borde del viewBox | Agregar padding en viewBox |
| **Filtro recortado** | sombra/glow se corta | Aumentar x/y/width/height del filter |
| **Olvidar xmlns** | SVG no funciona en HTML | `xmlns="http://www.w3.org/2000/svg"` |
| **Falta viewBox** | SVG no escala | Siempre incluir viewBox |
| **Decimales excesivos** | Archivo inflado innecesariamente | Redondear a 2 decimales |
| **Grupos anidados inútiles** | `<g>` con un solo hijo | Aplanar la estructura |
| **Fuentes no instaladas** | SVG depende de fuentes locales | Usar web fonts o convertir texto a paths |
| **JavaScript en SVG standalone** | No funciona en `<img>` | Usar inline u `<object>` si se necesita JS |
| **SMIL en contextos restrictivos** | CSP puede bloquear SMIL | Considerar CSS animation como alternativa |

## Render Hints

```xml
<svg shape-rendering="geometricPrecision">
  <!-- Para iconos/logos: geometricPrecision -->
  <!-- Para gráficos animados: optimizeSpeed -->
  <!-- Para mapas: crispEdges -->
</svg>
```

Valores de `shape-rendering`:
- `auto` — browser elige
- `optimizeSpeed` — prioriza rendimiento
- `crispEdges` — bordes nítidos (sin anti-aliasing)
- `geometricPrecision` — máxima precisión (para iconos)

```xml
<svg text-rendering="optimizeLegibility">
  <!-- Para texto: optimizeLegibility -->
  <!-- Para rendimiento: optimizeSpeed -->
</svg>
```

## Cheatsheet de viewBox

| viewBox | Efecto |
|---|---|
| `0 0 100 100` | 1:1, coordenadas 0-100 |
| `0 0 200 200` | 1:1, más espacio de trabajo |
| `-50 -50 100 100` | Origen centrado (como coordenadas cartesianas) |
| `0 0 100 50` | Proporción 2:1 (ancho:alto) |
