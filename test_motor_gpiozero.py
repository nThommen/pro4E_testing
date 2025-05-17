#!/usr/bin/env python3
from gpiozero import OutputDevice
from time import sleep

STEP = OutputDevice(20, active_high=True, initial_value=False)
DIR  = OutputDevice(21, active_high=True, initial_value=False)

print("▶ Richtung vorwärts (LOW)")
DIR.off(); sleep(0.1)
print("▶ 200 Pulse vorwärts")
for _ in range(200):
    STEP.on(); sleep(0.002)
    STEP.off(); sleep(0.002)

sleep(1)
print("▶ Richtung rückwärts (HIGH)")
DIR.on(); sleep(0.1)
print("▶ 200 Pulse rückwärts")
for _ in range(200):
    STEP.on(); sleep(0.002)
    STEP.off(); sleep(0.002)

print("✅ Motor-Test abgeschlossen")