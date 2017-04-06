"""
author: Connor Goldberg
project: High Altitude Balloon Instrumentation Platform
description: Default logger settings and helper functions
"""

import common
import logging
import time


class logger(object):

	DEFAULT_FMT = "%(asctime)s.%(msecs)d : %(name)s : %(levelname)s : %(message)s"
	DEFAULT_DATEFMT = "%Y-%m-%d_%H:%M:%S"
	DEFAULT_FILENAME_FORMAT = "{logFileName}_%Y-%m-%d.log"

	def __init__(self, loggerName, logFileName=None, logFormat=None,
			dateFormat=None, logFileHandler=None, baseLogger=True,
			logErrorToConsole=True):
		self.loggerName = loggerName
		self.logFileName = None
		self.logFormat = None
		self.dateFormat = None
		self.logFileHandler = None
		self.log = None
		self.logErrorToConsole = logErrorToConsole

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
		ch = logging.StreamHandler()
		ch.setLevel(logging.ERROR)
		ch.setFormatter(formatter)

		# File Handler
		if self.logFileHandler is None:
			fh = logging.FileHandler(filename=self.logFileName)
			fh.setLevel(logging.DEBUG)
			fh.setFormatter(formatter)
		else:
			fh = self.logFileHandler

		# Add the handles to the logger
		logger.addHandler(ch)
		logger.addHandler(fh)

		return logger


	def getLogger(self, name):
		newName = "{}.{}".format(self.loggerName, name)
		c = logger(newName, logFileName=self.logFileName,
			logFormat=self.logFormat, dateFormat=self.dateFormat,
			logFileHandler=self.logFileHandler, baseLogger=False,
			logErrorToConsole=self.logErrorToConsole)
		return c

# Testing
if __name__ == "__main__":

	myLogger = logger("myLogger")

	# Test Code
	myLogger.log.debug("debug message!")
	myLogger.log.error("error message!")
	myLogger.log.warning("warning message!")
