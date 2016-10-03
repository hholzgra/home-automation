import os
from Screens.Screen import Screen
from Components.MenuList import MenuList
from Components.ActionMap import ActionMap
from Screens.MessageBox import MessageBox
from Plugins.Plugin import PluginDescriptor



class HdmiSwitch(Screen):
    skin = """<screen position="100,150" size="460,400" title="HDMI Quellen" >
                  <widget name="myMenu" position="10,10" size="420,380" scrollbarMode="showOnDemand" />
              </screen>"""
              
    def sendCmd(self, cmd1, cmd2):
        device1 = "/dev/ttyS0"
        device1_options = "-hupcl 19200"
       
        os.system("stty %s -F %s" % (device1_options, device1))
        f1 = open(device, "w")
        f1.write(cmd1+"\n")
        f1.close()

        device2 = "/dev/ttyS0"
        device2_options = "-hupcl 9600"

        os.system("stty %s -F %s" % (device2_options, device2))
        f2 = open(device, "w")
        f2.write(" "+cmd2+"\n")
        f2.close()


    def __init__(self, session, args =0):
        self.session = session
       
        # switch to first port, assuming that this is the Sat receiver port
        # to make sure the menu becomes visible
        self.sendCmd("swi01o01", "A")
        
        list = []
        list.append(("SAT-Fernsehn",     "swi01o01", "A"));
        list.append(("AppleTV",          "swi02o01", "B"));
        list.append(("DVD-Player",       "swi03o01", "C"));
        list.append(("Raspberry Pi",     "swi04o01", "D"));
        list.append(("ChromeStick",      "swi05o01", "E"));
        list.append(("-- frei --",       "swi06o01", "F"));
        list.append(("Amazon FireStick", "swi07o01", "G"));
        list.append(("Laptop",           "swi08o01", "H"));
        
        Screen.__init__(self, session)
        self["myMenu"] = MenuList(list)
        self["myActionMap"] = ActionMap(["SetupActions"],
                                        {
                                            "ok": self.go,
                                            "cancel": self.cancel
                                        } , -1)
        
        
    def go(self):
        retVal1 = self["myMenu"].l.getCurrentSelection()[1]
        retVal2 = self["myMenu"].l.getCurrentSelection()[2]

        if returnValue is not None:
            self.sendCmd(retVal1, retVal2)
            
        self.close(None)
        
    def cancel(self):
        self.close(None)




                    
def main(session, **kwargs):
    session.open(HdmiSwitch)
    
def Plugins(**kwargs):
    return PluginDescriptor(name="HDMI Switch",
                            description="ATEN VS0801H HDMI Switch RS232 Control",
                            where = PluginDescriptor.WHERE_PLUGINMENU,
                            fnc=main)

