# routines/routine_engine.py
import schedule
import time
import threading
from routines.routine_db import load_routines
from routines.routine_executor import execute_action

schedule_lock = threading.Lock()

def wrap_execute(action):
    try:
        execute_action(action)
    except Exception as e:
        print(f"[ROUTINE ERROR] {e}")

def register_routine(routine):
    t = routine["trigger"]
    action = routine["action"]
    value = t.get("value")
    freq = t.get("frequency", "once")
    
    if not value:
        print("[WARN] Skipping routine with no time")
        return

    with schedule_lock:
        if freq == "daily":
            schedule.every().day.at(value).do(wrap_execute, action)
        elif freq in ["monday","tuesday","wednesday","thursday","friday","saturday","sunday"]:
            getattr(schedule.every(), freq).at(value).do(wrap_execute, action)
        else:  # once
            schedule.every().day.at(value).do(wrap_execute, action)

def reload_routines():
    with schedule_lock:
        schedule.clear()
        routines = load_routines()
        for r in routines:
            register_routine(r)

def start_engine():
    reload_routines()
    print("[ROUTINE ENGINE] Started")
    while True:
        schedule.run_pending()
        time.sleep(1)