from STT.whisper_stt import main as stt_main
from Drone.connection import connect_vehicle

def main():
    vehicle = connect_vehicle()
    stt_main(vehicle)

if __name__ == "__main__":
    main()