# src/imu.py
import board, time
import adafruit_bno055
import numpy as np
import matplotlib.pyplot as plt
from scipy.spatial.transform import Rotation as R

class IMU:
    def __init__(self, i2c_bus, address, offset_accel, offset_gyro, offset_mag):
        self.imu = adafruit_bno055.BNO055_I2C(i2c_bus, address=address)
        self.offset_accelerometer = offset_accel
        self.offset_gyroscope = offset_gyro
        self.offset_magnetometer = offset_mag
        time.sleep(0.5)

    def get_quaternion(self):
        q = self.imu.quaternion
        if q is None:
            return None
        
    
    def plot(self, ax):
        q = self.imu.quaternion
        r = R.from_quat([q[1], q[2], q[3], q[0]])
        ax.quiver(0, 0, 0, *r.as_matrix()[:, 0], color='r', label='X-axis')
        ax.quiver(0, 0, 0, *r.as_matrix()[:, 1], color='g', label='Y-axis')
        ax.quiver(0, 0, 0, *r.as_matrix()[:, 2], color='b', label='Z-axis')
        
    
        