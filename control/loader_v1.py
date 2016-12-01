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

# The first byte of the line indicates the line type
LEDLINE = 1     # control byte (fade, blinking,...)+ 10*3 bytes (RGB) + '\n'
DELAYLINE = 2   # delay with time in seconds to wait for next line
TURNOFFLINE = 3 # turn off all LED strips

# control byte indicates effects on line, information is coded in the bits
BLINKINGBIT = 1 # bit pattern 0000 0001, first bit
FADINGBIT = 2   # bit pattern 0000 0010, second bit

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

def resetAll():
    try:
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(GPIOPIN, GPIO.OUT)
        GPIO.output(GPIOPIN, GPIO.LOW)
        time.sleep(1)
        GPIO.output(GPIOPIN, GPIO.HIGH)
    except:
        logging.debug('Error on GPIO reset')
    finally:
        GPIO.cleanup()
        return;

def getCommandConfirmation (Command) :
    i2c = smbus.SMBus(I2C_BUS)

    for i in range (1, NUMARDUINO):
        try:
            state = i2c.read_byte(i+NUMOFFSET)
            logging.info('Command %d to %d result %d (0=busy, 1=ready)' % {Command, i, state})
        except IOError:
            logging.debug('ERROR Command %d to %d' % {Command, i})
    return;

def doFadeIn(line):
    i2c = smbus.SMBus(I2C_BUS)

    for i in range (1, NUMARDUINO):
        try:
            i2c.write_byte(i+NUMOFFSET, FADING)
            i2c.write_byte(i+NUMOFFSET, line[3*(i-1)])
            i2c.write_byte(i+NUMOFFSET, line[3*(i-1)+1])
            i2c.write_byte(i+NUMOFFSET, line[3*(i-1)+2])
            i2c.write_byte(i+NUMOFFSET, 0x00)
            logging.info('Sent fade in to Arduino %d' % i)
        except IOError:
            logging.debug('ERROR fade in of Arduino %d' % i)
    getCommandConfirmation(FADING)
    return;

def doBlinking(line):
    i2c = smbus.SMBus(I2C_BUS)

    for i in range (1, NUMARDUINO):
        try:
            i2c.write_byte(i+NUMOFFSET, BLINKING)
            i2c.write_byte(i+NUMOFFSET, line[3*(i-1)])
            i2c.write_byte(i+NUMOFFSET, line[3*(i-1)+1])
            i2c.write_byte(i+NUMOFFSET, line[3*(i-1)+2])
            i2c.write_byte(i+NUMOFFSET, 0x00)
            logging.info('Sent blinking to Arduino %d' % i)
        except IOError:
            logging.debug('ERROR blinking of Arduino %d' % i)
    getCommandConfirmation(BLINKING)
    return;

def doSetColor(line):
    i2c = smbus.SMBus(I2C_BUS)

    for i in range (1, NUMARDUINO):
        try:
            i2c.write_byte(i+NUMOFFSET, SETCOLOR)
            i2c.write_byte(i+NUMOFFSET, line[3*(i-1)])
            i2c.write_byte(i+NUMOFFSET, line[3*(i-1)+1])
            i2c.write_byte(i+NUMOFFSET, line[3*(i-1)+2])
            i2c.write_byte(i+NUMOFFSET, 0x00)
            logging.info('Sent color to Arduino %d' % i)
        except IOError:
            logging.debug('ERROR color of Arduino %d' % i)
    getCommandConfirmation(SETCOLOR)
    return;

def doTurnOff():
    i2c = smbus.SMBus(I2C_BUS)

    for i in range (1, NUMARDUINO):
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

def checkBit(byteval,idx):
    return ((byteval&(1<<idx))!=0);

def handleLine(line):
    effect = line[0]
    if checkBit(effect,FADINGBIT):
        doFadeIn(line[1:])
    if checkBit(effect,BLINKINGBIT):
        doBlinking(line[1:])
    else: doSetColor(line[1:])

    return;

def handleDelay(line):
    time.sleed(int(bytearray(line)))
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
           print 'loader.py -f <inputfile> --log=debug'
           sys.exit()
        elif opt in ("-f", "--file"):
           fileName = arg
           logging.info('Opening %s' % fileName)
    return (fileName);

if __name__ == "__main__":
    # Debug Level, set with --log=debug, or --log=info
    numeric_level = getattr(logging, loglevel.upper(), None)
    if not isinstance(numeric_level, int):
        raise ValueError('Invalid log level: %s' % loglevel)
    logging.basicConfig(level=numeric_level, filename='loader.log',format='%(asctime)s %(message)s')

    fileName = getConfigFile(sys.argv[1:])

    resetAll()  # cleanup all Arduino with hard reset

    with open(fileName, 'r') as configFile:
        for line in configFile:
            if line[0] == LEDLINE:
                handleLine(line[1:])
            elif line[0] == DELAYLINE:
                handleDelay(line[1:])
            elif line[0] == TURNOFFLINE:
                handleTurnOff()
