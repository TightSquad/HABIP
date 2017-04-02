#!/usr/bin/env python

"""
file: pct2075.py
author: Chris Schwab
project: High Altitude Balloon Instrumentation Platform
description: Demo script for the PCT2075 I2C temperature sensor
	
	data-sheet: http://www.nxp.com/documents/data_sheet/PCT2075.pdf
"""

# sudo apt-get install python-smbus
import smbus
import time

##############
# "Constants"
##############

# sensor registers 
reg_temp  = 0x0	# r/w, Temperature register: contains two 8-bit data bytes; to store the measured Temp data.
reg_conf  = 0x1	# r  , Configuration register: contains a single 8-bit data byte; to set the device operating condition; default = 0.
reg_thyst = 0x2	# r/w, Hysteresis register: contains two 8-bit data bytes; to store the hysteresis Thys limit; default = 75 C.
reg_tos   = 0x3	# r/w, Overtemperature shutdown threshold register: contains two 8-bit data bytes; to store the overtemperature shutdown Tots limit; default = 80 C.
reg_tidle = 0x4	# r/w, Temperature conversion cycle default to 100 ms.

# sensor addresses
temp0_addr = 0x48	#right-side temp sensor
temp1_addr = 0x4A	# left side temp sensor

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

# enable printing
printing_enabled = 1

# i2c bus object
bus = smbus.SMBus(1)

# starting time stamp
t_start = time.time()

# main loop to keep reading the sensor
while(1):
	# varaibles for temperature data
	temperature_c = None
	temperature_f = None
	# read temp value from sensor 0
	temperature = smbus_read_word(bus, temp0_addr, reg_temp)
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

	if (printing_enabled):
		print "Temp Sensor 0 --> Temp (c): %f" % temperature_c
		print "Temp Sensor 0 --> Temp (f): %f" % temperature_f

	# varaibles for temperature data
	temperature_c = None
	temperature_f = None
	# read temp value from sensor 1
	temperature = smbus_read_word(bus, temp1_addr, reg_temp)
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

	if (printing_enabled):
		print "Temp Sensor 0 --> Temp (c): %f" % temperature_c
		print "Temp Sensor 0 --> Temp (f): %f" % temperature_f

	print "elapsed time: %f seconds\n" % (time.time() - t_start)
	time.sleep(1)
