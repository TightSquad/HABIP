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
log_file_base = "photo_video_logger"
log_base_path = "/home/pi/habip/photo_video_sw/logs/"

# 	start log index at 0
log_file_index = 0
log_files_found = False
# check for all log_file_base files and increment the index to the next unique number
for file in os.listdir(log_base_path):
	if (file[6:].startswith(log_file_base) and file.endswith('.log')):
		log_files_found = True
		number_in_use = int(file[0:5])
		if (number_in_use > log_file_index):
			log_file_index = number_in_use
if (log_files_found):
	print "Found log file index up to: {}".format(log_file_index)
	log_file_index = log_file_index + 1
# pad index to 5 places
log_file_index = "{:05d}".format(log_file_index)
print "Log file index set to: {}".format(log_file_index)

###########################
# photo_video logger object
###########################
photo_video_logger = logger.logger("photo_video_logger", logFileName="{}{}_{}.log".format(log_base_path, log_file_index, log_file_base))

###########################
# Photo/Video Dirs
###########################
# NOTE: Use absolute paths since this script will be run from /etc/rc.local on boot!
photo_save_file_base = "photo"
photo_save_base_path = "/home/pi/habip/photo_video_sw/photos/"
video_save_file_base = "video"
video_save_base_path = "/home/pi/habip/photo_video_sw/videos/"

# photo_naming / video_naming
# 	check for already used video/photo names (aka if the RasPi had been previously booted or crashed --> videoXXXXX_DATE_TIME.h264, photoXXXXX_DATE_TIME.jpg)
# start photo index at 0
photo_file_index = 0
photo_files_found = False
# check for all photo_save_file_base files and increment the index to the next unique number
for file in os.listdir(photo_save_base_path):
	if (file.startswith(photo_save_file_base) and file.endswith('.jpeg')):
		photo_files_found = True
		number_in_use = int(file[5:10])
		if (number_in_use > photo_file_index):
			photo_file_index = number_in_use
if (photo_files_found):
	print "Found photo file index up to: {}".format(photo_file_index)
	photo_video_logger.log.warning("Found photo file index up to: {}".format(photo_file_index))
	photo_file_index = photo_file_index + 1
# pad index to 5 places
photo_file_index_padded = "{:05d}".format(photo_file_index)
print "Photo file index set to: {}".format(photo_file_index_padded)
photo_video_logger.log.warning("Photo file index set to: {}".format(photo_file_index_padded))

# start video index at 0
video_file_index = 0
video_files_found = False
# check for all video_save_file_base files and increment the index to the next unique number
for file in os.listdir(video_save_base_path):
	if (file.startswith(video_save_file_base) and file.endswith('.h264')):
		video_files_found = True
		number_in_use = int(file[5:10])
		if (number_in_use > video_file_index):
			video_file_index = number_in_use
if (video_files_found):
	print "Found video file index up to: {}".format(video_file_index)
	photo_video_logger.log.warning("Found video file index up to: {}".format(video_file_index))
	video_file_index = video_file_index + 1
# pad index to 5 places
video_file_index_padded = "{:05d}".format(video_file_index)
print "Video file index set to: {}".format(video_file_index_padded)
photo_video_logger.log.warning("Video file index set to: {}".format(video_file_index_padded))

###########################
# Amount of Photos/Videos
###########################
photo_burst_amount 		= 4			# number of photos to take
video_capture_time 		= 60 		# length of video to capture

###########################
# "Main"
###########################

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
	# capture set amount of photos
	for x in range (0, photo_burst_amount):
		# set save file name: photoXXXX_DATE_TIME.jpeg
		photo_file_index_padded = "{:05d}".format(photo_file_index)
		photo_file_name = photo_save_base_path + photo_save_file_base + photo_file_index_padded + "_" + time.strftime("%Y-%m-%d_%H-%M-%S", time.gmtime()) + ".jpeg"
		
		print "capturing photo..."
		photo_video_logger.log.warning("Capturing photo: {}".format(photo_file_name))
		# capture photo
		camera.capture(photo_file_name, format='jpeg')
		
		# increment phot index number
		photo_file_index = photo_file_index + 1
		
		# toggle the DGB1 LED to show script is still running
		dbg_led1_value = dbg_led1_value ^ 0x1
		GPIO.output(dbg_led1, dbg_led1_value)
		
		# wait 0.5 seconds
		time.sleep(0.5)

	# record video
	# set save file name: videoXXXX_DATE_TIME.h264
	video_file_index_padded = "{:05d}".format(video_file_index)
	video_file_name = video_save_base_path + video_save_file_base + video_file_index_padded + "_" + time.strftime("%Y-%m-%d_%H-%M-%S", time.gmtime()) + ".h264"
	
	print "capturing video..."
	photo_video_logger.log.warning("Capturing video: {}".format(video_file_name))
	# record
	camera.start_recording(video_file_name)
	camera.wait_recording(video_capture_time)
	camera.stop_recording()

	# increment video index number
	video_file_index = video_file_index + 1

	# increment loop counter
	loop_index = loop_index + 1
	print "loop index: {}".format(loop_index)
	photo_video_logger.log.warning("loop index: {}".format(loop_index))
	print "elapsed time (s): {}\n".format(time.time() - t_start_rel)
	photo_video_logger.log.warning("elapsed time (s): {}".format(time.time() - t_start_rel))

camera.close()
sys.exit(1)
