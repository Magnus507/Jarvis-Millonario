"""
TTS usando edge-tts (Microsoft, gratuito).
Playback via pygame — soporta MP3 nativamente en Windows.
"""
import asyncio
import tempfile
import os
import edge_tts
from config.settings import settings
from core import events

FALLBACK_VOICE = "es-MX-JorgeNeural"


async def speak(text: str):
    if not text or not settings.VOICE_ENABLED:
        return

    await events.publish("state_change", {"state": "speaking"})
    short_text = _trim_for_voice(text)

    try:
        voice = await _resolve_voice(settings.TTS_VOICE)
        communicate = edge_tts.Communicate(short_text, voice)

        with tempfile.NamedTemporaryFile(suffix=".mp3", delete=False) as f:
            tmp_path = f.name

        await communicate.save(tmp_path)
        await asyncio.get_event_loop().run_in_executor(None, _play_mp3, tmp_path)

    except Exception as e:
        print(f"[TTS Error] {e}")
    finally:
        try:
            os.unlink(tmp_path)
        except Exception:
            pass
        await events.publish("state_change", {"state": "idle"})


async def _resolve_voice(voice: str) -> str:
    """Verifica que la voz existe; si no, usa el fallback."""
    try:
        voices = await edge_tts.list_voices()
        available = {v["ShortName"] for v in voices}
        if voice in available:
            return voice
        print(f"[TTS] Voz '{voice}' no disponible. Usando: {FALLBACK_VOICE}")
        return FALLBACK_VOICE
    except Exception:
        return FALLBACK_VOICE


def _play_mp3(path: str):
    """Reproduce un MP3 usando pygame (soporta MP3 nativo en Windows)."""
    try:
        import pygame
        pygame.mixer.init()
        pygame.mixer.music.load(path)
        pygame.mixer.music.play()
        while pygame.mixer.music.get_busy():
            pygame.time.Clock().tick(10)
        pygame.mixer.music.stop()
        pygame.mixer.quit()
    except Exception as e:
        # Fallback: reproducir con Windows directamente
        print(f"[TTS] pygame falló ({e}), usando reproductor del sistema...")
        import subprocess
        subprocess.Popen(
            ["powershell", "-c", f'(New-Object Media.SoundPlayer).Play()'],
            stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL
        )
        # Esperar aprox la duración del audio
        import time
        time.sleep(3)


def _trim_for_voice(text: str) -> str:
    """Respuestas de voz cortas — reportes largos van a pantalla."""
    sentences = text.replace(".", ".|").replace("!", "!|").replace("?", "?|").split("|")
    sentences = [s.strip() for s in sentences if s.strip()]
    if len(sentences) <= 3:
        return text
    return " ".join(sentences[:3]) + "..."
