#!/usr/bin/python
## TODO add negative temperature compatability
import smbus
import time
degree_sign= u'\N{DEGREE SIGN}'
debug = 1
def setupI2Cbus(DEVICE_BUS):
	bus = smbus.SMBus(DEVICE_BUS)

def readTempF():
	
	TEMP_REG = 0x00
	DEVICE_ADDR = 0x48
	DEVICE_BUS = 1
	bus = smbus.SMBus(DEVICE_BUS)

	raw_w = bus.read_word_data(DEVICE_ADDR, TEMP_REG)
	MSByte = raw_w & 0xFF
	LSByte = raw_w/256
	word = MSByte*256 + LSByte
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
def i2cgrabTemp():
	
	TEMP_REG = 0x00
	DEVICE_ADDR = 0x48
	DEVICE_BUS = 1
	bus = smbus.SMBus(DEVICE_BUS)

	raw_w = bus.read_word_data(DEVICE_ADDR, TEMP_REG)
	MSByte = raw_w & 0xFF
	LSByte = raw_w/256
	word = MSByte*256 + LSByte
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
