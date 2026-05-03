from __future__ import annotations

import json
import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
ENV_PATH = BASE_DIR / ".env"
API_KEYS_PATH = BASE_DIR / "config" / "api_keys.json"

_ENV_LOADED = False


def _load_env_file() -> None:
    global _ENV_LOADED
    if _ENV_LOADED:
        return
    _ENV_LOADED = True
    if not ENV_PATH.exists():
        return
    for raw_line in ENV_PATH.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        key = key.strip()
        value = value.strip().strip('"').strip("'")
        os.environ.setdefault(key, value)


def _load_json() -> dict:
    if not API_KEYS_PATH.exists():
        return {}
    try:
        return json.loads(API_KEYS_PATH.read_text(encoding="utf-8-sig"))
    except Exception:
        return {}


def get_secret(env_name: str, json_name: str | None = None, default: str = "") -> str:
    _load_env_file()
    value = os.getenv(env_name, "").strip()
    if value:
        return value
    data = _load_json()
    return str(data.get(json_name or env_name.lower(), default) or "").strip()


def get_gemini_api_key() -> str:
    return get_secret("GEMINI_API_KEY", "gemini_api_key")


def get_openrouter_api_key() -> str:
    return get_secret("OPENROUTER_API_KEY", "openrouter_api_key")


def load_public_settings() -> dict:
    data = _load_json()
    return {k: v for k, v in data.items() if "key" not in k.lower() and "token" not in k.lower()}
