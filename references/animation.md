# Animación SVG

Guía completa de animación SVG con CSS, SMIL y JavaScript.

## 1. Animación con CSS Transitions

La técnica más simple. Muchos atributos SVG (especialmente los de presentación) son propiedades CSS animables:

```css
/* En SVG inline o CSS externo */
circle {
  fill: #4F46E5;
  transition: fill 600ms, r 400ms, transform 300ms;
}
circle:hover {
  fill: #7C3AED;
  r: 30;
  transform: scale(1.2);
}
```

**Propiedades SVG animables con CSS transitions:**
- `fill`, `fill-opacity`
- `stroke`, `stroke-opacity`, `stroke-width`
- `stroke-dasharray`, `stroke-dashoffset`
- `opacity`
- `transform`, `transform-origin` (SVG 2)
- `cx`, `cy`, `r`, `rx`, `ry` (SVG 2)
- `x`, `y`, `width`, `height` (SVG 2)

## 2. Animación con CSS @keyframes

Para animaciones más complejas:

```css
@keyframes pulso {
  0%, 100% { transform: scale(1); opacity: 1; }
  50% { transform: scale(1.1); opacity: 0.7; }
}

@keyframes dibujar {
  from { stroke-dashoffset: 1000; }
  to { stroke-dashoffset: 0; }
}

@keyframes girar {
  from { transform: rotate(0deg); }
  to { transform: rotate(360deg); }
}

.mi-elemento {
  animation: pulso 2s ease-in-out infinite;
}

.path-animado {
  stroke-dasharray: 1000;
  stroke-dashoffset: 1000;
  animation: dibujar 2s ease forwards;
}
```

### Técnica: Animación de "dibujo" (drawing)

Hace que un SVG parezca dibujarse solo:

```css
path {
  stroke-dasharray: var(--path-length, 1000);
  stroke-dashoffset: var(--path-length, 1000);
  animation: draw 2s ease-out forwards;
}
@keyframes draw {
  to { stroke-dashoffset: 0; }
}
```

```javascript
// Obtener longitud exacta
const path = document.querySelector('path');
const length = path.getTotalLength();
// o usar pathLength="100" en el SVG para simplificar
```

### Técnica: Spinner animado

```css
.spinner {
  animation: spin 2s linear infinite;
  transform-origin: center;
}
@keyframes spin {
  to { transform: rotate(360deg); }
}

.spinner-circle {
  stroke-dasharray: 200;
  stroke-dashoffset: 0;
  animation: dash 1.5s ease-in-out infinite;
}
@keyframes dash {
  0% { stroke-dashoffset: 200; }
  50% { stroke-dashoffset: 50; transform: rotate(90deg); }
  100% { stroke-dashoffset: 200; transform: rotate(360deg); }
}
```

## 3. Animación con SMIL (Declarativa)

SMIL (Synchronized Multimedia Integration Language) permite animaciones declarativas directamente en SVG, sin CSS ni JavaScript.

### `<animate>`

```xml
<circle cx="50" cy="50" r="20" fill="blue">
  <!-- Mover de 50 a 150 horizontalmente -->
  <animate attributeName="cx" from="50" to="150" dur="2s"
           repeatCount="indefinite" />
  <!-- Hacer pulso en el radio -->
  <animate attributeName="r" values="20;30;20" dur="1s"
           repeatCount="indefinite" />
  <!-- Fundido -->
  <animate attributeName="opacity" from="1" to="0.3" dur="1s"
           repeatCount="indefinite" autofill="freeze" />
</circle>
```

### Atributos de `<animate>`

| Atributo | Descripción | Ejemplo |
|---|---|---|
| `attributeName` | Atributo a animar | `"cx"` |
| `from` | Valor inicial | `"50"` |
| `to` | Valor final | `"150"` |
| `values` | Lista de valores | `"20;30;20"` |
| `dur` | Duración | `"2s"`, `"500ms"` |
| `repeatCount` | Repeticiones | `"2"`, `"indefinite"` |
| `fill` | Estado final | `"freeze"` |
| `calcMode` | Modo de interpolación | `"linear"`, `"paced"`, `"spline"` |
| `begin` | Inicio | `"0s"`, `"click"` |
| `end` | Fin | `"5s"` |
| `keyTimes` | Puntos de tiempo para keySplines | `"0;0.5;1"` |
| `keySplines` | Curvas de easing (con calcMode=spline) | `"0.4 0 0.6 1"` |

### `<animateTransform>`

Animación específica para transformaciones:

```xml
<rect x="50" y="50" width="50" height="50" fill="red">
  <animateTransform attributeName="transform" type="rotate"
    from="0 75 75" to="360 75 75" dur="3s" repeatCount="indefinite" />
</rect>

<g>
  <animateTransform attributeName="transform" type="translate"
    values="0,0; 100,0; 100,100; 0,100; 0,0" dur="5s" repeatCount="indefinite" />
  <circle cx="10" cy="10" r="10" fill="blue" />
</g>
```

Tipos: `rotate`, `translate`, `scale`, `skewX`, `skewY`

### `<animateMotion>`

Animación a lo largo de un path:

```xml
<defs>
  <path id="trayectoria" d="M 50,50 C 100,0 200,100 250,50"
        fill="none" stroke="none" />
</defs>

<!-- Opcional: mostrar el path -->
<use href="#trayectoria" stroke="#ccc" stroke-width="1" />

<!-- Elemento que se mueve -->
<circle r="8" fill="#4F46E5">
  <animateMotion dur="3s" repeatCount="indefinite">
    <mpath href="#trayectoria" />
  </animateMotion>
</circle>
```

### Encadenamiento (begin con IDs)

```xml
<animate id="anim1" attributeName="opacity" from="0" to="1" dur="1s"
         begin="0s" fill="freeze" />
<animate attributeName="opacity" from="1" to="0" dur="1s"
         begin="anim1.end" fill="freeze" />
```

### Interactividad en SMIL

```xml
<circle cx="50" cy="50" r="20" fill="blue">
  <animate attributeName="r" from="20" to="35" dur="0.3s"
           begin="mouseover" end="mouseout" fill="freeze" />
  <animate attributeName="fill" from="blue" to="red" dur="0.3s"
           begin="mouseover" end="mouseout" fill="freeze" />
</circle>
```

## 4. Animación con JavaScript

```javascript
const svg = document.querySelector('svg');
const circle = document.querySelector('circle');

// Usando Web Animations API
circle.animate([
  { r: 20, fill: '#4F46E5' },
  { r: 35, fill: '#7C3AED' },
  { r: 20, fill: '#4F46E5' }
], {
  duration: 2000,
  iterations: Infinity,
  easing: 'ease-in-out'
});

// Manipulación directa de atributos
let start = null;
function animate(timestamp) {
  if (!start) start = timestamp;
  const progress = (timestamp - start) / 2000;
  const cx = 50 + Math.sin(progress * 2 * Math.PI) * 40;
  circle.setAttribute('cx', cx);
  requestAnimationFrame(animate);
}
requestAnimationFrame(animate);
```

## 5. Comparación de Enfoques

| Enfoque | Complejidad | Control | Rendimiento | Cuándo usar |
|---|---|---|---|---|
| **CSS Transitions** | Baja | Medio | Excelente | Hover, estados simples |
| **CSS @keyframes** | Media | Alto | Excelente | Animaciones autónomas |
| **SMIL animate** | Media | Alto | Excelente | Animación nativa SVG, atributos no-CSS |
| **JavaScript** | Alta | Total | Bueno | Animaciones dinámicas/complejas |

## Ejemplos Completos

### Loading spinner

```xml
<svg viewBox="0 0 24 24" width="48" height="48">
  <circle cx="12" cy="12" r="10" fill="none"
          stroke="#e0e0e0" stroke-width="2" />
  <circle cx="12" cy="12" r="10" fill="none"
          stroke="#4F46E5" stroke-width="2"
          stroke-dasharray="62.83" stroke-dashoffset="62.83"
          stroke-linecap="round">
    <animate attributeName="stroke-dashoffset"
             from="62.83" to="15.7" dur="1.5s"
             repeatCount="indefinite" />
    <animateTransform attributeName="transform" type="rotate"
             from="0 12 12" to="360 12 12" dur="2s"
             repeatCount="indefinite" />
  </circle>
</svg>
```

### Barra de progreso animada

```xml
<svg viewBox="0 0 200 10" width="100%" height="10">
  <rect width="200" height="10" rx="5" fill="#e0e0e0" />
  <rect x="0" y="0" height="10" rx="5" fill="#4F46E5">
    <animate attributeName="width" from="0" to="150" dur="3s"
             fill="freeze" />
  </rect>
</svg>
```
