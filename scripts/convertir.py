#!/usr/bin/env python3
"""convertir.py — cambio de extencion UNICO para imagen, video y audio.

Detecta el tipo por la extencion de entrada y enruta al motor adecuado:
  imagen -> Pillow (png, jpg, webp, bmp, tif, ico, gif) o svg_a_raster (svg)
  video  -> scripts/video.py (mp4, webm, mov, mkv, avi, gif)
  audio  -> scripts/audio.py (mp3, wav, flac, ogg, m4a, aac, opus)

Uso:
  python scripts/convertir.py foto.png -o foto.webp
  python scripts/convertir.py clip.mov -o clip.mp4 --crf 20
  python scripts/convertir.py cancion.wav -o cancion.mp3 --bitrate 192k
  python scripts/convertir.py logo.svg -o logo.png --escala 2
Opciones: --calidad N (imagen lossy 1-100), --crf N (video), --bitrate X (audio),
          --escala N (svg), --ancho N (gif de video)
"""
import argparse
import os
import subprocess
import sys

AQUI = os.path.dirname(os.path.abspath(__file__))

IMAGEN_EXTS = {"png", "jpg", "jpeg", "webp", "bmp", "tif", "tiff", "ico", "gif", "ppm", "pgm"}
VIDEO_EXTS = {"mp4", "webm", "mov", "mkv", "avi", "gif"}
AUDIO_EXTS = {"mp3", "wav", "flac", "ogg", "m4a", "aac", "opus", "wma"}
SIN_PERDIDA = {"png", "bmp", "tif", "tiff", "ppm", "pgm", "wav", "flac"}


def ext(ruta):
    return os.path.splitext(ruta)[1].lstrip(".").lower()


def convertir_imagen(entrada, salida, calidad, escala):
    from PIL import Image, ImageOps
    if ext(entrada) == "svg":
        cmd = [sys.executable, os.path.join(AQUI, "svg_a_raster.py"), entrada, "-o", salida]
        if escala != 1:
            cmd += ["--escala", str(escala)]
        r = subprocess.run(cmd)   # sin check: svg_a_raster ya explica qué instalar
        sys.exit(r.returncode)
    im = ImageOps.exif_transpose(Image.open(entrada))
    formato = ext(salida)
    guardar = {}
    if formato in ("jpg", "jpeg"):
        im = im.convert("RGB")
        guardar = {"quality": calidad}
    elif formato == "webp":
        guardar = {"quality": calidad}
    elif formato == "ico":
        guardar = {"sizes": [(s, s) for s in (16, 32, 48, 64, 128, 256)
                             if s <= max(im.size)]}
    elif formato == "gif" and im.mode != "P":
        # gif estatico: primera paleta; para GIF animado usar video.py/ editar_imagen.py gif
        im = im.convert("P", palette=Image.ADAPTIVE)
    if formato in SIN_PERDIDA and formato != "gif":
        guardar = {}
    im.save(salida, **guardar)


def main():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("entrada")
    p.add_argument("-o", "--salida", required=True, help="ruta de salida con la extencion destino")
    p.add_argument("--calidad", type=int, default=90, help="imagen lossy: 1-100 (def. 90)")
    p.add_argument("--crf", type=int, default=23, help="video: calidad x264 (18-28)")
    p.add_argument("--bitrate", default="192k", help="audio lossy (def. 192k)")
    p.add_argument("--escala", type=float, default=1, help="svg: multiplicador")
    p.add_argument("--ancho", type=int, default=480, help="gif de video: ancho")
    a = p.parse_args()

    if not os.path.exists(a.entrada):
        sys.exit(f"no existe: {a.entrada}")
    src, dst = ext(a.entrada), ext(a.salida)
    if not dst:
        sys.exit("la salida debe llevar extension (p. ej. -o salida.mp4)")
    if src == dst:
        sys.exit(f"misma extension: {src}")

    # enrutado por tipo de ORIGEN (svg -> imagen; gif origen -> video: GIF animado)
    if src == "svg" or (src in IMAGEN_EXTS and src != "gif"):
        convertir_imagen(a.entrada, a.salida, a.calidad, a.escala)
    elif src in AUDIO_EXTS:
        subprocess.run([sys.executable, os.path.join(AQUI, "audio.py"), "convertir",
                        a.entrada, "-o", a.salida, "--bitrate", a.bitrate], check=True)
        return
    elif src in VIDEO_EXTS:
        cmd = [sys.executable, os.path.join(AQUI, "video.py"), "convertir",
               a.entrada, "-o", a.salida, "--crf", str(a.crf)]
        subprocess.run(cmd, check=True)
        return
    else:
        sys.exit(f"combinacion no soportada: {src} -> {dst}")
    print(f"OK {a.salida}")


if __name__ == "__main__":
    main()
