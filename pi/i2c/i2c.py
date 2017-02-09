"""
file: i2c.py
author: Connor Goldberg
project: High Altitude Balloon Instrumentation Platform
description: Abstracts some functionality of the i2c interface
"""

# Add the pi directory to $PYTHONPATH then export it
import logger

# sudo apt-get install python-smbus
import smbus

class i2c(object):
	"""
	Abstract some basic i2c functionality using the smbus module to provide
	consistency
	"""

	def __init__(self, address=None, busID=None, interface=None):
		"""
		address - The I2C address of the device you want to communicate with
		busID - The I2C bus ID to use if not providing an interface
		interface - An SMBus interface to use instead of initializing one
		"""
		
		if address is not None:
			self.address = address
		else:
			print "ERROR: must provide an address"

		if busID is None and interface is None:
			print "ERROR: must provide either a busID or an i2c interface \
				object (SMBus)"
			sys.exit(1)

		elif interface is not None:
			self.interface = interface

		else:
			self.busID = busID
			try:
				self.interface = smbus.SMBus(self.busID)
			except IOError as e:
				print "IOError: {}".format(e)
				sys.exit(1)

		# Defaults that can be overwritten
		self.maxReadAttempts = 3
		self.maxWriteAttempts = 3


	def readByte(self, regAddress):
		attempts = 0
		while attempts < self.maxReadAttempts:
			try:
				return self.interface.read_byte_data(self.address, regAddress)
			except IOError as e:
				print "IOError: {}".format(e)
				attempts += 1

		return None

	def readWord(self, regAddress):
		attempts = 0
		while attempts < self.maxReadAttempts:
			try:
				return self.interface.read_word_data(self.address, regAddress)
			except IOError as e:
				print "IOError: {}".format(e)
				attempts += 1

		return None

	def writeByte(self, regAddress, data=0):
		attempts = 0
		while attempts < self.maxWriteAttempts:
			try:
				self.interface.write_byte_data(self.address, regAddress, data)
				return True
			except IOError as e:
				print "IOError: {}".format(e)
				attempts += 1

		return False


	def writeWord(self, regAddress, data=0):
		attempts = 0
		while attempts < self.maxWriteAttempts:
			try:
				self.interface.write_word_data(self.address, regAddress, data)
				return True
			except IOError as e:
				print "IOError: {}".format(e)
				attempts += 1

		return False
