#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# creates files with data to play

import sys
import random

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

def line_turnoff(fd):
  fd.write(chr(TURNOFFLINE))
  fd.write('\n')
  return;

def makeRandomDots(fd):
    dotsColor = [RED, GREEN, BLUE, YELLOW, CYAN, PINK, WHITE, ORANGE]
    write_line(fd, RANDOMBIT, random.choice(dotsColor), random.choice(dotsColor), random.choice(dotsColor), random.choice(dotsColor), random.choice(dotsColor), random.choice(dotsColor), random.choice(dotsColor), random.choice(dotsColor), random.choice(dotsColor), random.choice(dotsColor))
    line_delay(fd, 1)
    return;

def makePacManLeft(fd):
    dotsColor = [RED, GREEN, BLUE, YELLOW, CYAN, PINK, WHITE, ORANGE]
    selectedColors = [random.choice(dotsColor), random.choice(dotsColor), random.choice(dotsColor), random.choice(dotsColor), random.choice(dotsColor), random.choice(dotsColor), random.choice(dotsColor), random.choice(dotsColor), random.choice(dotsColor), random.choice(dotsColor)]
    write_line(fd, ROLLINBIT, selectedColors[0], selectedColors[1], selectedColors[2], selectedColors[3], selectedColors[4], selectedColors[5], selectedColors[6], selectedColors[7], selectedColors[8], selectedColors[9])
    write_line(fd, ROLLINBIT, selectedColors[0], selectedColors[1], selectedColors[2], selectedColors[3], selectedColors[4], selectedColors[5], selectedColors[6], selectedColors[6], selectedColors[8], selectedColors[9])
    write_line(fd, ROLLINBIT, selectedColors[0], selectedColors[1], selectedColors[2], selectedColors[3], selectedColors[4], selectedColors[5], selectedColors[6], selectedColors[6], selectedColors[6], selectedColors[9])
    write_line(fd, ROLLINBIT, selectedColors[0], selectedColors[1], selectedColors[2], selectedColors[3], selectedColors[4], selectedColors[5], selectedColors[6], selectedColors[6], selectedColors[6], selectedColors[6])
    write_line(fd, ROLLINBIT, selectedColors[0], selectedColors[1], selectedColors[2], selectedColors[3], selectedColors[4], selectedColors[6], selectedColors[6], selectedColors[6], selectedColors[6], selectedColors[6])
    write_line(fd, ROLLINBIT, selectedColors[0], selectedColors[1], selectedColors[2], selectedColors[3], selectedColors[6], selectedColors[6], selectedColors[6], selectedColors[6], selectedColors[6], selectedColors[6])
    write_line(fd, ROLLINBIT, selectedColors[0], selectedColors[1], selectedColors[2], selectedColors[6], selectedColors[6], selectedColors[6], selectedColors[6], selectedColors[6], selectedColors[6], selectedColors[6])
    write_line(fd, ROLLINBIT, selectedColors[0], selectedColors[1], selectedColors[6], selectedColors[6], selectedColors[6], selectedColors[6], selectedColors[6], selectedColors[6], selectedColors[6], selectedColors[6])
    write_line(fd, ROLLINBIT, selectedColors[0], selectedColors[6], selectedColors[6], selectedColors[6], selectedColors[6], selectedColors[6], selectedColors[6], selectedColors[6], selectedColors[6], selectedColors[6])
    write_line(fd, ROLLINBIT, selectedColors[6], selectedColors[6], selectedColors[6], selectedColors[6], selectedColors[6], selectedColors[6], selectedColors[6], selectedColors[6], selectedColors[6], selectedColors[6])
    write_line(fd, ROLLINBIT, selectedColors[6], selectedColors[6], selectedColors[6], selectedColors[6], selectedColors[6], selectedColors[6], selectedColors[6], selectedColors[7], selectedColors[6], selectedColors[6])
    write_line(fd, ROLLINBIT, selectedColors[6], selectedColors[6], selectedColors[6], selectedColors[6], selectedColors[6], selectedColors[6], selectedColors[6], selectedColors[7], selectedColors[8], selectedColors[6])
    write_line(fd, ROLLINBIT, selectedColors[6], selectedColors[6], selectedColors[6], selectedColors[6], selectedColors[6], selectedColors[6], selectedColors[6], selectedColors[7], selectedColors[8], selectedColors[9])
    write_line(fd, ROLLINBIT, selectedColors[6], selectedColors[6], selectedColors[6], selectedColors[6], selectedColors[6], selectedColors[5], selectedColors[6], selectedColors[7], selectedColors[8], selectedColors[9])
    write_line(fd, ROLLINBIT, selectedColors[6], selectedColors[6], selectedColors[6], selectedColors[6], selectedColors[4], selectedColors[5], selectedColors[6], selectedColors[7], selectedColors[8], selectedColors[9])
    write_line(fd, ROLLINBIT, selectedColors[6], selectedColors[6], selectedColors[6], selectedColors[3], selectedColors[4], selectedColors[5], selectedColors[6], selectedColors[7], selectedColors[8], selectedColors[9])
    write_line(fd, ROLLINBIT, selectedColors[6], selectedColors[6], selectedColors[6], selectedColors[3], selectedColors[4], selectedColors[5], selectedColors[6], selectedColors[7], selectedColors[8], selectedColors[9])
    write_line(fd, ROLLINBIT, selectedColors[6], selectedColors[1], selectedColors[6], selectedColors[3], selectedColors[4], selectedColors[5], selectedColors[6], selectedColors[7], selectedColors[8], selectedColors[9])
    write_line(fd, ROLLINBIT, selectedColors[6], selectedColors[1], selectedColors[2], selectedColors[3], selectedColors[4], selectedColors[5], selectedColors[6], selectedColors[7], selectedColors[8], selectedColors[9])
    write_line(fd, ROLLINBIT, selectedColors[0], selectedColors[1], selectedColors[2], selectedColors[3], selectedColors[4], selectedColors[5], selectedColors[6], selectedColors[7], selectedColors[8], selectedColors[9])
    return;

def makePacManRight(fd):
    dotsColor = [RED, GREEN, BLUE, YELLOW, CYAN, PINK, WHITE, ORANGE]
    selectedColors = [random.choice(dotsColor), random.choice(dotsColor), random.choice(dotsColor), random.choice(dotsColor), random.choice(dotsColor), random.choice(dotsColor), random.choice(dotsColor), random.choice(dotsColor), random.choice(dotsColor), random.choice(dotsColor)]
    write_line(fd, ROLLINBIT, selectedColors[0], selectedColors[1], selectedColors[2], selectedColors[3], selectedColors[4], selectedColors[5], selectedColors[6], selectedColors[7], selectedColors[8], selectedColors[9])
    write_line(fd, ROLLINBIT, selectedColors[0], selectedColors[1], selectedColors[2], selectedColors[3], selectedColors[4], selectedColors[5], selectedColors[6], selectedColors[7], selectedColors[9], selectedColors[9])
    write_line(fd, ROLLINBIT, selectedColors[0], selectedColors[1], selectedColors[2], selectedColors[3], selectedColors[4], selectedColors[5], selectedColors[6], selectedColors[9], selectedColors[9], selectedColors[9])
    write_line(fd, ROLLINBIT, selectedColors[0], selectedColors[1], selectedColors[2], selectedColors[3], selectedColors[4], selectedColors[5], selectedColors[9], selectedColors[9], selectedColors[9], selectedColors[9])
    write_line(fd, ROLLINBIT, selectedColors[0], selectedColors[1], selectedColors[2], selectedColors[9], selectedColors[4], selectedColors[5], selectedColors[9], selectedColors[9], selectedColors[9], selectedColors[9])
    write_line(fd, ROLLINBIT, selectedColors[0], selectedColors[1], selectedColors[2], selectedColors[9], selectedColors[9], selectedColors[5], selectedColors[9], selectedColors[9], selectedColors[9], selectedColors[9])
    write_line(fd, ROLLINBIT, selectedColors[0], selectedColors[1], selectedColors[2], selectedColors[9], selectedColors[9], selectedColors[9], selectedColors[9], selectedColors[9], selectedColors[9], selectedColors[9])
    write_line(fd, ROLLINBIT, selectedColors[0], selectedColors[1], selectedColors[9], selectedColors[9], selectedColors[9], selectedColors[9], selectedColors[9], selectedColors[9], selectedColors[9], selectedColors[9])
    write_line(fd, ROLLINBIT, selectedColors[0], selectedColors[9], selectedColors[9], selectedColors[9], selectedColors[9], selectedColors[9], selectedColors[9], selectedColors[9], selectedColors[9], selectedColors[9])
    write_line(fd, ROLLINBIT, selectedColors[9], selectedColors[9], selectedColors[9], selectedColors[9], selectedColors[9], selectedColors[9], selectedColors[9], selectedColors[9], selectedColors[9], selectedColors[9])
    write_line(fd, ROLLINBIT, selectedColors[9], selectedColors[9], selectedColors[9], selectedColors[9], selectedColors[9], selectedColors[9], selectedColors[9], selectedColors[9], selectedColors[8], selectedColors[9])
    write_line(fd, ROLLINBIT, selectedColors[9], selectedColors[9], selectedColors[9], selectedColors[9], selectedColors[9], selectedColors[9], selectedColors[9], selectedColors[7], selectedColors[8], selectedColors[9])
    write_line(fd, ROLLINBIT, selectedColors[9], selectedColors[9], selectedColors[9], selectedColors[9], selectedColors[9], selectedColors[9], selectedColors[6], selectedColors[7], selectedColors[8], selectedColors[9])
    write_line(fd, ROLLINBIT, selectedColors[9], selectedColors[9], selectedColors[9], selectedColors[3], selectedColors[9], selectedColors[9], selectedColors[6], selectedColors[7], selectedColors[8], selectedColors[9])
    write_line(fd, ROLLINBIT, selectedColors[9], selectedColors[9], selectedColors[9], selectedColors[3], selectedColors[4], selectedColors[9], selectedColors[6], selectedColors[7], selectedColors[8], selectedColors[9])
    write_line(fd, ROLLINBIT, selectedColors[9], selectedColors[9], selectedColors[9], selectedColors[3], selectedColors[4], selectedColors[5], selectedColors[6], selectedColors[7], selectedColors[8], selectedColors[9])
    write_line(fd, ROLLINBIT, selectedColors[9], selectedColors[9], selectedColors[2], selectedColors[3], selectedColors[4], selectedColors[5], selectedColors[6], selectedColors[7], selectedColors[8], selectedColors[9])
    write_line(fd, ROLLINBIT, selectedColors[9], selectedColors[1], selectedColors[2], selectedColors[3], selectedColors[4], selectedColors[5], selectedColors[6], selectedColors[7], selectedColors[8], selectedColors[9])
    write_line(fd, ROLLINBIT, selectedColors[0], selectedColors[1], selectedColors[2], selectedColors[3], selectedColors[4], selectedColors[5], selectedColors[6], selectedColors[7], selectedColors[8], selectedColors[9])
    return;

def makePacManTop(fd):
    dotsColor = [RED, GREEN, BLUE, YELLOW, CYAN, PINK, WHITE, ORANGE]
    selectedColors = [random.choice(dotsColor), random.choice(dotsColor), random.choice(dotsColor), random.choice(dotsColor), random.choice(dotsColor), random.choice(dotsColor), random.choice(dotsColor), random.choice(dotsColor), random.choice(dotsColor), random.choice(dotsColor)]
    write_line(fd, ROLLINBIT, selectedColors[0], selectedColors[1], selectedColors[2], selectedColors[3], selectedColors[4], selectedColors[5], selectedColors[6], selectedColors[7], selectedColors[8], selectedColors[9])
    write_line(fd, ROLLINBIT, selectedColors[0], selectedColors[0], selectedColors[2], selectedColors[3], selectedColors[4], selectedColors[5], selectedColors[6], selectedColors[7], selectedColors[8], selectedColors[9])
    write_line(fd, ROLLINBIT, selectedColors[0], selectedColors[0], selectedColors[0], selectedColors[3], selectedColors[4], selectedColors[5], selectedColors[6], selectedColors[7], selectedColors[8], selectedColors[9])
    write_line(fd, ROLLINBIT, selectedColors[0], selectedColors[0], selectedColors[0], selectedColors[3], selectedColors[4], selectedColors[0], selectedColors[6], selectedColors[7], selectedColors[8], selectedColors[9])
    write_line(fd, ROLLINBIT, selectedColors[0], selectedColors[0], selectedColors[0], selectedColors[3], selectedColors[0], selectedColors[0], selectedColors[6], selectedColors[7], selectedColors[8], selectedColors[9])
    write_line(fd, ROLLINBIT, selectedColors[0], selectedColors[0], selectedColors[0], selectedColors[0], selectedColors[0], selectedColors[0], selectedColors[6], selectedColors[7], selectedColors[8], selectedColors[9])
    write_line(fd, ROLLINBIT, selectedColors[0], selectedColors[0], selectedColors[0], selectedColors[0], selectedColors[0], selectedColors[0], selectedColors[0], selectedColors[7], selectedColors[8], selectedColors[9])
    write_line(fd, ROLLINBIT, selectedColors[0], selectedColors[0], selectedColors[0], selectedColors[0], selectedColors[0], selectedColors[0], selectedColors[0], selectedColors[0], selectedColors[8], selectedColors[9])
    write_line(fd, ROLLINBIT, selectedColors[0], selectedColors[0], selectedColors[0], selectedColors[0], selectedColors[0], selectedColors[0], selectedColors[0], selectedColors[0], selectedColors[0], selectedColors[9])
    write_line(fd, ROLLINBIT, selectedColors[0], selectedColors[0], selectedColors[0], selectedColors[0], selectedColors[0], selectedColors[0], selectedColors[0], selectedColors[0], selectedColors[0], selectedColors[0])
    write_line(fd, ROLLINBIT, selectedColors[0], selectedColors[1], selectedColors[0], selectedColors[0], selectedColors[0], selectedColors[0], selectedColors[0], selectedColors[0], selectedColors[0], selectedColors[0])
    write_line(fd, ROLLINBIT, selectedColors[0], selectedColors[1], selectedColors[2], selectedColors[0], selectedColors[0], selectedColors[0], selectedColors[0], selectedColors[0], selectedColors[0], selectedColors[0])
    write_line(fd, ROLLINBIT, selectedColors[0], selectedColors[1], selectedColors[2], selectedColors[0], selectedColors[0], selectedColors[5], selectedColors[0], selectedColors[0], selectedColors[0], selectedColors[0])
    write_line(fd, ROLLINBIT, selectedColors[0], selectedColors[1], selectedColors[2], selectedColors[0], selectedColors[4], selectedColors[5], selectedColors[0], selectedColors[0], selectedColors[0], selectedColors[0])
    write_line(fd, ROLLINBIT, selectedColors[0], selectedColors[1], selectedColors[2], selectedColors[3], selectedColors[4], selectedColors[5], selectedColors[0], selectedColors[0], selectedColors[0], selectedColors[0])
    write_line(fd, ROLLINBIT, selectedColors[0], selectedColors[1], selectedColors[2], selectedColors[3], selectedColors[4], selectedColors[5], selectedColors[6], selectedColors[0], selectedColors[0], selectedColors[0])
    write_line(fd, ROLLINBIT, selectedColors[0], selectedColors[1], selectedColors[2], selectedColors[3], selectedColors[4], selectedColors[5], selectedColors[6], selectedColors[7], selectedColors[0], selectedColors[0])
    write_line(fd, ROLLINBIT, selectedColors[0], selectedColors[1], selectedColors[2], selectedColors[3], selectedColors[4], selectedColors[5], selectedColors[6], selectedColors[7], selectedColors[8], selectedColors[0])
    write_line(fd, ROLLINBIT, selectedColors[0], selectedColors[1], selectedColors[2], selectedColors[3], selectedColors[4], selectedColors[5], selectedColors[6], selectedColors[7], selectedColors[8], selectedColors[9])
    return;

def makeFallingDots(fd):
    dotsColor = [RED, GREEN, BLUE, YELLOW, CYAN, PINK, WHITE, ORANGE]
    selectedColors = [random.choice(dotsColor), random.choice(dotsColor), random.choice(dotsColor), random.choice(dotsColor), random.choice(dotsColor), random.choice(dotsColor), random.choice(dotsColor), random.choice(dotsColor), random.choice(dotsColor), random.choice(dotsColor)]
    write_line(fd, INOUTBIT, selectedColors[9], BLACK, BLACK, BLACK, BLACK, BLACK, BLACK, BLACK, BLACK, BLACK)
    write_line(fd, INOUTBIT, BLACK, BLACK, selectedColors[9], BLACK, BLACK, BLACK, BLACK, BLACK, BLACK, BLACK)
    write_line(fd, INOUTBIT, BLACK, BLACK, BLACK, BLACK, BLACK, selectedColors[9], BLACK, BLACK, BLACK, BLACK)
    write_line(fd, INOUTBIT, BLACK, BLACK, BLACK, BLACK, BLACK, BLACK, BLACK, BLACK, BLACK, selectedColors[9])
    write_line(fd, INOUTBIT, selectedColors[8], BLACK, BLACK, BLACK, BLACK, BLACK, BLACK, BLACK, BLACK, selectedColors[9])
    write_line(fd, INOUTBIT, BLACK, BLACK, selectedColors[8], BLACK, BLACK, BLACK, BLACK, BLACK, BLACK, selectedColors[9])
    write_line(fd, INOUTBIT, BLACK, BLACK, BLACK, BLACK, selectedColors[8], BLACK, BLACK, BLACK, BLACK, selectedColors[9])
    write_line(fd, INOUTBIT, BLACK, BLACK, BLACK, BLACK, BLACK, BLACK, BLACK, BLACK, selectedColors[8], selectedColors[9])
    write_line(fd, INOUTBIT, selectedColors[7], BLACK, BLACK, BLACK, BLACK, BLACK, BLACK, BLACK, selectedColors[8], selectedColors[9])
    write_line(fd, INOUTBIT, BLACK, selectedColors[7], BLACK, BLACK, BLACK, BLACK, BLACK, BLACK, selectedColors[8], selectedColors[9])
    write_line(fd, INOUTBIT, BLACK, BLACK, BLACK, BLACK, selectedColors[7], BLACK, BLACK, BLACK, selectedColors[8], selectedColors[9])
    write_line(fd, INOUTBIT, BLACK, BLACK, BLACK, BLACK, BLACK, BLACK, BLACK, selectedColors[7], selectedColors[8], selectedColors[9])
    write_line(fd, INOUTBIT, selectedColors[6], BLACK, BLACK, BLACK, BLACK, BLACK, BLACK, selectedColors[7], selectedColors[8], selectedColors[9])
    write_line(fd, INOUTBIT, BLACK, selectedColors[6], BLACK, BLACK, BLACK, BLACK, BLACK, selectedColors[7], selectedColors[8], selectedColors[9])
    write_line(fd, INOUTBIT, BLACK, BLACK, BLACK, selectedColors[6], BLACK, BLACK, BLACK, selectedColors[7], selectedColors[8], selectedColors[9])
    write_line(fd, INOUTBIT, BLACK, BLACK, BLACK, BLACK, BLACK, BLACK, selectedColors[6], selectedColors[7], selectedColors[8], selectedColors[9])
    write_line(fd, INOUTBIT, selectedColors[5], BLACK, BLACK, BLACK, BLACK, BLACK, selectedColors[6], selectedColors[7], selectedColors[8], selectedColors[9])
    write_line(fd, INOUTBIT, BLACK, BLACK, selectedColors[5], BLACK, BLACK, BLACK, selectedColors[6], selectedColors[7], selectedColors[8], selectedColors[9])
    write_line(fd, INOUTBIT, BLACK, BLACK, BLACK, BLACK, BLACK, selectedColors[5], selectedColors[6], selectedColors[7], selectedColors[8], selectedColors[9])
    write_line(fd, INOUTBIT, selectedColors[4], BLACK, BLACK, BLACK, BLACK, selectedColors[5], selectedColors[6], selectedColors[7], selectedColors[8], selectedColors[9])
    write_line(fd, INOUTBIT, BLACK, selectedColors[4], BLACK, BLACK, BLACK, selectedColors[5], selectedColors[6], selectedColors[7], selectedColors[8], selectedColors[9])
    write_line(fd, INOUTBIT, BLACK, BLACK, BLACK, BLACK, selectedColors[4], selectedColors[5], selectedColors[6], selectedColors[7], selectedColors[8], selectedColors[9])
    write_line(fd, INOUTBIT, selectedColors[3], BLACK, BLACK, BLACK, selectedColors[4], selectedColors[5], selectedColors[6], selectedColors[7], selectedColors[8], selectedColors[9])
    write_line(fd, INOUTBIT, BLACK, selectedColors[3], BLACK, BLACK, selectedColors[4], selectedColors[5], selectedColors[6], selectedColors[7], selectedColors[8], selectedColors[9])
    write_line(fd, INOUTBIT, BLACK, BLACK, BLACK, selectedColors[3], selectedColors[4], selectedColors[5], selectedColors[6], selectedColors[7], selectedColors[8], selectedColors[9])
    write_line(fd, INOUTBIT, selectedColors[2], BLACK, BLACK, selectedColors[3], selectedColors[4], selectedColors[5], selectedColors[6], selectedColors[7], selectedColors[8], selectedColors[9])
    write_line(fd, INOUTBIT, BLACK, BLACK, selectedColors[2], selectedColors[3], selectedColors[4], selectedColors[5], selectedColors[6], selectedColors[7], selectedColors[8], selectedColors[9])
    write_line(fd, INOUTBIT, selectedColors[1], BLACK, selectedColors[2], selectedColors[3], selectedColors[4], selectedColors[5], selectedColors[6], selectedColors[7], selectedColors[8], selectedColors[9])
    write_line(fd, INOUTBIT, BLACK, selectedColors[1], selectedColors[2], selectedColors[3], selectedColors[4], selectedColors[5], selectedColors[6], selectedColors[7], selectedColors[8], selectedColors[9])
    write_line(fd, INOUTBIT, selectedColors[0], selectedColors[1], selectedColors[2], selectedColors[3], selectedColors[4], selectedColors[5], selectedColors[6], selectedColors[7], selectedColors[8], selectedColors[9])
    line_delay(fd, 1)
    return;

if __name__ == "__main__":
    for j in range (1,11) :
      fileName = './makeRandomDots' + str(j) + '.dat'
      fd = open(fileName, 'wb')
      for i in range (1, 61) :
          makeRandomDots(fd)
      fd.close()

    fd = open('./makePacManTop.dat', 'wb')
    for i in range (1, 3) :
        makePacManTop(fd)
    fd.close()

    fd = open('./makePacManLeft.dat', 'wb')
    for i in range (1, 3) :
        makePacManLeft(fd)
    fd.close()

    fd = open('./makePacManRight.dat', 'wb')
    for i in range (1, 3) :
        makePacManRight(fd)
    fd.close()

    for j in range (1,11) :
      fileName = './makeFallingDots' + str(j) + '.dat'
      fd = open(fileName, 'wb')
      for i in range (1, 3) :
          makeFallingDots(fd)
      fd.close()
