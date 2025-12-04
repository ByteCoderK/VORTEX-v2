# routines/routine_executor.py
import logging
import time

logger = logging.getLogger("routine_executor")

# Import your ESPController class and call via instance pattern used in your router.
# We'll attempt to import a global 'esp' if present (router.py creates it).
# Fallback: try import commands.XAUTOMATION.ESPController and create a local instance (best-effort).
try:
    # most of your code expects there to be a global `esp` object created in router
    from commands.XAUTOMATION import ESPController  # just to check available
except Exception:
    ESPController = None

def _get_esp_instance():
    # prefer a global esp if already created by router; otherwise make a local one (requires credentials)
    try:
        # if router created an esp in global scope, it'll be imported into same interpreter
        import builtins
        if hasattr(builtins, "esp"):
            return getattr(builtins, "esp")
    except Exception:
        pass

    # fallback: try to import the module-level 'esp' if available
    try:
        from router.router import esp as esp_from_router
        return esp_from_router
    except Exception:
        pass

    # last resort: don't create a new connection here automatically (credentials would be needed).
    return None

def execute_action(action: dict):
    """
    action example:
    {
        "type": "device",
        "relay": 1,
        "state": "ON"
    }
    """
    logger.info("[ROUTINE] execute_action: %s", action)
    typ = action.get("type")
    if typ == "device":
        relay = action.get("relay")
        state = action.get("state")
        if relay is None or state is None:
            logger.warning("[ROUTINE] Invalid device action (missing relay/state): %s", action)
            return

        esp = _get_esp_instance()
        if esp:
            try:
                esp.RoomControl(relay, state)
                logger.info("[ROUTINE] Sent RoomControl relay=%s state=%s", relay, state)
            except Exception as e:
                logger.exception("[ROUTINE] Failed to send RoomControl: %s", e)
        else:
            logger.warning("[ROUTINE] No ESP controller instance available; cannot send command.")
    elif typ == "delay":
        seconds = action.get("seconds", 1)
        time.sleep(seconds)
    else:
        logger.warning("[ROUTINE] Unknown action type: %s", action)