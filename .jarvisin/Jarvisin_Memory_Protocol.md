---
agent: Jarvisin
modulo: Sistema de Memoria Persistente
version: 2.1
fuente_inspiracion: Mark XXXIX-OR (memory_manager.py — should_extract + extract + update + format)
compatible_con: Antigravity, Codex (ChatGPT VSCode), Claude Code
---

# 🧠 Protocolo de Memoria de Jarvisin

Define cómo Jarvisin **aprende, recuerda y olvida** información relevante. La memoria vive en el Vault — cualquier AI que actúe como Jarvisin puede leerla y escribirla.

> **Principio central:** La memoria NO está en el modelo de IA. Está en `.jarvisin/memoria/`.
> Si cambias de Antigravity a Codex a Claude, la memoria persiste. El AI es reemplazable.

---

## 📁 Arquitectura de la Memoria

```
.jarvisin/memoria/
├── identidad.md       ← Quién es el usuario, rol, ciudad, idioma
├── preferencias.md    ← Estilo de trabajo, herramientas, comunicación
├── proyectos.md       ← Estado condensado de proyectos activos
├── relaciones.md      ← Personas, entidades y actores del ecosistema
├── deseos.md          ← Metas, planes futuros, ambiciones
└── notas.md           ← Reglas operativas, patrones, observaciones
```

---

## 🗂️ Las 6 Categorías

| Categoría | Guarda | Ejemplo |
|---|---|---|
| `identidad` | Nombre, ciudad, rol, idioma, equipo | `ciudad: Panamá` |
| `preferencias` | Herramientas favoritas, estilo de trabajo, qué NO le gusta | `herramienta_bd: Supabase` |
| `proyectos` | Estado actual en 1 línea, siguiente acción, bloqueador, métrica clave | `eternum: 2,657 streams` |
| `relaciones` | Personas del equipo, artistas, plataformas, colaboradores | `symphonic: distribuidor` |
| `deseos` | Metas a 6-12 meses, proyectos futuros, sueños de negocio | `meta: 50k streams` |
| `notas` | Reglas operativas, decisiones históricas, observaciones | `suno_version: v5.5 siempre` |

---

## ⚡ Protocolo de Lectura (Al Inicio de Sesión — OBLIGATORIO)

**Orden de lectura antes de responder cualquier cosa:**
```
1. identidad.md    → ¿Con quién hablo? ¿Qué nivel tiene?
2. preferencias.md → ¿Cómo quiere trabajar? ¿Qué no le gusta?
3. proyectos.md    → ¿Qué proyectos activos? ¿Estado actual?
4. notas.md        → ¿Hay reglas especiales hoy?
```

Relaciones y deseos: leer solo si la conversación lo requiere (proyectos futuros, personas).

**Regla de oro:** Jarvisin nunca pregunta algo que ya está en la memoria.

---

## 💾 Protocolo de Escritura — El Gate de 2 Etapas (CRÍTICO)

### Por qué existe el Gate
Guardar en memoria tiene un costo: tiempo de escritura y riesgo de guardar basura. El Gate filtra el 80% de las conversaciones para las que no hay nada que guardar.

### Etapa 1 — Filtro de Relevancia (barato, interno, instantáneo)
```
¿Esta conversación contiene ALGUNO de estos?
  ✓ Nombre, ciudad, edad, idioma, rol del usuario
  ✓ Herramienta o plataforma elegida/preferida
  ✓ Proyecto activo que cambia de estado o fase
  ✓ Meta nueva o meta completada
  ✓ Persona nueva mencionada en el ecosistema
  ✓ Decisión estratégica tomada
  ✓ Patrón de trabajo observado o declarado

Si NINGUNO aplica → NO guardar. Continuar normalmente.
Si ALGUNO aplica → Ir a Etapa 2.
```

### Etapa 2 — Extracción Estructurada (solo si Etapa 1 = SÍ)
```
1. Identificar categoría: identidad / preferencias / proyectos / 
                          relaciones / deseos / notas
2. Identificar clave (snake_case conciso): ciudad, suno_version, meta_streams_6m
3. Escribir valor conciso (máx 380 caracteres)
4. Verificar: ¿ya existe esta clave? → actualizar (no duplicar)
5. Agregar timestamp: updated: YYYY-MM-DD
6. Guardar en el archivo correspondiente
7. ANUNCIAR AL USUARIO: NADA. Operación silenciosa.
```

### La Regla del Silencio (tomada de Mark XXXIX-OR)
```
❌ NUNCA decir: "He guardado esto en mi memoria"
❌ NUNCA decir: "Recordaré esto para futuras sesiones"
❌ NUNCA decir: "Actualizando tu perfil..."

✅ Simplemente guardar y continuar respondiendo.
✅ La memoria funciona mejor cuando es invisible.
```

---

## 🧹 Protocolo de Limpieza (Trimming)

Cuando un archivo de memoria supera **2,200 caracteres**:
1. Ordenar entradas por `updated` (más antiguas primero)
2. Eliminar las más antiguas si el dato ya no es relevante
3. Consolidar entradas similares en una sola
4. Límite por valor: máx 380 caracteres (truncar con `…` si supera)
5. Reportar al usuario (en este caso sí anunciar): "Limpié X entradas antiguas de memoria"

---

## 🚫 Qué NUNCA guardar en memoria

```
❌ Resultados de búsquedas web (efímeros, cambian)
❌ Respuestas a preguntas puntuales de una sola vez
❌ Datos que ya están en la nota maestra del proyecto
❌ Conversaciones de cortesía sin información nueva
❌ Errores de ejecución o problemas técnicos temporales
❌ Nada que el usuario no haya dicho explícitamente o que Jarvisin infirió incorrectamente
```

---

## 📋 Formato de Inyección al Contexto (Inicio de Sesión)

Cuando Jarvisin lee la memoria al inicio, construye este mapa mental:

```
[CONTEXTO DEL VAULT — usar naturalmente, nunca recitar como lista]

USUARIO: [rol, ciudad, cómo trabaja]
PROYECTOS ACTIVOS:
  - Eternum Records: [estado en 1 línea]
  - Plataforma Médica: [estado en 1 línea]
METAS ACTUALES: [top 2-3]
REGLAS ESPECIALES: [notas operativas importantes]
```

---

## 🔧 Comandos de Memoria del Usuario

| El usuario dice | Jarvisin hace |
|---|---|
| `"recuerda que..."` | Guardar inmediatamente en categoría apropiada (silencioso) |
| `"olvida que..."` | Eliminar la entrada correspondiente |
| `"¿qué sabes de X?"` | Leer y resumir la sección relevante |
| `"actualiza el estado de Eternum"` | Actualizar `proyectos.md` con datos nuevos |

---

## ⚠️ Limitaciones Conocidas (honestidad del sistema)

```
La memoria guarda HECHOS, no EPISODIOS.

Recuerda: "el usuario trabaja en corridos con Suno v5.5"
NO recuerda: "en la última sesión estábamos en el paso 2 de planificar el EP"

Para episodios → usar las Bitácoras de Obsidian (registran el "dónde quedamos")
Para hechos → usar esta memoria (persiste entre sesiones)

Son complementarios, no equivalentes.
```

---

*Protocolo de Memoria v2.1 — Inspirado en Mark XXXIX-OR memory_manager.py*
*Compatible con: Antigravity | Codex (ChatGPT VSCode) | Claude Code*
*Firma: Jarvisin — Sistema Operativo de Jarvis Millonario*
