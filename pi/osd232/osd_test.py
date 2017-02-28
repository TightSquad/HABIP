#!/usr/bin/env python

"""
title: OSD Test
author: Connor Goldberg
project: High Altitude Balloon Instrumentation Platform
description: Tests the OSD API
"""

import sys

import common
import osd232

# PORT = "/dev/ttyAMA0"
# PORT = "/dev/tty.usbserial"
PORT = "/dev/tty.usbserial-FTF83XB6"

BAUDRATE = 4800
osd = osd232.osd232(port=PORT, baudrate=BAUDRATE)

# if not osd.open():
# 	sys.exit(1)

def main():

	osd.clearScreen()
	osd.resetSettings()

	osd.setPosition(row=1, column=8)
	common.msleep(100)
	osd.display("{} The HABIP {}".format(osd.symbol["satellite"], osd.symbol["heart"]))
	common.msleep(100)

	osd.setPosition(row=11)
	common.msleep(100)
	osd.display("KC3HUO")
	common.msleep(100)

	fakeData()

	osd.connection.close()

def fakeData():
	temp = 35.0
	alt = 10000
	pressure = 1.0
	north = 43.0848
	west = 77.6793

	common.msleep(5000)

	for x in range(0,20):
		counter = 6

		osd.setPosition(row=counter)
		common.msleep(100)
		osd.display("Temp: {}C".format(str(temp)))
		common.msleep(100)
		temp-=3
		counter+=1

		osd.setPosition(row=counter)
		common.msleep(100)
		osd.display("Alt: {}ft".format(str(alt)))
		common.msleep(100)
		alt+=10000
		counter+=1

		osd.setPosition(row=counter)
		common.msleep(100)
		osd.display("Pressure: {}B".format(str(pressure)))
		common.msleep(100)
		pressure -= 0.1
		counter+=1

		osd.setPosition(row=counter)
		common.msleep(100)
		osd.display("GPS: N{} W{}".format(north,west))
		common.msleep(100)
		north += 0.034
		west += 0.219
		counter+=1

		common.msleep(5000)

if __name__ == "__main__":
	main()