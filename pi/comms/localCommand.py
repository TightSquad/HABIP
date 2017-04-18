"""
author: Connor Goldberg
project: High Altitude Balloon Instrumentation Platform
description: Code for commands between pis and the msp
"""

class localCommand(object):
	"""
	Class for representing local platform commands
	"""

	commandIDTable = {
		"DATA" 		: "00",
		"ALLDATA" 	: "01",
		"RWPWR"		: "03",
		"RWCTL"		: "04",
		"RST"		: "05",
		"TIME"		: "06",

		"CUTDOWN" : "FF"
	}

	# static members
	startChar = '{'
	endChar = '}'
	seperator = ':'


	def __init__(self, logger, commandID=None, data=None, isAllData=False):

		self.logger = logger

		# String storing the original data
		self.fullString = None

		# The command ID number
		if isAllData:
			self.commandID = None
		elif type(commandID) is str:
			try:
				self.commandID = int(commandID,16)
			except Exception as e:
				self.logger.log.error("Could not convert commandID to int: {}".format(commandID))
				self.commandID = None
		elif type(commandID) is int:
			self.commandID = commandID
		else:
			self.logger.log.error("Invalid commandID type: {}".format(type(commandID)))
			self.commandID = None

		# The command data
		if type(data) is str:
			self.data = data.split(localCommand.seperator)
		elif type(data) is list:
			self.data = data
		elif data is None:
			self.data = []
		else:
			self.logger.log.error("Invalid data type: {}".format(type(data)))


	def __str__(self):
		if self.commandID is None:
			return "{}{}{}".format(self.startChar,
				localCommand.seperator.join(self.data) if self.data else '',
				localCommand.endChar)
		else:
			return "{}{:02X}{}{}".format(self.startChar, self.commandID,
				(localCommand.seperator + 
				localCommand.seperator.join(self.data) if self.data else ''),
				localCommand.endChar)


	@staticmethod
	def parseCommandFromString(commandString, logger):
		if not commandString.startswith(localCommand.startChar):
			logger.log.error("Command does not start with correct start char ({}): {}".format(localCommand.startChar), commandString)
			return None
		elif not commandString.endswith(localCommand.endChar):
			logger.log.error("Command does not end with correct end char ({}): {}".format(localCommand.endChar), commandString)
			return None
		else:
			fields = commandString.strip("{}{}".format(localCommand.startChar, localCommand.endChar)).split(localCommand.seperator)
			if len(fields) < 1:
				logger.log.error("Found empty command")
				return None
			else:
				try:
					commandID = int(fields[0], 16)
				except Exception as e:
					logger.log.error("Could not find valid command ID in command: {}".format(commandString))
					return None

				return localCommand(logger=logger, commandID=commandID, data=fields[1:])


	@staticmethod
	def parseDataFromString(dataString, logger):
		if not dataString.startswith(localCommand.startChar):
			logger.log.error("Data does not start with correct start char ({}): {}".format(localCommand.startChar), dataString)
			return None
		elif not dataString.endswith(localCommand.endChar):
			logger.log.error("Data does not end with correct end char ({}): {}".format(localCommand.endChar), dataString)
			return None
		else:
			fields = dataString.strip("{}{}".format(localCommand.startChar, localCommand.endChar)).split(localCommand.seperator)
			if len(fields) < 1:
				logger.log.error("Found empty data")
				return None
			else:
				return localCommand(logger=logger, data=fields[0:], isAllData=True)


	@staticmethod
	def timeCommand(logger, secondsString):
		return localCommand(logger=logger, commandID=localCommand.commandIDTable["TIME"], data=secondsString)

##### Testing
if __name__ == "__main__":
	t1 = localCommand(logger=None, commandID=0x10, data="test0")
	t2 = localCommand(logger=None, commandID="20", data=["test1"])
	t3 = localCommand(logger=None, commandID=0x30, data=["test2a","test2b"])
	t4 = localCommand(logger=None, commandID=None, data=["test3a","test3b", "test3c"], isAllData=True)

	print t1
	print localCommand.parseCommandFromString(str(t1), None)

	print t2
	print localCommand.parseCommandFromString(str(t2), None)

	print t3
	print localCommand.parseCommandFromString(str(t3), None)

	print t4
	print localCommand.parseDataFromString(str(t4), None)

