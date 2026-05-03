import sqlite3
import json
from pathlib import Path
from config.settings import settings


def _conn() -> sqlite3.Connection:
    Path(settings.DB_PATH).parent.mkdir(parents=True, exist_ok=True)
    con = sqlite3.connect(settings.DB_PATH)
    con.row_factory = sqlite3.Row
    return con


def init_db():
    con = _conn()
    con.executescript("""
        CREATE TABLE IF NOT EXISTS memories (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            category TEXT NOT NULL,
            key TEXT NOT NULL,
            value TEXT NOT NULL,
            created_at TEXT DEFAULT (datetime('now')),
            updated_at TEXT DEFAULT (datetime('now')),
            UNIQUE(category, key)
        );

        CREATE VIRTUAL TABLE IF NOT EXISTS memories_fts
            USING fts5(category, key, value, content='memories', content_rowid='id');

        CREATE TRIGGER IF NOT EXISTS memories_ai AFTER INSERT ON memories BEGIN
            INSERT INTO memories_fts(rowid, category, key, value)
            VALUES (new.id, new.category, new.key, new.value);
        END;

        CREATE TRIGGER IF NOT EXISTS memories_au AFTER UPDATE ON memories BEGIN
            INSERT INTO memories_fts(memories_fts, rowid, category, key, value)
            VALUES ('delete', old.id, old.category, old.key, old.value);
            INSERT INTO memories_fts(rowid, category, key, value)
            VALUES (new.id, new.category, new.key, new.value);
        END;

        CREATE TABLE IF NOT EXISTS conversations (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            session_id TEXT,
            role TEXT,
            content TEXT,
            created_at TEXT DEFAULT (datetime('now'))
        );

        CREATE TABLE IF NOT EXISTS tool_runs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            tool TEXT,
            params TEXT,
            result TEXT,
            success INTEGER,
            created_at TEXT DEFAULT (datetime('now'))
        );

        CREATE TABLE IF NOT EXISTS learned_procedures (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT UNIQUE,
            description TEXT,
            steps TEXT,
            created_at TEXT DEFAULT (datetime('now'))
        );
    """)
    con.commit()
    con.close()


def upsert_memory(category: str, key: str, value: str):
    con = _conn()
    con.execute("""
        INSERT INTO memories (category, key, value, updated_at)
        VALUES (?, ?, ?, datetime('now'))
        ON CONFLICT(category, key) DO UPDATE SET
            value = excluded.value,
            updated_at = datetime('now')
    """, (category, key, value))
    con.commit()
    con.close()


def get_memory(category: str | None = None) -> list[dict]:
    con = _conn()
    if category:
        rows = con.execute(
            "SELECT category, key, value, updated_at FROM memories WHERE category=? ORDER BY updated_at DESC",
            (category,)
        ).fetchall()
    else:
        rows = con.execute(
            "SELECT category, key, value, updated_at FROM memories ORDER BY updated_at DESC LIMIT 100"
        ).fetchall()
    con.close()
    return [dict(r) for r in rows]


def search_memory(query: str) -> list[dict]:
    con = _conn()
    rows = con.execute("""
        SELECT m.category, m.key, m.value FROM memories m
        JOIN memories_fts f ON m.id = f.rowid
        WHERE memories_fts MATCH ? LIMIT 10
    """, (query,)).fetchall()
    con.close()
    return [dict(r) for r in rows]


def log_tool_run(tool: str, params: dict, result: any, success: bool):
    con = _conn()
    con.execute(
        "INSERT INTO tool_runs (tool, params, result, success) VALUES (?, ?, ?, ?)",
        (tool, json.dumps(params), str(result), int(success))
    )
    con.commit()
    con.close()


def save_procedure(name: str, description: str, steps: list[dict]):
    con = _conn()
    con.execute("""
        INSERT INTO learned_procedures (name, description, steps)
        VALUES (?, ?, ?)
        ON CONFLICT(name) DO UPDATE SET description=excluded.description, steps=excluded.steps
    """, (name, description, json.dumps(steps)))
    con.commit()
    con.close()
