#!/usr/bin/env python3
"""svg_a_raster.py — convierte SVG a PNG/PDF con cadena de backends (no falla sin instalar todo).

Cadena: cairosvg (rapido) -> svglib+reportlab (PDF puro Python) -> inkscape/rsvg-convert (binarios).
Requiere al menos UNO: pip install cairosvg   |   pip install svglib reportlab   |   Inkscape/rsvg-convert.

Uso:
  python svg_a_raster.py entrada.svg -o salida.png --escala 2
  python svg_a_raster.py entrada.svg -o salida.pdf --ancho-px 1600
"""
import argparse
import os
import shutil
import subprocess
import sys


def con_cairosvg(src, dst, escala, ancho):
    try:
        import cairosvg
    except (ImportError, OSError):
        # ImportError: no instalado; OSError: falta la DLL/DLL nativa de Cairo
        return False
    kw = {"scale": escala} if escala else {}
    if ancho:
        kw = {"output_width": ancho}
    if dst.lower().endswith(".pdf"):
        cairosvg.svg2pdf(url=src, write_to=dst, **kw)
    else:
        cairosvg.svg2png(url=src, write_to=dst, **kw)
    return True


def con_svglib(src, dst, escala, ancho):
    try:
        from svglib.svglib import svg2rlg
        from reportlab.graphics import renderPDF, renderPM
    except (ImportError, OSError):
        return False
    d = svg2rlg(src)
    if d is None:
        sys.exit(f"svglib no pudo interpretar {src} (si usa mask/foreignObject usa cairosvg o inkscape)")
    if escala != 1:
        d.width *= escala; d.height *= escala; d.scale(escala, escala)
    if ancho:
        f = ancho / float(d.width)
        d.width *= f; d.height *= f; d.scale(f, f)
    if dst.lower().endswith(".pdf"):
        renderPDF.drawToFile(d, dst)
    else:
        renderPM.drawToFile(d, dst, fmt="PNG")  # requiere: pip install "svglib[bitmaps]"
    return True


def con_binario(src, dst, escala, ancho):
    binario, extra = None, []
    if shutil.which("inkscape"):
        binario, extra = "inkscape", ["--export-type=" + dst.rsplit(".", 1)[1],
                                      "--export-filename=" + dst]
    elif shutil.which("rsvg-convert"):
        binario, extra = "rsvg-convert", ["-o", dst]
        if ancho:
            extra += ["-w", str(ancho)]
    if not binario:
        return False
    subprocess.run([binario, src] + extra, check=True)
    return True


def main():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("entrada")
    p.add_argument("-o", "--salida", required=True)
    p.add_argument("--escala", type=float, default=1, help="multiplicador (def. 1; p.ej. 2 = doble resolucion)")
    p.add_argument("--ancho-px", type=int, help="ancho de salida en px")
    a = p.parse_args()

    if not os.path.exists(a.entrada):
        sys.exit(f"no existe: {a.entrada}")
    for intento in (lambda: con_cairosvg(a.entrada, a.salida, a.escala, a.ancho_px),
                    lambda: con_svglib(a.entrada, a.salida, a.escala, a.ancho_px),
                    lambda: con_binario(a.entrada, a.salida, a.escala, a.ancho_px)):
        if intento():
            print(f"OK {a.salida}")
            return
    sys.exit("sin backend: instala 'pip install cairosvg' (recomendado), "
             "'pip install svglib reportlab' o Inkscape/rsvg-convert")


if __name__ == "__main__":
    main()
