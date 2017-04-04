"""
file: i2c.py
author: Connor Goldberg
project: High Altitude Balloon Instrumentation Platform
description: Abstracts some functionality of the i2c interface
"""

import smbus
import sys

import logger


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
		
		# Create the logger
		self.baseLogger = logger.logger("i2c")

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
				byte = self.interface.read_byte_data(self.address, regAddress)
				self.baseLogger.log.debug(
					"Received byte: {}, from device: {}, register: {}".format(
						hex(byte), hex(self.address), hex(regAddress)))
				return byte
			except IOError as e:
				self.baseLogger.log.warning("IOError: {}".format(e))
				attempts += 1

		self.baseLogger.log.error("Failed to read byte from device: \
			{}, register: {} after {} attempts".format(
				hex(self.address), hex(regAddress), attempts))
		return None

	def readWord(self, regAddress):
		attempts = 0
		while attempts < self.maxReadAttempts:
			try:
				word = self.interface.read_word_data(self.address, regAddress)
				self.baseLogger.log.debug(
					"Received word: {}, from device: {}, register: {}".format(
						hex(word), hex(self.address), hex(regAddress)))
				return word
			except IOError as e:
				self.baseLogger.log.warning("IOError: {}".format(e))
				attempts += 1

		self.baseLogger.log.error("Failed to read word from device: \
			{}, register: {} after {} attempts".format(
				hex(self.address), hex(regAddress), attempts))
		return None

	def readWordSwapped(self, regAddress):
		data = self.readWord(regAddress)
		
		# Swap nibbles
		return ((data & 0xFF) << 8) | ((data & 0xFF00) >> 8)

	def writeByte(self, regAddress, data=0):
		attempts = 0
		while attempts < self.maxWriteAttempts:
			try:
				self.interface.write_byte_data(self.address, regAddress, data)
				self.baseLogger.log.debug(
					"Sent byte: {}, to device: {}, register: {}".format(
						hex(data), hex(self.address), hex(regAddress)))
				return True
			except IOError as e:
				self.baseLogger.log.warning("IOError: {}".format(e))
				attempts += 1

		self.baseLogger.log.error("Failed to write byte: {} to device: \
			{}, register: {} after {} attempts".format(
				hex(data), hex(self.address), hex(regAddress), attempts))
		return False


	def writeWord(self, regAddress, data=0):
		attempts = 0
		while attempts < self.maxWriteAttempts:
			try:
				self.interface.write_word_data(self.address, regAddress, data)
				self.baseLogger.log.debug(
					"Sent word: {}, to device: {}, register: {}".format(
						hex(data), hex(self.address), hex(regAddress)))
				return True
			except IOError as e:
				self.baseLogger.log.warning("IOError: {}".format(e))
				attempts += 1

		self.baseLogger.log.error("Failed to write word: {} to device: \
			{}, register: {} after {} attempts".format(
				hex(data), hex(self.address), hex(regAddress), attempts))
		return False

	def writeWordSwapped(self, regAddress, data=0):
		# Swap nibbles
		data = ((data & 0xFF) << 8) | ((data & 0xFF00) >> 8)
		self.writeWord(regAddress, data)