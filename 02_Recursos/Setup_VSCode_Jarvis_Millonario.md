---
tipo: recurso
estado: activo
updated: 2026-04-30
tags:
  - vscode
  - jarvisin
  - herramientas
  - git
---

# Setup VSCode Jarvis Millonario

Este setup convierte VSCode en una segunda cabina de operacion para el Vault, complementando Obsidian con Git, busqueda, edicion Markdown y asistencia de IA.

## Extension Base

| Extension | Uso principal en el Vault |
|---|---|
| ChatGPT / Codex | Operacion con IA dentro del repositorio, lectura de contexto y edicion asistida |
| GitLens | Historial por archivo, autores, commits recientes y comparacion entre PCs |
| Markdown All in One | Edicion rapida de notas, listas, tablas e indices |
| Foam | Navegacion tipo segundo cerebro: backlinks, grafo y notas conectadas |
| Todo Tree | Deteccion de pendientes como `TODO`, `PENDIENTE`, `REVISAR`, `ACCION` y `BLOQUEO` |
| GitHub Pull Requests | Revision de PRs, issues y flujo GitHub desde VSCode |
| Markdown Preview Enhanced | Vista previa avanzada de documentacion y notas largas |
| Mermaid Markdown Syntax Highlighting | Diagramas de procesos, arquitectura y flujos operativos |
| Prettier | Formato consistente para Markdown, JSON, JS/TS y archivos tecnicos |

## Uso Operativo

1. Abrir la carpeta raiz `Jarvis Millonario` en VSCode.
2. Revisar GitLens antes de editar si se trabajo desde otra PC.
3. Usar Todo Tree para convertir pendientes dispersos en acciones reales.
4. Usar Foam para navegar notas conectadas sin depender solo de Obsidian.
5. Usar Markdown Preview Enhanced para revisar documentos de sistema antes de commit.
6. Usar GitHub Pull Requests cuando el flujo pase de commits directos a revisiones.

## Reglas Para Jarvisin En VSCode

- Al iniciar sesion: leer `00_Dashboard_Operativo.md`, luego `.jarvisin/memoria/proyectos.md` y `.jarvisin/memoria/notas.md`.
- Antes de editar: ejecutar `git status`.
- Si hay cambios remotos: `git pull --ff-only` antes de trabajar.
- Si hay cambios locales de otra persona: no sobrescribir sin instruccion explicita.
- Despues de cambios significativos: actualizar dashboard, memoria o bitacora segun aplique.
- No subir secretos, `.env`, builds, paquetes locales ni credenciales.

## Pendientes Recomendados

- Revisar si Foam detecta correctamente los WikiLinks existentes.
- Definir convencion unica para tags de accion: `PENDIENTE`, `REVISAR`, `ACCION`, `BLOQUEO`.
- Crear snippets de VSCode para notas repetitivas: bitacora, cancion, idea, proyecto.
- Evaluar si conviene activar formato automatico solo para JSON/JS y dejar Markdown manual.

## Bitacora

- [2026-04-30] - @Codex: Documentado setup VSCode con 8 extensiones instaladas y recomendaciones del workspace. Impacto: el Vault queda mejor preparado para operar desde varias PCs con Git, Markdown, Foam, Todo Tree y Codex.
