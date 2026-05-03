"""
Integración con VSCode: abrir archivos, ejecutar comandos, abrir terminal.
También interactúa con Antigravity (Claude Code) via CLI.
"""
import subprocess
import os
from tools.registry import register


def vscode_open(path: str) -> str:
    try:
        subprocess.Popen(["code", path], shell=True)
        return f"VSCode abriendo: {path}"
    except Exception as e:
        return f"Error abriendo VSCode: {e}"


def vscode_open_folder(folder: str) -> str:
    if not os.path.isabs(folder):
        folder = os.path.expanduser(f"~/{folder}")
    try:
        subprocess.Popen(["code", folder], shell=True)
        return f"VSCode abriendo carpeta: {folder}"
    except Exception as e:
        return f"Error: {e}"


def vscode_new_terminal() -> str:
    import pyautogui
    pyautogui.hotkey("ctrl", "shift", "`")
    return "Nueva terminal abierta en VSCode"


def vscode_run_command(command: str) -> str:
    """Ejecuta un comando en la terminal integrada de VSCode."""
    import pyautogui
    import time
    pyautogui.hotkey("ctrl", "shift", "`")
    time.sleep(0.5)
    pyautogui.write(command, interval=0.03)
    pyautogui.press("enter")
    return f"Comando ejecutado en VSCode: {command}"


def run_in_terminal(command: str, cwd: str = "") -> str:
    """Ejecuta un comando shell y devuelve el output."""
    try:
        result = subprocess.run(
            command,
            shell=True,
            capture_output=True,
            text=True,
            cwd=cwd or None,
            timeout=30,
        )
        output = (result.stdout + result.stderr).strip()
        return output[:2000] if output else "Comando ejecutado sin output."
    except subprocess.TimeoutExpired:
        return "Timeout: el comando tardó más de 30 segundos."
    except Exception as e:
        return f"Error ejecutando comando: {e}"


def antigravity_ask(question: str, context_path: str = "") -> str:
    """Lanza Claude Code (Antigravity) para responder una pregunta sobre código."""
    cmd = f'claude -p "{question}"'
    if context_path:
        cmd = f'cd "{context_path}" && {cmd}'
    return run_in_terminal(cmd)


register(
    name="vscode_open",
    description="Abre un archivo o carpeta en VSCode.",
    parameters={"path": {"type": "string", "description": "Ruta del archivo o carpeta", "required": True}},
    executor=vscode_open,
    category="development",
)

register(
    name="run_command",
    description="Ejecuta un comando en la terminal y devuelve el resultado.",
    parameters={
        "command": {"type": "string", "description": "Comando a ejecutar", "required": True},
        "cwd": {"type": "string", "description": "Directorio de trabajo (opcional)"},
    },
    executor=run_in_terminal,
    category="development",
    risk="moderate",
    requires_confirm=True,
    timeout=35,
)

register(
    name="antigravity_ask",
    description="Consulta a Antigravity (Claude Code CLI) sobre código o el Vault.",
    parameters={
        "question": {"type": "string", "description": "Pregunta o tarea", "required": True},
        "context_path": {"type": "string", "description": "Ruta del proyecto (opcional)"},
    },
    executor=antigravity_ask,
    category="development",
    timeout=60,
)
