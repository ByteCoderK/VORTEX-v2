# routines/routine_db.py
import os
import sqlite3
import json
from threading import Lock

MODULE_DIR = os.path.dirname(__file__)
DATA_DIR = os.path.join(MODULE_DIR, "data")
os.makedirs(DATA_DIR, exist_ok=True)
DB_PATH = os.path.join(DATA_DIR, "routines.db")

lock = Lock()

def init_db():
    """Ensure DB and table exist."""
    with lock:
        conn = sqlite3.connect(DB_PATH)
        cur = conn.cursor()
        cur.execute("""
            CREATE TABLE IF NOT EXISTS routines (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                time TEXT,         -- stored HH:MM (IST)
                frequency TEXT,    -- daily/monday/.../once
                device TEXT,
                relay INTEGER,
                state TEXT,
                raw_json TEXT       -- original routine dict (optional)
            )
        """)
        conn.commit()
        conn.close()

def add_routine(routine: dict) -> int:
    """
    Accepts the routine dict returned by routine_parser.parse_routine(...)
    Saves into sqlite and returns the new row id (index).
    """
    init_db()
    with lock:
        conn = sqlite3.connect(DB_PATH)
        cur = conn.cursor()
        trigger = routine.get("trigger", {})
        action = routine.get("action", {})
        t = trigger.get("value")
        freq = trigger.get("frequency") or "once"
        device = action.get("device") or ""
        relay = action.get("relay") if action.get("relay") is not None else -1
        state = action.get("state") or ""
        raw = json.dumps(routine)
        cur.execute(
            "INSERT INTO routines (time, frequency, device, relay, state, raw_json) VALUES (?, ?, ?, ?, ?, ?)",
            (t, freq, device, relay, state, raw)
        )
        rowid = cur.lastrowid
        conn.commit()
        conn.close()
        return rowid

def load_routines() -> list:
    """
    Returns a list of routines (same format as parse_routine -> dict)
    """
    init_db()
    with lock:
        conn = sqlite3.connect(DB_PATH)
        cur = conn.cursor()
        cur.execute("SELECT id, time, frequency, device, relay, state, raw_json FROM routines")
        rows = cur.fetchall()
        conn.close()

    routines = []
    for r in rows:
        # if raw_json exists and valid use it (keeps original structure)
        try:
            parsed = json.loads(r[6]) if r[6] else None
        except Exception:
            parsed = None

        if parsed:
            routines.append(parsed)
        else:
            routines.append({
                "id": r[0],
                "trigger": {"type": "time", "value": r[1], "frequency": r[2]},
                "action": {"type": "device", "device": r[3], "relay": r[4], "state": r[5]}
            })
    return routines

def delete_routine(index: int) -> bool:
    init_db()
    with lock:
        conn = sqlite3.connect(DB_PATH)
        cur = conn.cursor()
        cur.execute("DELETE FROM routines WHERE id = ?", (index,))
        changed = cur.rowcount
        conn.commit()
        conn.close()
        return changed > 0

def save_routines_as_json(path):
    """Utility: dump DB to a JSON file (for debugging)."""
    r = load_routines()
    with open(path, "w") as f:
        json.dump(r, f, indent=4)