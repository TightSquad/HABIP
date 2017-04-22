"""
author: Connor Goldberg
project: High Altitude Balloon Instrumentation Platform
description: The main executable
"""

import common
import dataManager
import groundComms
import interfaces
import logger

def test(mainInterfaces):
	data = mainInterfaces.gps.get_data()
	while data.lock is None:
		common.msleep(1000)
		data = mainInterfaces.gps.get_data()

	mainInterfaces.habip_osd.update_temp("B0:TB0",-10.7)
	mainInterfaces.habip_osd.update_pres("B0:P0", 1842.2)
	mainInterfaces.habip_osd.update_humid("B1:H", 17.3)
	mainInterfaces.habip_osd.update_speed("MS", -1234.56)
	mainInterfaces.habip_osd.update_accel(x=3023.23, y=-4023.54, z=9711.21)
	mainInterfaces.habip_osd.update_gps(lat=data.lat, lon=data.lon)
	mainInterfaces.habip_osd.update_callsign("W2RIT-11")

	for i in range(0, 50):
		camNum = i%4
		mainInterfaces.cameraMux.selectCamera(camNum)
		mainInterfaces.habip_osd.update_cam_num(camNum)
		common.msleep(5000)

def openInterfaces(mainInterfaces):
	mainInterfaces.openbeacon()
	mainInterfaces.opengpio()
	mainInterfaces.opencameramux()
	mainInterfaces.openhabiposd() # This will also open the uart interface
	mainInterfaces.openspi()
	mainInterfaces.opengps()
	mainInterfaces.opentemperature()
	mainInterfaces.openpressure()
	mainInterfaces.opendaqcs()

def main():
	mainLogger = logger.logger("main")
	mainLogger.log.info("Starting main")

	mainInterfaces = interfaces.interfaces()
	openInterfaces(mainInterfaces)

	mainDataManager = dataManager.dataManager(interfaces=mainInterfaces)

	axLogPath = "/home/pi/axlisten.log"
	ground = groundComms.groundComms(axLogPath=axLogPath, interfaces=mainInterfaces)

	mainInterfaces.gpio.setPinMode(pin=18, mode=mainInterfaces.gpio.OUTPUT) # Status LED

	run = True
	while run:
		mainInterfaces.gpio.toggleOutput(18) # Status LED

		ground.update()
		ground.executeCommands(withDelay=100)

		mainDataManager.update()

		mainInterfaces.daqcs.update()

		mainInterfaces.habip_osd.update_all() # This takes about a second to process
		# common.msleep(1000)

	mainLogger.log.info("main loop terminating")

if __name__ == '__main__':
	main()
