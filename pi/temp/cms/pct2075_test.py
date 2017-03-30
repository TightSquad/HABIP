#!/usr/bin/env python

import smbus
import time

bus = smbus.SMBus(1)

t_start = time.time()

# sensor registers 
reg_temp = 0x0	# r/w, Temperature register: contains two 8-bit data bytes; to store the measured Temp data.
reg_conf = 0x1	# r  , Configuration register: contains a single 8-bit data byte; to set the device operating condition; default = 0.
reg_thyst = 0x2	# r/w, Hysteresis register: contains two 8-bit data bytes; to store the hysteresis Thys limit; default = 75 C.
reg_tos = 0x3		# r/w, Overtemperature shutdown threshold register: contains two 8-bit data bytes; to store the overtemperature shutdown Tots limit; default = 80 C.
reg_tidle = 0x4	# r/w, Temperature conversion cycle default to 100 ms.

# sensor addresses
temp0_addr = 0x48	#right-side temp sensor
temp1_addr = 0x4A	# left side temp sensor

while(1):
	# read temp value from sensor 0
	bus_val = bus.read_word_data(temp0_addr, reg_temp)
	# convert to binary, zero pad to make sure 16-bits
	bus_val = bin(bus_val)[2:].zfill(16)
	# data recieved as {LS_byte, MS_byte} and rearrange to {MS_byte, LS_byte}
	bus_val_flip = bus_val[8:] + bus_val[:8]
	# shift to discard unused 5 LSbits
	bus_val_shifted = bus_val_flip[:11]
	# convert shifter value to celcius (value * 0.125)
	temp_c = int(bus_val_shifted, 2) * 0.125
	# convert celcius to fahrenheit
	temp_f = temp_c * (9.0/5.0) + 32

	print "Temp Sensor 0 --> Temp (c): %f" % temp_c
	print "Temp Sensor 0 --> Temp (f): %f" % temp_f

	# read temp value from sensor 1
	bus_val = bus.read_word_data(temp1_addr, reg_temp)
	bus_val = bin(bus_val)[2:].zfill(16)
	bus_val_flip = bus_val[8:] + bus_val[:8]
	bus_val_shifted = bus_val_flip[:11]
	temp_c = int(bus_val_shifted, 2) * 0.125
	temp_f = temp_c * (9.0/5.0) + 32

	print "Temp Sensor 1 --> Temp (c): %f" % temp_c
	print "Temp Sensor 1 --> Temp (f): %f" % temp_f

	print "elapsed time: %f seconds\n" % (time.time() - t_start)
	time.sleep(1)
