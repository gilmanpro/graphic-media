# Flujos multimedia y de diseño — buenas prácticas condensadas

Conocimiento de referencia para producir contenido visual/multimedia de forma consistente (imágenes, gráficos, infografías, paneles, presentaciones visuales y ediciones de medios).

Índice: [1 Producción](#1-producción) · [2 Prompts](#2-prompts-creativos) · [3 Estilos](#3-estilos-y-plantillas-de-salida) · [4 Automatización](#4-automatización-de-lo-repetitivo) · [5 QA](#5-revisión-y-refinamiento)

## 1 Producción

- **Especializa la tarea**: un flujo por tipo de salida (gráfico, infografía, edición, animación) da resultados más consistentes que un flujo genérico que lo hace todo.
- **Combina etapas en un pipeline**: guion/concepto → creación visual → edición → revisión → entrega; cada etapa con su salida intermedia versionable.
- **Itera con variantes**: en diseño, la primera versión es una base — genera 2-3 direcciones (color, composición, tipografía), compara y elige; no defiendas el primer intento.
- **Flujos reutilizables**: convierte los prompts/ajustes que funcionaron en plantillas para tareas repetibles (mismo formato de informe, mismo tamaño de banner, misma paleta).

## 2 Prompts creativos

Prompt detallado = menos revisiones. Siempre incluir:

1. **Propósito** del diseño y a quién va dirigido.
2. **Estilo** deseado (minimalista, editorial, retro-tech…).
3. **Paleta** (colores exactos o referencia de marca) y **tipografía**.
4. **Composición y dimensiones** de salida (px, mm, relación de aspecto).
5. **Elementos obligatorios** (logo, texto mínimo, datos a mostrar).
6. **Formato final** (PNG, SVG, PDF, GIF, HTML autocontenido).

Con materiales de referencia (capturas, moodboards, guías de marca): describir qué se toma de cada referencia (composición, color, ritmo), no copiar la obra.

## 3 Estilos y plantillas de salida

- **Gráfico de datos con calidad de publicación** (PNG): línea, barras, área, velas, circular, heatmap — el camino es matplotlib (ver SKILL.md §1.2).
- **Infografía / panel autocontenido**: HTML+SVG inline sin dependencias externas; paleta e íconos integrados; se abre en cualquier navegador y se captura a PNG.
- **Estilo editorial de revista**: rejilla de columnas, fotografía protagonista a sangre, tipografía grande en títulos, tarjetas de datos, separadores de sección; usar para portadas e informes visuales.
- **Estilo retro-tech**: neón sobre oscuro, grid de perspectiva, tramas CRT/halftone, tipografía de los 80-90 — aplicar como capa estética, no cambiar la estructura del dato.
- **Temas aplicables a cualquier artefacto**: definir tema (colores + tipografía) una vez y reutilizarlo en láminas, páginas y paneles para coherencia de proyecto.

## 4 Automatización de lo repetitivo

Lotes típicos para el script `editar_imagen.py` del SKILL.md (nunca editar originales en sitio):

- Conversión de formatos (JPG↔PNG, export a GIF).
- Quitar fondo plano y transparencias.
- Redimension/corte por tamaño de destino (redes, impresión).
- Mejora (brillo/contraste/enfoque) en lote.
- Hojas de contacto para revisar muchas variantes de una vez.

## 5 Revisión y refinamiento

Checklist de entrega multimedia:

- [ ] Calidad visual: nitidez, sin compresión visible, dimensiones exactas del target.
- [ ] Consistencia de marca: paleta y tipografía igual que el resto del proyecto.
- [ ] Legibilidad: texto sin solapes, contraste suficiente (fondo/texto).
- [ ] Iteración final: ajustar espaciado, tipografía y color SOBRE el resultado, sin añadir elementos nuevos.
- [ ] Documentar lo que funcionó (prompt/ajuste) para la próxima ejecución.
