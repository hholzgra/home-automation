from Plugins.Plugin import PluginDescriptor
from Components.config import config
from Components.SystemInfo import SystemInfo
from Screens.Standby import inStandby
import os
import os.path

# the standby and wakeup hooks are not really simple / intuitive
# see https://www.dream-multimedia-tv.de/board/index.php?page=Thread&postID=102386#post102386

# plugin main entry point, doesn't really do anything besides printing a log message
def main(session, **kwargs):
	print "\nArduinoIR PLUGIN\n"

# send a string to the arduino via usb2serial
def sendCommand(cmd):
	device = "/dev/ttyUSB0"

        if os.path.exists(device):
          # we need to repeat this every time as the arduino 
	  # may have been pulled and re-attached between commands
          os.system("stty -hupcl -F " + device)

          f = open(device, "w")
          f.write(cmd)
          f.close()

# when leaving standby we send the activation command to the arduino
# this callback is set up by instandby.onClose below
def leaveStandby():
	# "activate" command
	sendCommand(" 1\n")

# when entering standby we send the deactivation command to the arduino
# and set up the leaveStandby callback above to be called when standby ends
def standbyCounterChanged(configElement):
	# "deactivate" command
        sendCommand(" 0\n")

	# register "leaveStandby" callback
	inStandby.onClose.append(leaveStandby)

# plugin registration
def Plugins(**kwargs):
	# hook into standby notification events
	config.misc.standbyCounter.addNotifier(standbyCounterChanged, initial_call = False)

        # register the plugin
 	return [
                PluginDescriptor(
		  name="ArduinoIR",
		  description="control external devices via attached Arduino",
		  where = PluginDescriptor.WHERE_PLUGINMENU,
		  fnc=main)
               ]
