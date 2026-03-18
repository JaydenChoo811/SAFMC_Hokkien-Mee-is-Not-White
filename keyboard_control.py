import time
from Drone.controller import connect_vehicle
from NLP.commands import execute
import logging
logging.getLogger("dronekit").setLevel(logging.CRITICAL)

def keyboard_loop():
    """
    Simple command loop to control the drone via keyboard input.
    Type commands like: ARM, FORWARD 2, UP 1, YAW_LEFT 90 etc.
    Type QUIT to exit.
    """

    mav = connect_vehicle("udp:127.0.0.1:14540")
    print("[INFO] Connected to vehicle")
    print("Enter commands (type QUIT to exit)")

    try:
        while True:
            user_input = input(">>> ").strip()
            if not user_input:
                continue

            # Quit
            if user_input.upper() == "QUIT":
                print("[INFO] Exiting keyboard control")
                break

            parts = user_input.split()
            cmd = parts[0].upper()
            distance = None

            if len(parts) > 1:
                try:
                    distance = float(parts[1])
                except ValueError:
                    print("[WARN] Invalid distance, ignoring")

            print(f"[INPUT] Command: {cmd}, Distance: {distance}")
            execute(mav, cmd, distance)

    except KeyboardInterrupt:
        print("\n[INFO] Keyboard loop interrupted")

    finally:
        mav.close()
        print("[INFO] Vehicle disconnected")

if __name__ == "__main__":
    keyboard_loop()