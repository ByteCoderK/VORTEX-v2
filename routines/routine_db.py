# routines/routine_db.py
import json
import os
import logging

logger = logging.getLogger("routine_db")

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
            data = json.load(f)
            return data if isinstance(data, list) else []
        except Exception:
            logger.exception("Failed to load routines.json; returning empty list")
            return []

def save_routines(routines):
    with open(DB_PATH, "w") as f:
        json.dump(routines, f, indent=4)

def add_routine(routine: dict):
    """
    Append a routine and attempt to notify the running engine to reload.
    Returns the index of the added routine.
    """
    routines = load_routines()
    routines.append(routine)
    save_routines(routines)

    # Try to call reload_routines in routine_engine (lazy import to avoid circular imports)
    try:
        from routines.routine_engine import reload_routines
        try:
            reload_routines()
        except Exception:
            logger.exception("reload_routines() raised; routine saved but reload failed")
    except Exception:
        # It's ok if the engine isn't running/importable (e.g., unit tests)
        logger.debug("routine_engine.reload_routines not available at this moment")

    return len(routines) - 1

def delete_routine(index: int):
    routines = load_routines()
    if 0 <= index < len(routines):
        routines.pop(index)
        save_routines(routines)
        return True
    return False