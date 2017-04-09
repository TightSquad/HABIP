#!/usr/bin/env python

"""
file: log_all_pihat_sensors.py
author: Chris Schwab
project: High Altitude Balloon Instrumentation Platform
description: Script to log all PiHat Sensors to csv
"""

# sudo apt-get install python-smbus
import smbus
import sys
import time
import logger
import csv

# Custom i2c sensor classes
from power_ina219 import powerMonitorINA219
from temp_pct2075 import tempSensorPCT2075
from press_ms5607 import pressSensorMS5607
from press_ms5803 import pressSensorMS5803
from humid_si7021 import humidSensorSI7021

# sensor addresses
power0_addr = 0x44		# INA219 power monitor
temp0_addr 	= 0x48		# PCT2075 right-side temp sensor
temp1_addr 	= 0x4A		# PCT2075 left side temp sensor
press0_addr = 0x77		# MS5607 altimeter (rectangle sensor)
press1_addr = 0x76		# MS5803 altimeter (round sensor)
humid0_addr = 0x40		# SI7021 humidity sensor

# i2c bus object
bus = smbus.SMBus(1)

# i2c logger object
i2c_logger = logger.logger("i2c_logger")

# create and initialize sensor objects
power0 	= powerMonitorINA219(power0_addr, None, bus, i2c_logger)
power0.config()
power0.calibrate()

temp0 	= tempSensorPCT2075(temp0_addr, None, bus, i2c_logger)

temp1 	= tempSensorPCT2075(temp1_addr, None, bus, i2c_logger)

press0 	= pressSensorMS5607(press0_addr, None, bus, i2c_logger)
press0.reset()
press0.readSensorPROM()

press1 	= pressSensorMS5803(press1_addr, None, bus, i2c_logger)
press1.reset()
press1.readSensorPROM()

humid0 	= humidSensorSI7021(humid0_addr, None, bus, i2c_logger)

# enable printing
printing_enabled = 0

# enable csv logging
logging_enabled = 1

# loop counter
loop_index = 0

# csv file name
logfile_name = "all_sensors_logged.csv"
logfile_header = ["Sample Index","Elapsed Time (s)","Shunt Voltage (mV)","Bus Voltage (V)","Current (mA)","Power (mW)", "Temp0 Temp (C)", "Temp0 Temp (F)", "Temp1 Temp (C)", "Temp1 Temp (F)", "Press0 Temp (C)", "Press0 Temp (F)", "Press0 Press (mBar)", "Press0 Press (Pa)", "Press0 Alt (m)", "Press0 Alt (ft)", "Press1 Temp (C)", "Press1 Temp (F)", "Press1 Press (mBar)", "Press1 Press (Pa)", "Press1 Alt (m)", "Press1 Alt (ft)", "Humid0 RH (%%)", "Humid0 Temp (C)", "Humid0 Temp (F)"]

if (logging_enabled):
	with open(logfile_name, 'w+') as f:
		writer = csv.writer(f)
		writer.writerow(logfile_header)

if (printing_enabled):
	print logfile_header

# starting relative time stamp
t_start = time.time()

while(1):
	power0_data = None
	temp0_data 	= None
	temp1_data 	= None
	press0_data = None
	press1_data = None
	humid0_data = None

	# get power0 sensor data
	while (power0.conversionNotValid()):
		if (printing_enabled):
			print "CONVERSION IS NOT VALID\n"
		time.sleep(0.01)
	power0_data = power0.readVIP()

	# get temp0 sensor data
	temp0_data = temp0.readTempCF()

	# get temp1 sensor data
	temp1_data = temp1.readTempCF()

	# get press0 sensor data
	press0_data = press0.readAll()

	# get press1 sensor data
	press1_data = press0.readAll()

	# get humid0 sensor data
	humid0_data = humid0.readHumidTemp()

	## NEED TO ADD

	# logging of 1-wire
	# logging of internal voltage / temp sensors in the BCM chip

	# write all data to log file or print results
	all_data = power0_data + temp0_data + temp1_data + press0_data + press1_data + humid0_data
	if (logging_enabled):
		with open(logfile_name, 'a+') as f:
			writer = csv.writer(f)
			writer.writerow([loop_index, (time.time() - t_start)] + all_data)
	if (printing_enabled):
		print [loop_index, (time.time() - t_start)] + all_data

	# delay between samples
	time.sleep(0.87)

	# increment loop counter
	loop_index = loop_index + 1

sys.exit(1)
