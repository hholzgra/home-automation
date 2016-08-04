Arduino serial controlled infrared sender
=========================================

Automation tool to move down and up a motor screen and
switch on and off a projector, triggered by simple serial
commands sent by an Enigma2 plugin whenever the TV receiver
wakes up or goes back to standby.


Files
-----

my-remote.ino - Arduino project file containing source code
nano-ir.fzz   - Fritzing project for the Arduino board setup
nano-ir.png   - PNG export of the Fritzing schematics


Devices
-------

* Arduino Nano with a few external parts on a breadboard
* VuPlus Duo² SAT TV receiver (a DreamBox clone)
* LG PT1500 Projector
* a no-name motor screen


Funtionality
------------

On receiving a '1' via USB2Serial the motor screen starts
to move down. After 30 seconds, when the screen is about
2/3rd down, the projector is switched on. This is to not
blind the neighbours through the window behind the screen,
but also to give the projector enough time to initialize
and find the HDMI input signal so that it's fully working
when the screen is fully down. After another 17 seconds
the screen is stopped as it has reached the final position
right above the window sill.

On receiving a '0' the projector is switched off and the
screen starts to move up. After 50s the screen is stopped.
The screen is slightly slower when moving up, but 50s is
more than enough to fully go up for sure.


TODO
----

Right now the activation and deactivation sequences are
are blocking. So if the receiver got sent to sleep by
accident, and is woken up right away again the screen
will fully go up, then down again and the projector
will be off for most of the time.

Similarily when turned on by accident the screen will
move down and up again for almost two minutes total,
and the projector will be active for 17 seconds.


This was sort of OK with the original projector as the
lamp needed some warmup and cooldown time anyway. The
current projector uses a LED light source though so it
can be turned on and off again without delays.

So an improved implementation would use a state machine
and would keep track of screen up and down movement time
to be able to reverse operation at any time instead of
fully performing the "up" or "down" sequence before
processing the next command.