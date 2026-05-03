import google.generativeai as genai
from typing import AsyncGenerator
from .base import AIProvider
from config.settings import settings


class GeminiProvider(AIProvider):
    name = "gemini"

    def __init__(self):
        if settings.GEMINI_API_KEY:
            genai.configure(api_key=settings.GEMINI_API_KEY)
        self.model_name = settings.GEMINI_MODEL

    def is_available(self) -> bool:
        return bool(settings.GEMINI_API_KEY)

    def _get_model(self, tools=None):
        config = genai.GenerationConfig(max_output_tokens=4096)
        return genai.GenerativeModel(
            model_name=self.model_name,
            system_instruction=settings.SYSTEM_PROMPT,
            generation_config=config,
            tools=tools or [],
        )

    def _to_gemini_messages(self, messages: list[dict]) -> list[dict]:
        result = []
        for m in messages:
            role = "user" if m["role"] == "user" else "model"
            content = m["content"]
            if isinstance(content, str):
                result.append({"role": role, "parts": [content]})
        return result

    async def chat(self, messages: list[dict], tools: list[dict] | None = None) -> dict:
        model = self._get_model(tools)
        history = self._to_gemini_messages(messages[:-1])
        last = messages[-1]["content"]

        chat = model.start_chat(history=history)
        response = await chat.send_message_async(last)

        tool_calls = None
        text = ""

        for part in response.parts:
            if hasattr(part, "text") and part.text:
                text += part.text
            elif hasattr(part, "function_call") and part.function_call.name:
                if tool_calls is None:
                    tool_calls = []
                tool_calls.append({
                    "id": f"gemini_{len(tool_calls)}",
                    "name": part.function_call.name,
                    "input": dict(part.function_call.args),
                })

        return {"text": text, "tool_calls": tool_calls}

    async def chat_stream(self, messages: list[dict]) -> AsyncGenerator[str, None]:
        model = self._get_model()
        history = self._to_gemini_messages(messages[:-1])
        last = messages[-1]["content"]

        chat = model.start_chat(history=history)
        async for chunk in await chat.send_message_async(last, stream=True):
            if chunk.text:
                yield chunk.text
