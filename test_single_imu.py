#!/usr/bin/env python3
import sys, os, time
sys.path.insert(0, os.path.abspath("src"))
from adafruit_mpu9250 import MPU9250

import board, busio

print("🚀 Einzel-IMU-Test @0x68 …")
i2c = busio.I2C(board.SCL, board.SDA)
while not i2c.try_lock(): pass

imu = IMUReader(i2c, address=0x68)
for i in range(5):
    r, p, y = imu.get_euler()
    print(f"Messung {i+1}: Roll={r:.1f}°, Pitch={p:.1f}°, Yaw={y:.1f}°")
    time.sleep(0.5)

i2c.unlock()
print("🎉 Test beendet")