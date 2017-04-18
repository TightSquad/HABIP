"""
author: Connor Goldberg, Matt Zachary
project: High Altitude Balloon Instrumentation Platform
description: Camera Mux Control
"""

import logger

class cameraMux(object):

	def __init__(self, gpio):
		"""
		Set up the camera mux gpio outputs. Needs the gpio class handle
		"""

		self.logger = logger.logger("cameraMux")

		self.gpio = gpio

		for pin in [11, 13, 15, 16, 36, 38, 40]:
			self.gpio.setPinMode(pin, self.gpio.GPIO.OUT)
			self.gpio.setLow(pin)


		self.logger.log.info("Opened camera mux interface")

	def selectCamera(self, index):
		if index in range(0,4):
			if index == 0:
				self.gpio.setOutput(38,0)
				self.gpio.setOutput(40,0)
				self.gpio.setOutput(11,1)
			elif index == 1:
				self.gpio.setOutput(38,1)
				self.gpio.setOutput(40,0)
				self.gpio.setOutput(13,1)
			elif index == 2:
				self.gpio.setOutput(38,0)
				self.gpio.setOutput(40,1)
				self.gpio.setOutput(15,1)
			elif index == 3:
				self.gpio.setOutput(38,1)
				self.gpio.setOutput(40,1)
				self.gpio.setOutput(16,1)

			self.logger.log.info("Changed camera mux to index: {}".format(index))
		else:
			self.logger.log.error("Selected camera mux index out of range: {}".format(index))
