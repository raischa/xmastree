#!/usr/bin/env python
#
# send commands to i2c bus. 
# arduino is wainting for command, loader sends to all of them
# sending first byte = 13 sets RGB color
# reading from ID gives the state of the arduino
import time
import RPi.GPIO as GPIO
import sys
import smbus
import logging
import getopt

I2C_BUS = 1
GPIOPIN = 4
SETCOLOR = 13
NUMARDUINO = 10
NUMOFFSET = 10

def resetAll():
    sys.stderr.write('got Reset')
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(GPIOPIN, GPIO.OUT)
    GPIO.output(GPIOPIN, GPIO.LOW)
    time.sleep(1)
    GPIO.output(GPIOPIN, GPIO.HIGH)
    sys.stderr.write('done Reset')
    GPIO.cleanup()
    time.sleep(2)
    return;

def doSetColor(line):  
  i2c = smbus.SMBus(I2C_BUS)

  for j in range (1,2):
    for i in range (1, NUMARDUINO+1):
      try:
        i2c.write_byte(i+NUMOFFSET, SETCOLOR)
        i2c.write_byte(i+NUMOFFSET, 0xff)
        i2c.write_byte(i+NUMOFFSET, 0x00)
        i2c.write_byte(i+NUMOFFSET, 0x00)
        i2c.write_byte(i+NUMOFFSET, 0x00)
        sys.stderr.write("sent red to:%d" % i)
      except IOError:
        sys.stderr.write("*** ERROR Sending RED ***")

      sys.stdout.write("Sent color RED    ")
      time.sleep(0.5)
 
      try:
        state = i2c.read_byte(i+NUMOFFSET)
        sys.stdout.write("state (0=busy, 1=ready) %d \n" % state)
      except IOError:
        sys.stderr.write("**** ERROR Reading RED ***")

      try:
        i2c.write_byte(i+NUMOFFSET, SETCOLOR)
        i2c.write_byte(i+NUMOFFSET, 0x00)
        i2c.write_byte(i+NUMOFFSET, 0xff)
        i2c.write_byte(i+NUMOFFSET, 0x00)
        i2c.write_byte(i+NUMOFFSET, 0x00)
        sys.stderr.write("sent green to:%d" % i)
      except IOError:
        sys.stderr.write("*** ERROR Sending GREEN ***")

      sys.stdout.write("Sent color GREEN  ")
      time.sleep(0.5)
 
      try:
        state = i2c.read_byte(i+NUMOFFSET)
        sys.stdout.write("state (0=busy, 1=ready) %d \n" % state)
      except IOError:
        sys.stderr.write("**** ERROR Reading GREEN ***")

      try:
        i2c.write_byte(i+NUMOFFSET, SETCOLOR)
        i2c.write_byte(i+NUMOFFSET, 0x00)
        i2c.write_byte(i+NUMOFFSET, 0x00)
        i2c.write_byte(i+NUMOFFSET, 0xff)
        i2c.write_byte(i+NUMOFFSET, 0x00)
        sys.stderr.write("sent blue to:%d" % i)
      except IOError:
        sys.stderr.write("*** ERROR Sending BLUE ***")

      sys.stdout.write("Sent color BLUE   ")
      time.sleep(0.5)
 
      try:
        state = i2c.read_byte(i+NUMOFFSET)
        sys.stdout.write("state (0=busy, 1=ready) %d \n" % state)
      except IOError:
        sys.stderr.write("**** ERROR Reading BLUE ***")
  return;

def handleLine(line):
  doSetColor(line[1:])
  return;

if __name__ == '__main__':

  resetAll()
  
  with open("/var/www/html/data.dat", 'r') as configFile:
    for line in configFile:
      handleLine(line[1:])
