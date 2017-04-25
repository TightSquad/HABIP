"""
author: Connor Goldberg
project: High Altitude Balloon Instrumentation Platform
description: Default logger settings and helper functions
"""

import logging
import time
import os


class logger(object):
	DEBUG = logging.DEBUG
	INFO = logging.INFO
	ERROR = logging.ERROR
	WARNING = logging.WARNING

	DEFAULT_FMT = "%(asctime)s.%(msecs)d : %(name)s : %(levelname)s : %(message)s"
	DEFAULT_DATEFMT = "%Y-%m-%d_%H:%M:%S"
	DEFAULT_FILENAME_FORMAT = "{logFileName}_%Y-%m-%d.log"

	def __init__(self, loggerName, logFileName=None, logFormat=None,
			dateFormat=None, logFileHandler=None, baseLogger=True,
			logErrorToConsole=True, useLogsDirectory=True, fileLevel=logging.DEBUG):
		self.loggerName = loggerName
		self.logFileName = None
		self.logFormat = None
		self.dateFormat = None
		self.logFileHandler = None
		self.log = None
		self.logErrorToConsole = logErrorToConsole
		self.useLogsDirectory = useLogsDirectory
		self.logDirectory = "logs"
		self.fileLevel = fileLevel

		self.consoleHandler = None
		self.fileHandler = None

		if logFileName is not None:
			self.logFileName = logFileName
		else:
			self.logFileName = time.strftime(logger.DEFAULT_FILENAME_FORMAT.format(logFileName=loggerName))

		if logFormat is not None:
			self.logFormat = logFormat
		else:
			self.logFormat = logger.DEFAULT_FMT

		if dateFormat is not None:
			self.dateFormat = dateFormat
		else:
			self.dateFormat = logger.DEFAULT_DATEFMT

		if logFileHandler is not None:
			self.logFileHandler = logFileHandler

		if baseLogger:
			self.log = self.__create__()
		else:
			self.log = logging.getLogger(self.loggerName)


	def __create__(self):
		# Create the logger
		logger = logging.getLogger(self.loggerName)
		logger.setLevel(logging.DEBUG)

		# Create the formatter
		formatter = logging.Formatter(fmt=self.logFormat,
			datefmt=self.dateFormat)
		formatter.converter = time.gmtime # set time to UTC

		# Create the console handler
		self.consoleHandler = logging.StreamHandler()
		self.consoleHandler.setLevel(logging.ERROR)
		self.consoleHandler.setFormatter(formatter)

		# Create logs directory
		if self.useLogsDirectory:
			if not os.path.isdir(self.logDirectory):
				try:
					os.mkdir(self.logDirectory)
				except Exception as e:
					print "ERROR: {}".format(e)
					
			self.logFileName = os.path.join(self.logDirectory, self.logFileName)

		# File Handler
		if self.logFileHandler is None:
			self.fileHandler = logging.FileHandler(filename=self.logFileName)
			self.fileHandler.setLevel(self.fileLevel)
			self.fileHandler.setFormatter(formatter)
		else:
			self.fileHandler = self.logFileHandler

		# Add the handles to the logger
		if self.logErrorToConsole:
			logger.addHandler(self.consoleHandler)

		logger.addHandler(self.fileHandler)

		return logger

	def changeLevel(self, level):
		"""
		Removes, changes the level of the file handler, then adds it back
		"""
		self.log.removeHandler(self.fileHandler)

		self.fileLevel = level
		self.fileHandler.setLevel(self.fileLevel)
		self.log.addHandler(self.fileHandler)


	def getLogger(self, name):
		newName = "{}.{}".format(self.loggerName, name)
		c = logger(newName, logFileName=self.logFileName,
			logFormat=self.logFormat, dateFormat=self.dateFormat,
			logFileHandler=self.logFileHandler, baseLogger=False,
			logErrorToConsole=self.logErrorToConsole,
			useLogsDirectory=self.useLogsDirectory)
		return c

# Testing
if __name__ == "__main__":

	myLogger = logger("myLogger")

	# Test Code
	myLogger.log.debug("debug message 1")
	myLogger.log.info("info message 1")
	myLogger.log.warning("warning message 1")
	myLogger.log.error("error message 1")

	myLogger.changeLevel(logger.INFO)

	myLogger.log.debug("debug message 2") # This won't get logged
	myLogger.log.info("info message 2")
	myLogger.log.warning("warning message 2")
	myLogger.log.error("error message 2")
