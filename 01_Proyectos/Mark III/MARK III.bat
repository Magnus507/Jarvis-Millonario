@echo off
title MARK III - Personal AI OS
color 0B
cd /d "%~dp0"

echo.
echo  ============================================================
echo    M A R K  III  -  Personal AI Operating System v3.0
echo  ============================================================
echo.

:: Si no existe el venv, crearlo
if not exist ".venv\Scripts\python.exe" (
    echo  Creando entorno virtual...
    python -m venv .venv
    if errorlevel 1 (
        echo  ERROR: No se pudo crear el entorno virtual.
        echo  Asegurate de tener Python 3.11 instalado.
        pause
        exit /b 1
    )
    echo  Entorno virtual creado.
    echo.
)

:: Siempre instalar/verificar dependencias
echo  Instalando dependencias...
".venv\Scripts\python.exe" -m pip install --upgrade pip --quiet
".venv\Scripts\python.exe" -m pip install -r requirements.txt --quiet
if errorlevel 1 (
    echo  ERROR: Fallo la instalacion de dependencias.
    pause
    exit /b 1
)
echo  Dependencias OK.

:: Instalar Playwright si no esta instalado
echo  Verificando Playwright...
".venv\Scripts\python.exe" -m playwright install chromium --quiet 2>nul
echo  Playwright OK.

echo.
echo  Iniciando MARK III...
echo  Navegador: http://localhost:8765
echo  Para apagar: Ctrl+C
echo  ------------------------------------------------------------
echo.

".venv\Scripts\python.exe" main.py

echo.
echo  MARK III detenido.
pause
