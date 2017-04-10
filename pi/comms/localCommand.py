"""
file: localCommand.py
author: Connor Goldberg
project: High Altitude Balloon Instrumentation Platform
description: Code for commands between pis and the msp
"""

class localCommand(object):
	"""
	Class for representing local platform commands
	"""

	startChar = '{'
	endChar = '}'
	seperator = ':'

	def __init__(self, logger, commandID=None, data=None):

		self.logger = logger

		# String storing the original data
		self.fullString = None

		# The command ID number
		if type(commandID) is str:
			try:
				self.commandID = int(commandID,16)
			except Exception as e:
				self.logger.log.error("Could not convert commandID to int: {}".format(commandID))
				self.commandID = None
		elif type(commandID) is int:
			self.commandID = commandID
		else:
			self.logger.log.error("Invalid commandID type: {}".format(type(commandID)))

		# The command data
		if type(data) is str:
			self.data = [data]
		elif type(data) is list:
			self.data = data
		elif data is None:
			self.data = []
		else:
			self.logger.log.error("Invalid data type: {}".format(type(data)))

	def __str__(self):
		return "{}{:02X}{}{}".format(self.startChar, self.commandID, localCommand.seperator + 
			localCommand.seperator.join(self.data) if self.data else '',localCommand.endChar)

#####
if __name__ == "__main__":
	print localCommand(logger=None, commandID=0x10, data="test0")
	print localCommand(logger=None, commandID="20", data=["test1"])
	print localCommand(logger=None, commandID=0x30, data=["test2a","test2b"])