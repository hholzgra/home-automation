clean:
	rm -f \#*

install:
	@echo "run 'make install-duo' or 'install-duo2' instead"

install-duo2:
	scp -r -O -o HostKeyAlgorithms=+ssh-rsa -o PubkeyAcceptedAlgorithms=+ssh-rsa . root@192.168.23.100:/usr/lib/enigma2/python/Plugins/Extensions/ArduinoIR

install-duo:
	scp -r -O -o HostKeyAlgorithms=+ssh-rsa -o PubkeyAcceptedAlgorithms=+ssh-rsa . root@192.168.23.110:/usr/lib/enigma2/python/Plugins/Extensions/ArduinoIR


