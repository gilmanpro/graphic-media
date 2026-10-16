# Arte algorítmico y estilos de dibujo expresivo

Generar imágenes artísticas/abstractas con código (no hay datos de por medio: la fórmula ES la obra). Recetas listas con matplotlib + numpy.

Índice: [1 Base](#1-base) · [2 Recetas](#2-recetas) · [3 Estilos](#3-estilos-expresivos) · [4 Control](#4-control-estético)

## 1 Base

```python
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt, numpy as np

fig, ax = plt.subplots(figsize=(6, 6))
ax.set_xlim(-1.2, 1.2); ax.set_ylim(-1.2, 1.2)
ax.set_aspect("equal"); ax.axis("off")     # lienzo cuadrado sin ejes: base de todo arte
fig.savefig("arte.png", dpi=300, transparent=True, bbox_inches="tight")
plt.close(fig)
```

## 2 Recetas

**Lissajous** (curvas paramétricas elegantes):

```python
t = np.linspace(0, 2 * np.pi, 2000)
for a, b, fase, color in [(3, 2, 0, "#4F46E5"), (5, 4, 0.7, "#FF6B6B")]:
    ax.plot(np.sin(a * t + fase), np.sin(b * t), color=color, lw=0.8, alpha=0.7)
```

**Espiral de puntos (dorado ≈ 137.5°)**:

```python
n = np.arange(1500); th = n * np.deg2rad(137.508); r = np.sqrt(n)
ax.scatter(np.cos(th) * r, np.sin(th) * r, s=4 + n / 60, c=th, cmap="viridis", alpha=0.8)
```

**Curvas de flujo (campo de ruido suave)**:

```python
x, y = np.meshgrid(np.linspace(-1, 1, 60), np.linspace(-1, 1, 60))
u = np.sin(3 * x) * np.cos(3 * y); v = -np.cos(3 * x) * np.sin(3 * y)
ax.streamplot(x, y, u, v, color=np.hypot(u, v), cmap="magma", lw=1.2, density=1.4)
```

**Trapecio/onda cuadrada artístico**:

```python
tt = np.linspace(0, 6 * np.pi, 400)
for k in range(1, 12, 2):                      # armónicos impares atenuados
    ax.plot(tt, np.sin(k * tt) / k, lw=0.7, alpha=0.5, color="#0EA5E9")
```

**Retícula de círculos concéntricos con jitter controlado**:

```python
rng = np.random.default_rng(7)
for cx in np.arange(-1, 1.01, 0.4):
    for cy in np.arange(-1, 1.01, 0.4):
        rr = 0.06 + 0.1 * rng.random()
        ax.add_patch(plt.Circle((cx + 0.03 * rng.standard_normal(),
                                 cy + 0.03 * rng.standard_normal()), rr,
                                fill=False, lw=0.6, ec="#111"))
```

## 3 Estilos expresivos

| Estilo | Cómo lograrlo |
|---|---|
| Tinta / boceto | `ax.plot(..., lw=0.5)` + temblor: añade `rng.normal(0, 0.003, t.shape)` a los valores; fondo `#FAFAF5` |
| Retrato de halftone | Dispersión de puntos cuyo radio depende de una imagen de luminancia (abrir con Pillow, muestrear) |
| Geométrico Bauhaus | Paleta de 3 colores planos + formas primitivas (círculo/triángulo/cuadrado) en composición asimétrica |
| Plano sobre cuadrícula | Cuadrícula fina `ax.grid(alpha=0.1)` + bloques de color rectangulares alineados |
| Ruido valor | `ax.imshow(rng.random((64, 64)), cmap="cubehelix", interpolation="bicubic")` + superponer formas blancas |
| Monocromo con acento | Todo en grises (`cmap="Greys"`) + UN elemento en color de acento |

## 4 Control estético

- **Semilla fija** (`np.random.default_rng(7)`): la obra es reproducible y refinable (mismo seed = mismos cambios).
- Itera por capas: estructura → densidad → paleta → grosor; guarda variantes (`arte_v2.png`) en vez de sobrescribir.
- Paleta limitada (2-4 colores) y un solo peso de línea dominante; el ruido/grosor uniforme da acabado de cartel.
- Exporta siempre a PNG 300dpi o SVG; verifica con `scripts/editar_imagen.py info`.
- Anti-patrones: colormaps del arcoíris (`jet`) como paleta de arte; más de 5 capas de alpha encima (vuelve barro); «arte» con texto explicativo pegado (eso es infografía, §1.5).
