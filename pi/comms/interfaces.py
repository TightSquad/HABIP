"""
author: Connor Goldberg
project: High Altitude Balloon Instrumentation Platform
description: Holder for all of the pi interfaces
"""

import logger

import beacon
import board
import cameraMux
import daqcsComms
import gpio
import gps
import osd232
import habip_osd
import spi
import temp_pct2075
import press_ms5607
import uart
import watchdog


class interfaces(object):
	"""
	Object to hold all of the interfaces
	"""

	def __init__(self):
		self.logger = logger.logger("interfaces")

		self.beacon = None
		self.boards = None
		self.cameraMux = None
		self.daqcs = None
		self.gpio = None
		self.gps = None
		self.habip_osd = None
		self.spi = None
		self.temperature = None
		self.pressure = None
		self.uart = None
		self.osd232 = None
		self.watchdog = None

		# Initalize the boards and the data
		self.boards = {}
		for boardID, boardNum in board.board.num.iteritems():
			self.boards[boardID] = board.board.getBoard(num=boardNum)

	def openbeacon(self):
		self.beacon = beacon.beacon(interface="sm0", source="W2RIT-11", destination="W2RIT")
		self.logger.log.debug("Opened beacon interface")

	def opencameramux(self):
		if self.gpio is not None:
			self.cameraMux = cameraMux.cameraMux(self.gpio)
			self.logger.log.debug("Opened camera mux interface")
			self.cameraMux.selectCamera(0)
		else:
			self.logger.log.error("Cannot open camera mux interface before GPIO")

	def opendaqcs(self):
		if self.spi is not None:
			self.daqcs = daqcsComms.daqcsComms(spi=self.spi, boards=self.boards)
			self.logger.log.debug("Opened daqcs interface")
		else:
			self.logger.log.error("Cannot open daqcs interface before SPI")

	def opengpio(self):
		self.gpio = gpio.gpio()
		self.logger.log.debug("Opened GPIO interface")

	def opengps(self):
		self.gps = gps.gps()
		self.logger.log.debug("Opened GPS")

	def openhabiposd(self):
		self.osd232 = osd232.osd232(port="/dev/ttyAMA0")
		self.logger.log.debug("Opened osd232")
		
		self.uart = self.osd232.connection
		self.logger.log.debug("Opened uart")

		if self.gpio is not None and self.cameraMux is not None:
			self.habip_osd = habip_osd.habip_osd(osd232=self.osd232, gpio=self.gpio, boards=self.boards, cameraMux=self.cameraMux)
			self.logger.log.debug("Opened osd232")
		else:
			self.logger.log.error("Must open GPIO and cameraMux interface before OSD")

	def openspi(self):
		self.spi = spi.spi()
		self.logger.log.debug("Opened SPI interface")

	def opentemperature(self):
		self.temperature = temp_pct2075.tempSensorPCT2075(address=0x48, busID=0)
		self.logger.log.debug("Opened temperature interface")

	def openpressure(self):
		self.pressure = press_ms5607.pressSensorMS5607(address=0x77, busID=0)
		self.logger.log.debug("Opened pressure interface")

	def openuart(self, port, baudrate):
		self.uart = uart.uart(port=port, baudrate=baudrate)
		if self.uart.open():
			self.logger.log.debug("Opened UART interface")
			return True
		else:
			self.logger.log.error("Could not open UART interface")
			return False

	def openwatchdog(self):
		if self.gpio is not None:
			self.watchdog = watchdog.watchdog(gpio=self.gpio)
		else:
			self.logger.log.error("Cannot open watchdog interface before GPIO")
