"""
Operaciones de archivos: leer, escribir, mover, copiar, listar, buscar.
"""
import os
import shutil
from pathlib import Path
from tools.registry import register


def read_file(path: str) -> str:
    try:
        path = os.path.expandvars(os.path.expanduser(path))
        content = Path(path).read_text(encoding="utf-8", errors="replace")
        return content[:3000]
    except Exception as e:
        return f"Error leyendo archivo: {e}"


def write_file(path: str, content: str, append: bool = False) -> str:
    try:
        path = os.path.expandvars(os.path.expanduser(path))
        p = Path(path)
        p.parent.mkdir(parents=True, exist_ok=True)
        mode = "a" if append else "w"
        with open(p, mode, encoding="utf-8") as f:
            f.write(content)
        return f"Archivo {'actualizado' if append else 'creado'}: {path}"
    except Exception as e:
        return f"Error escribiendo archivo: {e}"


def list_files(folder: str, pattern: str = "*") -> str:
    try:
        folder = os.path.expandvars(os.path.expanduser(folder))
        p = Path(folder)
        files = sorted(p.glob(pattern))[:30]
        return "\n".join(str(f.name) for f in files) or "Carpeta vacía"
    except Exception as e:
        return f"Error listando: {e}"


def delete_file(path: str) -> str:
    try:
        path = os.path.expandvars(os.path.expanduser(path))
        p = Path(path)
        if p.is_dir():
            shutil.rmtree(p)
        else:
            p.unlink()
        return f"Eliminado: {path}"
    except Exception as e:
        return f"Error eliminando: {e}"


def copy_file(source: str, destination: str) -> str:
    try:
        source = os.path.expandvars(os.path.expanduser(source))
        destination = os.path.expandvars(os.path.expanduser(destination))
        shutil.copy2(source, destination)
        return f"Copiado: {source} → {destination}"
    except Exception as e:
        return f"Error copiando: {e}"


def search_files(folder: str, query: str) -> str:
    try:
        folder = os.path.expandvars(os.path.expanduser(folder))
        results = []
        for root, _, files in os.walk(folder):
            for f in files:
                if query.lower() in f.lower():
                    results.append(os.path.join(root, f))
            if len(results) >= 20:
                break
        return "\n".join(results) if results else f"No se encontraron archivos con '{query}'"
    except Exception as e:
        return f"Error buscando: {e}"


register(
    name="read_file",
    description="Lee el contenido de un archivo.",
    parameters={"path": {"type": "string", "description": "Ruta del archivo", "required": True}},
    executor=read_file,
    category="files",
)

register(
    name="write_file",
    description="Crea o escribe en un archivo.",
    parameters={
        "path": {"type": "string", "description": "Ruta del archivo", "required": True},
        "content": {"type": "string", "description": "Contenido a escribir", "required": True},
        "append": {"type": "boolean", "description": "Agregar al final (default false)"},
    },
    executor=write_file,
    category="files",
    risk="moderate",
)

register(
    name="list_files",
    description="Lista archivos en una carpeta.",
    parameters={
        "folder": {"type": "string", "description": "Ruta de la carpeta", "required": True},
        "pattern": {"type": "string", "description": "Patrón glob (default: *)"},
    },
    executor=list_files,
    category="files",
)

register(
    name="delete_file",
    description="Elimina un archivo o carpeta.",
    parameters={"path": {"type": "string", "description": "Ruta a eliminar", "required": True}},
    executor=delete_file,
    category="files",
    risk="dangerous",
    requires_confirm=True,
)

register(
    name="search_files",
    description="Busca archivos por nombre en una carpeta.",
    parameters={
        "folder": {"type": "string", "description": "Carpeta donde buscar", "required": True},
        "query": {"type": "string", "description": "Texto a buscar en el nombre", "required": True},
    },
    executor=search_files,
    category="files",
)
