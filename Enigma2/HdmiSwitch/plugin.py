import os
from Screens.Screen import Screen
from Components.MenuList import MenuList
from Components.ActionMap import ActionMap, NumberActionMap
from Screens.MessageBox import MessageBox
from Plugins.Plugin import PluginDescriptor



class HdmiSwitch(Screen):
    skin = """<screen position="100,150" size="460,400" title="HDMI Quellen" >
                  <widget name="myMenu" position="10,10" size="420,380" scrollbarMode="showOnDemand" enableWrapAround="1" />
              </screen>"""
              
    def sendCmd(self, cmd):
        print "CMD '%s'" % cmd
        device = "/dev/ttyUSB0"
        device_options = "-hupcl 9600"

        os.system("stty %s -F %s" % (device_options, device))
        f = open(device, "w")
        f.write(" ")
        f.write(cmd)
        f.write(cmd)
        f.write(cmd)
        f.write("\n")
        f.close()

    def __init__(self, session, args =0):
        self.session = session
       
        # switch to first port, assuming that this is the Sat receiver port
        # to make sure the menu becomes visible
        self.sendCmd("A")
        
        list = []
        list.append(("1 SAT-Fernsehn",     "A"));
        list.append(("2 AppleTV",          "B"));
        list.append(("3 DVD-Player",       "C"));
        list.append(("4 Raspberry Pi",     "D"));
        list.append(("5 ChromeStick",      "E"));
        list.append(("6 -- frei --",       "F"));
        list.append(("7 Amazon FireStick", "G"));
        list.append(("8 Laptop-Kabel",     "H"));
        
        Screen.__init__(self, session)
        self["myMenu"] = MenuList(list)
        self["myActionMap"] = NumberActionMap(["SetupActions", "InputActions"],
                                        {
                                            "ok": self.go,
                                            "cancel": self.cancel,
                                            "1": self.keyNumber,
                                            "2": self.keyNumber,
                                            "3": self.keyNumber,
                                            "4": self.keyNumber,
                                            "5": self.keyNumber,
                                            "6": self.keyNumber,
                                            "7": self.keyNumber,
                                            "8": self.keyNumber,
                                        } , -1)
        
        
    def go(self):
        selection = self["myMenu"].l.getCurrentSelection()[1]

        if selection is not None:
            self.sendCmd(selection)
            
        self.close(None)
        
    def keyNumber(self, number):
	self.sendCmd(str(chr(number + ord('A') - 1)))
        self.close(None)

    def cancel(self):
        self.close(None)




                    
def main(session, **kwargs):
    session.open(HdmiSwitch)
    
def Plugins(**kwargs):
    return PluginDescriptor(name="HDMI Switch",
                            description="ATEN VS0801H HDMI Switch RS232 Control",
                            where = PluginDescriptor.WHERE_PLUGINMENU,
			    icon = "arduino-HDMI.png",
                            fnc=main)

