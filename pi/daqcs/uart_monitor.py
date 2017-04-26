#!/usr/bin/env python

"""
file: uart_monitor.py
author: Chris Schwab
project: High Altitude Balloon Instrumentation Platform
description: Script to monitor the UART communication (Tx sensor data, Rx epoch time)
"""

###########################
# Imports
###########################
import uart
import os
import subprocess
import time

###########################
# Config
###########################
PORT = "/dev/ttyAMA0"
BAUDRATE = 115200

i2c_csv_file_base 	= "i2c_sensors_logged.csv"
i2c_csv_base_path 	= "/home/pi/habip/sensors_sw/data_i2c"

w1_csv_file_base 	= "w1_sensors_logged.csv"
w1_csv_base_path 	= "/home/pi/habip/sensors_sw/data_w1"

i2c_cmd_to_header = {	'TD0'	: 'ARM0 Core Temp (C)',
						'TB0'	: 'Temp0 Temp (C)',
						'TB1'	: 'Temp1 Temp (C)',
						'P0'	: 'Press0 Press (mBar)',
						'P1'	: 'Press1 Press (mBar)',
						'H'		: 'Humid0 RH (%)',
						'V'		: 'Power0 Bus Voltage (V)',
						'C'		: 'Power0 Current (mA)'
					}

w1_cmd_to_header = 	{	'TE0'	: 'w1_0 Temp (C)',
						'TE1'	: 'w1_1 Temp (C)'
					}


###########################
# Functions
###########################

def find_last_csv_log(absolute_csv_base_path, csv_log_file_base):
	"""
    inputs:
        none
    outputs:
        string - returns absolute path of the latest csv data log (based on incrementing filename index)
    """
	csv_filename = None

	csv_file_index = 0
	csv_files_found = False
	# check for csv files and find most recent file index
	for file in os.listdir(absolute_csv_base_path):
		if (file.endswith(csv_log_file_base)):
			log_files_found = True
			index_in_use = int(file[0:5])
			if (index_in_use > csv_file_index):
				csv_file_index = index_in_use
	# if files are found, the highest index (most recent) is chosen
	if (log_files_found):
		csv_filename = absolute_csv_base_path + "/{:05d}".format(csv_file_index) + "_" + csv_log_file_base

	return csv_filename

def get_latest_sensor_data(absolute_filename):
	"""
    inputs:
        none
    outputs:
        list - returns list of data from the second-to-last i2c csv data log line (split at the ',')
    """

	tail_csv_file = ['tail', absolute_filename, '--lines', '2']
	last_two_lines = subprocess.check_output(tail_csv_file)
	last_two_lines = last_two_lines.split('\r\n')
	second_to_last_line = last_two_lines[0]

	return second_to_last_line.split(',')

def get_csv_log_header(absolute_filename):
	"""
    inputs:
        none
    outputs:
        list - returns list of header data from absolute_filename
    """

	head_csv_file = ['head', absolute_filename, '--lines', '1']
	header_string = subprocess.check_output(head_csv_file)

	return header_string.split(',')


# def send(con):
# 	con.sendRaw("Testing!!"+uart.EOT)

def recv(con):
	data = con.readUntil(uart.uart.EOT)
	return data


###########################
# MAIN
###########################

# dictionaries to hold the column index of the required send data
i2c_cmd_to_header_index = {	'TD0'	: None,
							'TB0'	: None,
							'TB1'	: None,
							'P0'	: None,
							'P1'	: None,
							'H'		: None,
							'V'		: None,
							'C'		: None
						  }

w1_cmd_to_header_index 	= {	'TE0'	: None,
							'TE1'	: None
						  }

combined_tx_data 		= {	'TD0'	: None,
							'TB0'	: None,
							'TB1'	: None,
							'P0'	: None,
							'P1'	: None,
							'H'		: None,
							'V'		: None,
							'C'		: None,
							'TE0'	: None,
							'TE1'	: None
						  }

# open UART port
con = uart.uart(port=PORT, baudrate=BAUDRATE)
con.open()

while (1):
# 	rx_string = recv(con)

# 	if (rx_string == '{01}'):
# 		print "Received 01"
# 	elif (rx_string == '{05}'):
# 		print "Received 01"
# 	elif (rx_string == '{06}'):
# 		print "Received 01"
# 	else:
# 		print "Recieved bad data: " + rx_string
	
	# find latest csv data logs
	i2c_csv_filename 	= find_last_csv_log(i2c_csv_base_path, i2c_csv_file_base)
	w1_csv_filename 	= find_last_csv_log(w1_csv_base_path, w1_csv_file_base)

	# find headers from those files (this should not change, BUT adding this functionality in so that if the log file order does change this script is not obsolete)
	i2c_csv_header 		= get_csv_log_header(i2c_csv_filename)
	w1_csv_header 		= get_csv_log_header(w1_csv_filename)

	# set column indices of the log files for sensor data to be Tx'd (loop through dictionaries alpha-numerically)
	for key, value in sorted(i2c_cmd_to_header.iteritems()):
		i2c_cmd_to_header_index[key] = i2c_csv_header.index(value)
	for key, value in sorted(w1_cmd_to_header.iteritems()):
		w1_cmd_to_header_index[key] = w1_csv_header.index(value)

	# grab latest data from those logs
	i2c_sensor_data 	= get_latest_sensor_data(i2c_csv_filename)
	w1_sensor_data 		= get_latest_sensor_data(w1_csv_filename)

	# build combined_tx_data dict
	for key, value in sorted(i2c_cmd_to_header_index.iteritems()):
		# if humidity, remove last decimal place to match spec
		if (key == 'H'):
			combined_tx_data[key] = i2c_sensor_data[value][:-1]
		# if voltage, remove first digit to match spec
		elif (key == 'V'):
			combined_tx_data[key] = i2c_sensor_data[value][1:]
		else:
			combined_tx_data[key] = i2c_sensor_data[value]
	for key, value in sorted(w1_cmd_to_header_index.iteritems()):
		combined_tx_data[key] = w1_sensor_data[value]

	# build tx_string (sorted alpha-numerically based on CMD name)
	tx_string = uart.uart.SOT
	for key, value in sorted(combined_tx_data.iteritems()):
		tx_string = tx_string + str(key) + ':' + str(value) + ';'
	tx_string = tx_string[:-1] + uart.uart.EOT 		# remove last ';' and at END character

	print tx_string

	time.sleep(5)

# con.close()

sys.exit(1)
