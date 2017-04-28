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
import habip_osd

PORT = "/dev/ttyAMA0"
# PORT = "/dev/tty.usbserial"
# PORT = "/dev/tty.usbserial-FTF83XB6"

BAUDRATE = 4800
osd = osd232.osd232(port=PORT, baudrate=BAUDRATE)

# if not osd.open():
# 	sys.exit(1)

def main():
	osd.clearScreen()
	osd.resetSettings()

	hab = habip_osd.habip_osd(osd)

	hab.update_temp("B0:TB0",-10.7)
	hab.update_pres("B0:P0", 1842.2)
	hab.update_humid("B1:H", 17.3)
	hab.update_speed("MS", -1234.56)
	hab.update_accel([3023.23,-4023.54,9711.21])
	hab.update_gps(["34.34939N","145.34931E"])
	hab.update_callsign("W2RIT-11")
	hab.update_cam_num(3)	

	osd.connection.close()

if __name__ == "__main__":
	main()
