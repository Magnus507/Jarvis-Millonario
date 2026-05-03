"""
Control de navegador via Playwright.
Puede abrir URLs, hacer clic, escribir, navegar, extraer contenido.
"""
import asyncio
from tools.registry import register

_browser = None
_page = None


async def _get_page():
    global _browser, _page
    if _browser is None:
        from playwright.async_api import async_playwright
        pw = await async_playwright().start()
        _browser = await pw.chromium.launch(headless=False)
        _page = await _browser.new_page()
    return _page


async def open_url(url: str) -> str:
    if not url.startswith("http"):
        url = "https://" + url
    page = await _get_page()
    await page.goto(url, wait_until="domcontentloaded", timeout=15000)
    return f"Navegando a: {url}"


async def browser_click(selector: str) -> str:
    page = await _get_page()
    await page.click(selector, timeout=5000)
    return f"Click en: {selector}"


async def browser_type(selector: str, text: str) -> str:
    page = await _get_page()
    await page.fill(selector, text)
    return f"Texto ingresado en {selector}"


async def browser_get_text(selector: str = "body") -> str:
    page = await _get_page()
    text = await page.inner_text(selector)
    return text[:2000]


async def browser_screenshot() -> str:
    import os
    from pathlib import Path
    from datetime import datetime

    page = await _get_page()
    save_dir = Path.home() / "Pictures" / "Mark3"
    save_dir.mkdir(parents=True, exist_ok=True)
    path = str(save_dir / f"browser_{datetime.now().strftime('%H%M%S')}.png")
    await page.screenshot(path=path)
    return f"Captura del navegador: {path}"


async def browser_search(query: str, engine: str = "google") -> str:
    engines = {
        "google": f"https://www.google.com/search?q={query.replace(' ', '+')}",
        "bing": f"https://www.bing.com/search?q={query.replace(' ', '+')}",
        "duckduckgo": f"https://duckduckgo.com/?q={query.replace(' ', '+')}",
    }
    url = engines.get(engine.lower(), engines["google"])
    await open_url(url)
    await asyncio.sleep(2)
    return f"Búsqueda realizada: '{query}' en {engine}"


async def browser_close() -> str:
    global _browser, _page
    if _browser:
        await _browser.close()
        _browser = None
        _page = None
    return "Navegador cerrado"


register(
    name="open_url",
    description="Abre una URL en el navegador.",
    parameters={"url": {"type": "string", "description": "URL a abrir", "required": True}},
    executor=open_url,
    category="browser",
    timeout=20,
)

register(
    name="browser_search",
    description="Realiza una búsqueda web en el navegador.",
    parameters={
        "query": {"type": "string", "description": "Término de búsqueda", "required": True},
        "engine": {"type": "string", "description": "Motor: google, bing, duckduckgo"},
    },
    executor=browser_search,
    category="browser",
    timeout=20,
)

register(
    name="browser_get_text",
    description="Extrae el texto de la página web actual.",
    parameters={"selector": {"type": "string", "description": "Selector CSS (default: body)"}},
    executor=browser_get_text,
    category="browser",
    timeout=10,
)

register(
    name="browser_click",
    description="Hace click en un elemento de la página web.",
    parameters={"selector": {"type": "string", "description": "Selector CSS del elemento", "required": True}},
    executor=browser_click,
    category="browser",
)

register(
    name="browser_type",
    description="Escribe texto en un campo de la página web.",
    parameters={
        "selector": {"type": "string", "description": "Selector CSS del campo", "required": True},
        "text": {"type": "string", "description": "Texto a ingresar", "required": True},
    },
    executor=browser_type,
    category="browser",
)
