#!/usr/bin/env python

"""
file: humid_si7021.py
author: Chris Schwab
project: High Altitude Balloon Instrumentation Platform
description: API for the SI7021 digital humidity sensor on the RasPi HAT Board
"""

# sudo apt-get install python-smbus
import smbus

import sys

import time

# Custom i2c class
from i2c import i2c


class humidSensorSI7021(i2c):
	"""
	Abstract the SI7021 digital humidity sensor
	DataSheet found here:
		http://www.silabs.com/documents/public/data-sheets/Si7021-A20.pdf
	"""

	# Register Addresses and Bit Masks
	#
	# HMM --> clock stretching
	# NHMM --> not ack read requests
	#
	REG_MEAS_REL_HUMID_HMM  = 0xE5 	# W: w  : Measure Relative Humidity, Hold Master Mode (also triggers a Temp measurement, use reg 0xE0 to read it)
	REG_MEAS_REL_HUMID_NHMM = 0xF5 	# W: w  : Measure Relative Humidity, No Hold Master Mode (also triggers a Temp measurement, use reg 0xE0 to read it)
	REG_MEAS_TEMP_HMM       = 0xE3 	# W: w  : Measure Temperature, Hold Master Mode (this takes a new temperature measurement)
	REG_MEAS_TEMP_NHMM 		= 0xF3 	# W: w  : Measure Temperature, No Hold Master Mode (this takes a new temperature measurement)
	REG_PREV_TEMP_VALUE 	= 0xE0 	# W: w  : Read Temperature Value from Previous RH Measurement
	REG_RESET 				= 0xFE 	# B: w  : Reset
	REG_WRITE_USER_REG1 	= 0xE6 	# B: w  : Write RH/T User Register 1

									# 		Set RES[1:0] = 00 for 12bit RH / 14bit Temp conv. Total time = t_convRH + t_convT = 12ms + 10.8ms = 22.8ms MAX
	USER_REG_RES1 			= 0x80 	# r/w 	: Measurement resolution bit 1
	USER_REG_RES0 			= 0x01 	# r/w 	: Measurement resolution bit 0
	USER_REG_VDDS 			= 0x40 	# r 	: Vdd Status (0 = Vdd OK, 1 = Vdd low)
	USER_REG_HTRE 			= 0x04 	# w/r 	: On-chip heater enable (0 = disable, 1 = enable)

	REG_READ_USER_REG1 		= 0xE7 	# B: w  : Read RH/T User Register 1
	REG_WRITE_HEAT_CTRL 	= 0x51 	# B: w  : Write Heater Control Register (HEATER[3:0] sets heater power)
	REG_READ_HEAT_CTRL 		= 0x11 	# B: w  : Read Heater Control Register

	def __init__(self, address=None, busID=None, interface=None):
		# Call super init
		super(self.__class__, self).__init__(address, busID, interface)

		# Make a device logger
		self.deviceLogger = self.baseLogger.getLogger(("humidSensorSI7021@"+str(hex(address))))
		self.deviceLogger.log.info("Instantiated humidSensorSI7021@"+str(hex(address)))


	def readHumidTemp(self):
		"""
		Read the temperature sensor value.
			RETURNS list of floats: [relhumid, temp_c,temp_f]
		"""

		# trigger humidity/temperature measurement with manual delay for conversion time (NHMM)
		write_status = self.sendWrite(humidSensorSI7021.REG_MEAS_REL_HUMID_NHMM)
		if (write_status == False):
			return [None, None, None]

		# wait for conversion time --> max t_conv = 22.8ms
		time.sleep(0.03)

		# read back humidity MSByte
		rh_byte1 = self.sendRead(self.address)

		# read back humidity LSByte
		rh_byte0 = self.sendRead(self.address)

		# shift to get the rh_code
		rh_code = (rh_byte1 << 8) | (rh_byte0)

		# convert rh_code to %RH
		rh_percent = ((125 * rh_code) / 65536.0) - 6

		# read the temperture value used in the humidity conversion
		temp_code = self.readWordSwapped(humidSensorSI7021.REG_PREV_TEMP_VALUE)

		# convert temp_code to C
		temp_c = ((175.72 * temp_code) / 65536.0) - 46.85
		#convert temp_c to F
		temp_f = temp_c * (9.0/5.0) + 32


		return ["{:07.3f}".format(rh_percent)
				"{:+08.3f}".format(temp_c),
				"{:+08.3f}".format(temp_f)]

################################################################################

# Just some testing
if __name__ == "__main__":
	
	# i2c bus object
	bus = smbus.SMBus(1)

	# sensor addresses
	humid0_addr = 0x40	# SI7021 humidity sensor

	humid0 = humidSensorSI7021(temp0_addr, None, bus)

	while(1):
		print humid0.readHumidTemp()
		time.sleep(1)

	sys.exit(1)
