#!/usr/bin/env python3
"""editar_imagen.py — CLI de edicion de imagenes con Pillow (operaciones preestablecidas).

Uso: python editar_imagen.py <comando> ...
Comandos: info | recortar | redimensionar | filtro | transparencia | gif | contacto | superponer
Requiere: pip install pillow
"""
import argparse
import sys

from PIL import Image, ImageOps, ImageEnhance, ImageFilter

FILTROS = {
    "grayscale": lambda i: i.convert("L").convert("RGB"),
    "sepia": lambda i: ImageOps.colorize(i.convert("L"), "#704214", "#ffe9c9"),
    "blur": lambda i: i.filter(ImageFilter.GaussianBlur(4)),
    "sharp": lambda i: i.filter(ImageFilter.SHARPEN),
    "contour": lambda i: i.filter(ImageFilter.CONTOUR),
    "bright": lambda i: ImageEnhance.Brightness(i).enhance(1.3),
    "contrast": lambda i: ImageEnhance.Contrast(i).enhance(1.4),
    "posterizar": lambda i: i.quantize(colors=64).convert("RGB"),
}


def abrir(ruta):
    # exif_transpose: si no, recortes de fotos salen girados
    return ImageOps.exif_transpose(Image.open(ruta))


def cmd_info(a):
    im = Image.open(a.imagen)
    print(f"{a.imagen}: {im.size[0]}x{im.size[1]} modo={im.mode} formato={im.format}")


def cmd_recortar(a):
    x, y, w, h = (int(v) for v in a.box.split(","))
    im = abrir(a.imagen)
    if x < 0 or y < 0 or x + w > im.size[0] or y + h > im.size[1]:
        sys.exit(f"recorte fuera de limites: imagen es {im.size[0]}x{im.size[1]}")
    im.crop((x, y, x + w, y + h)).save(a.salida, optimize=True)


def cmd_redimensionar(a):
    im = abrir(a.imagen)
    if a.alto:
        size = (a.ancho, a.alto)
    else:
        size = (a.ancho, round(im.size[1] * a.ancho / im.size[0]))
    im.resize(size, Image.LANCZOS).save(a.salida, optimize=True)


def cmd_filtro(a):
    if a.filtro not in FILTROS:
        sys.exit(f"filtro desconocido: {a.filtro} (opciones: {', '.join(FILTROS)})")
    im = abrir(a.imagen).convert("RGB")
    FILTROS[a.filtro](im).save(a.salida, optimize=True)


def cmd_transparencia(a):
    im = abrir(a.imagen).convert("RGBA")
    c = a.color.lstrip("#")
    clave = tuple(int(c[i:i + 2], 16) for i in (0, 2, 4))
    px = im.load()
    for y in range(im.size[1]):
        for x in range(im.size[0]):
            r, g, b, _ = px[x, y]
            if abs(r - clave[0]) + abs(g - clave[1]) + abs(b - clave[2]) <= a.tolerancia * 3:
                px[x, y] = (r, g, b, 0)
    im.save(a.salida, optimize=True)


def cmd_gif(a):
    frames = [abrir(p).convert("RGB").quantize(colors=256, method=Image.MEDIANCUT)
              for p in a.imagenes]
    if not frames:
        sys.exit("gif: indica al menos un frame de entrada")
    frames[0].save(a.salida, save_all=True, append_images=frames[1:],
                   duration=a.duracion, loop=0, disposal=2)  # disposal=2: sin parpadeo
    print(f"{a.salida}: {len(frames)} frames")


def cmd_contacto(a):
    thumbs = [ImageOps.fit(abrir(p).convert("RGB"), (a.celda, a.celda)) for p in a.imagenes]
    cols = a.columnas
    filas = (len(thumbs) + cols - 1) // cols
    hoja = Image.new("RGB", (a.celda * cols, a.celda * filas), "white")
    for i, t in enumerate(thumbs):
        hoja.paste(t, (a.celda * (i % cols), a.celda * (i // cols)))
    hoja.save(a.salida, quality=90)


def cmd_superponer(a):
    base = abrir(a.imagen).convert("RGBA")
    capa = abrir(a.cap).convert("RGBA")
    if a.redimensionar:
        w = a.redimensionar
        capa = capa.resize((w, round(capa.size[1] * w / capa.size[0])), Image.LANCZOS)
    base.alpha_composite(capa, (a.x, a.y))
    base.save(a.salida, optimize=True)


def main():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = p.add_subparsers(dest="cmd", required=True)

    s = sub.add_parser("info", help="dimensiones, modo y formato")
    s.add_argument("imagen")

    s = sub.add_parser("recortar", help="recorte x,y,ancho,alto en px")
    s.add_argument("imagen"); s.add_argument("salida"); s.add_argument("--box", required=True,
                   metavar="X,Y,ANCHO,ALTO")

    s = sub.add_parser("redimensionar", help="cambio de tamano (conserva proporcion si no pides --alto)")
    s.add_argument("imagen"); s.add_argument("salida"); s.add_argument("--ancho", type=int, required=True)
    s.add_argument("--alto", type=int)

    s = sub.add_parser("filtro", help=f"filtro estetico: {', '.join(FILTROS)}")
    s.add_argument("imagen"); s.add_argument("salida"); s.add_argument("--filtro", required=True)

    s = sub.add_parser("transparencia", help="vuelve transparente un color de fondo")
    s.add_argument("imagen"); s.add_argument("salida")
    s.add_argument("--color", required=True, metavar='"#RRGGBB"'); s.add_argument("--tolerancia", type=int, default=30)

    s = sub.add_parser("gif", help="combina frames en un GIF animado")
    s.add_argument("salida"); s.add_argument("imagenes", nargs="+")
    s.add_argument("--duracion", type=int, default=400, help="ms por frame (def. 400)")

    s = sub.add_parser("contacto", help="hoja de contacto en rejilla (QA de lotes)")
    s.add_argument("salida"); s.add_argument("imagenes", nargs="+")
    s.add_argument("--celda", type=int, default=300); s.add_argument("--columnas", type=int, default=4)

    s = sub.add_parser("superponer", help="pinta una imagen sobre otra (marca de agua, stickers)")
    s.add_argument("imagen"); s.add_argument("cap"); s.add_argument("salida")
    s.add_argument("--x", type=int, default=0); s.add_argument("--y", type=int, default=0)
    s.add_argument("--redimensionar", type=int, help="ancho de la capa en px")

    args = p.parse_args()
    {"info": cmd_info, "recortar": cmd_recortar, "redimensionar": cmd_redimensionar,
     "filtro": cmd_filtro, "transparencia": cmd_transparencia, "gif": cmd_gif,
     "contacto": cmd_contacto, "superponer": cmd_superponer}[args.cmd](args)


if __name__ == "__main__":
    main()
