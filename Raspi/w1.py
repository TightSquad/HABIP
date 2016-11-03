#!/usr/bin/env python
# Code taken from https://cdn-learn.adafruit.com/downloads/pdf/adafruits-raspberry-pi-lesson-11-ds18b20-temperature-sensing.pdf - LG 10/30/16
# Modified for timestamp and formatting - LG 10/30/16 
import os
import glob
import time
degree_sign=u'\N{DEGREE SIGN}'

os.system('modprobe w1-gpio')
os.system('modprobe w1-therm')
device_file = []

base_dir = '/sys/bus/w1/devices/'
#device_folder = glob.glob(base_dir + '28*')[0]
device_folder = glob.glob(base_dir + '28-000008a0dc59')[0]
device_file.append(device_folder + '/w1_slave')

#print 'Device Folder: ' + device_folder + '\n'
#device_folder1 = glob.glob(base_dir + '28*')[0]
device_folder1 = glob.glob(base_dir + '28-000008a2ad2d')[0]
device_file.append(device_folder1 + '/w1_slave')

#print 'Device Folder1: ' + device_folder1 + '\n'

def read_temp_raw(sensor_index):
	f = open(device_file[sensor_index], 'r')
	lines = f.readlines()
	f.close()
	return lines

def read_temp(sensor_index):
	lines = read_temp_raw(sensor_index = sensor_index)
	while lines[0].strip()[-3:] != 'YES':
		time.sleep(0.2)
		lines = read_temp_raw()
	equals_pos = lines[1].find('t=')
	if equals_pos != -1:
		temp_string = lines[1][equals_pos+2:]
		temp_c = float(temp_string) / 1000.0
		temp_f = round((temp_c * 9.0 / 5.0 + 32.0),3)
		timestamp = time.asctime( time.localtime(time.time()) )
		rstring = timestamp + ' --'+repr(sensor_index)+'-- ' + repr(temp_c) + degree_sign +'C'
		rstring = rstring + ' --'+repr(sensor_index)+'-- ' + repr(temp_f) + degree_sign + 'F'
		return rstring 

def grab_temp(sensor_index):
	lines = read_temp_raw(sensor_index = sensor_index)
	while lines[0].strip()[-3:] != 'YES':
		time.sleep(0.2)
		lines = read_temp_raw()
	equals_pos = lines[1].find('t=')
	if equals_pos != -1:
		temp_string = lines[1][equals_pos+2:]
		temp_c = float(temp_string) / 1000.0
		temp_f = round((temp_c * 9.0 / 5.0 + 32.0),3)
		timestamp = time.asctime( time.localtime(time.time()) )
		return temp_c,temp_f,timestamp 


