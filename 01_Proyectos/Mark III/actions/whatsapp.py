"""
Interacción con WhatsApp Web.
"""
import asyncio
from tools.registry import register


async def whatsapp_open() -> str:
    from actions.browser_control import open_url
    await open_url("https://web.whatsapp.com")
    await asyncio.sleep(3)
    return "WhatsApp Web abierto. Si es primera vez, escanea el QR."


async def whatsapp_send(contact: str, message: str) -> str:
    from actions.browser_control import _get_page, open_url
    page = await _get_page()

    current_url = page.url
    if "web.whatsapp.com" not in current_url:
        await open_url("https://web.whatsapp.com")
        await asyncio.sleep(3)

    try:
        search_box = await page.wait_for_selector(
            'div[data-testid="chat-list-search"]', timeout=5000
        )
        await search_box.click()
        await search_box.fill(contact)
        await asyncio.sleep(1.5)

        first_result = await page.wait_for_selector(
            'div[data-testid="cell-frame-container"]', timeout=5000
        )
        await first_result.click()
        await asyncio.sleep(1)

        msg_box = await page.wait_for_selector(
            'div[data-testid="conversation-compose-box-input"]', timeout=5000
        )
        await msg_box.click()
        await msg_box.type(message)
        await page.keyboard.press("Enter")
        return f"Mensaje enviado a {contact}: '{message}'"
    except Exception as e:
        return f"Error enviando WhatsApp: {e}"


async def whatsapp_read_last(contact: str) -> str:
    from actions.browser_control import _get_page
    page = await _get_page()

    try:
        search_box = await page.wait_for_selector(
            'div[data-testid="chat-list-search"]', timeout=5000
        )
        await search_box.click()
        await search_box.fill(contact)
        await asyncio.sleep(1.5)

        first_result = await page.wait_for_selector(
            'div[data-testid="cell-frame-container"]', timeout=5000
        )
        await first_result.click()
        await asyncio.sleep(1)

        messages = await page.query_selector_all('div.message-in span.selectable-text')
        if messages:
            last = await messages[-1].inner_text()
            return f"Último mensaje de {contact}: '{last}'"
        return f"No se encontraron mensajes de {contact}"
    except Exception as e:
        return f"Error leyendo WhatsApp: {e}"


register(
    name="whatsapp_open",
    description="Abre WhatsApp Web en el navegador.",
    parameters={},
    executor=whatsapp_open,
    category="communication",
    timeout=15,
)

register(
    name="whatsapp_send",
    description="Envía un mensaje de WhatsApp a un contacto.",
    parameters={
        "contact": {"type": "string", "description": "Nombre del contacto", "required": True},
        "message": {"type": "string", "description": "Mensaje a enviar", "required": True},
    },
    executor=whatsapp_send,
    category="communication",
    risk="moderate",
    requires_confirm=True,
    timeout=20,
)

register(
    name="whatsapp_read_last",
    description="Lee el último mensaje de un contacto en WhatsApp.",
    parameters={"contact": {"type": "string", "description": "Nombre del contacto", "required": True}},
    executor=whatsapp_read_last,
    category="communication",
    timeout=15,
)
