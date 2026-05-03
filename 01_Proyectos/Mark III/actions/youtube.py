"""
Interacción con YouTube — buscar, reproducir, pausar, volumen, siguiente.
"""
import asyncio
from tools.registry import register


async def youtube_search(query: str) -> str:
    from actions.browser_control import open_url, _get_page
    search_url = f"https://www.youtube.com/results?search_query={query.replace(' ', '+')}"
    await open_url(search_url)
    await asyncio.sleep(2)

    page = await _get_page()
    try:
        first_video = await page.query_selector("a#video-title")
        if first_video:
            await first_video.click()
            return f"Reproduciendo primer resultado de: '{query}'"
    except Exception:
        pass
    return f"Búsqueda de YouTube abierta: '{query}'"


async def youtube_play_pause() -> str:
    from actions.browser_control import _get_page
    page = await _get_page()
    await page.keyboard.press("k")
    return "Play/Pause toggled"


async def youtube_next() -> str:
    from actions.browser_control import _get_page
    page = await _get_page()
    await page.keyboard.press("shift+n")
    return "Siguiente video"


async def youtube_fullscreen() -> str:
    from actions.browser_control import _get_page
    page = await _get_page()
    await page.keyboard.press("f")
    return "Pantalla completa toggled"


async def youtube_seek(seconds: int) -> str:
    from actions.browser_control import _get_page
    page = await _get_page()
    if seconds > 0:
        for _ in range(abs(seconds) // 5):
            await page.keyboard.press("l")
    else:
        for _ in range(abs(seconds) // 5):
            await page.keyboard.press("j")
    return f"Adelantado {abs(seconds)} segundos"


async def youtube_volume(level: int) -> str:
    from actions.browser_control import _get_page
    page = await _get_page()
    await page.evaluate(f"""
        const video = document.querySelector('video');
        if (video) video.volume = {max(0, min(100, level)) / 100};
    """)
    return f"Volumen de YouTube: {level}%"


register(
    name="youtube_search",
    description="Busca y reproduce un video en YouTube.",
    parameters={"query": {"type": "string", "description": "Búsqueda de YouTube", "required": True}},
    executor=youtube_search,
    category="media",
    timeout=15,
)

register(
    name="youtube_play_pause",
    description="Pausa o reanuda el video de YouTube.",
    parameters={},
    executor=youtube_play_pause,
    category="media",
)

register(
    name="youtube_next",
    description="Pasa al siguiente video de YouTube.",
    parameters={},
    executor=youtube_next,
    category="media",
)

register(
    name="youtube_fullscreen",
    description="Activa o desactiva pantalla completa en YouTube.",
    parameters={},
    executor=youtube_fullscreen,
    category="media",
)

register(
    name="youtube_volume",
    description="Ajusta el volumen del video de YouTube.",
    parameters={"level": {"type": "integer", "description": "Volumen 0-100", "required": True}},
    executor=youtube_volume,
    category="media",
)
