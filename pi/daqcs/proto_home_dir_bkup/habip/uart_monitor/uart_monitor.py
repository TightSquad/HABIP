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
import logger

###########################
# Config
###########################
printing_enabled = 0

PORT = "/dev/ttyAMA0"
#BAUDRATE = 115200
BAUDRATE = 9600

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

uart_log_file_base = "uart_logger"
uart_log_base_path = "/home/pi/habip/uart_monitor/logs_uart/"

###########################
# Log File Naming
###########################
# NOTE: Use absolute paths since script will be called froma boot area

# uart_log
# 	check for already used log names (aka if the RasPi had been previously booted or crashed --> XXXXX_uart_logger.log)
# 	start log index at 0
log_file_index = 0
log_files_found = False
# check for all uart_log_file_base files and increment the index to the next unique number
for file in os.listdir(uart_log_base_path):
	if (file[6:].startswith(uart_log_file_base) and file.endswith('.log')):
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

def get_all_sensor_data():
	"""
    inputs:
        none
    outputs:
        list - returns list of all data sequences to send to the host board: ex, {TE0:+101.000}
    """

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

	# dictionary for i2c and w1 combined data
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

	# # build tx_string (sorted alpha-numerically based on CMD name)
	# tx_string = uart.uart.SOT
	# for key, value in sorted(combined_tx_data.iteritems()):
	# 	tx_string = tx_string + str(key) + ':' + str(value) + ';'
	# tx_string = tx_string[:-1] + uart.uart.EOT 		# remove last ';' and at END character

	# build tx_string_list
	tx_string_list = []
	for key, value in sorted(combined_tx_data.iteritems()):
		tx_string_list = tx_string_list + ['{' + key + ':' + value + '}']

	if (printing_enabled):
		print tx_string_list
	return tx_string_list

###########################
# MAIN
###########################

# uart logger object
uart_logger = logger.logger("uart_logger", logFileName="{}{}_{}.log".format(uart_log_base_path, log_file_index, uart_log_file_base), useLogsDirectory=False)

# open UART port
uart_logger.log.info("Opening UART comm at {} baud".format(BAUDRATE))
uart_logger.log.info("Opening UART comm on port {}".format(PORT))

con = uart.uart(port=PORT, baudrate=BAUDRATE)
con.open()

uart_logger.log.info("UART port is open!")

# main while loop
while (1):
	# read until end of command character is Rx'd
	rx_string = con.readUntil(uart.uart.EOT)
	if (printing_enabled):
		print "Received: " + rx_string
	uart_logger.log.info("Received: {}".format(rx_string))

	# if requesting all sensor data
	if (rx_string == '{01}'):
		if (printing_enabled):
			print "HOST is requesting ALL sensor data..."
		uart_logger.log.info("HOST is requesting ALL sensor data...")
		tx_string_list = get_all_sensor_data()
		for item in tx_string_list:
			con.sendRaw(item)

	# else if sending an epoch time sync (ex: {06:1491592543})
	elif (rx_string.startswith('{06:') and rx_string.endswith('}')):
		if (printing_enabled):
			print "HOST is sending an epoch time sync..."
		uart_logger.log.info("HOST is sending an epoch time sync...")

		epoch_time_rxd = int(rx_string[4:14])
		set_epoch_command = ['sudo', 'date', '--set', '@{}'.format(epoch_time_rxd)]
		set_epoch_status = subprocess.check_output(set_epoch_command)

	# else if recieved a ready status from the HOST
	elif (rx_string == '{RDY?}'):
		if (printing_enabled):
			print "HOST is sending a READY request..."
		uart_logger.log.info("HOST is sending a READY request...")
		con.sendRaw('{RDY}')

	else:
		if (printing_enabled):
			print "Recieved bad data: " + rx_string
		uart_logger.log.info("Recieved bad data: " + rx_string)

con.close()

sys.exit(1)
