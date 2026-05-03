"""
Control total del PC en Windows: volumen, brillo, bloqueo, apagado, etc.
"""
import subprocess
import ctypes
from tools.registry import register


def set_volume(level: int) -> str:
    from ctypes import cast, POINTER
    from comtypes import CLSCTX_ALL
    from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume

    devices = AudioUtilities.GetSpeakers()
    interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
    volume = cast(interface, POINTER(IAudioEndpointVolume))
    scalar = max(0.0, min(1.0, level / 100.0))
    volume.SetMasterVolumeLevelScalar(scalar, None)
    return f"Volumen establecido en {level}%"


def mute_toggle(mute: bool) -> str:
    from ctypes import cast, POINTER
    from comtypes import CLSCTX_ALL
    from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume

    devices = AudioUtilities.GetSpeakers()
    interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
    volume = cast(interface, POINTER(IAudioEndpointVolume))
    volume.SetMute(int(mute), None)
    return "Silenciado" if mute else "Audio activado"


def lock_pc() -> str:
    ctypes.windll.user32.LockWorkStation()
    return "PC bloqueada"


def shutdown_pc(delay_seconds: int = 60) -> str:
    subprocess.Popen(["shutdown", "/s", "/t", str(delay_seconds)])
    return f"Apagado programado en {delay_seconds} segundos"


def cancel_shutdown() -> str:
    subprocess.Popen(["shutdown", "/a"])
    return "Apagado cancelado"


def restart_pc(delay_seconds: int = 60) -> str:
    subprocess.Popen(["shutdown", "/r", "/t", str(delay_seconds)])
    return f"Reinicio programado en {delay_seconds} segundos"


def take_screenshot(filename: str = "") -> str:
    import pyautogui
    import os
    from pathlib import Path

    save_dir = Path.home() / "Pictures" / "Mark3"
    save_dir.mkdir(parents=True, exist_ok=True)

    if not filename:
        from datetime import datetime
        filename = f"screenshot_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"

    path = save_dir / filename
    img = pyautogui.screenshot()
    img.save(str(path))
    return f"Captura guardada en: {path}"


def set_brightness(level: int) -> str:
    try:
        import wmi
        c = wmi.WMI(namespace="wmi")
        methods = c.WmiMonitorBrightnessMethods()[0]
        methods.WmiSetBrightness(level, 0)
        return f"Brillo establecido en {level}%"
    except Exception as e:
        return f"Error ajustando brillo: {e}"


def type_text(text: str) -> str:
    import pyautogui
    pyautogui.write(text, interval=0.03)
    return f"Texto escrito: '{text}'"


def press_key(key: str) -> str:
    import pyautogui
    pyautogui.hotkey(*key.split("+"))
    return f"Tecla presionada: {key}"


def move_mouse(x: int, y: int) -> str:
    import pyautogui
    pyautogui.moveTo(x, y, duration=0.3)
    return f"Mouse movido a ({x}, {y})"


def click_mouse(x: int = -1, y: int = -1, button: str = "left") -> str:
    import pyautogui
    if x >= 0 and y >= 0:
        pyautogui.click(x, y, button=button)
    else:
        pyautogui.click(button=button)
    return f"Click {button} en ({x}, {y})"


register(
    name="set_volume",
    description="Ajusta el volumen del sistema. level: 0-100.",
    parameters={"level": {"type": "integer", "description": "Nivel de volumen 0-100", "required": True}},
    executor=set_volume,
    category="system",
)

register(
    name="mute_toggle",
    description="Silencia o activa el audio del sistema.",
    parameters={"mute": {"type": "boolean", "description": "true para silenciar, false para activar", "required": True}},
    executor=mute_toggle,
    category="system",
)

register(
    name="lock_pc",
    description="Bloquea el PC (requiere contraseña para desbloquear).",
    parameters={},
    executor=lock_pc,
    category="system",
    risk="moderate",
)

register(
    name="shutdown_pc",
    description="Apaga el PC después de un delay.",
    parameters={"delay_seconds": {"type": "integer", "description": "Segundos antes de apagar (default 60)"}},
    executor=shutdown_pc,
    category="system",
    risk="dangerous",
    requires_confirm=True,
)

register(
    name="restart_pc",
    description="Reinicia el PC.",
    parameters={"delay_seconds": {"type": "integer", "description": "Segundos antes de reiniciar (default 60)"}},
    executor=restart_pc,
    category="system",
    risk="dangerous",
    requires_confirm=True,
)

register(
    name="take_screenshot",
    description="Captura una pantalla y la guarda.",
    parameters={"filename": {"type": "string", "description": "Nombre del archivo (opcional)"}},
    executor=take_screenshot,
    category="system",
)

register(
    name="type_text",
    description="Escribe texto usando el teclado (como si el usuario lo escribiera).",
    parameters={"text": {"type": "string", "description": "Texto a escribir", "required": True}},
    executor=type_text,
    category="system",
)

register(
    name="press_key",
    description="Presiona una tecla o combinación (ej: 'ctrl+c', 'alt+tab', 'win+d').",
    parameters={"key": {"type": "string", "description": "Tecla o combinación", "required": True}},
    executor=press_key,
    category="system",
)

register(
    name="set_brightness",
    description="Ajusta el brillo de la pantalla (0-100).",
    parameters={"level": {"type": "integer", "description": "Nivel de brillo 0-100", "required": True}},
    executor=set_brightness,
    category="system",
)
