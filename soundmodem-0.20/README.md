# Building soundmodem-0.20 on Linux

1. Install pre-reqs:
	
	```bash
	$ sudo apt update
	$ sudo apt install libasound2-dev libxml2-dev libgtk2.0-dev libaudiofile-dev autoconf
	```

2. Configure and build soundmodem

	```bash
	cd soundmodem-0.20
	./configure
	make
	```
