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

class gpsData(object):

	def __init__(self):
		self.lat = None
		self.lon = None
		self.date = None
		self.time = None
		self.alt = None
		self.speed = None
		self.lock = False

	def __str__(self):
		return "lat: {}, lon: {}, date: {}, time: {}, alt: {}, speed: {}, lock: {}".format(self.lat, self.lon, self.date, self.time, self.alt, self.speed, self.lock)

	def __repr__(self):
		return str(self)

class gps(i2c):
	def __init__(self, address=0x42, busID=0, interface=None):
		# Call super init
		super(self.__class__, self).__init__(address, busID, interface)

		# Make a device logger
		self.deviceLogger = self.baseLogger.getLogger("gps")
		self.deviceLogger.log.info("Instantiated the gps")

		# Following configs taken from u-blox M8 receiver description, Protocol Specification PDF
		# https://www.u-blox.com/sites/default/files/products/documents/u-blox8-M8_ReceiverDescrProtSpec_(UBX-13003221)_Public.pdf
		self.disable_i2c_gsa = [0xB5, 0x62, 0x06, 0x01, 0x08, 0x00, 0xF0, 0x02, 0x00, 0x01, 0x00, 0x01, 0x01, 0x00, 0x04, 0x3B]
		self.disable_i2c_gll = [0xB5, 0x62, 0x06, 0x01, 0x08, 0x00, 0xF0, 0x01, 0x00, 0x01, 0x00, 0x01, 0x01, 0x00, 0x03, 0x34]
		self.disable_i2c_gsv = [0xB5, 0x62, 0x06, 0x01, 0x08, 0x00, 0xF0, 0x03, 0x00, 0x01, 0x00, 0x01, 0x01, 0x00, 0x05, 0x42]
		#self.disable_i2c_vtg = [0xB5, 0x62, 0x06, 0x01, 0x08, 0x00, 0xF0, 0x05, 0x00, 0x01, 0x00, 0x01, 0x01, 0x00, 0x07, 0x50]

		self.config()

	def readRegister(self, regAddress):
		"""
		The gps's specific protocol for reading a register
		0xfd = number of bytes available, msb
		0xfe = number of bytes available, lsb
		0xff = data stream
		"""
		data = self.readWord(regAddress)

		if data is None:
			self.deviceLogger.log.debug("Could not read register: {}".format(
				hex(regAddress)))
		else:
			self.deviceLogger.log.debug("Read {} from register: {}".format(
				hex(data), hex(regAddress)))
		
		return ((data << 8) & 0xff00) | ((data >> 8) & 0xff) 


	def writeRegister(self, regAddress, data):
		"""
		The gps's specific protocol for writing a register
		"""
		data = data & 0xff
		if not self.writeWord(regAddress, data):
			self.deviceLogger.log.debug("Could not write {} to register: {}"
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


	def config(self):
		"""
		Writes to the GPS configuration port, telling the GPS to turn off sending specific data points during data acquisition
		"""
		# GPS doesn't require a register address, so start with data
		self.writeBlock(self.disable_i2c_gll[0], self.disable_i2c_gll[1:])
		self.writeBlock(self.disable_i2c_gsa[0], self.disable_i2c_gsa[1:])
		self.writeBlock(self.disable_i2c_gsv[0], self.disable_i2c_gsv[1:])


	def get_data(self):
		"""
		Reads the GPS data bytestream
		Returns a list of important data
			latitude (string)
			longitude (string)
			date (date object)
			time (time object)
			altitude (float)
			speed (float)
		"""
		# Perform the config command, because why not
		self.config()

		# Get the byte stream as a continuous string of ASCII character
		byte_stream = self.readByteStream()

		# Convert continuous string to list of string of messages
		commands = byte_stream.splitlines()

		# Blank line
		if commands[-1] == '\x7f':
			commands = commands[:-1]

		# Parse commands using pynmea2 package
		parsed = []
		for command in commands:
			try:
				parsed.append(pynmea2.parse(command))
			except Exception as e:
				self.deviceLogger.log.debug("Error parsing commands from GPS")
				self.deviceLogger.log.debug("Got exception: {}".format(e))
				return gpsData()

		# Check and see if the GPS is locked	
		status = parsed[0].status
		if status == 'A':
			# Extract data from the command
			lat = parsed[0].lat
			lon = parsed[0].lon
			lat_dir = parsed[0].lat_dir
			lon_dir = parsed[0].lon_dir
			date = parsed[0].datestamp
			time = parsed[2].timestamp
			alt = parsed[2].altitude
			speed = parsed[0].spd_over_grnd

			# Format latitude better
			lat_deg = int(lat[0:2])
			lat_min = int(lat[2:4])/60.0
			lat_sec = float(lat[4:10])/60.0
			lat_dec = lat_deg + lat_min + lat_sec

			# Format longitude better
			lon_deg = int(lon[0:3])
			lon_min = int(lon[3:5])/60.0
			lon_sec = float(lon[5:11])/60.0
			lon_dec = lon_deg + lon_min + lon_sec
		
			# Append +/- latitude
			if (lat_dir == 'S'):
				lat_dec = lat_dec * -1

			# Append +/- longitutde
			if (lon_dir == 'W'):
				lon_dec = lon_dec * -1

			data = gpsData()
			data.lat = lat_dec
			data.lon = lon_dec
			data.date = date
			data.time = time
			data.alt = alt
			data.speed = speed
			data.lock = True

			return data

		else:
			return gpsData()
