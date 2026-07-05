from Plugins.Plugin import PluginDescriptor
from Components.config import config
from Components.SystemInfo import SystemInfo
import Screens.Standby
import os
import os.path

# Arduino tty device
arduino_tty = "/dev/ttyACM0"

# Denon AVC-S670H Amplifer settings
amplifier_host     = "192.168.23.114"
amplifier_port     = "11080"
amplifier_protocol = "http"
amplifier_path     = "/ajax/globals/set_config"
amplifier_url      = amplifier_protocol + "://" + amplifier_host + ":" + amplifier_port + amplifier_path

# the standby and wakeup hooks are not really simple / intuitive
# see https://www.dream-multimedia-tv.de/board/index.php?page=Thread&postID=102386#post102386

# plugin main entry point, doesn't really do anything besides printing a log message
def main(session, **kwargs):
        print "\n[ArduinoIR] main\n"

# send a string to the arduino via usb2serial
def sendCommand(cmd):
        print "[ArduinoIR] sendCommand '%s'" % cmd

        if os.path.exists(device):
          # we need to repeat this every time as the arduino 
          # may have been pulled and re-attached between commands
          os.system("stty -hupcl -F " + arduino_tty)

          f = open(arduino_tty, "w")
          f.write(cmd)
          f.close()

# when leaving standby we send the activation command to the arduino
# this callback is set up by instandby.onClose below
def leaveStandby():
        print "[ArduinoIR] leaveStandby"
        # HDMI switch to input #1
        sendCommand(" AAA\n")

        # "activate" command
        sendCommand(" 1\n")

        # wake up amplifier
        os.system("wget '" + amplifier_url + "?type=4&data=<MainZone><Power>1</Power></MainZone>'")

        # switch amplifier to receiver input
        os.system("wget '" + amplifier_url + "?type=7&data=<Source zone=\"1\" index=\"1\"></Source>'")

# when entering standby we send the deactivation command to the arduino
# and set up the leaveStandby callback above to be called when standby ends
def standbyCounterChanged(configElement):
        print "[ArduinoIR] standbyCounterChanged"
        # "deactivate" command
        sendCommand(" 0\n")

        # suspend amplifier
        os.system("wget " + amplifier_url + "?type=4&data=<MainZone><Power>3</Power></MainZone>'")

        if not Screens.Standby.inStandby:
            print "[ArduinoIR] no standby"
        else:
            print "[ArduinoIR] standby"

        # register "leaveStandby" callback
        Screens.Standby.inStandby.onClose.append(leaveStandby)

def autostart(reason, **kwargs):
        print "[ArduinoIR] autostart...."
        if reason == 0:
                print "[ArduinoIR] reason == 0"
                # hook into standby notification events
                config.misc.standbyCounter.addNotifier(standbyCounterChanged, initial_call = False)


# plugin registration
def Plugins(**kwargs):
        print "[ArduinoIR] Plungin init...."
        # register the plugin
        return [
                PluginDescriptor(
                  name="ArduinoIR",
                  description="control external devices via attached Arduino",
                  where = PluginDescriptor.WHERE_PLUGINMENU,
                  icon = "arduino-IR.png",
                  fnc=main),
                PluginDescriptor(
                  where = PluginDescriptor.WHERE_SESSIONSTART, 
                  fnc = autostart
                )
               ]
