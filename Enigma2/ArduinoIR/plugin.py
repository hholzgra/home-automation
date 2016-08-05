from Plugins.Plugin import PluginDescriptor
from Components.config import config
from Components.SystemInfo import SystemInfo
import os
import os.path

def main(session, **kwargs):
	print "\nArduinoIR PLUGINMENU\n"

def autostart(reason, **kwargs):
        if reason == 0:
          print "\nArduinoIR AUTOSTART 0\n"
        else:
          print "\nArduinoIR AUTOSTART 1\n"

def leaveStandby():
        if os.path.exists("/dev/ttyUSB0"):
          os.system("stty -hupcl -F /dev/ttyUSB0")
          f = open("/dev/ttyUSB0", "w")
          f.write(" 1\n")
          f.close()

def standbyCounterChanged(configElement):
	from Screens.Standby import inStandby
	inStandby.onClose.append(leaveStandby)
        if os.path.exists("/dev/ttyUSB0"):
          os.system("stty -hupcl -F /dev/ttyUSB0")
          f = open("/dev/ttyUSB0", "w")
          f.write(" 0\n")
          f.close()

def Plugins(**kwargs):
	config.misc.standbyCounter.addNotifier(standbyCounterChanged, initial_call = False)

 	return [
                PluginDescriptor(
		  name="ArduinoIR",
		  description="control external devices via attached Arduino",
		  where = PluginDescriptor.WHERE_PLUGINMENU,
		  fnc=main),
	        PluginDescriptor(
		  where =  PluginDescriptor.WHERE_AUTOSTART,
		  fnc = autostart)
               ]
