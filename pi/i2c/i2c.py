"""
file: i2c.py
authors: Connor Goldberg, Chris Schwab
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


	#
	#	Read byte from I2C bus
	#
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

	#
	#	Read word from I2C bus
	#
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

	#
	#	Most I2C transmit MSByte first, so the recieved word byte order needs to be swapped for most devices
	#
	def readWordSwapped(self, regAddress):
		data = self.readWord(regAddress)

		if (data == None):
			return None
		else:
			# Swap bytes
			return ((data & 0xFF) << 8) | ((data & 0xFF00) >> 8)

	#
	#	Read block from I2C bus (returns list = [first_byte_received, second byte_received, ...]
	#
	def readBlock (self, regAddress, numBytes):
		attempts = 0
		while attempts < self.maxReadAttempts:
			try:
				byte_list = self.interface.read_i2c_block_data(self.address, regAddress, numBytes)
				self.baseLogger.log.debug(
					"Received bytes: {}, from device: {}, register: {}".format(
						map(hex, byte_list), hex(self.address), hex(regAddress)))
				return byte_list
			except IOError as e:
				self.baseLogger.log.warning("IOError: {}".format(e))
				attempts += 1

		self.baseLogger.log.error("Failed to read bytes from device: \
			{}, register: {} after {} attempts".format(
				hex(self.address), hex(regAddress), attempts))
		return None

	#
	#	Write byte to I2C bus
	#
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

	#
	#	Write word to I2C bus
	#
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

	#
	#	Most I2C transmit MSByte first, so the transmitted word byte order needs to be swapped for most devices
	#
	def writeWordSwapped(self, regAddress, data=0):
		# Swap bytes
		data = ((data & 0xFF) << 8) | ((data & 0xFF00) >> 8)
		return self.writeWord(regAddress, data)

	#
	#	Write block to I2C bus (sends list = [first_byte_transmitted, second byte_transmitted, ...]
	#
	def writeBlock (self, regAddress, dataList=[]):
		attempts = 0
		while attempts < self.maxWriteAttempts:
			try:
				self.interface.write_i2c_block_data(self.address, regAddress, dataList)
				self.baseLogger.log.debug(
					"Sent bytes: {}, to device: {}, register: {}".format(
						map(hex, dataList), hex(self.address), hex(regAddress)))
				return True
			except IOError as e:
				self.baseLogger.log.warning("IOError: {}".format(e))
				attempts += 1

		self.baseLogger.log.error("Failed to write bytes: {} to device: \
			{}, register: {} after {} attempts".format(
				map(hex, dataList), hex(self.address), hex(regAddress), attempts))
		return False

	#
	# 	Initiates a register-address-less read / write used by some sensors
	#		- offers alternative over sensors that need clock stretching for extended conversion time
	# 		- M=master, S=slave, W=write bit set, R=read dbit set, pkts=byte packets
	# 		- standard I2C read protocol: M[slave_address,W] M[slave_register_addr] M[slave_address,R] S[data_packets]
	# 									 |--------------------------------readByte------------------------------------|
	# 								or	 |--------------------------------readWordSwapped-----------------------------|
	# 								or 	 |--------------------------------readBurst-----------------------------------|
	# 		- "stretched" I2C read protocol: M[slave_address,W] M[slave_register_addr] {TIME DELAY FOR CONVERSION} M[slave_address,R] S[data_packets]
	# 										 |--------------sendWrite----------------| |----------delay----------| |--------sendRead x #pkts--------|
	#
	def sendRead(self):
		attempts = 0
		while attempts < self.maxReadAttempts:
			try:
				byte = self.interface.read_byte(self.address)
				self.baseLogger.log.debug(
					"Received byte: {}, from device: {}, register: N/A (stretched read packet only)".format(
						hex(byte), hex(self.address)))
				return byte
			except IOError as e:
				self.baseLogger.log.warning("IOError: {}".format(e))
				attempts += 1

		self.baseLogger.log.error("Failed to read byte from device: \
			{}, register: N/A (stretched read packet only) after {} attempts".format(
				hex(self.address), attempts))
		return None

	def sendWrite(self, data=0):
		attempts = 0
		while attempts < self.maxWriteAttempts:
			try:
				self.interface.write_byte(self.address, data)
				self.baseLogger.log.debug(
					"Sent byte: {}, from device: {}, register: N/A (stretched write packet only)".format(
						hex(byte), hex(self.address)))
				return True
			except IOError as e:
				self.baseLogger.log.warning("IOError: {}".format(e))
				attempts += 1

		self.baseLogger.log.error("Failed to write byte: {} to device: \
			{}, register: N/A (stretched write packet only) after {} attempts".format(
				hex(data), attempts))
		return False
