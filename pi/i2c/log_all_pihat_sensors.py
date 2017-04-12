#!/usr/bin/env python

"""
file: log_all_pihat_sensors.py
author: Chris Schwab
project: High Altitude Balloon Instrumentation Platform
description: Script to log all I2C/1-wire/internalARM PiHat sensors to csv as well as "pet" the hardware WDT
"""

###########################
# Imports
###########################
# sudo apt-get install python-smbus
import smbus
import sys
import time
import logger
import csv
import subprocess
import os
import RPi.GPIO as GPIO

# Custom i2c sensor classes
from power_ina219 import powerMonitorINA219
from temp_pct2075 import tempSensorPCT2075
from press_ms5607 import pressSensorMS5607
from press_ms5803 import pressSensorMS5803
from humid_si7021 import humidSensorSI7021

# Custom 1-wire sensor class


###########################
# LOGGING / PRINTING CONFIG
###########################
# enable printing to terminal
printing_enabled = 0
# enable csv logging
logging_enabled = 1

###########################
# Sensor Addresses
###########################
# i2c sensors
power0_addr = 0x44		# INA219 power monitor
temp0_addr 	= 0x48		# PCT2075 right-side temp sensor
temp1_addr 	= 0x4A		# PCT2075 left side temp sensor
press0_addr = 0x77		# MS5607 altimeter (rectangle sensor)
press1_addr = 0x76		# MS5803 altimeter (round sensor)
humid0_addr = 0x40		# SI7021 humidity sensor

# 1-wire sensors

###########################
# GPIO Pins
###########################
# GPIO pin numbers
dbg_led0 	= 20
wdt_pet 	= 21

# set GPIO pin numbering to match the RasPi board header
GPIO.setmode(GPIO.BCM)

# set GPIOs as outputs
GPIO.setwarnings(False)
GPIO.setup(dbg_led0, GPIO.OUT)
GPIO.setup(wdt_pet, GPIO.OUT)

###########################
# Log File Naming
###########################
# NOTE: Use absolute paths since this script will be run from /etc/rc.local on boot!

# i2c_bus_log
# 	check for already used log names (aka if the RasPi had been previously booted or crashed --> i2c_bus_logger_XXXXX.log)
# 	start log index at 0
log_file_index = 0
i2c_log_file_base = "i2c_bus_logger"
i2c_log_base_path = "/home/pi/habip/sensors_logs/"
log_files_found = False
# check for all i2c_log_file_base files and increment the index to the next unique number
for file in os.listdir(i2c_log_base_path):
	if (file.startswith(i2c_log_file_base) and file.endswith('.log')):
		log_files_found = True
		number_in_use = int(file[-8:][0:4])
		if (number_in_use > log_file_index):
			log_file_index = number_in_use
if (log_files_found):
	log_file_index = log_file_index + 1
# pad index to 5 places
log_file_index = "{:05d}".format(log_file_index)
print "Log file index set to: {}".format(log_file_index)

# csv data logs
# 	use the unique log_file_index from the i2c_log_file search
csv_logfile_name 	= "all_sensors_logged_{}.csv".format(log_file_index)
csv_logfile_header 	= ["Sample Index", "Elapsed Time (s)", "Epoch Time (s)", "Power0 Shunt Voltage (mV)", "Power0 Bus Voltage (V)", "Power0 Current (mA)", "Power0 Power (mW)", "Temp0 Temp (C)", "Temp0 Temp (F)", "Temp1 Temp (C)", "Temp1 Temp (F)", "Press0 Temp (C)", "Press0 Temp (F)", "Press0 Press (mBar)", "Press0 Press (Pa)", "Press0 Alt (m)", "Press0 Alt (ft)", "Press1 Temp (C)", "Press1 Temp (F)", "Press1 Press (mBar)", "Press1 Press (Pa)", "Press1 Alt (m)", "Press1 Alt (ft)", "Humid0 RH (%%)", "Humid0 Temp (C)", "Humid0 Temp (F)", "ARM0 Core Temp (C)", "ARM0 Core Temp (F)", "ARM0 Core Voltage (V)", "ARM0 SDRAM_c Voltage (V)", "ARM0 SDRAM_i Voltage (V)", "ARM0 SDRAM_p Voltage (V)"]
csv_log_base_path 	= "/home/pi/habip/sensors_logs/"

# 	sensor headers and sensor log file names
sample_time_header 	= ["Sample Index", "Elapsed Time (s)", "Epoch Time (s)"]
power0_header 		= ["Power0 Shunt Voltage (mV)", "Power0 Bus Voltage (V)", "Power0 Current (mA)", "Power0 Power (mW)"]
power0_logfile_name = "power0_sensor_logged_{}.csv".format(log_file_index)
temp0_header 		= ["Temp0 Temp (C)", "Temp0 Temp (F)"]
temp0_logfile_name 	= "temp0_sensor_logged_{}.csv".format(log_file_index)
temp1_header 		= ["Temp1 Temp (C)", "Temp1 Temp (F)"]
temp1_logfile_name 	= "temp1_sensor_logged_{}.csv".format(log_file_index)
press0_header 		= ["Press0 Temp (C)", "Press0 Temp (F)", "Press0 Press (mBar)", "Press0 Press (Pa)", "Press0 Alt (m)", "Press0 Alt (ft)"]
press0_logfile_name = "press0_sensor_logged_{}.csv".format(log_file_index)
press1_header 		= ["Press1 Temp (C)", "Press1 Temp (F)", "Press1 Press (mBar)", "Press1 Press (Pa)", "Press1 Alt (m)", "Press1 Alt (ft)"]
press1_logfile_name = "press1_sensor_logged_{}.csv".format(log_file_index)
humid0_header 		= ["Humid0 RH (%%)", "Humid0 Temp (C)", "Humid0 Temp (F)"]
humid0_logfile_name = "humid0_sensor_logged_{}.csv".format(log_file_index)
arm0_header 		= ["ARM0 Core Temp (C)", "ARM0 Core Temp (F)", "ARM0 Core Voltage (V)", "ARM0 SDRAM_c Voltage (V)", "ARM0 SDRAM_i Voltage (V)", "ARM0 SDRAM_p Voltage (V)"]
arm0_logfile_name 	= "arm0_sensor_logged_{}.csv".format(log_file_index)

# 	create log files
if (logging_enabled):
	# all sensors
	with open(csv_log_base_path + csv_logfile_name, 'w+') as f:
		writer = csv.writer(f)
		writer.writerow(csv_logfile_header)
	# power0
	with open(csv_log_base_path + power0_logfile_name, 'w+') as f:
		writer = csv.writer(f)
		writer.writerow(sample_time_header + power0_header)
	# temp0
	with open(csv_log_base_path + temp0_logfile_name, 'w+') as f:
		writer = csv.writer(f)
		writer.writerow(sample_time_header + temp0_header)
	# temp1
	with open(csv_log_base_path + temp1_logfile_name, 'w+') as f:
		writer = csv.writer(f)
		writer.writerow(sample_time_header + temp1_header)
	# press0
	with open(csv_log_base_path + press0_logfile_name, 'w+') as f:
		writer = csv.writer(f)
		writer.writerow(sample_time_header + press0_header)
	# press1
	with open(csv_log_base_path + press1_logfile_name, 'w+') as f:
		writer = csv.writer(f)
		writer.writerow(sample_time_header + press1_header)
	# humid0
	with open(csv_log_base_path + humid0_logfile_name, 'w+') as f:
		writer = csv.writer(f)
		writer.writerow(sample_time_header + humid0_header)
	# arm0
	with open(csv_log_base_path + arm0_logfile_name, 'w+') as f:
		writer = csv.writer(f)
		writer.writerow(sample_time_header + arm0_header)

###########################
# "Main"
###########################

# i2c bus object
bus = smbus.SMBus(1)

# i2c logger object
i2c_logger = logger.logger("i2c_logger", logFileName="{}{}_{}.log".format(i2c_log_base_path, i2c_log_file_base, log_file_index))

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

# loop counter
loop_index = 0

# GPIO output values
dbg_led0_value 	= 0x0
wdt_pet_value 	= 0x0

# starting relative time stamp
t_start_rel = time.time()

# main logging loop
while(1):
	power0_data = None
	temp0_data 	= None
	temp1_data 	= None
	press0_data = None
	press1_data = None
	humid0_data = None
	arm0_data 	= None

	# get power0 sensor data
	while (power0.conversionNotValid()):
		if (printing_enabled):
			print "Power0 CONVERSION IS NOT VALID\n"
		i2c_logger.log.warning("Power0 CONVERSION IS NOT VALID")
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

	# get internal BCM ARM0 sensor data
	arm0_temp_c 		= subprocess.check_output(["vcgencmd", "measure_temp"]).split("\n")[0][5:][:-2]
	arm0_temp_f 		= float(arm0_temp_c) * (9.0/5.0) + 32
	arm0_core_volt 		= subprocess.check_output(["vcgencmd", "measure_volts", "core"]).split("\n")[0][5:][:-1]
	arm0_sdramc_volt 	= subprocess.check_output(["vcgencmd", "measure_volts", "sdram_c"]).split("\n")[0][5:][:-1]
	arm0_sdrami_volt 	= subprocess.check_output(["vcgencmd", "measure_volts", "sdram_i"]).split("\n")[0][5:][:-1]
	arm0_sdramp_volt 	= subprocess.check_output(["vcgencmd", "measure_volts", "sdram_p"]).split("\n")[0][5:][:-1]
	arm0_data 			= [ "{:+08.3f}".format(float(arm0_temp_c)),
							"{:+08.3f}".format(arm0_temp_f),
							"{:07.3f}".format(float(arm0_core_volt)),
							"{:07.3f}".format(float(arm0_sdramc_volt)),
							"{:07.3f}".format(float(arm0_sdrami_volt)),
							"{:07.3f}".format(float(arm0_sdramp_volt))]

	#end of loop epoch time
	t_loop_end_epoch = time.time()
	# end of loop relative time stamp
	t_loop_end_rel = t_loop_end_epoch - t_start_rel
	# loop index and time data
	sample_time_data = [loop_index, t_loop_end_rel, t_loop_end_epoch]
	
	# write all data to log files or print results
	if (logging_enabled):
		all_data = power0_data + temp0_data + temp1_data + press0_data + press1_data + humid0_data + arm0_data
		# log all data
		with open(csv_log_base_path + csv_logfile_name, 'a+') as f:
			writer = csv.writer(f)
			writer.writerow(sample_time_data + all_data)
		# power0
		with open(csv_log_base_path + power0_logfile_name, 'a+') as f:
			writer = csv.writer(f)
			writer.writerow(sample_time_data + power0_data)
		# temp0
		with open(csv_log_base_path + temp0_logfile_name, 'a+') as f:
			writer = csv.writer(f)
			writer.writerow(sample_time_data + temp0_data)
		# temp1
		with open(csv_log_base_path + temp1_logfile_name, 'a+') as f:
			writer = csv.writer(f)
			writer.writerow(sample_time_data + temp1_data)
		# press0
		with open(csv_log_base_path + press0_logfile_name, 'a+') as f:
			writer = csv.writer(f)
			writer.writerow(sample_time_data + press0_data)
		# press1
		with open(csv_log_base_path + press1_logfile_name, 'a+') as f:
			writer = csv.writer(f)
			writer.writerow(sample_time_data + press1_data)
		# humid0
		with open(csv_log_base_path + humid0_logfile_name, 'a+') as f:
			writer = csv.writer(f)
			writer.writerow(sample_time_data + humid0_data)
		# arm0
		with open(csv_log_base_path + arm0_logfile_name, 'a+') as f:
			writer = csv.writer(f)
			writer.writerow(sample_time_data + arm0_data)

	elif (printing_enabled):
		print sample_time_header
		print sample_time_data
		print power0_header
		print power0_data
		print temp0_header
		print temp0_data
		print temp1_header
		print temp1_data
		print press0_header
		print press0_data
		print press1_header
		print press1_data
		print humid0_header
		print humid0_data
		print arm0_header
		print arm0_data
		print "\n"

	# delay between samples (want a sample period of ~1second)
	time.sleep(0.78)

	# toggle the DGB0 LED to show script is still running
	dbg_led0_value = dbg_led0_value ^ 0x1
	GPIO.output(dbg_led0, dbg_led0_value)
	# "pet" (aka toggle) the hardware WDT
	wdt_pet_value = wdt_pet_value ^ 0x1
	GPIO.output(wdt_pet, wdt_pet_value)

	# increment loop counter
	loop_index = loop_index + 1

sys.exit(1)
