#!/usr/bin/env python

"""
file: press_ms5803.py
author: Chris Schwab
project: High Altitude Balloon Instrumentation Platform
description: API for the MS5803 digital pressure sensor on the RasPi HAT Board
"""

# sudo apt-get install python-smbus
import smbus

import sys

import time
import logger

# Custom i2c class
from i2c import i2c


class pressSensorMS5803(i2c):
	"""
	Abstract the MS5803 digital pressure sensor
	DataSheet found here:
		http://www.te.com/commerce/DocumentDelivery/DDEController?Action=srchrtrv&DocNm=MS5803-05BA&DocType=Data+Sheet&DocLang=English
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

	def __init__(self, address=None, busID=None, interface=None, busLogger=None):
		# Call super init
		super(self.__class__, self).__init__(address, busID, interface, busLogger)

		# Make a device logger
		self.deviceLogger = self.baseLogger.getLogger(("pressSensorMS5803_addr"+str(hex(address))))
		self.deviceLogger.log.info("Instantiated pressSensorMS5803_addr"+str(hex(address)))

		# Sensor PROM Constants
		self.SENS_T1 	= None 		# constant C1 = Pressure Sensitivity
		self.OFF_T1 	= None 		# constant C2 = Pressure Offset
		self.TCS 		= None 		# constant C3 = Temp Coeff of Pressure Sensitivity
		self.TCO 		= None 		# constant C4 = Temp Coeff of Pressure Offset
		self.T_REF 		= None 		# constant C5 = Reference temperature
		self.TEMPSENSE 	= None 		# constant C6 = Temp Coeff of the temperature

		self.readSensorPROM()

	def reset(self):
		"""
		Sends reset to the pressure sensor, ensures PROM is properly loaded to internal registers
			RETURNS boolean of write completion status: True=completed, False=failed
		"""

		# send reset
		self.deviceLogger.log.debug("Sending reset to ensure PROM is properly loaded into internal registers...")
		write_status = self.sendWrite(pressSensorMS5803.REG_RESET)
		# wait non-zero amount of time for reset
		time.sleep(0.5)

		return write_status

	def readSensorPROM(self):
		"""
		Reads sensor PROM constants C1 through C6 and adjusts C1, C2 and C5
			RETURNS boolean of PROM read completion status: True=completed, False=failed
		"""

		# read C1
		self.SENS_T1 = self.readWordSwapped(pressSensorMS5803.REG_PROM_C1)
		# if read failed
		if (self.SENS_T1 == None):
			return False
		# else adjust the constant
		else:
			self.deviceLogger.log.debug("Read PROM, C1: {} from register: {}".format(hex(self.SENS_T1), pressSensorMS5803.REG_PROM_C1))
			self.SENS_T1 = self.SENS_T1 << 17
			self.deviceLogger.log.debug("Modified C1 by << 17bits: {}".format(hex(self.SENS_T1)))

		# read C2
		self.OFF_T1 = self.readWordSwapped(pressSensorMS5803.REG_PROM_C2)
		# if read failed
		if (self.OFF_T1 == None):
			return False
		# else adjust the constant
		else:
			self.deviceLogger.log.debug("Read PROM, C2: {} from register: {}".format(hex(self.OFF_T1), pressSensorMS5803.REG_PROM_C2))
			self.OFF_T1 = self.OFF_T1 << 18
			self.deviceLogger.log.debug("Modified C2 by << 18bits: {}".format(hex(self.OFF_T1)))

		# read C3
		self.TCS = self.readWordSwapped(pressSensorMS5803.REG_PROM_C3)
		# if read failed
		if (self.TCS == None):
			return False
		# else adjust the constant
		# else:
		# 	self.TCS = self.TCS >> 7 				#NO! shift by 7 AFTER multiplying with dT (see below)
		self.deviceLogger.log.debug("Read PROM, C3: {} from register: {}".format(hex(self.TCS), pressSensorMS5803.REG_PROM_C3))

		# read C4
		self.TCO = self.readWordSwapped(pressSensorMS5803.REG_PROM_C4)
		# if read failed
		if (self.TCO == None):
			return False
		# else adjust the constant
		# else:
		# 	self.TCO = self.TCO >> 5 				#NO! shift by 5 AFTER multiplying with dT (see below)
		self.deviceLogger.log.debug("Read PROM, C4: {} from register: {}".format(hex(self.TCO), pressSensorMS5803.REG_PROM_C4))

		# read C5
		self.T_REF = self.readWordSwapped(pressSensorMS5803.REG_PROM_C5)
		# if read failed
		if (self.T_REF == None):
			return False
		# else adjust the constant
		else:
			self.deviceLogger.log.debug("Read PROM, C5: {} from register: {}".format(hex(self.T_REF), pressSensorMS5803.REG_PROM_C5))
			self.T_REF = self.T_REF << 8
			self.deviceLogger.log.debug("Modified C5 by << 8bits: {}".format(hex(self.T_REF)))

		# read C6
		self.TEMPSENS = self.readWordSwapped(pressSensorMS5803.REG_PROM_C6)
		# if read failed
		if (self.TEMPSENS == None):
			return False
		# else adjust the constant
		# else:
		# 	self.TEMPSENS = self.TEMPSENS >> 23      #NO! shift by 23 AFTER multiplying with dT (see below)
		self.deviceLogger.log.debug("Read PROM, C6: {} from register: {}".format(hex(self.TEMPSENS), pressSensorMS5803.REG_PROM_C6))

		return True

	def readAll (self):
		"""
		Read the temperature (c/f), pressure (mBar, Pa), and calculate altitude (m/ft)
			RETURNS list of floats: [temp_c, temp_f, press_mbar, press_pa, altitude_m, altitude_f]
		"""

		# trigger D1 (digital pressure value) conversion
		write_status = self.sendWrite(pressSensorMS5803.REG_CONV_D1_4096)
		if (write_status == False):
			return [None, None, None, None, None]

		# wait longer than the max ADC conversion time (9.04ms for OSR=4096) or data will be corrupt
		time.sleep(0.01)

		# read the 24-bit (3 byte) ADC pressure result
		adc_pressure = self.readBlock(pressSensorMS5803.REG_ADC_READ, 3)
		if (adc_pressure == None):
			return [None, None, None, None, None]

		# trigger D2 (digital temperature value) conversion
		write_status = self.sendWrite(pressSensorMS5803.REG_CONV_D2_4096)
		if (write_status == False):
			return [None, None, None, None, None]

		# wait longer than the max ADC conversion time (9.04ms for OSR=4096) or data will be corrupt
		time.sleep(0.01)

		# read the 24-bit (3 byte) ADC temperature result
		adc_temperature = self.readBlock(pressSensorMS5803.REG_ADC_READ, 3)
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

		# second order temperature compensation
		T2 		= 0
		OFF2 	= 0
		SENS2 	= 0
		# if TEMP is < 2000 (aka less than 20.00C)
		if (TEMP < 2000):
			T2 		= (3 * (dT**2)) >> 33
			OFF2 	= (3 * ((TEMP - 2000)**2)) >> 3
			SENS2 	= (7 * ((TEMP - 2000)**2)) >> 3
			self.deviceLogger.log.debug("Read temperature is less than 20.00C, performing second order temperature compensation: T2 = {}, OFF2 = {}, SENS2 = {}".format(hex(T2), hex(OFF2), hex(SENS2)))
			if (TEMP < -1500):
				SENS2 	= SENSE2 + (3 * ((TEMP + 1500)**2))
				self.deviceLogger.log.debug("Read temperature is ALSO less than -15.00C, modifying SENS2: SENS2 = {}".format(hex(SENS2)))
		
		# calculate temperature compensated pressure
		TEMP = TEMP - T2 									# Adjusting TEMP with second order compensation (if no compensation then TEMP2 = 0)
		OFF = self.OFF_T1 + ((self.TCO * dT) >> 5) 			# Offset at actual temperature
		OFF = OFF - OFF2 									# Adjusting OFF with second order compensation (if no compensation then OFF2 = 0)
		SENS = self.SENS_T1 + ((self.TCS * dT) >> 7) 		# Sensitivity at actual temperature
		SENS = SENS - SENS2 								# Adjusting SENS with second order compensation (if no compensation then SENS2 = 0)
		P = (((d1_pressure * SENS) >> 21) - OFF) >> 15 		# Temperature compensated pressure (0...6000mbar with 0.03mbar resolution)

		# convert pressure to proper sensor units
		press_mbar = P / 100.0 								# Pressur in mBar
		press_pa = press_mbar * 100							# Pressure in Pascals (1Bar = 100,000Pa) --> (1mBar = 100Pa)

		# calculate altitude (in meters) from the pressure reading
		altitude_m = 44330 * (1 - ((press_pa/pressSensorMS5803.PRESSURE0)**(1/5.255)))

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
	
	header = ["temp_c", "temp_f", "press_mbar", "press_pa", "altitude_m", "altitude_ft"]

	# sensor addresses
	press1_addr = 0x76	# MS5803 altimeter (round sensor)

	# i2c bus object
	bus = smbus.SMBus(1)

	# i2c logger object
	press_logger = logger.logger("pressSensorMS5803_logger")

	press1 = pressSensorMS5803(press1_addr, None, bus, press_logger)

	press1.reset()
	press1.readSensorPROM()
	print header
	while (1):
		print press1.readAll()
		time.sleep(1)

	sys.exit(1)
