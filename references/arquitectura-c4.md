# Arquitectura — modelo C4 y vistas de infraestructura

Cómo estructurar un diagrama de arquitectura para que sea legible: niveles C4 + convenciones de vistas de red/sistema.

Índice: [1 C4](#1-modelo-c4) · [2 Cómo dibujarlo](#2-cómo-dibujarlo) · [3 Vistas de red](#3-vistas-de-red) · [4 Reglas](#4-reglas)

## 1 Modelo C4

Cuatro niveles, uno por pregunta. **Nunca mezclar niveles en un mismo diagrama.**

| Nivel | Pregunta | Elementos | Ejemplo |
|---|---|---|---|
| 1. Contexto | ¿Qué hace el sistema y con quién habla? | Sistema, actores (personas/otros sistemas), relaciones | «Tienda online ↔ Clientes, Pasarela pago» |
| 2. Contenedores | ¿Qué piezas desplegables hay? | Apps, bases de datos, colas, microservicios | Web SPA, API, MySQL, Redis |
| 3. Componentes | ¿Qué hay dentro de un contenedor? | Módulos, servicios internos | Controladores, repositorios, dominio |
| 4. Código | ¿Cómo está implementado? | Clases/métodos (solo si hace falta) | Diagrama de clases UML |

Pedir «un diagrama de arquitectura» sin nivel = empezar por **Contexto** y bajar de nivel solo si lo piden.

## 2 Cómo dibujarlo

Camino rápido (PNG con iconos de proveedor): script con la librería `diagrams` (SKILL.md §1.3).

Camino C4 a mano (SVG/draw.io):

```xml
<!-- contenedor = caja con cabecera de color; Persona = círculo+stickman simple -->
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 800 480" role="img">
  <title>Sistema de pedidos — contexto</title>
  <!-- actor -->
  <circle cx="90" cy="240" r="18" fill="#6B7280"/>
  <text x="90" y="285" text-anchor="middle" font-size="14">Cliente</text>
  <!-- sistema -->
  <rect x="300" y="190" width="200" height="100" rx="8" fill="#4F46E5"/>
  <text x="400" y="245" text-anchor="middle" fill="#fff" font-size="16">Tienda online</text>
  <!-- relación etiquetada SIEMPRE con el protocolo/qué viaja -->
  <line x1="110" y1="240" x2="298" y2="240" stroke="#111" marker-end="url(#f)"/>
  <text x="204" y="230" text-anchor="middle" font-size="12">HTTPS</text>
</svg>
```

- Nivel 1-2: cajas grandes con nombre del **rol** («API de pedidos»), no del artifacto (`pedidos-service-v2`).
- Toda arista **etiquetada** con el protocolo o contenido (REST/HTTPS, SQL, eventos JSON).
- Zonas: contorno punteado con etiqueta para «Nube X» o «On-prem».

## 3 Vistas de red

- Segmentos: rectángulos anidados con etiqueta de red (`10.0.1.0/24`), bordes discontinuos para DMZ.
- Elementos estándar: `internet ☁ → firewall → load balancer → app servers → DB primaria réplica`.
- Zonas de confianza con color de fondo; toda flecha entre zonas pasa por el firewall.
- Puertos anotados en la arista (`443/TCP`), no en el nodo.

## 4 Reglas

- Un diagrama = un nivel C4 + una audiencia (directivos: contexto; ingeniería: contenedores/componentes).
- Nombres de rol, no de release; versiones solo si cambian decisiones.
- Máximo ~15 nodos por vista; si hay más, agrupa (cluster) o sube de nivel.
- Anti-patrones: flechas sin etiqueta, mezcla de BD y cajas de app en el mismo plano que contexto de usuario, diagramas «todo conectado con todo» (dibuja solo relaciones reales y necesarias).
