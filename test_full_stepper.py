#!/usr/bin/env python3
import time
from periphery import GPIO

GPIO_CHIP = "/dev/gpiochip0"
pins = {
    "sleep": 17, "reset": 27, "enable": 16,
    "ms1": 5, "ms2": 6, "ms3": 13,
    "dir": 21, "step": 20
}
lines = {n: GPIO(GPIO_CHIP, p, "out") for n, p in pins.items()}

# wake, not reset, enable, full-step
lines["sleep"].write(True)
lines["reset"].write(True)
lines["enable"].write(False)
lines["ms1"].write(False)
lines["ms2"].write(False)
lines["ms3"].write(False)

# forward
lines["dir"].write(True)
print("▶ 200 Vollschritt-Pulse…")
for _ in range(200):
    lines["step"].write(True); time.sleep(0.005)
    lines["step"].write(False); time.sleep(0.005)

# cleanup
for l in lines.values(): l.close()
print("✅ Full-Stepper-Test fertig")