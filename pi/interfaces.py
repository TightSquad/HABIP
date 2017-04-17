"""
author: Connor Goldberg
project: High Altitude Balloon Instrumentation Platform
description: Holder for all of the pi interfaces
"""

import cameraMux
import gpio
import i2c
import osd232
import spi
import uart

import logger

class interfaces(object):
	"""
	Object to hold all of the interfaces
	"""

	# Static members
	cameraMux = None
	gpio = None
	i2c = None
	spi = None
	uart = None
	osd232 = None

	def __init__(self):
		self.logger = logger.logger("interfaces")

	def opencameramux(self):
		if interfaces.gpio is not None:
			interfaces.cameraMux = cameraMux.cameraMux(interfaces.gpio)
			interfaces.cameraMux.selectCamera(0)
		else:
			self.logger.log.error("Cannot open camera mux interface before GPIO")

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

	def openosd232(self, port="/dev/ttyAMA0", baudrate=4800):
		interfaces.osd232 = osd232.osd232(port=port)
		interfaces.uart = interfaces.osd232.connection
