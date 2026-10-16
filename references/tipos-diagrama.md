# Catálogo de tipos de diagrama — cuándo usar cada uno

Mapa completo de tipos (familia de los 44 del skill `diagram-design` + los de diagramas como texto). Gramática única para todos: **nodo = caja redondeada · relación = flecha etiquetada · agrupación = contorno punteado · datos = tabla/columna**.

Índice: [1 Por intención](#1-por-intención) · [2 Fórmulas visuales](#2-fórmulas-visuales) · [3 Errores por tipo](#3-errores-por-tipo)

## 1 Por intención

| Quiero mostrar... | Tipo | Herramienta (SKILL) |
|---|---|---|
| Cómo avanza un proceso con decisiones | Flujo / flowchart | Mermaid §1.1 |
| Quién llama a quién y en qué orden | Secuencia | Mermaid `sequenceDiagram` |
| Estructura de datos/entidades y relaciones | ER (entidad-relación) | Mermaid `erDiagram` |
| Clases y sus métodos | Clases UML | PlantUML (`diagramas-texto.md`) |
| Estados de un objeto y transiciones | Estados | Mermaid `stateDiagram-v2` |
| Arquitectura de software/nube | Contexto/Contenedores C4 | `arquitectura-c4.md` + `diagrams` §1.3 |
| Red/segmentos/firewalls | Vista de red | `arquitectura-c4.md` §3 |
| Proceso de negocio formal | BPMN | `diagramas-texto.md` §4 |
| Tareas en el tiempo (proyecto) | Gantt | Mermaid `gantt` |
| Ideas y sus ramas | Mindmap | Mermaid `mindmap` |
| Jerarquía de personas/u org | Organigrama | Mermaid `flowchart TD` con subgrafos |
| Comparar opciones en 2 ejes | Cuadrante (ej. esfuerzo/impacto) | SVG/HTML editorial (§1.5) |
| Evolución en el tiempo | Timeline | SVG + tipografía grande (§1.5) |
| Proporciones de un total | Pastel/donut | `grafico.py --tipo pie` |
| Distribución/relación de datos | Histograma/dispersión | `grafico.py --tipo hist/scatter` |
| Embudo de conversión | Embudo | SVG (rectángulos decrecientes, §1.5) |
| Matriz de criterios | Matriz/tabla visual | SVG grid (§1.5) |
| Relaciones de un grafo grande | Red/network | Graphviz DOT (`diagramas-texto.md` §3) |
| Persona vs. sistema alrededor | Diagrama de contexto | `arquitectura-c4.md` §1 |
| Camino del usuario en una app | User flow / wireframes | draw.io / Excalidraw (`como-hacerlo.md` §4) |
| Ciclo de vida, bucle de feedback | Diagrama circular | SVG (arcos + flechas, §4) |
| Antes/después o comparativa | Split comparativo | Dos paneles + corte, §1.5 |
| Cadena de valor/proceso con entradas | Swimlanes | Mermaid flowchart con subgrafos por carril |

Regla de elección: **intención primero, herramienta después** (columna 1 decide); si es para debatir → hand-drawn (`hand-drawn.md`); si es para publicar → editorial SVG/HTML (§1.5).

## 2 Fórmulas visuales

- **Cuadrante**: viewBox 800x800, ejes que se cruzan al centro con puntas, fondo de cuadrante tintado muy suave, etiquetas de extremo del eje («Bajo»/«Alto»), ítems como punto + rótulo.
- **Timeline**: línea horizontal gruesa, hitos como círculos alternando arriba/abajo, fecha en negrita y descripción corta.
- **Embudo**: rectángulos apilados de ancho decreciente (cada etapa 60-80% del anterior), valor a la derecha, caída entre etapas en gris.
- **Circular**: 5-7 nodos en círculo (posición angular `θ = 2πi/n`), flechas siguiendo el arco, centro con el título del ciclo.
- **Organigrama**: raíz arriba, hijos centrados bajo el padre, uniones en árbol ortogonal (bajada → barra horizontal → bajada), 3 niveles máximo por vista.

## 3 Errores por tipo

- Flujo: más de 3 caminos en un mismo decisional → parte en dos decisiones.
- Secuencia: actores sin mensaje de retorno o bucles no marcados (`loop`).
- ER: relaciones sin cardinalidad (`||--o{`); atributos que son entidades.
- Cuadrante/timeline/embudo dibujados a mano sin rejilla → ejes no perpendiculares, hitos desiguales (usar SVG con coordenadas calculadas).
- Organigrama con más de ~15 nodos → subir de nivel o partir por áreas.
- Mezclar tipos en un lienzo (ej. flujo + cuadrante): produce lectura imposible; séiene un tipo por pieza.
