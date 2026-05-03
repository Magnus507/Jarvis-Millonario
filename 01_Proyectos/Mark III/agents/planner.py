"""
Planner: descompone tareas complejas en pasos ejecutables.
Se activa cuando el router detecta 3+ herramientas necesarias.
"""
from core.providers import get_provider
from tools.registry import TOOL_REGISTRY
import json


PLANNER_PROMPT = """
You are the Planner for MARK III, an AI assistant.
Your job: decompose complex tasks into ordered steps using available tools.

Available tools: {tools}

User request: {request}

Return a JSON plan with this exact structure:
{{
  "goal": "one sentence goal",
  "steps": [
    {{"step": 1, "tool": "tool_name", "params": {{"param": "value"}}, "depends_on": []}},
    {{"step": 2, "tool": "tool_name", "params": {{"param": "value"}}, "depends_on": [1]}}
  ]
}}

Rules:
- Max 5 steps
- Only use tools from the available list
- depends_on: list of step numbers that must complete first (empty list if none)
- params: exact parameters the tool expects
- Return ONLY valid JSON, no markdown
"""


async def plan(request: str) -> dict:
    provider = get_provider()
    tool_names = list(TOOL_REGISTRY.keys())

    prompt = PLANNER_PROMPT.format(
        tools=", ".join(tool_names),
        request=request,
    )

    response = await provider.chat([{"role": "user", "content": prompt}])
    text = response["text"].strip()

    if text.startswith("```"):
        text = text.split("```")[1]
        if text.startswith("json"):
            text = text[4:]

    try:
        return json.loads(text)
    except json.JSONDecodeError:
        return {
            "goal": request,
            "steps": [
                {"step": 1, "tool": "web_search", "params": {"query": request}, "depends_on": []}
            ],
        }
