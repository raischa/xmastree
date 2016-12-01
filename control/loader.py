# Version 1.0
# Author Rainer Schatzmayr
#
# This is the loader of the Arduino, it expects a config file with several lines.
# The loader handles line by line, each line has a control byte followed by other data
# Loader always resets the Arduinos before starting loading
import time
import RPi.GPIO as GPIO
import sys
import smbus
import logging
import getopt
import os
import os.path

# The first byte of the line indicates the line type
LEDLINE = 1     # control byte (fade, blinking,...)+ 10*3 bytes (RGB) + '\n'
DELAYLINE = 2   # delay with time in seconds to wait for next line
TURNOFFLINE = 3 # turn off all LED strips
RINGLINE = 4    # control byte (fade, blinking,...)+ ring number + 3 bytes (RGB) + '\n'

# control byte indicates effects on line, information is coded in the bits
# higher nimble is entry effect, lower nimble is runtime effect
BLINKINGBIT = 1 # bit pattern 0000 0001
FADINGBIT = 16  # bit pattern 0001 0000
ROLLINBIT = 32  # bit pattern 0010 0000
INOUTBIT = 48   # bit pattern 0011 0000
PULSINGBIT = 2  # bit pattern 0000 0010
RANDOMBIT = 64  # bit pattern 0100 0000

# using I2C bus number 1
I2C_BUS = 1

# Raspberry PIN 4 default high, on low causes rst on all Arduinos
GPIOPIN = 4

# Number of Arduinos connecgted and I2C address offset as can't start address 1
NUMARDUINO = 10 # we have 10 Arduinos on I2C bus
NUMOFFSET = 10  # first Arduino is 10+1=11, last is 10+10=20

# Current commands handled by Arduino. All commands are 5 bytes logging
# If less than 5 bytes are used, unused bytes are padding with 0x00
ALLOFF = 10     # turn off all LEDs of the Arduino
RESET = 11      # software reset of the Arduino
BLINKCTRL = 12  # blink control LED of the Arduino
SETCOLOR = 13   # load LED strip of Arduino with color in bytes 2-4
BLINKING = 14   # load LED with color in bytes 2-4 and blink a random LED for 100ms every second.
FADING = 15     # load LED with color in bytes 2-4 with fade-in
ROLLIN = 16     # load LED with color in bytes 2-4 by roll-in of new color
INOUT = 17      # load LED with color in bytes 2-4 from inside out
PULSING = 18    # load LED with color in bytes 2-4 and pulse every 10s
RANDOM = 19     # load LED with color in bytes 2-4 by random order

def resetAll():
    logging.info('got Reset')
    try:
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(GPIOPIN, GPIO.OUT)
        GPIO.output(GPIOPIN, GPIO.LOW)
        time.sleep(1)
        GPIO.output(GPIOPIN, GPIO.HIGH)
        logging.info('done Reset')
    except:
        logging.debug('Error on GPIO reset')
    finally:
        GPIO.cleanup()
        time.sleep(2)  # need to wait that Arduino perform reset
        return;

def getCommandConfirmation (CommandPassed) :
    i2c = smbus.SMBus(I2C_BUS)

    Command = CommandPassed
    for i in range (1, NUMARDUINO+1):
        try:
            state = i2c.read_byte(i+NUMOFFSET)
            logging.info('Command %d to %d result %d (0=ready, 1=busy, 11,12,13,14=cmd bytes rcv)', Command, i, state)
            if 11 <= state <= 14 :
                for j in range (1, 16 - state):
                    i2c.write_byte(i+NUMOFFSET, 0x00)
                    logging.info('Recovering Arduino %d in state %d by sending byte 0x00', i, state)
        except IOError:
            logging.debug('ERROR confirmation command %d to Arduino: %d', Command, i)
    return;

def doRandom(line):
    logging.info('got Random')
    i2c = smbus.SMBus(I2C_BUS)

    for i in range (1, NUMARDUINO+1):
        try:
            i2c.write_byte(i+NUMOFFSET, RANDOM)
            i2c.write_byte(i+NUMOFFSET, ord(line[3*(i-1)]))
            i2c.write_byte(i+NUMOFFSET, ord(line[3*(i-1)+1]))
            i2c.write_byte(i+NUMOFFSET, ord(line[3*(i-1)+2]))
            i2c.write_byte(i+NUMOFFSET, 0x00)
            logging.info('Sent random to Arduino %d' % i)
        except IOError:
            logging.debug('ERROR random of Arduino %d' % i)
    time.sleep(3)  # give time to random
    getCommandConfirmation(RANDOM)

    return;

def doPulsing(line):
    logging.info('got Pulsing')
    i2c = smbus.SMBus(I2C_BUS)

    for i in range (1, NUMARDUINO+1):
        try:
            i2c.write_byte(i+NUMOFFSET, PULSING)
            i2c.write_byte(i+NUMOFFSET, ord(line[3*(i-1)]))
            i2c.write_byte(i+NUMOFFSET, ord(line[3*(i-1)+1]))
            i2c.write_byte(i+NUMOFFSET, ord(line[3*(i-1)+2]))
            i2c.write_byte(i+NUMOFFSET, 0x00)
            logging.info('Sent pulsing to Arduino %d' % i)
        except IOError:
            logging.debug('ERROR pulsing in of Arduino %d' % i)
    time.sleep(1)  # give time to Pulse
    getCommandConfirmation(PULSING)

    return;

def doInOut(line):
    logging.info('got In-Out')
    i2c = smbus.SMBus(I2C_BUS)

    for i in range (1, NUMARDUINO+1):
        try:
            i2c.write_byte(i+NUMOFFSET, INOUT)
            i2c.write_byte(i+NUMOFFSET, ord(line[3*(i-1)]))
            i2c.write_byte(i+NUMOFFSET, ord(line[3*(i-1)+1]))
            i2c.write_byte(i+NUMOFFSET, ord(line[3*(i-1)+2]))
            i2c.write_byte(i+NUMOFFSET, 0x00)
            logging.info('Sent In Out to Arduino %d' % i)
        except IOError:
            logging.debug('ERROR In Out of Arduino %d' % i)
    time.sleep(1)  # give time to InOut
    getCommandConfirmation(INOUT)

    return;


def doRollIn(line):
    logging.info('got Roll-in')
    i2c = smbus.SMBus(I2C_BUS)

    for i in range (1, NUMARDUINO+1):
        try:
            i2c.write_byte(i+NUMOFFSET, ROLLIN)
            i2c.write_byte(i+NUMOFFSET, ord(line[3*(i-1)]))
            i2c.write_byte(i+NUMOFFSET, ord(line[3*(i-1)+1]))
            i2c.write_byte(i+NUMOFFSET, ord(line[3*(i-1)+2]))
            i2c.write_byte(i+NUMOFFSET, 0x00)
            logging.info('Sent roll in to Arduino %d' % i)
        except IOError:
            logging.debug('ERROR roll in of Arduino %d' % i)
    time.sleep(1)  # give time to roll-in
    getCommandConfirmation(ROLLIN)

    return;

def doFadeIn(line):
    logging.info('got Fade-in')
    i2c = smbus.SMBus(I2C_BUS)

    for i in range (1, NUMARDUINO+1):
        try:
            i2c.write_byte(i+NUMOFFSET, FADING)
            i2c.write_byte(i+NUMOFFSET, ord(line[3*(i-1)]))
            i2c.write_byte(i+NUMOFFSET, ord(line[3*(i-1)+1]))
            i2c.write_byte(i+NUMOFFSET, ord(line[3*(i-1)+2]))
            i2c.write_byte(i+NUMOFFSET, 0x00)
            logging.info('Sent fade in to Arduino %d' % i)
        except IOError:
            logging.debug('ERROR fade in of Arduino %d' % i)
    time.sleep(1)  # give time to fade-in
    getCommandConfirmation(FADING)

    return;

def doBlinking(line):
    logging.info('got Blinking')
    i2c = smbus.SMBus(I2C_BUS)

    for i in range (1, NUMARDUINO+1):
        try:
            i2c.write_byte(i+NUMOFFSET, BLINKING)
            i2c.write_byte(i+NUMOFFSET, ord(line[3*(i-1)]))
            i2c.write_byte(i+NUMOFFSET, ord(line[3*(i-1)+1]))
            i2c.write_byte(i+NUMOFFSET, ord(line[3*(i-1)+2]))
            i2c.write_byte(i+NUMOFFSET, 0x00)
            logging.info('Sent blinking to Arduino %d' % i)
        except IOError:
            logging.debug('ERROR blinking of Arduino %d' % i)
    getCommandConfirmation(BLINKING)
    return;

def doSetColor(line):
    logging.info('got Set Color')

    try:
        i2c = smbus.SMBus(I2C_BUS)
    except IOError, err:
        logging.debug('ERROR accessing bus')

    for i in range (1, NUMARDUINO+1):
        try:
            i2c.write_byte(i+NUMOFFSET, SETCOLOR)
            i2c.write_byte(i+NUMOFFSET, ord(line[3*(i-1)]))
            i2c.write_byte(i+NUMOFFSET, ord(line[3*(i-1)+1]))
            i2c.write_byte(i+NUMOFFSET, ord(line[3*(i-1)+2]))
            i2c.write_byte(i+NUMOFFSET, 0x00)
            logging.info('Sent color to Arduino %d' % i)
        except IOError:
            logging.debug('ERROR color of Arduino %d' % i)
    getCommandConfirmation(SETCOLOR)
    return;

def doTurnOff():
    logging.info('got Turn off')
    i2c = smbus.SMBus(I2C_BUS)

    for i in range (1, NUMARDUINO+1):
        try:
            i2c.write_byte(i+NUMOFFSET, ALLOFF)
            i2c.write_byte(i+NUMOFFSET, 0x00)
            i2c.write_byte(i+NUMOFFSET, 0x00)
            i2c.write_byte(i+NUMOFFSET, 0x00)
            i2c.write_byte(i+NUMOFFSET, 0x00)
            logging.info('Sent turn LEDs off to Arduino %d' % i)
        except IOError:
            logging.debug('ERROR turning all LEDs off of Arduino %d' % i)
    getCommandConfirmation(ALLOFF)
    return;

def handleLine(line):
    logging.info('got a new line with LED colors')

    if ord(line[0]) & 0xf0 == FADINGBIT:
        doFadeIn(line[1:])
    if ord(line[0]) & 0xf0 == ROLLINBIT:
        doRollIn(line[1:])
    if ord(line[0]) & 0xf0 == INOUTBIT:
        doInOut(line[1:])
    if ord(line[0]) & 0xf0 == RANDOMBIT:
        doRandom(line[1:])
    if ord(line[0]) & 0x0f == BLINKINGBIT:
        doBlinking(line[1:])
    if ord(line[0]) & 0x0f == PULSINGBIT:
        doPulsing(line[1:])
    if ord(line[0])== 0:
        doSetColor(line[1:])

    return;

def handleDelay(line):
    time.sleep(ord(line[0]))
    return;

def handleTurnOff():
    doTurnOff()
    return;

def getConfigFile(argv):
    fileName = ''
    try:
        opts, args = getopt.getopt(argv,"hf:",["file="])
    except getopt.GetoptError:
        print 'loader.py -f <inputfile>'
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
           print 'loader.py -f <inputfile>'
           sys.exit()
        elif opt in ("-f", "--file"):
           fileName = arg
           logging.info('Opening %s' % fileName)
    return (fileName);

def becomeMaster():
    # verify if another Loader is running, kill it, and become the master
    logging.info('verifying if other loader is running')
    try:
        loaderPid = '/var/www/html/loader.pid'
        if os.path.isfile(loaderPid) and (os.path.getsize(loaderPid) > 0):
            logging.info('found loader.pid file')
            with open(loaderPid, 'r') as f:
              pid = int(f.readline())
              logging.info('going to kill loader pid: %d' % pid)
              if os.path.exists("/proc/%d" % pid):
                  os.kill(pid,9)
              else :
                  logging.info('loader pid: %d is not running anymore' % pid)
              os.remove(loaderPid)
        with open(loaderPid, 'w') as f:
            pid = os.getpid()
            logging.info('new loader pid: %d' % pid)
            f.write("%s" % pid)
    except IOError:
        logging.debug('Error handling PID file')
    return;

if __name__ == "__main__":
    # DEBUG is on
    logging.basicConfig(filename='/var/www/html/loader.log', level=logging.DEBUG, format='%(asctime)s %(message)s')

    becomeMaster()

    fileName = getConfigFile(sys.argv[1:])

    resetAll()  # cleanup all Arduino with hard reset

    with open(fileName, 'r') as configFile:
        for line in configFile:
            if ord(line[0]) == LEDLINE:
                handleLine(line[1:])
            elif ord(line[0]) == DELAYLINE:
                handleDelay(line[1:])
            elif ord(line[0]) == TURNOFFLINE:
                handleTurnOff()
