/*
  my_remote: send infrared remote control codes to various devices

  sending infrared commands based on serial input
*/

void my_debug(char *msg)
{
//    Serial.println(msg);
}

#include <IRremote.h>

IRsend irsend;

/* Beamer codes - LG PF1500 */

/* we only need the */
const unsigned long beamer_power_toggle = 0x20F0B54AL;


/* motor screen raw code arrays */

#define SCREEN_CMD_LEN 49

unsigned int screen_up[SCREEN_CMD_LEN] = {
  550, 1400, 1600,  450,  550, 1450, 1550,  450,  550, 1450,
 1550,  450,  550, 1450, 1600,  450,  550, 1400, 1600,  450,
  550, 1450, 1550,  450,  550, 1450, 1600,  400,  600, 1400,
 1600,  450, 1550,  450, 1600,  450,  550, 1450,  550, 1450,
  550, 1450,  550, 1450,  550, 1450,  550, 1450,  550
};

unsigned int screen_stop[SCREEN_CMD_LEN] = {
  550, 1450, 1550,  450,  550, 1450, 1550,  450,  550, 1450,
 1550,  450,  550, 1450, 1600,  450,  550, 1450, 1550,  450,
  550, 1450, 1550,  450,  550, 1450, 1600,  450,  550, 1450,
 1550,  450,  550, 1450,  550, 1450, 1550,  450, 1600,  450,
  550, 1450,  550, 1450,  550, 1450,  550, 1450,  550
};

unsigned int screen_down[SCREEN_CMD_LEN] = {
  550, 1450, 1550,  450,  550, 1450, 1550,  450,  550, 1450,
 1550,  450,  600, 1400, 1600,  450,  550, 1450, 1550,  450,
  550, 1450, 1550,  450,  550, 1450, 1600,  450,  550, 1450,
 1550,  450,  550, 1450,  550, 1450,  550, 1450,  550, 1450,
  550, 1450,  550, 1450, 1600,  450, 1550,  450,  550
};


void send_screen(unsigned int cmd[])
{
  /* screen commands need to be sent 3 times in a row */
  for (int i = 0; i < 3; i++) {
    irsend.sendRaw(cmd, SCREEN_CMD_LEN, 38 /* Hz */);
    delay(40);
  }
}

void blink(int n)
{
  while(n--) {
    digitalWrite(LED_BUILTIN, HIGH);  // turn the LED on (HIGH is the voltage level)
    delay(1000);                      // wait for a second
    digitalWrite(LED_BUILTIN, LOW);   // turn the LED off by making the voltage LOW
    delay(1000);
  }                      // wait for a second
}

// activation sequence: move screen down and turn on projector
void activate()
{
  my_debug("activate: start");

  /* start to move down the screen */
  my_debug("activate: screen down");
  send_screen(screen_down);

  /* wait until it is down by ca. 2/3rds      */
  /* (far enough to not blind the neighbours) */
  delay(30000);

  /* switch projector on */
  my_debug("activate: projector down\n");
  irsend.sendNEC(beamer_power_toggle, 32);

  /* wait until screen is fully down (47.1s total) */
  delay(17100);

  /* stop screen */
  my_debug("activate: stop screen\n");
  send_screen(screen_stop);

  my_debug("activate: done\n");
}

// shutdown sequence: turn off projector and move screen up */
void deactivate()
{
  /* turn of the projector */
  my_debug("deactivate: beamer off");
  irsend.sendNEC(beamer_power_toggle, 32);

  /* start to move up the screen */
  my_debug("deactivate: screen up");
  send_screen(screen_up);

  /* wait until screen is definetly fully up (50s) */
  delay(50000);

  /* stop screen */
  my_debug("deactivate:scren off");
  send_screen(screen_stop);
}

/* Arduino initialization */
void setup()
{
  Serial.begin(9600);
  while (! Serial) {} /* Wait untilSerial is ready - Leonardo */      
  my_debug("Hello World!\n");
  blink(5);
}

int screen_state = -1; /* 'unknown' */

unsigned long hdmi_codes [] = {
  0x00FF20DF,
  0x00FFA05F,
  0x00FF609F,
  0x00FF7887,
  0x00FFE01F,
  0x00FF10EF,
  0x00FF906F,
  0x00FFD827,
};

void switch_hdmi(int chan)
{
  my_debug("HDMI ");
  my_debug(chan);

  irsend.sendNEC(hdmi_codes[chan], 32);
}


/* Arduino main loop */
void loop()
{
  if (Serial.available())
    {
      char ch = Serial.read();

      switch(ch) {
      case '1':
      my_debug("#1: ON");
      if (screen_state != 1) {
          screen_state = 1;
          activate();
        }
        break;

      case '0':
        if (screen_state != 0) {
          screen_state = 0;
          deactivate();
        }
        break;

      case 'A':
      case 'B':
      case 'C':
      case 'D':
      case 'E':
      case 'F':
      case 'G':
      case 'H':
        switch_hdmi(ch - 'A');
        break;

      case 'X':
        blink(3);
        break;

      default:
        break;
      }
    }
}
