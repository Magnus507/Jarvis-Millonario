import anthropic
from typing import AsyncGenerator
from .base import AIProvider
from config.settings import settings


class ClaudeProvider(AIProvider):
    name = "claude"

    def __init__(self):
        self.client = anthropic.AsyncAnthropic(api_key=settings.ANTHROPIC_API_KEY)
        self.model = settings.CLAUDE_MODEL

    def is_available(self) -> bool:
        return bool(settings.ANTHROPIC_API_KEY)

    async def chat(self, messages: list[dict], tools: list[dict] | None = None) -> dict:
        kwargs = {
            "model": self.model,
            "max_tokens": 4096,
            "system": settings.SYSTEM_PROMPT,
            "messages": messages,
        }
        if tools:
            kwargs["tools"] = tools

        response = await self.client.messages.create(**kwargs)

        tool_calls = None
        text_parts = []

        for block in response.content:
            if block.type == "text":
                text_parts.append(block.text)
            elif block.type == "tool_use":
                if tool_calls is None:
                    tool_calls = []
                tool_calls.append({
                    "id": block.id,
                    "name": block.name,
                    "input": block.input,
                })

        return {"text": " ".join(text_parts), "tool_calls": tool_calls}

    async def chat_stream(self, messages: list[dict]) -> AsyncGenerator[str, None]:
        async with self.client.messages.stream(
            model=self.model,
            max_tokens=2048,
            system=settings.SYSTEM_PROMPT,
            messages=messages,
        ) as stream:
            async for text in stream.text_stream:
                yield text
