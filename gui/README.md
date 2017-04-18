# Installing Python with Tkinter support on Ubuntu

1. Download Python-2.7.13

	```bash
	wget https://www.python.org/ftp/python/2.7.13/Python-2.7.13.tgz
	tar -xzvf Python-2.7.13.tgz
	```

2. Install the tk-dev package

	```bash
	sudo apt install tk-dev
	```

3. Build and install Python

	```bash
	cd Python-2.7.13
	./configure
	make
	sudo make install
	```

4. ?????

5. Profit!!!