import re
import config

def parse_command(text):

    text = text.lower().strip()
    distance = None

    # Extract number
    match = re.search(r'(\d+(\.\d+)?)\s*(m|metre|meter|meters)', text)
    if match:
        distance = float(match.group(1))

    if "arm" in text:
        return "ARM"
    elif "forward" in text:
        return ("FORWARD", distance)
    elif "right" in text:
        return ("RIGHT", distance)
    elif "left" in text:
        return ("LEFT", distance)
    elif "turn left" in text:
        return "TURN LEFT"
    elif "turn right" in text:
        return "TURN RIGHT"
    elif "up" in text:
        return ("UP", distance)
    elif "down" in text:
        return ("DOWN", distance)
    elif "stop" in text:
        return "STOP"
    elif "collect" in text:
        return "COLLECT"
    elif "drop" in text:
        return "DROP"
    elif "rotate" in text:
        return "ROTATE DRUM"
    else:
        return "UNKNOWN"