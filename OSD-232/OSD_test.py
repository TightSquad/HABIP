#!/usr/bin/env python

"""
title: OSD Test
author: Connor Goldberg
project: High Altitude Balloon Instrumentation Platform
description: Tests the OSD API
"""

import OSD232

PORT = "/dev/tty.usbserial-FTF83XB6"
BAUDRATE = 4800

osd = OSD232.OSD232(port=PORT,baudrate=BAUDRATE)
osd.open()

osd.clearScreen()
osd.resetSettings()

osd.setPosition(row=1, column=8)
osd.sendRaw("{} The HABIP {}".format(osd.symbol["satellite"], osd.symbol["heart"]))

osd.setPosition(row=11)
osd.sendRaw("KC3HUO")

# temp = 35.0
# alt = 10000
# pressure = 1.0
# north = 43.0848
# west = 77.6793

# OSD232.msleep(10000)

# for x in range(0,8):
# 	counter = 8

# 	osd.setPosition(row=counter)
# 	osd.sendRaw("Temp: {}C".format(str(temp)))
# 	temp-=3
# 	counter+=1

# 	osd.setPosition(row=counter)
# 	osd.sendRaw("Alt: {}ft".format(str(alt)))
# 	alt+=10000
# 	counter+=1

# 	osd.setPosition(row=counter)
# 	osd.sendRaw("Pressure: {}B".format(str(pressure)))
# 	pressure -= 0.1
# 	counter+=1

# 	osd.setPosition(row=counter)
# 	osd.sendRaw("GPS: N{} W{}".format(north,west))
# 	north += 0.034
# 	west += 0.219
# 	counter+=1

# 	OSD232.msleep(5000)

osd.close()