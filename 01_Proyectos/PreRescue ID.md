---
tags:
  - proyecto
  - prerescue-id
  - externo
estado: activo
ultima_actualizacion: 2026-05-09
---

# PreRescue ID

> [!ABSTRACT] Contexto para Jarvisin
> **Proposito:** Registrar PreRescue ID como tercer proyecto activo dentro de Jarvi Millonario.
> **Vision:** Trabajar el proyecto desde su propio repositorio/carpeta, manteniendo a Jarvi como centro de memoria y coordinacion.

---

## Estado y Progreso
- **Fase Actual:** Migración de repositorio completada y corrección de deuda técnica (Prisma migrations).
- **Bloqueadores:** Ninguno.
- **Siguiente paso:** Validar despliegue en Vercel desde el nuevo repositorio.

---

## Manual de Operacion
- **Ubicacion interna:** `C:\Users\geank\OneDrive\Desktop\Jarvi Millonario\01_Proyectos\PreRescue ID`
- **Regla principal:** PreRescue ID vive dentro de `01_Proyectos`, pero se trabaja como repositorio separado; Jarvi solo guarda memoria, contexto y coordinacion.
- **GitHub:** Tiene flujo/subida propia en `https://github.com/Magnus507/PreRescueID.git`, separada del repositorio de Jarvi Millonario.
- **Instrucciones:**
    1. No modificar archivos de PreRescue ID sin autorizacion directa del usuario.
    2. Si se hacen cambios en Jarvi sobre la memoria/documentacion, subirlos al GitHub de Jarvi.
    3. Si se hacen cambios en PreRescue ID, subirlos aparte al GitHub propio de PreRescue ID.
    4. Cuando se suba PreRescue ID, actualizar tambien la memoria de Jarvi y subir Jarvi Millonario en su repo correspondiente.

---

## Documentacion Relacionada
- Memoria ejecutiva: [[proyectos]]
- Dashboard: [[00_Dashboard_Operativo]]

---

## Bitacora de Actualizaciones

### 2026-05-01 - @Codex
- **Cambio:** Actualizada ubicacion de PreRescue ID: ahora vive dentro de `01_Proyectos`, manteniendo repositorio Git independiente.
- **Impacto:** Jarvi coordina el proyecto sin mezclar su GitHub con el repositorio propio de PreRescue ID.

### 2026-05-01 - @Codex
- **Cambio:** Registro inicial de PreRescue ID como tercer proyecto activo de Jarvi.
- **Impacto:** Jarvi reconoce PreRescue ID como proyecto separado, con repositorio y subida de GitHub independientes.

### 2026-05-09 - @Antigravity
- **Cambio:** Migración de repositorio a `PreRescueID` y corrección de `.gitignore` para incluir `prisma/migrations`.
- **Impacto:** Se resolvió el problema de sincronización con GitHub y se aseguró que el esquema de la base de datos se rastree correctamente. Se unificaron las ramas `master` y `main`.

---
Volver al [[Jarvis Millonario|Cerebro Digital]]
