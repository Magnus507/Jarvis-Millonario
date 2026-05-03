from .claude_provider import ClaudeProvider
from .gemini_provider import GeminiProvider
from .local_provider import LocalProvider
from config.settings import settings


def get_provider():
    providers = {
        "claude": ClaudeProvider,
        "gemini": GeminiProvider,
        "local": LocalProvider,
    }
    order = [settings.AI_PROVIDER, "claude", "gemini", "local"]
    for name in order:
        cls = providers.get(name)
        if cls:
            p = cls()
            if p.is_available():
                return p
    raise RuntimeError("No AI provider available. Check your .env file.")
