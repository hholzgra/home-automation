# Simple plugin to allow selecting HDMI input port on a ATEN VS0801H HDMI switch
# Author: Hartmut Holzgraefe <hartmut@php.net>
# 
# On activation the plugin does the following:
#
# * activate HDMI input port one on the switch to make sure the selection
#   menu will be visible (assuming that the receiver will always be on
#   input port one)
#
# * show a select menu offering the different input source names
#   (so far hardcoded in the plugin source code)
#
# * switch to selected HDMI input port
#
#
# TODO:
#
# * make several things configurable via a setup screen:
#   * names of input sources
#   * serial device (a USB2serial device may be used instead of direct RS232)
#   * HDMI port number for the receiver itself instead of fixed port #1
# 
# * assign to a remote control key directly instead of relying on the 
#   "Quickbutton" plugin for this
#
# * if the ATEN switch ever supports this: read out HDMI port signal / power
#   states and only offer those ports for selection that are actually active
#
# * read out active input port first, and switch back to that port on [Cancel]
#
# * verify that the selected port was indeed activated, retry a few times if not
#
# * allow quick selection of list item by number

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
              
    def sendCmd(self, cmd):
        fullCmd = "echo " + cmd + " > /dev/ttyS0"
        print fullCmd + "\n"
        os.system("stty -hupcl 19200 -F /dev/ttyS0")
        os.system(fullCmd)
       

    def __init__(self, session, args =0):
        self.session = session
       
        # switch to first port, assuming that this is the Sat receiver port
        # to make sure the menu becomes visible
        self.sendCmd("swi01o01")
        
        list = []
        list.append(("SAT-Fernsehn",     "swi01o01"));
        list.append(("AppleTV",          "swi02o01"));
        list.append(("DVD-Player",       "swi03o01"));
        list.append(("Raspberry Pi",     "swi04o01"));
        list.append(("ChromeStick",      "swi05o01"));
        list.append(("-- frei --",       "swi06o01"));
        list.append(("Amazon FireStick", "swi07o01"));
        list.append(("Laptop",           "swi08o01"));
        
        Screen.__init__(self, session)
        self["myMenu"] = MenuList(list)
        self["myActionMap"] = ActionMap(["SetupActions"],
                                        {
                                            "ok": self.go,
                                            "cancel": self.cancel
                                        } , -1)
        
        
    def go(self):
        returnValue = self["myMenu"].l.getCurrentSelection()[1]

        if returnValue is not None:
            self.sendCmd(returnValue)
            
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

