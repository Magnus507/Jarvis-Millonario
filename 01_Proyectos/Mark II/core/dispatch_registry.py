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
        CREATE TABLE IF NOT EXISTS dispatches (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            goal TEXT NOT NULL,
            status TEXT NOT NULL DEFAULT 'pending',
            summary TEXT NOT NULL DEFAULT '',
            result TEXT NOT NULL DEFAULT '',
            created_at REAL NOT NULL,
            updated_at REAL NOT NULL,
            completed_at REAL
        );
        CREATE INDEX IF NOT EXISTS idx_dispatches_status ON dispatches(status);
        CREATE INDEX IF NOT EXISTS idx_dispatches_updated ON dispatches(updated_at DESC);
        """
    )
    conn.close()


class DispatchRegistry:
    """SQLite registry for long-running plans and builds."""

    def __init__(self) -> None:
        init_db()

    def register(self, name: str, goal: str) -> int:
        now = time.time()
        conn = _connect()
        cur = conn.execute(
            "INSERT INTO dispatches (name, goal, status, created_at, updated_at) VALUES (?, ?, 'pending', ?, ?)",
            (name or "task", goal, now, now),
        )
        row_id = int(cur.lastrowid)
        conn.commit()
        conn.close()
        return row_id

    def update(self, dispatch_id: int, status: str, summary: str = "", result: str = "") -> None:
        now = time.time()
        completed_at = now if status in {"completed", "failed", "cancelled", "timeout"} else None
        conn = _connect()
        conn.execute(
            "UPDATE dispatches SET status = ?, summary = ?, result = ?, updated_at = ?, completed_at = COALESCE(?, completed_at) WHERE id = ?",
            (status, summary[:1000], result[:5000], now, completed_at, dispatch_id),
        )
        conn.commit()
        conn.close()

    def recent(self, limit: int = 10) -> list[dict[str, Any]]:
        conn = _connect()
        rows = conn.execute("SELECT * FROM dispatches ORDER BY updated_at DESC LIMIT ?", (limit,)).fetchall()
        conn.close()
        return [dict(row) for row in rows]

    def active(self) -> list[dict[str, Any]]:
        conn = _connect()
        rows = conn.execute(
            "SELECT * FROM dispatches WHERE status IN ('pending','planning','running') ORDER BY updated_at DESC"
        ).fetchall()
        conn.close()
        return [dict(row) for row in rows]

    def format_for_prompt(self) -> str:
        active = self.active()
        if active:
            return "ACTIVE DISPATCHES:\n" + "\n".join(
                f"- [{item['status']}] {item['name']}: {item['goal'][:120]}" for item in active[:5]
            )
        recent = [item for item in self.recent(3) if item["status"] == "completed"]
        if recent:
            return "RECENT DISPATCHES:\n" + "\n".join(
                f"- {item['name']}: {item['summary'] or item['goal'][:120]}" for item in recent
            )
        return "No active dispatches."
