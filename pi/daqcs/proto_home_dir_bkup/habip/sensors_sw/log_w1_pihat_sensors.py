#!/usr/bin/env python

"""
file: log_w1_pihat_sensors.py
author: Chris Schwab
project: High Altitude Balloon Instrumentation Platform
description: Script to log all 1-wire PiHat sensors to csv as well as "pet" the hardware WDT
"""

###########################
# Imports
###########################
# sudo apt-get install python-smbus
import smbus
import sys
import time
import csv
import subprocess
import os
import glob
import RPi.GPIO as GPIO

# Custom logger class
import logger

###########################
# LOGGING / PRINTING CONFIG
###########################
# enable printing to terminal
printing_enabled = 0
# enable csv logging
logging_enabled = 1

###########################
# Initialize 1-wire sensors
###########################
subprocess.call('modprobe w1-gpio', shell=True)
subprocess.call('modprobe w1-therm', shell=True)
w1_base_dir = '/sys/bus/w1/devices/'
w1_sensor_base_dirs = glob.glob(w1_base_dir + '28*')
w1_sensors = [element + '/w1_slave' for element in w1_sensor_base_dirs]
num_w1_sensors = len(w1_sensors)
if (num_w1_sensors == 0):
	print "No 1-Wire Sensors detected..."

w1_header = []
# build 1-wire header
for i in range (0, num_w1_sensors):
	w1_header.append("w1_{} Temp (C)".format(i))
	w1_header.append("w1_{} Temp (F)".format(i))

###########################
# Log File Naming
###########################
# NOTE: Use absolute paths since script will be called froma boot area

# w1_bus_log
# 	check for already used log names (aka if the RasPi had been previously booted or crashed --> XXXXX_w1_bus_logger.log)
# 	start log index at 0
log_file_index = 0
w1_log_file_base = "w1_bus_logger"
w1_log_base_path = "/home/pi/habip/sensors_sw/logs_w1/"
log_files_found = False
# check for all w1_log_file_base files and increment the index to the next unique number
for file in os.listdir(w1_log_base_path):
	if (file[6:].startswith(w1_log_file_base) and file.endswith('.log')):
		log_files_found = True
		number_in_use = int(file[0:5])
		if (number_in_use > log_file_index):
			log_file_index = number_in_use
if (log_files_found):
	log_file_index = log_file_index + 1
# pad index to 5 places
log_file_index = "{:05d}".format(log_file_index)
print "Log file index set to: {}".format(log_file_index)

# csv data logs
# 	use the unique log_file_index from the w1_log_file search
csv_logfile_name 	= "{}_w1_sensors_logged.csv".format(log_file_index)
sample_time_header 	= ["Sample Index", "Elapsed Time (s)", "Sample Time Delta (s)", "Epoch Time (s)", "Date Time Stamp"]
csv_logfile_header 	= sample_time_header + w1_header

csv_log_base_path 	= "/home/pi/habip/sensors_sw/data_w1/"

# 1-wire sensors headers and sensor log file names
w1_logfile_name 	= "{}_w1_sensors_logged.csv".format(log_file_index)

# 	create log files
if (logging_enabled):
	# w1
	with open(csv_log_base_path + w1_logfile_name, 'w+') as f:
		writer = csv.writer(f)
		writer.writerow(sample_time_header + w1_header)

###########################
# "Main"
###########################

# w1 logger object
w1_logger = logger.logger("w1_logger", logFileName="{}{}_{}.log".format(w1_log_base_path, log_file_index, w1_log_file_base))

# loop counter
loop_index = 0

# starting relative time stamp
t_start_rel = time.time()

# previous time
prev_epoch_time = t_start_rel

# If there are no w1 sensors, exit
if (num_w1_sensors == 0):
	w1_logger.log.warning("NO W1 SENSORS DETECTED!!!")
	sys.exit(1)
# ELse, main logging loop
else:
	while(1):
		w1_data = []

		# get all 1-wire sensor data
		for w1_sensor in w1_sensors:
			# read w1_sensor data
			catdata = subprocess.Popen(['cat', w1_sensor], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
			out,err = catdata.communicate()
			out_decode = out.decode('utf-8')
			lines = out_decode.split('\n')
			
			# check to make sure data is valid
			if lines[0].strip()[-3:] != 'YES':
				print "bad data 0"

			# collect the temp data
			equals_pos = lines[1].find('t=')
			if equals_pos != -1:
				temp_string = lines[1][equals_pos+2:]
				temp_c = float(temp_string) / 1000.0
				temp_f = temp_c * 9.0 / 5.0 + 32
				w1_data.append("{:+08.3f}".format(temp_c))
				w1_data.append("{:+08.3f}".format(temp_f))
			else:
				print "bad data 1"

		# end of loop epoch time
		t_loop_end_epoch = time.time()
		# sample delta time
		sample_delta_time = t_loop_end_epoch - prev_epoch_time
		prev_epoch_time = t_loop_end_epoch
		# end of loop relative time stamp
		t_loop_end_rel = t_loop_end_epoch - t_start_rel
		# date time stamp
		date_time_stamp = time.strftime("%Y-%m-%d_%H-%M-%S", time.gmtime())
		# loop index and time data
		sample_time_data = [loop_index, t_loop_end_rel, sample_delta_time, t_loop_end_epoch, date_time_stamp]

		# write all data to log files or print results
		if (logging_enabled):
			# w1
			with open(csv_log_base_path + w1_logfile_name, 'a+') as f:
				writer = csv.writer(f)
				writer.writerow(sample_time_data + w1_data)

		if (printing_enabled):
			print sample_time_header
			print sample_time_data
			print w1_header
			print w1_data
			print "\n"

		# increment loop counter
		loop_index = loop_index + 1

	sys.exit(1)
