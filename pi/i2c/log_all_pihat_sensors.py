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
temp_logger = logger.logger("i2c_logger")

# create sensor objects
power0 	= powerMonitorINA219(power0_addr, None, bus, i2c_logger)
temp0 	= tempSensorPCT2075(temp0_addr, None, bus, i2c_logger)
temp1 	= tempSensorPCT2075(temp1_addr, None, bus, i2c_logger)
press0 	= pressSensorMS5607(press0_addr, None, bus, i2c_logger) 
press1 	= pressSensorMS5803(press1_addr, None, bus, i2c_logger)
humid0 	= humidSensorSI7021(humid0_addr, None, bus, i2c_logger)

# print header

# while(1):
# 	print temp0.readTempCF()
# 	print temp1.readTempCF()
# 	time.sleep(1)

sys.exit(1)
