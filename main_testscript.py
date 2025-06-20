#!/usr/bin/env python3
import sys, os
import threading
sys.path.insert(0, os.path.abspath("src"))
from motor_controller import MotorController
from imu import IMU
from scipy.spatial.transform import Rotation as R
import board
import matplotlib.pyplot as plt
import numpy as np
from gpiozero import OutputDevice
from time import sleep

motor = MotorController(step_pin=20, dir_pin=21, enable_pin=None)
num_steps = 6400  # Adjust as needed for your motor
delay = 0.0005  # Adjust as needed for your motor speed

sensor_gimbal = IMU(
    i2c_bus=board.I2C(),
    address=0x28,
    offset_accel=(1, -48, -31),
    offset_gyro=(-1, -2, -1),
    offset_mag=(-151, 499, 570)
)

sensor_tisch = IMU(
    i2c_bus=board.I2C(),
    address=0x29,
    offset_accel=(-15, -15, -20),
    offset_gyro=(-2, -3, 0),
    offset_mag=(-10, 371, 5)
)
# Wait for the sensors to initialize
sleep(1)


def to_scipy_quat(q):
    # Convert (w, x, y, z) → (x, y, z, w)
    return [q[1], q[2], q[3], q[0]]

def motor_task():
    while True:
        motor.rotate(num_steps, False, delay)
        sleep(1)
        motor.rotate(num_steps, True, delay)
        sleep(1)

# Start the motor control in a separate thread
motor_thread = threading.Thread(target=motor_task, daemon=True)
motor_thread.start()

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
plt.ion()
plt.show()



while motor_thread.is_alive():
    q_tisch = sensor_tisch.imu.quaternion
    q_gimbal = sensor_gimbal.imu.quaternion
        
    r_tisch = R.from_quat(to_scipy_quat(q_tisch))
    r_gimbal = R.from_quat(to_scipy_quat(q_gimbal))
    
    q_relative = r_gimbal * r_tisch.inv()
    rotation_matrix = q_relative.as_matrix()
    
    # Axes
    origin = np.array([0, 0, 0])
    x_axis = rotation_matrix @ np.array([1, 0, 0])
    y_axis = rotation_matrix @ np.array([0, 1, 0])
    z_axis = rotation_matrix @ np.array([0, 0, 1])
    
    ax.clear()
    ax.quiver(*origin, *x_axis, color='r', label='X-axis')
    ax.quiver(*origin, *y_axis, color='g', label='Y-axis')
    ax.quiver(*origin, *z_axis, color='b', label='Z-axis')
    ax.set_xlim([-1, 1])
    ax.set_ylim([-1, 1])
    ax.set_zlim([-1, 1])
    ax.set_xlabel('X-axis')
    ax.set_ylabel('Y-axis')
    ax.set_zlabel('Z-axis')
    ax.set_title('Relative Orientation of Gimbal and Tisch')
    ax.legend()    
        
    plt.draw()
    plt.pause(0.1)


"""print("▶ Richtung rückwärts (HIGH)")
motor.rotate(num_steps, True, delay)
sleep(1)

print("▶ Richtung vorwärts (LOW)")
motor.rotate(num_steps, False, delay)
sleep(1)

print("✅ Motor-Test abgeschlossen")"""
