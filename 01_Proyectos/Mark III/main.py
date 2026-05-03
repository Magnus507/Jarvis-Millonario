"""
MARK III — Entry Point
Starts the FastAPI server, opens the browser UI, and activates voice listening.
"""
import asyncio
import sys
import os
import webbrowser
import threading
from pathlib import Path

# Ensure the project root is in sys.path
ROOT = Path(__file__).parent
sys.path.insert(0, str(ROOT))

# Load env before anything else
from dotenv import load_dotenv
load_dotenv()

from config.settings import settings
from core.memory.sqlite_store import init_db
from core import events


def _print_banner():
    print("""
╔══════════════════════════════════════════════════════╗
║                    M A R K  I I I                    ║
║         Personal AI Operating System v3.0            ║
╠══════════════════════════════════════════════════════╣
║  Provider : {provider:<41}║
║  Voice    : {voice:<41}║
║  Safe Mode: {safe:<41}║
║  URL      : http://{host}:{port:<33}║
╚══════════════════════════════════════════════════════╝
""".format(
        provider=settings.AI_PROVIDER.upper(),
        voice="ON — " + settings.TTS_VOICE if settings.VOICE_ENABLED else "OFF",
        safe="ON" if settings.SAFE_MODE else "OFF",
        host=settings.HOST,
        port=settings.PORT,
    ))


def _start_voice_listener(loop):
    """Run voice listener in a background thread."""
    if not settings.VOICE_ENABLED:
        print("[Voice] Desactivado (VOICE_ENABLED=false)")
        return

    from voice.listener import VoiceListener
    from core.brain import brain

    async def on_command(text: str):
        print(f"[Voice] Comando: '{text}'")
        response = await brain.process(text, source="voice")
        from voice.speaker import speak
        await speak(response)

    def run_listener():
        listener = VoiceListener(on_command=on_command)
        listener.start()
        threading.Event().wait()

    t = threading.Thread(target=run_listener, daemon=True)
    t.start()
    print(f"[Voice] Wake words activas: {settings.WAKE_WORDS}")


def main():
    # Init database
    init_db()

    _print_banner()

    import uvicorn
    from server.api import app

    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)

    # Start voice listener
    _start_voice_listener(loop)

    # Auto-open browser
    if settings.AUTO_OPEN_BROWSER:
        url = f"http://{settings.HOST}:{settings.PORT}"
        threading.Timer(1.5, lambda: webbrowser.open(url)).start()

    print(f"[Mark III] Servidor activo en http://{settings.HOST}:{settings.PORT}")
    print("[Mark III] Presiona Ctrl+C para apagar.\n")

    uvicorn.run(
        app,
        host=settings.HOST,
        port=settings.PORT,
        log_level=settings.LOG_LEVEL.lower(),
        loop="asyncio",
    )


if __name__ == "__main__":
    main()
