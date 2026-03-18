from pymavlink import mavutil
import time
import threading
from config import PX4_MODE_OFFBOARD, TAKEOFF_ALTITUDE

# Global State
current_velocity = [0, 0, 0]
current_yaw_rate = 0
offboard_running = False


# Connection
def connect_vehicle(connection_string):
    print("[INFO] Connecting...")
    mav = mavutil.mavlink_connection(connection_string)
    mav.wait_heartbeat()
    print(f"[INFO] Connected (system={mav.target_system})")
    return mav

# Heartbeat & Mode Check
def refresh_heartbeat(mav):
    while True:
        msg = mav.recv_match(blocking=False)
        if msg is None:
            break
        if msg.get_type() == 'HEARTBEAT':
            mav._last_heartbeat = msg

def is_offboard(mav):
    hb = getattr(mav, '_last_heartbeat', None)
    return hb is not None and hb.custom_mode == PX4_MODE_OFFBOARD

def is_armed(mav):
    hb = getattr(mav, '_last_heartbeat', None)
    return hb is not None and bool(
        hb.base_mode & mavutil.mavlink.MAV_MODE_FLAG_SAFETY_ARMED
    )

# Offboard Stream
def offboard_loop(mav):
    global current_velocity, current_yaw_rate, offboard_running

    print("[INFO] OFFBOARD stream started")

    while offboard_running:
        vx, vy, vz = current_velocity
        yaw_rate = current_yaw_rate

        mav.mav.set_position_target_local_ned_send(
            0,
            mav.target_system,
            mav.target_component,
            mavutil.mavlink.MAV_FRAME_BODY_NED,
            0b0000011111000111,
            0, 0, 0,
            vx, vy, vz,
            0, 0, 0,
            0, yaw_rate
        )

        time.sleep(0.05)  # 20 Hz

def start_offboard_stream(mav):
    global offboard_running

    offboard_running = True
    threading.Thread(target=offboard_loop, args=(mav,), daemon=True).start()

    print("[INFO] Priming OFFBOARD stream...")
    time.sleep(2)

def stop_offboard_stream():
    global offboard_running
    offboard_running = False

# Control Primitives
def set_velocity(vx, vy, vz):
    global current_velocity
    current_velocity = [vx, vy, vz]

def set_yaw_rate(rate):
    global current_yaw_rate
    current_yaw_rate = rate

def request_offboard(mav):
    mav.mav.command_long_send(
        mav.target_system,
        mav.target_component,
        mavutil.mavlink.MAV_CMD_DO_SET_MODE,
        0,
        mavutil.mavlink.MAV_MODE_FLAG_CUSTOM_MODE_ENABLED,
        6,
        0, 0, 0, 0, 0
    )

def send_arm(mav, arm=True):
    mav.mav.command_long_send(
        mav.target_system,
        mav.target_component,
        mavutil.mavlink.MAV_CMD_COMPONENT_ARM_DISARM,
        0,
        1 if arm else 0,
        0, 0, 0, 0, 0, 0
    )

# Arm & Takeoff
def arm_and_takeoff(mav, altitude=TAKEOFF_ALTITUDE):
    print("[INFO] Starting takeoff sequence")

    # Start stream
    start_offboard_stream(mav)

    # Enter OFFBOARD
    print("[INFO] Switching to OFFBOARD...")
    start = time.time()
    while True:
        refresh_heartbeat(mav)

        if is_offboard(mav):
            break

        if time.time() - start > 10:
            print("[ERROR] OFFBOARD rejected")
            stop_offboard_stream()
            return False

        request_offboard(mav)
        time.sleep(0.5)

    print("[INFO] OFFBOARD mode active")

    # Arm
    print("[INFO] Arming...")
    start = time.time()
    while True:
        refresh_heartbeat(mav)

        if is_armed(mav):
            break

        if time.time() - start > 10:
            print("[ERROR] Arming failed")
            stop_offboard_stream()
            return False

        send_arm(mav, True)
        time.sleep(0.5)

    print("[INFO] Armed!")

    # Takeoff
    print("[INFO] Taking off...")
    set_velocity(0, 0, -1.5)

    start = time.time()
    while True:
        msg = mav.recv_match(type='GLOBAL_POSITION_INT', blocking=False)
        alt = (msg.relative_alt / 1000.0) if msg else 0

        if alt >= altitude * 0.95:
            break

        if time.time() - start > 20:
            print("[WARN] Takeoff timeout")
            break

        time.sleep(0.2)

    set_velocity(0, 0, 0)
    print("[INFO] Hovering")

    return True

# Movement & Yaw
def move_forward(mav, distance, speed=1.0):
    print(f"[INFO] Moving forward {distance}m")

    set_velocity(speed, 0, 0)
    time.sleep(distance / speed)

    set_velocity(0, 0, 0)
    time.sleep(0.5)

def move_backward(mav, distance, speed=1.0):
    print(f"[INFO] Moving backward {distance}m")

    set_velocity(-speed, 0, 0)
    time.sleep(distance / speed)

    set_velocity(0, 0, 0)
    time.sleep(0.5)

def move_left(mav, distance, speed=1.0):
    print(f"[INFO] Moving left {distance}m")

    set_velocity(0, speed, 0)
    time.sleep(distance / speed)

    set_velocity(0, 0, 0)
    time.sleep(0.5)

def move_right(mav, distance, speed=1.0):
    print(f"[INFO] Moving right {distance}m")

    set_velocity(0, -speed, 0)
    time.sleep(distance / speed)

    set_velocity(0, 0, 0)
    time.sleep(0.5)

def move_up(mav, distance, speed=1.0):
    print(f"[INFO] Moving up {distance}m")

    set_velocity(0, 0, -speed)
    time.sleep(distance / speed)

    set_velocity(0, 0, 0)
    time.sleep(0.5)

def move_down(mav, distance, speed=1.0):
    print(f"[INFO] Moving down {distance}m")

    set_velocity(0, 0, speed)
    time.sleep(distance / speed)

    set_velocity(0, 0, 0)
    time.sleep(0.5)

def yaw_left(mav, angle=90, rate=30):
    print(f"[INFO] Yawing left {angle} degrees")
    yaw_rate_rad = rate * (3.14159 / 180)
    duration = angle / rate
    set_yaw_rate(-yaw_rate_rad)
    time.sleep(duration)
    set_yaw_rate(0)
    time.sleep(0.5)

def yaw_right(mav, angle=90, rate=30):
    print(f"[INFO] Yawing right {angle} degrees")
    yaw_rate_rad = rate * (3.14159 / 180)
    duration = angle / rate
    set_yaw_rate(yaw_rate_rad)
    time.sleep(duration)
    set_yaw_rate(0)
    time.sleep(0.5)

# Landing & Disarm
def land(mav):
    print("[INFO] Landing...")

    set_velocity(0, 0, 0.8)

    while True:
        msg = mav.recv_match(type='GLOBAL_POSITION_INT', blocking=False)

        if msg:
            alt = (msg.relative_alt / 1000.0)

        if alt <= 0.1:
            print("[INFO] Landed!")
            break
    time.sleep(4)

    set_velocity(0, 0, 0)
    time.sleep(1)

    send_arm(mav, False)
    stop_offboard_stream()

    print("[INFO] Disarmed")