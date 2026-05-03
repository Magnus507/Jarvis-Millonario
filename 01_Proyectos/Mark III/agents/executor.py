"""
Executor: ejecuta el plan del Planner paso a paso.
Maneja dependencias entre pasos e inyecta resultados como contexto.
"""
import asyncio
from tools.runner import run_tool
from core import events


async def execute_plan(plan: dict) -> str:
    steps = plan.get("steps", [])
    results: dict[int, any] = {}

    for step in steps:
        step_num = step["step"]
        tool = step["tool"]
        params = step.get("params", {})
        depends_on = step.get("depends_on", [])

        for dep in depends_on:
            if dep not in results:
                results[step_num] = f"Error: paso {dep} no completado."
                continue

        await events.publish("tool_start", {"tool": tool, "params": params, "step": step_num})

        result = await run_tool(tool, params)
        results[step_num] = result

        await events.publish("tool_end", {"tool": tool, "result": result, "step": step_num})

    summary_lines = [f"**{plan.get('goal', 'Tarea completada')}**\n"]
    for step in steps:
        num = step["step"]
        tool = step["tool"]
        result = results.get(num, "no ejecutado")
        summary_lines.append(f"✓ [{tool}]: {str(result)[:200]}")

    return "\n".join(summary_lines)
