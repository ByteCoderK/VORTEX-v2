import os
import sqlite3
from threading import Lock

DATA_DIR = os.path.join(os.path.dirname(__file__), "data")
os.makedirs(DATA_DIR, exist_ok=True)
DB_PATH = os.path.join(DATA_DIR, "routines.db")
lock = Lock()


def init_db():
    """Create the DB and table if not exists."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS routines (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            time TEXT NOT NULL,
            frequency TEXT NOT NULL,
            device TEXT NOT NULL,
            relay INTEGER NOT NULL,
            state TEXT NOT NULL
        )
    """)
    conn.commit()
    conn.close()


def load_routines():
    """Load all routines from the DB."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM routines")
    rows = cursor.fetchall()
    conn.close()

    routines = []
    for r in rows:
        routines.append({
            "id": r[0],
            "trigger": {
                "type": "time",
                "value": r[1],
                "frequency": r[2]
            },
            "action": {
                "type": "device",
                "device": r[3],
                "relay": r[4],
                "state": r[5]
            }
        })

    return routines


def add_routine(time, frequency, device, relay, state):
    """Add a new routine into DB."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO routines (time, frequency, device, relay, state) VALUES (?, ?, ?, ?, ?)",
        (time, frequency, device, relay, state)
    )
    conn.commit()
    conn.close()