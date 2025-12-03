# routines/routine_db.py
import json
import os

# Use file next to this module for reliability
MODULE_DIR = os.path.dirname(__file__)
DATA_DIR = os.path.join(MODULE_DIR, "data")
DB_PATH = os.path.join(DATA_DIR, "routines.json")

# Ensure data dir exists
os.makedirs(DATA_DIR, exist_ok=True)

def load_routines():
    if not os.path.exists(DB_PATH):
        return []
    with open(DB_PATH, "r") as f:
        try:
            return json.load(f)
        except Exception:
            return []

def save_routines(routines):
    with open(DB_PATH, "w") as f:
        json.dump(routines, f, indent=4)

def add_routine(routine: dict):
    routines = load_routines()
    routines.append(routine)
    save_routines(routines)
    # Return the new length/index for convenience
    return len(routines) - 1

def delete_routine(index: int):
    routines = load_routines()
    if 0 <= index < len(routines):
        routines.pop(index)
        save_routines(routines)
        return True
    return False