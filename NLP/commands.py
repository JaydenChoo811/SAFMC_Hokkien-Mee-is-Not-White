from Drone.controller import *
from config import SPEED, YAW_RATE

def execute(mav, command, value):
    print(f"[EXEC] {command} | value={value}")

    if command == "ARM":
        arm_and_takeoff(mav, altitude=3)

    elif command == "FORWARD":
        dist = value if value else 2
        move_forward(mav, dist, SPEED)

    elif command == "BACKWARD":
        dist = value if value else 2
        move_backward(mav, dist, SPEED)

    elif command == "LEFT":
        dist = value if value else 2
        move_left(mav, dist, SPEED)

    elif command == "RIGHT":
        dist = value if value else 2
        move_right(mav, dist, SPEED)

    elif command == "UP":
        dist = value if value else 2
        move_up(mav, dist, SPEED)

    elif command == "DOWN":
        dist = value if value else 1
        move_down(mav, dist, SPEED)

    elif command == "YAW_LEFT":
        angle = value if value else 90
        yaw_left(mav, angle, YAW_RATE)

    elif command == "YAW_RIGHT":
        angle = value if value else 90
        yaw_right(mav, angle, YAW_RATE)

    elif command == "STOP":
        set_velocity(0, 0, 0)
        set_yaw_rate(0)

    elif command == "LAND":
        land(mav)

    else:
        print("[WARN] Unknown command")