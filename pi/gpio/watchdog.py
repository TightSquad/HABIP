"""
author: Connor Goldberg
project: High Altitude Balloon Instrumentation Platform
description: Controls the Watchdog
"""

import common
import logger

class watchdog(object):

	def __init__(self, gpio, pin=31, activeLow=False):
		self.logger = logger.logger("watchdog")
		self.gpio = gpio
		self.pin = 31
		self.holdTime = 50 # Default time to hold the GPIO pin active
		self.activeLow = activeLow

		# Setup the GPIO pin
		self.gpio.setPinMode(self.pin, gpio.OUTPUT)

		self.unset()


	def pet(self, withHoldTime=None):
		"""
		Pets the watchdog timer by pulsing the GPIO pin for the number of
		milliseconds specified by self.holdTime or withHoldTime (if present)
		"""

		self.set()

		if withHoldTime is not None:
			common.msleep(withHoldTime)
		elif self.holdTime is not None:
			common.msleep(self.holdTime)

		self.unset()

		self.logger.log.info("Toggled watchdog timer")


	def set(self):
		"""
		Sets the pin to its active state
		"""

		if self.activeLow is True:
			self.gpio.setLow(self.pin)
		else:
			self.gpio.setHigh(self.pin)

		self.logger.log.debug("Set watchdog pin to active")


	def unset(self):
		"""
		Sets the pin to its inactive state
		"""

		if self.activeLow is True:
			self.gpio.setHigh(self.pin)
		else:
			self.gpio.setLow(self.pin)

		self.logger.log.debug("Set watchdog pin to inactive")
