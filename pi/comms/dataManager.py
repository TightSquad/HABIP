"""
author: Connor Goldberg
project: High Altitude Balloon Instrumentation Platform
description: Manages retrieving, storing, and logging sensor data
"""

import csv
import datetime
import os
import subprocess

import board
import localCommand
import logger

class dataManager(object):
	"""
	Manages the retrieving, storing, and logging sensor data
	"""

	LOG_BASE_DIR = "logs"
	LOG_FILE_NAME = "dataStorage.log"

	def __init__(self, interfaces):
		self.logger = logger.logger("dataManager")
		self.interfaces = interfaces
		self.shouldSyncTime = False

		self.sensorOrder = []
		self.initLog()


	def initLog(self):
		"""
		Initialize the log file and sensor order
		"""

		if not os.path.isdir(dataManager.LOG_BASE_DIR):
			try:
				os.mkdir(dataManager.LOG_BASE_DIR)
			except Exception as e:
				print "ERROR: {}".format(e)

		logFile = os.path.join(dataManager.LOG_BASE_DIR, dataManager.LOG_FILE_NAME)
		self.logFileHandle = open(logFile, "a")
		self.csvWriter = csv.writer(self.logFileHandle)

		for boardID in board.board.boardIDs:
			if boardID in self.interfaces.boards.keys():
				brd = self.interfaces.boards[boardID]
				for sensor in brd.sensors:
					self.sensorOrder.append((boardID, sensor))

		header = ["{}:{}".format(boardID,sensor) for boardID,sensor in self.sensorOrder]
		self.csvWriter.writerow(header)


	def log(self):
		"""
		Log all the data to the log
		"""

		data = []
		for boardID, sensor in self.sensorOrder:
			data.append(self.interfaces.boards[boardID].data[sensor])

		self.csvWriter.writerow(data)


	def update(self):
		"""
		Update all the data
		"""

		self.updateGps()
		self.updateComms()


	def updateGps(self):
		"""
		Update the gps data
		"""

		gpsData = self.interfaces.gps.get_data()
		
		if gpsData.lock is True:
			# Set the date and time right away
			date = datetime.datetime.combine(gpsData.date, gpsData.time)
			cmd = ["sudo", "date", "-s", "{}".format(date)]
			
			try:
				resp = subprocess.check_output(cmd)
				self.logger.log.debug("Set time to: {}".format(resp))
			except Exception as e:
				self.logger.log.warning("Could not set time from GPS: {}".format(e))

			seconds = (date - datetime.datetime(1970,1,1)).total_seconds()
			if seconds:
				try:
					seconds = int(seconds)
					self.interfaces.boards["B5"].data["TM"] = seconds

					if self.shouldSyncTime:
						self.shouldSyncTime = False
						timeCmd = localCommand.localCommand.timeCommand(logger=self.logger, secondsString=str(seconds))
						self.interfaces.daqcs.queue.append(timeCmd)

				except Exception as e:
					self.logger.log.warning("Could not convert time to seconds: {}".format(seconds))

			self.interfaces.boards["B5"].data["LAT"] = gpsData.lat
			self.interfaces.boards["B5"].data["LON"] = gpsData.lon
			self.interfaces.boards["B5"].data["SPD"] = gpsData.speed
			self.interfaces.boards["B5"].data["ALT"] = gpsData.alt


	def setTimeSync(self):
		"""
		Sets the option to sync the time next time the GPS is updated
		"""

		self.shouldSyncTime = True


	def updateComms(self):
		"""
		Update the sensors on the Comms board
		"""

		# Temp sensor
		self.interfaces.temperature.readTempCF()
		self.interfaces.boards["B5"].data["TB0"] = self.interfaces.temperature.prev_temp_c

		# Pressure sensor
		self.interfaces.pressure.readAll()
		self.interfaces.boards["B5"].data["P0"] = self.interfaces.pressure.prev_press_mbar

		# Die temp
		try:
			dieTemp = subprocess.check_output(["vcgencmd","measure_temp"])
		except Exception as e:
			self.logger.log.warning("Could not read die temp: {}".format(e))
			return

		dieTemp = dieTemp.strip().split("=")
		if len(dieTemp) == 2 and dieTemp[1].endswith("'C"):
			dieTemp = dieTemp[1].strip("'C")
			try:
				dieTemp = float(dieTemp)
				self.interfaces.boards["B5"].data["TD0"]
			except Exception as e:
				self.logger.log.warning("Could not convert die temp to float: {}".format(dieTemp))

