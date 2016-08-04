/*
 state machine version of the serial to IR command sketch
 */

#include <IRremote.h>

#include "types.h"

IRsend irsend;

/* Vu+ duo codes - RC6*/

const unsigned long long receiver_mute  = 0xC8052260DLL;
const unsigned long long receiver_power = 0xC8052A60CLL;

/* Beamer codes - NEC */

const unsigned long beamer_power_toggle = 0xE1A2E817L;
const unsigned long beamer_power_off    = 0xE1A2E81EL;
const unsigned long beamer_power_on     = 0xE1A2E81DL;

/* motor screen raw code arrays */

unsigned int screen_up[49] = {
  550, 1400, 1600,  450,  550, 1450, 1550,  450,  550, 1450, 
 1550,  450,  550, 1450, 1600,  450,  550, 1400, 1600,  450, 
  550, 1450, 1550,  450,  550, 1450, 1600,  400,  600, 1400, 
 1600,  450, 1550,  450, 1600,  450,  550, 1450,  550, 1450, 
  550, 1450,  550, 1450,  550, 1450,  550, 1450,  550
};

unsigned int screen_stop[49] = {
  550, 1450, 1550,  450,  550, 1450, 1550,  450,  550, 1450, 
 1550,  450,  550, 1450, 1600,  450,  550, 1450, 1550,  450, 
  550, 1450, 1550,  450,  550, 1450, 1600,  450,  550, 1450, 
 1550,  450,  550, 1450,  550, 1450, 1550,  450, 1600,  450, 
  550, 1450,  550, 1450,  550, 1450,  550, 1450,  550
};
  
unsigned int screen_down[49] = {
  550, 1450, 1550,  450,  550, 1450, 1550,  450,  550, 1450, 
 1550,  450,  600, 1400, 1600,  450,  550, 1450, 1550,  450,
  550, 1450, 1550,  450,  550, 1450, 1600,  450,  550, 1450, 
 1550,  450,  550, 1450,  550, 1450,  550, 1450,  550, 1450,  
  550, 1450,  550, 1450, 1600,  450, 1550,  450,  550  
};


enum state_t state = STATE_OFF;

static const char *state_name(enum state_t state)
{
  switch (state) {
  case STATE_OFF:     return "OFF ";
  case STATE_ON:      return "ON  ";
  case STATE_DOWN:    return "DOWN";
  case STATE_WAIT:    return "WAIT";
  case STATE_UP:      return "UP  ";
  case STATE_UNKNOWN: return "UNKN";
  default: return "(??)";
  }
}

static void set_state(enum state_t s)
{
  if (s != state) {
    Serial.print("Changing state from ");
    Serial.print(state_name(state));
    Serial.print(" to ");
    Serial.println(state_name(s));
  } 
  
  state = s;
}

void setup()
{
  Serial.begin(9600);
  while (! Serial); // Wait untilSerial is ready - Leonardo
}

void send_screen(unsigned int cmd[]) 
{
  for (int i = 0; i < 3; i++) {
    irsend.sendRaw(cmd,49,38);   
    delay(40);
  }
}

unsigned long end_time;

void loop() 
{
  switch (state) {
    case STATE_UNKNOWN:
      if (Serial.available()) {
        switch (Serial.read()) {
          case '0':
            Serial.println("Reading: 0");
            set_state(STATE_WAIT);
            break;
          case '1':
            Serial.println("Reading: 1");
            set_state(STATE_DOWN);
            break;
          default:
            Serial.println("Reading: (???)");
            break;
        }
      }
      break;

    case STATE_OFF:
      if (Serial.available()) {
        switch (Serial.read()) {
           case '0':
             Serial.println("Reading: 0");
             break;
           case '1':
             Serial.println("Reading: 1");
             set_state(STATE_DOWN);
             break;
          default:
            Serial.println("Reading: (???)");
            break;
        }
      }
      break;
    
    case STATE_ON:
      if (Serial.available()) {
        switch (Serial.read()) {
           case '0':
             Serial.println("Reading: 0");
             set_state(STATE_WAIT);
             break;
           case '1':
             Serial.println("Reading: 1");
             break;
          default:
            Serial.println("Reading: (???)");
            break;
        }
      }
      break;
    
    case STATE_DOWN:
      send_screen(screen_down);
      delay(30000);
      irsend.sendNEC(beamer_power_on, 32);
      delay(17000);
      send_screen(screen_stop);
      set_state(STATE_ON);
      break;
    
    case STATE_WAIT:
      delay(5000); 
      while (Serial.available()) {
        switch (Serial.read()) {
           case '0':
             Serial.println("Reading: 0");
             break;
           case '1':
             Serial.println("Reading: 1");
             set_state(STATE_ON);
             break;
          default:
            Serial.println("Reading: (???)");
            break;
        }
      }
      if (state == STATE_WAIT) {
        set_state(STATE_UP);
      }     
      break;
    
    case STATE_UP:
      irsend.sendNEC(beamer_power_off, 32);
      delay(200);
      irsend.sendNEC(beamer_power_off, 32);
      send_screen(screen_up);
      delay(60000);
      send_screen(screen_stop);
      set_state(STATE_OFF);
      break;

    default:
      break;
  }    
}


