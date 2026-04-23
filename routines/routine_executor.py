import logging
import time

logger = logging.getLogger("routine_executor")
try:
    from commands.XAUTOMATION import ESPController
except Exception:
    ESPController = None

def _get_esp_instance():
    try:
        import builtins
        if hasattr(builtins, "esp"):
            return getattr(builtins, "esp")
    except Exception:
        pass

    try:
        from router.router import esp as esp_from_router
        return esp_from_router
    except Exception:
        pass

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