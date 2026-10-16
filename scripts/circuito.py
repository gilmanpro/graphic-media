#!/usr/bin/env python3
"""circuito.py — genera circuitos eléctricos preestablecidos (símbolos IEC) a SVG/PNG.

Requiere: pip install schemdraw
Uso:
  python circuito.py --tipo rc -o rc.svg
  python circuito.py --tipo rlc -o rlc.png
  python circuito.py --tipo led -o led.svg --etiquetas "R1=220Ω, D1=rojo"
Tipos: rc | rlc | led | divisor | puente   (ver --help para la descripción de cada uno)
El PNG pasa por svg_a_raster.py si no hay backend directo de schemdraw.
"""
import argparse
import sys


def construir(tipo, etiquetas):
    try:
        import schemdraw
        import schemdraw.elements as elm
    except ImportError:
        sys.exit("falta schemdraw: pip install schemdraw")
    d = schemdraw.Drawing(unit=2.5)

    if tipo == "rc":  # paso bajo RC clásico
        d += elm.Dot(open=True).label("Vin", loc="left")
        d += elm.Resistor().right().label(etiquetas.get("R", "10kΩ"))
        d += elm.Capacitor().down().label(etiquetas.get("C", "100nF"))
        d += elm.Ground()
        d += elm.Line().left(d.unit * 2)
        d += elm.Line().up(d.unit * 0.5)
        d += elm.Dot().label("Vout", loc="right")
        d += elm.Line().right()
        d += elm.Dot(open=True)
    elif tipo == "rlc":  # serie RLC
        d += elm.Dot(open=True).label("Vin", loc="left")
        d += elm.Resistor().right().label(etiquetas.get("R", "1kΩ"))
        d += elm.Inductor().right().label(etiquetas.get("L", "10mH"))
        d += elm.Capacitor().down().label(etiquetas.get("C", "10nF"))
        d += elm.Ground()
    elif tipo == "led":  # LED con resistencia de limitación
        d += elm.Dot(open=True).label("+5V", loc="left")
        d += elm.Resistor().down().label(etiquetas.get("R", "220Ω"))
        d += elm.LED().down().label(etiquetas.get("D", "D1"))
        d += elm.Ground()
    elif tipo == "divisor":  # divisor de tensión con toma central
        d += elm.Dot(open=True).label("Vin", loc="left")
        d += elm.Resistor().down().label(etiquetas.get("R1", "10kΩ"))
        n = d.add(elm.Dot().label("Vout", loc="right"))
        d += elm.Resistor().down().label(etiquetas.get("R2", "10kΩ"))
        d += elm.Ground()
        d += n
    elif tipo == "puente":  # puente de Wheatstone
        d += elm.Resistor().right().label(etiquetas.get("R1", "1kΩ"))
        d += elm.Resistor().down().label(etiquetas.get("R2", "1kΩ"))
        d += elm.Resistor().left().label(etiquetas.get("R3", "1kΩ"))
        d += elm.Resistor().up().label(etiquetas.get("R4", "1kΩ"))
        d += elm.Ground().at(d.center).toy(3)
    else:
        sys.exit(f"tipo desconocido: {tipo}")
    return d


def main():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--tipo", required=True,
                   choices=["rc", "rlc", "led", "divisor", "puente"])
    p.add_argument("-o", "--salida", default="circuito.svg")
    p.add_argument("--etiquetas", default="", help='pares K=V separados por coma, p.ej. "R=220Ω,C=1µF"')
    a = p.parse_args()

    et = dict(kv.split("=", 1) for kv in (x.strip() for x in a.etiquetas.split(",")) if "=" in kv)
    d = construir(a.tipo, et)
    if a.salida.lower().endswith(".svg"):
        d.save(a.salida)
        print(f"OK {a.salida}")
    else:
        tmp = a.salida.rsplit(".", 1)[0] + ".svg"
        d.save(tmp)  # schemdraw SVG primero; a PNG con svg_a_raster.py (backends)
        import subprocess, sys as _sys
        script = _sys.argv[0].replace("circuito.py", "svg_a_raster.py")
        subprocess.run([_sys.executable, script, tmp, "-o", a.salida], check=True)


if __name__ == "__main__":
    main()
