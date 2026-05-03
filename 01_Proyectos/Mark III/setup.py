"""
MARK III — Setup Script
Instala dependencias y configura el entorno.
"""
import subprocess
import sys
import shutil
from pathlib import Path


def run(cmd: list, check=True):
    print(f"  > {' '.join(cmd)}")
    subprocess.run(cmd, check=check)


def main():
    print("\n╔══════════════════════════════════╗")
    print("║    MARK III — Setup Wizard       ║")
    print("╚══════════════════════════════════╝\n")

    # 1. Create venv
    venv_path = Path(".venv")
    if not venv_path.exists():
        print("[1/5] Creando entorno virtual...")
        run([sys.executable, "-m", "venv", ".venv"])
    else:
        print("[1/5] Entorno virtual ya existe.")

    python = str(venv_path / "Scripts" / "python.exe") if sys.platform == "win32" else str(venv_path / "bin" / "python")

    # 2. Install requirements
    print("[2/5] Instalando dependencias...")
    run([python, "-m", "pip", "install", "--upgrade", "pip"])
    run([python, "-m", "pip", "install", "-r", "requirements.txt"])

    # 3. Playwright
    print("[3/5] Instalando Playwright (Chromium)...")
    run([python, "-m", "playwright", "install", "chromium"])

    # 4. Create .env if not exists
    print("[4/5] Configurando .env...")
    env_path = Path(".env")
    if not env_path.exists():
        shutil.copy(".env.example", ".env")
        print("  → .env creado desde .env.example")
        print("  ⚠  EDITA .env con tus API keys antes de iniciar.")
    else:
        print("  → .env ya existe.")

    # 5. Create data dir
    print("[5/5] Creando directorio de datos...")
    Path("data").mkdir(exist_ok=True)

    print("\n✅ Setup completo.")
    print("   1. Edita .env con tus API keys")
    print("   2. Ejecuta: .venv\\Scripts\\python.exe main.py")
    print("   3. Abre: http://localhost:8765\n")


if __name__ == "__main__":
    main()
