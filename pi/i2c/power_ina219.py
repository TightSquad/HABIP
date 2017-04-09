#!/usr/bin/env python

"""
file: power_ina219.py
author: Chris Schwab
project: High Altitude Balloon Instrumentation Platform
description: API for the INA219 digital power monitor on the RasPi HAT Board
"""

# sudo apt-get install python-smbus
import smbus

import sys

import time
import logger

# Custom i2c class
from i2c import i2c


class powerMonitorINA219(i2c):
	"""
	Abstract the INA219 digital power monitor
	DataSheet found here:
		http://www.ti.com/lit/ds/symlink/ina219.pdf
	"""

	# Register Addresses and Bit Masks
	REG_CONF 			= 0x0		# W: r/w, All-register reset, settings for bus voltage range, PGA Gain, ADC resolution/averaging.
	CONF_RST   	= 0x0800 				# see data sheet for register bit fields
	CONF_RSVVD 	= 0x4000
	CONF_BRNG  	= 0x2000
	CONF_PG1   	= 0x1000
	CONF_PG0   	= 0x0800
	CONF_BADC4 	= 0x0400
	CONF_BADC3 	= 0x0200
	CONF_BADC2 	= 0x0100
	CONF_BADC1 	= 0x0080
	CONF_SADC4 	= 0x0040
	CONF_SADC3 	= 0x0020
	CONF_SADC2 	= 0x0010
	CONF_SADC1 	= 0x0008
	CONF_MODE3 	= 0x0004
	CONF_MODE2 	= 0x0002
	CONF_MODE1 	= 0x0001

	REG_SHUNT_VOLTAGE 	= 0x1	# W: r  , Shunt voltage measurement data.
									# [15:12] = sign
									# [11:0] = shunt voltage
	SHUNT_VOLTAGE_PRECISION = 10	# LSB = 10uV

	REG_BUS_VOLTAGE 	= 0x2	# W: r  , Bus voltage measurement data.
									# [1] = CNVR = conversion ready, clears only when reg_power is READ
	BUS_VOLTAGE_PRECISION = 4	# LSB = 4mV
	BUS_VOLTAGE_CNVR 	= 0x0002
	BUS_VOLTAGE_OVF 	= 0x0001

	REG_POWER 			= 0x3	# W: r  , Power measurement data.
									# NOTE: reading this register clears the CVNR bit in reg_bus_voltage
	POWER_PRECISION = 1 		# LSB = 1mA, this is set by solving for power_LSB

	REG_CURRENT 		= 0x4	# W: r  , Contains the value of the current flowing through the shunt resistor.
	CURRENT_PRECISION = 50		# LSB = 50uA, this is set by solving for current_LSB

	REG_CALIB 			= 0x5	# W: r/w, Sets full-scale range and LSB of current and power measurements. Overall system calibration.


	def __init__(self, address=None, busID=None, interface=None, busLogger=None):
		# Call super init
		super(self.__class__, self).__init__(address, busID, interface, busLogger)

		# Make a device logger
		self.deviceLogger = self.baseLogger.getLogger(("powerMonitorINA219_addr"+str(hex(address))))
		self.deviceLogger.log.info("Instantiated powerMonitorINA219_addr"+str(hex(address)))

	def config(self):
		"""
		Sets the INA219 configuration register
			RETURNS boolean of write completion status: True=completed, False=failed
		"""

		# BRNG=32V, Range = +/- 40mV, shunt/bus ADC = 12bit --> 532us conversion time, shunt/bus continuous mode
		set_value = powerMonitorINA219.CONF_BRNG  | powerMonitorINA219.CONF_BADC2 | powerMonitorINA219.CONF_BADC1 | powerMonitorINA219.CONF_SADC2 | powerMonitorINA219.CONF_SADC1 | powerMonitorINA219.CONF_MODE3 | powerMonitorINA219.CONF_MODE2 | powerMonitorINA219.CONF_MODE1
		# write to CONF reg
		write_status = self.writeWordSwapped(powerMonitorINA219.REG_CONF, set_value)
		if (write_status == False):
			return False

		# read back value to log
		read_value = self.readWordSwapped(powerMonitorINA219.REG_CONF)
		if (read_value == None):
			return False
		self.deviceLogger.log.debug("Set CONFIG register: {}".format(hex(read_value)))

		return write_status

	def calibrate(self):
		"""
		Writes constant to CALIB register for conversion scaling
			RETURNS boolean of write completion status: True=completed, False=failed
		"""

		#######
		# set calibration register
		#	calib_val = (0.04096 / (current_LSB * r_shunt))	--> 24824_decimal = 0x60F8
		#		current_LSB = (max_expected_current / 2^15)	--> 1.6384 Amps / 2^15 = 0.00005 A = 50uA
		#		r_shunt = value in Ohms of shunt resistor 	--> 0.033
		# 		power_LSB = 20 * current_LSB = 1000uW = 1mW
		#######
		calib_val = 0x60F8
		# shift cal_value_calc left by 1-bit since reg_calib[0] is not used to store the calibration value
		calib_val = calib_val << 1
		# write to CONF reg
		write_status = self.writeWordSwapped(powerMonitorINA219.REG_CALIB, calib_val)
		if (write_status == False):
			return False

		# read back value to log
		read_value = self.readWordSwapped(powerMonitorINA219.REG_CALIB)
		if (read_value == None):
			return False
		self.deviceLogger.log.debug("Set CALIB register: {}".format(hex(read_value)))
		
		return write_status

	def conversionNotValid(self):
		"""
		Checks to make sure the current conversion values are valid
			RETURNS boolean of conversion completion status: True=conv is NOT valid, False=conv IS valid
		"""
		read_value = self.readWordSwapped(powerMonitorINA219.REG_BUS_VOLTAGE)
		if (read_value == None):
			return True

		return (read_value & powerMonitorINA219.BUS_VOLTAGE_CNVR) != powerMonitorINA219.BUS_VOLTAGE_CNVR


	def readVIP (self):
		"""
		Read the shunt voltage (mV), bus voltage (V), current (mA), and power (mW)
			RETURNS list of floats: [shunt_voltage_mv, bus_voltage_V, current_ma, power_mw]
		"""

		# log warning if power or current calculations are out of range
		read_value = self.readWordSwapped(powerMonitorINA219.REG_BUS_VOLTAGE)
		if (read_value == None):
			return [None, None, None, None]

		if ((read_value & powerMonitorINA219.BUS_VOLTAGE_OVF) == powerMonitorINA219.BUS_VOLTAGE_OVF):
			self.deviceLogger.log.debug("DANGER! WARNING! Power or Current calculations are out of range")

		######
		# read the shunt voltage
		######
		shunt_voltage_uv = None	# variable for shunt voltage
		shunt_voltage = self.readWordSwapped(powerMonitorINA219.REG_SHUNT_VOLTAGE)
		if (shunt_voltage == None):
			return [None, None, None, None]
		# if shunt voltage is negative ([15:12] are sign bits)
		if (shunt_voltage & 0x8000):
			self.deviceLogger.log.debug("WARNING: shunt voltage is negative")
			# convert from 2s comp --> invert (aka XOR with all 1s) then add 1
			shunt_voltage_2s_comp = (shunt_voltage ^ 0xFFFF) + 1
			# convert to uV and throw on a minus sign
			shunt_voltage_uv = (-1) * (shunt_voltage_2s_comp * powerMonitorINA219.SHUNT_VOLTAGE_PRECISION)
		# else, convert register value to uV
		else:
			shunt_voltage_uv = shunt_voltage * powerMonitorINA219.SHUNT_VOLTAGE_PRECISION
		# convert to mV
		shunt_voltage_mv = shunt_voltage_uv / 1000.0

		######
		# read the bus voltage
		######
		bus_voltage_mv = None # variable for bus voltage
		bus_voltage = self.readWordSwapped(powerMonitorINA219.REG_BUS_VOLTAGE)
		if (bus_voltage == None):
			return [None, None, None, None]
		# convert bus voltage to mV (voltage is in reg_bus_voltage bits [15:3])
		bus_voltage_mv = ((bus_voltage >> 3) & 0x1FFF) * powerMonitorINA219.BUS_VOLTAGE_PRECISION
		# convert to V
		bus_voltage_v = bus_voltage_mv / 1000.0

		######
		# read the current
		######
		current_ua = None # variable for current
		current = self.readWordSwapped(powerMonitorINA219.REG_CURRENT)
		if (current == None):
			return [None, None, None, None]
		# if current is negative
		if (current & 0x8000):
			self.deviceLogger.log.debug("WARNING: current is negative")
			# convert from 2s comp --> invert (aka XOR with all 1s) then add 1
			current_2s_comp = (current ^ 0xFFFF) + 1
			# convert to uV and throw on a minus sign
			current_ua = (-1) * (current_2s_comp * powerMonitorINA219.CURRENT_PRECISION)
		# else, convert register value to uV
		else:
			current_ua = current * powerMonitorINA219.CURRENT_PRECISION
		# convert to mA
		current_ma = current_ua / 1000.0

		######
		# read the power (current_units * bus_voltage_mv)
		#	NOTE: reading reg_power CLEARS the CNVR bit of reg_bus_voltage
		######
		power_mw = None # variable for bus voltage
		power = self.readWordSwapped(powerMonitorINA219.REG_POWER)
		if (power == None):
			return [None, None, None, None]	
		# convert bus voltage to mV (voltage is in reg_bus_voltage bits [15:3])
		power_mw = power * powerMonitorINA219.POWER_PRECISION

		return ["{:+08.3f}".format(shunt_voltage_mv),
				"{:07.3f}".format(bus_voltage_v),
				"{:+09.3f}".format(current_ma),
				"{:07.1f}".format(power_mw)]

################################################################################

# Just some testing
if __name__ == "__main__":
	
	header = ["shunt_voltage_mv", "bus_voltage_v", "current_ma", "power_mw"]

	# sensor addresses
	power0_addr = 0x44		# power monitor

	# i2c bus object
	bus = smbus.SMBus(1)

	# i2c logger object
	power_logger = logger.logger("powerMonitorINA219_logger")

	power0 = powerMonitorINA219(power0_addr, None, bus, power_logger)

	power0.config()
	power0.calibrate()
	print header
	while (1):
		while (power0.conversionNotValid()):
			print "CONVERSION IS NOT VALID\n"
			time.sleep(0.01)
		print power0.readVIP()
		time.sleep(1)

	sys.exit(1)
