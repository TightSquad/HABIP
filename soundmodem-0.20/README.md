# Building soundmodem-0.20 on Linux

1. Install pre-reqs:
	
	```bash
	$ sudo apt update
	$ sudo apt install libasound2-dev libxml2-dev libgtk2.0-dev libaudiofile-dev
	```

2. Download and extract source code (if using original source):

	```bash
	wget http://download.gna.org/soundmodem/soundmodem-0.20.tar.gz
	tar -xvzf soundmodem-0.20.tar.gz
	```

3. Configure and build soundmodem

	```bash
	cd soundmodem-0.20
	./configure
	make
	```
