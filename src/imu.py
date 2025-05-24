# src/imu.py
import board, busio, time, math
from adafruit_mpu9250 import MPU9250
import imufusion
import numpy as np

class IMUReader:
    def __init__(self, i2c_bus, address=0x68):
        self.imu = MPU9250(i2c_bus, address=address)
        self.ahrs = imufusion.Ahrs()
        time.sleep(0.5)

    def get_euler(self):
        ax, ay, az = self.imu.acceleration
        roll  = math.degrees(math.atan2(ay, az))
        pitch = math.degrees(math.atan2(-ax, math.sqrt(ay*ay+az*az)))
        mx, my, mz = self.imu.magnetic
        yaw   = math.degrees(math.atan2(my, mx))
        return (roll, pitch, yaw)