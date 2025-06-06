# src/imu.py
import board, busio, time, math
import adafruit_bno055
import imufusion
import numpy as np

class IMUReader:
    def __init__(self, i2c_bus, address, sample_rate=100):
        self.imu = adafruit_bno055(i2c_bus, address=address)
        self.ahrs = imufusion.Ahrs()
        self.sample_rate = sample_rate  # Hz
        time.sleep(0.5)

    def update(self):
        # Read sensor data
        gyro = np.array(self.imu.gyro)  # degrees/s
        accel = np.array(self.imu.acceleration)  # g
        mag = np.array(self.imu.magnetic)  # uT

        # Feed data to AHRS
        self.ahrs.update(gyro, accel, mag, 1.0 / self.sample_rate)

    def get_euler(self):
        # Call update before getting orientation
        self.update()
        # Returns (roll, pitch, yaw) in degrees
        return tuple(self.ahrs.quaternion.to_euler())

    def get_quaternion(self):
        # Call update before getting orientation
        self.update()
        # Returns quaternion as (w, x, y, z)
        q = self.ahrs.quaternion
        return (q.w, q.x, q.y, q.z)
        