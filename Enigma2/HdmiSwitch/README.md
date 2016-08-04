Simple plugin to allow selecting HDMI input port on a ATEN VS0801H HDMI switch
==============================================================================

Author: Hartmut Holzgraefe <hartmut@php.net>


Functionality
-------------

On activation the plugin does the following:

* activate HDMI input port one on the switch to make sure the selection
  menu will be visible (assuming that the receiver will always be on
  input port one)

* show a select menu offering the different input source names
  (so far hardcoded in the plugin source code)

* switch to selected HDMI input port


TODO
----

* make several things configurable via a setup screen:
  * names of input sources
  * serial device (a USB2serial device may be used instead of direct RS232)
  * HDMI port number for the receiver itself instead of fixed port #1

* assign to a remote control key directly instead of relying on the 
  "Quickbutton" plugin for this

* if the ATEN switch ever supports this: read out HDMI port signal / power
  states and only offer those ports for selection that are actually active

* read out active input port first, and switch back to that port on [Cancel]

* verify that the selected port was indeed activated, retry a few times if not

* allow quick selection of list item by number

