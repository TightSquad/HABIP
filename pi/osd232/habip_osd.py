"""
author: Matt Zachary 
project: High Altitude Balloon Instrumentation Platform
description: Uses the osd232 class to format our data
"""

import board
import common

class habip_osd(object):

	POWER_CONTROL_PIN = 32

	def __init__(self, osd232, gpio, boards):
		self.osd232 = osd232
		self.sleeptime = 100
		self.osd_width = 28
		self.osd_height = 11

		self.gpio = gpio # Used for controlling the power
		self.boards = boards # Used for getting sensor information

		# Make sure the power is on
		self.gpio.setPinMode(habip_osd.POWER_CONTROL_PIN, gpio.OUTPUT)
		self.gpio.setHigh(habip_osd.POWER_CONTROL_PIN)

		# Set default sensors
		self.humiditySensor = board.sensor(boardID="B0", sensorID="H")
		self.temperatureSensor = board.sensor(boardID="B5", sensorID="TB0")
		self.pressureSensor = board.sensor(boardID="B5", sensorID="P0")
		self.motorSpeed = board.sensor(boardID="B4", sensorID="MS")
		self.xGyro = board.sensor(boardID="B4", sensorID="XGY")
		self.yGyro = board.sensor(boardID="B4", sensorID="YGY")
		self.zGyro = board.sensor(boardID="B4", sensorID="ZGY")
		self.gpsLat = board.sensor(boardID="B5", sensorID="LAT")
		self.gpsLon = board.sensor(boardID="B5", sensorID="LON")
		self.callSign = "W2RIT-11"
		self.camera = 0

	def power_on(self):
		"""
		Ensure power to the OSD is on
		"""
		self.gpio.setHigh(habip_osd.POWER_CONTROL_PIN)


	def power_off(self):
		"""
		Ensure power to the OSD is off
		"""
		self.gpio.setLow(habip_osd.POWER_CONTROL_PIN)


	def update_all(self):
		# Temperature
		self.update_temp(data_source=str(self.temperatureSensor), 
			data_value=self.boards[self.temperatureSensor.boardID].data[self.temperatureSensor.sensorID])

		# Pressure
		self.update_pres(data_source=str(self.pressureSensor), 
			data_value=self.boards[self.pressureSensor.boardID].data[self.pressureSensor.sensorID])

		# Humidity
		self.update_humid(data_source=str(self.humiditySensor), 
			data_value=self.boards[self.humiditySensor.boardID].data[self.humiditySensor.sensorID])

		# Motor Speed
		self.update_speed(data_source=str(self.motorSpeed), 
			data_value=self.boards[self.motorSpeed.boardID].data[self.motorSpeed.sensorID])

		# IMU X,Y,Z
		self.update_accel(x=self.boards[self.xGyro.boardID].data[self.xGyro.sensorID],
			y=self.boards[self.yGyro.boardID].data[self.yGyro.sensorID],
			z=self.boards[self.zGyro.boardID].data[self.zGyro.sensorID])

		# Lat, Lon
		self.update_gps(lat=self.boards[self.gpsLat.boardID].data[self.gpsLat.sensorID],
			lon=self.boards[self.gpsLon.boardID].data[self.gpsLon.sensorID])

		# Call
		self.update_callsign(callsign=self.callSign)

		# Camera
		self.update_cam_num(cam_num=self.camera)

	def update_sensor(self, row_number, update_string):
		"""	
		Update a given OSD row, with a given string
	
		Input: row_number: row number to update (int, 1 through 11)
	   		   update_string: string to put in this row (string, 28 characters)
	   	"""
		self.osd232.setPosition(row=row_number)
		common.msleep(self.sleeptime)
		self.osd232.display(update_string)
		common.msleep(self.sleeptime)


	def update_temp(self, data_source, data_value):
		"""
		Update temperature row
	
		Input: data_source: the sensor we're pulling the data from (string)
		       data_value: the actual value (float)
	
		Spacing: source: 6, blank space: 17, data: 5
		"""
		row_number = 1

		# Truncate the input data
		data_source_formatted = str(data_source)
		data_value_formatted = str(data_value)[0:5].rjust(5)

		# Calculate number of spaces
		num_spaces = self.osd_width - len(data_source_formatted) - len(data_value_formatted)

		update_string = data_source_formatted + " "*num_spaces + data_value_formatted

		self.update_sensor(row_number, update_string[0:28])


	def update_pres(self, data_source, data_value):
		"""
		Update pressure row
		
		Input: data_source: the sensor we're pulling the data from (string)
		       data_value: the actual value (float)
		
		Spacing: source: 5, blank space: 17, data: 6
		"""
		row_number = 2

		# Truncate the input data
		data_source_formatted = str(data_source)
		data_value_formatted = str(data_value)[0:6].rjust(6)

		# Calculate number of spaces
		num_spaces = self.osd_width - len(data_source_formatted) - len(data_value_formatted)

		update_string = data_source_formatted + " "*num_spaces + data_value_formatted

		self.update_sensor(row_number, update_string[0:28])
		

	def update_humid(self, data_source, data_value):
		"""
		Update humidity row
		
		Input: data_source: the sensor we're pulling the data from (string)
		       data_value: the actual value (float)
		
		Spacing: source: 4, blank space: 20, data: 4
		"""
		row_number = 3

		# Truncate the input data
		data_source_formatted = str(data_source)
		data_value_formatted = str(data_value)[0:4].rjust(4)

		# Calculate number of spaces
		num_spaces = self.osd_width - len(data_source_formatted) - len(data_value_formatted)

		update_string = data_source_formatted + " "*num_spaces + data_value_formatted

		self.update_sensor(row_number, update_string[0:28])

	
	def update_speed(self, data_source, data_value):
		"""
		Update speed row
		
		Input: data_source: the sensor we're pulling the data from (string)
		       data_value: the actual value (float)
		
		Spacing: source: 2, blank space: 18, data: 8
		"""
		row_number = 4

		# Truncate the input data
		data_source_formatted = str(data_source)
		data_value_formatted = str(data_value)[0:8].rjust(8)

		# Calculate number of spaces
		num_spaces = self.osd_width - len(data_source_formatted) - len(data_value_formatted)

		update_string = data_source_formatted + " "*num_spaces + data_value_formatted

		self.update_sensor(row_number, update_string[0:28])


	def update_accel(self, x, y, z):
		"""
		Update acceleration rows (3 rows)
		
		Input: data_value: x,y,z acceleration, as floats
		
		Spacing: source: 1, blank space: 19, data: 8
		"""
		x_row_number = 5
		y_row_number = 6
		z_row_number = 7

		x_formatted = str(x)[0:8].rjust(8)
		y_formatted = str(y)[0:8].rjust(8)
		z_formatted = str(z)[0:8].rjust(8)

		x_update_string = "X" + " "*19 + x_formatted
		y_update_string = "Y" + " "*19 + y_formatted
		z_update_string = "Z" + " "*19 + z_formatted

		self.update_sensor(x_row_number, x_update_string)
		self.update_sensor(y_row_number, y_update_string)
		self.update_sensor(z_row_number, z_update_string)


	def update_gps(self, lat, lon):
		"""
		Update latitude/longitude row
		
		Input: lat, long: GPS position, as strings
		
		Spacing: source: 3, blank space: 16(lat), 15(lon), data: 9(lat), 10(lon)
		"""
		lat_row_number = 8
		lon_row_number = 9

		lat_formatted = str(lat)[0:9].rjust(9)
		lon_formatted = str(lon)[0:10].rjust(10)

		lat_update_string = "LAT" + " "*16 + lat_formatted
		lon_update_string = "LON" + " "*15 + lon_formatted

		self.update_sensor(lat_row_number, lat_update_string)
		self.update_sensor(lon_row_number, lon_update_string)


	def update_callsign (self, callsign):
		"""
		Update callsign
		
		Input: callsign as string
		
		Spacing: source: 4, blank space: 16, data: 8 (typ)
		"""
		row_number = 10
		data_source_formatted = "CALL"

		data_value_formatted = str(callsign)

		# Calculate number of spaces
		num_spaces = self.osd_width - len(data_source_formatted) - len(data_value_formatted)

		update_string = data_source_formatted + " "*num_spaces + data_value_formatted

		self.update_sensor(row_number, update_string[0:28])


	def update_cam_num(self, cam_num):
		"""
		Update Camera number
		
		Input: cam_num: the current active camera number (int, 0-3)
		
		Spacing: source: 3, blank space: 24, data: 1
		"""
		row_number = 11

		# Truncate the input data
		data_source_formatted = "CAM"
		data_value_formatted = str(cam_num)[0:1].rjust(1)

		# Calculate number of spaces
		num_spaces = self.osd_width - len(data_source_formatted) - len(data_value_formatted)

		update_string = data_source_formatted + " "*num_spaces + data_value_formatted

		self.update_sensor(row_number, update_string[0:28])

