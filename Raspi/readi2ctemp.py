#!/usr/bin/python
import time
import i2ctemp
from i2ctemp import setupI2Cbus
from i2ctemp import readTempF

while 1:
	readTempF()
	time.sleep(5)
