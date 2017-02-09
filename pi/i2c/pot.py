#!/usr/bin/env python

"""
file: pot.py
author: Connor Goldberg
project: High Altitude Balloon Instrumentation Platform
description: API for the digi-pot that controls the ATV transmit power
"""

# sudo apt-get install python-smbus
import smbus

import sys

# Custom i2c class
from i2c import i2c


class digitalPotentiometer(i2c):
	"""
	Abstract the digital potentiometer (MCP454X, 7-bit)
	DataSheet found here:
		http://ww1.microchip.com/downloads/en/DeviceDoc/22107B.pdf
	"""

	# Physical constants
	maxResistance = 9380
	minResistance = 125

	def __init__(self, address=0x2f, busID=None, interface=None):
		# Call super init
		super(self.__class__, self).__init__(address, busID, interface)

		self._writeProtection = True

		# Make a device logger
		self.deviceLogger = self.baseLogger.getLogger("digi-pot")
		self.deviceLogger.log.info("Instantiated the digi-pot")


	def __disableWriteProtection__(self):
		"""
		Disable write protection of the non-volatile registers
		See datasheet page 65
		"""
		self.readWord(regAddress=0xF4)


	def __enableWriteProtection__(self):
		"""
		Disable write protection of the non-volatile registers
		See datasheet page 65
		"""
		self.readWord(regAddress=0xF8)


	def get_writeProtection(self):
		"""
		writeProtection property getter
		"""
		return self._writeProtection


	def set_writeProtection(self, value):
		"""
		writeProtection property setter
		"""
		if type(value) is not bool:
			print "ERROR: writeProtection must be bool"
		else:
			if self.writeProtection != value:
				if value is True:
					self.__enableWriteProtection__()
				else:
					self.__disableWriteProtection__()


	# Link Property
	writeProtection = property(get_writeProtection, set_writeProtection)


	def readRegister(self, regAddress):
		"""
		The digipot's specific protocol for reading a register
		See datasheet page 61, Figure 7-5
		"""
		newAddress = ((regAddress & 0xF) << 4) | 0xC
		data = self.readWord(newAddress)

		if data is None:
			self.deviceLogger.log.error("Could not read register: {}".format(
				hex(regAddress)))
		else:
			self.deviceLogger.log.debug("Read {} from register: {}".format(
				hex(data), hex(regAddress)))

			# Swap nibbles
			data = ((data & 0xFF) << 8) | ((data & 0xFF00) >> 8)
		
		return data


	def writeRegister(self, regAddress, data):
		"""
		The digipot's specific protocol for writing a register
		See datasheet page 59, Figure 7-2
		"""
		newAddress = ((regAddress & 0xF) << 4) | ((data & 0x100) >> 8)
		data = data & 0xff
		if not self.writeWord(newAddress, data):
			self.deviceLogger.log.error("Could not write {} to register: {}"
				.format(hex(data), hex(regAddress)))
			return False
		else:
			self.deviceLogger.log.debug("Wrote {} to register: {}"
				.format(hex(data), hex(regAddress)))
			return True


	@staticmethod
	def valueForResistance(resistance):
		"""
		Calculate the value to write in order to set the resistance in ohms
		Datasheet page 44, Figure 5-2 (7-bit Device)
		"""
		return int(round((resistance-30.0)*(128.0/9380.0)))-1


	@staticmethod
	def resistanceFromValue(value):
		"""
		Calculate the resistance from the value set
		Datasheet page 44, Figure 5-2 (7-bit Device)
		"""
		return int(round(((value+1)*(9380.0/128.0))+30))


	def setResistance(self, resistance):
		"""
		Sets the resistance of the digi-pot to the resistance parameter
		"""
		data = digitalPotentiometer.valueForResistance(resistance)
		if data < 0x0:
			data = 0x0 # Min value
		elif data > 0x80:
			data = 0x80 # Max value
		self.deviceLogger.log.info("Setting resistance to {} (~{})".format(
			resistance, digitalPotentiometer.resistanceFromValue(data)))
		pot.writeRegister(regAddress=0x0, data=data)


################################################################################

# Just some testing
if __name__ == "__main__":
	
	pot = digitalPotentiometer(busID=1)
	if pot.interface is None:
		print "Fail"
		sys.exit(1)

	# for r in range(0,4):
	# 	print "Reg {} = {}".format(r, hex(pot.readRegister(r)))

	# pot.writeRegister(0x0, 0x40)

	## Set resistance
	pot.setResistance(7778)
	wiper0 = pot.readRegister(0x0)
	if wiper0:
		print "Wiper 0 = {}".format(hex(wiper0))
