"""
author: Connor Goldberg
project: High Altitude Balloon Instrumentation Platform
description: Manages the daqcs communicaions
"""

import logger
import localCommand

class daqcsComms(self):
	"""
	Class for managing the daqcs communications
	"""

	daqcsStates = {
		"L" : 0x0, # Listening
		"C" : 0x1, # Capturing
		"O" : 0x2, # Obtaining data
		"U"	: 0x3, # Unknown
	}

	state = {
		"REQ"	: 0x0, 	# Request data
		"READ"	: 0x1, 	# Read data
		"EXE"	: 0x2,	# Execute command from the queue
	}

	def __init__(self, spi):
		self.logger = logger.logger("daqcsComms")
		self.spi = spi

		self.daqcsState = daqcsComms.daqcsStates["U"]
		self.currentState = daqcsComms.state["REQ"]

		self.queue = []


	def update(self):
		"""
		Process the state machine
		"""

		# First get the state of daqcs
		resp = self.checkState()

		if self.currentState = daqcsComms.state["REQ"]:
			# Request data from daqcs
			lc = localCommand.localCommand(logger=self.logger, commandID=01)

		elif self.currentState = daqcsComms.state["READ"]:
			pass

		elif self.currentState = daqcsComms.state["EXE"]:
			pass


	def readString(self, maxCharsSent=1500, validOverride=False):
		"""
		Read a string from the SPI interface by sending bytes one at a time
		and reading back the responses. Only do this while the number of bytes
		sent is less than the maxCharsSent parameter

		Can pass in valid in case we were checking the state and got some data
		"""

		response = []

		if validOverride:
			response.append(localCommand.localCommand.startChar)

		valid = validOverride
		charsSent = 0
		run = True

		while run and (valid or (charsSent < maxCharsSent)):
			char = chr(self.spi.readByte())
			charsSent += 1

			if char == '{':
				valid = True
			elif char == '}':
				run = False

			if valid:
				response.append(char)

		string = "".join(response)
		self.logger.log.debug("received string: {}".format(string))
		return string


	def checkState(self, maxTries = 10):
		tries = 0
		success = False
		while tries < maxTries:
			tries += 1
			resp = self.spi.readChar()
			if resp in daqcsComms.daqcsStates.keys():
				success = True
				self.state = daqcsComms.daqcsStates[resp]
				return True
			elif resp == localCommand.localCommand.startChar:
				resp = self.readString(validOverride=True)
				return resp


