#!/usr/bin/env python3
import board, busio

i2c = busio.I2C(board.SCL, board.SDA)
while not i2c.try_lock(): pass
print("✅ I2C-Bus OK:", i2c)
i2c.unlock()