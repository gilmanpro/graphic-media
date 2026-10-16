# Máquinas isométricas dibujadas como código

Metodología para explicar un objeto físico (máquina, instrumento, herramienta, mueble) construyéndolo como figura isométrica interactiva hecha de código — el dibujo es SVG/HTML que el navegador renderiza, no un píxel generado.

Índice: [1 Principio](#1-principio) · [2 Flujo](#2-flujo-de-ingeniería) · [3 Kit isométrico](#3-kit-isométrico) · [4 Sombreado](#4-sombreado-de-cuatro-tonos) · [5 Efectos](#5-capa-de-efectos-fuego-agua-luz) · [6 Auditoría](#6-auditoría-antes-de-entregar) · [7 Límites](#7-límites)

## 1 Principio

Una figura de código es **editable, inspeccionable y exacta**: cada parte tiene tamaño real y posición calculada. El objetivo no es «una imagen bonita» sino **explicar una idea construyéndola como objeto real**: el usuario puede rotarla, desmontarla y verla funcionar.

## 2 Flujo de ingeniería

Secuencia obligatoria (no saltar pasos):

1. **Cifras verdaderas primero**: recoge dimensiones y proporciones reales del objeto (o rango creíble si es inventado). Nada de «más o menos»: cada parte tiene tamaño.
2. **Lista de partes**: enumera componentes con nombre, medida y posición aproximada (`base 120x40, eje Ø8, soporte x2`).
3. **Construye geometría** con el kit isométrico (§3): primitivas (caja, cilindro, disco, cuña) proyectadas.
4. **Pinta de atrás hacia delante** (painter's algorithm): orden de profundidad del isométrico; una parte pintada antes queda tapada por la siguiente.
5. **Audita** (§6) antes de entregar.

## 3 Kit isométrico

Proyección isométrica estándar (eje X a 30°, Z arriba):

```
x' = (x - y) * cos(30°)     # 0.866
y' = (x + y) * sin(30°) - z # 0.5
```

Primitivas del kit (todas como `<g transform>` o paths calculados):

| Parte | Cómo se dibuja |
|---|---|
| Caja | Paralelepípedo: 3 caras visibles (superior, izq., dcha.) como polígonos |
| Cilindro / eje | Elipse superior + rectángulo lateral + arco inferior |
| Disco / dial | Elipse con ratio 2:1 (isométrica), anillo concéntrico para espesor |
| Cuña / chaflán | Trapecio en la cara correspondiente |
| Tornillos | Cruz o estrella de 6-8px en la cara; repetir con `<use>` |

Convenciones: grilla de 10u; ángulos de proyección fijos (no mezclar perspectivas); medidas anotadas como lectura viva en una esquina de la tarjeta (HTML), no sobre la figura.

## 4 Sombreado de cuatro tonos

Cada cara recibe uno de 4 tonos del mismo color según su orientación:

- **Superior**: tono más claro (luz cenital).
- **Izquierda**: tono base.
- **Derecha**: tono oscuro (-20% luminosidad).
- **Interior/oculto**: el más oscuro, solo si se ve al desmontar.

Deriva los tonos con una función (`mezcla(color, blanco/negro, 0.2)`) — nunca colores elegidos a ojo por cara.

## 5 Capa de efectos (fuego, agua, luz, vapor)

Cuando el objeto lleve fuego, humo, chorro o luz:

- Capa opcional **dentro de la misma cámara isométrica** (la figura SVG sigue leyéndose sin ella; degradar a nada si no hay soporte WebGL).
- La capa no puede cambiar la geometría: solo emisión, partículas y brillo encima de las caras.
- SVG-first: si el efecto se puede con `feTurbulence`/`feGaussianBlur`/degradados animados, quédate en SVG (portable y capturable); WebGL solo si hace falta animación por frame intensa.

## 6 Auditoría antes de entregar

Checklist mecánico (un script de comprobación si la figura es grande):

- [ ] Ninguna parte atraviesa a otra (intersección de volúmenes = 0).
- [ ] Toda parte apoya en un soporte o conexión (nada flotando sin motivo).
- [ ] Orden de pintado correcto: sin caras tapando lo que debería verse delante.
- [ ] Proporciones coherentes con la lista de partes (medidas reales vs. dibujadas).
- [ ] Sin solapes de texto; la lectura viva no se sale de la tarjeta.
- [ ] Rota/parpadea a ~60fps con <100 partes; si supera, reduce piezas o pasa partes estáticas a un único grupo.

## 7 Límites

- **No es una librería de gráficos**: no lleva ejes ni series de datos — los datos van con `scripts/grafico.py` (§1.2 del SKILL.md), esta figura explica objetos.
- **Lento a propósito**: una figura bien hecha lleva sesión larga; prioriza exactitud sobre rapidez y avisa del alcance.
- **Alcance**: máquinas, instrumentos, herramientas y muebles; no personas ni mapas exactos (esas formas necesitan otro enfoque).
- **3D real**: si piden rotación en tres ejes de verdad (no isométrica), es un alcance aparte con más coste — proponer primero la isométrica con despiece.
