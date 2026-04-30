---
skill: Orquestador de Tareas Multi-Paso
agent: Jarvisin
version: 2.0
fuente_inspiracion: Mark XXXIX-OR (agent_task + task_queue + executor)
---

# 🎛️ Skill: Orquestador de Tareas Multi-Paso

Este módulo faculta a Jarvisin para **planificar y ejecutar objetivos complejos** que requieren múltiples Skills o pasos secuenciales. Es la skill más poderosa del sistema — convierte objetivos de alto nivel en ejecución real.

---

## 🎯 Cuándo Activar Esta Skill

**ACTIVAR cuando el objetivo requiere:**
- 3 o más pasos distintos
- Múltiples Skills diferentes en secuencia
- El resultado de un paso alimenta al siguiente
- El proceso tarda más de 2-3 minutos en completarse

**NO activar para:**
- Preguntas o consultas simples (responder directamente)
- Edición de una sola nota (hacerlo directo)
- Búsqueda o análisis de una sola cosa

**Regla de oro:** Si cabe en 1 acción → directo. Si necesita 3+ pasos → esta Skill.

---

## 🔄 Flujo de Ejecución

```
RECIBIR GOAL DEL USUARIO
        │
        ▼
PLANIFICAR (≤5 pasos, skills disponibles)
        │
        ▼
EJECUTAR PASO 1
  → Si éxito: guardar resultado, continuar
  → Si falla: Error Handler (RETRY / SKIP / REPLAN / ABORT)
        │
        ▼
INYECTAR CONTEXTO AL PASO 2
(resultado del paso anterior → input del siguiente)
        │
        ▼
EJECUTAR PASO 2, 3, 4... (igual que arriba)
        │
        ▼
RESUMEN FINAL + ACTUALIZAR BITÁCORA
```

---

## 📋 Capacidades de Planificación

### Goals que puede manejar:

**Eternum Records:**
- "Crea una nueva canción para La Trilogía de Oro sobre [tema]" → A&R + Suno + Registrar en catálogo
- "Analiza nuestras métricas y sugiere estrategia para el próximo mes" → Data + Business + Plan
- "Investiga tendencias de corridos 2026 y actualiza la incubadora" → Research + A&R + Structure
- "Prepara el lanzamiento de [canción] para [fecha]" → Symphonic checklist + Socials + Bitácora

**Plataforma Médica:**
- "Diseña el flujo de registro de paciente desde cero" → Research + Technical + Structure
- "Investiga la Ley 81 de Panamá y redacta resumen de cumplimiento" → Research + Legal + Structure
- "Actualiza el esquema de BD con la tabla de notificaciones" → Technical + Structure

**Jarvis Millonario:**
- "Audita el Vault y sugiere mejoras de estructura" → Structure + Business
- "Onboarding de nuevo miembro: prepara guía de inicio" → Structure + Research

---

## 🚦 Prioridades de Tareas

Cuando hay múltiples tasks en cola, esta skill las ordena así:

| Prioridad | Señal | Ejemplo |
|---|---|---|
| **URGENTE** | Fecha límite inminente o bloqueador | "El lanzamiento es mañana y falta el prompt" |
| **NORMAL** | Flujo estándar de trabajo | "Investiga tendencias para la próxima canción" |
| **BAJO** | Mejoras no urgentes | "Reorganiza los recursos de la carpeta" |

---

## 💉 Inyección de Contexto (Cómo Conectar Pasos)

Cuando un paso produce información, esta skill la pasa al siguiente paso:

**Ejemplo:**
```
Paso 1: [Deep_Researcher] → "Corridos 2026: sintetizadores oscuros, narrativa introspectiva..."
         ↓
Paso 2: [Eternum_A_R] recibe: resultado_paso_1 + "Filtra lo que aplica a La Trilogía de Oro"
         ↓
Paso 3: [Suno_Experto] recibe: resultado_paso_2 + "Crea prompt para canción con estas características"
```

---

## 📊 Formato de Reporte al Usuario

```
🎯 Iniciando tarea: [objetivo completo]
Plan: 3 pasos

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
▶ Paso 1/3: Investigación de tendencias...
✓ Paso 1 completado

▶ Paso 2/3: Análisis aplicado a Eternum...
✓ Paso 2 completado

▶ Paso 3/3: Actualizando Incubadora de Ideas...
✓ Paso 3 completado
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

✅ Tarea completada
Resultado: [1 oración de lo que se logró]
Nota actualizada: [[ruta/a/la/nota]]
Bitácora: ✓ Registrada
```

---

## 🔧 Protocolo de Entrega

1. Crear o actualizar las notas relevantes en `01_Proyectos/` o `02_Recursos/`
2. Registrar en la Bitácora del proyecto afectado
3. Si aplica, crear WikiLinks entre notas nuevas y existentes
4. Sugerir el siguiente paso natural al usuario

---

*Skill: Orquestador de Tareas v2.0 — Inspirado en Mark XXXIX-OR agent_task*
*Módulo de Skill: v2.0*
