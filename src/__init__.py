import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), "src"))

import board, busio, threading
from motor_controller import MotorController
from imu import IMU
from gimbal_test import test_vertical_setup, test_horizontal_setup
from evaluate import log_result, plot_results
from dashboard import create_app

def run_tests():
    # I2C initialisieren
    i2c = busio.I2C(board.SCL, board.SDA)
    while not i2c.try_lock(): pass

    imu_base   = IMU(i2c, address=0x68)
    imu_gimbal = IMU(i2c, address=0x69)
    motor = MotorController(step_pin=20, dir_pin=21, enable_pin=16)

    diff_v = test_vertical_setup(motor, imu_base, imu_gimbal)
    log_result("vertical", diff_v)
    input("→ Position ändern (90° drehen) und Enter drücken …")
    diff_h = test_horizontal_setup(motor, imu_base, imu_gimbal)
    log_result("horizontal", diff_h)

    plot_results()
    i2c.unlock()

if __name__ == "_main_":
    app = create_app()
    threading.Thread(target=lambda: app.run(host='0.0.0.0', port=5000),
                     daemon=True).start()
    run_tests()