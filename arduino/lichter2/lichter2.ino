#include <EEPROM.h>
#include <Wire.h>
#include <avr/wdt.h>
#include <Adafruit_NeoPixel.h>

/*
  Arduino NeoPixel player 

  This is the controller of the pixels of the LED rings. Each Ring has a total of 61 LEDs, 
  where each LED has 3 bytes (RGB) for its color. 24 bytes (start byte 0) for outer ring, 
  18 bytes for 2nd outer ring, 12 bytes for 3rd outer ring, 8 bytes for inner ring, 1 byte center. 

  Communication is via the I2C bus, where the Arduino is slave, and Sender is master. 
  The Sender can control many Arduinos, so each Arduino has an ID stored at EEPROM.
  This ID is configured at first time, and is not lost after power cycle. The I2C bus
  does not allows ID = 0, 1, 2. We start first Arduino with 11 (0x0b).
    
  The Sender (other side of Arduino) sends commands to this controller informing what should
  be done. Commands are a set of 5 bytes. Always 5 bytes, even when the command uses less.
  Commands are received assynchronous, via an interrupt and an event handler. The event handler 
  counts up to 5 bytes and only then the main loop starts processing the command. The Sender 
  can read the state of the Arduino by reading if the Arduino is busy with a command.
  Reading is done by an event handler.

  The main loop is informed that a new command is available by the event handler. The main 
  loop than executes the command. The command is the first byte received. Current commands:
  010: Turn all LEDs off
  011: Reset controller
  012: blink control LED
  013: load LED with color in bytes 1-3
  014: load LED with color in bytes 1-3 and blink a random LED for 100ms every second.
  015: load LED with color in bytes 1-3 with fade-in.
  016: load LED with color in bytes 1-3 by loading LED one by one from first to last LED every 10ms
  017: load LED with color in bytes 1-3 by rings (center, inner ring to outter ring)
  018: load LED with color in bytes 1-3 and pulse (dimm outter to inner ring and back) every 10s
  019: load LED with color in bytes 1-3 by loading random LED with new color every 100ms
 
*/

#define NUMPIXEL 61   // 61 LEDs per strip or ring
#define PIN 6         // connected to pin 6 PWM
#define CMD_LENGTH 5  // byte length of a command
#define LEDPIN 13     // Turn +5V on PIN 13 (internal LED)
#define BRIGTHNESS 8  // maximal brigthness to be used 1 to 32 (max)

#define BUSY 0        // I2C slave is processing command
#define READY 1       // I2C slave has executed command

#define TRUE 1
#define FALSE 0

Adafruit_NeoPixel strip = Adafruit_NeoPixel (NUMPIXEL, PIN); 

char FrameBuffer[NUMPIXEL*3];           // playout buffer that has a complete setting of target LED(RGB) colors

char I2CID;                             // Id of device in I2C. Must have been written with 
                                        // EEPROM.write(0,I2CID) on memory 0 of Arduino previously.
                                        
volatile char Command[CMD_LENGTH];      // Commands sent by Sender, volatile to avoid interrupt problem.
volatile char gotCmd = 0;               // variable informs that received a new Command, or bytes received so far
                                        // variable is returned on read event. Can be used to detect lost bytes
                                        // == 0: idle, no command
                                        // == 1: New command
                                        // == 11: idle, but 1 byte of new command
                                        // == 12: idle, but 2 bytes of new command
                                        // == 13: idle, but 3 bytes of new command
                                        // == 14: idle, but 4 bytes of new command
char cmdCount = 0;                      // counts how many bytes have been received so far

char doBlinking = FALSE;                // set to 1 when on blinking LEDs
char doPulse = FALSE;                   // set to 1 when pulsing LEDs

void setup() {
//  Serial.begin (9600);                  // starts serial port
  I2CID = EEPROM.read(0);               // read I2C Id from EEPROM byte 0
  Wire.begin(I2CID);                    // join I2C bus with ID = I2CID
  Wire.onRequest(requestEvent);         // register event handler for read requests from I2C master
  Wire.onReceive(receiveEvent);         // register event handler for write requests from I2C master
  strip.begin();                        // intialize LED strip
  strip.setBrightness(BRIGTHNESS);      // set LED power
  strip.show();                         // clean up strip
  randomSeed(analogRead(0));            // read pin 0 and seed random generator
}

void loop() {
  if (gotCmd==1){
    doBlinking = FALSE;               // new command, stop old blinking, pulse
    doPulse = FALSE;

    switch (Command[0]) {
      case 10: cmdOff(); break;       // turn LED off
      case 11: cmdReset(); break;     // reset Arduino
      case 12: cmdLED(); break;       // blink control LED
      case 13: cmdColor(Command[1], Command[2], Command[3]); break;       // set all LED to color RGB at once
      case 14: cmdColorBlink(Command[1], Command[2], Command[3]); break;  // set LED to RGB and blink
      case 15: cmdColorFade(Command[1], Command[2], Command[3]); break;   // set LED to RGB with fade-in
      case 16: cmdColorRoll(Command[1], Command[2], Command[3]); break;   // roll-in new color
      case 17: cmdColorInOut(Command[1], Command[2], Command[3]); break;  // set new color form inner to outter
      case 18: cmdColorPulse(Command[1], Command[2], Command[3]); break;  // set color and pulse
      case 19: cmdColorRandom(Command[1], Command[2], Command[3]); break; // set new color by random LED
    }
    gotCmd = 0;                      // finished processing command
  }

  if (doBlinking){
    blinkLED();
  }
  if (doPulse) {      
    checkPulse();      
  }
  
}

void receiveEvent(int howMany) {
  while (Wire.available()){                            // read bytes from I2C bus
    Command[cmdCount] = Wire.read();
    if (cmdCount < 4 ) {
      cmdCount++; 
      if (cmdCount == 1) gotCmd = 11;                  // received first byte of new command
      else gotCmd++;                                   // 
    }
    else { 
      cmdCount = 0;                                    // got all 5 bytes
      gotCmd = 1;                                      // ready to process command in "loop"
    }
  }
}

void requestEvent() {
  Wire.write(byte(gotCmd));       // return state of Command variable 
}

void cmdOff() {
  cmdColor(0,0,0);    // Write all to black
}

void cmdReset() {      // Reset is done by expiring a watchdog timer with 15ms
  wdt_disable();
  wdt_enable(WDTO_15MS);
  while(1) {}          // loop until timeout of 15ms
}

void cmdLED() {
  digitalWrite(LEDPIN, HIGH);  // turn LED on
  delay (50);                  // wait 50ms
  digitalWrite(LEDPIN, LOW);   // turn LED off
}

void cmdColor(char Red, char Green, char Blue) {
  for (int pixel=0; pixel<NUMPIXEL; pixel++) {
    FrameBuffer[pixel*3] = Red;
    FrameBuffer[pixel*3+1] = Green;
    FrameBuffer[pixel*3+2] = Blue;    
  }
  ShowTime();
}

void cmdColorBlink(char Red, char Green, char Blue) {
  cmdColor(Red, Green, Blue);
  doBlinking = TRUE;    
}

void blinkLED() {
  char pixel;
  char shouldBlink;

  shouldBlink = random (0,9);            // only blink 1 of 10 times we get here
  if (shouldBlink == 0) {
    pixel = random(1,NUMPIXEL - 1);      // select one pixel to blick. But not LED 0, used as reference
    FrameBuffer[pixel*3] = 0xff;
    FrameBuffer[pixel*3+1] = 0xff;
    FrameBuffer[pixel*3+2] = 0xff;    
    ShowTime();
    delay(100);                          // turn on for 0.1 second
    FrameBuffer[pixel*3] = FrameBuffer[0];
    FrameBuffer[pixel*3+1] = FrameBuffer[1];
    FrameBuffer[pixel*3+2] = FrameBuffer[2];    
    ShowTime();                          // restore original color, stored in LED 0
  } else delay(100);
}

void cmdColorFade(char Red, char Green, char Blue) {
  int i;
  for (i=BRIGTHNESS-1; i>=1; i--) {    // fade out old colors
    strip.setBrightness(i);
    ShowTime();
    delay(50);
  }
  cmdColor(Red, Green, Blue);  
  for (i=2; i<=BRIGTHNESS; i++) {      // fade in new colors
    strip.setBrightness(i);
    ShowTime();
    delay(50);
  }
}

void cmdColorRoll(char Red, char Green, char Blue) {
  for (int pixel=0; pixel<NUMPIXEL; pixel++) {
    FrameBuffer[pixel*3] = Red;
    FrameBuffer[pixel*3+1] = Green;
    FrameBuffer[pixel*3+2] = Blue;   
    ShowTime(); 
    delay(10);
  }
}

void cmdColorInOut(char Red, char Green, char Blue) {
  // assumes a ring with 1 central LED = 60
  // inner ring with 8 LED = 52 to 59
  // second inner ring with LED = 40 to 51
  // second outter ring with LED = 24 to 39
  // outter ring with LED = 0 to 23
  FrameBuffer[180] = Red;
  FrameBuffer[181] = Green;
  FrameBuffer[182] = Blue;
  ShowTime();
  delay(100);
  for (int pixel=52; pixel<=59; pixel++) {
    FrameBuffer[pixel*3] = Red;
    FrameBuffer[pixel*3+1] = Green;
    FrameBuffer[pixel*3+2] = Blue;   
  }
  ShowTime();
  delay(100);
  for (int pixel=40; pixel<=51; pixel++) {
    FrameBuffer[pixel*3] = Red;
    FrameBuffer[pixel*3+1] = Green;
    FrameBuffer[pixel*3+2] = Blue;   
  }
  ShowTime();
  delay(100);
  for (int pixel=24; pixel<=39; pixel++) {
    FrameBuffer[pixel*3] = Red;
    FrameBuffer[pixel*3+1] = Green;
    FrameBuffer[pixel*3+2] = Blue;   
  }
  ShowTime();
  delay(100);
  for (int pixel=0; pixel<=23; pixel++) {
    FrameBuffer[pixel*3] = Red;
    FrameBuffer[pixel*3+1] = Green;
    FrameBuffer[pixel*3+2] = Blue;   
  }  
  ShowTime();
  delay(100);
}

void cmdColorPulse(char Red, char Green, char Blue) {
  cmdColor(Red, Green, Blue);  // store color in central LED, that will not pulse
  doPulse = 11;                // will be decremented by 1 per 1s, if == 1 pulse, start again on 11
}

void checkPulse() {    // don't want blocking, so make 90 delays in 0.1s interval plus 1s pulse
  if (doPulse == 1) {
    pulseLED();        // takes 1 second
    doPulse = 91;      // start anothe cycle of 9 seconds
  } else {
    doPulse--;
    delay (100);       // sleep 0.1 second
  }
}
  
void pulseLED() {
  // assumes a ring with 1 central LED = 60 that has the color
  // inner ring with 8 LED = 52 to 59
  // second inner ring with LED = 40 to 51
  // second outter ring with LED = 24 to 39
  // outter ring with LED = 0 to 23

  for (int pixel=0; pixel<=23; pixel++) {
    FrameBuffer[pixel*3] = 0;
    FrameBuffer[pixel*3+1] = 0;
    FrameBuffer[pixel*3+2] = 0;   
  }  
  ShowTime();
  delay(125);
  for (int pixel=24; pixel<=39; pixel++) {
    FrameBuffer[pixel*3] = 0;
    FrameBuffer[pixel*3+1] = 0;
    FrameBuffer[pixel*3+2] = 0;   
  }  
  ShowTime();
  delay(125);
  for (int pixel=40; pixel<=51; pixel++) {
    FrameBuffer[pixel*3] = 0;
    FrameBuffer[pixel*3+1] = 0;
    FrameBuffer[pixel*3+2] = 0;   
  }  
  ShowTime();
  delay(125);
  for (int pixel=52; pixel<=59; pixel++) {
    FrameBuffer[pixel*3] = 0;
    FrameBuffer[pixel*3+1] = 0;
    FrameBuffer[pixel*3+2] = 0;   
  }  
  ShowTime();
  delay(125);
  for (int pixel=52; pixel<=59; pixel++) {
    FrameBuffer[pixel*3] = FrameBuffer[180];
    FrameBuffer[pixel*3+1] = FrameBuffer[181];
    FrameBuffer[pixel*3+2] = FrameBuffer[182];   
  }  
  ShowTime();
  delay(125);
  for (int pixel=40; pixel<=51; pixel++) {
    FrameBuffer[pixel*3] = FrameBuffer[180];
    FrameBuffer[pixel*3+1] = FrameBuffer[181];
    FrameBuffer[pixel*3+2] = FrameBuffer[182];   
  }  
  ShowTime();
  delay(125);
  for (int pixel=24; pixel<=39; pixel++) {
    FrameBuffer[pixel*3] = FrameBuffer[180];
    FrameBuffer[pixel*3+1] = FrameBuffer[181];
    FrameBuffer[pixel*3+2] = FrameBuffer[182];   
  }  
  ShowTime();
  delay(125);
  for (int pixel=0; pixel<=24; pixel++) {
    FrameBuffer[pixel*3] = FrameBuffer[180];
    FrameBuffer[pixel*3+1] = FrameBuffer[181];
    FrameBuffer[pixel*3+2] = FrameBuffer[182];   
  }  
  ShowTime();
  delay(125);
}

void cmdColorRandom(char Red, char Green, char Blue) {
  char chaos[NUMPIXEL];             // sequence of pixels to change
  for (int i=0; i<NUMPIXEL; i++)    // array with 0 to NUMPIXEL
    chaos[i] = i;  
  for (int i=0; i<NUMPIXEL; i++) {  // shuffle the array NUMPIXEL times, not perfect, but OK
    int temp = chaos[i];
    int randomPixel = random (0,NUMPIXEL);
    chaos[i] = chaos[randomPixel];
    chaos[randomPixel] = temp;
  }

  for (int pixel=0; pixel<NUMPIXEL; pixel++) {   // update color according to random array
    FrameBuffer[chaos[pixel]*3] = Red;
    FrameBuffer[chaos[pixel]*3+1] = Green;
    FrameBuffer[chaos[pixel]*3+2] = Blue;   
    ShowTime();
    delay(20);  
  }
}

void ShowTime() {  
  for (int pixel=0; pixel<NUMPIXEL; pixel++) {       // each pixel has RGB (3 bytes)
    char pixelRed = FrameBuffer[pixel*3];      
    char pixelGreen = FrameBuffer[pixel*3+1];
    char pixelBlue = FrameBuffer[pixel*3+2];
    strip.setPixelColor (pixel, pixelRed, pixelGreen, pixelBlue); // write NeoPixel
  }
  strip.show();             
}
