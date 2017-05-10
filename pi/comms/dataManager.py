"""
author: Connor Goldberg
project: High Altitude Balloon Instrumentation Platform
description: Manages retrieving, storing, and logging sensor data
"""

import csv
import datetime
import os
import subprocess
import sys

import board
import common
import localCommand
import logger

class dataManager(object):
	"""
	Manages the retrieving, storing, and logging sensor data
	"""

	LOG_BASE_DIR = "logs"
	LOG_FILE_NAME = "dataStorage.csv"

	def __init__(self, interfaces):
		self.logger = logger.logger("dataManager")
		self.logger.log.info("Started dataManager")
		self.interfaces = interfaces
		self.shouldSyncTime = False

		self.sensorOrder = []
		self.csvWriter = None
		self.initLog()

		# Number of times to start soundmodem
		self.soundmodemAttempts = 0


	def checkSoundmodem(self):
		"""
		Checks to see if soundmodem is running, and restarts it if not
		"""

		if self.soundmodemAttempts > 10:
			# Fatal error, quit out
			self.logger.log.fatal("Could not start soundmodem after {} attempts".format(self.soundmodemAttempts))
			sys.exit(1)

		if not common.processIsRunning("soundmodem"):
			self.soundmodemAttempts += 1
			cmd = ["sudo", "/home/pi/scripts/startsoundmodem.sh"]
			try:
				subprocess.Popen(cmd)
				self.logger.log.debug("Called: $ {}".format(" ".join(cmd)))
			except Exception as e:
				self.logger.log.error("Got exception in soundmodem: {} with output: {}".format(e, e.output))
		else:
			self.soundmodemAttempts = 0


	def initLog(self):
		"""
		Initialize the log file and sensor order
		"""

		if not os.path.isdir(dataManager.LOG_BASE_DIR):
			try:
				os.mkdir(dataManager.LOG_BASE_DIR)
			except Exception as e:
				self.logger.log.warning("Could not make directory: {}".format(e))
				return

		logFile = os.path.join(dataManager.LOG_BASE_DIR, dataManager.LOG_FILE_NAME)
		self.logFileHandle = open(logFile, "a")
		self.csvWriter = csv.writer(self.logFileHandle)
		self.logger.log.info("Initialized data logger: {}".format(logFile))

		for boardID in board.board.boardIDs:
			if boardID in self.interfaces.boards.keys():
				brd = self.interfaces.boards[boardID]
				for sensor in brd.sensors:
					self.sensorOrder.append((boardID, sensor))

		header = ["{}:{}".format(boardID,sensor) for boardID,sensor in self.sensorOrder]
		try:
			self.csvWriter.writerow(header)
			self.logger.log.info("Wrote csv header")
		except Exception as e:
			self.logger.log.warning("Could not write csv header: {}".format(e))


	def genFakeData(self):
		fakeData = 0.0

		for boardID, sensor in self.sensorOrder:
			data = self.interfaces.boards[boardID].data[sensor]
			if data is None and boardID != "B5":
				self.interfaces.boards[boardID].data[sensor] = fakeData
				fakeData += 1.0


	def getTelemetryStream(self):
		"""
		Get the string to send all the sensor data
		"""

		allData = []
		for boardID, sensor in self.sensorOrder:
			data = self.interfaces.boards[boardID].data[sensor]
			if data is not None:
				allData.append("{}:{}:{}".format(boardID, sensor, data))

		return allData


	def log(self):
		"""
		Log all the data to the log
		"""

		if self.csvWriter:
			data = []
			for boardID, sensor in self.sensorOrder:
				data.append(self.interfaces.boards[boardID].data[sensor])

			try:
				self.csvWriter.writerow(data)
				self.logger.log.debug("Logging sensor data to csv")
			except Exception as e:
				self.logger.log.warning("Could not log sensor data: {}".format(e))


	def setTimeSync(self):
		"""
		Sets the option to sync the time next time the GPS is updated
		"""

		self.shouldSyncTime = True


	def update(self):
		"""
		Update all the data
		"""

		self.updateGps()
		self.updateComms()
		self.checkSoundmodem()


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


	def updateComms(self):
		"""
		Update the sensors on the Comms board
		"""

		# Temp sensor
		self.interfaces.temperature.readTempCF()
		self.interfaces.boards["B5"].data["TB0"] = self.interfaces.temperature.prev_temp_c

		# # Balloon Temp sensor
		# self.interfaces.balloonTemperature.readTempCF()
		# self.interfaces.boards["B5"].data["TBL"] = self.interfaces.balloonTemperature.prev_temp_c

		# Pressure sensor
		self.interfaces.pressure.readAll()
		self.interfaces.boards["B5"].data["P0"] = self.interfaces.pressure.prev_press_mbar

		# # Balloon Pressure sensor
		# self.interfaces.balloonPressure.readAll()
		# self.interfaces.boards["B5"].data["PBL"] = self.interfaces.balloonPressure.prev_press_mbar

		# Die temp
		try:
			dieTemp = subprocess.check_output(["vcgencmd", "measure_temp"])
		except Exception as e:
			self.logger.log.warning("Could not read die temp: {}".format(e))
			return

		dieTemp = dieTemp.strip().split("=")
		if len(dieTemp) == 2 and dieTemp[1].endswith("'C"):
			dieTemp = dieTemp[1].strip("'C")
			try:
				dieTemp = float(dieTemp)
				self.interfaces.boards["B5"].data["TD0"] = dieTemp
			except Exception as e:
				self.logger.log.warning("Could not convert die temp to float: {}".format(dieTemp))

