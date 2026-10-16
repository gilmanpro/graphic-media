# Animación asistida por IA (dibujo + video)

De un boceto a una escena animada: la skill aporta el dibujo y el guion visual; la generación de video se hace con la herramienta de imagen→video que esté disponible en el entorno (si no la hay, el camino propio es GIF/MP4 con matplotlib — ver histogramas animados en el SKILL.md).

Índice: [1 Fundamentos](#1-fundamentos-antes-de-generar) · [2 Flujo en 3 pasos](#2-flujo-en-3-pasos) · [3 Prompts](#3-dirección-de-ia-cómo-escribir-el-movimiento) · [4 Coherencia](#4-coherencia-de-personaje) · [5 Práctica](#5-práctica-y-buenos-hábitos)

## 1 Fundamentos antes de generar

- **Dibujo y pose**: una pose sólida se lee de un vistazo; deja espacio alrededor de brazos/manos para que el gesto no se pierda contra el cuerpo. Rostro, manos, vestimenta y silueta principales siempre visibles: son la información que sigue el motor.
- **Puesta en escena**: decide qué nota el espectador primero. Medio cuerpo = expresión + lenguaje corporal; primer plano = rostro.
- **Sincronización**: define el «carácter» del movimiento antes de generarlo (saludo rápido = enérgico; lento con pausa = tímido).
- **Narrativa visual**: incluso 5 segundos necesitan inicio y respuesta (ve al amigo → gira → saluda). 2-3 bocetos de storyboard bastan para planificar.
- **Preparación del dibujo**: papel → foto/escaneo con luz uniforme y recorte de sobrantes; digital → exportar JPG/PNG limpio. Boceto a lápiz limpio sirve; no hace falta acabado pulido.

## 2 Flujo en 3 pasos

1. **Referencia**: subir el dibujo como imagen de referencia (y opcionalmente como primer cuadro) para que el personaje, la pose y el estilo sean la base.
2. **Dirección**: describir acción, microexpresiones, comportamiento de cámara (fija o paneo) y ambiente; diálogo con indicación de quién habla.
3. **Generar, ajustar, exportar**: relación de aspecto, duración y resolución; recortar/ensamblar tomas en un editor si se combinan clips.

## 3 Dirección de IA: cómo escribir el movimiento

- **Describe en orden, no en abstracto**: «mira hacia arriba, hace una pausa y luego sonríe» en vez de «se mueve de forma natural».
- Especifica cámara explícitamente: «cámara quieta», «primer plano fijo», «paneo lento siguiendo al personaje».
- Fija estilo: «conserva el aspecto dibujado a lápiz» para que la IA no pierda la mano del dibujante.
- Multi-toma: enumerar plano por plano con duración (`Plano 1 (3s): ... Plano 2 (4s): ...`) y ángulo de cada uno.

## 4 Coherencia de personaje

- Vistas de referencia (frontal, lateral, 3/4) del mismo personaje para mantener rostro, ropa, proporciones y estilo entre tomas y ángulos.
- Detalles clave verificables en cada toma: si algo importante cambia entre versiones, añadir esa vista a las referencias.
- Fondos sencillos cuando el personaje es el foco; escenas detalladas solo donde el entorno importe.

## 5 Práctica y buenos hábitos

| Enfoque | Ejercicio |
|---|---|
| Movimiento | Giro, extensión o retroceso con ritmo y peso claros |
| Interpretación | El mismo momento con dos emociones distintas |
| Encuadre | Comparar primer plano vs. plano medio vs. toma amplia |
| Narración | Unir 2-3 tomas con bocetos de storyboard como guía |
| Coherencia | Mismo personaje en varias tomas, detalles reconocibles |

- **Compara dos versiones cambiando UNA sola cosa** (timing, ángulo, prompt) lado a lado.
- **Dibuja la parte complicada antes** de reintentar: si un gesto falla, esboza la pose objetivo en vez de adivinar con otro prompt.
- **Busca un problema a la vez** por iteración.
- **Biblioteca propia**: guarda prompts, imágenes de referencia y clips que funcionaron.
