#!/usr/bin/env python3
"""video.py — herramientas de video con FFmpeg (convertir, recortar, filtros, denoise, frames, gif).

Requiere: FFmpeg en el PATH (Windows: winget install Gyan.FFmpeg)
Uso: python scripts/video.py <comando> ...
  info        -> duracion, resolucion, fps, codecs
  convertir   -> cambio de contenedor/extencion (mp4, webm, mov, mkv, avi, gif)
  recortar    -> corte por tiempo
  redimensionar -> escala conservando aspecto
  filtro      -> grayscale|sepia|blur|brillo|contraste|denoise|nitidez
  comprimir   -> reducir tamano (CRF)
  frames      -> video a secuencia PNG
  gif         -> video a GIF de calidad (paleta doble pasada)
  ensamblar   -> secuencia PNG a MP4
  silenciar   -> quitar pista de audio
  extraer-audio -> sacar la pista de audio
"""
import argparse
import json
import os
import shutil
import subprocess
import sys

VIDEO_EXTS = {"mp4": "libx264", "webm": "libvpx-vp9", "mov": "libx264",
              "mkv": "libx264", "avi": "mpeg4"}


def ff(nombre):
    exe = shutil.which(nombre)
    if not exe:
        sys.exit(f"falta {nombre}: instala FFmpeg (Windows: winget install Gyan.FFmpeg)")
    return exe


def run(args, entrada=None):
    r = subprocess.run(args, capture_output=True, text=True, encoding="utf-8",
                       errors="replace")
    if r.returncode != 0:
        tail = "\n".join((r.stderr or "").strip().splitlines()[-12:])
        sys.exit(f"ffmpeg fallo:\n{tail}")
    return r


def salida(a, defecto_ext):
    if not a.salida:
        base = os.path.splitext(a.entrada)[0]
        a.salida = base + "." + defecto_ext
    return a.salida


def cmd_info(a):
    r = run([ff("ffprobe"), "-v", "error", "-print_format", "json",
             "-show_format", "-show_streams", a.entrada])
    j = json.loads(r.stdout)
    print(f"{a.entrada}: {j['format'].get('duration', '?')}s "
          f"{j['format'].get('format_name', '?')} "
          f"{round(float(j['format'].get('size', 0)) / 1e6, 2)} MB")
    for s in j["streams"]:
        if s["codec_type"] == "video":
            try:
                num, den = s.get("avg_frame_rate", "0/1").split("/")
                fps = float(num) / float(den) if float(den) else 0.0
            except (ValueError, ZeroDivisionError):
                fps = 0.0
            print(f"  video: {s['width']}x{s['height']} {s['codec_name']} {fps:.0f}fps")
        elif s["codec_type"] == "audio":
            print(f"  audio: {s['codec_name']} {s.get('sample_rate')}Hz "
                  f"{s.get('channels')}ch")


def cmd_convertir(a):
    out = salida(a, "mp4")
    ext = os.path.splitext(out)[1].lstrip(".").lower()
    if ext == "gif":
        return cmd_gif(a)
    if ext not in VIDEO_EXTS:
        sys.exit(f"extencion de video no soportada: {ext} ({', '.join(sorted(VIDEO_EXTS))})")
    cmd = [ff("ffmpeg"), "-y", "-i", a.entrada, "-c:v", VIDEO_EXTS[ext]]
    if VIDEO_EXTS[ext] == "libx264":
        cmd += ["-pix_fmt", "yuv420p", "-crf", str(a.crf)]
    else:
        cmd += ["-b:v", "0", "-crf", str(a.crf)]
    cmd += ["-c:a", "aac" if ext in ("mp4", "mov", "mkv") else "libopus", out]
    run(cmd)
    print(f"OK {out}")


def cmd_recortar(a):
    out = salida(a, "mp4")
    cmd = [ff("ffmpeg"), "-y", "-ss", str(a.inicio), "-i", a.entrada]
    if a.duracion:
        cmd += ["-t", str(a.duracion)]
    cmd += ["-c", "copy", out]  # corte clave a clave; sin re-codificar
    run(cmd)
    print(f"OK {out}")


def cmd_redimensionar(a):
    out = salida(a, "mp4")
    # divisibles por 2: requisito de x264/yuv420p
    vf = f"scale={a.ancho}:-2:flags=lanczos"
    run([ff("ffmpeg"), "-y", "-i", a.entrada, "-vf", vf,
         "-c:v", "libx264", "-crf", str(a.crf), "-pix_fmt", "yuv420p",
         "-c:a", "copy", out])
    print(f"OK {out}")


FILTROS = {
    "grayscale": "hue=s=0",
    "sepia": "colorchannelmixer=.393:.769:.189:0:.349:.686:.168:0:.272:.534:.131",
    "blur": "gblur=sigma=3",
    "brillo": "eq=brightness=0.08",
    "contraste": "eq=contrast=1.25",
    "denoise": "hqdn3d=3:3:6:6",          # ruido de sensor/compresion
    "denoise-fuerte": "nlmeans=s=7:p=7:r=15",
    "nitidez": "unsharp=5:5:0.8:5:5:0.0",
}


def cmd_filtro(a):
    if a.filtro not in FILTROS:
        sys.exit(f"filtro desconocido: {a.filtro} (opciones: {', '.join(FILTROS)})")
    out = salida(a, "mp4")
    run([ff("ffmpeg"), "-y", "-i", a.entrada, "-vf", FILTROS[a.filtro],
         "-c:v", "libx264", "-crf", str(a.crf), "-pix_fmt", "yuv420p",
         "-c:a", "copy", out])
    print(f"OK {out}")


def cmd_comprimir(a):
    out = salida(a, "mp4")
    run([ff("ffmpeg"), "-y", "-i", a.entrada, "-c:v", "libx264",
         "-crf", str(a.crf), "-preset", "slow", "-pix_fmt", "yuv420p",
         "-c:a", "aac", "-b:a", "128k", out])
    print(f"OK {out}")


def cmd_frames(a):
    os.makedirs(a.carpeta, exist_ok=True)
    pat = os.path.join(a.carpeta, "frame%04d.png")
    cmd = [ff("ffmpeg"), "-y", "-i", a.entrada]
    if a.fps:
        cmd += ["-vf", f"fps={a.fps}"]
    cmd += [pat]
    run(cmd)
    print(f"OK {a.carpeta} ({len(os.listdir(a.carpeta))} frames)")


def cmd_gif(a):
    out = salida(a, "gif")
    fps = str(getattr(a, "fps", 12))
    ancho = getattr(a, "ancho", 480)
    # paleta doble pasada: sin bandas de color (el -y encadena los dos filtros)
    run([ff("ffmpeg"), "-y", "-i", a.entrada, "-vf",
         f"fps={fps},scale={ancho}:-1:flags=lanczos,split[s0][s1];"
         f"[s0]palettegen=max_colors=256[p];[s1][p]paletteuse=dither=bayer:bayer_scale=5",
         out])
    print(f"OK {out}")


def cmd_ensamblar(a):
    if not any(f.endswith(".png") for f in os.listdir(a.carpeta)):
        sys.exit(f"no hay .png en {a.carpeta}")
    pat = os.path.join(a.carpeta, "frame%04d.png")
    out = salida(a, "mp4")
    run([ff("ffmpeg"), "-y", "-framerate", str(a.fps), "-i", pat,
         "-c:v", "libx264", "-crf", str(a.crf), "-pix_fmt", "yuv420p", out])
    print(f"OK {out}")


def cmd_silenciar(a):
    out = salida(a, "mp4")
    run([ff("ffmpeg"), "-y", "-i", a.entrada, "-c:v", "copy", "-an", out])
    print(f"OK {out}")


def cmd_extraer_audio(a):
    ext = os.path.splitext(a.salida)[1].lstrip(".").lower() if a.salida else "wav"
    out = salida(a, "wav")
    codec = {"mp3": "libmp3lame", "flac": "flac", "wav": "pcm_s16le",
             "ogg": "libvorbis", "m4a": "aac", "aac": "aac"}.get(ext)
    if not codec:
        sys.exit(f"extencion de audio no soportada: {ext}")
    cmd = [ff("ffmpeg"), "-y", "-i", a.entrada, "-vn", "-c:a", codec, out]
    if ext == "mp3":
        cmd += ["-b:a", "192k"]
    run(cmd)
    print(f"OK {out}")


def main():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = p.add_subparsers(dest="cmd", required=True)

    def comun(s, defecto=None):
        s.add_argument("entrada")
        s.add_argument("-o", "--salida", default=defecto)
        s.add_argument("--crf", type=int, default=23,
                       help="calidad x264: 18 excelente, 23 def., 28 comprimido")

    s = sub.add_parser("info"); s.add_argument("entrada")
    s = sub.add_parser("convertir"); comun(s)
    s = sub.add_parser("recortar"); comun(s)
    s.add_argument("--inicio", type=float, required=True, help="segundos")
    s.add_argument("--duracion", type=float, help="segundos")
    s = sub.add_parser("redimensionar"); comun(s)
    s.add_argument("--ancho", type=int, required=True)
    s = sub.add_parser("filtro"); comun(s)
    s.add_argument("--filtro", required=True, help=f"{', '.join(FILTROS)}")
    s = sub.add_parser("comprimir"); comun(s)
    s = sub.add_parser("frames"); s.add_argument("entrada")
    s.add_argument("--carpeta", default="frames")
    s.add_argument("--fps", type=float, default=0, help="extraer a N fps (def. todos)")
    s = sub.add_parser("gif"); comun(s, defecto=None)
    s.add_argument("--fps", type=int, default=12)
    s.add_argument("--ancho", type=int, default=480)
    s = sub.add_parser("ensamblar"); comun(s)
    s.add_argument("--carpeta", default="frames")
    s.add_argument("--fps", type=int, default=24)
    s = sub.add_parser("silenciar"); comun(s)
    s = sub.add_parser("extraer-audio"); comun(s, defecto=None)

    a = p.parse_args()
    {"info": cmd_info, "convertir": cmd_convertir, "recortar": cmd_recortar,
     "redimensionar": cmd_redimensionar, "filtro": cmd_filtro,
     "comprimir": cmd_comprimir, "frames": cmd_frames, "gif": cmd_gif,
     "ensamblar": cmd_ensamblar, "silenciar": cmd_silenciar,
     "extraer-audio": cmd_extraer_audio}[a.cmd](a)


if __name__ == "__main__":
    main()
