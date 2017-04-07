#!/usr/bin/env python

"""
file: temp_pct2075.py
author: Chris Schwab
project: High Altitude Balloon Instrumentation Platform
description: API for the PCT2075 digital temperature sensor on the RasPi HAT Board
"""

# sudo apt-get install python-smbus
import smbus

import sys

import time

# Custom i2c class
from i2c import i2c


class tempSensorPCT2075(i2c):
	"""
	Abstract the PCT2075 digital temperature sensor
	DataSheet found here:
		http://www.nxp.com/documents/data_sheet/PCT2075.pdf
	"""

	# Register Addresses
	REG_TEMP  = 0x0	# W: r/w, Temperature register: contains two 8-bit data bytes; to store the measured Temp data [15:5].
	REG_CONF  = 0x1	# B: r/w, Configuration register: contains a single 8-bit data byte; to set the device operating condition; default = 0.
	REG_THYST = 0x2	# W: r/w, Hysteresis register: contains two 8-bit data bytes; to store the hysteresis Thys limit; default = 75 C.
	REG_TOS   = 0x3	# W: r/w, Overtemperature shutdown threshold register: contains two 8-bit data bytes; to store the overtemperature shutdown Tots limit; default = 80 C.
	REG_TIDLE = 0x4	# B: r/w, Temperature conversion cycle default to 100 ms.

	def __init__(self, address=None, busID=None, interface=None):
		# Call super init
		super(self.__class__, self).__init__(address, busID, interface)

		# Make a device logger
		self.deviceLogger = self.baseLogger.getLogger(("tempSensorPCT2075@"+str(hex(address))))
		self.deviceLogger.log.info("Instantiated tempSensorPCT2075@"+str(hex(address)))


	def readTempCF(self):
		"""
		Read the temperature sensor value.
			RETURNS list of floats: [temp_c,temp_f]
		"""

		# varaibles for temperature data
		temperature_c = None
		temperature_f = None
		# read temp value from sensor
		temperature = self.readWordSwapped(tempSensorPCT2075.REG_TEMP)
		# check to make sure data is valid
		if (temperature == None):
			self.deviceLogger.log.error("Could not read temp register: {}".format(
				hex(tempSensorPCT2075.REG_TEMP)))
			# return None
			return [None, None]
		else:
			self.deviceLogger.log.debug("Read {} from register: {}".format(
				hex(temperature), tempSensorPCT2075.REG_TEMP))
			# shift value since temp is the most significant 11 bits
			temperature_shifted = temperature >> 5
			# if MSB == 1 (11bit value) then result is negative (convert from 2's comp)
			if (temperature_shifted & 0x400):
				# convert from 2s comp --> invert (aka XOR with all 1s) then add 1. and make sure to mask for only 11 bits
				temperature_shifted_2s_comp = ((temperature_shifted ^ 0xFFFF) & 0x7FF) + 1
				# convert to celcius and throw on a minus sign
				temperature_c = (-1) * (temperature_shifted_2s_comp * 0.125)
				# convert to fahrenheit
				temperature_f = temperature_c * (9.0/5.0) + 32
			else:
				# convert shifter value to celcius (value * 0.125)
				temperature_c = temperature_shifted * 0.125
				# convert celcius to fahrenheit
				temperature_f = temperature_c * (9.0/5.0) + 32

			return [temperature_c, temperature_f]

################################################################################

# Just some testing
if __name__ == "__main__":
	
	# i2c bus object
	bus = smbus.SMBus(1)

	# sensor addresses
	temp0_addr = 0x48	# right-side temp sensor
	temp1_addr = 0x4A	# left side temp sensor

	temp0 = tempSensorPCT2075(temp0_addr, None, bus)
	temp1 = tempSensorPCT2075(temp1_addr, None, bus)

	while(1):
		print temp0.readTempCF()
		print temp1.readTempCF()
		time.sleep(1)

	sys.exit(1)
