from __future__ import annotations

import threading
import time
from typing import Any, Callable

from core.events import publish
from core.tools.registry import get_tool
from memory.sqlite_store import record_tool_run


def execute_tool(
    name: str,
    parameters: dict[str, Any] | None = None,
    *,
    player: Any = None,
    speak: Callable[[str], Any] | None = None,
    current_file: str | None = None,
) -> str:
    """Execute a MARK II tool by name using the central registry.

    This keeps main.py, planner.py, and executor.py aligned around one tool list.
    Voice is intentionally not changed here; callers keep their current speak path.
    """

    args = dict(parameters or {})
    spec = get_tool(name)
    if spec is None:
        raise ValueError(f"Unknown tool: {name}")

    started = time.perf_counter()
    publish("tool_started", name=name, category=spec.category, risk=spec.risk)
    try:
        result = _execute_known_tool(name, args, player=player, speak=speak, current_file=current_file)
        record_tool_run(name, True, time.perf_counter() - started)
        publish("tool_finished", name=name, ok=True, result=str(result)[:500])
        return result or "Done."
    except Exception as exc:
        record_tool_run(name, False, time.perf_counter() - started, str(exc))
        publish("tool_finished", name=name, ok=False, error=str(exc)[:500])
        raise


def _execute_known_tool(
    name: str,
    args: dict[str, Any],
    *,
    player: Any,
    speak: Callable[[str], Any] | None,
    current_file: str | None,
) -> str:
    if name == "open_app":
        from actions.open_app import open_app
        return open_app(parameters=args, response=None, player=player) or f"Opened {args.get('app_name')}."

    if name == "weather_report":
        from actions.weather_report import weather_action
        return weather_action(parameters=args, player=player) or "Weather delivered."

    if name == "browser_control":
        from actions.browser_control import browser_control
        return browser_control(parameters=args, player=player) or "Done."

    if name == "file_controller":
        from actions.file_controller import file_controller
        return file_controller(parameters=args, player=player) or "Done."

    if name == "send_message":
        from actions.send_message import send_message
        return send_message(parameters=args, response=None, player=player, session_memory=None) or f"Message sent to {args.get('receiver')}."

    if name == "reminder":
        from actions.reminder import reminder
        return reminder(parameters=args, response=None, player=player) or "Reminder set."

    if name == "youtube_video":
        from actions.youtube_video import youtube_video
        return youtube_video(parameters=args, response=None, player=player) or "Done."

    if name == "file_processor":
        from actions.file_processor import file_processor
        if not args.get("file_path") and current_file:
            args["file_path"] = current_file
        return file_processor(parameters=args, player=player, speak=speak) or "Done."

    if name == "screen_process":
        from actions.screen_processor import screen_process
        threading.Thread(
            target=screen_process,
            kwargs={"parameters": args, "response": None, "player": player, "session_memory": None},
            daemon=True,
        ).start()
        return "Vision module activated. Stay silent; the vision module will report directly."

    if name == "computer_settings":
        from actions.computer_settings import computer_settings
        return computer_settings(parameters=args, response=None, player=player) or "Done."

    if name == "desktop_control":
        from actions.desktop import desktop_control
        return desktop_control(parameters=args, player=player) or "Done."

    if name == "code_helper":
        from actions.code_helper import code_helper
        return code_helper(parameters=args, player=player, speak=speak) or "Done."

    if name == "dev_agent":
        from actions.dev_agent import dev_agent
        return dev_agent(parameters=args, player=player, speak=speak) or "Done."

    if name == "agent_task":
        from agent.task_queue import TaskPriority, get_queue
        priority_map = {"low": TaskPriority.LOW, "normal": TaskPriority.NORMAL, "high": TaskPriority.HIGH}
        priority = priority_map.get(str(args.get("priority", "normal")).lower(), TaskPriority.NORMAL)
        task_id = get_queue().submit(goal=args.get("goal", ""), priority=priority, speak=speak)
        return f"Task started (ID: {task_id})."

    if name == "web_search":
        from actions.web_search import web_search
        return web_search(parameters=args, player=player) or "Done."

    if name == "computer_control":
        from actions.computer_control import computer_control
        return computer_control(parameters=args, player=player) or "Done."

    if name == "game_updater":
        from actions.game_updater import game_updater
        return game_updater(parameters=args, player=player, speak=speak) or "Done."

    if name == "flight_finder":
        from actions.flight_finder import flight_finder
        return flight_finder(parameters=args, player=player) or "Done."

    raise ValueError(f"Tool is registered but has no runner: {name}")
