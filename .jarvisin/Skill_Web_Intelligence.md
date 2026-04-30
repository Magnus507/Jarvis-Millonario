---
skill: Inteligencia Web y Búsqueda Avanzada
agent: Jarvisin
version: 2.0
fuente_inspiracion: Mark XXXIX-OR (web_search.py + browser_control.py + or_client.py)
---

# 🌐 Skill: Inteligencia Web y Búsqueda Avanzada

Este módulo faculta a Jarvisin para **buscar, extraer, sintetizar y aplicar** información externa al ecosistema de Jarvis Millonario. Va más allá de una búsqueda simple — es investigación estructurada orientada a decisiones.

---

## 🎯 Cuándo Activar Esta Skill

- El usuario pide información que no está en el Vault
- Se necesita validar datos actuales (métricas, precios, tendencias)
- Se requiere investigación de mercado o competencia
- Se necesita monitorear plataformas externas (Spotify stats, Symphonic)
- Se necesita comparar opciones (herramientas, servicios, precios)

---

## 📋 Capacidades

### 1. Búsqueda Enfocada
- **Acción:** Buscar información específica con queries optimizadas
- **Regla:** Una query bien escrita > tres queries vagas
- **Formato de query:** Específico + contexto + fuente preferida (si aplica)

**Ejemplos de queries optimizadas:**
```
❌ "corridos tendencias"
✅ "corridos tumbados tendencias 2026 streaming Spotify crecimiento"

❌ "plataforma médica panamá"
✅ "plataforma historial clínico digital Panamá regulación Ley 81 requisitos"

❌ "suno prompts"
✅ "Suno AI v5.5 advanced prompting techniques metatags voice control 2026"
```

### 2. Búsqueda Comparativa
- **Acción:** Comparar múltiples opciones en una dimensión específica
- **Dimensiones:** precio, características, reseñas, compatibilidad, popularidad
- **Output:** Tabla comparativa con recomendación final

**Casos de uso:**
- Comparar distribuidores musicales (Symphonic vs DistroKid vs TuneCore)
- Comparar stacks técnicos para Plataforma Médica
- Comparar costos de plataformas de BaaS (Supabase vs Firebase vs PlanetScale)

### 3. Monitoreo de Tendencias
- **Acción:** Investigar el estado actual de un nicho o mercado
- **Foco principal:** Tendencias de corridos 2026, plataformas de salud digital, IA generativa musical
- **Output:** Resumen + 3-5 puntos aplicables al proyecto actual

### 4. Investigación Normativa y Legal
- **Acción:** Buscar regulaciones, leyes y cumplimiento legal relevante
- **Caso principal:** Ley 81 de Panamá (protección de datos de salud)
- **Output:** Resumen ejecutivo + lista de requisitos + implicaciones para el MVP

### 5. Extracción de Datos Externos
- **Acción:** Obtener datos de plataformas externas cuando es posible
- **Casos:** Estadísticas Spotify públicas, tendencias YouTube Music, charts Billboard corridos

---

## 🔄 Pool de Modelos Libres (Adaptado de OpenRouter)

Cuando se requieren análisis complejos de información buscada, Jarvisin puede usar este principio de fallback:

```
Modelo preferido: Claude (principal)
Fallback 1: Modelos Gemini
Fallback 2: Modelos Llama (via OpenRouter free tier)
Fallback 3: Modelos Qwen / Mistral

Regla: Si un modelo falla o está saturado → siguiente del pool
Límite de rate: Esperar 60 segundos antes de reintentar el mismo modelo
```

---

## 🧠 Proceso de Síntesis

Jarvisin no entrega raw research — siempre sintetiza:

```
DATOS CRUDOS (búsqueda)
    │
    ▼
FILTRAR lo irrelevante para Jarvis Millonario
    │
    ▼
CONECTAR con proyectos activos (Eternum / Medicina)
    │
    ▼
EXTRAER 3-5 puntos accionables
    │
    ▼
ENTREGAR con recomendación de siguiente paso
```

---

## 📑 Protocolo de Entrega

Los resultados de investigación se guardan en:
- `02_Recursos/[Categoría]/` → Para conocimiento permanente
- `01_Proyectos/[Proyecto]/` → Para contexto específico del proyecto
- `00_Bandeja_de_Entrada/` → Solo si requiere clasificación posterior

Formato de entrega al usuario:
```
🔍 Investigación: [tema]
Fuentes consultadas: [número]

📌 Hallazgos clave:
  1. [Punto aplicable al proyecto]
  2. [Punto aplicable al proyecto]
  3. [Punto aplicable al proyecto]

💡 Recomendación:
[Una acción concreta basada en los hallazgos]

📁 Guardado en: `ruta/a/la/nota`
```

---

## ⚠️ Reglas de Uso

1. **Nunca inventar datos** — si no se encuentra información, reportar honestamente
2. **Nunca citar URLs inventadas** — solo URLs que el usuario ya proporcionó o que se obtuvieron de búsqueda real
3. **Siempre contextualizar** — los datos solos no sirven; conectar con el proyecto relevante
4. **Máximo 5 puntos clave** — síntesis, no volumen

---

*Skill: Inteligencia Web v2.0 — Inspirado en Mark XXXIX-OR web_search + browser_control + or_client*
*Módulo de Skill: v2.0*
