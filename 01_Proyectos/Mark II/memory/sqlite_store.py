from __future__ import annotations

import sqlite3
import time
from pathlib import Path
from typing import Any

BASE_DIR = Path(__file__).resolve().parent.parent
DB_PATH = BASE_DIR / "memory" / "mark_ii.sqlite3"


def _connect() -> sqlite3.Connection:
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(str(DB_PATH))
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA journal_mode=WAL")
    return conn


def init_db() -> None:
    conn = _connect()
    conn.executescript(
        """
        CREATE TABLE IF NOT EXISTS memories (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            category TEXT NOT NULL DEFAULT 'notes',
            key TEXT NOT NULL DEFAULT '',
            value TEXT NOT NULL,
            source TEXT NOT NULL DEFAULT '',
            importance INTEGER NOT NULL DEFAULT 5,
            created_at REAL NOT NULL,
            updated_at REAL NOT NULL,
            access_count INTEGER NOT NULL DEFAULT 0
        );

        CREATE VIRTUAL TABLE IF NOT EXISTS memory_fts USING fts5(
            category, key, value, source,
            content='memories', content_rowid='id'
        );

        CREATE TABLE IF NOT EXISTS tool_runs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            tool_name TEXT NOT NULL,
            success INTEGER NOT NULL,
            duration_s REAL NOT NULL DEFAULT 0,
            error TEXT NOT NULL DEFAULT '',
            created_at REAL NOT NULL
        );
        CREATE INDEX IF NOT EXISTS idx_tool_runs_name ON tool_runs(tool_name);
        CREATE INDEX IF NOT EXISTS idx_tool_runs_created ON tool_runs(created_at DESC);
        """
    )
    conn.close()


def remember(category: str, key: str, value: str, source: str = "", importance: int = 5) -> int:
    init_db()
    now = time.time()
    conn = _connect()
    cur = conn.execute(
        "INSERT INTO memories (category, key, value, source, importance, created_at, updated_at) VALUES (?, ?, ?, ?, ?, ?, ?)",
        (category or "notes", key or "", value, source or "", int(importance), now, now),
    )
    row_id = int(cur.lastrowid)
    conn.execute(
        "INSERT INTO memory_fts (rowid, category, key, value, source) VALUES (?, ?, ?, ?, ?)",
        (row_id, category or "notes", key or "", value, source or ""),
    )
    conn.commit()
    conn.close()
    return row_id


def _fts_query(query: str) -> str:
    words = [w.strip('"\'*-:()[]{}') for w in (query or "").split()]
    words = [w for w in words if len(w) > 2]
    return " OR ".join(words[:8])


def recall(query: str, limit: int = 5) -> list[dict[str, Any]]:
    init_db()
    fts = _fts_query(query)
    if not fts:
        return []
    conn = _connect()
    try:
        rows = conn.execute(
            """
            SELECT m.*
            FROM memory_fts f
            JOIN memories m ON m.id = f.rowid
            WHERE memory_fts MATCH ?
            ORDER BY rank
            LIMIT ?
            """,
            (fts, limit),
        ).fetchall()
    except sqlite3.Error:
        rows = []
    for row in rows:
        conn.execute("UPDATE memories SET access_count = access_count + 1 WHERE id = ?", (row["id"],))
    conn.commit()
    conn.close()
    return [dict(row) for row in rows]


def record_tool_run(tool_name: str, success: bool, duration_s: float = 0, error: str = "") -> None:
    init_db()
    conn = _connect()
    conn.execute(
        "INSERT INTO tool_runs (tool_name, success, duration_s, error, created_at) VALUES (?, ?, ?, ?, ?)",
        (tool_name, 1 if success else 0, float(duration_s or 0), (error or "")[:1000], time.time()),
    )
    conn.commit()
    conn.close()


def tool_stats(limit: int = 50) -> list[dict[str, Any]]:
    init_db()
    conn = _connect()
    rows = conn.execute(
        """
        SELECT tool_name,
               COUNT(*) AS calls,
               SUM(success) AS successes,
               AVG(duration_s) AS avg_duration_s,
               MAX(created_at) AS last_called_at
        FROM tool_runs
        GROUP BY tool_name
        ORDER BY calls DESC, last_called_at DESC
        LIMIT ?
        """,
        (limit,),
    ).fetchall()
    conn.close()
    data = []
    for row in rows:
        item = dict(row)
        item["success_rate"] = (item["successes"] / item["calls"]) if item["calls"] else 0
        data.append(item)
    return data


def memory_count() -> int:
    init_db()
    conn = _connect()
    count = conn.execute("SELECT COUNT(*) FROM memories").fetchone()[0]
    conn.close()
    return int(count)
