#!/usr/bin/env python3
"""audio.py — herramientas de audio con FFmpeg (convertir, normalizar, recortar, silencios, mezcla).

Requiere: FFmpeg en el PATH (Windows: winget install Gyan.FFmpeg)
Uso: python scripts/audio.py <comando> ...
  info          -> duracion, codecs, canales, pico/LUFS
  convertir     -> mp3, wav, flac, ogg, m4a, aac, opus
  recortar      -> corte por tiempo
  normalizar    -> loudnorm EBU R128 en dos pasadas (podcast -16 LUFS / radiodifusion -23)
  volumen       -> ganancia en dB
  silencios     -> recorta silencios del principio/final (y internos opcionales)
  extraer       -> sacar pista de audio de un video
  unir          -> concatenar varios audios
  forma         -> imagen de la onda (waveform) PNG
  fundir        -> mezclar dos pistas (voz sobre fondo, con ducking automatico)
"""
import argparse
import json
import os
import re
import shutil
import subprocess
import sys

CODECS = {"mp3": ("libmp3lame", ["-b:a", "{br}"]), "wav": ("pcm_s16le", []),
          "flac": ("flac", []), "ogg": ("libvorbis", []),
          "m4a": ("aac", ["-b:a", "{br}"]), "aac": ("aac", ["-b:a", "{br}"]),
          "opus": ("libopus", ["-b:a", "{br}"])}


def ff(nombre):
    exe = shutil.which(nombre)
    if not exe:
        sys.exit(f"falta {nombre}: instala FFmpeg (Windows: winget install Gyan.FFmpeg)")
    return exe


def run(args):
    r = subprocess.run(args, capture_output=True, text=True, encoding="utf-8",
                       errors="replace")
    if r.returncode != 0:
        tail = "\n".join((r.stderr or "").strip().splitlines()[-12:])
        sys.exit(f"ffmpeg fallo:\n{tail}")
    return r


def salida(a, defecto):
    if not a.salida:
        a.salida = os.path.splitext(a.entrada)[0] + "." + defecto
    return a.salida


def cmd_info(a):
    r = run([ff("ffprobe"), "-v", "error", "-print_format", "json",
             "-show_format", "-show_streams", a.entrada])
    j = json.loads(r.stdout)
    print(f"{a.entrada}: {j['format'].get('duration', '?')}s "
          f"{j['format'].get('format_name', '?')} "
          f"{round(float(j['format'].get('size', 0)) / 1e6, 2)} MB")
    for s in j["streams"]:
        print(f"  {s['codec_name']} {s.get('sample_rate')}Hz {s.get('channels')}ch "
              f"{s.get('bit_rate', '?')}bps")


def cmd_convertir(a):
    ext = os.path.splitext(a.salida)[1].lstrip(".").lower() if a.salida else "mp3"
    out = salida(a, "mp3")
    ext = os.path.splitext(out)[1].lstrip(".").lower()
    if ext not in CODECS:
        sys.exit(f"extencion de audio no soportada: {ext} ({', '.join(CODECS)})")
    codec, extra = CODECS[ext]
    cmd = [ff("ffmpeg"), "-y", "-i", a.entrada, "-vn", "-c:a", codec]
    cmd += [x.format(br=a.bitrate) for x in extra]
    cmd.append(out)
    run(cmd)
    print(f"OK {out}")


def cmd_recortar(a):
    out = salida(a, "mp3")
    cmd = [ff("ffmpeg"), "-y", "-ss", str(a.inicio), "-i", a.entrada]
    if a.duracion:
        cmd += ["-t", str(a.duracion)]
    cmd += ["-c:a", "copy", out]
    run(cmd)
    print(f"OK {out}")


def medir_lufs(entrada):
    r = run([ff("ffmpeg"), "-i", entrada, "-af",
              "loudnorm=I=-16:TP=-1.5:LRA=11:print_format=json", "-f", "null", "-"])
    bloques = re.findall(r"\{[^{}]*\}", r.stderr)
    return json.loads(bloques[-1])


def cmd_normalizar(a):
    out = salida(a, "mp3")
    objetivo = a.lufs
    m = medir_lufs(a.entrada)  # pasada 1: medir
    af = (f"loudnorm=I={objetivo}:TP={a.tp}:LRA=11:"
          f"measured_I={m['input_i']}:measured_TP={m['input_tp']}:"
          f"measured_LRA={m['input_lra']}:measured_thresh={m['input_thresh']}:"
          f"offset={m['target_offset']}:linear=true")  # pasada 2: aplicar
    run([ff("ffmpeg"), "-y", "-i", a.entrada, "-af", af, "-ar", "48000",
         "-c:a", "libmp3lame", "-b:a", "192k", out])
    print(f"OK {out} (objetivo {objetivo} LUFS; medido {m['input_i']} LUFS)")


def cmd_volumen(a):
    out = salida(a, "mp3")
    run([ff("ffmpeg"), "-y", "-i", a.entrada, "-af",
         f"volume={a.db}dB", "-c:a", "libmp3lame", "-b:a", "192k", out])
    print(f"OK {out}")


def cmd_silencios(a):
    out = salida(a, "mp3")
    # borra silencios iniciales/finales; con --internos tambien los del medio
    if a.internos:
        filt = ("silenceremove=start_periods=1:start_threshold=-50dB:"
                "start_silence=0.3,areverse,"
                "silenceremove=start_periods=1:start_threshold=-50dB:"
                "start_silence=0.3,areverse,"
                "silenceremove=start_periods=1:start_threshold=-50dB:"
                "start_duration=0.2")
    else:
        filt = ("silenceremove=start_periods=1:start_threshold=-50dB:"
                "start_silence=0.3,areverse,"
                "silenceremove=start_periods=1:start_threshold=-50dB:"
                "start_silence=0.3,areverse")
    run([ff("ffmpeg"), "-y", "-i", a.entrada, "-af", filt,
         "-c:a", "libmp3lame", "-b:a", "192k", out])
    print(f"OK {out}")


def cmd_extraer(a):
    out = salida(a, "wav")
    run([ff("ffmpeg"), "-y", "-i", a.entrada, "-vn", out])
    print(f"OK {out}")


def cmd_unir(a):
    lista = "lista_audio.txt"
    with open(lista, "w", encoding="utf-8") as f:
        for e in a.entradas:
            f.write(f"file '{os.path.abspath(e)}'\n")
    out = a.salida or "unido.mp3"
    run([ff("ffmpeg"), "-y", "-f", "concat", "-safe", "0", "-i", lista,
         "-c:a", "libmp3lame", "-b:a", "192k", out])
    os.unlink(lista)
    print(f"OK {out}")


def cmd_forma(a):
    out = salida(a, "png")
    run([ff("ffmpeg"), "-y", "-i", a.entrada, "-filter_complex",
         "showwavespic=s=1200x300:colors=#4F46E5", out])
    print(f"OK {out}")


def cmd_fundir(a):
    # voz arriba; el fondo baja automaticamente (ducking) mientras suena la voz
    out = salida(a, "mp3")
    filt = ("[1:a]volume=1.0[fondo];[fondo][0:a]sidechaincompress="
            "threshold=0.03:ratio=8:attack=20:release=300[m];"
            "[0:a][m]amix=inputs=2:duration=first:dropout_transition=0")
    run([ff("ffmpeg"), "-y", "-i", a.voz, "-i", a.fondo, "-filter_complex", filt,
         "-c:a", "libmp3lame", "-b:a", "192k", out])
    print(f"OK {out}")


def main():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = p.add_subparsers(dest="cmd", required=True)

    s = sub.add_parser("info"); s.add_argument("entrada")

    s = sub.add_parser("convertir"); s.add_argument("entrada")
    s.add_argument("-o", "--salida"); s.add_argument("--bitrate", default="192k")

    s = sub.add_parser("recortar"); s.add_argument("entrada"); s.add_argument("-o", "--salida")
    s.add_argument("--inicio", type=float, required=True)
    s.add_argument("--duracion", type=float)

    s = sub.add_parser("normalizar"); s.add_argument("entrada"); s.add_argument("-o", "--salida")
    s.add_argument("--lufs", type=float, default=-16,
                   help="-16 podcast/streaming (def.), -23 radiodifusion EBU")
    s.add_argument("--tp", type=float, default=-1.5, help="pico maximo dBTP")

    s = sub.add_parser("volumen"); s.add_argument("entrada"); s.add_argument("-o", "--salida")
    s.add_argument("--db", type=float, required=True)

    s = sub.add_parser("silencios"); s.add_argument("entrada"); s.add_argument("-o", "--salida")
    s.add_argument("--internos", action="store_true")

    s = sub.add_parser("extraer"); s.add_argument("entrada"); s.add_argument("-o", "--salida")
    s = sub.add_parser("unir"); s.add_argument("entradas", nargs="+")
    s.add_argument("-o", "--salida")
    s = sub.add_parser("forma"); s.add_argument("entrada"); s.add_argument("-o", "--salida")

    s = sub.add_parser("fundir"); s.add_argument("voz"); s.add_argument("fondo")
    s.add_argument("-o", "--salida")

    a = p.parse_args()
    {"info": cmd_info, "convertir": cmd_convertir, "recortar": cmd_recortar,
     "normalizar": cmd_normalizar, "volumen": cmd_volumen, "silencios": cmd_silencios,
     "extraer": cmd_extraer, "unir": cmd_unir, "forma": cmd_forma,
     "fundir": cmd_fundir}[a.cmd](a)


if __name__ == "__main__":
    main()
