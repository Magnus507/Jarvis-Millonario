# MARK II - Roadmap de Evolucion Inspirado en Otros Jarvis

Fecha: 2026-05-01
Estado: propuesta escrita. No se han hecho cambios de codigo.
Voz: mantener la voz actual de Gemini Live. No migrar a ElevenLabs por ahora.

## Objetivo

Convertir MARK II en un Jarvis mas estable, visual, modular y escalable, sin perder su ventaja principal: funciona en Windows y ya controla acciones reales del computador.

La idea no es reemplazar MARK II por otro proyecto. La idea es tomar lo mejor de tres referencias:

- Ethanplusai/Jarvis: inspiracion visual, experiencia de voz y arquitectura backend/frontend.
- Bertrand/Jarvis: tool registry, multi-agent, dashboard, runtime settings y control operativo.
- Microsoft/JARVIS: modelo conceptual de planner -> model/tool selection -> execution -> response generation.

## Principio Rector

MARK II debe seguir siendo Windows-first, practico y accionable. Cualquier mejora visual o arquitectonica debe reforzar esa base, no convertirlo en un clon macOS ni en un demo academico pesado.

## Que Sacar De Ethanplusai/Jarvis

### 1. Orbe Cinematica

Tomar como inspiracion la orbe reactiva tipo Three.js:

- Particulas en varias capas.
- Deformacion segun estado: idle, listening, thinking, speaking, error.
- Pulso de audio cuando Jarvis habla.
- Arcos electricos y anillos holograficos.
- Transiciones suaves entre estados.

Aplicacion en MARK II:

- Fase rapida: mejorar la orbe PyQt actual en `ui.py`.
- Fase premium: incrustar una vista web/Three.js dentro de PyQt o crear un frontend web separado.

Decision recomendada:

- Mantener PyQt como app nativa.
- Crear una orbe web en Three.js embebida o conectada por WebSocket.

### 2. Separacion Backend/Frontend

Ethanplusai separa mejor la experiencia visual del cerebro.

Aplicacion en MARK II:

- Crear un backend local con FastAPI/WebSocket.
- Dejar PyQt como cliente visual.
- Permitir un dashboard web opcional.
- Enviar eventos por WebSocket: listening, thinking, speaking, tool_started, tool_finished, error.

Beneficio:

- La UI deja de depender tanto de `main.py`.
- Podemos tener varias interfaces: PyQt, web dashboard, futura app movil.

### 3. Memoria SQLite Con Busqueda

MARK II usa memoria JSON. Funciona, pero escala mal.

Aplicacion en MARK II:

- Migrar `memory/long_term.json` hacia SQLite.
- Usar FTS5 para busqueda textual.
- Guardar hechos, preferencias, proyectos, errores, acciones exitosas y notas.

Tablas sugeridas:

- `memories`: facts, preferences, personal_context, projects.
- `conversations`: resumen por sesion.
- `tool_runs`: historial de herramientas.
- `procedures`: pasos aprendidos para tareas repetidas.

### 4. Respuestas De Voz Cortas

Ethanplusai limita respuestas habladas a 1-2 frases.

Aplicacion en MARK II:

- Mantener respuestas habladas cortas.
- Mostrar reportes largos en texto.
- Jarvis debe hablar como operador, no como articulo.

### 5. Work Mode

Idea: sesiones largas de trabajo que sobreviven reinicios.

Aplicacion en MARK II:

- Guardar tareas largas en disco/SQLite.
- Poder pausar, continuar o cancelar proyectos.
- Integrar con `dev_agent.py` y `agent/task_queue.py`.

## Que Sacar De Bertrand/Jarvis

### 1. Tool Registry Central

Este es probablemente el cambio arquitectonico mas importante.

Problema actual:

- Las herramientas estan duplicadas en `main.py`, `agent/planner.py` y `agent/executor.py`.
- Si cambia una herramienta, hay que actualizar varios lugares.
- Hay referencia a `cmd_control`, pero no aparece `actions/cmd_control.py`.

Solucion:

Crear un registry unico, por ejemplo:

- `core/tools/registry.py`
- `core/tools/schemas.py`
- `core/tools/permissions.py`

Cada herramienta debe declarar:

- nombre
- descripcion corta
- parametros JSON schema
- funcion ejecutora
- categoria
- riesgo: safe, moderate, dangerous
- requiere confirmacion: true/false
- timeout
- si puede ejecutarse en paralelo

Beneficio:

- Gemini Live lee las mismas herramientas que el planner.
- El executor llama desde la misma fuente de verdad.
- El dashboard puede mostrar herramientas disponibles automaticamente.

### 2. Multi-Agent Real

MARK II ya tiene planner/executor/error_handler, pero se puede formalizar.

Agentes recomendados:

- Router: decide si es chat, herramienta simple o tarea compleja.
- Planner: descompone tareas multi-step.
- Executor: ejecuta herramientas.
- QA: verifica si el resultado realmente cumple el objetivo.
- Memory: decide que recordar.
- Safety: revisa acciones peligrosas.

Beneficio:

- Menos acciones impulsivas.
- Mejor recuperacion de errores.
- Mejor planificacion para tareas largas.

### 3. Dashboard Operativo

Crear dashboard local para ver el estado de Jarvis.

Paneles sugeridos:

- Estado actual: listening, thinking, speaking, executing.
- Herramienta activa.
- Cola de tareas.
- Ultimos errores.
- Memoria reciente.
- Uso por proveedor: Gemini, OpenRouter, futuro ElevenLabs.
- Costo estimado.
- Modelos activos.
- Permisos y modo seguro.

### 4. Runtime Settings

Permitir cambiar opciones sin editar archivos.

Settings sugeridos:

- modelo principal
- modelo economico
- voz actual
- volumen
- modo silencioso
- limite de costo mensual
- confirmacion para acciones peligrosas
- navegador predeterminado
- nivel de autonomia

Nota:

- Mantener la voz actual por ahora.
- ElevenLabs debe quedar como proveedor opcional futuro, no activo.

### 5. QA Agent

Antes de decir "listo", Jarvis deberia revisar:

- La herramienta devolvio exito real?
- El archivo fue creado?
- La busqueda produjo datos?
- El navegador llego a la pagina correcta?
- La tarea necesita otro paso?

Esto evita respuestas falsas de completado.

## Que Sacar De Microsoft/JARVIS

Microsoft/JARVIS no es un asistente personal tipo Iron Man. Es un proyecto de investigacion tambien conocido como HuggingGPT: un LLM controlador que conecta con muchos modelos expertos de Hugging Face.

Lo rescatable para MARK II no es instalarlo completo, sino copiar su flujo mental:

1. Task Planning: entender la solicitud y partirla en tareas.
2. Model/Tool Selection: elegir la herramienta o modelo adecuado.
3. Task Execution: ejecutar herramientas/modelos.
4. Response Generation: integrar resultados y responder.

Aplicacion en MARK II:

- Usar este flujo como contrato interno del agent system.
- Mejorar el planner para representar dependencias entre pasos.
- Guardar grafos de tarea simples cuando haya pasos dependientes.
- Permitir que el QA verifique cada etapa.

Tambien vale la pena estudiar EasyTool:

- Convertir documentacion larga de herramientas en instrucciones cortas y consistentes.
- Esto encaja perfecto con el futuro `tool_registry`.

Y TaskBench:

- Crear pruebas de tareas para MARK II.
- Evaluar si el planner elige bien herramientas y parametros.

## Voz

Decision actual:

- No cambiar la voz.
- Mantener Gemini Live con la voz actual configurada en MARK II.

ElevenLabs queda como opcion futura.

Si se agrega despues:

- Debe ser proveedor opcional.
- Debe tener limite mensual.
- Debe usar cache de frases comunes.
- Debe usarse solo para respuestas cortas.
- Reportes largos deben mostrarse en texto, no leerse completos.

## Arquitectura Propuesta

Estructura futura sugerida:

```text
Mark II/
  app/
    main.py
  core/
    brain/
      router.py
      model_provider.py
      prompts.py
    tools/
      registry.py
      schemas.py
      permissions.py
      runner.py
    agents/
      planner.py
      executor.py
      qa.py
      safety.py
      memory_agent.py
    memory/
      sqlite_store.py
      migrations.py
    events/
      bus.py
      types.py
  actions/
    open_app.py
    browser_control.py
    computer_control.py
    file_controller.py
    file_processor.py
    game_updater.py
  server/
    api.py
    websocket.py
  ui/
    desktop_pyqt/
    web_dashboard/
  config/
    settings.example.json
    .env.example
  tests/
    test_tool_registry.py
    test_planner.py
    test_memory.py
```

## Fases Recomendadas

### Fase 1: Higiene y Seguridad

- Renombrar referencias internas de MARK XXXIX/MARK XXV a MARK II.
- Mover secretos a `.env`.
- Crear `.env.example`.
- Agregar `.gitignore` especifico para config/secrets.
- Corregir o eliminar referencia a `cmd_control` si no existe.
- Crear tests minimos de importacion.

### Fase 2: Tool Registry

- Crear registry central.
- Migrar declaraciones de herramientas desde `main.py`.
- Hacer que `planner.py` consuma el registry.
- Hacer que `executor.py` ejecute desde el registry.
- Agregar permisos por riesgo.

### Fase 3: Memoria SQLite

- Crear `memory.sqlite`.
- Migrar JSON actual.
- Agregar busqueda FTS5.
- Guardar ejecuciones de herramientas.

### Fase 4: Eventos y Dashboard

- Crear event bus interno.
- Exponer WebSocket local.
- Dashboard con estado, herramientas, costos, errores y memoria.

### Fase 5: Orbe Premium

- Mejorar orbe PyQt actual.
- Crear version Three.js si se quiere visual top.
- Conectar estados por WebSocket/event bus.

### Fase 6: Multi-Agent y QA

- Separar router, planner, executor, QA, safety y memory.
- Agregar verificacion antes de responder completado.
- Guardar resultados para aprendizaje.

### Fase 7: Voz Premium Opcional

- Mantener Gemini Live por defecto.
- Agregar ElevenLabs solo como proveedor opcional.
- Agregar limite de costo y cache.

## Orden Recomendado Para Empezar

1. Tool registry central.
2. Seguridad/config con `.env`.
3. Memoria SQLite.
4. Event bus + dashboard basico.
5. Orbe visual mejorada.
6. Multi-agent con QA.

## Veredicto

MARK II ya tiene el cuerpo: controla Windows, usa voz, ejecuta herramientas y tiene vision. Lo que le falta es columna vertebral de producto: registry, memoria seria, dashboard, eventos y QA.

Ethanplusai aporta alma visual.
Bertrand aporta cabina de control.
Microsoft/JARVIS aporta el patron academico para pensar tareas como grafo de planificacion, seleccion, ejecucion y respuesta.

## Implementacion Inicial Completada - 2026-05-01

Se implemento una primera fase real de la evolucion, manteniendo la voz actual intacta.

Cambios aplicados:

- Tool registry central en `core/tools/registry.py`.
- Runner central en `core/tools/runner.py` para evitar duplicacion entre Live, planner y executor.
- `main.py` ahora usa `TOOL_DECLARATIONS` desde el registry.
- `agent/planner.py` genera su lista de herramientas desde el registry y bloquea `cmd_control`/`generated_code` como herramientas planificables.
- `agent/executor.py` ejecuta herramientas registradas desde `core.tools`.
- Event bus local en `core/events/bus.py`.
- SQLite store inicial en `memory/sqlite_store.py` para memoria nueva y telemetria de herramientas.
- Dispatch registry en `core/dispatch_registry.py` para tareas largas.
- `agent/task_queue.py` registra tareas en dispatches y publica eventos.
- Dashboard FastAPI opcional en `server/dashboard.py` con `/`, `/health` y `/status`.
- `.env.example` y `config/secrets.py` para permitir secretos por variables de entorno sin romper compatibilidad con `config/api_keys.json`.
- Tests basicos del registry en `tests/test_tool_registry.py`.
- Dependencias nuevas: `fastapi`, `uvicorn`, `pytest`.

Verificacion:

- `python -m compileall '01_Proyectos\\Mark II'` paso correctamente.
- Tests manuales del registry pasaron correctamente.
- La voz sigue usando `Charon` de Gemini Live.
