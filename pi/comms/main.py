"""
author: Connor Goldberg
project: High Altitude Balloon Instrumentation Platform
description: The main executable
"""

import common
import interfaces
import logger
import groundComms

def main():
	mainLogger = logger.logger("main")
	mainLogger.log.info("Starting main")

	mainInterfaces = interfaces.interfaces()
	mainInterfaces.openbeacon()
	mainInterfaces.opengpio()
	mainInterfaces.opencameramux()
	# mainInterfaces.openosd232() # This will open the uart interface
	mainInterfaces.openspi()

	axLogPath = "/home/pi/axlisten.log"

	ground = groundComms.groundComms(axLogPath=axLogPath, interfaces=mainInterfaces)

	run = True
	while run:

		ground.update()
		
		# ground.executeCommands(withDelay=100)


		common.msleep(1000)

	mainLogger.log.info("main loop terminating")

if __name__ == '__main__':
	main()
