# Planos y figuras 3D

Del dibujo isométrico al modelo 3D: proyecciones, recetas matplotlib (`scripts/plot3d.py`) y límites de cada camino.

Índice: [1 Elegir](#1-elegir-el-tipo-de-3d) · [2 Proyecciones](#2-proyecciones-para-dibujar-a-mano) · [3 Script](#3-script-plot3dpy) · [4 Calidad](#4-calidad-de-render) · [5 Sólidos CAD](#5-sólidos-cad)

## 1 Elegir el tipo de 3D

| Necesidad | Camino |
|---|---|
| Croquis isométrico de plano/habitación | SVG a mano (§3.2 del SKILL) o `references/maquinas-isometricas.md` |
| Superficie de datos/función, nube de puntos, barras 3D | `scripts/plot3d.py` (matplotlib) |
| Vista rotatoria (GIF) de esa figura | `plot3d.py --gif` (PillowWriter, sin ffmpeg) |
| Planta con volumen (test de masas) | isométrico SVG o `plot3d.py barras` sobre huella |
| Sólido paramétrico real (pieza, junta, carcasa) | OpenSCAD/FreeCAD (fuera del alcance por defecto — avisar) |
| CAD con capas editable en 3D | DXF con coordenadas Z (`ezdxf`, `references/ingenieria.md`) |

## 2 Proyecciones (para dibujar a mano en SVG)

- **Isométrica**: X/Y a 30°, Z arriba; sin distorsión de escala en los 3 ejes (fórmulas en `maquinas-isometricas.md`).
- **Dimétrica/caballera**: un eje a 45° con escala ½ — para bocetos rápidos con un lado «real».
- **Perspectiva 1 punto**: un solo punto de fuga (frontal); edificios y interiores.
- **Perspectiva 2 puntos**: dos fugas en el horizonte; exteriores dinámicos.
- Regla: UNA proyección por pieza; construir con líneas guía al horizonte, no «a ojo».

## 3 Script plot3d.py

```bash
python scripts/plot3d.py superficie -o sup.png --titulo "Onda" --gif sup.gif   # superficie + órbita
python scripts/plot3d.py superficie -o f.png --func "np.sin(x)*np.cos(y)"      # función propia
python scripts/plot3d.py malla -o m.png --func "x*y"                           # wireframe
python scripts/plot3d.py nube puntos.csv --x edad --y peso --z talla -o n.png  # dispersión 3D
python scripts/plot3d.py barras datos.csv --x mes --y valor -o b.png           # barras 3D
```

- La expresión `--func` se evalúa con `x`, `y` y `np` en alcance (misma semilla de rejilla `linspace` del script); no meter efectos secundarios ahí.
- `--elev/--azim` fijan la cámara (def. 28°/-55°: lectura natural); `--gif` barre 360° de azimut.
- Transparencia para incrustar en slides: `--transparente`.

## 4 Calidad de render

- **Cámara primero**: misma elevación/azimut en todas las figuras de una serie (si rotan, mismo rango de frames).
- `depthshade=True` en scatter (profundidad legible); `alpha<1` solo si se apilan capas.
- Colormap único por figura (`viridis` por defecto); colorbar siempre con unidad.
- Warnings típicos: sin `projection="3d"` no hay 3D; ejes sin etiqueta con unidad → figura inútil; `plot_surface` con poca resolución (usa ≥100 puntos por lado en salidas grandes).
- GIF: 36 frames/12fps basta para orbitar; más frames solo si hay geometría fina (mallas densas).

## 5 Sólidos CAD

- **DXF 3D**: `ezdxf` admite `add_3dline`, `add_polyline3d` y `extrude` — para recorridos y perfiles extruidos sencillos; capas igual que el flujo 2D.
- **STL/paramétrico**: si el encargo es «pieza para imprimir/CNC», el flujo correcto es OpenSCAD (código) o FreeCAD; esta skill lo detecta y lo deriva con explicación (no inventa mallas).
- Malla sana = cerrada (watertight), triángulos con normal coherente, unidades en mm declaradas.

Anti-patrones: perspectiva mezclada con isométrica en la misma figura; rotar el GIF en dos ejes a la vez (marea); colormap arcoíris en figuras 3D de informe (ilegible en impresión); prometer render fotorrealista con matplotlib (no lo es — para eso hay motores dedicados).
