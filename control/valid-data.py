import sys
# The first byte of the line indicates the line type
LEDLINE = 1     # control byte (fade, blinking,...)+ 10*3 bytes (RGB) + '\n'
DELAYLINE = 2   # delay with time in seconds to wait for next line
TURNOFFLINE = 3 # turn off all LED strips

# control byte indicates effects on line, information is coded in the bits
BLINKINGBIT = 1 # bit pattern 0000 0001, first bit
FADINGBIT = 2   # bit pattern 0000 0010, second bit


def checkBit(byteval,idx):
    return ((byteval&(1<<(idx-1)))!= 0);

def handleLine(line):
    if checkBit(ord(line[0]),FADINGBIT):
        print 'got fade-in'
    if checkBit(ord(line[0]),BLINKINGBIT):
        print 'got blinking'  
    for i in range (1, (len(line) - 1)/3 + 1):
        print 'byte ', i, "\n", ' Red = ', ord(line[1+3*(i-1)])
        print ' Green = ', ord(line[2+3*(i-1)])
        print ' Blue = ', ord(line[3*i])
    return;

def handleDelay(line):
    print 'got a sleep of %d' % int(bytearray(line))  
    return;

def handleTurnOff():
    print 'got turn-off'
    return;

if __name__ == "__main__":
 with open('./candycrush1.dat', 'r') as configFile:
#     while True:
#         c = configFile.read(1)
#         if not c:
#             print "EOF"
#             break
#         print "read :", ord(c)
         
     for line in configFile:
         line.strip()
         if ord(line[0]) == LEDLINE:
             handleLine(line[1:])
         elif ord(line[0]) == DELAYLINE:
             handleDelay(line[1:])
         elif ord(line[0]) == TURNOFFLINE:
             handleTurnOff()
         else:
             print 'nothing to do with line[0] %s' % line[0] 
