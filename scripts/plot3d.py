#!/usr/bin/env python3
"""plot3d.py — figuras 3D con matplotlib (superficie, nube, barras, malla) + GIF rotatorio.

Requiere: pip install matplotlib numpy
Uso:
  python scripts/plot3d.py superficie -o sup.png                       # z = sin(x^2+y^2)
  python scripts/plot3d.py superficie -o sup.png --gif sup.gif         # orbita 360 grados
  python scripts/plot3d.py nube datos.csv --x px --y py --z pz -o n.png
  python scripts/plot3d.py barras datos.csv --x cat --y val -o b.png
  python scripts/plot3d.py malla --func "x*y" -o m.png                 # wireframe de una funcion
Opciones comunes: --titulo, --ejes "X,Y,Z", --ancho/--alto (pulgadas), --dpi, --transparente
El GIF usa PillowWriter (sin ffmpeg); para MP4: --gif x.gif y luego scripts/video.py convertir.
"""
import argparse
import csv
import sys

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np


def leer_cols(ruta, cols):
    with open(ruta, newline="", encoding="utf-8-sig") as f:
        rows = list(csv.DictReader(f))
    if not rows:
        sys.exit(f"CSV vacio: {ruta}")
    faltan = [c for c in cols if c not in rows[0]]
    if faltan:
        sys.exit(f"columna(s) inexistente(s): {', '.join(faltan)} (hay: {', '.join(rows[0])})")
    return {c: [r[c] for r in rows] for c in cols}   # strings crudos; convertir por uso


def num(vals):
    return np.array([float(str(v).replace(",", ".")) for v in vals])


def base(a, proj="3d"):
    fig = plt.figure(figsize=(a.ancho, a.alto))
    ax = fig.add_subplot(111, projection=proj)
    ax.view_init(elev=a.elev, azim=a.azim)
    if a.ejes:
        x, y, z = a.ejes.split(",")
        ax.set_xlabel(x.strip()); ax.set_ylabel(y.strip()); ax.set_zlabel(z.strip())
    if a.titulo:
        ax.set_title(a.titulo)
    return fig, ax


def guardar(fig, a):
    if a.gif:
        rotar(fig, a)
    salida = a.salida
    if a.salida.lower().endswith(".gif"):
        salida = a.salida
        fig.savefig(salida, dpi=a.dpi, transparent=a.transparente, bbox_inches="tight")
    else:
        fig.savefig(salida, dpi=a.dpi, transparent=a.transparente, bbox_inches="tight")
    plt.close(fig)
    print(f"OK {salida}" + (f" + {a.gif}" if a.gif else ""))


def rotar(fig, a):
    from matplotlib.animation import FuncAnimation, PillowWriter
    ax = fig.axes[0]

    def paso(i):
        ax.view_init(elev=a.elev, azim=a.azim + 360 * i / a.frames)

    anim = FuncAnimation(fig, paso, frames=a.frames, interval=1000 // a.fps)
    anim.save(a.gif, writer=PillowWriter(fps=a.fps))


def tipo_superficie(a):
    fig, ax = base(a)
    x = np.linspace(-3, 3, 120)
    X, Y = np.meshgrid(x, x)
    Z = np.sin(np.hypot(X, Y))                       # onda circular (demo)
    if a.func:
        Z = eval(a.func, {"x": X, "y": Y, "np": np})  # expresion controlada del usuario
    ax.plot_surface(X, Y, Z, cmap="viridis", linewidth=0, antialiased=True, alpha=0.95)
    guardar(fig, a)


def tipo_malla(a):
    fig, ax = base(a)
    x = np.linspace(-2, 2, 30)
    X, Y = np.meshgrid(x, x)
    Z = eval(a.func or "x*y", {"x": X, "y": Y, "np": np})
    ax.plot_wireframe(X, Y, Z, color="#4F46E5", linewidth=0.6, rstride=2, cstride=2)
    guardar(fig, a)


def tipo_nube(a):
    if not a.csv:
        sys.exit("nube necesita datos.csv --x --y --z")
    c = leer_cols(a.csv, [a.x, a.y, a.z])
    nx, ny, nz = num(c[a.x]), num(c[a.y]), num(c[a.z])
    fig, ax = base(a)
    p = ax.scatter(nx, ny, nz, c=nz, cmap="viridis",
                   s=24, alpha=0.85, depthshade=True)
    fig.colorbar(p, ax=ax, shrink=0.6, pad=0.1)
    guardar(fig, a)


def tipo_barras(a):
    if not a.csv:
        sys.exit("barras necesita datos.csv --x (categorias) --y (altura)")
    c = leer_cols(a.csv, [a.x, a.y])
    alturas = num(c[a.y])
    n = len(alturas)
    xs = np.arange(n)
    fig, ax = base(a)
    # bar3d: base en el plano xy, altura en z (apilado simple)
    dx = dy = 0.6
    ax.bar3d(xs - dx / 2, np.zeros(n) - dy / 2, np.zeros(n), dx, dy, alturas,
             color="#4F46E5", shade=True)
    ax.set_xticks(xs + 0.5)
    ax.set_xticklabels([str(v) for v in c[a.x]], fontsize=8, rotation=30, ha="right")
    guardar(fig, a)


def main():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = p.add_subparsers(dest="tipo", required=True)

    def comun(s):
        s.add_argument("-o", "--salida", default="plot3d.png")
        s.add_argument("--gif", help="ademas, GIF orbitando la figura")
        s.add_argument("--frames", type=int, default=36, help="frames del GIF (def. 36)")
        s.add_argument("--fps", type=int, default=12)
        s.add_argument("--titulo"); s.add_argument("--ejes", help='"X,Y,Z"')
        s.add_argument("--elev", type=float, default=28, help="grados de elevacion (def. 28)")
        s.add_argument("--azim", type=float, default=-55, help="grados de azimut (def. -55)")
        s.add_argument("--ancho", type=float, default=7); s.add_argument("--alto", type=float, default=5)
        s.add_argument("--dpi", type=int, default=200)
        s.add_argument("--transparente", action="store_true")

    s = sub.add_parser("superficie"); comun(s)
    s.add_argument("--func", help="expresion de z con x,y,np (p. ej. 'np.sin(x)*np.cos(y)')")
    s = sub.add_parser("malla"); comun(s)
    s.add_argument("--func", help="expresion de z (def. 'x*y')")
    s = sub.add_parser("nube"); comun(s)
    s.add_argument("csv", nargs="?"); s.add_argument("--x"); s.add_argument("--y"); s.add_argument("--z")
    s = sub.add_parser("barras"); comun(s)
    s.add_argument("csv", nargs="?"); s.add_argument("--x"); s.add_argument("--y")

    a = p.parse_args()
    {"superficie": tipo_superficie, "malla": tipo_malla,
     "nube": tipo_nube, "barras": tipo_barras}[a.tipo](a)


if __name__ == "__main__":
    main()
