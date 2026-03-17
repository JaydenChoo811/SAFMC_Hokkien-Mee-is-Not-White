from STT.whisper_stt import StreamingWhisper
from NLP.parser import parse_command
from NLP.commands import execute
from Drone.connection import connect_vehicle
import time

def main():
    stt = StreamingWhisper(model_size="base")
    vehicle = connect_vehicle()

    stt.start_stream()

    last_command = None
    last_time = 0

    print("[SYSTEM READY - STREAMING MODE]")

    try:
        while True:
            text = stt.listen()

            if text:
                print(f"[HEARD]: {text}")

                command = parse_command(text)

                # prevent repeated spam
                if command != "UNKNOWN":
                    current_time = time.time()

                    if command != last_command or (current_time - last_time > 2):
                        print(f"[COMMAND]: {command}")
                        execute(vehicle, command)

                        last_command = command
                        last_time = current_time

            time.sleep(0.5)

    except KeyboardInterrupt:
        print("[INFO] Shutting down...")
        stt.stop()
        vehicle.close()

if __name__ == "__main__":
    main()