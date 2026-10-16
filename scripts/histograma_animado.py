#!/usr/bin/env python3
"""histograma_animado.py — GIF de histograma animado (acumulado o evolutivo) sin ffmpeg.

Requiere: pip install matplotlib
Uso:
  python histograma_animado.py --simular 500 -o hist.gif
  python histograma_animado.py datos.csv --columna ventas --frames 40 -o hist.gif
Opciones: --evolutivo (distribucion distinta por frame en vez de acumulado)
          --bins 30 --duracion 120 (ms/frame via fps) --mp4 (requiere ffmpeg)
"""
import argparse
import csv
import sys

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation, PillowWriter
import numpy as np


def main():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("archivo", nargs="?", help="CSV con la columna a histogramar")
    p.add_argument("--columna", help="columna numerica del CSV")
    p.add_argument("--simular", type=int, nargs="?", const=500, help="N muestras N(0,1) si no hay CSV")
    p.add_argument("--frames", type=int, default=60)
    p.add_argument("--bins", type=int, default=40)
    p.add_argument("--evolutivo", action="store_true")
    p.add_argument("--fps", type=int, default=8)
    p.add_argument("-o", "--salida", default="histograma.gif")
    p.add_argument("--mp4", action="store_true", help="salida MP4 (requiere ffmpeg en PATH)")
    a = p.parse_args()

    if a.archivo:
        with open(a.archivo, newline="", encoding="utf-8-sig") as f:
            rows = list(csv.DictReader(f))
        if not a.columna:
            sys.exit("--archivo requiere --columna")
        datos = np.array([float(r[a.columna].replace(",", ".")) for r in rows])
        if a.evolutivo:  # repartir en frames
            trozos = np.array_split(datos, a.frames)
        else:
            trozos = [datos[: max(2, int(len(datos) * (i + 1) / a.frames))]
                      for i in range(a.frames)]
    elif a.simular:
        datos = np.random.default_rng(42).normal(0, 1, a.simular)
        if a.evolutivo:
            base = np.random.default_rng(7)
            trozos = [base.normal(0, 1, max(20, a.simular // a.frames)) for _ in range(a.frames)]
        else:
            trozos = [datos[: max(2, int(len(datos) * (i + 1) / a.frames))]
                      for i in range(a.frames)]
    else:
        sys.exit("indica un CSV con --columna o usa --simular")

    límite = max(abs(np.min(datos)), abs(np.max(datos))) * 1.1
    bins = np.linspace(-límite, límite, a.bins + 1)  # bins FIJOS: sin bins fijos el gif "baila"

    fig, ax = plt.subplots(figsize=(8, 4.5))

    def actualizar(i):
        ax.cla()
        ax.hist(trozos[i], bins=bins, color="#4F46E5", edgecolor="white")
        ax.set(xlim=(-límite, límite), xlabel="Valor", ylabel="Frecuencia",
               title=("Histograma evolutivo" if a.evolutivo else "Histograma acumulado")
                      + f" — frame {i + 1}/{a.frames}")
        ax.grid(True, alpha=0.3)

    anim = FuncAnimation(fig, actualizar, frames=a.frames, interval=1000 // a.fps)
    if a.mp4:
        anim.save(a.salida.rsplit(".", 1)[0] + ".mp4", writer="ffmpeg", fps=a.fps, dpi=150)
    else:
        if not a.salida.lower().endswith(".gif"):
            a.salida = a.salida.rsplit(".", 1)[0] + ".gif"
        anim.save(a.salida, writer=PillowWriter(fps=a.fps))  # PillowWriter: cero dependencias
    plt.close(fig)
    print(f"OK {a.salida}")


if __name__ == "__main__":
    main()
