import httpx
from typing import AsyncGenerator
from .base import AIProvider
from config.settings import settings


class LocalProvider(AIProvider):
    """Ollama via OpenAI-compatible API — runs fully offline."""
    name = "local"

    def __init__(self):
        self.base_url = settings.OLLAMA_BASE_URL.rstrip("/")
        self.model = settings.OLLAMA_MODEL

    def is_available(self) -> bool:
        try:
            import httpx
            r = httpx.get(f"{self.base_url}/api/tags", timeout=2)
            return r.status_code == 200
        except Exception:
            return False

    def _build_payload(self, messages: list[dict], stream: bool = False) -> dict:
        full = [{"role": "system", "content": settings.SYSTEM_PROMPT}] + messages
        return {"model": self.model, "messages": full, "stream": stream}

    async def chat(self, messages: list[dict], tools: list[dict] | None = None) -> dict:
        async with httpx.AsyncClient(timeout=60) as client:
            r = await client.post(
                f"{self.base_url}/api/chat",
                json=self._build_payload(messages),
            )
            r.raise_for_status()
            data = r.json()
            text = data.get("message", {}).get("content", "")
            return {"text": text, "tool_calls": None}

    async def chat_stream(self, messages: list[dict]) -> AsyncGenerator[str, None]:
        import json
        async with httpx.AsyncClient(timeout=60) as client:
            async with client.stream(
                "POST",
                f"{self.base_url}/api/chat",
                json=self._build_payload(messages, stream=True),
            ) as resp:
                async for line in resp.aiter_lines():
                    if line:
                        try:
                            chunk = json.loads(line)
                            content = chunk.get("message", {}).get("content", "")
                            if content:
                                yield content
                        except json.JSONDecodeError:
                            pass
