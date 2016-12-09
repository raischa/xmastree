# xmastree
Arduino, Raspberry, Web
This is the code repository for the different parts of the code that make the Christmas Tree. 
The code has 3 areas:
- Arduino: this is the C file (.ino) that contains the code for the Arduino
- Control: this is the Python code that runs on the Raspberry and controls the Arduino
- Web: this is the html/JavaScript/PHP code that runs on the Raspberry and presents a web interface


Main diagram
```
          raspberry pi                           arduino nano    led stripe
+--------------------------------------------+   +----------+    +-------+

+---------+      +---------+                      +--------+      +-----+
|  WEB    | +--> |data.dat | <--+            +--> |arduino0| +--> |ball0|
+---------+      +---------+    | +--------+ |    +--------+      +-----+
                                +-+ loader +-+
+---------+      +---------+    | +---+----+ |    +--------+      +-----+
|composer*| +--> |file*.dat| <--+     ^      +--> |arduino1| +--> |ball1|
+---------+      +---------+          |      |    +--------+      +-----+
                                      |      |
                                  +---+----+ |    +--------+      +-----+
                                  |cronjob | +--> |arduino9| +--> |ball9|
                                  +--------+      +--------+      +-----+
```
Hardware overview

The led stripe are WS2812 that can be controlled by writing sequentially to its data input.
It's a shift register with 3 colors (RGB) for each LED. Each strip has 61 LEDs. The LEDs have 5
rings: outer ring with 24 LED, 2nd outer ring with 16 LED, 2nd inner ring with 12 LED, inner
ring with 8 LEDs, and a central LED. The LED 0 is in the outer ring, LED 60 is the central LED.
The LED rings are on a disk, and the disk is inserted in a plexiglas ball. I used JR connectors
for the LED connection to the cable that goes to the box with the Arduinos. As this is for
outdoor scenario with rain, wind, snow, I used stronger cables.

An Arduino nano is used to control each stripe. I probably could have used one Arduino to control
more than one LED stripe. However it would have required more software development. The fun
was to play with multiple Arduinos. I used Arduino Nano for its size, and easy handle. Arduino
Micro Pro are smaller, but more complicated to handle as I bricked 2 during tests. The Arduino
modulates on one of its I/O pins the signal for the LEDs. Trying to modulate this signal (pulse
width, time) is very hard on a Raspberry, as Linux is more difficult to control.

The 'rst' reset pins of the Arduinos are connected to a Raspberry I/O pin via a level shifter.
3.3 (Raspberry) to 5V (Arduino). The Raspberry can use its I/O pin to reset all the Arduinos.
Arduinos reboot in 2 seconds. I reboot them when the Raspberry wants to start sending a set of
commands to the Arduinos. This has proven useful, as sometimes the Arduinos can get into
unknown states.

The 10 Arduinos for the 10 balls are mounted on a plexiglas board. It became quite tight to solder
all of it. I used IC sockets as the Arduino has to be disconnected from the board when I flash
it. The 'rst' pins of all Arduinos are all connected. Flashing one of them reseted the whole
thing. I put the board with the Arduinos in a case, and made some holes in it to pass the cables.
I made the box as tight as possible as it is for outside. As we are in winter, I don't have a
heating problem of locking all Arduinos in the box.

Power comes from an external 230VAC to 5VDC/15A. I never measured the power consumption. It has
power the Raspberry, the Arduinos and the 610 LEDs, where each LED is in fact 3 LEDs. The
Raspberry is powered form the Arduino board, the LEDs are powered from the Arduino board too.
I should have bought a larger box, instead of having 3 boxes for: Arduinos, Raspberry, and
power supply. The 3 boxes are inserted with a simple timer, power cords, and the power supply
for the other static LEDs in a larger box. The timer turns the whole thing on/off at night.

The Arduino <=> Raspberry interface is I2C. I write in the Arduino EPROM an ID for the I2C bus.
This is done once, and the ID is used as the ID for the I2C bus. Sometimes the communication of
this bus fails. I think it might be a problem with the Raspberry not being ready to handle
something on the I2C bus. But I didn't investigate further. I built a confirmation mechanism.

The Raspberry Pi (model B rev2) is connected on one side to the Arduino board, and on the other
side via a USB WiFi adapter to the home network. It has a static IPv4 address (192.168.1.87).
IPv6 is available, but more complicated to use as my ISP changes it from time to time. The
Raspberry is the I2C master, while the Arduinos are slaves.


Software on Arduino

The software of the Arduinos is written in C, including a library to control the LEDs. I used
the Arduino IDE. There are two programs. One of the is used only once when I write the Arduino
ID to EPROM address 0. The other program reads EPROM address 0 to finds its I2C address.

The Arduino is controlled by a set of commands received from the Raspberry. Each command has an
LED effect and a set of parameters. The main loop of the Arduino plays out a complete received
command. Commands are received via interrupt handler. The Arduino informs the Raspberry over the
I2C bus the state of execution of commands. This allows the Raspberry to recover from errors
over the I2C bus. For example if the command is incomplete, the Raspberry completes the missing
bytes. My main problem was with the I2C bus. The commands are 5 bytes long, and sometimes the
Arduino only receives 4, or 3, or 2, or 1 byte, and waits, and waits, and waits...


Software on Raspberry

The software on the Raspberry can be divided in two groups. The modules used to send commands
to the Arduinos (loader and cronjob) and the modules used to create playlists (web and composer)
that are read by the loader. The playlists (file: .dat) are a set of commands that describe a
sequence of commands to be sent to the Arduinos.

The playlists are a set of lines in a file. Each line describes either a complete frame of 10
balls (each ball with RGB) plus the effect for loading each ball and the effect when the ball is
shown. A line can contain the time the loader should wait before sending the next line to the
Arduinos. A line can also contain the change of a single ball color. I did not use this single
ball instructions. As the communication Raspberry <=> Arduino is not reliable, sometimes one
of the balls has the wrong color. Loading a complete frame (all 10 balls) reduces the wrong
color for just the interval until the next frame.

The loader is called by either the cronjob or by the WEB server. The cronjob is called
every minute. It verifies if there is a loader running by killing the running process with
the PID stored in loader.pid. This avoids that two loaders run in parallel. The cronjob
also verifies if the WEB is being used by verifying the date of the data.dat file. The
loader is only called if the data.dat is more than 2 minutes old. This avoids that the
WEB design is overwritten by the cronjob time triggered loader.

The cronjob is a Python script. Once it is executed, after the PID kill and the data.dat check,
it selects a random playlist file from the /var/www/html/playlist folder.  There is no check
to avoid that the loader plays similar files one after the other. This remains for further
work.

The loader is called by passing as a parameter the filename of the playlist to be played.
The loader reads the playlist line by line and interprets the line. Each line results in
commands to the respective Arduinos. The loader sends the commands to each Arduino and
reads from the Arduino the result of the command. The loader logs its activities to the
loader.log file. the cronjob verifies the size of the log file. Once it reaches a certain
size it is deleted. This should be improved to a rolling logfile. I used it mostly for
debugging purposes.

There are several composer that create several different playlists. Some composers create
more than one playlist. The quality of these Python scripts could be improved. They have
been built more out of "trial and error" than on design. If I have time I'll clean it up.
A description of playlists and effect follows.

The WEB module is built around an apache web server and has 3 components: html web page, a
javascript and a PHP web page. The html web page presents a default color for the 10 balls.
The javascript allows the selection of the color for each ball. The web page also has a
form field for the selection of effects on starting the colors and effects to be shown
during the presentation of the colors. The PHP is called from a html form. It writes into
the data.dat file the color for each ball, with the effects.


Effects and playlist composer

The Arduinos can perform the following effects on each ball:
- roll-in, where one LED is lit after the other. Basically the new color rolls from outside
ring to the central LED.
- In-out. First the central LED gets the new color, than the inner ring, then the 2nd
inner ring, ..., outer ring.
- Fading. The new color does not shows up at once, but the brightness is gradually increased.
- Random. The new LEDs get the new color one by one, with a random selection of the LED
order.

The Arduino can add the following effects once the Ball has a specific color:
- Blinking. Each 100 ms one random LED of the ball becomes the color white, and 100 ms
later it returns to the original color.
- pulsing. Every 10 seconds the ball fades away by reducing the brightness of the colors
and bringing the color back by restoring the brightness.

There are a set of playlist composers. Each one generates one or more playlist.dat files:
- SingleColor creates a set of playlists with single color balls.
- Multicolor creates a set of playlists with multiple colors.
- RunningDots creates a sequence of frames (10 balls) where two balls with the same color
force a third ball of a different color to the corner.
- CandyCrush creates a playlist where balls "fall" from the top and once two balls with
similar color are next to each other they get deleted. When there is no ball to be
deleted it removes randomly one of the balls of the lowest row.

More effects remain to be developed. The code of the composers needs improvement to
increase readability. 
