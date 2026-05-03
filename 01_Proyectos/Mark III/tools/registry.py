"""
Central tool registry — single source of truth for ALL capabilities.
Each tool: declaration (for AI), executor (Python function), metadata.
"""
from typing import Callable


TOOL_REGISTRY: dict[str, dict] = {}


def register(
    name: str,
    description: str,
    parameters: dict,
    executor: Callable,
    category: str = "general",
    risk: str = "safe",
    requires_confirm: bool = False,
    timeout: int = 30,
):
    TOOL_REGISTRY[name] = {
        "declaration": {
            "name": name,
            "description": description,
            "input_schema": {
                "type": "object",
                "properties": parameters,
                "required": [k for k, v in parameters.items() if v.get("required", False)],
            },
        },
        "executor": executor,
        "category": category,
        "risk": risk,
        "requires_confirm": requires_confirm,
        "timeout": timeout,
    }


def _load_all_tools():
    """Import all action modules so they self-register."""
    import actions.computer_control   # noqa: F401
    import actions.open_app           # noqa: F401
    import actions.browser_control    # noqa: F401
    import actions.youtube            # noqa: F401
    import actions.whatsapp           # noqa: F401
    import actions.vscode_control     # noqa: F401
    import actions.file_control       # noqa: F401
    import actions.screen             # noqa: F401
    import actions.web_search         # noqa: F401
    import actions.self_develop       # noqa: F401


_load_all_tools()
