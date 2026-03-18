import re

def parse_input(text):
    text = text.lower().strip()

    # Extract number (distance)
    match = re.search(r"\d+(\.\d+)?", text)
    distance = float(match.group()) if match else None

    # Command detection
    if "takeoff" in text or "arm" in text:
        return "ARM", distance

    elif "forward" in text:
        return "FORWARD", distance

    elif "back" in text:
        return "BACKWARD", distance

    elif "left" in text and "yaw" not in text:
        return "LEFT", distance

    elif "right" in text and "yaw" not in text:
        return "RIGHT", distance

    elif "up" in text:
        return "UP", distance

    elif "down" in text:
        return "DOWN", distance

    elif "yaw left" in text or "turn left" in text:
        return "YAW_LEFT", distance

    elif "yaw right" in text or "turn right" in text:
        return "YAW_RIGHT", distance

    elif "land" in text:
        return "LAND", None

    elif "stop" in text or "hover" in text:
        return "STOP", None

    return "UNKNOWN", None