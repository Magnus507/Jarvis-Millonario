import asyncio
from typing import Callable

_subscribers: dict[str, list[Callable]] = {}


def subscribe(event: str, callback: Callable):
    _subscribers.setdefault(event, []).append(callback)


async def publish(event: str, data: dict):
    for cb in _subscribers.get(event, []):
        try:
            if asyncio.iscoroutinefunction(cb):
                await cb(data)
            else:
                cb(data)
        except Exception:
            pass


# Standard events:
# "state_change"   → {"state": "idle"|"listening"|"thinking"|"speaking"|"error"}
# "message"        → {"role": "user"|"assistant", "text": str}
# "tool_start"     → {"tool": str, "params": dict}
# "tool_end"       → {"tool": str, "result": any}
# "memory_update"  → {"key": str, "value": str}
# "error"          → {"message": str}
