from dronekit import connect
import config

def connect_vehicle():
    print("[INFO] Connecting to Pixhawk...")
    vehicle = connect(config.CONNECTION_STRING, wait_ready=True)
    return vehicle