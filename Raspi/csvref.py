#!/usr/bin/env python
#TODO add relative timestamp
import time
import csv

#import w1
from w1 import grab_temp
from i2ctemp import i2cgrabTemp 
# 'a' ---- Append
# 'wb' ---- Write
# 'r' ---- Read
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

