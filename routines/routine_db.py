#routine_db.py
import os
import json
from threading import Lock
import sqlite3

DATA_DIR = os.path.join(os.path.dirname(__file__), "data")
os.makedirs(DATA_DIR, exist_ok=True)
DB_PATH = os.path.join(DATA_DIR, "routines.json")
lock = Lock()

def load_routines():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM routines")
    rows = cursor.fetchall()
    conn.close()

    # convert to your existing routine format
    routines = []
    for r in rows:
        routines.append({
            "trigger": {"type": "time", "value": r[1], "frequency": r[2]},
            "action": {"type": "device", "relay": r[4], "state": r[5]}
        })
    return routines

def save_routines(routines):
    with lock:
        with open(DB_PATH, "w") as f:
            json.dump(routines, f, indent=4)

def add_routine(time, frequency, device, relay, state):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO routines (time, frequency, device, relay, state) VALUES (?, ?, ?, ?, ?)",
        (time, frequency, device, relay, state)
    )
    conn.commit()
    conn.close()