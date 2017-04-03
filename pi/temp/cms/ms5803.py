#!/usr/bin/env python

"""
file: ms5803.py
author: Chris Schwab
project: High Altitude Balloon Instrumentation Platform
description: Demo script for the MS5803-05BA_B I2C pressure sensor
	
	http://www.te.com/commerce/DocumentDelivery/DDEController?Action=showdoc&DocId=Data+Sheet%7FMS5803-05BA%7FB%7Fpdf%7FEnglish%7FENG_DS_MS5803-05BA_B.pdf%7FCAT-BLPS0011
"""

# sudo apt-get install python-smbus
import smbus
import time

##############
# "Constants"
##############

# sensor registers
reg_reset         = 0x1E 	# B: w  : Reset to load PROM to registers, needed on power up (use data = 0x0)
reg_conv_d1_256   = 0x40 	# B: w  : Write triggers a D1(pressure) conversion with OSR = 256 (use data = 0x0)
reg_conv_d1_512   = 0x42 	# B: w  : Write triggers a D1(pressure) conversion with OSR = 512 (use data = 0x0)
reg_conv_d1_1024  = 0x44 	# B: w  : Write triggers a D1(pressure) conversion with OSR = 1024 (use data = 0x0)
reg_conv_d1_2048  = 0x46 	# B: w  : Write triggers a D1(pressure) conversion with OSR = 2048 (use data = 0x0)
reg_conv_d1_4096  = 0x48 	# B: w  : Write triggers a D1(pressure) conversion with OSR = 4096 (use data = 0x0)
reg_conv_d2_256   = 0x50 	# B: w  : Write triggers a D2(temp) conversion with OSR = 256 (use data = 0x0)
reg_conv_d2_512   = 0x52 	# B: w  : Write triggers a D2(temp) conversion with OSR = 512 (use data = 0x0)
reg_conv_d2_1024  = 0x54 	# B: w  : Write triggers a D2(temp) conversion with OSR = 1024 (use data = 0x0)
reg_conv_d2_2048  = 0x56 	# B: w  : Write triggers a D2(temp) conversion with OSR = 2048 (use data = 0x0)
reg_conv_d2_4096  = 0x58 	# B: w  : Write triggers a D2(temp) conversion with OSR = 4096 (use data = 0x0)
reg_adc_read      = 0x00 	# L: r  : Burst read from the ADC register (either D1 or D2 value), 24bits = 3 byte list
reg_prom_manu     = 0xA0 	# W: r  : PROM addr_0, word reserved for manufacturer
reg_prom_c1       = 0xA2 	# W: r  : PROM addr_1, constant C1 = Pressure Sensitivity = SENS_T1
reg_prom_c2       = 0xA4 	# W: r  : PROM addr_2, constant C2 = Pressure Offset = OFF_T1
reg_prom_c3       = 0xA6 	# W: r  : PROM addr_3, constant C3 = Temp Coeff of Pressure Sensitivity = TCS
reg_prom_c4       = 0xA8 	# W: r  : PROM addr_4, constant C4 = Temp Coeff of Pressure Offset = TCO
reg_prom_c5       = 0xAA 	# W: r  : PROM addr_5, constant C5 = Reference = T_REF
reg_prom_c6       = 0xAC 	# W: r  : PROM addr_6, constant C6 = Temp Coeff of the temperature = TEMPSENS
reg_prom_crc      = 0xAE 	# W: r  : PROM addr_7, CRC value, bitd [3:0]

# sensor addresses
press1_addr = 0x76	# MS5803 altimeter (round sensor)

# p0 is the average pressure at sea level = 101325 Pa
p0 = 101325

##############
# "functions"
##############

# I2C Word Functions
# 
# NOTE: smbus transmits and receives WORDS as MSByte first, LSByte second
# 	Register Bits	Python Integer	MSByte	LSByte 	Tx/Rx SMBus Word
#	[15..0] 		0xQRST			0xQR 	0xST 	0xSTQR
#
# NEED TO TAKE CARE OF THIS by re-arranging rx data and tx data for Words
# see functions 'smbus_read_word' and 'smbus_write_word' below 

def smbus_read_word (interface, device_addr, register_addr):
	# read i2c bus data word
	bus_val = interface.read_word_data(device_addr, register_addr)
	# pad with zeroes if necessary
	bus_val = bin(bus_val)[2:].zfill(16)
	# re-arrange MSByte and LSByte
	bus_val_flip = bus_val[8:] + bus_val[:8]

	return int(bus_val_flip, 2)

def smbus_write_word (interface, device_addr, register_addr, data):
	# pad with zeroes if necessary
	bus_val = bin(data)[2:].zfill(16)
	# re-arrange so MSByte is lower byte of integer
	bus_val = bus_val[8:] + bus_val[:8]
	# write to register
	interface.write_word_data(device_addr, register_addr, int(bus_val, 2))

# I2C Byte Functions
#

def smbus_read_byte (interface, device_addr, register_addr):
	# read i2c bus data byte
	return interface.read_byte_data(device_addr, register_addr)

def smbus_write_byte (interface, device_addr, register_addr, data):
	# write to register
	interface.write_byte_data(device_addr, register_addr, data)

# I2C Burst Functions
#

def smbus_read_burst (interface, device_addr, register_addr, num_bytes):
	# read i2c bus data bytes specified by num_bytes
	# returns list of bytes
	return interface.read_i2c_block_data(device_addr, register_addr, num_bytes)

def smbus_write_burst (interface, device_addr, register_addr, data_list):
	# write list of bytes to register
	interface.write_byte_data(device_addr, register_addr, data_list)


##############
# "Main"
##############

# enable printing
printing_enabled = 1

# i2c bus object
bus = smbus.SMBus(1)

# starting time stamp
t_start = time.time()

# reset the pressure sensor (ensures PROM is properly loaded to internal registers)
smbus_write_byte(bus, press1_addr, reg_reset, 0x00)

# wait non-zero amount of time for reset
time.sleep(0.5)

# read the PROM constant values used to calculate the pressure and temperature
SENS_T1 = smbus_read_word(bus, press1_addr, reg_prom_c1)
SENS_T1 = SENS_T1 << 17

OFF_T1 = smbus_read_word(bus, press1_addr, reg_prom_c2)
OFF_T1 = OFF_T1 << 18

TCS = smbus_read_word(bus, press1_addr, reg_prom_c3)
TCS = TCS >> 7

TCO = smbus_read_word(bus, press1_addr, reg_prom_c4)
TCO = TCO >> 5

T_REF = smbus_read_word(bus, press1_addr, reg_prom_c5)
T_REF = T_REF << 8

TEMPSENS = smbus_read_word(bus, press1_addr, reg_prom_c6)
TEMPSENS = TEMPSENS >> 23

# main loop to keep reading the sensor
while(1):
	# trigger D1 (digital pressure value) conversion
	smbus_write_byte(bus, press1_addr, reg_conv_d1_4096, 0x00)
	# wait longer than the max ADC conversion time (9.04ms for OSR=4096) or data will be corrupt
	time.sleep(0.01)
	# read the 24-bit (3 byte) ADC pressure result
	adc_pressure = smbus_read_burst(bus, press1_addr, reg_adc_read, 3)
	# trigger D2 (digital temperature value) conversion
	smbus_write_byte(bus, press1_addr, reg_conv_d2_4096, 0x00)
	# wait longer than the max ADC conversion time (9.04ms for OSR=4096) or data will be corrupt
	time.sleep(0.01)
	# read the 24-bit (3 byte) ADC temperature result
	adc_temperature = smbus_read_burst(bus, press1_addr, reg_adc_read, 3)

	# convert stored ADC value byte list to 24-bit value
	d1_pressure = (adc_pressure[0] << 16)|(adc_pressure[1] << 8)|(adc_pressure[2])
	d2_pressure = (adc_temperature[0] << 16)|(adc_temperature[1] << 8)|(adc_temperature[2])

	# calculate temperature
	dT = d2_pressure - T_REF 			# 25bit value, Difference between actual and reference temperature
	TEMP = 2000 + (dT * TEMPSENS) 		# Actual temperature (-40...85C with 0.01C resolution)

	# convert temp to proper sensor units
	TEMP_C = TEMP / 100.0 				# Temperature in C
	TEMP_F = TEMP_C * (9.0/5.0) + 32 	# Temperature in F

	# calculate temperature compensated pressure
	OFF = OFF_T1 + (TCO * dT) 					# Offset at actual temperature
	SENS = SENS_T1 + (TCS * dT) 				# Sensitivity at actual temperature
	P = (d1_pressure * (SENS / (2**21)) - OFF) / (2**15) 	# Temperature compensated pressure (0...6000mbar with 0.03mbar resolution)

	# convert pressure to proper sensor units
	P_mbar = P / 100.0 			# Pressur in mBar
	P_pa = P_mbar * 100			# Pressure in Pascals (1Bar = 100,000Pa) --> (1mBar = 100Pa)

	# calculate altitude (in meters) from the pressure reading
	altitude_m = 44330 * (1 - ((P_pa/p0)**(1/5.255)))

	# convert altitude to feet (1m ~= 3.28084 feet)
	altitude_ft = altitude_m * 3.28084

	if (printing_enabled):
		print "Temp (c)     : %f" % TEMP_C
		print "Temp (f)     : %f" % TEMP_F
		print "Press (mBar) : %f" % P_mbar
		print "Altitude (m) : %f" % altitude_m
		print "Altitude (ft): %f" % altitude_ft

		print "elapsed time: %f seconds\n" % (time.time() - t_start)

	time.sleep(1)
