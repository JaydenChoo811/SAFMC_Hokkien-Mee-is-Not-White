from Drone.controller import *
from config import *

def execute(vehicle, command, distance):

    if command == "ARM":
        arm(vehicle)

    elif command == "FORWARD":
        send_velocity(vehicle, VELOCITY_X, 0, 0, distance)

    elif command == "RIGHT":
        send_velocity(vehicle, 0, VELOCITY_Y, 0, distance)

    elif command == "LEFT":
        send_velocity(vehicle, 0, -VELOCITY_Y, 0, distance)

    elif command == "TURN LEFT":
        condition_yaw(vehicle, -YAW_INCREMENT, relative=True)

    elif command == "TURN RIGHT":
        condition_yaw(vehicle, YAW_INCREMENT, relative=True)

    elif command == "UP":
        send_velocity(vehicle, 0, 0, -VELOCITY_Z, distance)

    elif command == "DOWN":
        send_velocity(vehicle, 0, 0, VELOCITY_Z, distance)

    elif command == "STOP":
        send_velocity(vehicle, 0, 0, 0, 0)

    elif command == "COLLECT":
        electromagnet_on(vehicle)

    elif command == "DROP":
        electromagnet_off(vehicle)

    elif command == "ROTATE DRUM":
        rotate_drum(vehicle)

    else:
        print("[WARN] Unknown command")