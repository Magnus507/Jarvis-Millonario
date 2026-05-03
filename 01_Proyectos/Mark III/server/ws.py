"""
WebSocket handler — comunicación bidireccional en tiempo real entre UI y backend.
"""
import json
import asyncio
from fastapi import WebSocket, WebSocketDisconnect
from core.brain import brain
from core.memory.sqlite_store import get_memory, upsert_memory
from core import events
from config.settings import settings


class ConnectionManager:
    def __init__(self):
        self.connections: list[WebSocket] = []

    async def connect(self, ws: WebSocket):
        await ws.accept()
        self.connections.append(ws)

    def disconnect(self, ws: WebSocket):
        if ws in self.connections:
            self.connections.remove(ws)

    async def broadcast(self, msg: dict):
        dead = []
        for ws in self.connections:
            try:
                await ws.send_json(msg)
            except Exception:
                dead.append(ws)
        for ws in dead:
            self.connections.remove(ws)


manager = ConnectionManager()


def _setup_event_relay():
    """Forward internal events to all WebSocket clients."""
    async def relay(data: dict):
        await manager.broadcast({"type": "event", **data})

    events.subscribe("state_change", relay)
    events.subscribe("message", relay)
    events.subscribe("tool_start", relay)
    events.subscribe("tool_end", relay)
    events.subscribe("error", relay)


_setup_event_relay()


async def handle_ws(websocket: WebSocket):
    await manager.connect(websocket)
    await manager.broadcast({"type": "state_change", "state": "idle"})

    try:
        while True:
            raw = await websocket.receive_text()
            data = json.loads(raw)
            action = data.get("action")

            if action == "chat":
                text = data.get("text", "").strip()
                if text:
                    asyncio.create_task(_process_and_reply(text, websocket))

            elif action == "memory_get":
                memories = get_memory()
                await websocket.send_json({"type": "memory", "data": memories})

            elif action == "memory_set":
                upsert_memory(data["category"], data["key"], data["value"])
                await websocket.send_json({"type": "ack", "message": "Memoria guardada"})

            elif action == "reset":
                brain.reset_conversation()
                await websocket.send_json({"type": "ack", "message": "Conversación reiniciada"})

            elif action == "settings_get":
                await websocket.send_json({
                    "type": "settings",
                    "provider": settings.AI_PROVIDER,
                    "voice": settings.VOICE_ENABLED,
                    "safe_mode": settings.SAFE_MODE,
                    "tts_voice": settings.TTS_VOICE,
                })

    except WebSocketDisconnect:
        manager.disconnect(websocket)
    except Exception as e:
        await websocket.send_json({"type": "error", "message": str(e)})
        manager.disconnect(websocket)


async def _process_and_reply(text: str, websocket: WebSocket):
    try:
        response = await brain.process(text)
        await manager.broadcast({"type": "message", "role": "assistant", "text": response})

        if settings.VOICE_ENABLED:
            from voice.speaker import speak
            asyncio.create_task(speak(response))
    except Exception as e:
        await manager.broadcast({"type": "error", "message": str(e)})
