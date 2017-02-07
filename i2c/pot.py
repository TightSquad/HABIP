#!/usr/bin/env python

import smbus
import sys


class digitalPotentiometer(object):
	"""
	Abstract the digital potentiometer
	DataSheet found here: http://ww1.microchip.com/downloads/en/DeviceDoc/22107B.pdf
	"""

	def __init__(self, address=0x2f, bus=None, interface=None):
		"""
		address - The I2C addres of the potentiometer
		bus - The I2C bus ID to use if not providing an interface
		interface - An SMBus interface to use instead of initializing one
		"""

		self.address = address

		if bus is None and interface is None:
			print "ERROR: must provide either a busID or an i2c interface object (SMBus)"
			sys.exit(1)

		elif interface is not None:
			self.interface = interface

		else:
			self.bus = bus
			try:
				self.interface = smbus.SMBus(self.bus)
			except Exception as e:
				print e

	def readRegister(self, regAddress):
		regAddress = ((regAddress & 0xF) << 4) | 0xC
		data = self.interface.read_word_data(self.address, regAddress)

		# Swap nibbles
		data = ((data & 0xFF) << 8) | ((data & 0xFF00) >> 8)
		return data


	def writeRegister(self, regAddress, data):
		regAddress = ((regAddress & 0xF) << 4) | ((data & 0x100) >> 8)
		data = data & 0xff
		# print "Writing:\n{0:8b}\n{1:8b}".format(regAddress, data)
		self.interface.write_word_data(self.address, regAddress, data)

	def valueForOhms(self, ohms):
		return int(round((ohms-30.0)*(128.0/9380.0)))

	def setResistance(self, ohms):
		data = self.valueForOhms(ohms)
		data = data if data < 0x80 else 0x80
		pot.writeRegister(regAddress=0x0, data=data)

# pot = digitalPotentiometer(bus=1)
# if pot.interface is None:
# 	print "Fail"
# 	sys.exit(1)


# for r in range(0,4):
# 	print "Reg {} = {}".format(r, hex(pot.readRegister(r)))

# pot.writeRegister(0x0, 0x40)
# print "Wiper 0 = {}".format(hex(pot.readRegister(0x0)))

## Set resistance
# pot.setResistance(950)
