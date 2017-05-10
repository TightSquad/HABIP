"""
author: Connor Goldberg
project: High Altitude Balloon Instrumentation Platform
description: Default GPIO setup and helper functions
"""

import sys
import RPi.GPIO as GPIO

import common
import logger


class gpio(object):
	GPIO = GPIO # module

	OUTPUT = GPIO.OUT
	OUT = GPIO.OUT
	INPUT = GPIO.IN
	IN = GPIO.IN
	LOW = 0
	HIGH = 1

	lookupModeToString = {
		GPIO.IN : "GPIO.IN",
		GPIO.OUT : "GPIO.OUT",
		GPIO.SPI : "GPIO.SPI",
		GPIO.I2C : "GPIO.I2C",
		GPIO.HARD_PWM : "GPIO.HARD_PWM",
		GPIO.SERIAL : "GPIO.SERIAL",
		GPIO.UNKNOWN : "GPIO.UNKNOWN"
	}

	def __init__(self):
		self.logger = logger.logger("gpio")
		GPIO.setwarnings(False)
		GPIO.setmode(GPIO.BOARD)

	def getMode(self, pin):
		return lookupModeToString[GPIO.gpio_function(pin)]

	def read(self, pin):
		return GPIO.input(pin)

	def setPinMode(self, pin, mode):
		self.logger.log.debug("Set pin {} to {}".format(
			pin, gpio.lookupModeToString[mode]))
		GPIO.setup(pin, mode)

	def setHigh(self, pin):
		self.logger.log.debug("Setting pin {} to HIGH".format(pin))
		GPIO.output(pin, 1)

	def setLow(self, pin):
		self.logger.log.debug("Setting pin {} to LOW".format(pin))
		GPIO.output(pin, 0)

	def setOutput(self, pin, state):
		self.logger.log.debug("Setting pin {} to {}".format(pin, state))
		GPIO.output(pin, state)

	def toggleOutput(self, pin):
		self.logger.log.debug("Toggling pin {}".format(pin))
		GPIO.output(pin, not GPIO.input(pin))

	def status(self, *pins):
		displayString = "{:<2} : {}"
		if not pins:
			pins = range(1,41)

		for pin in pins:
			try:
				print displayString.format(pin, getMode(pin))
			except ValueError:
				print displayString.format(pin, "Error")

# Testing
if __name__ == "__main__":
	intf = gpio()
	intf.status()

