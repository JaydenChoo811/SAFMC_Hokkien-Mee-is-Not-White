from dronekit import VehicleMode
from pymavlink import mavutil
import time
from config import *
import config

drum_angle = 0 

def arm(vehicle):
    print("Arming")
    vehicle.mode = VehicleMode("GUIDED")
    vehicle.armed = True

    while not vehicle.armed:
        print("Arming...")
        time.sleep(1)

    vehicle.simple_takeoff(config.TAKEOFF_ALTITUDE)

# Motion
def send_velocity(vehicle, vx, vy, vz, distance):
    # Calculate speed magnitude
    speed = (vx**2 + vy**2 + vz**2)**0.5

    # Calculate duration to move the desired distance
    duration = distance / speed

    # Create MAVLink message
    msg = vehicle.message_factory.set_position_target_local_ned_encode(
        0, 0, 0,
        mavutil.mavlink.MAV_FRAME_BODY_NED,
        0b0000111111000111,  # use velocity
        0, 0, 0,             # positions ignored
        vx, vy, vz,          # velocity
        0, 0, 0,             # acceleration ignored
        0, 0
    )

    # Send repeatedly for the duration
    start_time = time.time()
    while time.time() - start_time < duration:
        vehicle.send_mavlink(msg)
        time.sleep(0.1)  # 10 Hz

# Yaw
def condition_yaw(vehicle, heading, relative=True):
    is_relative = 1 if relative else 0
    msg = vehicle.message_factory.command_long_encode(
        0, 0,
        mavutil.mavlink.MAV_CMD_CONDITION_YAW,
        0,
        heading,
        YAW_RATE, 1,
        is_relative,
        0, 0, 0
    )
    vehicle.send_mavlink(msg)


# Electromagnet - change aux port when connect
def electromagnet_on(vehicle):
    print("Electromagnet ON")
    set_servo(vehicle, 9, MAGNET_ON_PWM)   # HIGH

def electromagnet_off(vehicle):
    print("Electromagnet OFF")
    set_servo(vehicle, 9, MAGNET_OFF_PWM)   # LOW

# Drum - change aux port when connect
def set_servo(vehicle, channel, pwm):
    msg = vehicle.message_factory.command_long_encode(
        0, 0,
        mavutil.mavlink.MAV_CMD_DO_SET_SERVO,
        0,
        channel,
        pwm,
        0, 0, 0, 0, 0
    )
    vehicle.send_mavlink(msg)

def set_angle(vehicle, channel, angle):
    pwm = int(1000 + (angle / 180.0) * 1000)
    set_servo(vehicle, channel, pwm)

def rotate_drum(vehicle):
    global drum_angle
    print("Rotating drum 90")
    drum_angle += 90
    set_angle(vehicle, 10, drum_angle)