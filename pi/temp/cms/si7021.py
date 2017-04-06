#!/usr/bin/env python

"""
file: si7021.py
author: Chris Schwab
project: High Altitude Balloon Instrumentation Platform
description: Demo script for the Si7021-A20 I2C humidity sensor
	
	data-sheet: http://www.silabs.com/documents/public/data-sheets/Si7021-A20.pdf
"""

# sudo apt-get install python-smbus
import smbus
import time

##############
# "Constants"
##############

# sensor registers
#
# HMM --> clock stretching
# NHMM --> not ack read requests
#
reg_meas_rel_humid_hmm  = 0xE5 	# W: w  : Measure Relative Humidity, Hold Master Mode (also triggers a Temp measurement, use reg 0xE0 to read it)
reg_meas_rel_humid_nhmm = 0xF5 	# W: w  : Measure Relative Humidity, No Hold Master Mode (also triggers a Temp measurement, use reg 0xE0 to read it)
reg_meas_temp_hmm       = 0xE3 	# W: w  : Measure Temperature, Hold Master Mode (this takes a new temperature measurement)
reg_meas_temp_nhmm 		= 0xF3 	# W: w  : Measure Temperature, No Hold Master Mode (this takes a new temperature measurement)
reg_prev_temp_value 	= 0xE0 	# W: w  : Read Temperature Value from Previous RH Measurement
reg_reset 				= 0xFE 	# B: w  : Reset
reg_write_user_reg1 	= 0xE6 	# B: w  : Write RH/T User Register 1

								# 		Set RES[1:0] = 00 for 12bit RH / 14bit Temp conv. Total time = t_convRH + t_convT = 12ms + 10.8ms = 22.8ms MAX
USER_REG_RES1 			= 0x80 	# r/w 	: Measurement resolution bit 1
USER_REG_RES0 			= 0x01 	# r/w 	: Measurement resolution bit 0
USER_REG_VDDS 			= 0x40 	# r 	: Vdd Status (0 = Vdd OK, 1 = Vdd low)
USER_REG_HTRE 			= 0x04 	# w/r 	: On-chip heater enable (0 = disable, 1 = enable)

reg_read_user_reg1 		= 0xE7 	# B: w  : Read RH/T User Register 1
reg_write_heat_ctrl 	= 0x51 	# B: w  : Write Heater Control Register (HEATER[3:0] sets heater power)
reg_read_heat_ctrl 		= 0x11 	# B: w  : Read Heater Control Register

# sensor addresses
humid0_addr = 0x40	# SI7021 humidity sensor

##############
# "functions"
##############

# I2C Data Word Functions
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

# I2C Data Byte Functions
#

def smbus_read_byte (interface, device_addr, register_addr):
	# read i2c bus data byte
	return interface.read_byte_data(device_addr, register_addr)

def smbus_write_byte (interface, device_addr, register_addr, data):
	# write to register
	interface.write_byte_data(device_addr, register_addr, data)

# I2C Data Burst Functions
#

def smbus_read_burst (interface, device_addr, register_addr, num_bytes):
	# read i2c bus data bytes specified by num_bytes
	# returns list of bytes
	return interface.read_i2c_block_data(device_addr, register_addr, num_bytes)

def smbus_write_burst (interface, device_addr, register_addr, data_list):
	# write list of bytes to register
	interface.write_byte_data(device_addr, register_addr, data_list)

# I2C single byte bus transactions
#

def smbus_send_read (interface, device_addr):
	# initiate byte read from i2c device
	return interface.read_byte(device_addr)

def smbus_send_write (interface, device_addr, register_addr):
	# initiate byte write to i2c device
	interface.write_byte(device_addr, register_addr)


##############
# "Main"
##############

# enable printing
printing_enabled = 1

# i2c bus object
bus = smbus.SMBus(1)

# starting time stamp
t_start = time.time()

# configure user control registers
# 	- as per data sheet, read reg first, change ONLY the bits you want to change, then write back
# 	- 12bit RH / 14bit Temp, no heater --> 0x0XXXX0X0 (this is the POR default but just making sure)
user_reg_value = smbus_read_byte(bus, humid0_addr, reg_read_user_reg1)
print "POR User Reg 1 value: " + str(hex(user_reg_value))
user_reg_value = user_reg_value & ((USER_REG_RES1 | USER_REG_RES0 | USER_REG_HTRE) ^ 0xFF)
print "Writing User Reg 1 value: " + str(hex(user_reg_value))
smbus_write_byte(bus, humid0_addr, reg_write_user_reg1, user_reg_value)
# verify
user_reg_value = smbus_read_byte(bus, humid0_addr, reg_read_user_reg1)
print "User Reg 1 set value: " + str(hex(user_reg_value))

# main loop to keep reading the sensor
while(1):
	# trigger humidity/temperature measurement with manual delay for conversion time (NHMM)
	smbus_send_write(bus, humid0_addr, reg_meas_rel_humid_nhmm)
	# wait for conversion time --> max t_conv = 22.8ms
	time.sleep(0.3)
	# read back humidity MSByte
	rh_byte1 = smbus_send_read(bus, humid0_addr)
	# read back humidity LSByte
	rh_byte0 = smbus_send_read(bus, humid0_addr)
	# shift to get the rh_code
	rh_code = (rh_byte1 << 8) | (rh_byte0)
	# convert rh_code to %RH
	rh_percent = ((125 * rh_code) / 65536.0) - 6
	# read the temperture value used in the humidity conversion
	temp_code = smbus_read_word(bus, humid0_addr, reg_prev_temp_value)
	# convert temp_code to C
	temp_c = ((175.72 * temp_code) / 65536.0) - 46.85
	#convert temp_c to F
	temp_f = temp_c * (9.0/5.0) + 32

	# trigger stand alone temperature reading
	smbus_send_write(bus, humid0_addr, reg_meas_temp_nhmm)
	# wait for conversion time --> max t_conv = 10.8ms
	time.sleep(0.3)
	# read back tmep MSByte
	temp_sa_byte1 = smbus_send_read(bus, humid0_addr)
	# read back humidity LSByte
	temp_sa_byte0 = smbus_send_read(bus, humid0_addr)
	# shift to get the rh_code
	temp_sa_code = (temp_sa_byte1 << 8) | (temp_sa_byte0)
	# convert temp_sa_code to C
	temp_sa_c = ((175.72 * temp_sa_code) / 65536.0) - 46.85
	#convert temp_sa_c to F
	temp_sa_f = temp_c * (9.0/5.0) + 32

	if (printing_enabled):
		print "Rel.Humid (%%): %f" % rh_percent
		print "Temp (c)     : %f" % temp_c
		print "Temp (f)     : %f" % temp_f
		print "SA_Temp (c)     : %f" % temp_sa_c
		print "SA_Temp (f)     : %f" % temp_sa_f

		print "elapsed time: %f seconds\n" % (time.time() - t_start)

	time.sleep(1)
