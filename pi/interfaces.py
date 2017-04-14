"""
author: Connor Goldberg
project: High Altitude Balloon Instrumentation Platform
description: Holder for all of the pi interfaces
"""

import gpio
import i2c
import spi
import uart

import logger

class interfaces(object):
	"""
	Object to hold all of the interfaces
	"""

	# Static members
	gpio = None
	i2c = None
	spi = None
	uart = None

	def __init__(self):
		self.logger = logger.logger("interfaces")

	def opengpio(self):
		interfaces.gpio = gpio.gpio()
		self.logger.log.debug("Opened GPIO interface")

	def openspi(self):
		interfaces.spi = spi.spi()
		self.logger.log.debug("Opened SPI interface")

	def openuart(self, port, baudrate):
		interfaces.uart = uart.uart(port=port, baudrate=baudrate)
		if interfaces.uart.open():
			self.logger.log.debug("Opened UART interface")
			return True
		else:
			self.logger.log.error("Could not open UART interface")
			return False
