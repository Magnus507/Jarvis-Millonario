---
skill: Inteligencia de Código y Arquitectura
agent: Jarvisin
version: 2.0
fuente_inspiracion: Mark XXXIX-OR (code_helper.py + dev_agent.py + executor.py)
---

# 💻 Skill: Inteligencia de Código y Arquitectura

Este módulo faculta a Jarvisin para **escribir, revisar, explicar y arquitectar** código y sistemas técnicos dentro de Jarvis Millonario. Aplicación primaria: **Plataforma Médica Panamá**.

---

## 🎯 Cuándo Activar Esta Skill

- El usuario pide código, esquemas, consultas SQL o arquitectura técnica
- Se necesita revisar o mejorar código existente
- Se necesita explicar cómo funciona algo técnico
- Se necesita diseñar una nueva feature o componente de la Plataforma Médica
- Se necesita generar migraciones, seeds o scripts de BD

---

## 📋 Capacidades

### 1. Escritura de Código (`write`)
- **Qué genera:** Componentes React, endpoints API, schemas SQL, scripts Python
- **Estándar:** Código limpio, sin comentarios innecesarios, con nombres descriptivos
- **Stack de referencia:** PostgreSQL/Supabase, React/Next.js, Python, TypeScript

**Casos de uso frecuentes:**
```
- "Escribe la tabla SQL para permisos_temporales (QR de acceso médico)"
- "Crea el componente React del Timeline médico del paciente"
- "Genera el script de seed con especialidades médicas de Panamá"
- "Escribe el endpoint de Supabase para compartir QR con PIN temporal"
```

### 2. Revisión de Código (`review`)
- **Qué revisa:** Seguridad, rendimiento, correctitud, cumplimiento de RLS de Supabase
- **Entrega:** Lista de issues por severidad + código corregido
- **Foco especial:** Vulnerabilidades OWASP en contexto médico (SQL injection, XSS, acceso no autorizado)

### 3. Explicación Técnica (`explain`)
- **Qué explica:** Cómo funciona una decisión de arquitectura, por qué se eligió X sobre Y
- **Nivel:** Adaptado al usuario (puede leer código, no necesita sobre-explicaciones)
- **Foco:** El PORQUÉ más que el QUÉ (el código ya muestra el qué)

### 4. Construcción de Proyectos Completos (`build`)
- **Qué construye:** Estructura completa de un módulo o feature con todos sus archivos
- **Proceso:**
  1. Planificar estructura de archivos
  2. Escribir cada archivo
  3. Escribir instrucciones de instalación/ejecución
  4. Registrar en documentación del proyecto
- **Caso de uso:** "Construye el módulo completo de autenticación para la Plataforma Médica"

### 5. Optimización (`optimize`)
- **Qué optimiza:** Queries SQL lentas, componentes React con re-renders innecesarios, esquemas de BD
- **Entrega:** Código optimizado + explicación de la mejora y su impacto

---

## 🔐 Estándares de Seguridad (Obligatorios en Plataforma Médica)

```
SIEMPRE aplicar en código de Plataforma Médica:

✅ Row Level Security (RLS) en TODAS las tablas de Supabase
✅ Validar que pacientes solo accedan a SUS registros
✅ Permisos temporales QR con expiración estricta (máx 2 horas)
✅ Encriptar campos sensibles: diagnostico, prescripcion, archivos_adjuntos
✅ Nunca exponer IDs reales en URLs — usar UUIDs
✅ Sanitizar inputs médicos antes de guardar en BD
✅ Auditoría de accesos: quién vio qué y cuándo

NUNCA en código de Plataforma Médica:
❌ SQL concatenado con strings de usuario (SQL injection)
❌ Datos médicos en localStorage o sessionStorage
❌ Endpoints sin autenticación que retornen datos de pacientes
❌ Logs con información médica identificable
```

---

## 🗄️ Stack de Referencia (Plataforma Médica)

```yaml
base_de_datos: PostgreSQL via Supabase
orm: Supabase JS Client / Supabase Python Client
autenticacion: Supabase Auth (JWT)
storage: Supabase Storage (para archivos adjuntos médicos)
frontend: React / Next.js (App Router)
estilos: Tailwind CSS + Glassmorphism
tipado: TypeScript
testing: Jest (unit) + Playwright (e2e)
despliegue: Vercel (frontend) + Supabase (backend)
```

---

## 📐 Patrones de Código Preferidos

### SQL / Supabase
```sql
-- Usar CTEs para queries complejas, no subqueries anidadas
WITH paciente_registros AS (
  SELECT * FROM registros_medicos 
  WHERE paciente_id = auth.uid()
  AND publico_para_doctores = true
)
SELECT * FROM paciente_registros ORDER BY fecha_consulta DESC;

-- Siempre incluir RLS policy junto al CREATE TABLE
ALTER TABLE registros_medicos ENABLE ROW LEVEL SECURITY;
CREATE POLICY "pacientes_ven_sus_registros" ON registros_medicos
  FOR SELECT USING (paciente_id = auth.uid());
```

### React / Next.js
```typescript
// Server Components por defecto, Client Components solo cuando necesario
// Evitar useEffect para data fetching — usar Server Actions o Route Handlers
// Nombres descriptivos > comentarios: fetchPatientTimeline() no getData()
```

---

## 📑 Protocolo de Entrega

El código generado se guarda en:
- `01_Proyectos/Proyecto de medicina/` → Para código de la plataforma médica
- `02_Recursos/Código/` → Para snippets reutilizables

Formato de entrega:

```
💻 Código: [qué se genera]
Stack: [tecnología usada]

[bloque de código]

📋 Instrucciones:
1. [Cómo ejecutar/implementar]
2. [Dependencias necesarias]

⚠️ Consideraciones:
- [Implicación de seguridad o rendimiento importante]

📁 Guardado en: [[ruta/a/la/nota]]
```

---

## 🚀 Modo Dev Agent (Proyectos Completos)

Para construir un módulo completo desde cero, esta skill ejecuta:

```
1. PLANIFICAR estructura de archivos
2. ESCRIBIR cada archivo secuencialmente
3. GENERAR script de setup (install + env + seed)
4. DOCUMENTAR en la nota del proyecto
5. REGISTRAR en bitácora del proyecto
```

**Límite:** Si el módulo tiene +10 archivos, dividirlo en sub-tareas y usar `Skill_Task_Orchestrator`.

---

*Skill: Inteligencia de Código v2.0 — Inspirado en Mark XXXIX-OR code_helper + dev_agent*
*Módulo de Skill: v2.0*
