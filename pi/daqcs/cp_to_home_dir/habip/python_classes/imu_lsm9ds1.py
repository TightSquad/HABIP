#!/usr/bin/env python

"""
file: imu_lsm9ds1.py
author: Chris Schwab
project: High Altitude Balloon Instrumentation Platform
description: API for the LSM9DS1 IMU on the RasPi HAT Board
"""

# sudo apt-get install python-smbus
import smbus

import sys

import common
import logger

# Custom i2c class
from i2c import i2c


class imuLSM9DS1(i2c):
	"""
	Abstract the LSM9DS1 IMU
	DataSheet found here:
		http://www.st.com/content/ccc/resource/technical/document/datasheet/1e/3f/2a/d6/25/eb/48/46/DM00103319.pdf/files/DM00103319.pdf/jcr:content/translations/en.DM00103319.pdf
	"""

	# Accel/Gyro (XL/G) Registers
	ACT_THS				0x04
	ACT_DUR				0x05
	INT_GEN_CFG_XL		0x06
	INT_GEN_THS_X_XL	0x07
	INT_GEN_THS_Y_XL	0x08
	INT_GEN_THS_Z_XL	0x09
	INT_GEN_DUR_XL		0x0A
	REFERENCE_G			0x0B
	INT1_CTRL			0x0C
	INT2_CTRL			0x0D
	WHO_AM_I_XG			0x0F
	CTRL_REG1_G			0x10
	CTRL_REG2_G			0x11
	CTRL_REG3_G			0x12
	ORIENT_CFG_G		0x13
	INT_GEN_SRC_G		0x14
	OUT_TEMP_L			0x15
	OUT_TEMP_H			0x16
	STATUS_REG_0		0x17
	OUT_X_L_G			0x18
	OUT_X_H_G			0x19
	OUT_Y_L_G			0x1A
	OUT_Y_H_G			0x1B
	OUT_Z_L_G			0x1C
	OUT_Z_H_G			0x1D
	CTRL_REG4			0x1E
	CTRL_REG5_XL		0x1F
	CTRL_REG6_XL		0x20
	CTRL_REG7_XL		0x21
	CTRL_REG8			0x22
	CTRL_REG9			0x23
	CTRL_REG10			0x24
	INT_GEN_SRC_XL		0x26
	STATUS_REG_1		0x27
	OUT_X_L_XL			0x28
	OUT_X_H_XL			0x29
	OUT_Y_L_XL			0x2A
	OUT_Y_H_XL			0x2B
	OUT_Z_L_XL			0x2C
	OUT_Z_H_XL			0x2D
	FIFO_CTRL			0x2E
	FIFO_SRC			0x2F
	INT_GEN_CFG_G		0x30
	INT_GEN_THS_XH_G	0x31
	INT_GEN_THS_XL_G	0x32
	INT_GEN_THS_YH_G	0x33
	INT_GEN_THS_YL_G	0x34
	INT_GEN_THS_ZH_G	0x35
	INT_GEN_THS_ZL_G	0x36
	INT_GEN_DUR_G		0x37

	# Magneto Registers
	OFFSET_X_REG_L_M	0x05
	OFFSET_X_REG_H_M	0x06
	OFFSET_Y_REG_L_M	0x07
	OFFSET_Y_REG_H_M	0x08
	OFFSET_Z_REG_L_M	0x09
	OFFSET_Z_REG_H_M	0x0A
	WHO_AM_I_M			0x0F
	CTRL_REG1_M			0x20
	CTRL_REG2_M			0x21
	CTRL_REG3_M			0x22
	CTRL_REG4_M			0x23
	CTRL_REG5_M			0x24
	STATUS_REG_M		0x27
	OUT_X_L_M			0x28
	OUT_X_H_M			0x29
	OUT_Y_L_M			0x2A
	OUT_Y_H_M			0x2B
	OUT_Z_L_M			0x2C
	OUT_Z_H_M			0x2D
	INT_CFG_M			0x30
	INT_SRC_M			0x31
	INT_THS_L_M			0x32
	INT_THS_H_M			0x33

	# Who Am I Registers
	WHO_AM_I_AG_RSP		0x68
	WHO_AM_I_M_RSP		0x3D

	def __init__(self, xlg_address=None, busID=None, interface=None, busLogger=None):
		# Call super init
		super(self.__class__, self).__init__(address, busID, interface, busLogger)

		# Make a device logger
		self.deviceLogger = self.baseLogger.getLogger(("imuLSM9DS1_addr"+str(hex(xlg_address))))
		self.deviceLogger.log.info("Instantiated imuLSM9DS1_addr"+str(hex(xlg_address)))

		# configure the IMU
		self.config()

	def config(self):
		"""
		Configures the IMU
			RETURNS boolean of write completion status: True=completed, False=failed
		"""

		# send reset
		self.deviceLogger.log.debug("Configuring IMU for operation...")

		

		
		write_status = self.sendWrite(pressSensorMS5607.REG_RESET)
		# wait non-zero amount of time for reset
		common.msleep(50)

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
			self.deviceLogger.log.debug("Read PROM, C1: {} from register: {}".format(hex(self.SENS_T1), pressSensorMS5607.REG_PROM_C1))
			self.SENS_T1 = self.SENS_T1 << 16
			self.deviceLogger.log.debug("Modified C1 by << 16bits: {}".format(hex(self.SENS_T1)))

		# read C2
		self.OFF_T1 = self.readWordSwapped(pressSensorMS5607.REG_PROM_C2)
		# if read failed
		if (self.OFF_T1 == None):
			return False
		# else adjust the constant
		else:
			self.deviceLogger.log.debug("Read PROM, C2: {} from register: {}".format(hex(self.OFF_T1), pressSensorMS5607.REG_PROM_C2))
			self.OFF_T1 = self.OFF_T1 << 17
			self.deviceLogger.log.debug("Modified C2 by << 17bits: {}".format(hex(self.OFF_T1)))

		# read C3
		self.TCS = self.readWordSwapped(pressSensorMS5607.REG_PROM_C3)
		# if read failed
		if (self.TCS == None):
			return False
		# else adjust the constant
		# else:
		# 	self.TCS = self.TCS >> 7 				#NO! shift by 7 AFTER multiplying with dT (see below)
		self.deviceLogger.log.debug("Read PROM, C3: {} from register: {}".format(hex(self.TCS), pressSensorMS5607.REG_PROM_C3))

		# read C4
		self.TCO = self.readWordSwapped(pressSensorMS5607.REG_PROM_C4)
		# if read failed
		if (self.TCO == None):
			return False
		# else adjust the constant
		# else:
		# 	self.TCO = self.TCO >> 6 				#NO! shift by 6 AFTER multiplying with dT (see below)
		self.deviceLogger.log.debug("Read PROM, C4: {} from register: {}".format(hex(self.TCO), pressSensorMS5607.REG_PROM_C4))

		# read C5
		self.T_REF = self.readWordSwapped(pressSensorMS5607.REG_PROM_C5)
		# if read failed
		if (self.T_REF == None):
			return False
		# else adjust the constant
		else:
			self.deviceLogger.log.debug("Read PROM, C5: {} from register: {}".format(hex(self.T_REF), pressSensorMS5607.REG_PROM_C5))
			self.T_REF = self.T_REF << 8
			self.deviceLogger.log.debug("Modified C5 by << 8bits: {}".format(hex(self.T_REF)))

		# read C6
		self.TEMPSENS = self.readWordSwapped(pressSensorMS5607.REG_PROM_C6)
		# if read failed
		if (self.TEMPSENS == None):
			return False
		# else adjust the constant
		# else:
		# 	self.TEMPSENS = self.TEMPSENS >> 23      #NO! shift by 23 AFTER multiplying with dT (see below)
		self.deviceLogger.log.debug("Read PROM, C6: {} from register: {}".format(hex(self.TEMPSENS), pressSensorMS5607.REG_PROM_C6))

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
		common.msleep(10)

		# read the 24-bit (3 byte) ADC pressure result
		adc_pressure = self.readBlock(pressSensorMS5607.REG_ADC_READ, 3)
		if (adc_pressure == None):
			return [None, None, None, None, None]

		# trigger D2 (digital temperature value) conversion
		write_status = self.sendWrite(pressSensorMS5607.REG_CONV_D2_4096)
		if (write_status == False):
			return [None, None, None, None, None]

		# wait longer than the max ADC conversion time (9.04ms for OSR=4096) or data will be corrupt
		common.msleep(10)

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

		# second order temperature compensation
		T2 		= 0
		OFF2 	= 0
		SENS2 	= 0
		# if TEMP is < 2000 (aka less than 20.00C)
		if (TEMP < 2000):
			T2 		= (dT**2) >> 31
			OFF2 	= (61 * ((TEMP - 2000)**2)) >> 4
			SENS2 	= 2 * ((TEMP - 2000)**2)
			self.deviceLogger.log.debug("Read temperature is less than 20.00C, performing second order temperature compensation: T2 = {}, OFF2 = {}, SENS2 = {}".format(hex(T2), hex(OFF2), hex(SENS2)))
			if (TEMP < -1500):
				OFF2 	= OFF2 + (15 * ((TEMP + 1500)**2))
				SENS2 	= SENSE2 + (8 * ((TEMP + 1500)**2))
				self.deviceLogger.log.debug("Read temperature is ALSO less than -15.00C, modifying OFF2 and SENS2: OFF2 = {}, SENS2 = {}".format(hex(OFF2), hex(SENS2)))

		# calculate temperature compensated pressure
		TEMP = TEMP - T2 									# Adjusting TEMP with second order compensation (if no compensation then TEMP2 = 0)
		OFF = self.OFF_T1 + ((self.TCO * dT) >> 6) 			# Offset at actual temperature
		OFF = OFF - OFF2 									# Adjusting OFF with second order compensation (if no compensation then OFF2 = 0)
		SENS = self.SENS_T1 + ((self.TCS * dT) >> 7) 		# Sensitivity at actual temperature
		SENS = SENS - SENS2 								# Adjusting SENS with second order compensation (if no compensation then SENS2 = 0)
		P = (((d1_pressure * SENS) >> 21) - OFF) >> 15 		# Temperature compensated pressure (0...6000mbar with 0.03mbar resolution)

		# convert pressure to proper sensor units
		press_mbar = P / 100.0 								# Pressur in mBar
		press_pa = press_mbar * 100							# Pressure in Pascals (1Bar = 100,000Pa) --> (1mBar = 100Pa)

		# calculate altitude (in meters) from the pressure reading
		altitude_m = 44330 * (1 - ((press_pa/pressSensorMS5607.PRESSURE0)**(1/5.255)))

		# convert altitude to feet (1m ~= 3.28084 feet)
		altitude_ft = altitude_m * 3.28084

		self.prev_temp_c = temp_c
		self.prev_temp_f = temp_f
		self.prev_press_mbar = press_mbar
		self.prev_press_pa = press_pa
		self.prev_altitude_m = altitude_m
		self.prev_altitude_ft = altitude_ft

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
	acg_addr	= 0x6B	# MS5607 altimeter (rectangle sensor)
	mag_addr 	= 0x1E

	# i2c bus object
	bus = smbus.SMBus(1)

	# i2c logger object
	press_logger = logger.logger("pressSensorMS5607_logger")

	press0 = pressSensorMS5607(press0_addr, None, bus, press_logger)

	press0.reset()
	press0.readSensorPROM()
	print header
	while (1):
		print press0.readAll()
		common.msleep(1000)

	sys.exit(1)
