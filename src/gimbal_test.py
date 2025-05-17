# src/gimbal_test.py
import time
def measure_diff(motor, imu_base, imu_gimbal, steps, dir):
    motor.rotate(steps, dir); time.sleep(0.5)
    b=imu_base.get_euler(); g=imu_gimbal.get_euler()
    return tuple(g[i]-b[i] for i in range(3))

def test_vertical_setup(m,m1,m2):
    print("== Vertikal ==")
    d=measure_diff(m,m1,m2,200,True)
    print("Diff:",d); return d

def test_horizontal_setup(m,m1,m2):
    print("== Horizontal ==")
    d=measure_diff(m,m1,m2,200,True)
    print("Diff:",d); return d