#!/usr/bin/env python3
import sys, os, time

from src.imu import IMU
sys.path.insert(0, os.path.abspath("src"))
#not clear if this is needed, but it was in the original code
#from adafruit_mpu9250 import MPU9250

import board, busio

print("🚀 Einzel-IMU-Test @0x68 …")
i2c = busio.I2C(board.SCL, board.SDA)
while not i2c.try_lock(): pass

imu = IMU(i2c, address=0x68)

for i in range(5):
    
    quaternion = imu.get_quaternion()
    print(f"Messung {i+1}: Quaternion={quaternion}")
    time.sleep(0.5)

    # Uncomment the following lines to get Euler angles instead of quaternion
    """euler_angles = imu.get_euler()
    print(f"Messung {i+1}: Roll={euler_angles[0]:.1f}°, Pitch={euler_angles[1]:.1f}°, Yaw={euler_angles[2]:.1f}°")
    time.sleep(0.5)"""
    
    #Old code for Euler angles not using imufusion library
    """r, p, y = imu.get_euler()
    print(f"Messung {i+1}: Roll={r:.1f}°, Pitch={p:.1f}°, Yaw={y:.1f}°")
    time.sleep(0.5)"""

i2c.unlock()
print("🎉 Test beendet")