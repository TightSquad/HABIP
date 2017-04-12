#!/usr/bin/env python

"""
file: log_photo_video.py
author: Chris Schwab
project: High Altitude Balloon Instrumentation Platform
description: Script to capture 60seconds of video and then 4 photos FOREVER
"""

###########################
# Imports
###########################
# sudo apt-get install python-picamera
import picamera
import sys
import time
import csv
import subprocess
import os
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
# GPIO Pins
###########################
# GPIO pin numbers
dbg_led1 	= 26

# set GPIO pin numbering to match the RasPi board header
GPIO.setmode(GPIO.BCM)

# set GPIOs as outputs
GPIO.setwarnings(False)
GPIO.setup(dbg_led1, GPIO.OUT)

###########################
# Log File Naming
###########################
# NOTE: Use absolute paths since this script will be run from /etc/rc.local on boot!

# script_log
# 	check for already used log names (aka if the RasPi had been previously booted or crashed --> XXXXX_photo_video_logger.log)
# 	start log index at 0
log_file_index = 0
log_file_base = "photo_video_logger"
log_base_path = "/home/pi/habip/photo_video_sw/logs/"
log_files_found = False
# check for all log_file_base files and increment the index to the next unique number
for file in os.listdir(log_base_path):
	if (file[6:].startswith(log_file_base) and file.endswith('.log')):
		log_files_found = True
		number_in_use = int(file[0:5])
		if (number_in_use > log_file_index):
			log_file_index = number_in_use
if (log_files_found):
	log_file_index = log_file_index + 1
# pad index to 5 places
log_file_index = "{:05d}".format(log_file_index)
print "Log file index set to: {}".format(log_file_index)

###########################
# Photo/Video Dirs
###########################
# NOTE: Use absolute paths since this script will be run from /etc/rc.local on boot!
photo_save_file_base = "photo"
photo_save_base_path = "/home/pi/habip/photo_video_sw/photos/"
video_save_file_base = "video"
video_save_base_path = "/home/pi/habip/photo_video_sw/videos/"

# photo_naming / video_naming
# 	check for already used video/photo names (aka if the RasPi had been previously booted or crashed --> video_XXXXX.h264, photo_XXXXX.jpg)
# 	start log index at 0
photo_file_index = 0
photo_files_found = False
# check for all photo_save_file_base files and increment the index to the next unique number
for file in os.listdir(photo_save_base_path):
	if (file.startswith(photo_save_file_base) and file.endswith('.jpg')):
		log_files_found = True
		number_in_use = int(file[-8:][0:4])
		if (number_in_use > photo_file_index):
			photo_file_index = number_in_use
if (photo_files_found):
	photo_file_index = photo_file_index + 1
# pad index to 5 places
photo_file_index = "{:05d}".format(photo_file_index)
print "Photo file index set to: {}".format(photo_file_index)

video_file_index = 0
video_files_found = False
# check for all video_save_file_base files and increment the index to the next unique number
for file in os.listdir(video_save_base_path):
	if (file.startswith(video_save_file_base) and file.endswith('.h264')):
		log_files_found = True
		number_in_use = int(file[-8:][0:4])
		if (number_in_use > video_file_index):
			video_file_index = number_in_use
if (video_files_found):
	video_file_index = video_file_index + 1
# pad index to 5 places
video_file_index = "{:05d}".format(video_file_index)
print "Video file index set to: {}".format(video_file_index)

###########################
# "Main"
###########################

# photo_video logger object
photo_video_logger = logger.logger("photo_video_logger", logFileName="{}{}_{}.log".format(log_base_path, log_file_index, log_file_base))

# camera object
camera = picamera.PiCamera()

# configure camera settings
camera.sharpness 			= 0 						# defualt
camera.contrast 			= 0 						# defualt
camera.brightness 			= 50 						# defualt
camera.saturation 			= 0 						# defualt
camera.ISO 					= 0 						# defualt
camera.video_stabilization 	= True 						# defualt = False
camera.exposure_compensation= 0 						# defualt
camera.exposure_mode 		= 'auto' 					# default
camera.meter_mode 			= 'average' 				# default
camera.awb_mode 			= 'auto' 					# default
camera.image_effect 		= 'none' 					# default
camera.color_effects 		= None 						# default
camera.rotation 			= 0 						# default
camera.hflip 				= False 					# default
camera.vflip 				= False 					# default
camera.crop 				= (0.0, 0.0, 1.0, 1.0) 		# default

camera.led 					= False 					# disable camera LED

# loop counter
loop_index = 0

# GPIO output values
dbg_led1_value 	= 0x0

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
