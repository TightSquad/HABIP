"""
author: Connor Goldberg
project: High Altitude Balloon Instrumentation Platform
description: Manages the daqcs communicaions
"""

import board
import logger
import localCommand

class daqcsComms(object):
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

	def __init__(self, spi, boards):
		self.logger = logger.logger("daqcsComms")
		self.spi = spi
		self.boards = boards

		self.daqcsState = daqcsComms.daqcsStates["U"]
		self.currentState = daqcsComms.state["REQ"]

		self.queue = []

		self.logger.log.info("Started daqcsComms")

	def queueCommand(self, command):
		self.queue.insert(0, command)

	def update(self):
		"""
		Process the state machine
		"""

		# First get the state of daqcs
		resp = self.checkState()
		
		if resp is False:
			self.logger.log.warning("Did not get response from daqcs when checking state")
			return
		elif type(resp) is str:
			self.logger.log.warning("Got data to parse unexpectedly")
			self.parseData(resp)
			self.currentState = daqcsComms.state["EXE"]
			return

		if self.currentState == daqcsComms.state["REQ"]:
			self.logger.log.debug("Entered REQ state")
			# Request data from daqcs

			self.currentState = daqcsComms.state["READ"]
			if self.daqcsState != daqcsComms.daqcsStates["L"]:
				self.logger.log.warning("DAQCS not listening")
				return
			else:
				self.logger.log.debug("Sending get all data command to DAQCS")
				lc = localCommand.localCommand(logger=self.logger, commandID=01)
				self.spi.sendString(str(lc))

		elif self.currentState == daqcsComms.state["READ"]:
			self.logger.log.debug("Entered READ state")
			self.currentState = daqcsComms.state["EXE"]
			
			resp = self.readString()
			if resp:
				self.logger.log.debug("Got data to parse from DAQCS")
				self.parseData(resp)
			else:
				self.logger.log.debug("Did not get any data from READ")

		elif self.currentState == daqcsComms.state["EXE"]:
			self.logger.log.debug("Entered EXE state")
			self.currentState = daqcsComms.state["REQ"]
			
			if self.queue:
				command = self.queue.pop()
				self.logger.log.debug("About to send command: {}".format(command))
				self.spi.sendString(str(command))
			else:
				self.logger.log.debug("Queue empty")

	def checkState(self, maxTries = 10):
		"""
		Check the state of daqcs
		"""

		tries = 0
		success = False
		while tries < maxTries:
			tries += 1
			resp = self.spi.readChar()
			if resp in daqcsComms.daqcsStates.keys():
				success = True
				self.daqcsState = daqcsComms.daqcsStates[resp]
				return True
			elif resp == localCommand.localCommand.startChar:
				resp = self.readString(validOverride=True)
				return resp

		return False


	def readString(self, maxCharsSent=2000, validOverride=False):
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


	def parseData(self, dataString):
		"""
		Parse sensor data from daqcs
		"""

		dataString = dataString.strip("{}")
		items = dataString.split(";")
		for item in items:
			pieces = item.split(":")
			if len(pieces) != 3:
				self.logger.log.warning("Could not parse data: {}".format(item))
				continue
			else:
				if pieces[0] in board.board.num.keys():
					if pieces[1] in self.boards[pieces[0]].sensors():
						try:
							val = float(pieces[3])
							self.boards[pieces[0]].data[pieces[1]] = val
						except Exception as e:
							self.logger.log.warning("Could not convert value {} in {}".format(pieces[2], item))
					else:
						self.logger.log.warning("Could not find sensor {} in {}".format(pieces[1], item))
				else:
					self.logger.log.warning("Could not find board {} in {}".format(pieces[0], item))
