# src/calibrate.py
import board, busio, yaml, time
from motor import MotorController
from imu import IMUReader

def auto_calibrate(cfg="config.yaml"):
    c=yaml.safe_load(open(cfg))
    bus=busio.I2C(board.SCL,board.SDA)
    while not bus.try_lock(): pass
    imu0=IMUReader(bus, c["imu"]["base_addr"])
    imu1=IMUReader(bus, c["imu"]["gimbal_addr"])
    motor=MotorController(**c["motor"])
    offs=[]
    for angle in c["calibration"]["test_angles"]:
        steps=int(angle*c["calibration"]["steps_per_degree"])
        motor.rotate(steps,True); time.sleep(0.5)
        offs.append(tuple(g-b for g,b in zip(imu1.get_euler(), imu0.get_euler())))
        motor.rotate(steps,False)
    print("Offsets:",offs)
    return offs

if _name=="main_":
    auto_calibrate()