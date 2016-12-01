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

dotsColor = [RED, GREEN, BLUE, YELLOW, CYAN, PINK, WHITE, ORANGE]

FALSE = 0
TRUE = 1

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

def duplicatesExists(currentSet):
    tmp = FALSE
    if (currentSet[0] == currentSet[1]) : tmp = TRUE
    if (currentSet[0] == currentSet[2]) : tmp = TRUE
    if (currentSet[1] == currentSet[2]) : tmp = TRUE
    if (currentSet[1] == currentSet[3]) : tmp = TRUE
    if (currentSet[1] == currentSet[4]) : tmp = TRUE
    if (currentSet[2] == currentSet[4]) : tmp = TRUE
    if (currentSet[2] == currentSet[5]) : tmp = TRUE
    if (currentSet[3] == currentSet[4]) : tmp = TRUE
    if (currentSet[3] == currentSet[6]) : tmp = TRUE
    if (currentSet[3] == currentSet[7]) : tmp = TRUE
    if (currentSet[4] == currentSet[5]) : tmp = TRUE
    if (currentSet[4] == currentSet[7]) : tmp = TRUE
    if (currentSet[4] == currentSet[8]) : tmp = TRUE
    if (currentSet[5] == currentSet[8]) : tmp = TRUE
    if (currentSet[5] == currentSet[9]) : tmp = TRUE
    if (currentSet[6] == currentSet[7]) : tmp = TRUE
    if (currentSet[7] == currentSet[8]) : tmp = TRUE
    if (currentSet[8] == currentSet[9]) : tmp = TRUE
    return tmp;

def removeDuplicates(currentSet):
    newSet = [RED, RED, RED, RED, RED, RED, RED, RED, RED, RED]
    for i in range (0,10):
      newSet[i] = currentSet[i]

    if (currentSet[0] == currentSet[1]) :
        newSet[0] = BLACK
        newSet[1] = BLACK
    if (currentSet[0] == currentSet[2]) :
        newSet[0] = BLACK
        newSet[2] = BLACK
    if (currentSet[1] == currentSet[2]) :
        newSet[1] = BLACK
        newSet[2] = BLACK
    if (currentSet[1] == currentSet[3]) :
        newSet[1] = BLACK
        newSet[3] = BLACK
    if (currentSet[1] == currentSet[4]) :
        newSet[1] = BLACK
        newSet[4] = BLACK
    if (currentSet[2] == currentSet[4]) :
        newSet[2] = BLACK
        newSet[4] = BLACK
    if (currentSet[2] == currentSet[5]) :
        newSet[2] = BLACK
        newSet[5] = BLACK
    if (currentSet[3] == currentSet[4]) :
        newSet[3] = BLACK
        newSet[4] = BLACK
    if (currentSet[3] == currentSet[6]) :
        newSet[3] = BLACK
        newSet[6] = BLACK
    if (currentSet[3] == currentSet[7]) :
        newSet[3] = BLACK
        newSet[7] = BLACK
    if (currentSet[4] == currentSet[5]) :
        newSet[4] = BLACK
        newSet[5] = BLACK
    if (currentSet[4] == currentSet[7]) :
        newSet[4] = BLACK
        newSet[7] = BLACK
    if (currentSet[4] == currentSet[8]) :
        newSet[4] = BLACK
        newSet[8] = BLACK
    if (currentSet[5] == currentSet[8]) :
        newSet[5] = BLACK
        newSet[8] = BLACK
    if (currentSet[5] == currentSet[9]) :
        newSet[5] = BLACK
        newSet[9] = BLACK
    if (currentSet[6] == currentSet[7]) :
        newSet[6] = BLACK
        newSet[7] = BLACK
    if (currentSet[7] == currentSet[8]) :
        newSet[7] = BLACK
        newSet[8] = BLACK
    if (currentSet[8] == currentSet[9]) :
        newSet[8] = BLACK
        newSet[9] = BLACK
    return newSet;

def checkDotsBlack(newSet):
    tmp = FALSE
    if (newSet[0] == BLACK) : tmp = TRUE
    if (newSet[1] == BLACK) : tmp = TRUE
    if (newSet[2] == BLACK) : tmp = TRUE
    if (newSet[3] == BLACK) : tmp = TRUE
    if (newSet[4] == BLACK) : tmp = TRUE
    if (newSet[5] == BLACK) : tmp = TRUE
    if (newSet[6] == BLACK) : tmp = TRUE
    if (newSet[7] == BLACK) : tmp = TRUE
    if (newSet[8] == BLACK) : tmp = TRUE
    if (newSet[9] == BLACK) : tmp = TRUE
    return tmp;

def moveDots(currentSet):
#move dots down as soon as new hole (BLACK) is found
# add a new random color at top
    dotsColor = [RED, GREEN, BLUE, YELLOW, CYAN, PINK, WHITE, ORANGE]
    newSet = currentSet
    if newSet[0] == BLACK :
        newSet[0] = random.choice(dotsColor)
    else :
      if newSet[1] == BLACK :
         newSet[1] = currentSet[0]
         newSet[0] = BLACK
         write_line(fd, 0, newSet[0], newSet[1], newSet[2], newSet[3], newSet[4], newSet[5], newSet[6], newSet[7], newSet[8], newSet[9])
         line_delay(fd,1)
         newSet[0] = random.choice(dotsColor)
      else :
        if newSet[2] == BLACK :
           newSet[2] = currentSet[0]
           newSet[0] = BLACK
           write_line(fd, 0, newSet[0], newSet[1], newSet[2], newSet[3], newSet[4], newSet[5], newSet[6], newSet[7], newSet[8], newSet[9])
           line_delay(fd,1)
           newSet[0] = random.choice(dotsColor)
        else :
          if newSet[3] == BLACK :
             newSet[3] = currentSet[1]
             newSet[1] = BLACK
             write_line(fd, 0, newSet[0], newSet[1], newSet[2], newSet[3], newSet[4], newSet[5], newSet[6], newSet[7], newSet[8], newSet[9])
             line_delay(fd,1)
             newSet[1] = currentSet[0]
             newSet[0] = BLACK
             write_line(fd, 0, newSet[0], newSet[1], newSet[2], newSet[3], newSet[4], newSet[5], newSet[6], newSet[7], newSet[8], newSet[9])
             line_delay(fd,1)
             newSet[0] = random.choice(dotsColor)
          else :
            if newSet[4] == BLACK :
               newSet[4] = currentSet[1]
               newSet[1] = BLACK
               write_line(fd, 0, newSet[0], newSet[1], newSet[2], newSet[3], newSet[4], newSet[5], newSet[6], newSet[7], newSet[8], newSet[9])
               line_delay(fd,1)
               newSet[1] = currentSet[0]
               newSet[0] = BLACK
               write_line(fd, 0, newSet[0], newSet[1], newSet[2], newSet[3], newSet[4], newSet[5], newSet[6], newSet[7], newSet[8], newSet[9])
               line_delay(fd,1)
               newSet[0] = random.choice(dotsColor)
            else :
              if newSet[5] == BLACK :
                 newSet[5] = currentSet[2]
                 newSet[2] = BLACK
                 write_line(fd, 0, newSet[0], newSet[1], newSet[2], newSet[3], newSet[4], newSet[5], newSet[6], newSet[7], newSet[8], newSet[9])
                 line_delay(fd,1)
                 newSet[2] = currentSet[0]
                 newSet[0] = BLACK
                 write_line(fd, 0, newSet[0], newSet[1], newSet[2], newSet[3], newSet[4], newSet[5], newSet[6], newSet[7], newSet[8], newSet[9])
                 line_delay(fd,1)
                 newSet[0] = random.choice(dotsColor)
              else :
                if newSet[6] == BLACK :
                   newSet[6] = currentSet[3]
                   newSet[3] = BLACK
                   write_line(fd, 0, newSet[0], newSet[1], newSet[2], newSet[3], newSet[4], newSet[5], newSet[6], newSet[7], newSet[8], newSet[9])
                   line_delay(fd,1)
                   newSet[3] = currentSet[1]
                   newSet[1] = BLACK
                   write_line(fd, 0, newSet[0], newSet[1], newSet[2], newSet[3], newSet[4], newSet[5], newSet[6], newSet[7], newSet[8], newSet[9])
                   line_delay(fd,1)
                   newSet[1] = currentSet[0]
                   newSet[0] = BLACK
                   write_line(fd, 0, newSet[0], newSet[1], newSet[2], newSet[3], newSet[4], newSet[5], newSet[6], newSet[7], newSet[8], newSet[9])
                   line_delay(fd,1)
                   newSet[0] = random.choice(dotsColor)
                else :
                  if newSet[7] == BLACK :
                     newSet[7] = currentSet[4]
                     newSet[4] = BLACK
                     write_line(fd, 0, newSet[0], newSet[1], newSet[2], newSet[3], newSet[4], newSet[5], newSet[6], newSet[7], newSet[8], newSet[9])
                     line_delay(fd,1)
                     newSet[4] = currentSet[1]
                     newSet[1] = BLACK
                     write_line(fd, 0, newSet[0], newSet[1], newSet[2], newSet[3], newSet[4], newSet[5], newSet[6], newSet[7], newSet[8], newSet[9])
                     line_delay(fd,1)
                     newSet[1] = currentSet[0]
                     newSet[0] = BLACK
                     write_line(fd, 0, newSet[0], newSet[1], newSet[2], newSet[3], newSet[4], newSet[5], newSet[6], newSet[7], newSet[8], newSet[9])
                     line_delay(fd,1)
                     newSet[0] = random.choice(dotsColor)
                  else :
                    if newSet[8] == BLACK :
                       newSet[8] = currentSet[4]
                       newSet[4] = BLACK
                       write_line(fd, 0, newSet[0], newSet[1], newSet[2], newSet[3], newSet[4], newSet[5], newSet[6], newSet[7], newSet[8], newSet[9])
                       line_delay(fd,1)
                       newSet[4] = currentSet[2]
                       newSet[2] = BLACK
                       write_line(fd, 0, newSet[0], newSet[1], newSet[2], newSet[3], newSet[4], newSet[5], newSet[6], newSet[7], newSet[8], newSet[9])
                       line_delay(fd,1)
                       newSet[2] = currentSet[0]
                       newSet[0] = BLACK
                       write_line(fd, 0, newSet[0], newSet[1], newSet[2], newSet[3], newSet[4], newSet[5], newSet[6], newSet[7], newSet[8], newSet[9])
                       line_delay(fd,1)
                       newSet[0] = random.choice(dotsColor)
                    else :
                      if newSet[9] == BLACK :
                         newSet[9] = currentSet[5]
                         newSet[5] = BLACK
                         write_line(fd, 0, newSet[0], newSet[1], newSet[2], newSet[3], newSet[4], newSet[5], newSet[6], newSet[7], newSet[8], newSet[9])
                         line_delay(fd,1)
                         newSet[5] = currentSet[2]
                         newSet[2] = BLACK
                         write_line(fd, 0, newSet[0], newSet[1], newSet[2], newSet[3], newSet[4], newSet[5], newSet[6], newSet[7], newSet[8], newSet[9])
                         line_delay(fd,1)
                         newSet[2] = currentSet[0]
                         newSet[0] = BLACK
                         write_line(fd, 0, newSet[0], newSet[1], newSet[2], newSet[3], newSet[4], newSet[5], newSet[6], newSet[7], newSet[8], newSet[9])
                         line_delay(fd,1)
                         newSet[0] = random.choice(dotsColor)

    write_line(fd, 0, newSet[0], newSet[1], newSet[2], newSet[3], newSet[4], newSet[5], newSet[6], newSet[7], newSet[8], newSet[9])
    line_delay(fd,1)

    return newSet;

def rearangeDots(fd, newSet):
    while (checkDotsBlack(newSet)):
        newSet = moveDots(newSet)
    return newSet;

def removeOneDot(newSet):
# somehow tmpSet = newSet does not works.  
    tmpSet = [RED, RED, RED, RED, RED, RED, RED, RED, RED, RED]
    for i in range (0,10):
      tmpSet[i] = newSet[i]
 
    tmpSet[random.randint(6,9)] = BLACK
    return tmpSet;

if __name__ == "__main__":

# Initialize these 2 structures

    for j in range (1,21) :
      fileName = './candycrush' + str(j) + '.dat'
      fd = open(fileName, 'wb')

      currentSet = [random.choice(dotsColor), random.choice(dotsColor), random.choice(dotsColor), random.choice(dotsColor), random.choice(dotsColor), random.choice(dotsColor), random.choice(dotsColor), random.choice(dotsColor), random.choice(dotsColor), random.choice(dotsColor)]
      newSet = currentSet
      write_line(fd, 0, currentSet[0], currentSet[1], currentSet[2], currentSet[3], currentSet[4], currentSet[5], currentSet[6], currentSet[7], currentSet[8], currentSet[9])
      line_delay(fd,1)
      for i in range (1, 11) :
          while duplicatesExists(currentSet):
              newSet = removeDuplicates(currentSet)
              # flash the holes (BLACK)
              write_line(fd, 0, currentSet[0], currentSet[1], currentSet[2], currentSet[3], currentSet[4], currentSet[5], currentSet[6], currentSet[7], currentSet[8], currentSet[9])
              line_delay(fd,1)
              write_line(fd, 0, newSet[0], newSet[1], newSet[2], newSet[3], newSet[4], newSet[5], newSet[6], newSet[7], newSet[8], newSet[9])
              line_delay(fd,1)
              write_line(fd, 0, currentSet[0], currentSet[1], currentSet[2], currentSet[3], currentSet[4], currentSet[5], currentSet[6], currentSet[7], currentSet[8], currentSet[9])
              line_delay(fd,1)
              write_line(fd, 0, newSet[0], newSet[1], newSet[2], newSet[3], newSet[4], newSet[5], newSet[6], newSet[7], newSet[8], newSet[9])
              line_delay(fd,1)
              write_line(fd, 0, currentSet[0], currentSet[1], currentSet[2], currentSet[3], currentSet[4], currentSet[5], currentSet[6], currentSet[7], currentSet[8], currentSet[9])
              line_delay(fd,1)
              write_line(fd, 0, newSet[0], newSet[1], newSet[2], newSet[3], newSet[4], newSet[5], newSet[6], newSet[7], newSet[8], newSet[9])
              line_delay(fd,1)
              currentSet = rearangeDots(fd, newSet)
          newSet = removeOneDot(newSet)
          # flash the hole (BLACK)
          write_line(fd, 0, currentSet[0], currentSet[1], currentSet[2], currentSet[3], currentSet[4], currentSet[5], currentSet[6], currentSet[7], currentSet[8], currentSet[9])
          line_delay(fd,1)
          write_line(fd, 0, newSet[0], newSet[1], newSet[2], newSet[3], newSet[4], newSet[5], newSet[6], newSet[7], newSet[8], newSet[9])
          line_delay(fd,1)
          write_line(fd, 0, currentSet[0], currentSet[1], currentSet[2], currentSet[3], currentSet[4], currentSet[5], currentSet[6], currentSet[7], currentSet[8], currentSet[9])
          line_delay(fd,1)
          write_line(fd, 0, newSet[0], newSet[1], newSet[2], newSet[3], newSet[4], newSet[5], newSet[6], newSet[7], newSet[8], newSet[9])
          line_delay(fd,1)
          write_line(fd, 0, currentSet[0], currentSet[1], currentSet[2], currentSet[3], currentSet[4], currentSet[5], currentSet[6], currentSet[7], currentSet[8], currentSet[9])
          line_delay(fd,1)
          write_line(fd, 0, newSet[0], newSet[1], newSet[2], newSet[3], newSet[4], newSet[5], newSet[6], newSet[7], newSet[8], newSet[9])
          line_delay(fd,1)
          currentSet = rearangeDots(fd, newSet)
      fd.close()
