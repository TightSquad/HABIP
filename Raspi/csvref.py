#!/usr/bin/env python
#TODO add relative timestamp
import time
import csv

# import function for single wire interface temperature sensor. 
from w1 import grab_temp
# import function for i2c temperature sensor. 
from i2ctemp import i2cgrabTemp 

# Some helpful information for working with csv files. 
# 'a' ---- Append
# 'wb' ---- Write
# 'r' ---- Read

"""
setupCSV 
Function to create the individual CSV file

=== Inputs ===
--- sensor_index --- 
	An integer that will coordinate to the user-defined sensor number
	Ex: The first w1 sensor could have sensor_index = 0

--- sensor_type ---
	A string coordinating to the type of sensor that the csv file will grab data for. 
	Currently supports
		w1-temp
		i2c-temp
=== Outputs ===
--- File ---
	Creates file with name sensor_type+sensor_index+.csv
	Creates Header:
		Temperature(C) | Temperature(F) | Timestamp
	Grabs info from corresponding sensor and writes one row.
"""
def setupCSV(sensor_index,sensor_type='w1-temp'):
	if sensor_type == 'w1-temp':
		filename = 'w1Sensor'+repr(sensor_index)+'.csv'
	elif sensor_type == 'i2c-temp':
		filename = 'i2cSensor'+repr(sensor_index)+'.csv'
	with open(filename, 'wb') as csvfile:
		logWritingHandle = csv.writer(csvfile, delimiter=',',
								quotechar='|', quoting=csv.QUOTE_MINIMAL)
		if sensor_type == 'w1-temp':
			temp_c,temp_f,timestamp=grab_temp(sensor_index=sensor_index)
		elif sensor_type == 'i2c-temp':
			temp_c,temp_f,timestamp=i2cgrabTemp()
		logWritingHandle.writerow(['Temperature(C)'] + ['Temperature(F)'] + ['Timestamp'])
		logWritingHandle.writerow([temp_c] + [temp_f] + [timestamp])

"""
appendCSV 
Function to append to an already created CSV file

=== Inputs ===
--- sensor_index --- 
	An integer that will coordinate to the user-defined sensor number
	Ex: The first w1 sensor could have sensor_index = 0

--- sensor_type ---
	A string coordinating to the type of sensor that the csv file will grab data for. 
	Currently supports
		w1-temp
		i2c-temp
=== Outputs ===
--- File ---
	Appends to file with name sensor_type+sensor_index+.csv
	Grabs info from corresponding sensor and writes one row. 
"""
def appendCSV(sensor_index,sensor_type='w1-temp'):
	if sensor_type == 'w1-temp':
		filename = 'w1Sensor'+repr(sensor_index)+'.csv'
	elif sensor_type == 'i2c-temp':
		filename = 'i2cSensor'+repr(sensor_index)+'.csv'
	with open(filename, 'a') as csvfile:
		logWritingHandle = csv.writer(csvfile, delimiter=',',
								quotechar='|', quoting=csv.QUOTE_MINIMAL) 
		if sensor_type == 'w1-temp':
			temp_c,temp_f,timestamp=grab_temp(sensor_index=sensor_index)
		elif sensor_type == 'i2c-temp':
			temp_c,temp_f,timestamp=i2cgrabTemp()
		logWritingHandle.writerow([temp_c] + [temp_f] + [timestamp])

