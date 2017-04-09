#!/usr/bin/env python

"""
file: press_ms5607.py
author: Chris Schwab
project: High Altitude Balloon Instrumentation Platform
description: API for the MS5607 digital pressure sensor on the RasPi HAT Board
"""

# sudo apt-get install python-smbus
import smbus

import sys

import time

# Custom i2c class
from i2c import i2c


class pressSensorMS5607(i2c):
	"""
	Abstract the MS5607 digital pressure sensor
	DataSheet found here:
		http://www.te.com/commerce/DocumentDelivery/DDEController?Action=srchrtrv&DocNm=MS5607-02BA03&DocType=Data+Sheet&DocLang=English
	"""

	# Register Addresses
	REG_RESET         	= 0x1E 		# B: w  : Reset to load PROM to registers, needed on power up (use data = 0x0)
	REG_CONV_D1_256   	= 0x40 		# B: w  : Write triggers a D1(pressure) conversion with OSR = 256 (use data = 0x0)
	REG_CONV_D1_512   	= 0x42 		# B: w  : Write triggers a D1(pressure) conversion with OSR = 512 (use data = 0x0)
	REG_CONV_D1_1024  	= 0x44 		# B: w  : Write triggers a D1(pressure) conversion with OSR = 1024 (use data = 0x0)
	REG_CONV_D1_2048  	= 0x46 		# B: w  : Write triggers a D1(pressure) conversion with OSR = 2048 (use data = 0x0)
	REG_CONV_D1_4096  	= 0x48 		# B: w  : Write triggers a D1(pressure) conversion with OSR = 4096 (use data = 0x0)
	REG_CONV_D2_256   	= 0x50 		# B: w  : Write triggers a D2(temp) conversion with OSR = 256 (use data = 0x0)
	REG_CONV_D2_512   	= 0x52 		# B: w  : Write triggers a D2(temp) conversion with OSR = 512 (use data = 0x0)
	REG_CONV_D2_1024  	= 0x54 		# B: w  : Write triggers a D2(temp) conversion with OSR = 1024 (use data = 0x0)
	REG_CONV_D2_2048  	= 0x56 		# B: w  : Write triggers a D2(temp) conversion with OSR = 2048 (use data = 0x0)
	REG_CONV_D2_4096  	= 0x58 		# B: w  : Write triggers a D2(temp) conversion with OSR = 4096 (use data = 0x0)
	REG_ADC_READ      	= 0x00 		# L: r  : Burst read from the ADC register (either D1 or D2 value), 24bits = 3 byte list
	REG_PROM_MANU     	= 0xA0 		# W: r  : PROM addr_0, word reserved for manufacturer
	REG_PROM_C1       	= 0xA2 		# W: r  : PROM addr_1, constant C1 = Pressure Sensitivity = SENS_T1
	REG_PROM_C2       	= 0xA4 		# W: r  : PROM addr_2, constant C2 = Pressure Offset = OFF_T1
	REG_PROM_C3       	= 0xA6 		# W: r  : PROM addr_3, constant C3 = Temp Coeff of Pressure Sensitivity = TCS
	REG_PROM_C4       	= 0xA8 		# W: r  : PROM addr_4, constant C4 = Temp Coeff of Pressure Offset = TCO
	REG_PROM_C5       	= 0xAA 		# W: r  : PROM addr_5, constant C5 = Reference temperature = T_REF
	REG_PROM_C6       	= 0xAC 		# W: r  : PROM addr_6, constant C6 = Temp Coeff of the temperature = TEMPSENS
	REG_PROM_CRC      	= 0xAE 		# W: r  : PROM addr_7, CRC value, bitd [3:0]

	# Constants
	PRESSURE0 			= 101325 	# 	average pressure at sea level = 101325 Pa

	def __init__(self, address=None, busID=None, interface=None):
		# Call super init
		super(self.__class__, self).__init__(address, busID, interface)

		# Make a device logger
		self.deviceLogger = self.baseLogger.getLogger(("pressSensorMS5607@"+str(hex(address))))
		self.deviceLogger.log.info("Instantiated pressSensorMS5607@"+str(hex(address)))

		# Sensor PROM Constants
		self.SENS_T1 	= None 		# constant C1 = Pressure Sensitivity
		self.OFF_T1 	= None 		# constant C2 = Pressure Offset
		self.TCS 		= None 		# constant C3 = Temp Coeff of Pressure Sensitivity
		self.TCO 		= None 		# constant C4 = Temp Coeff of Pressure Offset
		self.T_REF 		= None 		# constant C5 = Reference temperature
		self.TEMPSENSE 	= None 		# constant C6 = Temp Coeff of the temperature

	def reset(self):
		"""
		Sends reset to the pressure sensor, ensures PROM is properly loaded to internal registers
			RETURNS boolean of write completion status: True=completed, False=failed
		"""

		# send reset
		write_status = self.sendWrite(pressSensorMS5607.REG_RESET)
		# wait non-zero amount of time for reset
		time.sleep(0.5)

		return write_status

	def readSensorPROM(self):
		"""
		Reads sensor PROM constants C1 through C6 and adjusts C1, C2 and C5
			RETURNS boolean of PROM read completion status: True=completed, False=failed
		"""

		# read C1
		self.SENS_T1 = self.readWordSwapped(pressSensorMS5607.REG_PROM_C1)
		# if read failed
		if (self.SENS_T1 == None):
			return False
		# else adjust the constant
		else:
			self.SENS_T1 = self.SENS_T1 << 16

		# read C2
		self.OFF_T1 = self.readWordSwapped(pressSensorMS5607.REG_PROM_C2)
		# if read failed
		if (self.OFF_T1 == None):
			return False
		# else adjust the constant
		else:
			self.OFF_T1 = self.OFF_T1 << 17

		# read C3
		self.TCS = self.readWordSwapped(pressSensorMS5607.REG_PROM_C3)
		# if read failed
		if (self.TCS == None):
			return False
		# else adjust the constant
		# else:
		# 	self.TCS = self.TCS >> 7 				#NO! shift by 7 AFTER multiplying with dT (see below)

		# read C4
		self.TCO = self.readWordSwapped(pressSensorMS5607.REG_PROM_C4)
		# if read failed
		if (self.TCO == None):
			return False
		# else adjust the constant
		# else:
		# 	self.TCO = self.TCO >> 6 				#NO! shift by 6 AFTER multiplying with dT (see below)

		# read C5
		self.T_REF = self.readWordSwapped(pressSensorMS5607.REG_PROM_C5)
		# if read failed
		if (self.T_REF == None):
			return False
		# else adjust the constant
		else:
			self.T_REF = self.T_REF << 8

		# read C6
		self.TEMPSENS = self.readWordSwapped(pressSensorMS5607.REG_PROM_C6)
		# if read failed
		if (self.TEMPSENS == None):
			return False
		# else adjust the constant
		# else:
		# 	self.TEMPSENS = self.TEMPSENS >> 23      #NO! shift by 23 AFTER multiplying with dT (see below)

		return True

	def readAll (self):
		"""
		Read the temperature (c/f), pressure (mBar, Pa), and calculate altitude (m/ft)
			RETURNS list of floats: [temp_c, temp_f, press_mbar, press_pa, altitude_m, altitude_f]
		"""

		# trigger D1 (digital pressure value) conversion
		write_status = self.sendWrite(pressSensorMS5607.REG_CONV_D1_4096)
		if (write_status == False):
			return [None, None, None, None, None]

		# wait longer than the max ADC conversion time (9.04ms for OSR=4096) or data will be corrupt
		time.sleep(0.01)

		# read the 24-bit (3 byte) ADC pressure result
		adc_pressure = self.readBlock(pressSensorMS5607.REG_ADC_READ, 3)
		if (adc_pressure == None):
			return [None, None, None, None, None]

		# trigger D2 (digital temperature value) conversion
		write_status = self.sendWrite(pressSensorMS5607.REG_CONV_D2_4096)
		if (write_status == False):
			return [None, None, None, None, None]

		# wait longer than the max ADC conversion time (9.04ms for OSR=4096) or data will be corrupt
		time.sleep(0.01)

		# read the 24-bit (3 byte) ADC temperature result
		adc_temperature = self.readBlock(pressSensorMS5607.REG_ADC_READ, 3)
		if (adc_temperature == None):
			return [None, None, None, None, None]

		# convert stored ADC value byte list to 24-bit value
		d1_pressure = (adc_pressure[0] << 16)|(adc_pressure[1] << 8)|(adc_pressure[2])
		d2_temp = (adc_temperature[0] << 16)|(adc_temperature[1] << 8)|(adc_temperature[2])

		# calculate temperature
		dT = d2_temp - self.T_REF 							# 25bit value, Difference between actual and reference temperature
		TEMP = 2000 + ((dT * self.TEMPSENS) >> 23) 			# Actual temperature (-40...85C with 0.01C resolution)

		# convert temp to proper sensor units
		temp_c = TEMP / 100.0 								# Temperature in C
		temp_f = temp_c * (9.0/5.0) + 32 					# Temperature in F

		# calculate temperature compensated pressure
		OFF = self.OFF_T1 + ((self.TCO * dT) >> 6) 			# Offset at actual temperature
		SENS = self.SENS_T1 + ((self.TCS * dT) >> 7) 		# Sensitivity at actual temperature
		P = (((d1_pressure * SENS) >> 21) - OFF) >> 15 		# Temperature compensated pressure (0...6000mbar with 0.03mbar resolution)

		# convert pressure to proper sensor units
		press_mbar = P / 100.0 								# Pressur in mBar
		press_pa = press_mbar * 100							# Pressure in Pascals (1Bar = 100,000Pa) --> (1mBar = 100Pa)

		# calculate altitude (in meters) from the pressure reading
		altitude_m = 44330 * (1 - ((press_pa/pressSensorMS5607.PRESSURE0)**(1/5.255)))

		# convert altitude to feet (1m ~= 3.28084 feet)
		altitude_ft = altitude_m * 3.28084

		#return [temp_c, temp_f, press_mbar, press_pa, altitude_m, altitude_ft]
		return ["{:+08.3f}".format(temp_c),
				"{:+08.3f}".format(temp_f),
				"{:08.3f}".format(press_mbar),
				"{:08.1f}".format(press_pa),
				"{:010.3f}".format(altitude_m),
				"{:010.3f}".format(altitude_ft)]

################################################################################

# Just some testing
if __name__ == "__main__":
	
	# i2c bus object
	bus = smbus.SMBus(1)

	# sensor addresses
	press0_addr = 0x77	# MS5607 altimeter (rectangle sensor)

	press0 = pressSensorMS5607(press0_addr, None, bus)

	press0.reset()
	press0.readSensorPROM()
	while (1):
		print press0.readAll()
		time.sleep(1)

	sys.exit(1)
