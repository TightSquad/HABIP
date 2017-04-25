#!/usr/bin/env python

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

###########################
# GPIO Pins
###########################
# GPIO pin numbers
#dbg_led0 	= 20
wdt_pet 	= 21

# set GPIO pin numbering to match the RasPi board header
GPIO.setmode(GPIO.BCM)

# set GPIOs as outputs and drive low
GPIO.setwarnings(False)			# disable printed warnings
#GPIO.setup(dbg_led0, GPIO.OUT) 	# set as output
GPIO.setup(wdt_pet, GPIO.OUT)

#GPIO.output(dbg_led0, 0x0) 		# drive low
GPIO.output(wdt_pet, 0x0)

# GPIO output values
#dbg_led0_value 	= 0x0
wdt_pet_value 	= 0x0

# toggle the DGB0 LED to show script is still running
#dbg_led0_value = dbg_led0_value ^ 0x1
#GPIO.output(dbg_led0, dbg_led0_value)

while(1):
	# "pet" (aka toggle) the hardware WDT
	wdt_pet_value = wdt_pet_value ^ 0x1
	GPIO.output(wdt_pet, wdt_pet_value)
	time.sleep(30)

# increment loop counter
#loop_index = loop_index + 1

sys.exit(1)
