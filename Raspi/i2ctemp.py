#!/usr/bin/python

# python library for 2 wire comms, including i2c. 
import smbus
import time
# unicode
degree_sign= u'\N{DEGREE SIGN}'

"""
readTempF 
Function to obtain current temperature and print to prompt

Note: Hard configured for PCT2075 I2C Temperature Sensor with
all three address pins tied to ground -> (0x48)

TODO: Address / Reg as inputs to function

=== Inputs ===

=== Outputs ===
	Command prompt output of timestamp with temperature in degF. 
"""
def readTempF():
	
	TEMP_REG = 0x00
	# All three address pins tied to ground
	DEVICE_ADDR = 0x48
	DEVICE_BUS = 1
	bus = smbus.SMBus(DEVICE_BUS)

	raw_w = bus.read_word_data(DEVICE_ADDR, TEMP_REG)
	# raw word is switched in the order of bytes. 
	MSByte = raw_w & 0xFF
	LSByte = raw_w/256
	word = MSByte*256 + LSByte
	# check for negative vs. positive temperature
	if word > 32767:
		sign = '-'
		word = word & 0x7FFF
                temp = ~(word/32) + 1
        else:
		sign = ''
		temp = (word/32)*0.125
	tempf = temp *(1.8) + 32
	timestamp = time.asctime( time.localtime(time.time()) )
	print '\n ' + timestamp + '   -------    ' + sign +  str(tempf) + degree_sign + 'F\n'	

"""
i2cgrabTemp 
Function to obtain current temperature and return it

Note: Hard configured for PCT2075 I2C Temperature Sensor with
all three address pins tied to ground -> (0x48)

TODO: Address / Reg as inputs to function
TODO: Relative to mission start timestamp

=== Inputs ===

=== Outputs ===
	Returns: 
		temp --- temperature in degC
		tempf --- temperature in degF
		timestamp 
"""
def i2cgrabTemp():
	
	TEMP_REG = 0x00
	# All three address pins tied to ground
	DEVICE_ADDR = 0x48
	DEVICE_BUS = 1
	bus = smbus.SMBus(DEVICE_BUS)

	raw_w = bus.read_word_data(DEVICE_ADDR, TEMP_REG)
	# raw word is switched in the order of bytes. 
	MSByte = raw_w & 0xFF
	LSByte = raw_w/256
	word = MSByte*256 + LSByte
	# check for negative vs. positive temperature
	if word > 32767:
		sign = '-'
		word = word & 0x7FFF
                temp = ~(word/32) + 1
        else:
		sign = ''
		temp = (word/32)*0.125
	tempf = temp *(1.8) + 32
	timestamp = time.asctime( time.localtime(time.time()) )
	return temp,tempf,timestamp
