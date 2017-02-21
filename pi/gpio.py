"""
author: Connor Goldberg
project: High Altitude Balloon Instrumentation Platform
description: Default GPIO setup and helper functions
"""

import sys
sys.path.append("..")

import common
import logger

import RPi.GPIO as GPIO

lookupModeToString = {
	GPIO.IN : "GPIO.IN",
	GPIO.OUT : "GPIO.OUT",
	GPIO.SPI : "GPIO.SPI",
	GPIO.I2C : "GPIO.I2C",
	GPIO.HARD_PWM : "GPIO.HARD_PWM",
	GPIO.SERIAL : "GPIO.SERIAL",
	GPIO.UNKNOWN : "GPIO.UNKNOWN"
}

def initialize():
	GPIO.setmode(GPIO.BOARD)

def getMode(pin):
	return lookupModeToString[GPIO.gpio_function(pin)]

def status(*pins):
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
	setup()
	status()

