---
tags:
  - guia
  - operativo
  - manual
  - eternum_records
version: 3.0
updated: 2026-08-27
---

# Guia de Operacion Eternum

> [!IMPORTANT]
> Este manual define cómo trabajamos Eternum: concepto, hook, letra, arquitectura vocal, producción, sound design, prompt, generación, revisión y lanzamiento.

## Estructura del Ecosistema

1. `Concepto_Eternum.md`: visión y dirección del proyecto.
2. `Incubadora_de_Ideas/00_Banco_de_Conceptos.md`: semillas de canciones o proyectos.
3. `Prompts_Suno/00_Dossier_Maestro_Suno.md`: reglas maestras de composición y prompt.
4. `Prompts_Suno/Recursos_Opcionales_Suno.md`: biblioteca amplia de recursos vocales, transiciones, ambientes y sound design.
5. `Agente_Suno_Experto.md`: rol del productor creativo principal.
6. `PROTOCOLO_CHAT_ETERNUM.md`: reglas para trabajar canciones desde el chat dedicado.
7. `Skills_Especializadas/`: skills locales del sistema antiguo.
8. Skills globales `eternum-*`: sistema por capas.
9. `Prompts_Suno/Canciones/`: historial de letras y prompts finales.
10. `Catalogo/` y `Artistas/`: registro de lanzamientos y perfiles.

## Flujo Maestro de Trabajo

### 1. Definir la Dirección

- Usar `eternum-ar`.
- Decidir género o fusión, energía, BPM aproximado, ambiente y referencia emocional.
- Si la dirección no está clara, no escribir todavía.

### 2. Construir la Idea

- Revisar el banco de conceptos cuando aplique.
- Definir una sola promesa emocional.
- Identificar la escena o mundo narrativo de la canción.

### 3. Construir el Hook

- Usar `eternum-hooklab`.
- El coro debe poder recordarse fuera del contexto completo de la canción.
- Priorizar frase central, ritmo vocal y repetibilidad.

### 4. Escribir la Letra

- Usar `eternum-lyrics`.
- Mantener métrica cantable.
- Dejar espacio para respiraciones, ad-libs y respuestas cuando la producción lo necesite.
- No meter instrucciones técnicas dentro de líneas cantadas.

### 5. Diseñar la Arquitectura Vocal

Antes del arreglo final, decidir:

- carácter de voz principal
- dobles
- armonías
- ad-libs
- call and response
- gang vocals
- crowd vocals
- gospel/church choir
- voces lejanas
- tratamientos especiales por sección

### 6. Diseñar la Producción

- Usar `eternum-production`.
- Definir secciones, capas, instrumentación, energía y contraste.
- Asegurar una columna vertebral rítmica clara.
- El coro debe crecer de forma intencional.

### 7. Diseñar Sound Design y Transiciones

Consultar `Prompts_Suno/Recursos_Opcionales_Suno.md`.

Elegir solo recursos que mejoren la historia o la dinámica:

- ambientes
- objetos narrativos
- sonidos de tecnología
- automóviles y movimiento
- impactos
- silencios
- texturas analógicas
- recursos cinematográficos

Los ejemplos del usuario son inspiración, no una lista obligatoria.

### 8. Clasificar Prioridades

Separar el prompt en:

- Nivel 1: columna vertebral obligatoria
- Nivel 2: firma de producción
- Nivel 3: microdetalles opcionales

Si el prompt se satura, eliminar primero Nivel 3.

### 9. Cerrar el Prompt

- Usar `eternum-suno`.
- Combinar concepto, letra, feel, arquitectura vocal, producción y sound design.
- Guardar la versión final en `Prompts_Suno/Canciones/` cuando corresponda.

### 10. Exportar a Suno

Entregar tres bloques limpios:

1. Lyrics
2. Style prompt
3. Excludes

Las notas internas no se mezclan con el bloque de copiado.

### 11. Revisar la Generación

Después de escuchar una versión, diagnosticar:

- hook
- interpretación vocal
- claridad de letra
- tamaño real del coro
- comportamiento de voces secundarias
- obediencia de cues
- calidad de transiciones
- utilidad del sound design
- exceso de elementos
- momento más memorable

Corregir el problema dominante antes de volver a generar.

### 12. Visual y Lanzamiento

- `eternum-visuals`: portada y estética.
- `eternum-release`: registro del lanzamiento.
- `eternum-growth`: promoción.
- `eternum-rights`: créditos y splits.

## Regla de Densidad

La producción no tiene un máximo fijo de efectos.

- Minimalista: 0–2 recursos fuertes.
- Moderna estándar: 2–4 recursos coordinados.
- Cinemática/narrativa: más recursos permitidos si están distribuidos por secciones y mantienen claridad.

## Reglas Fundamentales

- No repetir la misma base sonora sin razón artística.
- No publicar una canción sin hook sólido.
- No confundir complejidad con calidad.
- No usar efectos solo porque existen.
- No llenar el prompt de marcas o sonidos propietarios concretos.
- Si Suno no puede obedecer un detalle literal, reformularlo funcionalmente.
- Si el arreglo compite con la voz, simplificar.
- Si un silencio tiene más impacto que otro efecto, usar silencio.
- Las voces secundarias deben tener función, no rellenar espacio.

## Dirección por Sección Obligatoria

Toda canción debe poder resumirse con:

- Intro energy
- Verse energy
- Pre-Chorus lift
- Chorus energy
- Post-Chorus behavior
- Verse 2 evolution
- Bridge break
- Final Chorus expansion
- Outro decay
- Vocal layers by section
- Instrumental cues
- Sound-design cues

## Formato de Entrega de una Canción

1. Título provisional
2. Concepto
3. Dirección sonora
4. Hook/coro
5. Letra completa
6. Arquitectura vocal
7. Arreglo por secciones
8. Sound design
9. Transiciones
10. Style prompt
11. Excludes
12. Notas de producción
13. Dirección por sección
14. Bloque final listo para Suno

## Mantenimiento

- Si cambia el sistema, actualizar primero esta guía.
- Si un archivo queda obsoleto, simplificarlo o reemplazarlo.
- Si aparece un recurso útil, agregarlo a la biblioteca.
- Si un recurso falla repetidamente en Suno, documentar una formulación más robusta.
- El sistema debe evolucionar según resultados reales, no quedarse congelado en una receta.
