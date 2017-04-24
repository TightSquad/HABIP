"""
author: Connor Goldberg
project: High Altitude Balloon Instrumentation Platform
description: Manages retrieving, storing, and logging sensor data
"""

import datetime
import subprocess

import localCommand
import logger

class dataManager(object):
	"""
	Manages the retrieving, storing, and logging sensor data
	"""

	def __init__(self, interfaces):
		self.logger = logger.logger("dataManager")
		self.interfaces = interfaces

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

