import serial
from time import sleep 

print "getting serial port"
ser = serial.Serial('/dev/ttyACM0', 9600)
ser.close()  # might be left open froma previous ctrl C
ser.open()
print "ready to go"
sleep(2)     # give UART time to program

while (1):
  print "start red"  
  for i in range (0,60):
    ser.write(chr(255))
    ser.read()
    ser.write(chr(0))
    ser.read()
    ser.write(chr(0))
    ser.read()
  ser.write(chr(0))
  ser.read()
  ser.write(chr(200))
  ser.read()
  print "start green"  
  for i in range (0,60):
    ser.write(chr(0))
    ser.read()
    ser.write(chr(255))
    ser.read()
    ser.write(chr(0))
    ser.read()
  ser.write(chr(0))
  ser.read()
  ser.write(chr(200))
  ser.read()
  print "start blue"  
  for i in range (0,60):
    ser.write(chr(0))
    ser.read()
    ser.write(chr(0))
    ser.read()
    ser.write(chr(255))
    ser.read()
  ser.write(chr(1))
  ser.read()
  ser.write(chr(0))
  ser.read()
