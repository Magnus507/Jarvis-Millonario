"""
Central brain of MARK III.
Manages conversation history, coordinates router, memory, and voice.
"""
import asyncio
from core import events, router
from core.memory.memory_manager import MemoryManager
from config.settings import settings

memory = MemoryManager()


class Brain:
    def __init__(self):
        self.conversation: list[dict] = []
        self.state = "idle"

    async def process(self, user_input: str, source: str = "text") -> str:
        """Main entry point for any user input (text or voice)."""
        user_input = user_input.strip()
        if not user_input:
            return ""

        await events.publish("message", {"role": "user", "text": user_input})
        await events.publish("state_change", {"state": "thinking"})

        context = memory.get_context()
        if context:
            system_context = f"\n\n## Current Memory Context\n{context}"
            messages = [{"role": "user", "content": f"[CONTEXT]{system_context}[/CONTEXT]\n{user_input}"}]
        else:
            messages = [{"role": "user", "content": user_input}]

        try:
            response = await router.handle(user_input, self.conversation)
        except Exception as e:
            await events.publish("error", {"message": str(e)})
            response = f"Error interno: {e}"

        self.conversation.append({"role": "user", "content": user_input})
        self.conversation.append({"role": "assistant", "content": response})

        if len(self.conversation) > 40:
            self.conversation = self.conversation[-30:]

        await memory.maybe_save(user_input, response)
        await events.publish("message", {"role": "assistant", "text": response})
        await events.publish("state_change", {"state": "idle"})

        return response

    def reset_conversation(self):
        self.conversation = []


brain = Brain()
