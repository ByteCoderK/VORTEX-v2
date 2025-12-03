import schedule
import time
from datetime import datetime
project_root = os.path.abspath("C:\\Users\\User One\\Desktop\\VORTEX-v2")
sys.path.append(project_root)
logging.debug(f"Project root set to: {project_root}")

# routine imports
from routine_db import load_routines
from routine_executor import execute_action

def register_routine(routine):

    t = routine["trigger"]
    action = routine["action"]

    # Daily routines
    if t["frequency"] == "daily":
        schedule.every().day.at(t["value"]).do(execute_action, action)

    # Weekly routines
    elif t["frequency"] == "monday":
        schedule.every().monday.at(t["value"]).do(execute_action, action)

    elif t["frequency"] == "tuesday":
        schedule.every().tuesday.at(t["value"]).do(execute_action, action)

    # Add more days if needed
    elif t["frequency"] == "wednesday":
        schedule.every().wednesday.at(t["value"]).do(execute_action, action)

    elif t["frequency"] == "thursday":
        schedule.every().thursday.at(t["value"]).do(execute_action, action)

    elif t["frequency"] == "friday":
        schedule.every().friday.at(t["value"]).do(execute_action, action)

    elif t["frequency"] == "saturday":
        schedule.every().saturday.at(t["value"]).do(execute_action, action)

    elif t["frequency"] == "sunday":
        schedule.every().sunday.at(t["value"]).do(execute_action, action)

    else:
        # One-time routine
        schedule.every().day.at(t["value"]).do(execute_once, action)

def execute_once(action):
    execute_action(action)
    # TODO: remove routine from DB after execution

def start_engine():
    routines = load_routines()

    for r in routines:
        register_routine(r)

    print("[ROUTINE] Engine started.")

    while True:
        schedule.run_pending()
        time.sleep(1)