from dronekit import connect
import time
import logging
import config

# Silence DroneKit PX4 errors
logging.getLogger("dronekit").setLevel(logging.CRITICAL)


def connect_vehicle():
    print("[INFO] Connecting to Pixhawk...")

    vehicle = connect(
        config.CONNECTION_STRING,
        wait_ready=False,          # False for PX4
        heartbeat_timeout=60
    )

    # Initialisation time
    time.sleep(2)

    # prevent PX4 mode crash spam
    try:
        vehicle._heartbeat_error = True
        vehicle._autopilot_type = 12  # MAV_AUTOPILOT_PX4
    except:
        pass

    print("[INFO] Connected to vehicle")

    return vehicle


def disconnect_vehicle(vehicle):
    print("[INFO] Disconnecting vehicle...")
    vehicle.close()
    print("[INFO] Vehicle disconnected")