# Dibujo técnico e ingeniería (vistas, cotas, DXF)

Del boceto a un plano de ingeniería legible: proyección ortogonal, sistema de cotado y flujo DXF con `ezdxf`.

Índice: [1 Proyección](#1-proyección-ortogonal) · [2 Cotado](#2-cotado-iso) · [3 Tolerancias](#3-tolerancias-y-lectura) · [4 DXF con ezdxf](#4-dxf-con-ezdxf) · [5 Flujo](#5-flujo-de-trabajo)

## 1 Proyección ortogonal

- **Vistas**: alzado (frente), planta (arriba), perfil (lado). Colocación europea (primeraángulo): planta BAJO el alzado; americana (tercera): planta ENCIMA. Declarar el sistema en el cajetín.
- Toda vista se deriva del alzado con líneas de proyección (45° o lineas rectas entre vistas); NUNCA dibujar vistas inconsistentes entre sí.
- **Sección**: corte con tramas a 45° en las zonas materiales; contorno de corte más grueso.
- Vista isométrica de apoyo (una sola, esquina) para que se lea de un vistazo.

## 2 Cotado ISO

- Línea de cota: extensión (fina, con 1-2u de hueco al objeto) + línea de cota con **flechas** + número encima y alineado (lectura desde abajo/derecha según ISO 129).
- Cotas SIEMPRE en la vista que muestra la medida real (no en la proyectada con distorsión).
- Cadenas de cotas: la total fuera, las parciales dentro; sin redundancia (no cotar lo que ya se deduce con ±tolerancia).
- Ø para diámetros (`Ø12`), R para radios (`R4`), `4xØ5` para repetidos.
- Orden de cotas: líneas de referencia → tamaño de montaje → detallosesenciales.

## 3 Tolerancias y lectura

- Tolerancia: `20 ±0.1` (lineal) o `Ø12 H7` (ajuste indicial H7 = hueco normal); escribir la clase cuando el usuario la pida, no inventar ajustes.
- Cuadro de tolerancias genérico si no se especifica: ±0.2 en mm para mecanizado manual, ±0.05 CNC.
- Grosor de línea: contorno grueso (0.7u) · cotas/ejes finos (0.25u) · ejes de simetría de trazos alternos.

## 4 DXF con ezdxf

```python
import ezdxf

doc = ezdxf.new(setup=True)          # unidades y estilos incluidos
doc.header["$INSUNITS"] = 4          # milimetros
msp = doc.modelspace()

capa = lambda n: doc.layers.add(n, color=7)
msp.add_lwpolyline([(0, 0), (120, 0), (120, 80), (0, 80), (0, 0)],
                   dxfattribs={"layer": "MUROS"})
msp.add_line((0, -20), (120, -20), dxfattribs={"layer": "COTAS"})
msp.add_text("PLACA 120x80", height=5,
             dxfattribs={"layer": "TEXTO"}).set_placement((2, 40))
doc.saveas("pieza.dxf")
```

- Capas fijas: `MUROS`/`CONTORNO`, `COTAS`, `TEXTO`, `EJES`, `TRAZOS` (sección).
- DXF R2010 (`doc.dxfversion = "AC1024"`) máxima compatibilidad.
- Volver a mirar el resultado: `inkscape pieza.dxf -o revision.png` o abrir en cualquier visor DXF.

## 5 Flujo de trabajo

1. Recoger medidas REALES (y qué tolerancias aplica) antes de dibujar.
2. Boceto de vistas en orden: alzado → planta → perfil (solo las necesarias).
3. SVG si es para documento/web (seguir §3.1 del SKILL.md); **DXF con ezdxf** si es para CAD/CNC.
4. Cotejar: todas las vistas cuadran (misma medida en proyección) · sin cotas redundantes ni faltantes en la geometría crítica · cajetín con escala, unidades, sistema de proyección y autor.
5. Exportar revisión en PNG para que el usuario firme antes de dar el DXF por bueno.

Anti-patrones: cotar la vista distorsionada; medidas «de referencia» en un plano de fabricación; capas DXF mezcladas (un CAD no puede ocultar la capa de cotas); escala dibujada ≠ escala declarada en cajetín.
