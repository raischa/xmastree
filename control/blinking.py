#!/usr/bin/env python
#
# send commands to i2c bus. 
# arduino is wainting for command, ID is in argv1
# sending first byte = 14 sets RGB color, and starts binking
# reading from ID=4 gives the state of the arduino

import smbus
import sys
import time

I2C_BUS = 1
BLINKING = 14

if __name__ == '__main__':

  I2C_SLAVE = int(sys.argv[1])+10

  i2c = smbus.SMBus(I2C_BUS)

  while 1:
    try:
      i2c.write_byte(I2C_SLAVE, BLINKING)
      i2c.write_byte(I2C_SLAVE, 0xff)
      i2c.write_byte(I2C_SLAVE, 0x00)
      i2c.write_byte(I2C_SLAVE, 0x00)
      i2c.write_byte(I2C_SLAVE, 0x00)
    except IOError:
      sys.stderr.write("*** ERROR Sending RED ***")

    sys.stdout.write("Sent color RED    ")
    time.sleep(5)
 
    try:
      state = i2c.read_byte(I2C_SLAVE)
      sys.stdout.write("state (0=busy, 1=ready) %d \n" % state)
    except IOError:
      sys.stderr.write("**** ERROR Reading RED ***")

    try:
      i2c.write_byte(I2C_SLAVE, BLINKING)
      i2c.write_byte(I2C_SLAVE, 0x00)
      i2c.write_byte(I2C_SLAVE, 0xff)
      i2c.write_byte(I2C_SLAVE, 0x00)
      i2c.write_byte(I2C_SLAVE, 0x00)
    except IOError:
      sys.stderr.write("*** ERROR Sending GREEN ***")

    sys.stdout.write("Sent color GREEN  ")
    time.sleep(5)
 
    try:
      state = i2c.read_byte(I2C_SLAVE)
      sys.stdout.write("state (0=busy, 1=ready) %d \n" % state)
    except IOError:
      sys.stderr.write("**** ERROR Reading GREEN ***")

    try:
      i2c.write_byte(I2C_SLAVE, BLINKING)
      i2c.write_byte(I2C_SLAVE, 0x00)
      i2c.write_byte(I2C_SLAVE, 0x00)
      i2c.write_byte(I2C_SLAVE, 0xff)
      i2c.write_byte(I2C_SLAVE, 0x00)
    except IOError:
      sys.stderr.write("*** ERROR Sending BLUE ***")

    sys.stdout.write("Sent color BLUE   ")
    time.sleep(5)
 
    try:
      state = i2c.read_byte(I2C_SLAVE)
      sys.stdout.write("state (0=busy, 1=ready) %d \n" % state)
    except IOError:
      sys.stderr.write("**** ERROR Reading BLUE ***")