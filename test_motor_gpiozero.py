#!/usr/bin/env python3
import sys, os
from gpiozero import OutputDevice
sys.path.insert(0, os.path.abspath("src"))
from motor_controller import MotorController
from time import sleep

motor = MotorController(step_pin=20, dir_pin=21, enable_pin=None)

#STEP = OutputDevice(20, active_high=True, initial_value=False)
#DIR  = OutputDevice(21, active_high=True, initial_value=False)

print("▶ Richtung vorwärts (LOW)")
motor.rotate(6400, True, 0.000026)
"""
DIR.off(); sleep(0.1)
print("▶ 200 Pulse vorwärts")
for _ in range(200):
    STEP.on(); sleep(0.002)
    STEP.off(); sleep(0.002)
"""

sleep(1)

print("▶ Richtung rückwärts (HIGH)")
motor.rotate(6400, False, 0.000026)
"""DIR.on(); sleep(0.1)
print("▶ 200 Pulse rückwärts")
for _ in range(200):
    STEP.on(); sleep(0.002)
    STEP.off(); sleep(0.002)"""

print("✅ Motor-Test abgeschlossen")