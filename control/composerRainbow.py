#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# creates files with data to play

import sys
import random
import binascii

# The first byte of the line indicates the line type
LEDLINE = 1     # control byte (fade, blinking,...)+ 10*3 bytes (RGB) + '\n'
DELAYLINE = 2   # delay with time in seconds to wait for next line
TURNOFFLINE = 3 # turn off all LED strips
RINGLINE = 4    # control byte (fade, blinking,...)+ ring number + 3 bytes (RGB) + '\n'

# control byte indicates effects on line, information is coded in the bits
BLINKINGBIT = 1 # bit pattern 0000 0001
PULSINGBIT = 2  # bit pattern 0000 0010
FADINGBIT = 16  # bit pattern 0001 0000
ROLLINBIT = 32  # bit pattern 0010 0000
INOUTBIT = 48   # bit pattern 0011 0000
RANDOMBIT = 64  # bit pattern 0100 0000

# Number of Arduinos connecgted and I2C address offset as can't start address 1
NUMARDUINO = 10 # we have 10 Arduinos on I2C bus

# Some colors
RED = ['ff','00','00']
GREEN = ['00','ff','00']
BLUE = ['00','00','ff']
YELLOW = ['ff','ff','00']
CYAN = ['00','ff','ff']
PINK = ['ff','00','ff']
BLACK = ['00', '00', '00']
WHITE = ['ff', 'ff', 'ff']
ORANGE = ['ee', '33', '00']

def write_line(fd, controlByte, ring1, ring2, ring3, ring4, ring5, ring6, ring7, ring8, ring9, ring10):
  fd.write(chr(LEDLINE))
  fd.write(chr(controlByte))
  fd.write(chr(int(ring1[0],16)))
  fd.write(chr(int(ring1[1],16)))
  fd.write(chr(int(ring1[2],16)))
  fd.write(chr(int(ring2[0],16)))
  fd.write(chr(int(ring2[1],16)))
  fd.write(chr(int(ring2[2],16)))
  fd.write(chr(int(ring3[0],16)))
  fd.write(chr(int(ring3[1],16)))
  fd.write(chr(int(ring3[2],16)))
  fd.write(chr(int(ring4[0],16)))
  fd.write(chr(int(ring4[1],16)))
  fd.write(chr(int(ring4[2],16)))
  fd.write(chr(int(ring5[0],16)))
  fd.write(chr(int(ring5[1],16)))
  fd.write(chr(int(ring5[2],16)))
  fd.write(chr(int(ring6[0],16)))
  fd.write(chr(int(ring6[1],16)))
  fd.write(chr(int(ring6[2],16)))
  fd.write(chr(int(ring7[0],16)))
  fd.write(chr(int(ring7[1],16)))
  fd.write(chr(int(ring7[2],16)))
  fd.write(chr(int(ring8[0],16)))
  fd.write(chr(int(ring8[1],16)))
  fd.write(chr(int(ring8[2],16)))
  fd.write(chr(int(ring9[0],16)))
  fd.write(chr(int(ring9[1],16)))
  fd.write(chr(int(ring9[2],16)))
  fd.write(chr(int(ring10[0],16)))
  fd.write(chr(int(ring10[1],16)))
  fd.write(chr(int(ring10[2],16)))
  fd.write('\n')
  return;

def line_delay(fd, time_to_wait):
  fd.write(chr(DELAYLINE))
  fd.write(chr(time_to_wait))
  fd.write('\n')
  return;

def shiftColumns(currentColumns):
    newColumns = [BLACK, BLACK, BLACK, BLACK, BLACK, BLACK, BLACK, BLACK, BLACK, BLACK]
    newColumns[9] = currentColumns[5]
    newColumns[5] = currentColumns[8]
    newColumns[8] = currentColumns[4]
    newColumns[2] = currentColumns[4]
    newColumns[0] = currentColumns[1]
    newColumns[4] = currentColumns[1]
    newColumns[1] = currentColumns[3]
    newColumns[7] = currentColumns[3]
    newColumns[3] = currentColumns[6]
    newColumns[6] = currentColumns[6]
    return newColumns

def makeRainbow(fd, color1, color2):
    selectedColors = [BLACK, BLACK, BLACK, BLACK, BLACK, BLACK, BLACK, BLACK, BLACK, BLACK]
    write_line(fd, 0, selectedColors[0], selectedColors[1], selectedColors[2], selectedColors[3], selectedColors[4], selectedColors[5], selectedColors[6], selectedColors[7], selectedColors[8], selectedColors[9])
    for i in range (0, 256, 16):
        selectedColors = shiftColumns(selectedColors)
        selectedColors[6][0] = hex((int(color1[0],16) & 1) * i)  # not perfect as it becomes 0xf0 and not 0xff
        selectedColors[6][1] = hex((int(color1[1],16) & 1) * i)
        selectedColors[6][2] = hex((int(color1[2],16) & 1) * i)
        write_line(fd, 0, selectedColors[0], selectedColors[1], selectedColors[2], selectedColors[3], selectedColors[4], selectedColors[5], selectedColors[6], selectedColors[7], selectedColors[8], selectedColors[9])
    stepColor0 = (int(color2[0],16) - int(color1[0],16)) / 0xff
    stepColor1 = (int(color2[1],16) - int(color1[1],16)) / 0xff
    stepColor2 = (int(color2[2],16) - int(color1[2],16)) / 0xff
    for i in range (0, 256):
        selectedColors = shiftColumns(selectedColors)
        selectedColors[6][0] = hex(int(color1[0],16) + (stepColor0 * i))
        selectedColors[6][1] = hex(int(color1[1],16) + (stepColor1 * i))
        selectedColors[6][2] = hex(int(color1[2],16) + (stepColor2 * i))
        write_line(fd, 0, selectedColors[0], selectedColors[1], selectedColors[2], selectedColors[3], selectedColors[4], selectedColors[5], selectedColors[6], selectedColors[7], selectedColors[8], selectedColors[9])
    return;

if __name__ == "__main__":
    dotsColor = [RED, YELLOW, GREEN, CYAN, BLUE, PINK, RED]
    for j in range (1,7) :
      fileName = './makeRainbow' + str(j) + '.dat'
      fd = open(fileName, 'wb')
      makeRainbow(fd, dotsColor[j-1], dotsColor[j])
      fd.close()
