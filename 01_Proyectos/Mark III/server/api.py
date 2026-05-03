"""
FastAPI server: sirve la UI web y expone el WebSocket.
"""
from fastapi import FastAPI, WebSocket
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, JSONResponse
from pathlib import Path
from server.ws import handle_ws
from core.memory.sqlite_store import get_memory
from tools.registry import TOOL_REGISTRY
from config.settings import settings

BASE_DIR = Path(__file__).parent.parent
UI_DIR = BASE_DIR / "ui"

app = FastAPI(title="MARK III", version="3.0.0")
app.mount("/static", StaticFiles(directory=str(UI_DIR)), name="static")


@app.get("/")
async def root():
    return FileResponse(str(UI_DIR / "index.html"))


@app.websocket("/ws")
async def ws_endpoint(websocket: WebSocket):
    await handle_ws(websocket)


@app.get("/api/health")
async def health():
    return {"status": "online", "provider": settings.AI_PROVIDER, "name": settings.MARK_NAME}


@app.get("/api/tools")
async def list_tools():
    tools = [
        {
            "name": k,
            "description": v["declaration"]["description"],
            "category": v["category"],
            "risk": v["risk"],
        }
        for k, v in TOOL_REGISTRY.items()
    ]
    return JSONResponse({"tools": tools, "count": len(tools)})


@app.get("/api/memory")
async def api_memory():
    return JSONResponse({"memories": get_memory()})


@app.get("/api/status")
async def status():
    return JSONResponse({
        "provider": settings.AI_PROVIDER,
        "voice_enabled": settings.VOICE_ENABLED,
        "safe_mode": settings.SAFE_MODE,
        "tool_count": len(TOOL_REGISTRY),
        "wake_words": settings.WAKE_WORDS,
    })
