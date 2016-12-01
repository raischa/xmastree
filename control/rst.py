import RPi.GPIO as GPIO
import time

GPIOPIN = 4

GPIO.setmode(GPIO.BCM)
GPIO.setup(GPIOPIN, GPIO.OUT)
GPIO.output(GPIOPIN, GPIO.LOW)
time.sleep(1)
GPIO.output(GPIOPIN, GPIO.HIGH)
GPIO.cleanup()


