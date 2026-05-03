---
categoria: proyectos
updated: 2026-05-01
descripcion: Contexto condensado y estado actual de proyectos activos
---

# 🚀 Proyectos Activos

> Este archivo es el **resumen ejecutivo** de cada proyecto. Para contexto completo, ir a `01_Proyectos/`.

---

## 🎵 Eternum Records

```yaml
tipo: Disquera digital con IA
estado: En operación activa
fase: Ejecución de lanzamientos + monitoreo de analíticas
artista_principal: La Trilogía de Oro
genero: Corridos modernos / tumbados
produccion: Suno AI v5.5
distribuidor: Symphonic

# ─── MÉTRICAS (corte 2026-04-28) ──────────────────────────────
total_reproducciones: 2657
spotify_streams: 2439
oyentes_mensuales_spotify: 510
seguidores_spotify: 6
youtube_art_tracks: 216
apple_music: 0
instagram_seguidores: 2

# ─── CATÁLOGO ──────────────────────────────────────────────────
singles_lanzados: 7
singles_aprobados_en_cola: 4
total_canciones_documentadas: 11

top_3_canciones:
  1: "Polako — 1,131 reproducciones"
  2: "La Lancha — 977 reproducciones"
  3: "Entre Rutas — 374 reproducciones"

# ─── PRÓXIMOS LANZAMIENTOS ─────────────────────────────────────
proximo_lanzamiento: "No Era Locura — 2026-04-29"
siguiente: "Con eso me basta — 2026-05-04"
siguiente_2: "Rumbo al millón — 2026-05-11"
siguiente_3: "Mi Girasol — 2026-06-05"

# ─── PIPELINE FUTURO ───────────────────────────────────────────
ep_en_incubadora: "Sombra Digital (5 temas — Corrido Tumbado Cyber-Noir)"
album_en_incubadora: "El Reloj de Arena (15 temas)"

# ─── SKILLS ACTIVAS ────────────────────────────────────────────
skills_especializadas:
  - Skill_Eternum_Growth (TikTok, hooks, audiencia)
  - Skill_Eternum_Visuals (prompts Midjourney, branding)
  - Skill_Eternum_Rights (regalías, copyright IA, Symphonic)
  - Skill_Eternum_A_R (nichos, competencia, sonido)
  - Agente_Suno_Experto (letras + prompts Suno)
```

---

## 🏥 Plataforma Médica Panamá

```yaml
tipo: Ecosistema digital de salud
estado: Prototipado — arquitectura técnica definida
fase: Definición de Arquitectura + Prototipado Visual
pais_objetivo: Panamá
referencia_internacional: "HCDSNS (España) + Doctoralia"

# ─── PROPUESTA DE VALOR ────────────────────────────────────────
para_pacientes:
  - Perfil Médico Personal (PMP) con historial longitudinal
  - Timeline de consultas, diagnósticos, recetas, exámenes
  - Compartir perfil via QR o PIN temporal

para_medicos:
  - Perfil profesional público con credenciales
  - Dashboard clínico con lector QR
  - Notas de evolución por paciente

# ─── ARQUITECTURA TÉCNICA DEFINIDA ────────────────────────────
bd: PostgreSQL / Supabase
frontend: React / Next.js
tablas_principales: usuarios, perfiles_doctores, registros_medicos, citas, especialidades
autenticacion: Row Level Security (Supabase)
privacidad: Permisos temporales QR (max 2 horas)

# ─── DISEÑO UI/UX ──────────────────────────────────────────────
estilo: Glassmorphism (tarjetas de cristal)
colores_primarios: "Azul Médico #0F52BA / Verde Esmeralda suave"
tipografia: Inter o Roboto
pantallas_definidas: Dashboard Paciente, Buscador Especialistas, Portal Doctor

# ─── ESTADO ACTUAL ─────────────────────────────────────────────
completado:
  - Esquema relacional PostgreSQL/Supabase
  - Concepto UI/UX completo
  - Mockups de Timeline y Buscador
  - Propuesta de monetización

pendiente:
  - Validación legal (Ley 81 de Panamá — protección datos médicos)
  - Validar con 5 médicos + 10 pacientes
  - Prototipo interactivo (Figma o código)
  - Stack final confirmado

bloqueo_actual: "Pendiente revisión Ley 81 Panamá"
monetizacion: "Freemium médicos + Gratis pacientes + % por cita pagada"
```

---

## PreRescue ID

```yaml
tipo: Proyecto externo registrado en Jarvi
estado: Activo - pendiente de instrucciones
fase: Registrado para trabajo futuro
ubicacion_local: "C:\\Users\\geank\\OneDrive\\Desktop\\Jarvi Millonario\\01_Proyectos\\PreRescue ID"
nota_maestra: "01_Proyectos/PreRescue ID.md"
github_repo: "https://github.com/Magnus507/PreRescatePTY.git"

reglas_operativas:
  - "No leer, editar, ejecutar ni modificar archivos de PreRescue ID sin instruccion explicita del usuario."
  - "PreRescue ID vive dentro de 01_Proyectos, pero mantiene repositorio Git separado del Vault Jarvi Millonario."
  - "Los cambios de memoria/documentacion de Jarvi se suben al GitHub de Jarvi."
  - "Los cambios de PreRescue ID se suben aparte al GitHub propio de PreRescue ID."
  - "Cuando se suba PreRescue ID, actualizar tambien Jarvi Millonario y hacer push separado."

control_versiones: "GitHub independiente; no mezclar commits ni pushes con Jarvi Millonario"
```

---

## 🤖 MARK III — Asistente Personal de IA

```yaml
tipo: Asistente AI Personal tipo JARVIS de Iron Man
estado: Código completo — pendiente configurar .env y hacer setup
fase: Listo para instalación
ubicacion: "01_Proyectos/Mark III/"
version: 3.0.0
created: 2026-05-01

arquitectura:
  backend: Python + FastAPI + WebSocket
  frontend: Web UI + Three.js orb reactiva
  stt: faster-whisper (local)
  tts: edge-tts (gratuito, voz Roberto Panamá)
  wake_words: "hola mark", "mark tres", "mark 3"
  
proveedores_ia:
  principal: Claude (Anthropic) — claude-sonnet-4-6
  secundario: Gemini (Google) — gemini-2.0-flash-exp
  fallback: Ollama (local, sin internet)

capacidades:
  - Control de PC: volumen, mute, brillo, bloqueo, apagado
  - Abrir/cerrar aplicaciones (aliases en español)
  - Control navegador (Playwright): YouTube, WhatsApp Web
  - Control VSCode + Antigravity (Claude Code CLI)
  - Operaciones de archivos
  - Captura y análisis de pantalla
  - Búsqueda web (DuckDuckGo, sin API key)
  - Auto-desarrollo: puede aprender nuevas capacidades
  - Memoria SQLite con FTS5
  - Agentes: Planner + Executor + QA

setup:
  paso_1: "cp .env.example .env → agregar API keys"
  paso_2: "python setup.py → instala todo"
  paso_3: "python main.py → abre navegador automáticamente"

notas:
  - Mark II tenía el problema de correr 2 cosas en paralelo. Mark III usa un solo proceso FastAPI limpio.
  - La orb Three.js cambia de color según el estado: azul=idle, verde=escuchando, naranja=pensando, cyan=hablando
  - La voz usa es-PA-RobertoNeural (voz panameña masculina)
```

---

## 🤖 Jarvis Millonario (El Sistema Mismo)

```yaml
tipo: Vault Obsidian — Sistema Operativo Colaborativo
estado: Activo y en evolución
version_jarvisin: 2.0
metodologia: PARA
equipo: 2-3 personas
control_versiones: Git + GitHub
ia_orquestadora: Jarvisin (Claude Code)

modulos_activos:
  - Memoria Persistente (v2.0)
  - Protocolo de Agente Autónomo (v2.0)
  - Skills Core (Business, Research, Structure, Technical)
  - Skills Eternum (Growth, Visuals, Rights, A&R)
  - Agente Suno Experto

meta_sistema: "Vault 100% autónomo, documentado y escalable"
```
