#!/usr/bin/env python

import time
import os
# User python scripts
import csvref 
from csvref import setupCSV
from csvref import appendCSV

#print '\n Creating CSV files \n'
setupCSV(sensor_index=0)
setupCSV(sensor_index=1)
setupCSV(sensor_index=2,sensor_type='i2c-temp')
time.sleep(1)
#print '\n Currently acquiring temperature at 1 second intervals \n'
while True:
	appendCSV(sensor_index=0)
	appendCSV(sensor_index=1)
	appendCSV(sensor_index=2,sensor_type='i2c-temp')
	time.sleep(1)


