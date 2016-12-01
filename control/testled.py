#!/usr/bin/env python
#
# send commands to i2c bus. 
# arg[1] is the I2C slave, first arduino is 11, so add 10
# sending first byte = 12 turns on the LED on Arduino 
# reading from I2C_SLAVE gives the state of the arduino

import smbus
import sys
import time

I2C_BUS = 1
BLINKLED = 12

if __name__ == '__main__':

  i2c = smbus.SMBus(I2C_BUS)

  I2C_SLAVE = int(sys.argv[1]) + 10

  while 1:
    try:
      i2c.write_byte(I2C_SLAVE, BLINKLED)
      i2c.write_byte(I2C_SLAVE, 0x00)
      i2c.write_byte(I2C_SLAVE, 0x00)
      i2c.write_byte(I2C_SLAVE, 0x00)
      i2c.write_byte(I2C_SLAVE, 0x00)
    except IOError:
      sys.stderr.write("*** ERROR Sending ***")

    sys.stdout.write("Sent command LED   ")
    time.sleep(0.5)
 
    try:
      state = i2c.read_byte(I2C_SLAVE)
      sys.stdout.write("state (0=busy, 1=ready) %d \n" % state)
    except IOError:
      sys.stderr.write("**** ERROR Reading ***")



