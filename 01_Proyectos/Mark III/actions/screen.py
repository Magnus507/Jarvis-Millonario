"""
Captura y análisis de pantalla. Envía screenshots al AI para "ver" lo que hay.
"""
import asyncio
from tools.registry import register


def capture_screen() -> str:
    import pyautogui
    from pathlib import Path
    from datetime import datetime

    save_dir = Path.home() / "Pictures" / "Mark3"
    save_dir.mkdir(parents=True, exist_ok=True)
    path = str(save_dir / f"screen_{datetime.now().strftime('%H%M%S')}.png")
    img = pyautogui.screenshot()
    img.save(path)
    return path


async def analyze_screen(question: str = "¿Qué hay en la pantalla?") -> str:
    import base64
    from pathlib import Path
    from core.providers import get_provider

    path = capture_screen()
    img_bytes = Path(path).read_bytes()
    b64 = base64.b64encode(img_bytes).decode()

    provider = get_provider()
    if provider.name == "claude":
        from anthropic import AsyncAnthropic
        from config.settings import settings
        client = AsyncAnthropic(api_key=settings.ANTHROPIC_API_KEY)
        response = await client.messages.create(
            model=settings.CLAUDE_MODEL,
            max_tokens=1024,
            messages=[{
                "role": "user",
                "content": [
                    {"type": "image", "source": {"type": "base64", "media_type": "image/png", "data": b64}},
                    {"type": "text", "text": question},
                ],
            }],
        )
        return response.content[0].text
    else:
        return f"Captura guardada en {path}. Análisis visual requiere Claude."


register(
    name="analyze_screen",
    description="Captura la pantalla y la analiza para responder una pregunta sobre lo que ve.",
    parameters={"question": {"type": "string", "description": "¿Qué quieres saber de la pantalla?", "required": True}},
    executor=analyze_screen,
    category="vision",
    timeout=20,
)
