# routine_db.py

import json
import os

DB_PATH = "routines.json"

def load_routines():
    if not os.path.exists(DB_PATH):
        return []
    with open(DB_PATH, "r") as f:
        return json.load(f)

def save_routines(routines):
    with open(DB_PATH, "w") as f:
        json.dump(routines, f, indent=4)

def add_routine(routine: dict):
    routines = load_routines()
    routines.append(routine)
    save_routines(routines)

def delete_routine(index: int):
    routines = load_routines()
    if 0 <= index < len(routines):
        routines.pop(index)
        save_routines(routines)