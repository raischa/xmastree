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

TRUE = 1
FALSE = 0

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

def checkNotCorned(runnerDot, chaserDot1, chaserDot2) :
    tmp = TRUE;
    if (runnerDot == 0) and (chaserDot1 == 1) and (chaserDot2 == 2) : tmp = FALSE
    if (runnerDot == 0) and (chaserDot1 == 2) and (chaserDot2 == 1) : tmp = FALSE
    if (runnerDot == 6) and (chaserDot1 == 3) and (chaserDot2 == 7) : tmp = FALSE
    if (runnerDot == 6) and (chaserDot1 == 7) and (chaserDot2 == 3) : tmp = FALSE
    if (runnerDot == 9) and (chaserDot1 == 5) and (chaserDot2 == 8) : tmp = FALSE
    if (runnerDot == 9) and (chaserDot1 == 8) and (chaserDot2 == 5) : tmp = FALSE   
    return tmp;

def moveRunner(runnerDot, chaserDot1, chaserDot2) :
    if runnerDot == 0 :
      options = [1,2]
      try :
        options.remove(chaserDot1)
      except ValueError :
        pass
      try: 
        options.remove(chaserDot2)
      except ValueError :
        pass
      newDot = random.choice(options)
    if runnerDot == 1 :
      options = [0, 2, 3, 4]
      try :
        options.remove(chaserDot1)
      except ValueError :
        pass
      try: 
        options.remove(chaserDot2)
      except ValueError :
        pass
      newDot = random.choice(options)
    if runnerDot == 2 :
      options = [0, 1, 4, 5]
      try :
        options.remove(chaserDot1)
      except ValueError :
        pass
      try: 
        options.remove(chaserDot2)
      except ValueError :
        pass
      newDot = random.choice(options)
    if runnerDot == 3 :
      options = [2, 4, 6, 7]
      try :
        options.remove(chaserDot1)
      except ValueError :
        pass
      try: 
        options.remove(chaserDot2)
      except ValueError :
        pass
      newDot = random.choice(options)
    if runnerDot == 4 :
      options = [1, 2, 3, 5, 7, 8]
      try :
        options.remove(chaserDot1)
      except ValueError :
        pass
      try: 
        options.remove(chaserDot2)
      except ValueError :
        pass
      newDot = random.choice(options)
    if runnerDot == 5 :
      options = [2, 4, 8, 9]
      try :
        options.remove(chaserDot1)
      except ValueError :
        pass
      try: 
        options.remove(chaserDot2)
      except ValueError :
        pass
      newDot = random.choice(options)
    if runnerDot == 6 :
      options = [3, 7]
      try :
        options.remove(chaserDot1)
      except ValueError :
        pass
      try: 
        options.remove(chaserDot2)
      except ValueError :
        pass
      newDot = random.choice(options)
    if runnerDot == 7 :
      options = [3, 4, 6, 8]
      try :
        options.remove(chaserDot1)
      except ValueError :
        pass
      try: 
        options.remove(chaserDot2)
      except ValueError :
        pass
      newDot = random.choice(options)
    if runnerDot == 8 :
      options = [4, 5, 7, 9]
      try :
        options.remove(chaserDot1)
      except ValueError :
        pass
      try: 
        options.remove(chaserDot2)
      except ValueError :
        pass
      newDot = random.choice(options)
    if runnerDot == 9 :
      options = [5, 8]
      try :
        options.remove(chaserDot1)
      except ValueError :
        pass
      try: 
        options.remove(chaserDot2)
      except ValueError :
        pass
      newDot = random.choice(options)
    return newDot;

def moveChaserDot1(runnerDot, chaserDot1, chaserDot2) :
    if chaserDot1 == 0 :
      options = [0,1,2]
      try :
        options.remove(runnerDot)
      except ValueError :
        pass
      try: 
        options.remove(chaserDot2)
      except ValueError :
        pass
      newDot = random.choice(options)
    if chaserDot1 == 1 :
      options = [0, 1, 2, 3, 4]
      if runnerDot > 2 :
        options.remove(0)
        options.remove(2)
      try :
        options.remove(runnerDot)
      except ValueError :
        pass
      try: 
        options.remove(chaserDot2)
      except ValueError :
        pass
      newDot = random.choice(options)
    if chaserDot1 == 2 :
      options = [0, 2, 1, 4, 5]
      if runnerDot > 2 :
        options.remove(0)
        options.remove(1)
      try :
        options.remove(runnerDot)
      except ValueError :
        pass
      try: 
        options.remove(chaserDot2)
      except ValueError :
        pass
      newDot = random.choice(options)
    if chaserDot1 == 3 :
      options = [2, 3, 4, 6, 7]
      if (runnerDot != 6) or (runnerDot != 7) :
        options.remove(6)
        options.remove(7)
      try :
        options.remove(runnerDot)
      except ValueError :
        pass
      try: 
        options.remove(chaserDot2)
      except ValueError :
        pass
      newDot = random.choice(options)
    if chaserDot1 == 4 :
      options = [1, 2, 3, 4, 5, 7, 8]
      if (runnerDot == 0) or (runnerDot == 1) or (runnerDot == 2) :
        options.remove(7)
        options.remove(8)
      if (runnerDot == 3) or (runnerDot == 6) or (runnerDot == 7) :
        options.remove(2)
        options.remove(5)
      if (runnerDot == 5) or (runnerDot == 8) or (runnerDot == 9) :
        options.remove(1)
        options.remove(7)
      try :
        options.remove(runnerDot)
      except ValueError :
        pass
      try: 
        options.remove(chaserDot2)
      except ValueError :
        pass
      newDot = random.choice(options)
    if chaserDot1 == 5 :
      options = [2, 4, 5, 8, 9]
      if (runnerDot != 8) or (runnerDot != 9) :
        options.remove(8)
        options.remove(9)
      try :
        options.remove(runnerDot)
      except ValueError :
        pass
      try: 
        options.remove(chaserDot2)
      except ValueError :
        pass
      newDot = random.choice(options)
    if chaserDot1 == 6 :
      options = [3, 6, 7]
      try :
        options.remove(runnerDot)
      except ValueError :
        pass
      try: 
        options.remove(chaserDot2)
      except ValueError :
        pass
      newDot = random.choice(options)
    if chaserDot1 == 7 :
      options = [3, 4, 6, 7, 8]
      if (runnerDot != 3) or (runnerDot != 6) :
        options.remove(3)
        options.remove(6)
      try :
        options.remove(runnerDot)
      except ValueError :
        pass
      try: 
        options.remove(chaserDot2)
      except ValueError :
        pass
      newDot = random.choice(options)
    if chaserDot1 == 8 :
      options = [4, 5, 7, 8, 9]
      if (runnerDot != 5) or (runnerDot != 9) :
        options.remove(5)
        options.remove(9)
      try :
        options.remove(chaserDot1)
      except ValueError :
        pass
      try: 
        options.remove(chaserDot2)
      except ValueError :
        pass
      newDot = random.choice(options)
    if chaserDot1 == 9 :
      options = [5, 8, 9]
      try :
        options.remove(runnerDot)
      except ValueError :
        pass
      try: 
        options.remove(chaserDot2)
      except ValueError :
        pass
      newDot = random.choice(options)
    return newDot;

def moveChaserDot2(runnerDot, chaserDot1, chaserDot2) :
    if chaserDot2 == 0 :
      options = [0, 1,2]
      try :
        options.remove(runnerDot)
      except ValueError :
        pass
      try: 
        options.remove(chaserDot1)
      except ValueError :
        pass
      newDot = random.choice(options)
    if chaserDot2 == 1 :
      options = [0, 1, 2, 3, 4]
      if runnerDot > 2 :
        options.remove(0)
        options.remove(2)
      try :
        options.remove(runnerDot)
      except ValueError :
        pass
      try: 
        options.remove(chaserDot1)
      except ValueError :
        pass
      newDot = random.choice(options)
    if chaserDot2 == 2 :
      options = [0, 1, 2, 4, 5]
      if runnerDot > 2 :
        options.remove(0)
        options.remove(1)
      try :
        options.remove(runnerDot)
      except ValueError :
        pass
      try: 
        options.remove(chaserDot1)
      except ValueError :
        pass
      newDot = random.choice(options)
    if chaserDot2 == 3 :
      options = [2, 3, 4, 6, 7]
      if (runnerDot != 6) or (runnerDot != 7) :
        options.remove(6)
        options.remove(7)
      try :
        options.remove(runnerDot)
      except ValueError :
        pass
      try: 
        options.remove(chaserDot1)
      except ValueError :
        pass
      newDot = random.choice(options)
    if chaserDot2 == 4 :
      options = [1, 2, 3, 4, 5, 7, 8]
      if (runnerDot == 0) or (runnerDot == 1) or (runnerDot == 2) :
        options.remove(7)
        options.remove(8)
      if (runnerDot == 3) or (runnerDot == 6) or (runnerDot == 7) :
        options.remove(2)
        options.remove(5)
      if (runnerDot == 5) or (runnerDot == 8) or (runnerDot == 9) :
        options.remove(1)
        options.remove(7)
      try :
        options.remove(runnerDot)
      except ValueError :
        pass
      try: 
        options.remove(chaserDot1)
      except ValueError :
        pass
      newDot = random.choice(options)
    if chaserDot2 == 5 :
      options = [2, 4, 5, 8, 9]
      if (runnerDot != 8) or (runnerDot != 9) :
        options.remove(8)
        options.remove(9)
      try :
        options.remove(runnerDot)
      except ValueError :
        pass
      try: 
        options.remove(chaserDot1)
      except ValueError :
        pass
      newDot = random.choice(options)
    if chaserDot2 == 6 :
      options = [3, 6, 7]
      try :
        options.remove(runnerDot)
      except ValueError :
        pass
      try: 
        options.remove(chaserDot1)
      except ValueError :
        pass
      newDot = random.choice(options)
    if chaserDot2 == 7 :
      options = [3, 4, 6, 7, 8]
      if (runnerDot != 3) or (runnerDot != 6) :
        options.remove(3)
        options.remove(6)
      try :
        options.remove(runnerDot)
      except ValueError :
        pass
      try: 
        options.remove(chaserDot1)
      except ValueError :
        pass
      newDot = random.choice(options)
    if chaserDot2 == 8 :
      options = [4, 5, 7, 8, 9]
      if (runnerDot != 5) or (runnerDot != 9) :
        options.remove(5)
        options.remove(9)
      try :
        options.remove(chaserDot1)
      except ValueError :
        pass
      try: 
        options.remove(chaserDot1)
      except ValueError :
        pass
      newDot = random.choice(options)
    if chaserDot2 == 9 :
      options = [5, 8, 9]
      try :
        options.remove(runnerDot)
      except ValueError :
        pass
      try: 
        options.remove(chaserDot1)
      except ValueError :
        pass
      newDot = random.choice(options)
    return newDot;
  
def makeRunningDots(fd):
    dotsColor = [RED, GREEN, BLUE, PINK, WHITE, ORANGE]
    currentDots = [BLACK, BLACK, BLACK, BLACK, BLACK, BLACK, BLACK, BLACK, BLACK, BLACK]
    newDots = [BLACK, BLACK, BLACK, BLACK, BLACK, BLACK, BLACK, BLACK, BLACK, BLACK]
    runnerDotColor = random.choice(dotsColor)
    dotsColor.remove(runnerDotColor)
    chaserDotColor = random.choice(dotsColor)
    runnerDot = random.randint(0,9)
    chaserDot1 = random.randint(0,9)
    chaserDot2 = random.randint(0,9)
    currentDots[runnerDot] = runnerDotColor
    currentDots[chaserDot1] = chaserDotColor
    currentDots[chaserDot2] = chaserDotColor
    write_line(fd, 0, currentDots[0], currentDots[1], currentDots[2], currentDots[3], currentDots[4], currentDots[5], currentDots[6], currentDots[7], currentDots[8], currentDots[9])
    while checkNotCorned(runnerDot, chaserDot1, chaserDot2) :
      currentDots[runnerDot] = BLACK
      write_line(fd, 0, currentDots[0], currentDots[1], currentDots[2], currentDots[3], currentDots[4], currentDots[5], currentDots[6], currentDots[7], currentDots[8], currentDots[9])
      runnerDot = moveRunner(runnerDot, chaserDot1, chaserDot2)
      currentDots[runnerDot] = runnerDotColor
      write_line(fd, 0, currentDots[0], currentDots[1], currentDots[2], currentDots[3], currentDots[4], currentDots[5], currentDots[6], currentDots[7], currentDots[8], currentDots[9])
      currentDots[chaserDot1] = BLACK
      write_line(fd, 0, currentDots[0], currentDots[1], currentDots[2], currentDots[3], currentDots[4], currentDots[5], currentDots[6], currentDots[7], currentDots[8], currentDots[9])
      chaserDot1 = moveChaserDot1(runnerDot, chaserDot1, chaserDot2)
      currentDots[chaserDot1] = chaserDotColor
      write_line(fd, 0, currentDots[0], currentDots[1], currentDots[2], currentDots[3], currentDots[4], currentDots[5], currentDots[6], currentDots[7], currentDots[8], currentDots[9])
      currentDots[chaserDot2] = BLACK
      write_line(fd, 0, currentDots[0], currentDots[1], currentDots[2], currentDots[3], currentDots[4], currentDots[5], currentDots[6], currentDots[7], currentDots[8], currentDots[9])
      chaserDot2 = moveChaserDot2(runnerDot, chaserDot1, chaserDot2)
      currentDots[chaserDot2] = chaserDotColor
      write_line(fd, 0, currentDots[0], currentDots[1], currentDots[2], currentDots[3], currentDots[4], currentDots[5], currentDots[6], currentDots[7], currentDots[8], currentDots[9])

    for j in range (1,4) : 
      currentDots[runnerDot] = BLACK
      write_line(fd, INOUTBIT, currentDots[0], currentDots[1], currentDots[2], currentDots[3], currentDots[4], currentDots[5], currentDots[6], currentDots[7], currentDots[8], currentDots[9])
      line_delay(fd, 1)
      currentDots[runnerDot] = runnerDotColor
      write_line(fd, INOUTBIT, currentDots[0], currentDots[1], currentDots[2], currentDots[3], currentDots[4], currentDots[5], currentDots[6], currentDots[7], currentDots[8], currentDots[9])
      line_delay(fd, 1)
    write_line(fd, PULSINGBIT, currentDots[0], currentDots[1], currentDots[2], currentDots[3], currentDots[4], currentDots[5], currentDots[6], currentDots[7], currentDots[8], currentDots[9])
    return;

if __name__ == "__main__":

    for j in range (1,11) :
      fileName = './makeRunningDots' + str(j) + '.dat'
      fd = open(fileName, 'wb')
      for i in range (1, 2) :
          makeRunningDots(fd)
      fd.close()
