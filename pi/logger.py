"""
file: logger.py
author: Connor Goldberg
project: High Altitude Balloon Instrumentation Platform
description: Default logger settings
"""

import logging
import time

DEFAULT_FMT = "%(asctime)s.%(msecs)d : %(name)s : %(levelname)s : %(message)s"
DEFAULT_DATEFMT = "%Y-%m-%d_%H:%M:%S"

class logger(object):

	def __init__(self, loggerName, logFileName=None, logFormat=None, dateFormat=None, logFileHandler=None):
		self.loggerName = loggerName
		self.logFileName = None
		self.logFormat = None
		self.dateFormat = None
		self.logFileHandler = None

		if logFileName is not None:
			self.logFileName = logFileName
		else:
			self.logFileName = "{}.log".format(loggerName)

		if logFormat is not None:
			self.logFormat = logFormat
		else:
			self.logFormat = DEFAULT_FMT

		if dateFormat is not None:
			self.dateFormat = dateFormat
		else:
			self.dateFormat = DEFAULT_DATEFMT

		if logFileHandler is not None:
			self.logFileHandler = logFileHandler

		self.log = self.__create__()


	def __create__(self):
		# Create the logger
		logger = logging.getLogger(self.loggerName)
		logger.setLevel(logging.DEBUG)

		# Create the formatter
		formatter = logging.Formatter(fmt=self.logFormat, datefmt=self.dateFormat)
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


# Testing
if __name__ == "__main__":
	# logger = logging.getLogger("loggerName")
	# logger.setLevel(logging.DEBUG)

	# # Set format
	# formatter = logging.Formatter(fmt="%(asctime)s.%(msecs)d : %(name)s : %(levelname)s : %(message)s", datefmt="%Y-%m-%d_%H:%M:%S")
	# formatter.converter = time.gmtime

	# # Console Handler
	# ch = logging.StreamHandler()
	# ch.setLevel(logging.ERROR)
	# ch.setFormatter(formatter)

	# # File Handler
	# fh = logging.FileHandler(filename="testLog.log")
	# fh.setLevel(logging.DEBUG)
	# fh.setFormatter(formatter)	

	# # Add the handles to the logger
	# logger.addHandler(ch)
	# logger.addHandler(fh)

	myLogger = logger("myLogger")

	# Test Code
	myLogger.log.debug("debug message!")
	myLogger.log.error("error message!")
	myLogger.log.warning("warning message!")
