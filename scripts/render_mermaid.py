#!/usr/bin/env python3
"""render_mermaid.py — renderiza un fichero .mmd (o un bloque ```mermaid de Markdown) a SVG/PNG.

Requiere: npm install -g @mermaid-js/mermaid-cli  (comando 'mmdc'; con npx funciona sin instalar global)
Uso:
  python render_mermaid.py diagrama.mmd -o diagrama.svg
  python render_mermaid.py leer.md -o diagrama.png --ancho 1600 --tema dark
Si el origen es .md, extrae el PRIMER bloque ```mermaid del fichero.
Temas: default | dark | forest | neutral | base
"""
import argparse
import os
import re
import shutil
import subprocess
import sys
import tempfile


def extraer_mermaid(ruta):
    if ruta.lower().endswith((".mmd", ".mermaid")):
        return open(ruta, encoding="utf-8").read()
    texto = open(ruta, encoding="utf-8").read()
    m = re.search(r"```mermaid\s*\n(.*?)```", texto, re.S)
    if not m:
        sys.exit(f"no se encontro bloque ```mermaid en {ruta}")
    return m.group(1)


def main():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("entrada", help=".mmd o .md con bloque mermaid")
    p.add_argument("-o", "--salida", required=True)
    p.add_argument("--ancho", type=int, default=1200)
    p.add_argument("--tema", default="default")
    p.add_argument("--fondo", default="white")
    a = p.parse_args()

    if not os.path.exists(a.entrada):
        sys.exit(f"no existe: {a.entrada}")
    mmdc = shutil.which("mmdc")
    if not mmdc:
        sys.exit("falta mermaid-cli: npm install -g @mermaid-js/mermaid-cli  "
                 "(o ejecuta: npx -y @mermaid-js/mermaid-cli ...)")

    estilo = {"theme": a.tema, "themeVariables": {"background": a.fondo}}
    with tempfile.NamedTemporaryFile("w", suffix=".mmd", delete=False,
                                     encoding="utf-8") as tf:
        tf.write(extraer_mermaid(a.entrada))
        mmd_path = tf.name
    cfg = tempfile.NamedTemporaryFile("w", suffix=".json", delete=False,
                                      encoding="utf-8")
    import json
    json.dump(estilo, cfg); cfg.close()

    cmd = [mmdc, "-i", mmd_path, "-o", a.salida, "-w", str(a.ancho), "-c", cfg.name]
    r = subprocess.run(cmd, capture_output=True, text=True)
    os.unlink(mmd_path); os.unlink(cfg.name)
    if r.returncode != 0:
        sys.exit(f"mmdc fallo:\n{r.stderr.strip()}\n"
                 "Errores tipicos: parentesis sin comillas en A[texto (x)] o subgrafos sin 'end'")
    print(f"OK {a.salida}")


if __name__ == "__main__":
    main()
