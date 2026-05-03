from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Callable


JsonSchema = dict[str, Any]


@dataclass(frozen=True)
class ToolSpec:
    name: str
    description: str
    parameters: JsonSchema
    category: str
    risk: str = "safe"
    requires_confirmation: bool = False
    timeout_s: int = 60
    parallel_safe: bool = False
    aliases: tuple[str, ...] = field(default_factory=tuple)

    def declaration(self) -> dict[str, Any]:
        return {
            "name": self.name,
            "description": self.description,
            "parameters": self.parameters,
        }

    def planner_block(self) -> str:
        props = self.parameters.get("properties", {})
        required = set(self.parameters.get("required", []))
        lines = [self.name]
        for key, meta in props.items():
            marker = "required" if key in required else "optional"
            desc = meta.get("description", "")
            typ = meta.get("type", "ANY")
            lines.append(f"  {key}: {typ.lower()} ({marker}) - {desc}")
        if self.risk != "safe":
            lines.append(f"  risk: {self.risk}")
        return "\n".join(lines)


def _schema(properties: dict[str, Any], required: list[str] | None = None) -> JsonSchema:
    return {"type": "OBJECT", "properties": properties, "required": required or []}


def _prop(type_name: str, description: str, **extra: Any) -> dict[str, Any]:
    data = {"type": type_name, "description": description}
    data.update(extra)
    return data


TOOLS: tuple[ToolSpec, ...] = (
    ToolSpec(
        name="open_app",
        category="system",
        description="Opens or launches an application, website, or program on this computer.",
        parameters=_schema({"app_name": _prop("STRING", "Application, website, or program name, e.g. Chrome, WhatsApp, Spotify.")}, ["app_name"]),
    ),
    ToolSpec(
        name="web_search",
        category="research",
        description="Searches the web for information or compares items using search results.",
        parameters=_schema({
            "query": _prop("STRING", "Focused search query."),
            "mode": _prop("STRING", "search or compare. Default: search."),
            "items": {"type": "ARRAY", "items": {"type": "STRING"}, "description": "Items to compare."},
            "aspect": _prop("STRING", "Aspect to compare: price, specs, reviews, etc."),
        }, ["query"]),
        parallel_safe=True,
    ),
    ToolSpec(
        name="weather_report",
        category="research",
        description="Gets weather for a city.",
        parameters=_schema({"city": _prop("STRING", "City name.")}, ["city"]),
        parallel_safe=True,
    ),
    ToolSpec(
        name="send_message",
        category="communication",
        description="Sends a text message via WhatsApp, Telegram, Instagram, or another messaging platform.",
        parameters=_schema({
            "receiver": _prop("STRING", "Recipient contact name."),
            "message_text": _prop("STRING", "Message body."),
            "platform": _prop("STRING", "Messaging platform, e.g. WhatsApp or Telegram."),
        }, ["receiver", "message_text", "platform"]),
        risk="moderate",
        requires_confirmation=True,
    ),
    ToolSpec(
        name="reminder",
        category="productivity",
        description="Sets a timed reminder using Windows Task Scheduler.",
        parameters=_schema({
            "date": _prop("STRING", "Date in YYYY-MM-DD format."),
            "time": _prop("STRING", "Time in HH:MM 24-hour format."),
            "message": _prop("STRING", "Reminder text."),
        }, ["date", "time", "message"]),
    ),
    ToolSpec(
        name="youtube_video",
        category="media",
        description="Controls YouTube: play videos, summarize a video, get video info, or show trending videos.",
        parameters=_schema({
            "action": _prop("STRING", "play, summarize, get_info, or trending. Default: play."),
            "query": _prop("STRING", "Search query for play action."),
            "save": _prop("BOOLEAN", "Save summary to a file."),
            "region": _prop("STRING", "Country code for trending videos, e.g. US, PA."),
            "url": _prop("STRING", "Video URL for summarize/get_info."),
        }),
    ),
    ToolSpec(
        name="screen_process",
        category="vision",
        description="Captures and analyzes the screen or webcam. Required when the user asks what is visible.",
        parameters=_schema({
            "angle": _prop("STRING", "screen or camera. Default: screen."),
            "text": _prop("STRING", "Question or instruction about the captured image."),
        }, ["text"]),
        timeout_s=120,
    ),
    ToolSpec(
        name="computer_settings",
        category="system",
        description="Controls volume, brightness, windows, keyboard shortcuts, scrolling, tabs, screenshots, lock, restart, shutdown, wifi, and similar single computer actions.",
        parameters=_schema({
            "action": _prop("STRING", "Action to perform."),
            "description": _prop("STRING", "Natural language description of the action."),
            "value": _prop("STRING", "Optional value: level, text, key, etc."),
        }),
        risk="moderate",
    ),
    ToolSpec(
        name="browser_control",
        category="browser",
        description="Controls the browser: open websites, search, click elements, type, scroll, get page text, press keys, or close.",
        parameters=_schema({
            "action": _prop("STRING", "go_to, search, click, type, scroll, fill_form, smart_click, smart_type, get_text, press, close."),
            "url": _prop("STRING", "URL for go_to."),
            "query": _prop("STRING", "Search query."),
            "selector": _prop("STRING", "CSS selector for click/type."),
            "text": _prop("STRING", "Text to click/type/search."),
            "description": _prop("STRING", "Element description for smart actions."),
            "direction": _prop("STRING", "up or down for scroll."),
            "key": _prop("STRING", "Key name for press action."),
            "incognito": _prop("BOOLEAN", "Open private/incognito when supported."),
        }, ["action"]),
        risk="moderate",
        timeout_s=120,
    ),
    ToolSpec(
        name="file_controller",
        category="files",
        description="Manages files and folders: list, create, delete, move, copy, rename, read, write, find, disk usage, organize desktop, info.",
        parameters=_schema({
            "action": _prop("STRING", "list, create_file, create_folder, delete, move, copy, rename, read, write, find, largest, disk_usage, organize_desktop, info."),
            "path": _prop("STRING", "File/folder path or shortcut: desktop, downloads, documents, home."),
            "destination": _prop("STRING", "Destination path for move/copy."),
            "new_name": _prop("STRING", "New name for rename."),
            "content": _prop("STRING", "Content for create_file/write."),
            "name": _prop("STRING", "File name to search for."),
            "extension": _prop("STRING", "File extension to search."),
            "count": _prop("INTEGER", "Number of results for largest."),
        }, ["action"]),
        risk="moderate",
    ),
    ToolSpec(
        name="desktop_control",
        category="system",
        description="Controls desktop wallpaper, organization, cleaning, listing, stats, or a natural-language desktop task.",
        parameters=_schema({
            "action": _prop("STRING", "wallpaper, wallpaper_url, organize, clean, list, stats, task."),
            "path": _prop("STRING", "Image path for wallpaper."),
            "url": _prop("STRING", "Image URL for wallpaper_url."),
            "mode": _prop("STRING", "by_type or by_date."),
            "task": _prop("STRING", "Natural language desktop task."),
        }, ["action"]),
        risk="moderate",
    ),
    ToolSpec(
        name="code_helper",
        category="development",
        description="Writes, edits, explains, runs, builds, optimizes, or debugs code files.",
        parameters=_schema({
            "action": _prop("STRING", "write, edit, explain, run, build, screen_debug, optimize, auto."),
            "description": _prop("STRING", "What the code should do or what change to make."),
            "language": _prop("STRING", "Programming language. Default: python."),
            "output_path": _prop("STRING", "Where to save the file."),
            "file_path": _prop("STRING", "Existing file for edit/explain/run/build."),
            "code": _prop("STRING", "Raw code string for explain."),
            "args": _prop("STRING", "CLI arguments for run/build."),
            "timeout": _prop("INTEGER", "Execution timeout seconds."),
        }, ["action"]),
        risk="moderate",
        timeout_s=180,
    ),
    ToolSpec(
        name="dev_agent",
        category="development",
        description="Builds complete multi-file projects: plans, writes files, installs deps, opens VSCode, runs and fixes errors.",
        parameters=_schema({
            "description": _prop("STRING", "What the project should do."),
            "language": _prop("STRING", "Programming language. Default: python."),
            "project_name": _prop("STRING", "Optional project folder name."),
            "timeout": _prop("INTEGER", "Run timeout seconds."),
        }, ["description"]),
        risk="moderate",
        timeout_s=300,
    ),
    ToolSpec(
        name="agent_task",
        category="agent",
        description="Executes complex multi-step tasks requiring multiple different tools. Do not use for single commands or Steam/Epic requests.",
        parameters=_schema({
            "goal": _prop("STRING", "Complete description of what to accomplish."),
            "priority": _prop("STRING", "low, normal, or high. Default: normal."),
        }, ["goal"]),
        risk="moderate",
        timeout_s=300,
    ),
    ToolSpec(
        name="computer_control",
        category="system",
        description="Direct control: type, click, hotkeys, scroll, move mouse, screenshots, focus windows, find/click elements on screen.",
        parameters=_schema({
            "action": _prop("STRING", "type, smart_type, click, double_click, right_click, hotkey, press, scroll, move, copy, paste, screenshot, wait, clear_field, focus_window, screen_find, screen_click, random_data, user_data."),
            "text": _prop("STRING", "Text to type or paste."),
            "x": _prop("INTEGER", "X coordinate."),
            "y": _prop("INTEGER", "Y coordinate."),
            "keys": _prop("STRING", "Key combination, e.g. ctrl+c."),
            "key": _prop("STRING", "Single key, e.g. enter."),
            "direction": _prop("STRING", "up, down, left, right."),
            "amount": _prop("INTEGER", "Scroll amount."),
            "seconds": _prop("NUMBER", "Seconds to wait."),
            "title": _prop("STRING", "Window title for focus_window."),
            "description": _prop("STRING", "Element description for screen_find/screen_click."),
            "type": _prop("STRING", "Data type for random_data."),
            "field": _prop("STRING", "Field for user_data: name, email, city."),
            "clear_first": _prop("BOOLEAN", "Clear field before typing."),
            "path": _prop("STRING", "Save path for screenshot."),
        }, ["action"]),
        risk="moderate",
    ),
    ToolSpec(
        name="game_updater",
        category="gaming",
        description="The only tool for Steam or Epic Games: install, download, update, list games, status, scheduling updates.",
        parameters=_schema({
            "action": _prop("STRING", "update, install, list, download_status, schedule, cancel_schedule, schedule_status."),
            "platform": _prop("STRING", "steam, epic, or both. Default: both."),
            "game_name": _prop("STRING", "Game name; partial match supported."),
            "app_id": _prop("STRING", "Steam AppID for install."),
            "hour": _prop("INTEGER", "Hour for scheduled update, 0-23."),
            "minute": _prop("INTEGER", "Minute for scheduled update, 0-59."),
            "shutdown_when_done": _prop("BOOLEAN", "Shut down PC when download finishes."),
        }),
        risk="moderate",
        timeout_s=300,
    ),
    ToolSpec(
        name="flight_finder",
        category="travel",
        description="Searches Google Flights and reports the best options.",
        parameters=_schema({
            "origin": _prop("STRING", "Departure city or airport code."),
            "destination": _prop("STRING", "Arrival city or airport code."),
            "date": _prop("STRING", "Departure date, any format."),
            "return_date": _prop("STRING", "Return date for round trips."),
            "passengers": _prop("INTEGER", "Number of passengers."),
            "cabin": _prop("STRING", "economy, premium, business, first."),
            "save": _prop("BOOLEAN", "Save results to file/notepad."),
        }, ["origin", "destination", "date"]),
        timeout_s=180,
    ),
    ToolSpec(
        name="file_processor",
        category="files",
        description="Processes uploaded files: images, PDFs, docs, data, JSON/XML, code, audio, video, archives, presentations.",
        parameters=_schema({
            "file_path": _prop("STRING", "Full path to uploaded file; leave empty to use current uploaded file."),
            "action": _prop("STRING", "describe, ocr, resize, compress, convert, summarize, extract_text, to_word, fix, reformat, translate_hint, word_count, to_bullet, analyze, stats, filter, sort, validate, format, explain, review, run, document, test, transcribe, trim, info, extract_audio, extract_frame, list, extract."),
            "instruction": _prop("STRING", "Free-form instruction if action does not cover it."),
            "format": _prop("STRING", "Target conversion format."),
            "width": _prop("INTEGER", "Target width."),
            "height": _prop("INTEGER", "Target height."),
            "scale": _prop("NUMBER", "Scale factor."),
            "quality": _prop("INTEGER", "Quality 1-100."),
            "start": _prop("STRING", "Start time for trim."),
            "end": _prop("STRING", "End time for trim."),
            "timestamp": _prop("STRING", "Timestamp for frame extraction."),
            "column": _prop("STRING", "Column name for CSV filter/sort."),
            "value": _prop("STRING", "Filter value."),
            "condition": _prop("STRING", "equals, contains, gt, lt."),
            "ascending": _prop("BOOLEAN", "Sort order."),
            "save": _prop("BOOLEAN", "Save result to file."),
            "destination": _prop("STRING", "Output folder for extraction."),
        }),
        risk="moderate",
        timeout_s=300,
    ),
    ToolSpec(
        name="shutdown_jarvis",
        category="system",
        description="Shuts down the assistant completely when the user clearly wants to end the assistant session.",
        parameters=_schema({}),
        risk="dangerous",
        requires_confirmation=True,
    ),
    ToolSpec(
        name="save_memory",
        category="memory",
        description="Silently save an important personal fact about the user to long-term memory.",
        parameters=_schema({
            "category": _prop("STRING", "identity, preferences, projects, relationships, wishes, notes."),
            "key": _prop("STRING", "Short snake_case key."),
            "value": _prop("STRING", "Concise value in English."),
        }, ["category", "key", "value"]),
        parallel_safe=True,
    ),
)


TOOL_REGISTRY: dict[str, ToolSpec] = {tool.name: tool for tool in TOOLS}
for tool in TOOLS:
    for alias in tool.aliases:
        TOOL_REGISTRY[alias] = tool

TOOL_DECLARATIONS: list[dict[str, Any]] = [tool.declaration() for tool in TOOLS]


def get_tool(name: str) -> ToolSpec | None:
    return TOOL_REGISTRY.get((name or "").strip())


def get_tool_names(include_internal: bool = True) -> list[str]:
    names = []
    for tool in TOOLS:
        if not include_internal and tool.category in {"memory"}:
            continue
        names.append(tool.name)
    return names


def planner_tool_reference() -> str:
    return "\n\n".join(tool.planner_block() for tool in TOOLS if tool.name not in {"save_memory", "shutdown_jarvis"})


def registry_summary() -> dict[str, Any]:
    categories: dict[str, int] = {}
    risks: dict[str, int] = {}
    for tool in TOOLS:
        categories[tool.category] = categories.get(tool.category, 0) + 1
        risks[tool.risk] = risks.get(tool.risk, 0) + 1
    return {
        "tool_count": len(TOOLS),
        "categories": categories,
        "risks": risks,
        "tools": [
            {
                "name": tool.name,
                "category": tool.category,
                "risk": tool.risk,
                "requires_confirmation": tool.requires_confirmation,
                "timeout_s": tool.timeout_s,
            }
            for tool in TOOLS
        ],
    }
