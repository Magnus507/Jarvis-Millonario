---
tags:
  - guia
  - operativo
  - manual
  - eternum_records
version: 2.1
updated: 2026-07-15
---

# Guia de Operacion Eternum

> [!IMPORTANT]
> Este manual define como trabajamos el sistema Eternum de forma ordenada: idea, sonido, letra, produccion, lanzamiento y promocion.

## Estructura del ecosistema

1. `Concepto_Eternum.md`: vision y direccion del proyecto.
2. `Incubadora_de_Ideas/00_Banco_de_Conceptos.md`: semillas de canciones o proyectos.
3. `Prompts_Suno/00_Dossier_Maestro_Suno.md`: reglas de composicion y prompt.
4. `Prompts_Suno/Recursos_Opcionales_Suno.md`: recursos opcionales para alternar segun la cancion.
5. `Agente_Suno_Experto.md`: orquestacion de la IA musical.
6. `Skills_Especializadas/`: skills locales del sistema antiguo.
7. Skills globales `eternum-*`: sistema nuevo por capas.
8. `Prompts_Suno/Canciones/`: historial de letras y prompts finales.
9. `Catalogo/` y `Artistas/`: registro de lanzamientos y perfiles.

## Flujo de trabajo

### 1. Definir la direccion

- Usar `eternum-ar`.
- Decidir genero, energia, BPM aproximado y sensacion general.
- Si la direccion no esta clara, no se escribe todavia.

### 2. Construir la idea

- Revisar el banco de conceptos.
- Definir una sola promesa emocional.
- Marcar si es single, EP o album.

### 3. Escribir la cancion

- Usar `eternum-hooklab` para el coro.
- Usar `eternum-lyrics` para versos y estructura.
- Ajustar la respiracion y la claridad de cada linea.

### 4. Producir

- Usar `eternum-production`.
- Definir secciones, capas, transiciones y energia por bloque.
- Evitar arreglos saturados.
- Elegir recursos solo cuando la cancion los necesite.
- Revisar `Prompts_Suno/Recursos_Opcionales_Suno.md` para escoger solo lo que aporte.

### 5. Cerrar prompt

- Usar `eternum-suno`.
- Combinar concepto, letra, feel, style prompt, excludes y direccion por seccion.
- Guardar la version final en `Prompts_Suno/Canciones/`.
- Copiar a Suno solo `Letra`, `Style prompt` y `Excludes`.

### 6. Visual y lanzamiento

- Usar `eternum-visuals` para portada y estetica.
- Usar `eternum-release` para registrar el lanzamiento.
- Usar `eternum-growth` para promocion.
- Usar `eternum-rights` para creditos y splits.

## Regla de operacion

- No repetir la misma base sonora si no hay una razon artistica clara.
- No publicar una cancion sin hook solido.
- No cerrar un lanzamiento sin metadata basica.
- No asumir creditos ni propiedad.
- No confundir volumen con impacto.
- No escribir la letra como si fuera instrucciones de produccion.
- Si hay cambio de energia, debe quedar en la guia por seccion o en el prompt, no escondido en un verso.

## Orden recomendado para una cancion nueva

1. `eternum-ar`
2. `eternum-hooklab`
3. `eternum-lyrics`
4. `eternum-production`
5. `eternum-suno`
6. `eternum-visuals`
7. `eternum-release`
8. `eternum-growth`
9. `eternum-rights`

## Estandar Suno

Cada cancion debe poder resumirse por seccion antes de generarse:

- Intro energy
- Verse energy
- Chorus energy
- Bridge break
- Outro decay
- Instrumental cues

## Regla de cues

- Usar 1 o 2 cues fuertes por cancion, no diez.
- Si hay ad-libs o efectos, ponerlos en una seccion especifica.
- Si hay un cambio claro de ritmo, marcarlo como `[Bridge]`, `[Break]` o `[Drop]`.
- No esconder cambios de base dentro de la letra.
- Si la cancion no pide cue, no se agrega.
- Los recursos se alternan segun la letra, el ritmo y el objetivo emocional.
- Consultar la lista maestra de recursos opcionales antes de decidir.

## Export final

Cuando se vaya a pegar una cancion en Suno, copiar solo:

1. Letra
2. Style prompt
3. Excludes

La direccion por seccion y las notas internas quedan para trabajo interno del proyecto.
Si la cancion es minimalista, el export final debe ser aun mas limpio.

## Mantenimiento

- Si cambia el sistema, primero actualizamos esta guia.
- Si un archivo ya no describe el flujo real, se simplifica o reemplaza.
- Si aparece una nueva skill util, se agrega al mapa y al manual.
- Si aparece un recurso nuevo, se añade a `Recursos_Opcionales_Suno.md`.
