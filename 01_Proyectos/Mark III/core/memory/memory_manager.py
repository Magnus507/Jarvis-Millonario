"""
Decides what to remember and surfaces relevant context.
Uses a 2-stage gate: filter → extract → store.
"""
import re
from core.memory.sqlite_store import upsert_memory, get_memory, search_memory


MEMORY_TRIGGERS = [
    "me llamo", "mi nombre es", "trabajo en", "vivo en", "prefiero",
    "siempre hago", "nunca hagas", "recuerda que", "mi proyecto",
    "mi email", "mi teléfono", "usa siempre", "no uses",
]


class MemoryManager:
    def get_context(self) -> str:
        memories = get_memory()
        if not memories:
            return ""
        lines = [f"- [{m['category']}] {m['key']}: {m['value']}" for m in memories[:20]]
        return "\n".join(lines)

    def search(self, query: str) -> list[dict]:
        return search_memory(query)

    def save(self, category: str, key: str, value: str):
        upsert_memory(category, key, value)

    async def maybe_save(self, user_input: str, response: str):
        lowered = user_input.lower()
        should_save = any(trigger in lowered for trigger in MEMORY_TRIGGERS)
        if not should_save:
            return

        if "me llamo" in lowered or "mi nombre es" in lowered:
            match = re.search(r"(?:me llamo|mi nombre es)\s+(\w+)", lowered)
            if match:
                upsert_memory("identidad", "nombre_usuario", match.group(1))

        if "prefiero" in lowered:
            upsert_memory("preferencias", f"preferencia_{hash(user_input) % 10000}", user_input)

        if "mi proyecto" in lowered:
            upsert_memory("proyectos", f"nota_{hash(user_input) % 10000}", user_input)

        if "recuerda que" in lowered:
            content = lowered.split("recuerda que", 1)[-1].strip()
            upsert_memory("notas", f"recordatorio_{hash(content) % 10000}", content)
