"""
author: Connor Goldberg
project: High Altitude Balloon Instrumentation Platform
description: SPI Interface
"""

import spidev

import common
import logger


class spi(object):
	"""
	Abstract the Pi's SPI interface
	"""

	def __init__(self, busIndex=0, deviceIndex=0, maxSpeed=150000, logDebug=False):
		self.logger = logger.logger("spi")
		if not logDebug:
			self.logger.changeLevel(logger.logger.INFO) # Don't log DEBUG

		self.busIndex = busIndex
		self.deviceIndex = deviceIndex
		self.maxSpeed = maxSpeed
		self.interface = spidev.SpiDev()

		try:
			self.interface.open(busIndex,deviceIndex)
			self.interface.max_speed_hz = maxSpeed
			self.interface.cshigh = False
			self.isOpen = True
		except Exception as e:
			self.interface = None
			self.isOpen = False
			self.logger.log.error("Could not open SPI interface: {}".format(e))

		self.logger.log.info("Opened SPI interface: /dev/spidev{}.{}".format(
			self.busIndex, self.deviceIndex))

	def close(self):
		self.logger.log.info("Closed SPI interface: /dev/spidev{}.{}".format(
			self.busIndex, self.deviceIndex))
		self.interface.close()

	def sendString(self, string):
		"""
		Sends a string over the spi interface
		"""

		packet = [ord(c) for c in string]
		response = []

		for byte in packet:
			resp = self.sendByte(byte)
			if resp:
				response.append(resp)

		self.logger.log.debug("sent string: {}".format(string))
		return response

	def sendByte(self, byte):
		"""
		Sends a single byte over the spi interface
		"""

		resp = None
		try:
			resp = self.interface.xfer2([byte])[0]
			self.logger.log.debug("sent byte: {}, received byte: {}"
				.format(hex(byte), hex(resp)))
		except Exception as e:
			self.logger.log.error("could not send byte: {}, Exception: {}"
				.format(hex(byte), e))

		return resp

	def readByte(self):
		"""
		Send's a dont care byte to read the response
		"""
		return self.sendByte(byte=ord('X'))

	def readChar(self):
		"""
		Reads a byte as an ASCII character
		"""
		return chr(self.readByte())


########### Testing #############
if __name__ == "__main__":
	mySpi = spi()

	data = "{00:B4:ZGY}"
	
	mySpi.sendString(data)
	resp = mySpi.readString()

	print resp

	mySpi.close()
