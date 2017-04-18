#!/usr/bin/env python

"""
author: Matt Zachary
project: High Altitude Balloon Instrumentation Platform
description: API for the MAX-M8Q GPS
"""

# sudo apt-get install python-smbus
import smbus

import sys

# Command parser
import pynmea2

# Custom i2c class
from i2c import i2c

# UBlox MSG commands - disable messages sent over I2C
disable_i2c_gsa = [0xB5, 0x62, 0x06, 0x01, 0x08, 0x00, 0xF0, 0x02, 0x00, 0x01, 0x00, 0x01, 0x01, 0x00, 0x04, 0x3B]
disable_i2c_gll = [0xB5, 0x62, 0x06, 0x01, 0x08, 0x00, 0xF0, 0x01, 0x00, 0x01, 0x00, 0x01, 0x01, 0x00, 0x03, 0x34]
disable_i2c_gsv = [0xB5, 0x62, 0x06, 0x01, 0x08, 0x00, 0xF0, 0x03, 0x00, 0x01, 0x00, 0x01, 0x01, 0x00, 0x05, 0x42]
disable_i2c_vtg = [0xB5, 0x62, 0x06, 0x01, 0x08, 0x00, 0xF0, 0x05, 0x00, 0x01, 0x00, 0x01, 0x01, 0x00, 0x07, 0x50]

class gps(i2c):
	def __init__(self, address=0x42, busID=None, interface=None):
		# Call super init
		super(self.__class__, self).__init__(address, busID, interface)

		# Make a device logger
		self.deviceLogger = self.baseLogger.getLogger("gps")
		self.deviceLogger.log.info("Instantiated the gps")

	def readRegister(self, regAddress):
		"""
		The gps's specific protocol for reading a register
		0xfd = number of bytes available, msb
		0xfe = number of bytes available, lsb
		0xff = data stream
		"""
		data = self.readWord(regAddress)

		if data is None:
			self.deviceLogger.log.error("Could not read register: {}".format(
				hex(regAddress)))
		else:
			self.deviceLogger.log.debug("Read {} from register: {}".format(
				hex(data), hex(regAddress)))
		
		return ((data << 8) & 0xff00) | ((data >> 8) & 0xff) 


	def writeRegister(self, regAddress, data):
		"""
		The gps's specific protocol for writing a register
		"""
		if not self.writeWord(regAddress, data):
			self.deviceLogger.log.error("Could not write {} to register: {}"
				.format(hex(data), hex(regAddress)))
			return False
		else:
			self.deviceLogger.log.debug("Wrote {} to register: {}"
				.format(hex(data), hex(regAddress)))
			return True

	def readByteStream(self):
		"""
		Read the byte stream, sent every 1 second by the GPS
		Returns a string of the byte stream
		"""

		# Read that data stream register
		data_read = self.readRegister(0xff)

		# Wait until there's only 0xffff
		# i.e. done reading previous stream
		while data_read != 0xffff:
			data_read = self.readRegister(0xff)

		# Loop until there's no more 0xffff
		# Meaning the next stream is ready
		while data_read == 0xffff:
			data_read = self.readRegister(0xff)
	
		# Now we're into actual data, make a list
		byte_stream = [data_read]
		data_read = 0x0000

		# Now, wait until theres no more 0xffff
		# End of stream
		while data_read != 0xffff:
			data_read = self.readRegister(0xff)
			byte_stream.append(data_read)
		
		byte_stream = byte_stream[:-1]
		byte_stream_string = ""

		# Convert to string
		for x in byte_stream:
			# The MSbit seems to be getting corrupted
			# Ignore it, we don't actually need it for ascii :)
			lsb = chr(x & 0x7f)
			msb = chr((x & 0x7f00) >> 8)

			byte_stream_string = byte_stream_string + msb
			byte_stream_string = byte_stream_string + lsb
	
		return byte_stream_string

################################################################################

# Just some testing
if __name__ == "__main__":
	
	# Generate GPS instance
	my_gps = gps(busID=0)
	if my_gps.interface is None:
		print "Fail"
		sys.exit(1)

	# GPS doesn't require a register address, so start with data
	my_gps.writeBlock(disable_i2c_gll[0], disable_i2c_gll[1:])
	my_gps.writeBlock(disable_i2c_gsa[0], disable_i2c_gsa[1:])
	my_gps.writeBlock(disable_i2c_gsv[0], disable_i2c_gsv[1:])
	my_gps.writeBlock(disable_i2c_vtg[0], disable_i2c_vtg[1:])
	