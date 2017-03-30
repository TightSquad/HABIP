#!/usr/bin/env python

"""
file: ina219.py
author: Chris Schwab
project: High Altitude Balloon Instrumentation Platform
description: Demo script for the INA219 I2C power monitor chip
	
	data-sheet: http://www.ti.com/lit/ds/symlink/ina219.pdf
"""

# sudo apt-get install python-smbus
import smbus
import time

##############
# "Constants"
##############

# sensor registers and constants
reg_conf = 0x0			# r/w, All-register reset, settings for bus voltage range, PGA Gain, ADC resolution/averaging.
CONF_RST   = 0x0800 	# see data sheet for register bit meaning
CONF_RSVVD = 0x4000
CONF_BRNG  = 0x2000
CONF_PG1   = 0x1000
CONF_PG0   = 0x0800
CONF_BADC4 = 0x0400
CONF_BADC3 = 0x0200
CONF_BADC2 = 0x0100
CONF_BADC1 = 0x0080
CONF_SADC4 = 0x0040
CONF_SADC3 = 0x0020
CONF_SADC2 = 0x0010
CONF_SADC1 = 0x0008
CONF_MODE3 = 0x0004
CONF_MODE2 = 0x0002
CONF_MODE1 = 0x0001

reg_shunt_voltage = 0x1	# r  , Shunt voltage measurement data.
						# [15:12] = sign
						# [11:0] = shunt voltage
shunt_voltage_precision = 10	# LSB = 10uV

reg_bus_voltage = 0x2	# r  , Bus voltage measurement data.
						# [1] = CNVR = conversion ready, clears only when reg_power is READ
bus_voltage_precision = 4	# LSB = 4mV
BUS_VOLTAGE_CNVR = 0x0002
BUS_VOLTAGE_OVF = 0x0001

reg_power = 0x3			# r  , Power measurement data.
						# NOTE: reading this register clears the CVNR bit in reg_bus_voltage
power_precision = 1 	# this is set by solving for power_LSB

reg_current = 0x4		# r  , Contains the value of the current flowing through the shunt resistor.
current_precision = 50	# this is set by solving for current_LSB

reg_calib = 0x5			# r/w, Sets full-scale range and LSB of current and power measurements. Overall system calibration.

# sensor addresses
pow0_addr = 0x44	#power monitor

##############
# "functions"
##############

# NOTE: smbus transmits and receives WORDS as MSByte first, LSByte second
# 	Register Bits	Python Integer	MSByte	LSByte 	Tx/Rx SMBus Word
#	[15..0] 		0xQRST			0xQR 	0xST 	0xSTQR
#
# NEED TO TAKE CARE OF THIS by re-arranging rx data and tx data
# see functions 'smbus_read_word' and 'smbus_write_word' below 

def smbus_read_word (interface, device_addr, register_addr):
	# read i2c bus data word
	bus_val = interface.read_word_data(device_addr, register_addr)
	# convert to binary and zero pad if necessary to 16-bits
	bus_val = bin(bus_val)[2:].zfill(16)
	# re-arrange MSByte and LSByte
	bus_val_flip = bus_val[8:] + bus_val[:8]

	return int(bus_val_flip, 2)

def smbus_write_word (interface, device_addr, register_addr, data):
	bus_val = bin(data)[2:].zfill(16)
	# re-arrange so MSByte is lower byte of integer
	bus_val = bus_val[8:] + bus_val[:8]
	# write to CONF reg
	interface.write_word_data(device_addr, register_addr, int(bus_val, 2))

##############
# "Main"
##############

# i2c bus object
bus = smbus.SMBus(1)

######
# set CONFIG register
######
print "SETTING CONFIG REG"
# BRNG=32V, Range = +/- 40mV, shunt/bus ADC = 12bit, shunt/bus continuous mode
set_value = CONF_BRNG | CONF_BADC2 | CONF_BADC1 | CONF_SADC2 | CONF_SADC1 | CONF_MODE3 | CONF_MODE2 | CONF_MODE1
# write to CONF reg
smbus_write_word(bus, pow0_addr, reg_conf, set_value)
# read back value to check
print "Reading back CONFIG REG value: " + str(hex(smbus_read_word(bus, pow0_addr, reg_conf))) + "--> should be: " + hex(set_value)

#######
# set calibration register
#	calib_val = (0.04096 / (current_LSB * R_shunt))	--> 24824_decimal = 0x60F8
#		current_LSB = (max_expected_current / 2^15)	--> 1.6384 Amps / 2^15 = 0.00005 A = 50uA
#		R_shunt = value in Ohms of shunt resistor 	--> 0.033
# 		power_LSB = 20 * current_LSB = 1000uW = 1mW
#######
calib_val = 0x60F8
# shift cal_value_calc left by 1-bit since reg_calib[0] is not used to store the calibration value
calib_val = calib_val << 1
# write to CONF reg
smbus_write_word(bus, pow0_addr, reg_calib, calib_val)
# read back value to check
print "Reading back CALIB REG value: " + str(hex(smbus_read_word(bus, pow0_addr, reg_calib))) + "--> should be: " + hex(calib_val)

# starting time stamp
t_start = time.time()

while(1):

	# wait for valid conversion
	while ((smbus_read_word(bus, pow0_addr, reg_bus_voltage) & BUS_VOLTAGE_CNVR) != BUS_VOLTAGE_CNVR):
		print "CONVERSION IS NOT READY at elapsed time of %f\n" % (time.time() - t_start)
		print "Reg value: " + str(hex(smbus_read_word(bus, pow0_addr, reg_bus_voltage)))
		# wait 1 second
		time.sleep(5)

	# display warning is power or Current calculations are out of range
	if ((smbus_read_word(bus, pow0_addr, reg_bus_voltage) & BUS_VOLTAGE_OVF) == BUS_VOLTAGE_OVF):
		print "DANGER! WARNING! Power or Current calculations are out of range\n"

	######
	# read the shunt voltage
	######
	shunt_voltage_uv = None	# variable for shunt voltage
	shunt_voltage = smbus_read_word(bus, pow0_addr, reg_shunt_voltage)
	# if shunt voltage is negative ([15:12] are sign bits)
	if (shunt_voltage & 0x8000):
		# convert from 2s comp --> invert (aka XOR with all 1s) then add 1
		shunt_voltage_2s_comp = (shunt_voltage ^ 0xFFFF) + 1
		# convert to uV and throw on a minus sign
		shunt_voltage_uv = (-1) * (shunt_voltage_2s_comp * shunt_voltage_precision)
	# else, convert register value to uV
	else:
		shunt_voltage_uv = shunt_voltage * shunt_voltage_precision

	######
	# read the bus voltage
	######
	bus_voltage_mv = None # variable for bus voltage
	bus_voltage = smbus_read_word(bus, pow0_addr, reg_bus_voltage)
	# convert bus voltage to mV (voltage is in reg_bus_voltage bits [15:3])
	bus_voltage_mv = ((bus_voltage >> 3) & 0x1FFF) * bus_voltage_precision

	######
	# read the current
	######
	current_ua = None # variable for current
	current = smbus_read_word(bus, pow0_addr, reg_current)
	# if shunt voltage is negative
	if (current & 0x8000):
		# convert from 2s comp --> invert (aka XOR with all 1s) then add 1
		current_2s_comp = (current ^ 0xFFFF) + 1
		# convert to uV and throw on a minus sign
		current_ua = (-1) * (current_2s_comp * current_precision)
	# else, convert register value to uV
	else:
		current_ua = current * current_precision

	######
	# read the power (current_units * bus_voltage_mv)
	#	NOTE: reading reg_power CLEARS the CNVR bit of reg_bus_voltage
	######
	power_mw = None # variable for bus voltage
	power = smbus_read_word(bus, pow0_addr, reg_power)
	# convert bus voltage to mV (voltage is in reg_bus_voltage bits [15:3])
	power_mw = power * power_precision


	print "Power Sensor 0 --> Shunt Voltage (mV): %f" % (shunt_voltage_uv / 1000.0)
	print "Power Sensor 0 --> Bus Voltage    (V): %f" % (bus_voltage_mv / 1000.0)
	print "Power Sensor 0 --> Current       (mA): %f" % (current_ua / 1000.0)
	print "Power Sensor 0 --> Power         (mW): %f" % power_mw

	print "elapsed time: %f seconds\n" % (time.time() - t_start)
	time.sleep(1)
