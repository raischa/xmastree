#!/usr/bin/env python
#
# send commands to i2c bus. 
# arduino is wainting for command, ID in argv1
# sending first byte = 13 sets RGB color
# reading from ID gives the state of the arduino

import smbus
import sys
import time

I2C_BUS = 1
SETCOLOR = 13

if __name__ == '__main__':

  I2C_SLAVE = int(sys.argv[1])+10
  
  i2c = smbus.SMBus(I2C_BUS)

  while 1:
    try:
      i2c.write_byte(I2C_SLAVE, SETCOLOR)
      i2c.write_byte(I2C_SLAVE, 0xff)
      i2c.write_byte(I2C_SLAVE, 0x00)
      i2c.write_byte(I2C_SLAVE, 0x00)
      i2c.write_byte(I2C_SLAVE, 0x00)
    except IOError:
      sys.stderr.write("*** ERROR Sending RED ***")

    sys.stdout.write("Sent color RED    ")
    time.sleep(0.5)
 
    try:
      state = i2c.read_byte(I2C_SLAVE)
      sys.stdout.write("state (0=busy, 1=ready) %d \n" % state)
    except IOError:
      sys.stderr.write("**** ERROR Reading RED ***")

    try:
      i2c.write_byte(I2C_SLAVE, SETCOLOR)
      i2c.write_byte(I2C_SLAVE, 0x00)
      i2c.write_byte(I2C_SLAVE, 0xff)
      i2c.write_byte(I2C_SLAVE, 0x00)
      i2c.write_byte(I2C_SLAVE, 0x00)
    except IOError:
      sys.stderr.write("*** ERROR Sending GREEN ***")

    sys.stdout.write("Sent color GREEN  ")
    time.sleep(0.5)
 
    try:
      state = i2c.read_byte(I2C_SLAVE)
      sys.stdout.write("state (0=busy, 1=ready) %d \n" % state)
    except IOError:
      sys.stderr.write("**** ERROR Reading GREEN ***")

    try:
      i2c.write_byte(I2C_SLAVE, SETCOLOR)
      i2c.write_byte(I2C_SLAVE, 0x00)
      i2c.write_byte(I2C_SLAVE, 0x00)
      i2c.write_byte(I2C_SLAVE, 0xff)
      i2c.write_byte(I2C_SLAVE, 0x00)
    except IOError:
      sys.stderr.write("*** ERROR Sending BLUE ***")

    sys.stdout.write("Sent color BLUE   ")
    time.sleep(0.5)
 
    try:
      state = i2c.read_byte(I2C_SLAVE)
      sys.stdout.write("state (0=busy, 1=ready) %d \n" % state)
    except IOError:
      sys.stderr.write("**** ERROR Reading BLUE ***")
