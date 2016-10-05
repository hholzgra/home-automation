Enigma2 plugin that interfaces with Arduino IR module
=====================================================

This plugin hooks into receiver wakeup and standby transitions
and sends serial commands to the Arduino board that controls
the projector and motor screen.

USB2Serial installation
-----------------------

Install and load required kernel modules:

-----
opkg kernel-module-usbserial kernel-module-ftdi-sio
depmod -a
modprobe usbserial ftdi_sio
-----

Make sure the modules are loaded at boot time by creating
a file named `usbserial.conf` in `/etc/modprobe.d/`:

-----
usbserial
ftdi_sio
-----

