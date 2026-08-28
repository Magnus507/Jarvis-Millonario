---
tags:
  - suno
  - research
  - prompting
  - eternum_records
estado: activo
version: 1.0
updated: 2026-08-27
---

# Referencias y Benchmarks Suno 2026

## Objetivo

Mantener separadas tres cosas:

1. capacidades confirmadas oficialmente por Suno
2. buenas prácticas repetidas en guías comunitarias
3. hipótesis que deben probarse antes de convertirse en regla de Eternum

Esto evita que el sistema se vuelva dependiente de trucos virales o afirmaciones no verificadas.

---

# 1. Hallazgos Oficiales de Suno

## v5.5

Suno v5.5 fue presentado en marzo de 2026 como un modelo más expresivo, junto con Voices, Custom Models y My Taste. Para Eternum esto refuerza una idea: la identidad musical no debe depender únicamente de texto; cuando el usuario tenga una voz, persona o modelo consistente, conviene usarlo como ancla.

Fuente:
- https://about.suno.com/blog/v5-5

## Prompts más descriptivos

Desde v4.5 Suno indica que el modelo refleja mejor matices emocionales y elementos técnicos, e incluso incluye un prompt enhancement helper para transformar ideas de género en descripciones más detalladas.

Implicación Eternum:
- no limitarnos a keywords
- usar lenguaje natural cuando la canción necesite matiz
- mantenerlo enfocado para no introducir contradicciones

Fuente:
- https://blog.suno.com/blog/introducing-v4-5

## Personas

Personas permite preservar voz, estilo y vibe de una canción y reutilizar esa identidad en nuevas creaciones.

Implicación Eternum:
- cuando aparezca una generación con una identidad vocal especialmente fuerte, considerar convertirla en Persona para construir continuidad de artista
- no intentar reescribir en cada prompt toda la identidad que una Persona ya puede fijar

Fuente:
- https://suno.com/blog/personas

## Covers

Covers puede conservar melodía mientras cambia el estilo.

Implicación Eternum:
- una gran melodía con mala producción no debe desecharse
- probar Cover antes de reconstruir una canción valiosa desde cero

Fuente:
- https://suno.com/blog/covers

## Audio Input / Upload

Suno permite usar audio propio como punto de partida. Con uploads y herramientas posteriores se pueden usar melodías tarareadas, riffs, grooves y otras ideas propias como anclas.

Implicación Eternum:
- cuando el texto no controle suficientemente una melodía, utilizar audio propio puede ser más efectivo que añadir más palabras al prompt

Fuentes:
- https://suno.com/blog/audio-inputs
- https://suno.com/blog/songeditor

## Song Editor y Stems

Suno añadió herramientas para reemplazar letras, rehacer secciones, reordenar partes y separar stems.

Implicación Eternum:
- si 80% de una generación funciona, preservar ese 80%
- no regenerar una canción completa por un puente o un coro defectuoso
- separar composición, generación y postproducción como etapas distintas

Fuente:
- https://suno.com/blog/songeditor

## Studio 2.0

En agosto de 2026 Suno Studio 2.0 añadió MIDI, automatización, efectos, synth, chat de producción y separación avanzada de stems. Es una función Premier.

Implicación Eternum:
- el prompt ya no debe cargar con toda la responsabilidad de mezcla y producción fina
- para usuarios Premier, pasar a Studio cuando el problema sea de edición, automatización, stems, MIDI o mezcla
- para Pro, mantener un flujo prompt → editor/covers/personas/stems según disponibilidad

Fuentes:
- https://suno.com/blog/studio-2
- https://help.suno.com/en/articles/13670529

---

# 2. Patrones Útiles de la Comunidad

Estas prácticas aparecen repetidamente en proyectos de GitHub, pero no se deben presentar como garantías oficiales.

## Separar Style y Lyrics por función

Patrón repetido:
- Style = identidad global de sonido
- Lyrics = palabras, estructura y cues locales

Esto coincide bien con Eternum y debe mantenerse.

Referencias:
- https://github.com/xerohour-ai/suno-forge
- https://github.com/jeffvan302/Suno-Lyrics-Writer
- https://github.com/yzfly/awesome-music-prompts

## Mantener una columna vertebral clara

La comunidad coincide en que demasiados géneros, instrumentos o instrucciones contradictorias hacen que el modelo derive.

Regla Eternum:
- una familia principal
- una fusión secundaria cuando aporte
- instrumentos solo si cambian el arreglo

Referencias:
- https://github.com/jeffvan302/Suno-Lyrics-Writer
- https://github.com/AlijeeWrites/suno-prompts

## Metatags como anclas, no código

Usar `[Verse]`, `[Chorus]`, `[Bridge]`, etc. aparece consistentemente como una forma práctica de estructurar la canción. Las instrucciones dentro de tags deben permanecer breves.

Referencias:
- https://github.com/entrepeneur4lyf/suno_ai_meta_tags_guide
- https://github.com/AlijeeWrites/suno-prompts

## Prompt compacto vs prompt descriptivo

Existe desacuerdo en comunidad:
- algunas guías recomiendan tags compactos
- otras recomiendan frases descriptivas estructuradas

Decisión Eternum:
- no convertir ninguna en dogma
- usar prompt compacto como baseline
- usar una variante descriptiva cuando necesitamos matiz o cuando la versión compacta falla
- comparar resultados reales

Referencias:
- https://github.com/mttkllr/suno-field-guide
- https://github.com/AlijeeWrites/suno-v55-prompt-guide

## Referencias de artistas

Buenas guías recomiendan traducir referencias a atributos musicales: voz, instrumentación, energía, estructura y producción.

Decisión Eternum:
- usar nombres dados por el usuario como información de análisis
- construir el prompt final con rasgos musicales originales y concretos

Referencia:
- https://github.com/jeffvan302/Suno-Lyrics-Writer

---

# 3. Hipótesis Comunitarias que NO son Reglas Eternum

Algunas guías afirman cosas como:

- que las primeras palabras del Style prompt reciben un peso fijo mayor
- números exactos de tags óptimos
- porcentajes universales de sliders
- sintaxis especial garantizada

Estas afirmaciones pueden ser útiles para experimentar, pero no están suficientemente confirmadas para tratarlas como leyes.

Regla Eternum:
- probarlas A/B
- registrar resultados
- promoverlas a regla solo si funcionan de forma repetida en nuestro propio flujo

---

# 4. Mejora Principal Introducida en Eternum

El sistema pasa de "escribir un prompt detallado" a "controlar un proceso de generación".

## Antes

Idea → letra → prompt → generar

## Ahora

Idea
→ hook
→ letra
→ arquitectura vocal
→ arreglo
→ Style/Lyrics separados
→ V1 limpia
→ diagnóstico
→ V2 producción
→ V3 firma/sound design
→ edición de sección si aplica
→ Cover/Persona/Audio Input si conviene
→ stems/Studio si el problema es de producción fina

Esto reduce desperdicio de créditos y evita destruir buenas partes de una canción por perseguir un detalle menor.

---

# 5. Scorecard de una Generación

Cada versión importante puede evaluarse de 1 a 5 en:

- Hook / memorabilidad
- Letra / naturalidad
- Voz principal
- Coro / crecimiento
- Arreglo
- Identidad
- Sound design
- Claridad
- Momento de 5–15 segundos aprovechable como clip

No se escoge automáticamente la versión que obedeció más instrucciones. Se escoge la que funciona mejor como canción.

---

# 6. Regla de Investigación Continua

Suno cambia rápido. Revisar fuentes oficiales cuando cambien:

- modelo principal
- funciones de Voices/Personas
- Covers
- Song Editor
- stems
- Studio
- límites o disponibilidad por plan

Las guías comunitarias sirven como laboratorio de ideas, no como autoridad final.

## Repositorios de Referencia Observados

- https://github.com/mttkllr/suno-field-guide
- https://github.com/xerohour-ai/suno-forge
- https://github.com/sanic732/SunoForge
- https://github.com/jeffvan302/Suno-Lyrics-Writer
- https://github.com/yzfly/awesome-music-prompts
- https://github.com/entrepeneur4lyf/suno_ai_meta_tags_guide
- https://github.com/DianaWolfe/suno-album-creation-guide

Ninguno se copia como sistema completo. Eternum toma ideas útiles, las contrasta con documentación oficial y conserva solo lo que mejora nuestro flujo.
