"""
Abre aplicaciones en Windows por nombre o ruta.
"""
import subprocess
import os
from tools.registry import register


APP_ALIASES: dict[str, str] = {
    "chrome": "chrome",
    "google chrome": "chrome",
    "firefox": "firefox",
    "edge": "msedge",
    "notepad": "notepad",
    "bloc de notas": "notepad",
    "calculadora": "calc",
    "calc": "calc",
    "explorador": "explorer",
    "explorer": "explorer",
    "cmd": "cmd",
    "terminal": "wt",
    "powershell": "powershell",
    "vscode": "code",
    "visual studio code": "code",
    "spotify": "spotify",
    "discord": "discord",
    "whatsapp": "whatsapp",
    "teams": "teams",
    "zoom": "zoom",
    "paint": "mspaint",
    "word": "winword",
    "excel": "excel",
    "outlook": "outlook",
    "steam": "steam",
    "obs": "obs64",
    "vlc": "vlc",
}


def open_app(app_name: str) -> str:
    name_lower = app_name.lower().strip()
    resolved = APP_ALIASES.get(name_lower, app_name)

    try:
        if os.path.isabs(resolved) and os.path.exists(resolved):
            subprocess.Popen([resolved])
        else:
            subprocess.Popen(resolved, shell=True)
        return f"Abriendo: {app_name}"
    except Exception as e:
        return f"No se pudo abrir '{app_name}': {e}"


def close_app(app_name: str) -> str:
    try:
        subprocess.run(["taskkill", "/IM", f"{app_name}.exe", "/F"],
                       capture_output=True, text=True)
        return f"Cerrado: {app_name}"
    except Exception as e:
        return f"Error cerrando '{app_name}': {e}"


def list_running_apps() -> str:
    result = subprocess.run(["tasklist", "/FO", "CSV"], capture_output=True, text=True)
    lines = result.stdout.strip().split("\n")[1:16]
    apps = [l.split(",")[0].strip('"') for l in lines if l]
    return "Aplicaciones en ejecución: " + ", ".join(apps)


register(
    name="open_app",
    description="Abre una aplicación en Windows por nombre (chrome, spotify, vscode, etc).",
    parameters={"app_name": {"type": "string", "description": "Nombre de la aplicación", "required": True}},
    executor=open_app,
    category="system",
)

register(
    name="close_app",
    description="Cierra una aplicación por nombre de proceso.",
    parameters={"app_name": {"type": "string", "description": "Nombre del proceso (sin .exe)", "required": True}},
    executor=close_app,
    category="system",
    risk="moderate",
)

register(
    name="list_apps",
    description="Lista las aplicaciones actualmente en ejecución.",
    parameters={},
    executor=list_running_apps,
    category="system",
)
