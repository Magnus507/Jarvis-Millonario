import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

BASE_DIR = Path(__file__).parent.parent

class Settings:
    AI_PROVIDER: str = os.getenv("AI_PROVIDER", "claude")

    ANTHROPIC_API_KEY: str = os.getenv("ANTHROPIC_API_KEY", "")
    CLAUDE_MODEL: str = os.getenv("CLAUDE_MODEL", "claude-sonnet-4-6")

    GEMINI_API_KEY: str = os.getenv("GEMINI_API_KEY", "")
    GEMINI_MODEL: str = os.getenv("GEMINI_MODEL", "gemini-2.0-flash-exp")

    OLLAMA_BASE_URL: str = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
    OLLAMA_MODEL: str = os.getenv("OLLAMA_MODEL", "llama3.2")

    WAKE_WORDS: list[str] = [w.strip().lower() for w in os.getenv("WAKE_WORDS", "hola mark,mark tres,mark 3").split(",")]
    TTS_VOICE: str = os.getenv("TTS_VOICE", "es-PA-RobertoNeural")
    WHISPER_MODEL: str = os.getenv("WHISPER_MODEL", "base")
    VOICE_ENABLED: bool = os.getenv("VOICE_ENABLED", "true").lower() == "true"

    HOST: str = os.getenv("HOST", "localhost")
    PORT: int = int(os.getenv("PORT", "8765"))
    AUTO_OPEN_BROWSER: bool = os.getenv("AUTO_OPEN_BROWSER", "true").lower() == "true"

    MARK_NAME: str = os.getenv("MARK_NAME", "Mark")
    LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO")
    SAFE_MODE: bool = os.getenv("SAFE_MODE", "true").lower() == "true"

    SYSTEM_PROMPT: str = (BASE_DIR / "prompt.txt").read_text(encoding="utf-8")
    DB_PATH: str = str(BASE_DIR / "data" / "mark3.db")
    ACTIONS_DIR: str = str(BASE_DIR / "actions")

settings = Settings()
