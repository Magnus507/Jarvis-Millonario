---
tags:
  - suno
  - reglas
  - eternum_records
  - prompts
ultima_actualizacion: 2026-07-15
---

# Dossier Maestro Suno

## Proposito

Este dossier define como convertir una idea de Eternum en una cancion lista para generar en Suno sin perder identidad ni repetir formulas.

## Principios base

- Cada cancion necesita una identidad propia.
- No repetir estructura, ritmo o textura sin una razon artistica clara.
- La voz debe sentirse humana, respirable y creible.
- El prompt debe describir funcion, energia y atmosfera, no solo genero.
- El catalogo puede usar muchos ritmos, pero cada cancion debe tener una sola columna vertebral ritmica clara.
- Los cambios de energia, breaks, drops, ad-libs y efectos son recursos opcionales, no obligatorios.
- No todas las canciones deben usar los mismos recursos; se eligen segun letra, ritmo y objetivo.

## Cadena de trabajo

Antes de cerrar un prompt, definir siempre:

1. objetivo emocional
2. direccion sonora
3. hook o centro memorable
4. energia del verso y del coro
5. arreglo y capas
6. elementos a evitar
7. secciones donde debe entrar o salir la base instrumental

## Direccion por seccion

Cada cancion debe poder resumirse por seccion. Usa esta guia antes de cerrar el prompt:

- **Intro energy:** define el ambiente inicial y el gancho de entrada.
- **Verse energy:** controla la tension narrativa y deja espacio a la voz.
- **Chorus energy:** abre, eleva y vuelve facil de recordar la parte principal.
- **Bridge break:** baja la base o cambia el color para crear contraste real.
- **Outro decay:** deja caer la energia para cerrar con vacio, reflexion o impacto.
- **Instrumental cues:** marca donde entra o sale requinto, bajo, percusion, pads, 808 o breaks.

## Regla de alternancia

- Si la letra ya sostiene tension, no fuerces un break.
- Si el coro ya abre suficiente, no agregues un cambio extra.
- Si la cancion pide contraste, usa uno o dos recursos fuertes bien puestos.
- Si el tema es mas directo o minimalista, simplifica la produccion y deja que la letra mande.
- Si el tema es mas cinematografico o dramatico, usa mas transiciones, pero solo si aportan claridad.

## Flujo recomendado

- `eternum-ar` decide el sonido.
- `eternum-hooklab` construye el coro.
- `eternum-lyrics` escribe versos y estructura.
- `eternum-production` define el arreglo.
- `eternum-suno` une todo en el paquete final.

## Biblioteca ritmica

Eternum no se cierra en corridos. Cada cancion puede tomar una base distinta si sirve a la identidad del tema.

### Familias permitidas

- corrido moderno
- corrido tumbado
- corrido experimental
- trap latino
- reggaeton oscuro
- dembow
- afrobeat latino
- drill suave
- jersey club
- house latino
- pop urbano elegante
- fusion regional-urbana

### Regla de uso

- Elegir una familia principal.
- Elegir, como mucho, una segunda textura de apoyo.
- No mezclar tres o cuatro ritmos a la vez si el hook pierde claridad.
- Si la base cambia de energia, marcarlo como `[Instrumental Break]`, `[Bridge]` o `[Outro]`.
- Si el tema tiene cambios de energia, anotarlos en la direccion por seccion, no escondidos en la letra.

## Buen prompt

Un buen prompt para Suno combina:

- genero o fusion principal
- pulso ritmico principal
- atmosfera
- energia
- instrumentacion principal
- actitud vocal
- exclusiones claras

## Excludes utiles

- `generic pop`
- `overprocessed autotune`
- `big banda`
- `overly busy arrangement`
- `flat melody`
- `rhythm switches every bar`
- `vocal clutter`
- `instrumental fighting vocals`

## Regla final

Si el tema suena demasiado parecido a otro, se vuelve a `eternum-ar` antes de producirlo.
Si la letra y la base se pelean, se simplifica el arreglo antes de volver a escribir.
Si un cue no aporta claridad, se elimina.
Si un recurso no cambia la experiencia de la cancion, se quita.

## Export final a Suno

Para pegar en Suno, usa solo estos tres bloques:

1. Letra
2. Style prompt
3. Excludes

Todo lo demas es guia interna para construir mejor el tema.

## Formato de salida recomendado

1. Concepto
2. Ritmo / feel
3. Letra
4. Style prompt
5. Excludes
6. Notas de produccion
7. Direccion por seccion
