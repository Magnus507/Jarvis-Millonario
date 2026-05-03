from __future__ import annotations

import json
import sqlite3
import threading
import time
from collections import deque
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any, Callable

BASE_DIR = Path(__file__).resolve().parent.parent.parent
DB_PATH = BASE_DIR / "memory" / "mark_ii.sqlite3"


@dataclass
class Event:
    type: str
    payload: dict[str, Any]
    created_at: float


def _connect() -> sqlite3.Connection:
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(str(DB_PATH))
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA journal_mode=WAL")
    return conn


def _init_db() -> None:
    conn = _connect()
    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS events (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            type TEXT NOT NULL,
            payload TEXT NOT NULL DEFAULT '{}',
            created_at REAL NOT NULL
        )
        """
    )
    conn.execute("CREATE INDEX IF NOT EXISTS idx_events_created ON events(created_at DESC)")
    conn.commit()
    conn.close()


def _store_event(event: Event) -> None:
    try:
        _init_db()
        conn = _connect()
        conn.execute(
            "INSERT INTO events (type, payload, created_at) VALUES (?, ?, ?)",
            (event.type, json.dumps(event.payload, ensure_ascii=False), event.created_at),
        )
        conn.commit()
        # Keep the local event log from growing forever.
        conn.execute(
            "DELETE FROM events WHERE id NOT IN (SELECT id FROM events ORDER BY created_at DESC LIMIT 1000)"
        )
        conn.commit()
        conn.close()
    except Exception:
        pass


class EventBus:
    """Small event bus backed by SQLite so the web orb can run separately."""

    def __init__(self, max_events: int = 500):
        self._events: deque[Event] = deque(maxlen=max_events)
        self._subscribers: list[Callable[[Event], None]] = []
        self._lock = threading.Lock()

    def publish(self, event_type: str, **payload: Any) -> Event:
        event = Event(event_type, payload, time.time())
        with self._lock:
            self._events.append(event)
            subscribers = list(self._subscribers)
        _store_event(event)
        for callback in subscribers:
            try:
                callback(event)
            except Exception:
                pass
        return event

    def subscribe(self, callback: Callable[[Event], None]) -> Callable[[], None]:
        with self._lock:
            self._subscribers.append(callback)

        def unsubscribe() -> None:
            with self._lock:
                if callback in self._subscribers:
                    self._subscribers.remove(callback)

        return unsubscribe

    def recent(self, limit: int = 50) -> list[dict[str, Any]]:
        try:
            _init_db()
            conn = _connect()
            rows = conn.execute(
                "SELECT type, payload, created_at FROM events ORDER BY created_at DESC LIMIT ?",
                (limit,),
            ).fetchall()
            conn.close()
            events = []
            for row in reversed(rows):
                try:
                    payload = json.loads(row["payload"] or "{}")
                except Exception:
                    payload = {}
                events.append({"type": row["type"], "payload": payload, "created_at": row["created_at"]})
            return events
        except Exception:
            with self._lock:
                events = list(self._events)[-limit:]
            return [asdict(event) for event in events]


bus = EventBus()


def publish(event_type: str, **payload: Any) -> Event:
    return bus.publish(event_type, **payload)


def recent(limit: int = 50) -> list[dict[str, Any]]:
    return bus.recent(limit)
