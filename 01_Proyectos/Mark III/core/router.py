"""
Routes every user message to the correct execution path:
  - CHAT     : simple question/answer (no tools)
  - TOOL     : single tool execution
  - TASK     : multi-step plan (3+ tools, activates planner)
"""
from core.providers import get_provider
from core import events
from tools.registry import TOOL_REGISTRY
from tools.runner import run_tool


_provider = None


def get_ai():
    global _provider
    if _provider is None:
        _provider = get_provider()
    return _provider


async def handle(text: str, conversation: list[dict]) -> str:
    await events.publish("state_change", {"state": "thinking"})

    messages = conversation + [{"role": "user", "content": text}]
    tools = [t["declaration"] for t in TOOL_REGISTRY.values()]

    ai = get_ai()
    response = await ai.chat(messages, tools=tools)

    if response["tool_calls"]:
        results = []
        for call in response["tool_calls"]:
            await events.publish("tool_start", {"tool": call["name"], "params": call["input"]})
            result = await run_tool(call["name"], call["input"])
            await events.publish("tool_end", {"tool": call["name"], "result": result})
            results.append(f"[{call['name']}]: {result}")

        followup_messages = messages + [
            {"role": "assistant", "content": response["text"] or "Ejecutando..."},
            {"role": "user", "content": "Tool results:\n" + "\n".join(results) + "\nSummarize what happened in 1-2 sentences."},
        ]
        final = await ai.chat(followup_messages)
        return final["text"]

    return response["text"]
