import asyncio
from core.memory.sqlite_store import log_tool_run


async def run_tool(name: str, params: dict) -> any:
    from tools.registry import TOOL_REGISTRY
    from config.settings import settings

    entry = TOOL_REGISTRY.get(name)
    if not entry:
        return f"Error: herramienta '{name}' no encontrada."

    if entry["requires_confirm"] and settings.SAFE_MODE:
        return f"Acción '{name}' requiere confirmación del usuario (safe_mode activo)."

    executor = entry["executor"]
    timeout = entry["timeout"]

    try:
        if asyncio.iscoroutinefunction(executor):
            result = await asyncio.wait_for(executor(**params), timeout=timeout)
        else:
            result = await asyncio.wait_for(
                asyncio.get_event_loop().run_in_executor(None, lambda: executor(**params)),
                timeout=timeout,
            )
        log_tool_run(name, params, result, success=True)
        return result
    except asyncio.TimeoutError:
        log_tool_run(name, params, "timeout", success=False)
        return f"Error: '{name}' tomó demasiado tiempo (>{timeout}s)."
    except Exception as e:
        log_tool_run(name, params, str(e), success=False)
        return f"Error en '{name}': {e}"
