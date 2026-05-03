from abc import ABC, abstractmethod
from typing import AsyncGenerator

class AIProvider(ABC):
    name: str = "base"

    @abstractmethod
    async def chat(self, messages: list[dict], tools: list[dict] | None = None) -> dict:
        """Returns {"text": str, "tool_calls": list | None}"""

    @abstractmethod
    async def chat_stream(self, messages: list[dict]) -> AsyncGenerator[str, None]:
        """Yields text chunks for streaming."""

    def is_available(self) -> bool:
        return True
