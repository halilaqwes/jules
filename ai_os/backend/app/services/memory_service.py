import sqlite3
import sqlite_vec
import json
from typing import List, Dict, Any, Optional
import os

DB_PATH = "memory.db"

class MemoryService:
    def __init__(self, db_path: str = DB_PATH):
        self.db_path = db_path
        self._init_db()

    def _get_conn(self):
        conn = sqlite3.connect(self.db_path)
        # Attempt to load sqlite-vec if supported by the Python sqlite3 build
        try:
            conn.enable_load_extension(True)
            sqlite_vec.load(conn)
            conn.enable_load_extension(False)
        except AttributeError:
            pass # fallback to plain sqlite3 if extensions aren't supported
        conn.row_factory = sqlite3.Row
        return conn

    def _init_db(self):
        conn = self._get_conn()
        cursor = conn.cursor()

        # Regular structured memory (e.g. settings, goals, facts)
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS system_memory (
                key TEXT PRIMARY KEY,
                value TEXT NOT NULL,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')

        # Event memory (conversation history, tool runs, logs)
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS event_log (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                agent_id TEXT,
                event_type TEXT,
                content TEXT,
                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')

        # We can add a vector table here if we want to do semantic search over memory using sqlite-vec
        # For simplicity in this demo, we'll store memory as text.

        conn.commit()
        conn.close()

    def set_memory(self, key: str, value: Any):
        conn = self._get_conn()
        cursor = conn.cursor()
        val_str = json.dumps(value) if isinstance(value, (dict, list)) else str(value)
        cursor.execute('''
            INSERT INTO system_memory (key, value, updated_at)
            VALUES (?, ?, CURRENT_TIMESTAMP)
            ON CONFLICT(key) DO UPDATE SET value=excluded.value, updated_at=CURRENT_TIMESTAMP
        ''', (key, val_str))
        conn.commit()
        conn.close()

    def get_memory(self, key: str) -> Optional[str]:
        conn = self._get_conn()
        cursor = conn.cursor()
        cursor.execute('SELECT value FROM system_memory WHERE key = ?', (key,))
        row = cursor.fetchone()
        conn.close()
        if row:
            try:
                return json.loads(row['value'])
            except json.JSONDecodeError:
                return row['value']
        return None

    def log_event(self, agent_id: str, event_type: str, content: str):
        conn = self._get_conn()
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO event_log (agent_id, event_type, content)
            VALUES (?, ?, ?)
        ''', (agent_id, event_type, content))
        conn.commit()
        conn.close()

        # Trigger real-time hook if available
        if hasattr(self, 'log_event_hook') and self.log_event_hook:
            self.log_event_hook(agent_id, event_type, content)

    def get_recent_events(self, agent_id: str, limit: int = 50) -> List[Dict[str, Any]]:
        conn = self._get_conn()
        cursor = conn.cursor()
        cursor.execute('''
            SELECT id, agent_id, event_type, content, timestamp
            FROM event_log
            WHERE agent_id = ?
            ORDER BY id DESC LIMIT ?
        ''', (agent_id, limit))
        rows = cursor.fetchall()
        conn.close()
        return [dict(row) for row in rows][::-1]

memory_service = MemoryService()
