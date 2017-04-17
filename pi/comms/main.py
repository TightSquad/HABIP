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
	mainInterfaces.opengpio()
	mainInterfaces.opencameramux()
	mainInterfaces.openosd232() # This will open the uart interface
	mainInterfaces.openspi()

	ground = groundComms.groundComms(axLogPath="/home/pi/axlisten.log", interfaces=mainInterfaces)

	run = True

	while run:

		ground.update()
		ground.executeCommands(withDelay=100)


		common.msleep(1000)

	

if __name__ == '__main__':
	main()