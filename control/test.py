import serial
from time import sleep 

print "starting ..."
ser = serial.Serial('/dev/ttyACM0', 9600)
sleep(1)
Delay=0.0

while (1):
  print "red ..."
  for i in range (0, 60):
    ser.write(chr(255))
    ser.read()
    sleep(Delay)
    ser.write(chr(0))
    ser.read()
    sleep(Delay)
    ser.write(chr(0))
    ser.read()
    sleep(Delay)
  ser.write(chr(1))
  ser.read()
  sleep(Delay)
  ser.write(chr(1))
  ser.read()
  sleep(Delay)
  
  print "green ..."
  for i in range (0, 60):
    ser.write(chr(0))
    ser.read()
    sleep(Delay)
    ser.write(chr(255))
    ser.read()
    sleep(Delay)
    ser.write(chr(0))
    ser.read()
    sleep(Delay)
  ser.write(chr(1))
  ser.read()
  sleep(Delay)
  ser.write(chr(1))
  ser.read()
  sleep(Delay)

  print "blue ..."
  for i in range (0, 60):
    ser.write(chr(0))
    ser.read()
    sleep(Delay)
    ser.write(chr(0))
    ser.read()
    sleep(Delay)
    ser.write(chr(255))
    ser.read()
    sleep(Delay)
  ser.write(chr(1))
  ser.read()
  sleep(Delay)
  ser.write(chr(1))
  ser.read()
  sleep(Delay)
