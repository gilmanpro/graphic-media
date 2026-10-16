#!/usr/bin/env python3
"""grafico.py — genera graficos de datos PNG/SVG listos para publicar a partir de CSV.

Requiere: pip install matplotlib
CSV de entrada: primera fila = encabezados; para scatter/hist basta con columnas numericas.

Uso:
  python grafico.py datos.csv --tipo bar --x mes --y ventas --titulo "Ventas 2026" -o ventas.png
  python grafico.py datos.csv --tipo line --x fecha --y visitas,conversion -o trafico.png
  python grafico.py datos.csv --tipo hist --y edad -o hist.png
  python grafico.py datos.csv --tipo pie --x region --y total -o pastel.png
  python grafico.py datos.csv --tipo scatter --x edad --y ingresos -o nube.png
Opciones: --transparente --dpi 300 --svg (salida vectorial) --xlabel/--ylabel
"""
import argparse
import csv
import sys

import matplotlib
matplotlib.use("Agg")  # sin display, obligatorio en servidores
import matplotlib.pyplot as plt

PALETA = ["#4F46E5", "#FF6B6B", "#10B981", "#F59E0B", "#8B5CF6", "#0EA5E9"]


def leer_csv(ruta):
    with open(ruta, newline="", encoding="utf-8-sig") as f:
        rows = list(csv.DictReader(f))
    if not rows:
        sys.exit(f"CSV vacio: {ruta}")
    return rows


def col(rows, nombre, numerica=False):
    vals = [r[nombre] for r in rows]
    if numerica:
        try:
            return [float(v.replace(",", ".")) for v in vals]
        except (ValueError, AttributeError):
            sys.exit(f"columna '{nombre}' no es numerica")
    return vals


def main():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("csv")
    p.add_argument("--tipo", required=True, choices=["bar", "line", "area", "scatter", "hist", "pie"])
    p.add_argument("--x", help="columna categorica/eje X")
    p.add_argument("--y", help="columna(s) numericas, separadas por coma")
    p.add_argument("--titulo"); p.add_argument("--xlabel"); p.add_argument("--ylabel")
    p.add_argument("-o", "--salida", default="grafico.png")
    p.add_argument("--transparente", action="store_true")
    p.add_argument("--dpi", type=int, default=300)
    p.add_argument("--svg", action="store_true", help="guardar como SVG en vez de PNG")
    p.add_argument("--ancho", type=float, default=8); p.add_argument("--alto", type=float, default=4.5)
    a = p.parse_args()

    if not a.y:
        sys.exit("indica --y (y --x salvo para hist)")
    rows = leer_csv(a.csv)
    ys = [c.strip() for c in a.y.split(",")]

    fig, ax = plt.subplots(figsize=(a.ancho, a.alto))

    if a.tipo == "hist":
        datos = col(rows, ys[0], numerica=True)
        ax.hist(datos, bins=30, color=PALETA[0], edgecolor="white")
    elif a.tipo == "pie":
        if not a.x:
            sys.exit("pie necesita --x (etiquetas) y --y (valores)")
        ax.pie(col(rows, ys[0], numerica=True), labels=col(rows, a.x),
               colors=PALETA, autopct="%1.1f%%", startangle=90)
    elif a.tipo == "scatter":
        xs = col(rows, a.x, numerica=True)
        ax.scatter(xs, col(rows, ys[0], numerica=True), s=28, alpha=0.75, color=PALETA[0])
    else:
        xs = col(rows, a.x) if a.x else list(range(len(rows)))
        for i, y in enumerate(ys):
            datos = col(rows, y, numerica=True)
            if a.tipo == "bar":
                ax.bar(xs, datos, color=PALETA[i % len(PALETA)], label=y)
            elif a.tipo == "line":
                ax.plot(xs, datos, linewidth=2, color=PALETA[i % len(PALETA)], label=y)
            elif a.tipo == "area":
                ax.stackplot(xs, datos, colors=[PALETA[i % len(PALETA)]], alpha=0.7, labels=[y])
        if len(ys) > 1:
            ax.legend()
        if a.tipo == "bar" and a.x and len(rows) > 12:
            plt.setp(ax.get_xticklabels(), rotation=45, ha="right")

    if a.titulo:
        ax.set_title(a.titulo)
    ax.set_xlabel(a.xlabel or (a.x or ""))
    ax.set_ylabel(a.ylabel or (ys[0] if a.tipo != "pie" else ""))
    ax.grid(True, alpha=0.3)
    fig.tight_layout()

    salida = a.salida if not a.svg else (a.salida.rsplit(".", 1)[0] + ".svg")
    if a.svg:
        fig.savefig(salida, bbox_inches="tight")
    else:
        fig.savefig(salida, dpi=a.dpi, transparent=a.transparente, bbox_inches="tight")
    plt.close(fig)
    print(f"OK {salida}")


if __name__ == "__main__":
    main()
