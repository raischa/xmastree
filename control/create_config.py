import struct

def rgb(numFrames,timeDelay):
  timeDelayHigh = timeDelay/256
  timeDelayLow = timeDelay%256
  for line in range (0,numFrames):
    for pixel in range (0,60):
       configFile.write(chr(255))
       configFile.write(chr(0))    
       configFile.write(chr(0))    
    configFile.write(chr(timeDelayHigh))
    configFile.write(chr(timeDelayLow))
    configFile.write('\n')
   
    for pixel in range (0,60):
       configFile.write(chr(0))    
       configFile.write(chr(255))     
       configFile.write(chr(0))
    configFile.write(chr(timeDelayHigh))
    configFile.write(chr(timeDelayLow))
    configFile.write('\n')
   
    for pixel in range (0,60):
       configFile.write(chr(0))    
       configFile.write(chr(0))    
       configFile.write(chr(255))    
    configFile.write(chr(timeDelayHigh))
    configFile.write(chr(timeDelayLow))
    configFile.write('\n')
  return();

def rainbow(numFrames,timeDelay):
  timeDelayHigh = timeDelay/256
  timeDelayLow = timeDelay%256

#  red = (0xff, 0x00, 0x00)
#  green = (0x00, 0xff, 0x00)
#  blue = (0x00, 0x00, 0x255)
#  yellow = (0xff, 0xff, 0x00)
#  orange = (0xff, 0x80, 0x00)
#  purple = (0xff, 0x00, 0xff)

  color = [];
  for i in range (0,183):
    color.append(0);
    
  for i in range (0,183):
    if (i%18 == 0): color[i] = 255
    if (i%18 == 1): color[i] = 0
    if (i%18 == 2): color[i] = 0
    if (i%18 == 3): color[i] = 0
    if (i%18 == 4): color[i] = 255
    if (i%18 == 5): color[i] = 0
    if (i%18 == 6): color[i] = 0
    if (i%18 == 7): color[i] = 0
    if (i%18 == 8): color[i] = 255
    if (i%18 == 9): color[i] = 255
    if (i%18 == 10): color[i] = 255
    if (i%18 == 11): color[i] = 0
    if (i%18 == 12): color[i] = 255
    if (i%18 == 13): color[i] = 120
    if (i%18 == 14): color[i] = 0
    if (i%18 == 15): color[i] = 255
    if (i%18 == 16): color[i] = 0
    if (i%18 == 17): color[i] = 255
    
  for line in range (0,numFrames):
    for pixel in range (0,180):
      configFile.write(chr(color[pixel]))
    configFile.write(chr(timeDelayHigh))  
    configFile.write(chr(timeDelayLow))
    configFile.write('\n')
    for pixel in range (0,180):
      color[182-pixel] = color[182-pixel-3]
    color[0] = color[180]
    color[1] = color[181]
    color[2] = color[182]
  return();

configFile = open ("config.cfg", "w")

frames = int(raw_input ("how many frames? "))
delay = int(raw_input ("how much delay between frames? "))
selection = int(raw_input ("press 1 for rbg cycles " + "\n" + "press 2 for rainbow "))
if (selection == 1): rgb(frames, delay)
if (selection == 2): rainbow(frames, delay)


configFile.close()



