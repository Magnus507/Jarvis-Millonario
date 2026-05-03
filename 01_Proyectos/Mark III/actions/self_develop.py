"""
Auto-desarrollo: Mark III puede escribir nuevas capacidades para sí mismo.
Cuando el usuario pide una nueva habilidad, usa el AI para generarla,
la guarda como módulo y la carga en caliente.
"""
import asyncio
import importlib
import importlib.util
from pathlib import Path
from tools.registry import register
from config.settings import settings


ACTIONS_DIR = Path(settings.ACTIONS_DIR)


async def self_develop(capability_description: str) -> str:
    """Genera e integra una nueva capacidad usando el AI."""
    from core.providers import get_provider

    provider = get_provider()

    prompt = f"""
You are generating a new Python module for MARK III, an AI assistant.
The user wants a new capability: "{capability_description}"

Write a complete Python module that:
1. Implements the requested functionality
2. Registers itself using tools/registry.py's `register()` function
3. Follows the existing pattern from other action modules
4. Works on Windows
5. Has proper error handling

Return ONLY valid Python code, no markdown, no explanations.
The module should start with a docstring explaining what it does.
"""

    response = await provider.chat([{"role": "user", "content": prompt}])
    code = response["text"].strip()

    if code.startswith("```"):
        code = code.split("```")[1]
        if code.startswith("python"):
            code = code[6:]

    safe_name = capability_description.lower()[:30].replace(" ", "_").replace("-", "_")
    safe_name = "".join(c for c in safe_name if c.isalnum() or c == "_")
    module_path = ACTIONS_DIR / f"learned_{safe_name}.py"

    module_path.write_text(code, encoding="utf-8")

    try:
        spec = importlib.util.spec_from_file_location(f"actions.learned_{safe_name}", module_path)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        return f"Nueva capacidad creada y cargada: '{capability_description}'. Módulo: learned_{safe_name}.py"
    except Exception as e:
        module_path.unlink(missing_ok=True)
        return f"El código generado tuvo errores: {e}. Intenta con una descripción más específica."


async def list_learned_capabilities() -> str:
    """Lista todas las capacidades aprendidas."""
    learned = list(ACTIONS_DIR.glob("learned_*.py"))
    if not learned:
        return "No hay capacidades aprendidas aún."
    return "Capacidades aprendidas:\n" + "\n".join(f"- {p.stem.replace('learned_', '')}" for p in learned)


async def improve_tool(tool_name: str, improvement: str) -> str:
    """Mejora una herramienta existente."""
    from core.providers import get_provider
    from tools.registry import TOOL_REGISTRY

    if tool_name not in TOOL_REGISTRY:
        return f"Herramienta '{tool_name}' no encontrada."

    tool_file = ACTIONS_DIR / f"{tool_name.split('_')[0]}*.py"
    files = list(ACTIONS_DIR.glob("*.py"))
    matching = [f for f in files if tool_name in f.read_text(encoding="utf-8", errors="replace")]

    if not matching:
        return f"No encontré el archivo fuente de '{tool_name}'."

    source = matching[0].read_text(encoding="utf-8")
    provider = get_provider()

    prompt = f"""
Improve this Python function from MARK III's action module.
Requested improvement: "{improvement}"

Current source file:
```python
{source[:3000]}
```

Return ONLY the improved complete file. No markdown, no explanations.
"""
    response = await provider.chat([{"role": "user", "content": prompt}])
    new_code = response["text"].strip()
    if new_code.startswith("```"):
        new_code = new_code.split("```")[1]
        if new_code.startswith("python"):
            new_code = new_code[6:]

    backup = matching[0].with_suffix(".py.bak")
    backup.write_text(source, encoding="utf-8")
    matching[0].write_text(new_code, encoding="utf-8")

    return f"Herramienta '{tool_name}' mejorada. Backup guardado en {backup.name}"


register(
    name="self_develop",
    description="Permite que Mark III aprenda y cree nuevas capacidades. Describe qué habilidad quieres que aprenda.",
    parameters={
        "capability_description": {"type": "string", "description": "Descripción de la nueva capacidad a crear", "required": True},
    },
    executor=self_develop,
    category="meta",
    timeout=60,
)

register(
    name="list_learned_capabilities",
    description="Lista todas las capacidades que Mark III ha aprendido.",
    parameters={},
    executor=list_learned_capabilities,
    category="meta",
)

register(
    name="improve_tool",
    description="Mejora una herramienta existente de Mark III.",
    parameters={
        "tool_name": {"type": "string", "description": "Nombre de la herramienta a mejorar", "required": True},
        "improvement": {"type": "string", "description": "Qué mejorar", "required": True},
    },
    executor=improve_tool,
    category="meta",
    timeout=60,
)
