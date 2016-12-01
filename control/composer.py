#!/usr/bin/env python
#
# creates files with data to play

import sys

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

def line_color(fd, ring_color):
  fd.write(chr(LEDLINE))
  fd.write('\x00')
  for i in range (1, 11):
      fd.write(chr(int(ring_color[0],16)))
      fd.write(chr(int(ring_color[1],16)))
      fd.write(chr(int(ring_color[2],16)))
  fd.write('\n')
  return;

def line_color_fade(fd, ring_color):
  fd.write(chr(LEDLINE))
  fd.write(chr(FADINGBIT))
  for i in range (1, 11):
      fd.write(chr(int(ring_color[0],16)))
      fd.write(chr(int(ring_color[1],16)))
      fd.write(chr(int(ring_color[2],16)))
  fd.write('\n')
  return;

def line_color_roll(fd, ring_color):
  fd.write(chr(LEDLINE))
  fd.write(chr(ROLLINBIT))
  for i in range (1, 11):
      fd.write(chr(int(ring_color[0],16)))
      fd.write(chr(int(ring_color[1],16)))
      fd.write(chr(int(ring_color[2],16)))
  fd.write('\n')
  return;

def line_color_inout(fd, ring_color):
  fd.write(chr(LEDLINE))
  fd.write(chr(INOUTBIT))
  for i in range (1, 11):
      fd.write(chr(int(ring_color[0],16)))
      fd.write(chr(int(ring_color[1],16)))
      fd.write(chr(int(ring_color[2],16)))
  fd.write('\n')
  return;

def line_color_random(fd, ring_color):
  fd.write(chr(LEDLINE))
  fd.write(chr(RANDOMBIT))
  for i in range (1, 11):
      fd.write(chr(int(ring_color[0],16)))
      fd.write(chr(int(ring_color[1],16)))
      fd.write(chr(int(ring_color[2],16)))
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

if __name__ == "__main__":
  fd = open('./playlist.dat', 'wb')

  write_line(fd, RANDOMBIT, RED, RED, RED, RED, RED, RED, RED, RED, RED, RED)
  line_delay(fd, 1)
  write_line(fd, RANDOMBIT & BLINKINGBIT, GREEN, RED, RED, RED, RED, RED, RED, RED, RED, RED)
  line_delay(fd, 1)
  write_line(fd, RANDOMBIT & PULSINGBIT, GREEN, GREEN, RED, RED, RED, RED, RED, RED, RED, RED)
  line_delay(fd, 1)
  write_line(fd, RANDOMBIT, GREEN, GREEN, GREEN, RED, RED, RED, RED, RED, RED, RED)
  line_delay(fd, 1)
  write_line(fd, RANDOMBIT & BLINKINGBIT, GREEN, GREEN, GREEN, GREEN, RED, RED, RED, RED, RED, RED)
  line_delay(fd, 1)
  write_line(fd, RANDOMBIT & PULSINGBIT, GREEN, GREEN, GREEN, GREEN, GREEN, RED, RED, RED, RED, RED)
  line_delay(fd, 1)
  write_line(fd, RANDOMBIT, GREEN, GREEN, GREEN, GREEN, GREEN, GREEN, RED, RED, RED, RED)
  line_delay(fd, 1)
  write_line(fd, RANDOMBIT & BLINKINGBIT, GREEN, GREEN, GREEN, GREEN, GREEN, GREEN, GREEN, RED, RED, RED)
  line_delay(fd, 1)
  write_line(fd, RANDOMBIT & PULSINGBIT, GREEN, GREEN, GREEN, GREEN, GREEN, GREEN, GREEN, GREEN, RED, RED)
  line_delay(fd, 1)
  write_line(fd, RANDOMBIT, GREEN, GREEN, GREEN, GREEN, GREEN, GREEN, GREEN, GREEN, GREEN, RED)
  line_delay(fd, 1)
  write_line(fd, RANDOMBIT & BLINKINGBIT, GREEN, GREEN, GREEN, GREEN, GREEN, GREEN, GREEN, GREEN, GREEN, GREEN)
  line_delay(fd, 1)
  write_line(fd, INOUTBIT, BLUE, GREEN, GREEN, GREEN, GREEN, GREEN, GREEN, GREEN, GREEN, GREEN)
  line_delay(fd, 1)
  write_line(fd, INOUTBIT & BLINKINGBIT, BLUE, BLUE, GREEN, GREEN, GREEN, GREEN, GREEN, GREEN, GREEN, GREEN)
  line_delay(fd, 1)
  write_line(fd, INOUTBIT & PULSINGBIT, BLUE, BLUE, BLUE, GREEN, GREEN, GREEN, GREEN, GREEN, GREEN, GREEN)
  line_delay(fd, 1)
  write_line(fd, INOUTBIT, BLUE, BLUE, BLUE, BLUE, GREEN, GREEN, GREEN, GREEN, GREEN, GREEN)
  line_delay(fd, 1)
  write_line(fd, INOUTBIT & BLINKINGBIT, BLUE, BLUE, BLUE, BLUE, BLUE, GREEN, GREEN, GREEN, GREEN, GREEN)
  line_delay(fd, 1)
  write_line(fd, INOUTBIT & PULSINGBIT, BLUE, BLUE, BLUE, BLUE, BLUE, BLUE, GREEN, GREEN, GREEN, GREEN)
  line_delay(fd, 1)
  write_line(fd, INOUTBIT, BLUE, BLUE, BLUE, BLUE, BLUE, BLUE, BLUE, GREEN, GREEN, GREEN)
  line_delay(fd, 1)
  write_line(fd, INOUTBIT & BLINKINGBIT, BLUE, BLUE, BLUE, BLUE, BLUE, BLUE, BLUE, BLUE, GREEN, GREEN)
  line_delay(fd, 1)
  write_line(fd, INOUTBIT & PULSINGBIT, BLUE, BLUE, BLUE, BLUE, BLUE, BLUE, BLUE, BLUE, BLUE, GREEN)
  line_delay(fd, 1)
  write_line(fd, INOUTBIT, BLUE, BLUE, BLUE, BLUE, BLUE, BLUE, BLUE, BLUE, BLUE, BLUE)
  line_delay(fd, 1)
  write_line(fd, ROLLINBIT, YELLOW, BLUE, BLUE, BLUE, BLUE, BLUE, BLUE, BLUE, BLUE, BLUE)
  line_delay(fd, 1)
  write_line(fd, ROLLINBIT & BLINKINGBIT, YELLOW, YELLOW, BLUE, BLUE, BLUE, BLUE, BLUE, BLUE, BLUE, BLUE)
  line_delay(fd, 1)
  write_line(fd, ROLLINBIT & PULSINGBIT, YELLOW, YELLOW, YELLOW, BLUE, BLUE, BLUE, BLUE, BLUE, BLUE, BLUE)
  line_delay(fd, 1)
  write_line(fd, ROLLINBIT, YELLOW, YELLOW, YELLOW, YELLOW, BLUE, BLUE, BLUE, BLUE, BLUE, BLUE)
  line_delay(fd, 1)
  write_line(fd, ROLLINBIT & BLINKINGBIT, YELLOW, YELLOW, YELLOW, YELLOW, YELLOW, BLUE, BLUE, BLUE, BLUE, BLUE)
  line_delay(fd, 1)
  write_line(fd, ROLLINBIT, YELLOW, YELLOW, YELLOW, YELLOW, YELLOW, YELLOW, BLUE, BLUE, BLUE, BLUE)
  line_delay(fd, 1)
  write_line(fd, ROLLINBIT & BLINKINGBIT, YELLOW, YELLOW, YELLOW, YELLOW, YELLOW, YELLOW, YELLOW, BLUE, BLUE, BLUE)
  line_delay(fd, 1)
  write_line(fd, ROLLINBIT & PULSINGBIT, YELLOW, YELLOW, YELLOW, YELLOW, YELLOW, YELLOW, YELLOW, YELLOW, BLUE, BLUE)
  line_delay(fd, 1)
  write_line(fd, ROLLINBIT, YELLOW, YELLOW, YELLOW, YELLOW, YELLOW, YELLOW, YELLOW, YELLOW, YELLOW, BLUE)
  line_delay(fd, 1)
  write_line(fd, ROLLINBIT & BLINKINGBIT, YELLOW, YELLOW, YELLOW, YELLOW, YELLOW, YELLOW, YELLOW, YELLOW, YELLOW, YELLOW)
  line_delay(fd, 1)
  write_line(fd, ROLLINBIT & PULSINGBIT, YELLOW, YELLOW, YELLOW, YELLOW, YELLOW, YELLOW, YELLOW, YELLOW, YELLOW, YELLOW)
  line_delay(fd, 1)
  write_line(fd, FADINGBIT, CYAN, YELLOW, YELLOW, YELLOW, YELLOW, YELLOW, YELLOW, YELLOW, YELLOW, YELLOW)
  line_delay(fd, 1)
  write_line(fd, FADINGBIT & BLINKINGBIT, CYAN, CYAN, YELLOW, YELLOW, YELLOW, YELLOW, YELLOW, YELLOW, YELLOW, YELLOW)
  line_delay(fd, 1)
  write_line(fd, FADINGBIT, CYAN, CYAN, CYAN, YELLOW, YELLOW, YELLOW, YELLOW, YELLOW, YELLOW, YELLOW)
  line_delay(fd, 1)
  write_line(fd, FADINGBIT & PULSINGBIT, CYAN, CYAN, CYAN, CYAN, YELLOW, YELLOW, YELLOW, YELLOW, YELLOW, YELLOW)
  line_delay(fd, 1)
  write_line(fd, FADINGBIT & BLINKINGBIT, CYAN, CYAN, CYAN, CYAN, CYAN, YELLOW, YELLOW, YELLOW, YELLOW, YELLOW)
  line_delay(fd, 1)
  write_line(fd, FADINGBIT, CYAN, CYAN, CYAN, CYAN, CYAN, CYAN, YELLOW, YELLOW, YELLOW, YELLOW)
  line_delay(fd, 1)
  write_line(fd, FADINGBIT & PULSINGBIT, CYAN, CYAN, CYAN, CYAN, CYAN, CYAN, CYAN, YELLOW, YELLOW, YELLOW)
  line_delay(fd, 1)
  write_line(fd, FADINGBIT & BLINKINGBIT, CYAN, CYAN, CYAN, CYAN, CYAN, CYAN, CYAN, CYAN, YELLOW, YELLOW)
  line_delay(fd, 1)
  write_line(fd, FADINGBIT, CYAN, CYAN, CYAN, CYAN, CYAN, CYAN, CYAN, CYAN, CYAN, YELLOW)
  line_delay(fd, 1)
  write_line(fd, FADINGBIT & PULSINGBIT, CYAN, CYAN, CYAN, CYAN, CYAN, CYAN, CYAN, CYAN, CYAN, CYAN)
  line_delay(fd, 1)
  
#  for i in range (1, 2):
#    line_color_fade(fd, RED)
#    line_delay(configFile, 1)
#    line_color_fade(fd, GREEN)
#    line_delay(configFile, 1)
#    line_color_fade(fd, BLUE)
#    line_delay(configFile, 1)
#    line_color_fade(fd, YELLOW)
#    line_delay(configFile, 1)
#    line_color_fade(fd, CYAN)
#    line_delay(configFile, 1)
#    line_color_fade(fd, PINK)
#    line_delay(configFile, 1)
#
#  line_turnoff(fd)
    
  fd.close()
