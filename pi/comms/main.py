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
import scheduler


def openInterfaces(mainInterfaces):
	mainInterfaces.openbeacon()
	mainInterfaces.opengpio()
	mainInterfaces.openwatchdog()
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


	######## GENERATE FAKE DATA DONT FORGET TO REMOVE THIS #####################
	mainDataManager.genFakeData()
	############################################################################


	axLogPath = "/home/pi/axlisten.log"
	ground = groundComms.groundComms(axLogPath=axLogPath, interfaces=mainInterfaces, dataManager=mainDataManager)

	mainInterfaces.gpio.setPinMode(pin=18, mode=mainInterfaces.gpio.OUTPUT) # Status LED

	# Schedule tasks
	mainScheduler = scheduler.scheduler()
	mainScheduler.schedule(callback=mainDataManager.setTimeSync, frequency=20)
	mainScheduler.schedule(callback=mainDataManager.log, frequency=3)
	mainScheduler.schedule(callback=ground.streamTelemetry, frequency=10)

	run = True
	while run:

		mainInterfaces.watchdog.pet() # Pet the watchdog
		mainInterfaces.gpio.toggleOutput(18) # Status LED

		ground.update()
		ground.executeCommands(withDelay=100)

		mainDataManager.update()
		mainInterfaces.daqcs.update()
		mainScheduler.update()

		mainInterfaces.habip_osd.update_all() # This takes about a second to process

		# for name, board in mainInterfaces.boards.iteritems():
		# 	print "Data for board: {}".format(name)
		# 	board.printAllData()

	mainLogger.log.info("main loop terminating")

if __name__ == '__main__':
	main()
