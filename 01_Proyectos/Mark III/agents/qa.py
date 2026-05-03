"""
QA Agent: verifica que el resultado realmente cumple el objetivo.
Antes de responder "listo", confirma que pasó algo real.
"""
from core.providers import get_provider


async def verify(goal: str, result: str) -> str:
    provider = get_provider()

    prompt = f"""
You are the QA agent for MARK III.
Goal: "{goal}"
Result: "{result[:1000]}"

Answer in one sentence: Did the result actually accomplish the goal?
If YES: "✓ " + brief confirmation
If NO: "✗ " + what's missing or what to retry
"""
    response = await provider.chat([{"role": "user", "content": prompt}])
    return response["text"].strip()


def quick_check(result: any) -> bool:
    """Fast sanity check without AI."""
    if result is None:
        return False
    text = str(result).lower()
    failure_phrases = ["error:", "no se pudo", "failed", "exception", "timeout", "not found"]
    return not any(p in text for p in failure_phrases)
