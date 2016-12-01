#!/usr/bin/env python
#
# send commands to i2c bus.
# arduino is waiting for command with ID of argv
# sending first byte = 10 turns LEDs off
# reading from ID gives the state of the arduino

import smbus
import sys
import time

I2C_BUS = 1
BLINKLED = 13
SETCOLOR = 12
ALLOFF = 10

if __name__ == '__main__':

  I2C_SLAVE = int(sys.argv[1]) + 10

  i2c = smbus.SMBus(I2C_BUS)

  try:
    i2c.write_byte(I2C_SLAVE, ALLOFF)
    i2c.write_byte(I2C_SLAVE, 0x00)
    i2c.write_byte(I2C_SLAVE, 0x00)
    i2c.write_byte(I2C_SLAVE, 0x00)
    i2c.write_byte(I2C_SLAVE, 0x00)
  except IOError:
    sys.stderr.write("*** ERROR turning off ***")

  sys.stdout.write("Sent turn OFF\n")
