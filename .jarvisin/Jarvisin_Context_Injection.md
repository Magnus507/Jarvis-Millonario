---
agent: Jarvisin
modulo: Protocolo de Inyección de Contexto
version: 1.0
fuente_inspiracion: Mark XXXIX-OR (executor.py — _inject_context + _translate_to_goal_language)
compatible_con: Antigravity, Codex (ChatGPT VSCode), Claude Code
---

# 💉 Protocolo de Inyección de Contexto

Este protocolo define cómo el **resultado de un paso alimenta automáticamente al siguiente** en tareas multi-paso. Es lo que convierte una secuencia de pasos aislados en una cadena inteligente y coherente.

---

## ¿Por Qué Existe Este Protocolo?

El Planificador tiene una regla absoluta: **no puede referenciar resultados de pasos anteriores en los parámetros del plan**. Esto es intencional — hace el plan predecible y sin dependencias circulares.

Pero el Ejecutor SÍ puede conectar esos resultados. Lo hace automáticamente, sin que el Planificador lo sepa.

```
PLANIFICADOR escribe:
  Paso 1: [Deep_Researcher] busca → "tendencias corridos 2026"
  Paso 2: [Suno_Experto] crea canción → (parámetros vacíos de input)

EJECUTOR ejecuta:
  Paso 1 → produce: "Tendencias: sintetizadores oscuros, narrativa introspectiva..."
  Paso 2 → recibe: [resultado paso 1] + "Crea canción con estas características"
  
  El usuario nunca ve esta plomería. Solo ve el resultado final.
```

---

## 🔄 Cómo Funciona (3 Reglas de Inyección)

### Regla 1: Inyección de Contenido
Si un paso necesita "contenido" y ese contenido no fue especificado por el Planificador, tomar los resultados de TODOS los pasos anteriores relevantes y usarlos como input.

**Cuándo aplica:**
- Un paso escribe en una nota de Obsidian (Master of Structure)
- Un paso crea un documento o reporte
- Un paso necesita "material" para generar algo (Suno Expert, Visuals)

**Cómo hacerlo:**
```
resultados_anteriores = [r para r en resultados si r tiene contenido real]
contenido_combinado = unir(resultados_anteriores, separador="---")
usar contenido_combinado como input del paso actual
```

### Regla 2: Inyección de Contexto Acumulativo
El contexto del OBJETIVO GLOBAL siempre está disponible en todos los pasos.
El resultado de cada paso se acumula en un "diario de ejecución".

```
diario = {}
Para cada paso:
  diario[paso_N] = resultado_paso_N
  
  Cuando ejecuto el paso siguiente:
  → tengo acceso a diario completo
  → pero SOLO inyecto lo que es relevante para ese paso específico
```

### Regla 3: Inyección de Idioma
Si el objetivo fue escrito en español, todos los resultados (incluso los de búsqueda en inglés) deben entregarse en español.

```
Detectar idioma del objetivo → Español
Si resultados intermedios son en inglés → traducir antes de inyectar al siguiente paso
Si resultados intermedios son en español → inyectar directamente
```

---

## 📊 Mapa de Flujo de Contexto por Caso de Uso

### Caso 1: Investigar → Crear Canción
```
[Deep_Researcher / Web_Intelligence]
  → "Tendencias 2026: sintetizadores oscuros + rap introspectivo..."
  ↓ INYECTA
[Eternum_A_R]
  → Filtra: "De estas tendencias, aplica X a La Trilogía de Oro"
  ↓ INYECTA
[Agente_Suno_Experto]
  → Recibe análisis filtrado → Crea letra + prompt Suno
  ↓ INYECTA
[Master_of_Structure]
  → Recibe todo → Guarda en Prompts_Suno/Canciones/[nombre].md
```

### Caso 2: Investigar → Actualizar Arquitectura
```
[Web_Intelligence]
  → "Mejores prácticas para historial clínico digital 2026..."
  ↓ INYECTA
[Technical_Architect]
  → "Dado esto, propone mejoras al esquema actual de Medicina"
  ↓ INYECTA
[Code_Intelligence]
  → Recibe propuesta → Escribe migration SQL + nuevo esquema
  ↓ INYECTA
[Master_of_Structure]
  → Guarda en Proyecto de medicina/database_schema_v2.md
```

### Caso 3: Análisis → Estrategia → Documento
```
[Deep_Researcher]
  → "Estado del mercado de corridos en streaming Q2 2026..."
  ↓ INYECTA
[Business_Strategist]
  → "Dado el mercado, recomienda estrategia para Eternum Records"
  ↓ INYECTA
[Master_of_Structure]
  → Recibe estrategia completa → Crea nota en 02_Recursos/Estrategia/
```

---

## 🚦 Qué SE Inyecta y Qué NO

### SÍ inyectar:
- Resultados de investigación (Deep Researcher, Web Intelligence)
- Análisis y filtros (A&R, Business Strategist)
- Código generado hacia documentación (Code Intelligence → Master of Structure)
- Propuestas técnicas hacia implementación

### NO inyectar:
- Errores de pasos fallidos (el Error Handler los maneja, no los inyecta)
- Resultados de pasos omitidos (se saltan limpiamente)
- Respuestas de confirmación ("Done", "Completado") — no tienen valor como contexto
- Más de 4,000 caracteres por inyección (truncar si es necesario, preservar lo más relevante)

---

## 📏 Reglas de Truncamiento

Si el resultado de un paso es muy largo para inyectar completo:
1. Preservar los primeros 2,000 caracteres (resumen y puntos clave suelen estar al inicio)
2. Preservar los últimos 500 caracteres (conclusiones suelen estar al final)
3. Marcar el truncamiento: `[... contenido truncado por longitud ...]`
4. La nota completa siempre se guarda en el Vault sin truncar

---

## 🔎 Señales de que la Inyección Funcionó

El resultado final debe sentirse como si fuera UNO, no como varios pasos pegados:
- ✅ La canción refleja exactamente las tendencias investigadas
- ✅ El código implementa exactamente la arquitectura propuesta
- ✅ El documento de estrategia usa datos reales de la investigación
- ❌ Señal de falla: el paso final ignora lo producido por pasos anteriores

---

*Protocolo de Inyección de Contexto v1.0 — Inspirado en Mark XXXIX-OR executor.py*
*Compatible con: Antigravity | Codex (ChatGPT VSCode) | Claude Code*
*Firma: Jarvisin — Sistema Operativo de Jarvis Millonario*
