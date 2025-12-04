#routine_db.py
import os
import json
from threading import Lock

DATA_DIR = os.path.join(os.path.dirname(__file__), "data")
os.makedirs(DATA_DIR, exist_ok=True)
DB_PATH = os.path.join(DATA_DIR, "routines.json")
lock = Lock()

def load_routines():
    with lock:
        if not os.path.exists(DB_PATH):
            return []
        try:
            with open(DB_PATH, "r") as f:
                return json.load(f)
        except Exception:
            return []

def save_routines(routines):
    with lock:
        with open(DB_PATH, "w") as f:
            json.dump(routines, f, indent=4)

def add_routine(routine):
    routines = load_routines()
    routines.append(routine)
    save_routines(routines)