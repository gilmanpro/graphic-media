#!/usr/bin/env python3
"""plano_2d.py — genera un plano 2D a escala (SVG) desde un spec JSON de habitaciones.

Uso:
  python plano_2d.py plano.json -o plano.svg
  python plano_2d.py plano.json -o plano.svg --abrir   (abre en el navegador para revisar)

Spec JSON (unidades en cm, escala declarada en el cajetín):
{
  "titulo": "Apartamento 8x6",
  "escala": "1:50",
  "ancho": 800, "alto": 600,
  "habitaciones": [
    {"nombre": "Sala", "x": 0,   "y": 0, "w": 450, "h": 350},
    {"nombre": "Dorm", "x": 450, "y": 0, "w": 350, "h": 350},
    {"nombre": "Bano", "x": 0,   "y": 350, "w": 300, "h": 250}
  ]
}
Capas: rejilla -> muros -> habitaciones -> cotas -> textos -> cajetin
"""
import argparse
import json
import os
import sys
import webbrowser

MARGEN = 60  # px de margen para cotas y cajetin


def svg_escapar(t):
    return t.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def main():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("spec")
    p.add_argument("-o", "--salida", default="plano.svg")
    p.add_argument("--abrir", action="store_true")
    a = p.parse_args()

    spec = json.load(open(a.spec, encoding="utf-8"))
    hab = spec.get("habitaciones", [])
    if not hab:
        sys.exit("spec sin 'habitaciones'")
    W, H = spec.get("ancho", 800), spec.get("alto", 600)
    lienzo_w, lienzo_h = W + 2 * MARGEN, H + 2 * MARGEN + 40  # + cajetin
    ox, oy = MARGEN, MARGEN

    out = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {lienzo_w} {lienzo_h}" '
           f'role="img" font-family="sans-serif">',
           f'<title>{svg_escapar(spec.get("titulo", "Plano"))} — escala '
           f'{svg_escapar(spec.get("escala", "1:50"))}</title>',
           f'<rect width="{lienzo_w}" height="{lienzo_h}" fill="#fff"/>']

    # 1) rejilla cada 50 cm
    out.append('<g stroke="#E5E7EB" stroke-width="1">')
    x = 0
    while x <= W:
        out.append(f'<line x1="{ox + x}" y1="{oy}" x2="{ox + x}" y2="{oy + H}"/>'); x += 50
    y = 0
    while y <= H:
        out.append(f'<line x1="{ox}" y1="{oy + y}" x2="{ox + W}" y2="{oy + y}"/>'); y += 50
    out.append('</g>')

    # 2) muros exteriores (trazo grueso)
    out.append(f'<rect x="{ox}" y="{oy}" width="{W}" height="{H}" fill="none" '
               f'stroke="#111" stroke-width="6"/>')

    # 3) habitaciones
    for r in hab:
        out.append(f'<rect x="{ox + r["x"]}" y="{oy + r["y"]}" width="{r["w"]}" height="{r["h"]}" '
                   f'fill="none" stroke="#111" stroke-width="3"/>')
        cx = ox + r["x"] + r["w"] / 2
        cy = oy + r["y"] + r["h"] / 2
        out.append(f'<text x="{cx}" y="{cy}" font-size="18" text-anchor="middle" fill="#111">'
                   f'{svg_escapar(r["nombre"])}</text>')
        out.append(f'<text x="{cx}" y="{cy + 18}" font-size="12" text-anchor="middle" fill="#666">'
                   f'{r["w"]}x{r["h"]} cm</text>')

    # 4) cotas (exterior inferior y lateral)
    out.append('<g stroke="#666" stroke-width="1" fill="#666" font-size="14">')
    cy = oy + H + 24
    out.append(f'<line x1="{ox}" y1="{cy}" x2="{ox + W}" y2="{cy}"/>')
    out.append(f'<line x1="{ox}" y1="{cy - 6}" x2="{ox}" y2="{cy + 6}"/>')
    out.append(f'<line x1="{ox + W}" y1="{cy - 6}" x2="{ox + W}" y2="{cy + 6}"/>')
    out.append(f'<text x="{ox + W / 2}" y="{cy - 8}" text-anchor="middle" stroke="none">'
               f'{W} cm</text>')
    cx = ox - 24
    out.append(f'<line x1="{cx}" y1="{oy}" x2="{cx}" y2="{oy + H}"/>')
    out.append(f'<text x="{cx - 8}" y="{oy + H / 2}" text-anchor="middle" stroke="none" '
               f'transform="rotate(-90 {cx - 8} {oy + H / 2})">{H} cm</text>')
    out.append('</g>')

    # 5) cajetin
    ty = oy + H + 48
    out.append(f'<g font-size="14" fill="#111">'
               f'<text x="{ox}" y="{ty}">{svg_escapar(spec.get("titulo", "Plano"))}</text>'
               f'<text x="{ox + 260}" y="{ty}">Escala: {svg_escapar(spec.get("escala", "1:50"))}</text>'
               f'<text x="{ox + 440}" y="{ty}">Unidades: cm</text></g>')
    out.append('</svg>')

    open(a.salida, "w", encoding="utf-8").write("\n".join(out))
    print(f"OK {a.salida}")
    if a.abrir:
        webbrowser.open(os.path.abspath(a.salida))


if __name__ == "__main__":
    main()
