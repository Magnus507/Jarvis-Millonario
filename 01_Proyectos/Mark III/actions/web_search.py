"""
Búsqueda web real usando DuckDuckGo (sin API key necesaria).
Fallback: Google via scraping con Playwright.
"""
import httpx
from tools.registry import register


async def web_search(query: str, max_results: int = 5) -> str:
    try:
        return await _ddg_search(query, max_results)
    except Exception as e:
        return f"Error en búsqueda: {e}"


async def _ddg_search(query: str, max_results: int) -> str:
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}
    url = f"https://html.duckduckgo.com/html/?q={query.replace(' ', '+')}"

    async with httpx.AsyncClient(timeout=10, headers=headers) as client:
        resp = await client.get(url)
        resp.raise_for_status()

    from html.parser import HTMLParser

    class DDGParser(HTMLParser):
        def __init__(self):
            super().__init__()
            self.results = []
            self.in_result = False
            self.current_title = ""
            self.current_snippet = ""

        def handle_starttag(self, tag, attrs):
            attrs = dict(attrs)
            if tag == "a" and "result__a" in attrs.get("class", ""):
                self.in_result = True
            if tag == "a" and "result__snippet" in attrs.get("class", ""):
                self.in_snippet = True

        def handle_data(self, data):
            if self.in_result and not self.current_title:
                self.current_title = data.strip()
                self.in_result = False
                self.results.append({"title": self.current_title, "snippet": ""})

    parser = DDGParser()
    parser.feed(resp.text)

    if not parser.results:
        return f"No se encontraron resultados para: '{query}'"

    lines = [f"Resultados para '{query}':"]
    for i, r in enumerate(parser.results[:max_results], 1):
        lines.append(f"{i}. {r['title']}")

    return "\n".join(lines)


async def fetch_page_content(url: str) -> str:
    if not url.startswith("http"):
        url = "https://" + url
    try:
        headers = {"User-Agent": "Mozilla/5.0"}
        async with httpx.AsyncClient(timeout=15, headers=headers, follow_redirects=True) as client:
            resp = await client.get(url)
            resp.raise_for_status()

        from html.parser import HTMLParser

        class TextExtractor(HTMLParser):
            def __init__(self):
                super().__init__()
                self.text = []
                self.skip = False

            def handle_starttag(self, tag, attrs):
                self.skip = tag in ("script", "style", "nav", "footer")

            def handle_endtag(self, tag):
                if tag in ("script", "style", "nav", "footer"):
                    self.skip = False

            def handle_data(self, data):
                if not self.skip and data.strip():
                    self.text.append(data.strip())

        extractor = TextExtractor()
        extractor.feed(resp.text)
        text = " ".join(extractor.text)
        return text[:3000]
    except Exception as e:
        return f"Error cargando página: {e}"


register(
    name="web_search",
    description="Busca información en internet sobre cualquier tema.",
    parameters={
        "query": {"type": "string", "description": "Qué buscar", "required": True},
        "max_results": {"type": "integer", "description": "Número de resultados (default 5)"},
    },
    executor=web_search,
    category="research",
    timeout=15,
)

register(
    name="fetch_page",
    description="Lee el contenido de texto de una página web.",
    parameters={"url": {"type": "string", "description": "URL de la página", "required": True}},
    executor=fetch_page_content,
    category="research",
    timeout=20,
)
