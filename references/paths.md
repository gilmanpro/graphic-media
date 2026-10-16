# Referencia de Comandos de Path SVG

Guía completa de los comandos de `<path>` basada en SVG 2, MDN, y Josh W. Comeau.

## Sintaxis General

El atributo `d` define una secuencia de comandos de dibujo:

```xml
<path d="
  M x,y     — move (sin dibujar)
  L x,y     — line to
  H x       — horizontal line
  V y       — vertical line
  Z         — close path (cierra al inicio)
  Q cx,cy x,y     — quadratic Bézier
  T x,y            — smooth quadratic
  C c1x,c1y c2x,c2y x,y  — cubic Bézier
  S c2x,c2y x,y           — smooth cubic
  A rx,ry rot laf sf x,y  — arc
" />
```

**Mayúsculas** = coordenadas absolutas. **Minúsculas** = coordenadas relativas al punto anterior.

Cada comando hereda el punto final del comando previo como su punto de inicio.

## Move (M / m)

Mueve el "lápiz" sin dibujar. Todo path debe empezar con `M`.

```xml
<path d="M 10,10 L 50,50" />
<!-- Mueve a (10,10), luego dibuja línea hasta (50,50) -->
```

## Line (L / l)

Dibuja una línea recta desde la posición actual hasta (x, y).

```xml
<path d="M 10,10 L 50,10 L 50,50 L 10,50 Z" />
<!-- Un cuadrado -->
```

## Horizontal (H / h) y Vertical (V / v)

Abreviaturas para líneas horizontales/verticales (solo 1 parámetro):

```xml
<path d="M 10,10 H 90 V 90 H 10 Z" />
<!-- Rectángulo de 10,10 a 90,90 -->
```

## Close Path (Z / z)

Dibuja una línea recta desde la posición actual hasta el primer punto del subpath actual. No toma parámetros. **No hay diferencia entre mayúscula y minúscula.**

```xml
<path d="M 10,10 L 50,10 L 50,50 Z" />
<!-- Cierra formando un triángulo -->
```

El `Z` conecta con junta (linejoin), mientras que volver con `L` deja extremos con linecap. Esto es importante cuando se usan `stroke-linejoin: round` — `Z` suaviza la esquina final.

## Quadratic Bézier (Q / q)

Curva con 1 punto de control: `Q controlX,controlY endX,endY`

```xml
<path d="M 10,80 Q 95,10 180,80" />
```

El punto de control "jala" la curva hacia él. Es como un imán que atrae la línea.

## Smooth Quadratic (T / t)

Curva cuadrática que refleja automáticamente el punto de control anterior. Solo toma el punto final:

```xml
<path d="M 10,80 Q 52.5,10 95,80 T 180,80" />
```

Si no hay un `Q` o `T` previo, el control point se asume como el punto actual (resultando una línea recta).

## Cubic Bézier (C / c)

Curva con 2 puntos de control: `C c1x,c1y c2x,c2y endX,endY`

```xml
<path d="M 10,10 C 20,20 40,20 50,10" />
```

Para formas con doble curva (como una "S"), necesitas cúbicas. Las cuadráticas solo pueden curvar en una dirección.

## Smooth Cubic (S / s)

Curva cúbica que refleja el segundo punto de control del comando `C` o `S` anterior para usarlo como primer punto de control:

```xml
<path d="M 10,80 C 40,10 65,10 95,80 S 150,150 180,80" />
```

Si no hay `C` o `S` previo, el primer control point se asume como el punto actual.

## Elliptical Arc (A / a)

El comando más complejo: `A rx,ry x-axis-rotation large-arc-flag sweep-flag x,y`

```xml
<path d="M 10,315 L 110,215 A 30,50 0 0,1 162.55,162.45" />
```

### Parámetros del arco

| Parámetro | Valores | Descripción |
|---|---|---|
| `rx, ry` | números | Radios horizontal y vertical de la elipse hipotética |
| `x-axis-rotation` | grados | Rotación de la elipse (0 si es circular) |
| `large-arc-flag` | 0 o 1 | 0 = arco menor (≤180°), 1 = arco mayor (≥180°) |
| `sweep-flag` | 0 o 1 | 0 = sentido anti-horario, 1 = sentido horario |
| `x, y` | números | Punto final del arco |

### Intuición de arcos

Dados dos puntos, hay **4 arcos posibles** (2 elipses × 2 direcciones):

1. **Elipse A** (sentido horario):
   - `large-arc=0, sweep=1` → arco corto horario
   - `large-arc=1, sweep=1` → arco largo horario
2. **Elipse B** (sentido anti-horario):
   - `large-arc=0, sweep=0` → arco corto anti-horario
   - `large-arc=1, sweep=0` → arco largo anti-horario

> **Importante:** No se pueden hacer círculos/elipses completos con un solo arco porque el punto inicial y final son el mismo, creando infinitas soluciones. Para círculos, usa `<circle>`.

### Trabajo manual con arcos

- Para círculos/elipses completos usa `<circle>`/`<ellipse>`, nunca `A`.
- Si necesitas un arco concreto, genera el path con código (fórmula de conversión radio/ángulos a puntos) en vez de buscar editores online.

## Reglas de Path Data

1. **Comas y espacios son opcionales** (según W3C) pero se recomienda usarlos para legibilidad
2. **Los comandos se pueden repetir** sin repetir la letra: `M 10,10 20,20` equivale a `M 10,10 L 20,20` (excepto M que se convierte en L implícito)
3. **pathLength** permite sobrescribir la longitud del path para animaciones más fáciles:
   ```xml
   <path pathLength="100" d="..." />
   <!-- Ahora stroke-dasharray="100" = longitud completa -->
   ```

## Chained Curves (T y S)

Cuando encadenas curvas, los comandos `T` y `S` son esenciales para transiciones suaves:

- `T` después de `Q`: refleja el control point de la Q
- `S` después de `C`: refleja el segundo control point de la C

Sin estos comandos, las curvas encadenadas tienen "codos" visibles.

## getTotalLength()

En JavaScript, `element.getTotalLength()` devuelve la longitud total del path, útil para animaciones con stroke-dasharray:

```javascript
const path = document.querySelector('path');
const length = path.getTotalLength();
path.style.strokeDasharray = `${length} ${length}`;
path.style.strokeDashoffset = length;
// En CSS: animation que lleva stroke-dashoffset a 0
```

## Ejemplos Prácticos

```xml
<!-- Corazón -->
<path d="M 50,30
         A 20,20 0 0,1 90,30
         A 20,20 0 0,1 50,70
         A 20,20 0 0,1 10,30
         A 20,20 0 0,1 50,30
         Z" />

<!-- Estrella (polígono regular) -->
<path d="M 50,5 L 61,35 L 95,35 L 68,57 L 79,91
         L 50,70 L 21,91 L 32,57 L 5,35 L 39,35 Z" />

<!-- Onda senoidal -->
<path d="M 0,50 C 25,10 75,90 100,50 C 125,10 175,90 200,50" />
```
