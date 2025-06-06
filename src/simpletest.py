# Simple Adafruit BNO055 sensor reading example.  Will print the orientation
# and calibration data every second.
#
# Copyright (c) 2015 Adafruit Industries
# Author: Tony DiCola
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.
import time
import board
import adafruit_bno055
import numpy as np
import matplotlib.pyplot as plt
from scipy.spatial.transform import Rotation as R

i2c = board.I2C()
sensor_gimbal = adafruit_bno055.BNO055_I2C(i2c, address=0x28)
sensor_tisch = adafruit_bno055.BNO055_I2C(i2c, address=0x29)
frame_num = 0

# Define the sensor offsets for calibration.
# These offsets are specific to the sensors and were determined through calibration.
sensor_1_accel_offset = (1, -48, -31)
sensor_1_gyro_offset = (-1, -2, -1)
sensor_1_mag_offset = (-151, 499, 570)

sensor_2_accel_offset = (-15, -15, -20)
sensor_2_gyro_offset = (-2, -3, 0)
sensor_2_mag_offset = (-10, 371, 5)


# Set the sensor offsets for calibration.
sensor_gimbal.offsets_accelerometer = sensor_1_accel_offset
sensor_gimbal.offsets_gyroscope = sensor_1_gyro_offset
sensor_gimbal.offsets_magnetometer = sensor_1_mag_offset

sensor_tisch.offsets_accelerometer = sensor_2_accel_offset
sensor_tisch.offsets_gyroscope = sensor_2_gyro_offset
sensor_tisch.offsets_magnetometer = sensor_2_mag_offset

def to_scipy_quat(q):
    # Convert (w, x, y, z) → (x, y, z, w)
    return [q[1], q[2], q[3], q[0]]

# Wait for the sensors to initialize.
time.sleep(1)

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
plt.show(block=False)

# Main loop to read sensor data and print it.
while True:
    for idx, sensor in enumerate([sensor_gimbal, sensor_tisch], start=1):
        # Read the sensor calibration status.
        # The BNO055 has 4 sensors: system, gyro, accelerometer, and magnetometer.
        sys, gyro, accel, mag = sensor.calibration_status
        print(f"[Sensor {idx}] Calibration status: Sys={sys}, Gyro={gyro}, Accel={accel}, Mag={mag}")
        
        """offset_accel = sensor.offsets_accelerometer
        offset_gyro = sensor.offsets_gyroscope
        offset_mag = sensor.offsets_magnetometer
        print(f"[Sensor {idx}] Accel_Offset: {offset_accel}, Gyro_Offset: {offset_gyro}, Mag_Offset: {offset_mag}")"""

        print("-" * 60)
    
    q_tisch = sensor_tisch.quaternion
    q_gimbal = sensor_gimbal.quaternion
    
    #q_rel = q_gimbal * np.conjugate(q_tisch)
    #rot_matrix = R.from_quat(q_rel).as_matrix()

    r_gimbal = R.from_quat(to_scipy_quat(sensor_gimbal.quaternion))
    r_tisch  = R.from_quat(to_scipy_quat(sensor_tisch.quaternion))

    q_rel = r_gimbal * r_tisch.inv()
    rot_matrix = q_rel.as_matrix()

    
    # Axes
    origin = np.array([0, 0, 0])
    x_axis = rot_matrix @ np.array([1, 0, 0])
    y_axis = rot_matrix @ np.array([0, 1, 0])
    z_axis = rot_matrix @ np.array([0, 0, 1])
    
    # Plot the axes
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
    ax.set_title('Relative Orientation of Sensors')
    ax.legend()
    
    plt.pause(1)  # Update the plot
    plt.savefig(f"frame_{frame_num:04d}.png")
    frame_num += 1

    