#!/usr/bin/env python

#imported modules
import serial
import subprocess

# command to read the last two lines of the temp log file
#   We read the last two lines here just in case the file is being written to
#   That way, we read the second to last line and do not have to worry about incomplete lines
get_last_i2c_temp = ['tail', 'i2cSensor2.csv', '--lines', '2']
get_last_w0_temp = ['tail', 'w1Sensor0.csv', '--lines', '2']
get_last_w1_remp = ['tail', 'w1Sensor1.csv', '--lines', '2']

# open serial port
with serial.Serial(port='/dev/ttyAMA0', baudrate=9600, bytesize=serial.EIGHTBITS, parity=serial.PARITY_NONE, stopbits=serial.STOPBITS_ONE) as uart_port:
    # flush ports
    uart_port.flushInput()
    uart_port.flushOutput()
    # main
    while 1:
        # wait for command from MSP (read is blocking)
        msp_cmd = uart_port.read(1)
        # decode command
        if (msp_cmd == 'a'):
            print 'Received command for i2cSensor2 temp...\n'
            # read last two lines of temp log file (data_lines = single string with the two lines)
            data_lines = subprocess.check_output(get_last_i2c_temp)
            # split string at ',' since its a csv --> current temp will be fist entry
            current_temp = data_lines.split(',')[1]
            current_temp = "%07.3f" % float(current_temp)
            print '\tcurrent_temp: %sF\n' % current_temp
            # send temp to MSP
            uart_port.write(current_temp)
        elif (msp_cmd == 's'):
            print 'Received command for w1Sensor0 temp...\n'
            # read last two lines of temp log file (data_lines = single string with the two lines)
            data_lines = subprocess.check_output(get_last_w0_temp)
            # split string at ',' since its a csv --> current temp will be fist entry
            current_temp = data_lines.split(',')[1]
            current_temp = "%07.3f" % float(current_temp)
            print '\tcurrent_temp: %sF\n' % current_temp
            # send temp to MSP
            uart_port.write(current_temp)
        elif (msp_cmd == 'd'):
            print 'Received command for w1Sensor1 temp...\n'
            # read last two lines of temp log file (data_lines = single string with the two lines)
            data_lines = subprocess.check_output(get_last_w1_temp)
            # split string at ',' since its a csv --> current temp will be fist entry
            current_temp = data_lines.split(',')[1]
            current_temp = "%07.3f" % float(current_temp)
            print '\tcurrent_temp: %sF\n' % current_temp
            # send temp to MSP
            uart_port.write(current_temp)
        elif (msp_cmd == 'X'):
            print '\nSomething went terribly wrong...\n'
            exit()