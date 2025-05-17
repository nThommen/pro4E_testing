# src/motor.py
from periphery import GPIO
import time

GPIO_CHIP = "/dev/gpiochip0"
class MotorController:
    def __init__(self, step_pin, dir_pin, enable_pin=None):
        self.step   = GPIO(GPIO_CHIP, step_pin,   "out")
        self.dir    = GPIO(GPIO_CHIP, dir_pin,    "out")
        self.enable = GPIO(GPIO_CHIP, enable_pin, "out") if enable_pin else None
        if self.enable: self.enable.write(False)

    def rotate(self, steps, direction, delay=0.002):
        self.dir.write(direction)
        for _ in range(steps):
            self.step.write(True); time.sleep(delay)
            self.step.write(False); time.sleep(delay)

    def cleanup(self):
        self.step.close(); self.dir.close()
        if self.enable:
            self.enable.write(True)
            self.enable.close()