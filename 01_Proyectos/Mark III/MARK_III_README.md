# MARK III — Personal AI Operating System

> Inspirado en JARVIS de Iron Man. Construido desde cero el 2026-05-01.

---

## Inicio Rápido

```bash
# 1. Setup (solo la primera vez)
python setup.py

# 2. Editar .env con tus API keys
# (copiar .env.example → .env)

# 3. Iniciar
.venv\Scripts\python main.py
```

Abre automáticamente http://localhost:8765

---

## Activación por Voz

Di cualquiera de estas frases:
- **"Hola Mark"**
- **"Mark tres"**  
- **"Mark 3"**

Luego habla tu comando directamente.

---

## Capacidades

| Categoría | Comandos |
|---|---|
| **Sistema** | "sube el volumen a 80", "silencia", "bloquea el pc", "apaga en 10 minutos" |
| **Apps** | "abre Spotify", "abre Chrome", "abre VSCode" |
| **YouTube** | "busca música de corridos en YouTube", "pausa el video", "siguiente" |
| **WhatsApp** | "abre WhatsApp", "manda mensaje a Juan" |
| **Archivos** | "lee el archivo X", "crea el archivo Y con este contenido" |
| **Pantalla** | "¿qué hay en mi pantalla?", "toma una captura" |
| **Búsqueda** | "busca en internet sobre X" |
| **VSCode** | "abre la carpeta del proyecto", "ejecuta npm install" |
| **Auto-desarrollo** | "aprende a controlar Spotify", "mejórate" |

---

## Proveedores de IA

Se configura en `.env` → `AI_PROVIDER=claude|gemini|local`

| Proveedor | Cuándo usar |
|---|---|
| **Claude** (Anthropic) | Principal — mejor calidad |
| **Gemini** (Google) | Alternativa — gratuito |
| **Local** (Ollama) | Sin internet ni tokens |

Fallback automático: si Claude falla → Gemini → Local.

---

## Arquitectura

```
main.py                 ← Entry point (FastAPI + Voice)
├── core/
│   ├── brain.py        ← Cerebro central (conversación + memoria)
│   ├── router.py       ← Enruta: chat / tool / task
│   ├── providers/      ← Claude, Gemini, Ollama
│   ├── memory/         ← SQLite con FTS5
│   └── events/         ← Event bus interno
├── voice/
│   ├── listener.py     ← STT + Wake Word (faster-whisper)
│   └── speaker.py      ← TTS (edge-tts)
├── tools/
│   ├── registry.py     ← Fuente única de todas las herramientas
│   └── runner.py       ← Ejecutor con timeout y logging
├── actions/            ← Módulos de capacidades
│   ├── computer_control.py
│   ├── open_app.py
│   ├── browser_control.py
│   ├── youtube.py
│   ├── whatsapp.py
│   ├── vscode_control.py
│   ├── file_control.py
│   ├── screen.py
│   ├── web_search.py
│   └── self_develop.py ← Auto-aprendizaje
├── agents/
│   ├── planner.py      ← Descompone tareas complejas
│   ├── executor.py     ← Ejecuta el plan
│   └── qa.py           ← Verifica resultados
├── server/
│   ├── api.py          ← FastAPI + endpoints
│   └── ws.py           ← WebSocket bidireccional
└── ui/
    ├── index.html
    ├── app.js          ← Three.js orb + chat
    └── styles.css
```

---

## Auto-Desarrollo

Mark III puede aprender nuevas capacidades en caliente:

```
"Mark, aprende a controlar Spotify"
"Mark, aprende a leer correos de Gmail"
"Mark, mejora la herramienta de búsqueda web"
```

Los módulos aprendidos se guardan en `actions/learned_*.py` y se cargan automáticamente.

---

## Variables de Entorno (.env)

```env
AI_PROVIDER=claude              # claude | gemini | local
ANTHROPIC_API_KEY=sk-ant-...
GEMINI_API_KEY=AIza...
VOICE_ENABLED=true
WAKE_WORDS=hola mark,mark tres
TTS_VOICE=es-PA-RobertoNeural
SAFE_MODE=true                  # Confirma antes de acciones peligrosas
```

---

*MARK III v3.0.0 — Creado 2026-05-01*
