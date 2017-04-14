"""
author: Connor Goldberg
project: High Altitude Balloon Instrumentation Platform
description: The main executable
"""

import interfaces
import logger

def main():
	mainLogger = logger.logger("main")
	mainLogger.log.info("Starting main")

	mainInterfaces = interfaces.interfaces()
	mainInterfaces.opengpio()
	mainInterfaces.openuart()
	mainInterfaces.openspi()

	

if __name__ == '__main__':
	main()